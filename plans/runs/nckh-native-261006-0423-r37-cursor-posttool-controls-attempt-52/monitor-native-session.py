"""Observe one owned Cursor process generation; preserve terminal capture errors."""
import importlib.util
import json
import time
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("native_capture", RUN / "native-process-capture.py")
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
selected = read(RUN / "native-root-selection.json")
start = read(RUN / "terminal-start.json")
ticks = capture.creation_ticks(selected["pid"])
assert ticks is not None and abs(ticks-selected["creation_cim_ticks"]) <= 9
owner_path = RUN / "native-process-ownership.json"
assert not owner_path.exists()
ownership = {"root_pid":selected["pid"],"root_creation_filetime_ticks":ticks,"creation_utc":selected["creation_utc"],
    "session_id":start["session_id"],"project":selected["project"],"owner":"/root","port":None,"worktree":selected["project"],
    "command":"Cursor interactive --force --trust --sandbox disabled; existing selectedModel",
    "model":"grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]","generation_binding":"CIM selection plus exact GetProcessTimes"}
capture.save(owner_path,ownership)
root = selected["pid"]
identities, errors = {}, []
target = RUN / "commands/native-cursor-posttool.process-tree.json"
assert not target.exists()
try:
    while capture.creation_ticks(root) == ticks:
        try:
            rows = capture.tree(root,ticks)
        except ValueError:
            if capture.creation_ticks(root) != ticks:
                break
            raise
        for row in rows:
            identities[str(row["pid"])+":"+str(row["creation_filetime_ticks"])] = row
        capture.save(target,{"root_pid":root,"root_creation_filetime_ticks":ticks,"processes":list(identities.values()),
            "capture_errors":[],"status":"running","temporal_parent_identity":True,"captured_at":datetime.now(timezone.utc).isoformat()})
        time.sleep(0.25)
    capture.save(target,{"root_pid":root,"root_creation_filetime_ticks":ticks,"processes":list(identities.values()),
        "capture_errors":[],"status":"root-exited-or-reused","temporal_parent_identity":True,"captured_at":datetime.now(timezone.utc).isoformat()})
except Exception as error:
    errors.append(type(error).__name__+": "+str(error))
    failure=RUN / "monitor-failure.json"
    assert not failure.exists()
    failure.write_text(json.dumps({"root_pid":root,"root_creation_filetime_ticks":ticks,"error":errors[-1],
        "timestamp_utc":datetime.now(timezone.utc).isoformat(),"retained_identity_count":len(identities),"native_restart":False},indent=2)+"\n",encoding="utf8")
    raise
print(json.dumps({"status":"root-exited-or-reused","identities":len(identities),"errors":errors}),flush=True)
