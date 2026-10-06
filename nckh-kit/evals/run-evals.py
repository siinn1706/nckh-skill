import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core.evaluation import validate_cases
from core.agent_runs import prepare_agent_run, run_agent_cases
from core.schema import ContractError
from core.build import load_json, verify_source_lock
from core.paths import atomic_json, digest_bytes, digest_record


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate cases, run local suites, or preview/opt in to command observations; no automatic native/human acceptance.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--validate-only", action="store_true")
    mode.add_argument("--run-deterministic", action="store_true")
    mode.add_argument("--prepare-agent-run", action="store_true", help="Read-only preview of an explicit command-adapter recipe.")
    mode.add_argument("--run-agent", action="store_true", help="Opt-in development run; requires frozen references and the reviewed plan hash.")
    parser.add_argument("--recipe", type=Path, help="Explicit native command binding; JSON fields never grant execution authority.")
    parser.add_argument("--approve-plan-hash", help="Canonical SHA-256 printed by --prepare-agent-run for this exact transaction.")
    parser.add_argument("--allow-provider", action="store_true", help="Operator confirmation of the separately authorized provider scope.")
    parser.add_argument("--output", type=Path, help="Save a local structured receipt for these actual checks; no provider/human acceptance.")
    args = parser.parse_args(argv)
    summary = {"schema_version": 1, "evidence_class": "static"}
    command = None
    try:
        if args.prepare_agent_run or args.run_agent:
            if not args.recipe:
                raise ContractError("agent modes require --recipe")
            recipe = load_json(args.recipe)
            if args.prepare_agent_run:
                summary = prepare_agent_run(ROOT, recipe)
                summary["plan_hash"] = digest_record(summary)
            else:
                summary = run_agent_cases(ROOT, recipe, approved_plan_hash=args.approve_plan_hash,
                                          allow_provider=args.allow_provider)
            if args.output:
                atomic_json(args.output, summary)
            print(json.dumps(summary, indent=2))
            return 0 if summary["status"] in {"preview", "completed-unreviewed"} else 3
        if args.recipe or args.approve_plan_hash or args.allow_provider:
            raise ContractError("agent execution flags cannot be used with structural/deterministic modes")
        summary = validate_cases(ROOT)
        source_hash = digest_record(verify_source_lock(ROOT))
        summary.update(source_lock_hash=source_hash, recorded_at=datetime.now(timezone.utc).isoformat(),
                       environment={"python": sys.version.split()[0], "platform": sys.platform})
        if args.run_deterministic:
            command = [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-p", "test_*.py"]
            process = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=900)
            output = process.stdout + process.stderr
            count = re.search(r"Ran (\d+) tests?", output)
            if process.returncode or not count or int(count.group(1)) == 0:
                summary["deterministic"] = {"status": "fail", "exit_status": process.returncode,
                                            "tests": int(count.group(1)) if count else 0,
                                            "command": command, "output": output}
                print(output, file=sys.stderr)
                raise ContractError("deterministic suite failed or discovered no tests")
            summary["deterministic"] = {"status": "pass", "tests": int(count.group(1)),
                                         "exit_status": process.returncode, "command": command,
                                         "output_sha256": digest_bytes(output.encode("utf-8")), "output": output}
        if digest_record(verify_source_lock(ROOT)) != source_hash:
            raise ContractError("source changed during checks; receipt cannot certify the new revision")
        summary["status"] = "pass"
        if args.output:
            atomic_json(args.output, summary)
        print(json.dumps(summary, indent=2))
        return 0
    except (ContractError, OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        summary.update(status="timeout-unknown" if isinstance(error, subprocess.TimeoutExpired) else "fail",
                       error=str(error), recorded_at=datetime.now(timezone.utc).isoformat())
        if isinstance(error, subprocess.TimeoutExpired):
            chunks = [value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value or ""
                      for value in (error.stdout, error.stderr)]
            summary["deterministic"] = {"status": "timeout-unknown", "exit_status": None,
                                         "command": command, "output": "".join(chunks)}
        if args.output:
            try:
                atomic_json(args.output, summary)
            except OSError as receipt_error:
                summary["receipt_error"] = str(receipt_error)
        print(json.dumps(summary, indent=2), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
