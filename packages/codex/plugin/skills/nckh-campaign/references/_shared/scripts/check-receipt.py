"""Record a workspace inventory or verify a v2 command receipt against it and the disk.

inventory --root DIR --output F    hash every file (sha256, EOL, BOM) before an attempt
verify --receipt R [--before F] [--workspace DIR]
                                   check per-command exits, input preservation and real hashes

Exit 0 = VERIFIED, 1 = FAILED, 2 = usage error. Output is ASCII-safe JSON. Recorded
commands are never executed.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from core.ledger import inventory, validate_receipt
from core.schema import ContractError


class UsageError(Exception):
    pass


def emit(record, stream=None):
    print(json.dumps(record, ensure_ascii=True, indent=2, sort_keys=True), file=stream or sys.stdout)


def load_json(path, label):
    if not path.is_file():
        raise UsageError(f"{label} is not a file: {path}")
    return json.loads(path.read_bytes().decode("utf-8"))


def run_inventory(args):
    if not args.root.is_dir():
        raise UsageError(f"inventory root is not a directory: {args.root}")
    record = inventory(args.root)
    data = json.dumps(record, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    try:
        with args.output.open("x", encoding="ascii", newline="\n") as stream:
            stream.write(data)
    except FileExistsError as error:
        raise UsageError(f"output already exists; choose a fresh path: {args.output}") from error
    emit({"verdict": "RECORDED", "output": str(args.output), "files": len(record["files"]),
          "links": record["links"]})
    return 0


def run_verify(args):
    try:
        receipt = load_json(args.receipt, "receipt")
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        emit({"verdict": "FAILED", "findings": [f"receipt is not UTF-8 JSON: {error}"]})
        return 1
    before = load_json(args.before, "before inventory") if args.before else None
    if args.workspace is not None and not args.workspace.is_dir():
        raise UsageError(f"workspace is not a directory: {args.workspace}")
    result = validate_receipt(receipt, before=before, workspace=args.workspace)
    emit({"receipt": str(args.receipt), **result})
    return 0 if result["verdict"] == "VERIFIED" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    record = commands.add_parser("inventory", help="Write a before/after inventory of a directory")
    record.add_argument("--root", type=Path, required=True)
    record.add_argument("--output", type=Path, required=True)
    check = commands.add_parser("verify", help="Verify a v2 receipt")
    check.add_argument("--receipt", type=Path, required=True)
    check.add_argument("--before", type=Path, help="Inventory recorded before the attempt")
    check.add_argument("--workspace", type=Path, help="Directory the receipt paths are relative to")
    args = parser.parse_args()
    try:
        return run_inventory(args) if args.command == "inventory" else run_verify(args)
    except (UsageError, ContractError, OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        emit({"verdict": "ERROR", "error": str(error)}, sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
