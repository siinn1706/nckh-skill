"""Bounded diagnostic callback; deliberately no NCKH policy or runner invocation."""

import argparse
import atexit
import hashlib
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--event", required=True)
parser.add_argument("--evidence", type=Path, required=True)
args = parser.parse_args()
started = time.perf_counter()
payload = sys.stdin.buffer.read(65537)
native = json.loads(payload)
assert isinstance(native, dict)
target = args.evidence / "immediate-observations" / args.event / (uuid.uuid4().hex + ".json")
target.parent.mkdir(parents=True, exist_ok=True)
wire = {"permission": "allow"} if args.event == "preToolUse" else {}
record = {"status": "native-diagnostic-callback", "event": args.event,
    "reported_event": native.get("hook_event_name"), "input_fields": sorted(native),
    "input_sha256": hashlib.sha256(payload).hexdigest(), "input_size": len(payload),
    "pid": os.getpid(), "parent_pid": os.getppid(), "entered_at": datetime.now(timezone.utc).isoformat(),
    "native_tool_name": native.get("tool_name"), "native_tool_use_id": native.get("tool_use_id"),
    "native_model": native.get("model"), "native_version": native.get("cursor_version"),
    "wire": wire, "runner_invoked": False, "policy_invoked": False,
    "evidence_class": "native-timing-diagnostic-only"}


def save():
    target.write_text(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf8")


def on_exit():
    record.update(status="interpreter-atexit-observed", atexit_at=datetime.now(timezone.utc).isoformat(),
        interpreter_elapsed_seconds=time.perf_counter() - started)
    save()


atexit.register(on_exit)
save()
print(json.dumps(wire), flush=True)
record.update(status="output-flushed", output_flushed_at=datetime.now(timezone.utc).isoformat(),
    output_elapsed_seconds=time.perf_counter() - started)
save()
