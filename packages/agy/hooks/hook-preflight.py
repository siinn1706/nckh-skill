"""Read-only manual checker sharing the neutral policy; no generator or native enforcement."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
if (ROOT / "hooks/_shared").is_dir():
    sys.path.insert(0, str(ROOT / "hooks/_shared"))
from core.hook_policy import MAX_EVENT_BYTES, evaluate
from hooks.runner import load_context, strict_json
from core.schema import ContractError


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--context", required=True)
    args = parser.parse_args()
    try:
        data = sys.stdin.buffer.read(MAX_EVENT_BYTES + 1)
        if len(data) > MAX_EVENT_BYTES:
            raise ContractError("event too large")
        context, _ = load_context(args.project, args.context)
        result = evaluate(strict_json(data), context, project=args.project)
    except (ContractError, OSError, ValueError, KeyError, TypeError, RecursionError):
        result = {"decision": "block", "reason_codes": ["manual-preflight-invalid"], "status": "degraded-failed", "native_enforcement": "unverified"}
    print(json.dumps(result))
    return 0 if result["decision"] in {"allow", "advisory"} else 3


if __name__ == "__main__":
    sys.exit(main())
