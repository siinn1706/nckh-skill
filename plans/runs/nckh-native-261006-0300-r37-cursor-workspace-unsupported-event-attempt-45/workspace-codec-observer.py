"""Forward one bounded genuine workspace event unchanged to the packaged runner."""

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
parser.add_argument("--project", type=Path, required=True)
parser.add_argument("--evidence", type=Path, required=True)
parser.add_argument("--runner", type=Path, required=True)
args = parser.parse_args()
raw = sys.stdin.buffer.read(65537)
native = json.loads(raw)
assert len(raw) <= 65536 and isinstance(native, dict)
assert native.get("hook_event_name") == "workspaceOpen"
roots = native.get("workspace_roots")
assert isinstance(roots, list) and any(Path(root).resolve() == args.project.resolve() for root in roots)
args.evidence.resolve().relative_to(args.project.resolve())
sha = lambda data: hashlib.sha256(data).hexdigest()
target = args.evidence / "observations/workspace-codec" / (uuid.uuid4().hex + ".json")
target.parent.mkdir(parents=True, exist_ok=True)
record = {
    "event": "workspaceOpen", "reported_event": native["hook_event_name"],
    "selected_codec_event": "workspaceOpen", "callback_source": "project",
    "fault_origin": "none", "input_bytes_modified": False,
    "status": "entered-from-genuine-workspace-input", "input_fields": sorted(native),
    "input_size": len(raw), "input_sha256": sha(raw),
    "native_version": native.get("cursor_version"),
    "native_session_hash": sha(str(native.get("conversation_id")).encode()),
    "workspace_contains_selected_project": True, "observer_pid": os.getpid(),
    "parent_pid": os.getppid(), "started_at_utc": datetime.now(timezone.utc).isoformat(),
    "observer_sha256": sha(Path(__file__).read_bytes()), "runner_sha256": sha(args.runner.read_bytes()),
}

def save():
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf8")

save()
relative = args.evidence.relative_to(args.project).as_posix()
argv = [sys.executable, "-I", str(args.runner), "--host", "cursor", "--event", "workspaceOpen",
        "--project", str(args.project), "--context", relative + "/context-allow.json",
        "--receipt-dir", relative + "/policy-receipts/workspaceOpen"]
process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           creationflags=subprocess.CREATE_NO_WINDOW)
record["runner_pid"] = process.pid
record["forwarded_input_sha256"] = sha(raw)
save()
try:
    stdout, stderr = process.communicate(raw, timeout=5)
except subprocess.TimeoutExpired:
    process.terminate()
    try:
        stdout, stderr = process.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate(timeout=5)
    record["runner_timeout"] = True
record.update(status="completed", runner_exit_code=process.returncode,
              runner_exited=process.poll() is not None, output_sha256=sha(stdout),
              stderr_sha256=sha(stderr), completed_at_utc=datetime.now(timezone.utc).isoformat())
try:
    record["runner_output"] = json.loads(stdout)
except ValueError:
    record["runner_output"] = "invalid-json"
save()
sys.stdout.buffer.write(stdout)
sys.stderr.buffer.write(stderr)
sys.exit(process.returncode)
