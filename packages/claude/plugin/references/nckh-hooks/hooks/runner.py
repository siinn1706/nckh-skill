"""Bounded stdin hook runner; no payload command execution, transcript reads or egress."""

import argparse
import importlib
import json
import math
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
if (ROOT / "hooks/_shared").is_dir():
    sys.path.insert(0, str(ROOT / "hooks/_shared"))

from core.hook_policy import MAX_CONTEXT_BYTES, MAX_EVENT_BYTES, evaluate
from core.paths import atomic_json, contained, digest_bytes, digest_record, exclusive_file_lock, no_links
from core.schema import ContractError, validate_record

HOSTS = {"claude", "codex", "cursor", "agy"}


def strict_json(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ContractError("duplicate hook JSON key")
            result[key] = value
        return result
    def reject(value):
        raise ContractError("nonfinite hook JSON")
    def finite_float(value):
        number = float(value)
        if not math.isfinite(number):
            raise ContractError("nonfinite hook JSON number")
        return number
    try:
        value = json.loads(data, object_pairs_hook=unique, parse_constant=reject, parse_float=finite_float)
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ContractError("invalid hook JSON encoding or syntax") from exc
    if not isinstance(value, dict):
        raise ContractError("hook JSON must be an object")
    return value


def load_context(project, reference):
    path = contained(project, reference)
    if not path.is_file() or path.stat().st_size > MAX_CONTEXT_BYTES:
        raise ContractError("bounded controller context unavailable")
    data = path.read_bytes()
    return strict_json(data), digest_bytes(data)


def invoke(host, event_name, payload_bytes, *, project, context_reference):
    if host not in HOSTS:
        raise ContractError("unknown hook host")
    codec = importlib.import_module("hooks.codecs." + host)
    failure = {"schema_version": 1, "decision": "block", "reason_codes": ["hook-input-or-context-invalid"],
               "evidence_class": "deterministic", "native_enforcement": "unverified", "semantic_fidelity": "unverified", "side_effects": "none"}
    try:
        project = no_links(project).resolve()
        if len(payload_bytes) > MAX_EVENT_BYTES:
            raise ContractError("hook event byte limit exceeded")
        payload = strict_json(payload_bytes)
        decoded = codec.decode(payload, event_name)
        if str(project).casefold() not in {str(no_links(root).resolve()).casefold() for root in decoded["reported_roots"]}:
            raise ContractError("hook project identity mismatch")
        paths = []
        for path in decoded["raw_paths"]:
            candidate = Path(path)
            if candidate.is_absolute():
                candidate = no_links(candidate).resolve()
                if not candidate.is_relative_to(project):
                    raise ContractError("hook path escapes selected project")
                path = candidate.relative_to(project).as_posix()
            contained(project, path)
            paths.append(path)
        context, context_hash = load_context(project, context_reference)
        event = validate_record("hook-event", {"schema_version": 1, "phase": decoded["phase"], "host": host,
            "tool": decoded["tool"], "paths": paths, "session_key": decoded["session_key"],
            "task_key": digest_record(context.get("task_id", "unverified")),
            "artifact_sha256": context.get("artifact_sha256", digest_record(None)), "stop_active": decoded["stop_active"]})
        decision = evaluate(event, context, project=project)
        receipt = {"schema_version": 1, "host": host, "phase": event["phase"],
            "event_hash": digest_record(event), "context_hash": context_hash, "artifact_sha256": event["artifact_sha256"],
            "session_key": event["session_key"], "task_key": event["task_key"], **decision,
            "status": "checked-unreviewed", "native_host_response": "unobserved"}
        return codec.encode(event_name, decision), receipt
    except (ContractError, OSError, ValueError, KeyError, TypeError, RecursionError, OverflowError):
        wire, code = codec.encode(event_name, failure)
        return (wire, code if event_name in codec.EVENTS else 3), {
            **failure, "schema_version": 1, "host": host, "status": "degraded-failed",
            "event_hash": digest_bytes(payload_bytes), "native_host_response": "unobserved"}


def record_once(project, relative, receipt):
    directory = contained(project, relative)
    directory.mkdir(parents=True, exist_ok=True)
    identity = {name: receipt.get(name) for name in
        ("host", "phase", "session_key", "task_key", "artifact_sha256", "reason_codes")}
    if receipt.get("status") == "degraded-failed":
        identity.update(event_hash=receipt.get("event_hash"), failed_attempt=uuid.uuid4().hex)
    elif receipt.get("phase") != "stop":
        identity.update(context_hash=receipt.get("context_hash"), event_hash=receipt.get("event_hash"))
    key = digest_record(identity)
    path = contained(directory, key + ".json")
    for attempt in range(6):
        try:
            with exclusive_file_lock(contained(directory, key + ".lock")):
                if path.exists():
                    return "duplicate-suppressed"
                atomic_json(path, receipt)
                return "recorded"
        except ContractError:
            if attempt == 5:
                raise
            time.sleep(0.01)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=sorted(HOSTS), required=True)
    parser.add_argument("--event", required=True)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--context", required=True, help="Controller-selected project-relative context, never supplied by event payload.")
    parser.add_argument("--receipt-dir", help="Explicit owned project-relative receipt namespace.")
    args = parser.parse_args()
    payload = sys.stdin.buffer.read(MAX_EVENT_BYTES + 1)
    (wire, code), receipt = invoke(args.host, args.event, payload, project=args.project, context_reference=args.context)
    if args.receipt_dir:
        try:
            record_once(args.project, args.receipt_dir, receipt)
        except (ContractError, OSError):
            receipt["status"] = "degraded-failed"
            codec = importlib.import_module("hooks.codecs." + args.host)
            wire, code = codec.encode(args.event, {"decision": "block", "reason_codes": ["hook-receipt-conflict"]})
    print(json.dumps(wire, ensure_ascii=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
