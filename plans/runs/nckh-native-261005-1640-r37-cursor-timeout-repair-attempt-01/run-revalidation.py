"""Revalidate the frozen repair through unchanged local delivery stages."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
ROOT = WORK / "nckh-kit"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
from core.build import verify_source_lock
from core.paths import atomic_json, digest_file, digest_record
from core.processes import run_owned_command

lock = verify_source_lock(ROOT)
assert lock["revision"] == "37"
expected = digest_record(lock)
summary_path = RUN / "revalidation-summary.json"
if summary_path.exists():
    raise RuntimeError("Preserve earlier revalidation")
stages = [
    ("deterministic", [sys.executable, "-X", "utf8", "-B", str(RUN / "deterministic-without-global-deadline.py")]),
    ("build", [sys.executable, "-X", "utf8", "-B", str(RUN / "run-delivery-r37.py"), "build"]),
    ("archive", [r"C:\Program Files\PowerShell\7\pwsh.exe", "-NoProfile", "-File", str(RUN / "archive-delivery.ps1")]),
    ("smoke", [sys.executable, "-X", "utf8", "-B", str(RUN / "run-delivery-r37.py"), "smoke"]),
    ("preview", [sys.executable, "-X", "utf8", "-B", str(RUN / "run-delivery-r37.py"), "preview"]),
    ("preservation", [sys.executable, "-X", "utf8", "-B", str(RUN / "run-delivery-r37.py"), "final"]),
]
summary = {"status": "running", "source_revision": 37, "source_lock_hash": expected, "global_deadline_seconds": None,
    "owner": "/root", "port": None, "stages": [], "native_r37_retest": "pending", "installed_update": "not-performed"}
atomic_json(summary_path, summary)
for name, argv in stages:
    assert digest_record(verify_source_lock(ROOT)) == expected
    stem = RUN / "commands" / ("pipeline-" + name)
    receipt_path = Path(str(stem) + ".json")
    stdout, stderr = Path(str(stem) + ".stdout"), Path(str(stem) + ".stderr")
    record = {"argv": argv, "cwd": str(ROOT), "stage": name, "source_lock_hash": expected, "owner": "/root",
        "started_at": datetime.now(timezone.utc).isoformat(), "status": "starting", "port": None}

    def started(pid):
        record.update(pid=pid, status="running")
        atomic_json(receipt_path, record)

    result = run_owned_command(argv, ROOT, b"", stdout, stderr, timeout=None, on_started=started)
    record.update(**result, ended_at=datetime.now(timezone.utc).isoformat(), stdout_sha256=digest_file(stdout), stderr_sha256=digest_file(stderr))
    atomic_json(receipt_path, record)
    summary["stages"].append({"name": name, "receipt": receipt_path.relative_to(WORK).as_posix(), **result})
    if result["exit_status"] != 0:
        summary.update(status="failed", failed_stage=name)
        atomic_json(summary_path, summary)
        raise RuntimeError("Retain the actual failed stage: " + name)
    atomic_json(summary_path, summary)
    print(json.dumps({"stage": name, "status": "completed", "seconds": result["seconds"]}), flush=True)
summary.update(status="completed-local-checks-native-retest-pending", source_unchanged=digest_record(verify_source_lock(ROOT)) == expected)
atomic_json(summary_path, summary)
print(json.dumps({"status": summary["status"], "stages": len(summary["stages"])}), flush=True)
