"""Bounded, contained research artifact reads; records never execute commands."""

import hashlib
import json
import re
from dataclasses import dataclass

from core.paths import contained
from core.schema import ContractError


@dataclass(frozen=True)
class ResearchLimits:
    file_bytes: int = 8 * 1024 * 1024
    aggregate_bytes: int = 32 * 1024 * 1024
    records: int = 100000
    output_bytes: int = 2 * 1024 * 1024

    def __post_init__(self):
        if any(type(value) is not int or value <= 0 for value in vars(self).values()):
            raise ContractError("research limits must be trusted positive integers")


def unique_object(pairs):
    record = {}
    for key, value in pairs:
        if key in record:
            raise ContractError(f"duplicate JSON field: {key}")
        record[key] = value
    return record


def finite_number(value, label="number"):
    import math
    if type(value) not in {int, float} or not math.isfinite(value):
        raise ContractError(f"{label} must be a finite number")
    return value


def unique_ids(values, label):
    if any(not isinstance(value, str) or not value.strip() for value in values) or len(set(values)) != len(values):
        raise ContractError(f"{label} requires unique nonempty IDs")
    return set(values)


def receipt_outputs(run, task_id, inputs):
    """Resolve terminal receipt bindings without treating its claims as authentication."""
    if (not isinstance(run, dict) or run.get("task_id") != task_id
            or run.get("status") not in {"completed-unreviewed", "failed"}):
        raise ContractError("readout requires structured task-matching terminal run receipts")
    def reference(value):
        if (not isinstance(value, dict) or set(value) != {"path", "sha256"}
                or not isinstance(value["path"], str) or not value["path"]
                or not isinstance(value["sha256"], str) or not re.fullmatch(r"[a-f0-9]{64}", value["sha256"])):
            raise ContractError("run artifact requires exact path/hash binding")
        return value["path"], value["sha256"]
    if not isinstance(run.get("inputs"), list) or not {reference(ref) for ref in inputs} <= {reference(ref) for ref in run["inputs"]}:
        raise ContractError("run does not bind the actual readout inputs")
    if not isinstance(run.get("outputs"), list):
        raise ContractError("terminal run must retain its actual output bindings")
    result = set()
    paths = set()
    for row in run["outputs"]:
        if (not isinstance(row, dict) or set(row) != {"reference", "kind", "count"}
                or row["kind"] not in {"predictions", "metrics", "statistics", "oracle", "readout"}
                or type(row["count"]) is not int or row["count"] < 0):
            raise ContractError("run output requires canonical kind/reference/count fields")
        path, digest = reference(row["reference"])
        if path in paths:
            raise ContractError("run output paths must be unique")
        paths.add(path)
        result.add((row["kind"], path, digest))
    return result


