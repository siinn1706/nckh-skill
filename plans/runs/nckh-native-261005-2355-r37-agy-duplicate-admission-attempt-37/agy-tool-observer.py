"""Record bounded native callbacks; faults are explicit controller test injections."""

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
parser.add_argument("--host", choices=["cursor", "agy"], required=True)
parser.add_argument("--event", required=True)
parser.add_argument("--project", type=Path, required=True)
parser.add_argument("--evidence", type=Path, required=True)
parser.add_argument("--runner", type=Path, required=True)
parser.add_argument("--callback-source", choices=["project", "plugin"], default="project")
args = parser.parse_args()
control_path = args.evidence / "probe-control.json"
control = json.loads(control_path.read_text(encoding="utf8"))
mode = control["mode"]
fault = args.event == control.get("selected_event")
target = args.evidence / "observations" / control["attempt"] / args.event / (uuid.uuid4().hex + ".json")
target.parent.mkdir(parents=True, exist_ok=True)
data = sys.stdin.buffer.read(65537)
sha = lambda value: hashlib.sha256(value).hexdigest()
record = {"schema_version": 1, "host": args.host, "event": args.event, "mode": mode,
          "callback_source": args.callback_source,
          "attempt": control["attempt"], "started_at": datetime.now(timezone.utc).isoformat(),
          "status": "entered-from-native-host", "observer_pid": os.getpid(), "parent_pid": os.getppid(),
          "input_size": len(data), "input_sha256": sha(data), "control_sha256": sha(control_path.read_bytes()),
          "runner_sha256": sha(args.runner.read_bytes()), "fault_selected": fault,
          "fault_origin": "controller-injection-after-genuine-callback" if fault and mode not in
          {"allow", "policy-deny", "uncovered-tool", "duplicate"} else "none"}
try:
    native = json.loads(data)
    roots = native.get("workspace_roots", native.get("workspacePaths", []))
    call = native.get("toolCall", {})
    fields = native.get("tool_input", call.get("args", {}))
    record.update(input_fields=sorted(native), reported_event=native.get("hook_event_name"),
                  native_model=native.get("model", native.get("modelName")),
                  native_model_id=native.get("model_id"), native_model_params=native.get("model_params"),
                  native_version=native.get("cursor_version"),
                  native_tool_name=native.get("tool_name", call.get("name")),
                  native_tool_use_id=native.get("tool_use_id"), native_step_idx=native.get("stepIdx"), execution_num=native.get("executionNum"),
                  native_session_hash=sha(str(native.get("conversation_id", native.get("conversationId"))).encode()),
                  tool_input_fields=sorted(fields) if isinstance(fields, dict) else [],
                  workspace_contains_selected_project=any(str(Path(root).resolve()).casefold() ==
                  str(args.project.resolve()).casefold() for root in roots))
    if isinstance(fields, dict):
        record["native_path_fields"] = {key: value for key, value in fields.items() if isinstance(value, str) and key in {"path", "file_path", "filePath", "target_path", "targetFile", "TargetFile", "AbsolutePath", "DirectoryPath", "SearchDirectory", "SearchPath"}}
        command = fields.get("command", fields.get("CommandLine"))
        if isinstance(command, str):
            record["native_command_sha256"] = sha(command.encode())
            record["oracle_name_in_native_command"] = "oracle.txt" in command
except (ValueError, TypeError, AttributeError, OSError):
    record["input_schema"] = "not-readable-native-json-object"


def save():
    target.write_text(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf8")


save()
if fault and mode == "crash":
    record["status"] = "intentional-test-crash-exit-17"
    save()
    os._exit(17)
if fault and mode == "timeout":
    record["status"] = "intentional-test-sleep-eight-seconds"
    save()
    time.sleep(8)
if fault and mode == "malformed-output":
    record["status"] = "intentional-test-malformed-output"
    save()
    print("[invalid-native-hook-output", flush=True)
    sys.exit(0)
selected_event = "UnknownNckhEvent" if fault and mode == "unsupported-codec" else args.event
context = control["deny_context"] if fault and mode == "policy-deny" else control["allow_context"]
command = [sys.executable, "-I", str(args.runner), "--host", args.host, "--event", selected_event,
           "--project", str(args.project), "--context", (args.evidence.relative_to(args.project) / context).as_posix(),
           "--receipt-dir", args.evidence.relative_to(args.project).as_posix() + "/policy-receipts/" + control["attempt"] + "/" + args.event]
process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           creationflags=subprocess.CREATE_NO_WINDOW)
record["runner_pid"] = process.pid
save()
try:
    stdout, stderr = process.communicate(b"{" if fault and mode == "malformed-input" else data, timeout=5)
except subprocess.TimeoutExpired:
    process.terminate()
    try:
        stdout, stderr = process.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate(timeout=5)
    record["runner_timeout"] = True
record.update(status="completed", runner_exit_code=process.returncode, runner_exited=process.poll() is not None,
              output_sha256=sha(stdout), stderr_sha256=sha(stderr), completed_at=datetime.now(timezone.utc).isoformat())
try:
    record["runner_output"] = json.loads(stdout)
except ValueError:
    record["runner_output"] = "invalid-json"
save()
sys.stdout.buffer.write(stdout)
sys.stderr.buffer.write(stderr)
sys.exit(process.returncode)
