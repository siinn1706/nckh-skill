"""Forward genuine bounded native input and record declared source provenance."""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--event", required=True)
parser.add_argument("--project", type=Path, required=True)
parser.add_argument("--context", required=True)
parser.add_argument("--receipt-dir", required=True)
parser.add_argument("--evidence", type=Path, required=True)
parser.add_argument("--runner", type=Path, required=True)
parser.add_argument("--callback-source", choices=["project", "plugin"], required=True)
args = parser.parse_args()
data = sys.stdin.buffer.read(65537)
sha = lambda value: hashlib.sha256(value).hexdigest()
record = {"event": args.event, "callback_source": args.callback_source, "fault_origin": "none",
    "status": "entered-from-native-host", "input_size": len(data), "input_sha256": sha(data),
    "observer_pid": os.getpid(), "parent_pid": os.getppid(), "runner_sha256": sha(args.runner.read_bytes()),
    "observer_sha256": sha(Path(__file__).read_bytes()), "started_at": datetime.now(timezone.utc).isoformat()}
try:
    native = json.loads(data)
    record.update(reported_event=native.get("hook_event_name"), native_tool_name=native.get("tool_name"),
        native_tool_use_id=native.get("tool_use_id"), native_model=native.get("model"),
        native_session_hash=sha(str(native.get("session_id")).encode()), native_turn_id=native.get("turn_id"))
    fields = native.get("tool_input")
    if isinstance(fields, dict) and isinstance(fields.get("command"), str):
        record["native_command_sha256"] = sha(fields["command"].encode())
except (ValueError, TypeError, AttributeError):
    record["input_schema"] = "unreadable-native-object"
target = args.evidence / "observations" / args.event / (uuid.uuid4().hex + ".json")
target.parent.mkdir(parents=True, exist_ok=True)
def save():
    target.write_text(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf8")
save()
process = subprocess.Popen([sys.executable, "-I", str(args.runner), "--host", "codex", "--event", args.event,
    "--project", str(args.project), "--context", args.context, "--receipt-dir", args.receipt_dir],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
record["runner_pid"] = process.pid
save()
try:
    stdout, stderr = process.communicate(data, timeout=5)
except subprocess.TimeoutExpired:
    process.terminate()
    try:
        stdout, stderr = process.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate(timeout=5)
    record["runner_timeout"] = True
record.update(status="completed", runner_exit_code=process.returncode, runner_exited=process.poll() is not None,
    stdout_sha256=sha(stdout), stderr_sha256=sha(stderr), completed_at=datetime.now(timezone.utc).isoformat())
save()
sys.stdout.buffer.write(stdout)
sys.stderr.buffer.write(stderr)
sys.exit(process.returncode)
