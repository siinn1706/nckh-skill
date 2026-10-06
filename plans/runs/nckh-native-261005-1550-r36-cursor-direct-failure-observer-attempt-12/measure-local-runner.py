"""Measure synthetic local executions separately from genuine native observations."""

import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owned_cursor_failure_timing", RUN / "cursor-direct-failure-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
assert not (RUN / "local-runner-timing.json").exists()
stage = probe.read(RUN / "stage.json")
definition = probe.read(RUN / "definitions/session.json")
assert probe.digest_file(probe.CONFIG) == definition["config_sha256"]
context = {**probe.read(probe.EVIDENCE / "context-allow.json"), "task_id": "local-synthetic-timing-12"}
probe.atomic_json(probe.EVIDENCE / "context-local-timing.json", context)
argv = [sys.executable, "-I", stage["runner"], "--host", "cursor", "--event", "preToolUse",
        "--project", str(probe.PROJECT), "--context", ".nckh-native-r36-cursor-direct-failure-12/context-local-timing.json",
        "--receipt-dir", ".nckh-native-r36-cursor-direct-failure-12/local-timing-receipts"]
preparation = probe.read(RUN / "preparation.json")
payload = {"hook_event_name": "preToolUse", "conversation_id": "local-synthetic-timing-12",
           "workspace_roots": [str(probe.PROJECT)], "tool_name": "Read",
           "tool_input": {"file_path": str(probe.PROJECT / preparation["relative"])}}
rows = []
for index in range(3):
    start = time.perf_counter()
    result = subprocess.run(argv, cwd=probe.PROJECT, input=json.dumps(payload).encode(),
                            capture_output=True, timeout=25)
    row = {"index": index + 1, "elapsed_seconds": time.perf_counter() - start,
           "exit_code": result.returncode, "stdout": result.stdout.decode("utf8"),
           "stderr": result.stderr.decode("utf8"), "native_callback": False}
    rows.append(row)
    probe.atomic_json(RUN / "local-runner-timing.json", {"evidence_class": "synthetic-local-timing",
        "rows": rows, "command": argv, "payload": payload, "model_turns": 0,
        "source_lock_hash": probe.EXPECTED, "not_native_timeout_qualification": True})
    assert result.returncode == 0 and json.loads(result.stdout) == {}
print(json.dumps({"status": "measured-local-only", "seconds": [round(row["elapsed_seconds"], 3) for row in rows]}))
