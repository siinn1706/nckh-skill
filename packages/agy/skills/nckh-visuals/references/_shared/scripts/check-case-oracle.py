"""Score the mechanical oracle checks of one regression case against a finished workspace.

check-case-oracle.py --case-id ID --workspace DIR --before F [--response FILE]
check-case-oracle.py --case-id ID --print-prompt [--invocation TEMPLATE]

  --before    inventory written by `check-receipt.py inventory` before the attempt
  --response  the final user-visible response (UTF-8 text); needed by @response checks
  --print-prompt  print the exact prompt a runner sends for the case (its `dispatch` mode
              applied) as JSON and exit 0; scores nothing and needs no workspace
  --invocation  host invocation template for --print-prompt, default "/{skill}"
              (Codex uses "${skill}")

No model or provider is called and the case manifest is never modified. Only exit-status
checks run a command: the argv recorded in the kit manifest, on a temporary copy of the
workspace with a minimal environment, so the workspace itself is never modified. That is
filesystem isolation only, not network or process isolation; score untrusted workspaces
inside a disposable VM or container.
Exit 0 = every mechanical check passed, 1 = a check failed or setup is wrong (BLOCKED:
a fixture is missing or altered, or a git check has no workspace .git), 2 = usage error,
including a malformed before inventory. Output is ASCII-safe JSON; reviewer_acceptance lists the
criteria that still need a human or agent reviewer.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from core.build import load_json, validate_catalog
from core.evaluation import DEFAULT_INVOCATION, dispatch_prompt, evaluate_case, load_regression_cases
from core.schema import ContractError


class UsageError(Exception):
    pass


def emit(record, stream=None):
    print(json.dumps(record, ensure_ascii=True, indent=2, sort_keys=True), file=stream or sys.stdout)


def read_utf8(path, label):
    if not path.is_file():
        raise UsageError(f"{label} is not a file: {path}")
    try:
        return path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as error:
        raise UsageError(f"{label} is not UTF-8: {error}") from error


def load_case(case_id):
    identities = validate_catalog(load_json(ROOT / "core/registry/catalog/skills.json"))
    cases = load_regression_cases(ROOT, identities)
    if case_id not in cases:
        raise UsageError(f"unknown regression case id: {case_id}")
    return cases[case_id]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--before", type=Path)
    parser.add_argument("--response", type=Path)
    parser.add_argument("--print-prompt", action="store_true")
    parser.add_argument("--invocation", default=DEFAULT_INVOCATION)
    args = parser.parse_args()
    if args.print_prompt:
        if args.workspace or args.before or args.response:
            parser.error("--print-prompt takes no --workspace, --before or --response")
    elif args.workspace is None or args.before is None:
        parser.error("the following arguments are required: --workspace, --before")
    elif args.invocation != DEFAULT_INVOCATION:
        parser.error("--invocation applies only to --print-prompt")
    try:
        if args.print_prompt:
            case = load_case(args.case_id)
            emit({"case_id": case["id"], "dispatch": case.get("dispatch", "natural"),
                  "prompt": dispatch_prompt(case, args.invocation)})
            return 0
        if not args.workspace.is_dir():
            raise UsageError(f"workspace is not a directory: {args.workspace}")
        before = json.loads(read_utf8(args.before, "before inventory"))
        response = read_utf8(args.response, "response") if args.response else None
        result = evaluate_case(load_case(args.case_id), args.workspace, before, response)
    except (UsageError, ContractError, OSError, json.JSONDecodeError) as error:
        emit({"verdict": "ERROR", "error": str(error)}, sys.stderr)
        return 2
    emit({"workspace": str(args.workspace), **result})
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
