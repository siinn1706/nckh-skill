"""Bind actual callbacks and retain the frozen oracle before matching-file cleanup."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}

def write_new(path, value):
    with path.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

prepared = read(RUN / "preparation.json")
project = Path(prepared["project"])
evidence = Path(prepared["evidence"])
audit = read(RUN / "process-final-audit.json")
assert audit["matching_count"] == audit["tracked_live_count"] == 0
assert read(RUN / "terminal-exit-poll.json")["exit_code"] == 0
assert read(RUN / "monitor-exit.json")["exit_code"] == 0
assert read(RUN / "terminal-startup-window.json")["wall_time_seconds"] >= prepared["startup_observation_seconds"]
assert "--plugin-dir" not in prepared["argv"] and prepared["maximum_model_turns"] == 0
rows = [(path, read(path)) for path in (evidence / "observations").rglob("*.json")]
unsupported = [(path, row) for path, row in rows if row.get("selected_codec_event") == "workspaceOpen"]
diagnostic = [(path, row) for path, row in rows if row.get("status") == "completed-genuine-workspace-input"]
lifecycle = [(path, row) for path, row in rows if row["event"] == "sessionStart"]
receipts = [(path, read(path)) for path in (evidence / "policy-receipts").rglob("*.json")]
failed = [(path, row) for path, row in receipts if row["status"] == "degraded-failed"]
startup = [(path, row) for path, row in receipts if row.get("phase") == "advisory"]
checks = {
    "four_callbacks_only": len(rows) == 4 and {row["event"] for _, row in rows} == {"workspaceOpen", "sessionStart"},
    "one_genuine_unsupported_workspace_forward": len(unsupported) == 1,
    "one_separate_workspace_route_diagnostic": len(diagnostic) == 1,
    "two_same_input_sessionStart_callbacks": len(lifecycle) == 2 and {row["callback_source"] for _, row in lifecycle} == {"project", "plugin"}
        and len({row["input_sha256"] for _, row in lifecycle}) == 1 and len({row["native_session_hash"] for _, row in lifecycle}) == 1,
    "sessionStart_runner_completed_exit_zero": len(lifecycle) == 2 and all(row["status"] == "completed" and row["reported_event"] == "sessionStart"
        and row["runner_exit_code"] == 0 and row["runner_exited"] and row["fault_origin"] == "none" for _, row in lifecycle),
    "two_policy_receipts": len(receipts) == 2 and len(failed) == len(startup) == 1,
    "current_native_version": all(row.get("native_version") == "2026.09.15-d2fe57e" for _, row in rows),
}
if len(unsupported) == 1:
    row = unsupported[0][1]
    checks["unchanged_native_input_and_actual_selector"] = row["reported_event"] == row["selected_codec_event"] == row["event"] == "workspaceOpen"
    checks["no_fault_injection"] = row["fault_origin"] == "none" and row["input_bytes_modified"] is False and row["input_sha256"] == row["forwarded_input_sha256"]
    checks["unsupported_runner_completed_exit_three_empty_object"] = row["status"] == "completed" and row["runner_exit_code"] == 3
    checks["unsupported_runner_output_empty_object"] = row["runner_output"] == {} and row["runner_exited"] and not row.get("runner_timeout", False)
    if len(failed) == 1:
        receipt = failed[0][1]
        checks["failure_receipt_bound_to_native_input"] = receipt["event_hash"] == row["input_sha256"]
        checks["failure_receipt_exact_reason_no_decoded_context"] = receipt["decision"] == "block" and receipt["reason_codes"] == ["hook-input-or-context-invalid"]
        checks["no_decoded_phase_or_context_in_failed_receipt"] = not any(key in receipt for key in ("phase", "context_hash", "session_key", "task_key"))
    if len(diagnostic) == 1:
        checks["workspace_handlers_same_native_input"] = diagnostic[0][1]["input_sha256"] == row["input_sha256"]
        checks["route_diagnostic_returns_one_owned_plugin"] = diagnostic[0][1]["workspace_contains_selected_project"] and diagnostic[0][1]["returned_plugin_paths"] == 1
    if len(lifecycle) == 2:
        completion = datetime.fromisoformat(row["completed_at_utc"])
        checks["lifecycle_started_after_unsupported_runner_completion"] = all(datetime.fromisoformat(item["started_at"]) >= completion for _, item in lifecycle)

protected = []
for row in prepared["protected_configs"]:
    path = Path(row["path"])
    current = sha(path) if path.is_file() else None
    assert current == row["sha256"], "Protected config changed; retain before cleanup"
    protected.append({**row, "current_sha256": current})
historical = read(RUN / "historical-project-preimage.json")["members"]
assert all(sha(project / relative) == expected for relative, expected in historical.items())
for row in prepared["owned_files"]:
    target = project / row["path"]
    target.resolve().relative_to(project.resolve())
    assert sha(target) == row["sha256"], "Owned file changed; preserve cleanup conflict"
record = {
    "status": "verified-genuine-kit-unsupported-event-startup-continuation" if all(checks.values()) else "failed-frozen-startup-oracle-retained",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(), "source_revision": 37, "source_lock_hash": prepared["source_lock_hash"],
    "surface": "cursor-cli-interactive", "version": "2026.09.15-d2fe57e", "frozen_oracle_checks": checks,
    "callbacks": [bind(path) for path, _ in rows], "policy_receipts": [bind(path) for path, _ in receipts],
    "event_scope": prepared["event_scope"], "fault_origin": "none", "controller_model_prompts": 0, "controller_tool_requests": 0,
    "unsupported_callback_count": len(unsupported), "route_diagnostic_callback_count": len(diagnostic), "lifecycle_callback_count": len(lifecycle),
    "native_startup": "actual sessionStart callbacks and interactive readiness after workspace codec exit3",
    "mutation_prevention_qualification": "not-tested; zero model/tool requests", "unknown_host_event_qualification": "unverified",
    "instrumentation_timeouts": {"outer_seconds": 5, "inner_seconds": 5}, "default_enforcement_qualification": "unverified",
    "preparation": bind(RUN / "preparation.json"), "frozen_brief": bind(RUN / "frozen-brief.json"),
    "startup_window": bind(RUN / "terminal-startup-window.json"), "native_exit": 0, "monitor_exit": 0,
    "process_audit": bind(RUN / "process-final-audit.json"), "process_union_identities": len(audit["tracked"]),
    "processes_live": 0, "process_stop_performed": False, "historical_files_preserved": len(historical),
    "protected_configs": protected, "CLI_owned_state_preimage_sha256": prepared["global_cli_preimage_sha256"],
    "CLI_owned_state_current_sha256": sha(Path(r"C:/Users/USER\.cursor\cli-config.json")),
    "CLI_owned_state_changed_fields": "not-inferred-from-hash", "global_direct_writes": False,
    "full_native_gate": "unchecked", "verifier": bind(Path(__file__)), "review": "inline; no independent reviewer",
}
write_new(RUN / "verified-unsupported-event-observations.json", record)
removed = []
for row in prepared["owned_files"]:
    target = project / row["path"]
    target.resolve().relative_to(project.resolve())
    assert sha(target) == row["sha256"]
    target.unlink()
    removed.append(row)
assert all(sha(project / relative) == expected for relative, expected in historical.items())
cleanup = {
    "status": "removed-matching-owned-test-files", "removed": removed, "preserved_historical_files": len(historical),
    "retained_observations_and_receipts": [bind(path) for path, _ in rows + receipts],
    "process_audit": bind(RUN / "process-final-audit.json"), "recursive_delete_performed": False,
    "global_direct_writes": False, "verifier": bind(Path(__file__)),
}
write_new(RUN / "cleanup.json", cleanup)
print(json.dumps({"status": record["status"], "checks_passed": sum(checks.values()), "checks_total": len(checks),
    "callbacks": len(rows), "receipts": len(receipts), "removed_files": len(removed), "historical_files": len(historical),
    "process_union": len(audit["tracked"]), "live": 0}))
