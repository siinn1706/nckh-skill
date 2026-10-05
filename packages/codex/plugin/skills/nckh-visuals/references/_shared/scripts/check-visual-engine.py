"""Read-only integrity checking of an explicitly supplied task SVG engine binding."""

import argparse
import hashlib
import importlib.util
import json
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("visual_contract_schema", ROOT / "core/schema.py")
schema_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schema_module)
ContractError = schema_module.ContractError
validate = schema_module.validate
HASH = {"type": "string", "pattern": "^[a-f0-9]{64}$"}
REFERENCE = {"type": "object", "additionalProperties": False,
             "properties": {"path": {"type": "string", "minLength": 1}, "sha256": HASH},
             "required": ["path", "sha256"]}
RECEIPT_FIELDS = {
    "command": {"type": "array", "minItems": 2,
                "items": {"type": "string", "minLength": 1}},
    "exit_status": {"const": 0},
    "executable_sha256": HASH,
    "version": {"type": "string", "minLength": 1},
    "stdout": REFERENCE,
    "stderr": REFERENCE,
    "status": {"const": "completed-unreviewed"},
    "cleanup": {"const": "owned-process-group-closed"},
}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def strict_json(data):
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ContractError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def reject_constant(value):
        raise ContractError(f"nonfinite JSON constant: {value}")

    def finite_float(value):
        number = float(value)
        if not math.isfinite(number):
            raise ContractError("nonfinite JSON number")
        return number

    return json.loads(data, object_pairs_hook=unique_keys, parse_constant=reject_constant,
                      parse_float=finite_float)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def no_links(path):
    for current in (path, *path.parents):
        if current.is_symlink() or getattr(current, "is_junction", lambda: False)():
            raise ContractError(f"linked path is not allowed: {current}")
    return path


def absolute_path(value, *, directory=False):
    path = Path(value)
    if not path.is_absolute() or any(part in {".", ".."} for part in path.parts):
        raise ContractError("an absolute canonical path is required")
    path = no_links(path)
    if not (path.is_dir() if directory else path.is_file()):
        raise ContractError(f"required path is unavailable: {path}")
    return path.resolve()


def member(project, relative):
    if (not isinstance(relative, str) or not relative or relative.startswith("/")
            or "\\" in relative or ":" in relative
            or any(part in {"", ".", ".."} for part in relative.split("/"))):
        raise ContractError("references must be canonical project-relative paths")
    path = no_links(project.joinpath(*relative.split("/")))
    if not path.resolve().is_relative_to(project) or not path.is_file():
        raise ContractError(f"missing or escaping project reference: {relative}")
    return path.resolve()


def reference(project, record):
    validate(record, REFERENCE)
    path = member(project, record["path"])
    data = path.read_bytes()
    if digest(data) != record["sha256"]:
        raise ContractError(f"reference hash drift: {record['path']}")
    return path, data


def command_member(project, operand):
    path = Path(operand)
    if path.is_absolute():
        path = absolute_path(operand)
        if not path.is_relative_to(project):
            raise ContractError("command operand escapes project")
        return member(project, path.relative_to(project).as_posix())
    return member(project, operand)


def render_operands(command, project):
    source, output, format_seen = None, None, False
    arguments = iter(command[1:])
    for argument in arguments:
        if argument in {"-o", "--output"}:
            if output is not None:
                raise ContractError("duplicate render output argument")
            output = next(arguments, None)
            if output is None:
                raise ContractError("missing render output argument")
        elif argument.startswith("--output="):
            if output is not None:
                raise ContractError("duplicate render output argument")
            output = argument.split("=", 1)[1]
        elif argument in {"--format", "--format=png"}:
            if format_seen or (argument == "--format" and next(arguments, None) != "png"):
                raise ContractError("unsupported or duplicate render format")
            format_seen = True
        elif argument.startswith("-") or source is not None:
            raise ContractError("unsupported render command argument")
        else:
            source = argument
    if not source or not output:
        raise ContractError("render command must name one SVG input and one PNG output")
    return command_member(project, source), command_member(project, output)


