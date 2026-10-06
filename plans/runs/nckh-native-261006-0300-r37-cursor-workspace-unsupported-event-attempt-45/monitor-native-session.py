"""Track exact Windows child identities until the owned terminal exits."""
import importlib.util
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("session_owned", RUN / "owned-cli-command.py")
owned = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owned)
record = json.loads((RUN / "native-process-ownership.json").read_text(encoding="utf8"))
root = record["root_pid"]
ticks = owned.creation_ticks(root)
assert ticks is not None
expected_utc = datetime.fromisoformat(record["creation_utc"])
assert abs((datetime(1601, 1, 1, tzinfo=timezone.utc) + __import__('datetime').timedelta(microseconds=ticks // 10) - expected_utc).total_seconds()) < 0.000001
identities = {}
target = RUN / "commands/native-cursor-workspace-unsupported.process-tree.json"
assert not target.exists()
while owned.creation_ticks(root) == ticks:
    for row in owned.tree(root):
        identities[str(row["pid"]) + ":" + str(row["creation_filetime_ticks"])] = row
    owned.save(target, {"root_pid": root, "root_creation_filetime_ticks": ticks,
        "processes": list(identities.values()), "capture_errors": [], "status": "running",
        "captured_at": datetime.now(timezone.utc).isoformat()})
    time.sleep(0.25)
owned.save(target, {"root_pid": root, "root_creation_filetime_ticks": ticks,
    "processes": list(identities.values()), "capture_errors": [], "status": "root-exited-or-reused",
    "captured_at": datetime.now(timezone.utc).isoformat()})
print(json.dumps({"root_exited": True, "identities": len(identities)}), flush=True)
