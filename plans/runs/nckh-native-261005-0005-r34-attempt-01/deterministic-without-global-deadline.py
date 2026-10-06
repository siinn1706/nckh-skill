"""Run the reviewed r34 suite without an overall deadline; keep individual test timeouts."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2] / "nckh-kit"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from core.build import verify_source_lock
from core.evaluation import validate_cases
from core.paths import atomic_json, digest_file, digest_record
from core.processes import run_owned_command

name = "deterministic-r34-attempt-01"
receipt_path = RUN / "commands" / (name + ".json")
summary_path = RUN / (name + ".json")
result_path = RUN / (name + "-suite.json")
if any(path.exists() for path in (receipt_path, summary_path, result_path)):
    raise RuntimeError("Preserve existing attempts")
lock = verify_source_lock(ROOT)
source_hash = digest_record(lock)
if lock["revision"] != "34":
    raise RuntimeError("Select the actual reviewed source revision")
summary = validate_cases(ROOT)
argv = [sys.executable, "-X", "utf8", "-B", str(RUN / "direct-deterministic-suite.py"), str(result_path)]
stdout = RUN / "commands" / (name + ".stdout")
stderr = RUN / "commands" / (name + ".stderr")
record = {"argv": argv, "cwd": str(ROOT), "started_at": datetime.now(timezone.utc).isoformat(),
          "source_lock_hash": source_hash, "status": "starting", "port": None, "owner": "/root",
          "run": str(RUN), "global_deadline_seconds": None,
          "previous_attempt": 'C:/Users/USER\\Downloads\\test-skill\\plans\\runs\\nckh-native-261004-2112-r33-attempt-01\\deterministic-r33-attempt-01.json', "test_timeouts": "unchanged"}


def started(pid):
    record.update(pid=pid, status="running")
    atomic_json(receipt_path, record)


outcome = run_owned_command(argv, ROOT, b"", stdout, stderr, timeout=None, on_started=started)
record.update(outcome, ended_at=datetime.now(timezone.utc).isoformat(),
              stdout_sha256=digest_file(stdout), stderr_sha256=digest_file(stderr))
atomic_json(receipt_path, record)
result = json.loads(result_path.read_text(encoding="utf8"))
unchanged = digest_record(verify_source_lock(ROOT)) == source_hash
passed = outcome["exit_status"] == 0 and result["successful"] and unchanged
summary.update(status="pass" if passed else "fail", evidence_class="deterministic",
               source_revision=lock["revision"], source_lock_hash=source_hash,
               source_unchanged=unchanged, recorded_at=record["ended_at"],
               deterministic={**result, **outcome, "command": argv,
                              "output_sha256": digest_file(stderr), "output_path": str(stderr)},
               previous_attempt='C:/Users/USER\\Downloads\\test-skill\\plans\\runs\\nckh-native-261004-2112-r33-attempt-01\\deterministic-r33-attempt-01.json', native_qualification="separate")
atomic_json(summary_path, summary)
print(json.dumps({"status": summary["status"], "tests": result["tests"], "skipped": len(result["skipped"]),
                  "seconds": outcome["seconds"], "errors": [row["test"] for row in result["errors"]]}), flush=True)
sys.exit(0 if passed else 1)