def process_receipt(project, ref, engine, executable, *, render=False):
    _, data = reference(project, ref)
    receipt = strict_json(data)
    properties = dict(RECEIPT_FIELDS)
    if render:
        properties.update({"input_sha256": HASH, "render_sha256": HASH})
    validate(receipt, {"type": "object", "additionalProperties": False,
                       "properties": properties, "required": list(properties)})
    if (absolute_path(receipt["command"][0]) != executable
            or receipt["executable_sha256"] != engine["sha256"]
            or receipt["version"] != engine["version"]):
        raise ContractError("process receipt executable/version differs from the selected engine")
    _, stdout = reference(project, receipt["stdout"])
    reference(project, receipt["stderr"])
    if not render:
        if receipt["command"][1:] != ["--version"]:
            raise ContractError("unsupported version command")
        if stdout.decode("utf-8").strip() != engine["version"]:
            raise ContractError("version receipt output differs from the observed version")
    return receipt


def check_binding(project, task, host, binding, *, capability="svg-render", root=ROOT):
    project = absolute_path(project, directory=True)
    if not task.strip() or host not in {"claude", "codex", "cursor", "agy"}:
        raise ContractError("an explicit task and supported host are required")
    contract = strict_json((root / "extensions/native-documents/contract.json").read_bytes())
    validate(contract, strict_json((root / "core/contracts/extension.schema.json").read_bytes()))
    route = contract.get("runtime_binding")
    if not route or capability not in route["capabilities"]:
        raise ContractError("required capability has no permitted task binding route")
    path = member(project, binding)
    data = path.read_bytes()
    record = strict_json(data)
    validate(record, strict_json((root / route["schema"]).read_bytes()))
    scope = record["scope"]
    if (absolute_path(scope["project_root"], directory=True) != project
            or scope["task_id"] != task or scope["host"] != host):
        raise ContractError("binding project/task/host scope mismatch")
    capabilities = record["capabilities"]
    if len(set(capabilities)) != len(capabilities) or capability not in capabilities:
        raise ContractError("required capability is missing or duplicated")
    engine = record["engine"]
    executable = absolute_path(engine["executable"])
    if digest(executable.read_bytes()) != engine["sha256"]:
        raise ContractError("selected executable hash drift")
    observations = record["observations"]
    source, svg = reference(project, observations["input_svg"])
    render, png = reference(project, observations["render_png"])
    if source.suffix.lower() != ".svg" or ET.fromstring(svg).tag not in {
            "svg", "{http://www.w3.org/2000/svg}svg"}:
        raise ContractError("observed input is not an SVG document")
    if render.suffix.lower() != ".png" or not png.startswith(PNG_SIGNATURE):
        raise ContractError("observed render lacks the PNG signature")
    process_receipt(project, observations["version_receipt"], engine, executable)
    receipt = process_receipt(project, observations["render_receipt"], engine, executable, render=True)
    if (receipt["input_sha256"] != observations["input_svg"]["sha256"]
            or receipt["render_sha256"] != observations["render_png"]["sha256"]
            or render_operands(receipt["command"], project) != (source, render)):
        raise ContractError("render receipt input/output identity mismatch")
    return {"status": "integrity-verified", "scope": scope, "capability": capability,
            "binding_sha256": digest(data), "engine": engine,
            "global_status": contract["status"],
            "authorization": "not-established-by-checker",
            "acceptance": "pending-independent-gates",
            "limitations": ["Receipt integrity and matching do not authenticate execution or grant permission.",
                            "Final editability, open/render, source truth, accessibility and scientific meaning remain separate gates."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--host", required=True, choices=["claude", "codex", "cursor", "agy"])
    parser.add_argument("--binding", required=True, help="Explicit project-relative binding JSON path")
    parser.add_argument("--capability", required=True, choices=["svg-render"])
    args = parser.parse_args()
    try:
        result = check_binding(args.project, args.task, args.host, args.binding,
                               capability=args.capability)
    except (ContractError, OSError, ValueError, ET.ParseError) as error:
        print(json.dumps({"status": "unavailable", "reason": str(error), "fallback": False}))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
