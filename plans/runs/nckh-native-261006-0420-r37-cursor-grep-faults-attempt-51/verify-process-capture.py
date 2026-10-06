"""Focused controller checks; synthetic lineage fixtures are not host-hook evidence."""
import hashlib
import importlib.util
import json
import os
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
spec = importlib.util.spec_from_file_location("process_capture", RUN / "native-process-capture.py")
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}
row = lambda pid, parent, ticks: {"pid": pid, "parent_pid": parent, "creation_filetime_ticks": ticks, "name": "declared-synthetic"}
rows = [row(10, 1, 100), row(20, 10, 120), row(30, 20, 140), row(40, 10, 90), row(50, 40, 95), row(60, 99, 160)]
assert {entry["pid"] for entry in capture.select_temporal_descendants(rows, 10, 100)} == {10, 20, 30}
for malformed, expected in ((rows, 99), (rows + [row(20, 1, 80)], 100)):
    try:
        capture.select_temporal_descendants(malformed, 10, expected)
    except ValueError:
        pass
    else:
        raise AssertionError("Unbound or ambiguous generation was admitted")
pid = os.getpid()
ticks = capture.creation_ticks(pid)
assert ticks is not None
actual = capture.tree(pid, ticks)
assert any(entry["pid"] == pid and entry["creation_filetime_ticks"] == ticks for entry in actual)
for entry in actual:
    if entry["pid"] != pid:
        parent = next(item for item in actual if item["pid"] == entry["parent_pid"])
        assert entry["creation_filetime_ticks"] >= parent["creation_filetime_ticks"]
write_path = RUN / "controller-atomic-write-control.json"
assert not write_path.exists()
capture.save(write_path, {"purpose": "controller-local-write-check", "generation": 1})
capture.save(write_path, {"purpose": "controller-local-write-check", "generation": 2})
assert json.loads(write_path.read_text(encoding="utf8"))["generation"] == 2
assert not list(RUN.glob("controller-atomic-write-control.json.writing-*"))
record = {
    "status": "verified-focused-controller-process-capture-checks",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "checks": ["reject preexisting child and its subtree", "retain actual temporal child chain",
               "reject mismatched root generation", "reject ambiguous PID generations",
               "observe current checker root identity", "atomic same-directory write roundtrip"],
    "synthetic_scope": "declared lineage regression fixtures only",
    "real_process_scope": "current checker process; no native host or model",
    "maximum_atomic_commit_attempts": 6, "maximum_retry_delay_seconds": 0.775,
    "WinError5_cause_or_reproduction": "not-established",
    "native_oracle_regraded": False, "model_prompts": 0, "source_kit_modified": False,
    "process_stop_performed": False, "current_process_pid": pid, "current_process_ticks": ticks,
    "bindings": [bind(RUN / "native-process-capture.py"), bind(RUN / "owned-cli-command.py"),
                 bind(write_path), bind(Path(__file__))],
    "future_wiring": "explicit expected root creation ticks required; retain terminal errors and independent precision/ownership audit",
}
with (RUN / "verified-process-capture-checks.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": record["status"], "checks": len(record["checks"]), "native_prompts": 0}))
