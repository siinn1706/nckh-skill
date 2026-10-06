"""Bounded native callbacks with controller-declared fault selection."""

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
parser.add_argument("--event", required=True)
parser.add_argument("--project", type=Path, required=True)
parser.add_argument("--evidence", type=Path, required=True)
parser.add_argument("--runner", type=Path, required=True)
args = parser.parse_args()
control = json.loads((args.evidence / "control.json").read_text(encoding="utf8"))
selected = args.event == control["selected_event"]
mode = control["mode"] if selected else "allow"
sha = lambda value: hashlib.sha256(value).hexdigest()
data = sys.stdin.buffer.read(65537)
target = args.evidence / "observations" / control["attempt"] / args.event / (uuid.uuid4().hex + ".json")
target.parent.mkdir(parents=True, exist_ok=True)
record = {"event": args.event, "mode": mode, "attempt": control["attempt"], "selected": selected,
    "status": "entered-from-native-host", "observer_pid": os.getpid(), "parent_pid": os.getppid(),
    "started_at": datetime.now(timezone.utc).isoformat(), "input_size": len(data), "input_sha256": sha(data),
    "runner_sha256": sha(args.runner.read_bytes()), "fault_origin": "controller-after-genuine-callback" if mode in
    {"malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec"} else "none"}
try:
    native = json.loads(data)
    record.update(input_fields=sorted(native), reported_event=native.get("hook_event_name"),
        native_tool_name=native.get("tool_name"), native_tool_use_id=native.get("tool_use_id"),
        native_turn_id=native.get("turn_id"), native_model=native.get("model"),
        native_session_hash=sha(str(native.get("session_id")).encode()),
        native_permission_mode=native.get("permission_mode"),
        tool_input_fields=sorted(native.get("tool_input", {})) if isinstance(native.get("tool_input"), dict) else [])
    if isinstance(native.get("tool_input"), dict) and isinstance(native["tool_input"].get("command"), str):
        record["native_command_sha256"] = sha(native["tool_input"]["command"].encode())
    fields = native.get("tool_input")
    record["native_tool_input_type"] = type(fields).__name__
    record["native_direct_path_fields"] = {key: fields[key] for key in ("file_path", "path")
        if isinstance(fields, dict) and isinstance(fields.get(key), str)}
    patch_input = fields if isinstance(fields, str) else fields.get("input", fields.get("patch")) if isinstance(fields, dict) else None
    if isinstance(patch_input, str):
        record["native_text_input_sha256"] = sha(patch_input.encode())
        record["native_patch_header_paths"] = [line.split(": ", 1)[1] for line in patch_input.splitlines()
            if line.startswith(("*** Add File: ", "*** Update File: ", "*** Delete File: ", "*** Move to: "))][:16]
except (ValueError, TypeError, AttributeError):
    record["input_schema"] = "not-readable-native-object"


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
event = "UnknownNckhEvent" if mode == "unsupported-codec" else args.event
context = "context-deny.json" if mode == "policy-deny" else "context-uncovered.json" if mode == "uncovered-tool" else "context-allow.json"
argv = [sys.executable, "-I", str(args.runner), "--host", "codex", "--event", event, "--project", str(args.project),
        "--context", (args.evidence.relative_to(args.project) / context).as_posix(), "--receipt-dir", args.evidence.relative_to(args.project).as_posix() + "/policy-receipts/" + control["attempt"] + "/" + args.event]
process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           creationflags=subprocess.CREATE_NO_WINDOW)
record["runner_pid"] = process.pid
save()
try:
    stdout, stderr = process.communicate(b"{" if mode == "malformed-input" else data, timeout=5)
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
try:
    record["runner_output"] = json.loads(stdout)
except ValueError:
    record["runner_output"] = "invalid-json"
save()
sys.stdout.buffer.write(stdout)
sys.stderr.buffer.write(stderr)
sys.exit(process.returncode)
