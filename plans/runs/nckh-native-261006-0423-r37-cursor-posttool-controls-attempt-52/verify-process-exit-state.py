"""Observe a real owned process while retaining its handle after termination."""
import ctypes
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from ctypes import wintypes
from datetime import datetime, timezone
from pathlib import Path

RUN=Path(__file__).resolve().parent
WORK=RUN.parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
state=load("exit_state",RUN / "native-process-state.py")
legacy=load("legacy_times",RUN / "owned-cli-command.py")
started=datetime.now(timezone.utc).isoformat()
process=subprocess.Popen([sys.executable,"-X","utf8","-B","-c","import time; time.sleep(0.5)"],
    cwd=RUN,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
before=state.state(process.pid)
assert before["status"] == "active"
assert state.active_generation(process.pid,before["creation_filetime_ticks"])
state.kernel.WaitForSingleObject.argtypes=[wintypes.HANDLE,wintypes.DWORD]
state.kernel.WaitForSingleObject.restype=wintypes.DWORD
wait=state.kernel.WaitForSingleObject(int(process._handle),5000)
assert wait == 0, "Owned checker did not terminate"
after=state.state(process.pid)
legacy_after=legacy.creation_ticks(process.pid)
assert after["status"] == "terminated" and after["exit_code"] == 0
assert after["creation_filetime_ticks"] == before["creation_filetime_ticks"]
assert not state.active_generation(process.pid,before["creation_filetime_ticks"])
stdout,stderr=process.communicate(timeout=5)
assert process.returncode == 0 and not stdout and not stderr
current=state.state(os.getpid())
assert current["status"] == "active"
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
bind=lambda path:{"path":path.relative_to(WORK).as_posix(),"sha256":sha(path)}
record={"status":"verified-real-owned-process-exit-state-control","started_utc":started,
    "ended_utc":datetime.now(timezone.utc).isoformat(),"before":before,"after_with_handle_retained":after,
    "legacy_creation_ticks_after_exit":legacy_after,"legacy_times_can_remain_queryable":legacy_after == before["creation_filetime_ticks"],
    "actual_process_exit_code":process.returncode,"process_stop_performed":False,"native_model_prompts":0,
    "scope":"one controller-owned non-model Python process; actual GetExitCodeProcess observation",
    "native52_monitor_failure_regraded":False,"native52_closing_race_cause":"supported inference; raw native failure preserved",
    "bindings":[bind(RUN / "native-process-state.py"),bind(RUN / "owned-cli-command.py"),bind(Path(__file__))]}
with (RUN / "verified-process-exit-state-control.json").open("x",encoding="utf8") as stream:
    stream.write(json.dumps(record,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"status":record["status"],"actual_exit":0,"creation_times_still_queryable":record["legacy_times_can_remain_queryable"],
    "active_after_exit":False,"model_prompts":0}))
