"""An explicit, closed JSON Schema subset without runtime downloads."""

import json
import math
import re
from pathlib import Path


class ContractError(ValueError):
    pass


KEYWORDS = {"type", "properties", "required", "additionalProperties", "items",
            "enum", "const", "minLength", "minimum", "minItems", "pattern",
            "description", "$schema", "title"}


def validate(value, schema, path="$", *, check_schema=True):
    if check_schema:
        unknown = set(schema) - KEYWORDS
        if unknown:
            raise ContractError(f"{path}: unsupported schema keywords: {sorted(unknown)}")
        for child in schema.get("properties", {}).values():
            _check_schema(child)
        if "items" in schema:
            _check_schema(schema["items"])
    expected = schema.get("type")
    types = {"object": dict, "array": list, "string": str, "boolean": bool,
             "integer": int, "number": (int, float), "null": type(None)}
    if expected and (expected not in types or not isinstance(value, types[expected])
                     or expected in {"number", "integer"} and isinstance(value, bool)):
        raise ContractError(f"{path}: expected {expected}")
    if "const" in schema and not _json_equal(value, schema["const"]):
        raise ContractError(f"{path}: unsupported value/version {value!r}")
    if "enum" in schema and not any(_json_equal(value, member) for member in schema["enum"]):
        raise ContractError(f"{path}: value not in enum")
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        missing = set(schema.get("required", [])) - value.keys()
        if missing:
            raise ContractError(f"{path}: missing {sorted(missing)}")
        extra = value.keys() - properties.keys()
        if extra and schema.get("additionalProperties") is False:
            raise ContractError(f"{path}: unknown fields {sorted(extra)}")
        for key, item in value.items():
            if key in properties:
                validate(item, properties[key], f"{path}.{key}", check_schema=False)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ContractError(f"{path}: too few items")
        for index, item in enumerate(value):
            if "items" in schema:
                validate(item, schema["items"], f"{path}[{index}]", check_schema=False)
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise ContractError(f"{path}: empty or short string")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            raise ContractError(f"{path}: pattern mismatch")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if isinstance(value, float) and not math.isfinite(value):
            raise ContractError(f"{path}: nonfinite number")
        if value < schema.get("minimum", float("-inf")):
            raise ContractError(f"{path}: below minimum")
    return value


def _json_equal(left, right):
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(_json_equal(left[key], right[key]) for key in left)
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(_json_equal(a, b) for a, b in zip(left, right))
    return left == right


def _check_schema(schema):
    unknown = set(schema) - KEYWORDS
    if unknown:
        raise ContractError(f"unsupported schema keywords: {sorted(unknown)}")
    for child in schema.get("properties", {}).values():
        _check_schema(child)
    if "items" in schema:
        _check_schema(schema["items"])


def validate_record(kind, record):
    path = Path(__file__).parent / "contracts" / f"{kind}.schema.json"
    return validate(record, json.loads(path.read_text(encoding="utf-8")))
