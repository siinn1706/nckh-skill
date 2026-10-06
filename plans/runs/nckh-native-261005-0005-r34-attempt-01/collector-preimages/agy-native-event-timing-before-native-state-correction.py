"""Interpret retained native tool states and actual callback order; preserve raw receipts."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
SUMMARY = RUN / "agy-native-event-fault-summary.json"
OUT = RUN / "agy-native-event-timing.json"
if OUT.exists():
    raise RuntimeError("Preserve the previous native timing interpretation")
read = lambda path: json.loads(path.read_text(encoding="utf8"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
summary = read(SUMMARY)
assert summary["status"] == "recorded-genuine-callbacks" and len(summary["results"]) == 25
project = Path(summary["project"])
rows = []
for item in summary["results"]:
    attempt_path = RUN / item["attempt_receipt"]
    attempt = read(attempt_path)
    stdout = RUN / "commands" / ("agy-native-" + item["attempt"] + ".stdout.txt")
    frames = [json.loads(line) for line in stdout.read_text(encoding="utf8").splitlines()]
    terminal = [frame["step_update"] for frame in frames if frame.get("event") == "step_update"
                and frame.get("step_update", {}).get("step_type") == "tool"
                and frame["step_update"].get("state") in {"DONE", "ERROR"}]
    assert len(terminal) == 1 and terminal[0]["tool_name"] == "run_command"
    callbacks = sorted([read(project / relative) for relative in attempt["observations"]], key=lambda row: row["started_at"])
    pretool = [row for row in callbacks if row["event"] == "PreToolUse"]
    posttool = [row for row in callbacks if row["event"] == "PostToolUse"]
    assert len(pretool) == 1 and pretool[0]["native_command_sha256"] == attempt["oracle_command_sha256"]
    selected = [row for row in callbacks if row["event"] == item["event"] and row["fault_selected"]]
    ordering = []
    for row in selected:
        if row["event"] == "PreToolUse":
            position = "pre-tool-callback"
        elif row["started_at"] < pretool[0]["started_at"]:
            position = "before-pre-tool-callback"
        elif posttool and row["started_at"] >= posttool[0]["started_at"]:
            position = "at-or-after-post-tool-callback"
        else:
            position = "after-pre-tool-callback-no-post-tool-callback-observed"
        ordering.append(position)
    error = terminal[0].get("tool_info", {}).get("error", {}).get("message")
    if item["event"] == "PreToolUse":
        assert terminal[0]["state"] == "ERROR" and not item["oracle_created"] and error
        native_outcome = "native-tool-error-before-marker"
    else:
        assert terminal[0]["state"] == "DONE" and item["oracle_created"]
        native_outcome = "native-tool-completed-marker-preserved"
    rows.append({"event": item["event"], "fault": item["fault"], "attempt": item["attempt"],
        "native_tool_state": terminal[0]["state"], "native_error": error, "native_outcome": native_outcome,
        "oracle_created": item["oracle_created"], "selected_callback_positions": ordering,
        "callback_order": [{"event": row["event"], "started_at": row["started_at"], "observer_pid": row["observer_pid"]}
                           for row in callbacks],
        "command_matches_authorized_oracle": True, "attempt_sha256": sha(attempt_path), "stdout_sha256": sha(stdout)})
result = {"status": "recorded-native-tool-states-and-order", "source_revision": 34,
    "source_lock_hash": summary["source_lock_hash"], "raw_summary_sha256": sha(SUMMARY), "results": rows,
    "metadata_correction": {
        "field": "effect_timing", "raw_summary_preserved": True,
        "original": summary["effect_timing"],
        "interpretation": "PreToolUse precedes the native tool; PostToolUse follows it. PreInvocation/PostInvocation wrap each model invocation and occur both before and after the tool in these turns. Stop follows the final response. Use observed callback order, not the original broad post-event description."},
    "qualification": "specific native event/version/tool observations; full host/surface gate remains open"}
OUT.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf8")
print(json.dumps({"status": result["status"], "cases": len(rows), "native_tool_errors": sum(row["native_tool_state"] == "ERROR" for row in rows),
                  "completed_native_tools": sum(row["native_tool_state"] == "DONE" for row in rows), "raw_summary_preserved": True}))
