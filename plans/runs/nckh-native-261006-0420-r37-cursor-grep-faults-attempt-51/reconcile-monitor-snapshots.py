"""Retain the monitor failure and reconcile captured identities without rerunning native cases."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}
failed = read(RUN / "monitor-exit.json")
assert failed["exit_code"] == 1 and "WinError 5" in failed["output"]
assert read(RUN / "terminal-exit-poll-01.json")["exit_code"] == 0
ownership = read(RUN / "native-process-ownership.json")
retained = [
    RUN / "commands/native-cursor-grep-faults.process-tree.json",
    RUN / "commands/native-cursor-grep-faults.process-tree.json.writing",
    RUN / "process-tree-start.json",
    RUN / "process-tree-progress.json",
    RUN / "process-tree-before-stop.json",
]
identities = {}
snapshots = []
for path in retained:
    value = read(path)
    assert value["root_pid"] == ownership["root_pid"]
    rows = []
    for original in value["processes"]:
        row = dict(original)
        if "ProcessId" in row:
            utc = datetime.fromisoformat(row["creation_utc"])
            delta = utc - datetime(1601, 1, 1, tzinfo=timezone.utc)
            ticks = (delta.days * 86400 + delta.seconds) * 10000000 + delta.microseconds * 10
            row = {"pid": row["ProcessId"], "parent_pid": row["ParentProcessId"], "name": row["Name"],
                   "creation_utc": row["creation_utc"], "creation_filetime_ticks": ticks}
        key = str(row["pid"]) + ":" + str(row["creation_filetime_ticks"])
        identities[key] = row
        rows.append(key)
    snapshots.append({"binding": bind(path), "status": value.get("status"),
                      "captured_at": value.get("captured_at", value.get("timestamp_utc")), "identities": len(rows)})
target = RUN / "commands/monitor-retained-snapshots.process-tree.json"
assert not target.exists()
record = {
    "status": "retained-identities-reconciled-monitor-error-preserved",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "root_pid": ownership["root_pid"], "processes": list(identities.values()), "capture_errors": [],
    "capture_errors_scope": "snapshot parsing and identity merge only; no new continuous process capture",
    "snapshot_bindings": snapshots, "monitor_exit": bind(RUN / "monitor-exit.json"),
    "native_exit": bind(RUN / "terminal-exit-poll-01.json"),
    "monitor_terminal_success": False,
    "continuous_capture_after_failure": "unverified",
    "process_stop_performed": False, "native_or_model_retry": False,
    "cause": "native monitor os.replace failed with WinError5; exact lock holder and cause not established",
    "verification_scope": "merge existing PID/creation observations for a subsequent read-only live CIM audit",
    "reconciler": bind(Path(__file__))
}
with target.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": record["status"], "retained_identities": len(identities), "snapshots": len(snapshots)}))
