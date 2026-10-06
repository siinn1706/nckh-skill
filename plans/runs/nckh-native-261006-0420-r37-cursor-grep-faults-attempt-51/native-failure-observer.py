"""Capture bounded synthetic Read failure metadata without invoking policy or tools."""

import argparse
import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--evidence", type=Path, required=True)
parser.add_argument("--project", type=Path, required=True)
parser.add_argument("--selected-relative", required=True)
args = parser.parse_args()
data = os.fdopen(os.dup(0), "rb").read(65537)
sha = lambda value: hashlib.sha256(value).hexdigest()
record = {"status": "entered-from-native-failure-hook", "started_at": datetime.now(timezone.utc).isoformat(),
          "observer_pid": os.getpid(), "parent_pid": os.getppid(), "input_size": len(data), "input_sha256": sha(data),
          "fault_origin": "none", "policy_invoked": False, "full_transcript_read": False}
try:
    native = json.loads(data)
    if not isinstance(native, dict) or len(data) > 65536:
        raise ValueError("bounded native object unavailable")
    fields = native.get("tool_input", {})
    selected = (args.project / args.selected_relative).resolve()
    path = fields.get("file_path", fields.get("path")) if isinstance(fields, dict) else None
    selected_read = native.get("tool_name") == "Grep" and isinstance(path, str) and Path(path).resolve() == selected
    message = native.get("error_message", "")
    message = message if isinstance(message, str) else ""
    scrubbed = message.replace(str(args.project), "<owned-project>").replace(str(Path.home()), "<user-home>")[:2000]
    roots = native.get("workspace_roots", [])
    record.update(input_fields=sorted(native), reported_event=native.get("hook_event_name"),
                  native_version=native.get("cursor_version"), native_tool_name=native.get("tool_name"),
                  native_tool_use_id=native.get("tool_use_id"), native_session_hash=sha(str(native.get("conversation_id")).encode()),
                  failure_type=native.get("failure_type"), duration=native.get("duration"), is_interrupt=native.get("is_interrupt"),
                  workspace_contains_selected_project=isinstance(roots, list) and any(isinstance(root, str) and
                    Path(root).resolve() == args.project.resolve() for root in roots),
                  selected_path_matches=selected_read, native_error_sha256=sha(message.encode()),
                  scrubbed_selected_error=scrubbed if selected_read else "not-retained-for-unexpected-tool-or-path",
                  tool_input_fields=sorted(fields) if isinstance(fields, dict) else [])
except (ValueError, TypeError, OSError):
    record["input_schema"] = "unreadable-or-oversized-native-object"
record["status"] = "completed-native-failure-metadata-observation"
directory = args.evidence / "native-failures"
directory.mkdir(parents=True, exist_ok=True)
target = directory / (uuid.uuid4().hex + ".json")
temporary = target.with_suffix(".tmp")
temporary.write_text(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf8")
os.replace(temporary, target)
print("{}", flush=True)
