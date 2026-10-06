"""Return one controller-owned plugin path only after a genuine workspace callback."""

import argparse
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--project", type=Path, required=True)
parser.add_argument("--plugin", type=Path, required=True)
parser.add_argument("--evidence", type=Path, required=True)
args = parser.parse_args()
raw = sys.stdin.buffer.read(65537)
native = json.loads(raw)
assert len(raw) <= 65536 and isinstance(native, dict)
assert native.get("hook_event_name") == "workspaceOpen"
roots = native.get("workspace_roots")
assert isinstance(roots, list) and any(Path(root).resolve() == args.project.resolve() for root in roots)
args.plugin.resolve().relative_to(args.project.resolve())
assert args.plugin.is_dir()
output = json.dumps({"pluginPaths": [str(args.plugin.resolve())]}, separators=(",", ":")).encode()
record = {
    "event": "workspaceOpen", "callback_source": "project", "fault_origin": "none",
    "status": "completed-genuine-workspace-input", "native_version": native.get("cursor_version"),
    "input_fields": sorted(native), "input_size": len(raw), "input_sha256": hashlib.sha256(raw).hexdigest(),
    "workspace_contains_selected_project": True, "returned_plugin_paths": 1,
    "plugin_root_hash": hashlib.sha256(str(args.plugin.resolve()).encode()).hexdigest(),
    "output_sha256": hashlib.sha256(output).hexdigest(), "observer_pid": os.getpid(), "parent_pid": os.getppid(),
    "completed_at_utc": datetime.now(timezone.utc).isoformat(), "observer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
target = args.evidence / "observations/workspaceOpen" / (uuid.uuid4().hex + ".json")
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
sys.stdout.buffer.write(output)

