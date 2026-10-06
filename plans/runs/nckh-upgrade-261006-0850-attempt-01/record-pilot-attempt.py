"""Record a genuine known offline child process; manifest commands are never executed."""
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
KIT = RUN.parents[2] / "nckh-kit"
sys.path.insert(0, str(KIT))
from core.experiments import manifest_bindings, validate_experiment_manifest, validate_run_receipt

def bind(path): return {"path": path, "sha256": hashlib.sha256((RUN / path).read_bytes()).hexdigest()}
def now(): return datetime.now(timezone.utc).isoformat()
manifest = json.loads((RUN / "experiment-manifest.json").read_text())
validate_experiment_manifest(manifest, project=RUN)
directory = RUN / "receipts"
directory.mkdir(exist_ok=True)
receipt_path = directory / "pilot-attempt-01.json"
assert not receipt_path.exists() and all(not (RUN / row["path"]).exists() for row in manifest["expected_outputs"])
argv = [sys.executable, "-I", str(RUN / "pilot-code.py"), "--config", "pilot-config.json"]
started = now()
monotonic = time.monotonic()
process = subprocess.Popen(argv, cwd=RUN, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
reason = ""
try:
    stdout, stderr = process.communicate(timeout=60)
except subprocess.TimeoutExpired:
    reason = "accepted 60-second pilot budget exhausted; exact owned child terminated and reaped"
    process.terminate()
    stdout, stderr = process.communicate()
ended = now()
wall = time.monotonic() - monotonic
(directory / "pilot-attempt-01.stdout.txt").write_bytes(stdout)
(directory / "pilot-attempt-01.stderr.txt").write_bytes(stderr)
outputs = []
for row in manifest["expected_outputs"]:
    path = RUN / row["path"]
    if path.exists():
        value = json.loads(path.read_text())
        outputs.append({"reference": bind(row["path"]), "kind": row["kind"], "count": len(value) if row["kind"] == "predictions" else 1})
status = "completed-unreviewed" if process.returncode == 0 and not reason else "failed"
if process.returncode != 0 and not reason: reason = "actual nonzero child exit; original stdout/stderr retained"
receipt = {"schema_version": 1, "task_id": manifest["task_id"], "run_id": "vnm-offline-pilot-01", "attempt_id": "pilot-attempt-01",
    "manifest": bind("experiment-manifest.json"), "inputs": manifest_bindings(manifest), "argv": argv, "cwd": str(RUN), "environment": manifest["environment"],
    "started_at": started, "ended_at": ended, "timezone": "UTC", "exit_code": process.returncode, "status": status,
    "process": {"pid": process.pid, "parent_pid": os.getpid(), "identity_started_at": started, "cleanup": "exited",
        "evidence": "Actual Popen PID/owned handle around launch; communicate returned and child exit observed. OS CreationDate not independently queried."},
    "stdout": bind("receipts/pilot-attempt-01.stdout.txt"), "stderr": bind("receipts/pilot-attempt-01.stderr.txt"), "outputs": outputs,
    "resources": {"wall_seconds": wall, "cpu_seconds": None, "peak_memory_bytes": None, "provider_cost": None, "coverage": "actual monotonic wall elapsed only; CPU/peak memory/provider cost not measured; provider unused"},
    "output_semantics": "computed-from-observed-data", "failure_reason": reason, "deviation_reason": "",
    "reconciliation": {"status": "reaped", "observed_at": now(), "reason": "Supervisor's exact owned child handle returned actual terminal exit; no descendants launched by pilot code"}}
with receipt_path.open("x", encoding="utf-8") as stream: stream.write(json.dumps(receipt, indent=2) + "\n")
checks = validate_run_receipt(receipt, manifest, receipt["manifest"], project=RUN)
print(json.dumps({"pid": process.pid, "exit_code": process.returncode, "status": status, "wall_seconds": wall, "checks": checks}))
raise SystemExit(process.returncode or (1 if reason else 0))
