"""Identify impossible parent ancestry without treating unrelated applications as owned."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}
inspection = read(RUN / "live-process-identity-inspection.json")
precision = read(RUN / "process-exit-precision-audit.json")
original = read(RUN / "process-final-audit.json")
snapshots = [
    RUN / "commands/native-cursor-grep-faults.process-tree.json",
    RUN / "commands/native-cursor-grep-faults.process-tree.json.writing",
    RUN.parent / "nckh-native-261005-2320-r37-agy-event-controls-attempt-34/commands/agy-tools-stop-malformed-input.process-tree.json",
    RUN.parent / "nckh-native-261006-0400-r37-cursor-directory-denial-attempt-50/commands/native-cursor-directory-denial.process-tree.json",
    RUN.parent / "nckh-native-261006-0330-r37-agy-tool-route-inspection-attempt-46/commands/agy-agents-help.process-tree.json",
    RUN.parent / "nckh-native-261006-0215-r37-cursor-workspace-startup-attempt-43/commands/native-cursor-workspace-startup.process-tree.json",
]
data = []
for path in snapshots:
    value = read(path)
    roots = [row for row in value["processes"] if row["pid"] == value["root_pid"]]
    assert len(roots) == 1
    root_ticks = value.get("root_creation_filetime_ticks", roots[0]["creation_filetime_ticks"])
    assert root_ticks == roots[0]["creation_filetime_ticks"]
    data.append((path, value, root_ticks))
classified = []
for live in inspection["rows"]:
    assert live["matches_retained_precision"]
    assert not live["command_contains_work"] and not live["command_contains_current_run"]
    witnesses = []
    for path, value, root_ticks in data:
        matches = [row for row in value["processes"] if row["pid"] == live["pid"] and
                   abs(row["creation_filetime_ticks"] - live["creation_filetime_ticks"]) <= 9]
        for row in matches:
            assert row["creation_filetime_ticks"] < root_ticks, "Need further ownership evidence for this live identity"
            witnesses.append({"snapshot": bind(path), "root_pid": value["root_pid"], "root_ticks": root_ticks,
                              "recorded_process_ticks": row["creation_filetime_ticks"],
                              "created_before_root_seconds": (root_ticks - row["creation_filetime_ticks"]) / 10000000})
    assert witnesses, "Missing bound temporal counterevidence"
    classified.append({"pid": live["pid"], "name": live["name"], "creation_filetime_ticks": live["creation_filetime_ticks"],
                       "classification": "preexisting-process-impossible-as-descendant-of-retained-test-root",
                       "witnesses": witnesses, "process_stop_performed": False})
assert len(classified) == precision["matching_identity_count"] == 27
current = data[0][1]
current_tail = data[1][1]
root_ticks = data[0][2]
rows = {str(row["pid"]) + ":" + str(row["creation_filetime_ticks"]): row
        for value in (current, current_tail) for row in value["processes"]}
owned = {key: row for key, row in rows.items() if row["pid"] == current["root_pid"] and row["creation_filetime_ticks"] == root_ticks}
assert len(owned) == 1
while True:
    new = {key: row for key, row in rows.items() if key not in owned and
           any(parent["pid"] == row["parent_pid"] and parent["creation_filetime_ticks"] <= row["creation_filetime_ticks"]
               for parent in owned.values())}
    if not new:
        break
    owned.update(new)
owned_live = [identity for identity in precision["identities"] if identity["matches_within_cim_microsecond_precision"] and
              any(row["pid"] == identity["pid"] and abs(row["creation_filetime_ticks"] - identity["recorded_ticks"]) <= 9
                  for row in owned.values())]
assert not owned_live
result = {
    "status": "verified-scoped-native51-process-exit-with-historical-capture-correction",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(), "raw_identity_union": len(original["tracked"]),
    "raw_precision_live_matches": 27, "preexisting_applications_preserved": 27,
    "current_temporally_valid_captured_identities": len(owned),
    "current_snapshot_rows_rejected": len(rows) - len(owned),
    "current_scoped_owned_live": 0, "current_project_command_matches": original["matching_count"],
    "native_terminal_exit_code": read(RUN / "terminal-exit-poll-01.json")["exit_code"],
    "monitor_exit_code": read(RUN / "monitor-exit.json")["exit_code"],
    "continuous_monitor_success": False, "continuous_capture_after_failure": "unverified",
    "causes": [
        "tree traversal expands parent PID without requiring child creation after the retained parent",
        "FILETIME exact comparison against CIM microsecond timestamps can falsely classify a live process as a reused PID",
        "monitor os.replace WinError5 is preserved; the exact lock holder is unestablished"
    ],
    "historical_raw_zero_live_claim": "not-currently-qualified; source records preserved without regrading",
    "classified_live": classified,
    "owned_identity_keys": list(owned), "process_stop_performed": False, "global_direct_writes": False,
    "bindings": [bind(RUN / filename) for filename in (
        "monitor-exit.json", "original-verification-result.json", "process-final-audit.json",
        "process-exit-precision-audit.json", "live-process-identity-inspection.json")],
    "classifier": bind(Path(__file__))
}
target = RUN / "process-ownership-correction.json"
with target.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": result["status"], "raw_union": result["raw_identity_union"],
                  "preexisting_preserved": 27, "current_scoped_live": 0,
                  "temporal_owned": len(owned), "rejected_current_rows": result["current_snapshot_rows_rejected"]}))
