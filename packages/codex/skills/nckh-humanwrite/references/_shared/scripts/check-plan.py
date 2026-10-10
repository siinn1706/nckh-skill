"""Check a plan directory's structure: phase files, sections, links and status receipts.

Exit 0 = VERIFIED, 1 = FAILED, 2 = usage error. Output is ASCII-safe JSON.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from core.plan_check import check_plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan_dir", type=Path, help="Directory holding plan.md and phase-NN-*.md files")
    args = parser.parse_args()
    if not args.plan_dir.is_dir():
        print(json.dumps({"verdict": "ERROR", "error": f"not a directory: {args.plan_dir}"},
                         ensure_ascii=True), file=sys.stderr)
        return 2
    try:
        result = check_plan(args.plan_dir)
    except OSError as error:
        print(json.dumps({"verdict": "ERROR", "error": str(error)}, ensure_ascii=True), file=sys.stderr)
        return 2
    print(json.dumps({"plan_dir": str(args.plan_dir), **result}, ensure_ascii=True, indent=2))
    return 0 if result["verdict"] == "VERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
