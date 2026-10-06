"""Observe actual PreToolUse callbacks and inject explicitly declared test faults."""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--project", required=True, type=Path)
parser.add_argument("--runner", required=True, type=Path)
args = parser.parse_args()
control = args.project / "tool-probe-control.json"
specification = json.loads(control.read_text(encoding="utf8"))
mode = specification["mode"]
MODES = {"allow", "policy-deny", "malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec", "uncovered-tool"}
if mode not in MODES:
    raise RuntimeError("Undeclared tool probe mode")
target = args.project / "tool-observations" / mode / (uuid.uuid4().hex + ".json")
target.parent.mkdir(parents=True, exist_ok=True)
data = sys.stdin.buffer.read(65537)
record = {"schema_version": 1, "mode": mode, "started_at": datetime.now(timezone.utc).isoformat(),
          "status": "entered-from-native-host", "observer_pid": os.getpid(), "parent_pid": os.getppid(),
          "input_size": len(data), "input_sha256": hashlib.sha256(data).hexdigest(),
          "runner_sha256": hashlib.sha256(args.runner.read_bytes()).hexdigest(),
          "control_sha256": hashlib.sha256(control.read_bytes()).hexdigest(), "selected_event": "PreToolUse"}
try:
    parsed = json.loads(data)
    record.update(input_fields=sorted(parsed), reported_event=parsed.get("hook_event_name"),
                  native_tool_name=parsed.get("tool_name"), native_tool_use_id=parsed.get("tool_use_id"),
                  native_turn_id=parsed.get("turn_id"), native_model=parsed.get("model"),
                  tool_input_fields=sorted(parsed.get("tool_input", {})) if isinstance(parsed.get("tool_input"), dict) else [])
except (ValueError, TypeError):
    record["input_schema"] = "not-json-object"


def save():
    target.write_text(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf8")


save()
if mode == "crash":
    record["status"] = "intentional-test-crash-exit-17"
    save()
    os._exit(17)
if mode == "timeout":
    record["status"] = "intentional-test-sleep-eight-seconds"
    save()
    time.sleep(8)
if mode == "malformed-output":
    record["status"] = "intentional-test-malformed-output"
    save()
    print("[invalid-native-hook-output", flush=True)
    sys.exit(0)
event = "UnknownNckhEvent" if mode == "unsupported-codec" else "PreToolUse"
context = "tool-context-deny.json" if mode == "policy-deny" else "tool-context-uncovered.json" if mode == "uncovered-tool" else "tool-context-allow.json"
command = [sys.executable, "-I", str(args.runner), "--host", "codex", "--event", event,
           "--project", str(args.project), "--context", context, "--receipt-dir", "tool-policy-receipts/" + mode]
runner_input = b"{" if mode == "malformed-input" else data
process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           creationflags=subprocess.CREATE_NO_WINDOW)
record["runner_pid"] = process.pid
save()
try:
    stdout, stderr = process.communicate(runner_input, timeout=5)
except subprocess.TimeoutExpired:
    process.terminate()
    try:
        stdout, stderr = process.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate(timeout=5)
    record["runner_timeout"] = True
record.update(status="completed", runner_exit_code=process.returncode, runner_exited=process.poll() is not None,
              output_sha256=hashlib.sha256(stdout).hexdigest(), stderr_sha256=hashlib.sha256(stderr).hexdigest(),
              completed_at=datetime.now(timezone.utc).isoformat())
try:
    record["runner_output"] = json.loads(stdout)
except ValueError:
    record["runner_output"] = "invalid-json"
save()
sys.stdout.buffer.write(stdout)
sys.stderr.buffer.write(stderr)
sys.exit(process.returncode)