class ArtifactReader:
    """One trusted budget shared across every input of an artifact graph."""

    def __init__(self, root, limits=None):
        self.root = root
        self.limits = limits or ResearchLimits()
        self.bytes_read = 0
        self.records_read = 0

    def _preflight(self, source):
        """Count records and array members lexically before JSON allocation."""
        stack = []
        at = 0
        previous = ""
        while at < len(source):
            char = source[at]
            if char.isspace():
                at += 1
                continue
            array_value = bool(stack and stack[-1] == "[" and previous in {"[", ","})
            if char in "{[":
                if char == "{" or array_value:
                    self.count(1)
                stack.append(char)
                if len(stack) > 64:
                    raise ContractError("research JSON nesting exceeds trusted depth limit")
                previous = char
                at += 1
                continue
            if array_value and char != "]":
                self.count(1)
            if char == '"':
                at += 1
                while at < len(source):
                    if source[at] == "\\":
                        at += 2
                    elif source[at] == '"':
                        at += 1
                        break
                    else:
                        at += 1
                previous = "value"
                continue
            if char in "}]":
                if not stack or stack[-1] != {"}": "{", "]": "["}[char]:
                    raise ContractError("research JSON container mismatch")
                stack.pop()
                previous = "value"
            elif char in ",:":
                previous = char
            else:
                while at + 1 < len(source) and source[at + 1] not in " \r\n\t,]}":
                    at += 1
                previous = "value"
            at += 1
        if stack:
            raise ContractError("incomplete research JSON containers")

    def read(self, relative):
        path = contained(self.root, relative)
        size = path.stat().st_size
        if size > self.limits.file_bytes:
            raise ContractError("research input exceeds per-file byte limit before allocation")
        if size + self.bytes_read > self.limits.aggregate_bytes:
            raise ContractError("research inputs exceed aggregate byte limit before allocation")
        chunks = []
        with path.open("rb") as stream:
            total = 0
            while block := stream.read(min(65536, self.limits.file_bytes - total + 1)):
                total += len(block)
                if total > self.limits.file_bytes or self.bytes_read + total > self.limits.aggregate_bytes:
                    raise ContractError("research input grew beyond trusted byte limits")
                chunks.append(block)
        self.bytes_read += total
        data = b"".join(chunks)
        return data

    def json(self, relative):
        return self.parse(self.read(relative))

    def parse(self, data):
        try:
            source = data if isinstance(data, str) else data.decode("utf-8-sig")
            self._preflight(source)
            return json.loads(source, object_pairs_hook=unique_object,
                              parse_constant=lambda value: (_ for _ in ()).throw(ContractError("nonfinite JSON value")),
                              parse_float=lambda value: finite_number(float(value), "JSON number"))
        except (UnicodeError, ValueError, RecursionError) as error:
            raise ContractError(f"invalid bounded research JSON: {error}") from error

    def binding(self, reference):
        if set(reference) != {"path", "sha256"}:
            raise ContractError("artifact binding requires exact path/hash fields")
        data = self.read(reference["path"])
        if hashlib.sha256(data).hexdigest() != reference["sha256"]:
            raise ContractError(f"stale research artifact binding: {reference['path']}")
        return data

    def bound_json(self, reference):
        return self.parse(self.binding(reference))

    def rows(self, reference):
        try:
            source = self.binding(reference).decode("utf-8-sig")
        except UnicodeError as error:
            raise ContractError("canonical rows require UTF-8") from error
        self._preflight(source)
        decoder = json.JSONDecoder(object_pairs_hook=unique_object,
                                   parse_constant=lambda value: (_ for _ in ()).throw(ContractError("nonfinite JSON value")),
                                   parse_float=lambda value: finite_number(float(value), "JSON number"))
        at = re.compile(r"\s*").match(source, 0).end()
        if at >= len(source) or source[at] != "[":
            raise ContractError("canonical research rows must be an array")
        at += 1
        rows = []
        first = True
        try:
            while True:
                at = re.compile(r"\s*").match(source, at).end()
                if at < len(source) and source[at] == "]":
                    at += 1
                    break
                if not first:
                    if at >= len(source) or source[at] != ",":
                        raise ContractError("canonical array separator is missing")
                    at = re.compile(r"\s*").match(source, at + 1).end()
                row, at = decoder.raw_decode(source, at)
                rows.append(row)
                first = False
            if source[at:].strip():
                raise ContractError("canonical array has trailing data")
        except (ValueError, RecursionError) as error:
            raise ContractError(f"invalid bounded canonical row: {error}") from error
        return rows

    def count(self, number):
        if type(number) is not int or number < 0 or self.records_read + number > self.limits.records:
            raise ContractError("research record budget exceeded")
        self.records_read += number

    def output(self, record, *, indent=None, newline=False):
        chunks = []
        total = 0
        encoder = json.JSONEncoder(ensure_ascii=False, allow_nan=False, indent=indent)
        for part in encoder.iterencode(record):
            chunk = part.encode("utf-8")
            total += len(chunk)
            if total > self.limits.output_bytes:
                raise ContractError("research output exceeds trusted byte limit")
            chunks.append(chunk)
        if newline:
            total += 1
            if total > self.limits.output_bytes:
                raise ContractError("research output exceeds trusted byte limit")
            chunks.append(b"\n")
        return b"".join(chunks)
