"""Verify real startup callbacks, then remove only unchanged owned test files."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}
prepared = read(RUN / "preparation.json")
project = Path(prepared["project"])
evidence = Path(prepared["evidence"])
audit = read(RUN / "process-final-audit.json")
assert audit["matching_count"] == audit["tracked_live_count"] == 0
assert read(RUN / "terminal-exit-poll.json")["exit_code"] == 0
assert read(RUN / "monitor-exit.json")["exit_code"] == 0
assert read(RUN / "terminal-startup-window.json")["wall_time_seconds"] >= 12
assert "--plugin-dir" not in prepared["argv"] and prepared["maximum_model_turns"] == 0
rows = [(path, read(path)) for path in (evidence / "observations").rglob("*.json")]
workspace = [(path, row) for path, row in rows if row["event"] == "workspaceOpen"]
lifecycle = [(path, row) for path, row in rows if row["event"] == "sessionStart"]
assert len(rows) == 3 and len(workspace) == 1 and len(lifecycle) == 2
assert workspace[0][1]["status"] == "completed-genuine-workspace-input"
assert workspace[0][1]["workspace_contains_selected_project"] and workspace[0][1]["returned_plugin_paths"] == 1
assert workspace[0][1]["native_version"] == "2026.09.15-d2fe57e"
assert {row["callback_source"] for _, row in lifecycle} == {"project", "plugin"}
assert len({row["input_sha256"] for _, row in lifecycle}) == 1
assert len({row["native_session_hash"] for _, row in lifecycle}) == 1
assert all(row["reported_event"] == "sessionStart" and row["runner_exit_code"] == 0 and row["runner_exited"] for _, row in lifecycle)
receipts = list((evidence / "policy-receipts").rglob("*.json"))
assert len(receipts) == 1
protected = []
for row in prepared["protected_configs"]:
    path = Path(row["path"])
    current = sha(path) if path.is_file() else None
    assert current == row["sha256"], "Unrelated protected config changed; retain before cleanup"
    protected.append({**row, "current_sha256": current})
historical = read(RUN / "historical-project-preimage.json")["members"]
assert all(sha(project / relative) == expected for relative, expected in historical.items())
for row in prepared["owned_files"]:
    target = project / row["path"]
    target.resolve().relative_to(project.resolve())
    assert sha(target) == row["sha256"], "Owned target changed; cleanup conflict"
record = {
    "status": "verified-genuine-workspace-plugin-startup-route",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(), "source_revision": 37,
    "source_lock_hash": prepared["source_lock_hash"], "surface": "cursor-cli-interactive", "version": "2026.09.15-d2fe57e",
    "workspaceOpen_callbacks": 1, "project_sessionStart_callbacks": 1, "plugin_sessionStart_callbacks": 1,
    "same_native_lifecycle_input_and_session": True, "idempotent_policy_receipts": 1,
    "plugin_loading_route": "actual workspaceOpen output to owned plugin path; no --plugin-dir",
    "model_selection": prepared["selected_model"], "model_prompts": 0, "tool_requests": 0,
    "prompt_stop_duplicate_qualification": "not-run; remains pending",
    "unsupported_codec_event_qualification": "not-run; workspaceOpen diagnostic returns pluginPaths without invoking packaged codec",
    "callback_source_provenance": "controller-bound project/plugin command definitions; same native lifecycle input observed",
    "callbacks": [bind(path) for path, _ in rows], "policy_receipts": [bind(path) for path in receipts],
    "preparation": bind(RUN / "preparation.json"), "process_audit": bind(RUN / "process-final-audit.json"),
    "process_union_identities": len(audit["tracked"]), "processes_live": 0, "process_stop_performed": False,
    "native_exit": 0, "monitor_exit": 0, "historical_project_files_preserved": len(historical),
    "protected_configs": protected, "CLI_owned_state_preimage_sha256": prepared["global_cli_preimage_sha256"],
    "CLI_owned_state_current_sha256": sha(Path(r"C:/Users/USER\.cursor\cli-config.json")),
    "CLI_owned_state_changed_fields": "not-inferred-from-hash", "global_direct_writes": False,
    "full_native_gate": "unchecked", "verifier": bind(Path(__file__)),
}
with (RUN / "verified-startup-delivery.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
removed = []
for row in prepared["owned_files"]:
    target = project / row["path"]
    target.resolve().relative_to(project.resolve())
    assert sha(target) == row["sha256"]
    target.unlink()
    removed.append(row)
assert all(sha(project / relative) == expected for relative, expected in historical.items())
cleanup = {"status": "removed-matching-owned-test-files", "removed": removed,
    "preserved_historical_files": len(historical), "remaining_evidence_files": [bind(path) for path, _ in rows] + [bind(path) for path in receipts],
    "process_audit": bind(RUN / "process-final-audit.json"), "recursive_delete_performed": False,
    "global_direct_writes": False, "verifier": bind(Path(__file__))}
with (RUN / "cleanup.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(cleanup, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": record["status"], "callbacks": len(rows), "receipts": len(receipts),
    "removed_files": len(removed), "preserved_files": len(historical), "process_union": len(audit["tracked"]), "live": 0}))
