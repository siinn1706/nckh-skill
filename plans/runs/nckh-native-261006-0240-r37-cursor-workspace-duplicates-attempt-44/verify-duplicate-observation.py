"""Preserve the failed frozen oracle while verifying actual callback and file facts."""

import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}
p = read(RUN / "preparation.json")
project = Path(p["project"])
evidence = Path(p["evidence"])
assert read(RUN / "prompt-submission-intent.json")["prompt"] == p["prompt"]
assert read(RUN / "startup-prerequisite.json")["status"] == "qualified-genuine-startup-before-single-model-prompt"
assert read(RUN / "terminal-exit-poll.json")["exit_code"] == read(RUN / "monitor-exit.json")["exit_code"] == 0
audit = read(RUN / "process-final-audit.json")
assert audit["matching_count"] == audit["tracked_live_count"] == 0
assert p["final_marker"] in read(RUN / "terminal-turn-poll-02.json")["output"]
rows = [(path, read(path)) for path in (evidence / "observations").rglob("*.json")]
workspace = [(path, row) for path, row in rows if row["event"] == "workspaceOpen"]
native = [(path, row) for path, row in rows if row["event"] != "workspaceOpen"]
assert len(rows) == 11 and len(workspace) == 1 and len(native) == 10
assert workspace[0][1]["status"] == "completed-genuine-workspace-input"
assert all(row["status"] == "completed" and row["runner_exit_code"] == 0 for _, row in native)
assert len({row["native_session_hash"] for _, row in native}) == 1
grouped = defaultdict(list)
for path, row in native:
    grouped[(row["event"], row["input_sha256"])].append((path, row))
pairs = []
singles = []
for (event, digest), group in grouped.items():
    source_set = {row["callback_source"] for _, row in group}
    facts = {"event": event, "input_sha256": digest, "callbacks": [bind(path) for path, _ in group],
        "sources": sorted(source_set), "tool": group[0][1].get("native_tool_name")}
    if len(group) == 2 and source_set == {"project", "plugin"}:
        assert len({row.get("native_tool_use_id") for _, row in group}) == 1
        pairs.append(facts)
    else:
        assert len(group) == 1 and source_set == {"project"}
        singles.append(facts)
assert len(pairs) == 4 and {row["event"] for row in singles} == {"beforeSubmitPrompt", "stop"}
write_pre = [row for _, row in native if row["event"] == "preToolUse" and row.get("native_tool_name") == "Write"]
write_post = [row for _, row in native if row["event"] == "postToolUse" and row.get("native_tool_name") == "Write"]
read_pre = [row for _, row in native if row["event"] == "preToolUse" and row.get("native_tool_name") == "Read"]
assert len(write_pre) == len(write_post) == len(read_pre) == 2
assert len({row["native_tool_use_id"] for row in write_pre + write_post + read_pre}) == 1
oracle = project / p["selected_relative"]
assert all(Path(row["native_path_fields"]["file_path"]).resolve() == oracle.resolve() for row in write_pre + write_post + read_pre)
actual = oracle.read_bytes()
expected = bytes.fromhex(p["expected_marker_hex"])
assert actual == b"NCKH_CURSOR_WORKSPACE_DUPLICATE_OK\r\n" and expected == b"NCKH_CURSOR_WORKSPACE_DUPLICATE_OK\n"
assert actual != expected
receipts = [(path, read(path)) for path in (evidence / "policy-receipts").rglob("*.json")]
assert len(receipts) == 6
for event, expected_count in (("sessionStart", 1), ("beforeSubmitPrompt", 1), ("preToolUse", 2), ("postToolUse", 1), ("stop", 1)):
    assert sum(path.parent.name == event for path, _ in receipts) == expected_count
assert any(row["decision"] == "manual" and "tool-route-uncovered" in row["reason_codes"] for _, row in receipts)
assert any(row["decision"] == "pending" and "artifact-final-bytes-missing-or-stale" in row["reason_codes"] for _, row in receipts)
protected = []
for row in p["protected_configs"]:
    path = Path(row["path"])
    current = sha(path) if path.is_file() else None
    assert current == row["sha256"]
    protected.append({**row, "current_sha256": current})
historical = read(RUN / "historical-project-preimage.json")["members"]
assert all(sha(project / relative) == expected_hash for relative, expected_hash in historical.items())
for row in p["owned_files"]:
    target = project / row["path"]
    target.resolve().relative_to(project.resolve())
    assert sha(target) == row["sha256"]
record = {
    "status": "verified-native-observations-frozen-duplicate-oracle-failed",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(), "source_revision": 37, "source_lock_hash": p["source_lock_hash"],
    "surface": "cursor-cli-interactive", "version": "2026.09.15-d2fe57e", "requested_model": p["model"],
    "backend_effort_attestation": "not-observed", "native_input_callbacks": len(rows), "policy_callbacks": len(native),
    "project_plugin_same_input_pairs": pairs, "project_only_callbacks": singles, "policy_receipts": [bind(path) for path, _ in receipts],
    "policy_receipt_count": len(receipts), "idempotence_scope": "one receipt per distinct input within each event namespace in this instrumented control",
    "actual_write": "one matching Write pre/post ID with exact requested path and one changed public marker",
    "associated_Read_observation": "two preToolUse Read callbacks share the Write ID and path; extra route returns manual/tool-route-uncovered; independent model Read request not established",
    "posttool_policy": "pending/artifact-final-bytes-missing-or-stale; mutation has already occurred",
    "expected_marker_hex": expected.hex(), "actual_marker_hex": actual.hex(), "marker_sha256": sha(oracle),
    "frozen_oracle": "failed", "failure_reasons": ["missing-plugin-beforeSubmitPrompt", "missing-plugin-stop", "marker-LF-versus-CRLF-mismatch", "extra-Read-preflight-pair-and-six-instead-of-five-receipts"],
    "oracle_regraded": False, "model_prompts_submitted": 1, "requested_Write_calls": 1, "model_retries": 0,
    "final_marker_observed": True, "native_exit": 0, "monitor_exit": 0,
    "hook_outer_and_inner_timeout_seconds": 5, "definition_kind": "instrumented route/duplicate control; not default enforcement qualification",
    "preparation": bind(RUN / "preparation.json"), "startup_prerequisite": bind(RUN / "startup-prerequisite.json"),
    "callbacks": [bind(path) for path, _ in rows], "process_audit": bind(RUN / "process-final-audit.json"),
    "process_union_identities": len(audit["tracked"]), "processes_live": 0, "process_stop_performed": False,
    "historical_project_files_preserved": len(historical), "protected_configs": protected,
    "CLI_owned_state_preimage_sha256": p["global_cli_preimage_sha256"], "CLI_owned_state_current_sha256": sha(Path(r"C:/Users/USER\.cursor\cli-config.json")),
    "CLI_owned_state_changed_fields": "not-inferred-from-hash", "global_direct_writes": False,
    "full_native_gate": "unchecked", "verifier": bind(Path(__file__)),
}
with (RUN / "verified-duplicate-observations.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
with (RUN / "oracle-after.txt").open("xb") as stream:
    stream.write(actual)
removed = []
for row in p["owned_files"]:
    target = project / row["path"]
    target.resolve().relative_to(project.resolve())
    assert sha(target) == row["sha256"]
    target.unlink()
    removed.append(row)
assert all(sha(project / relative) == expected_hash for relative, expected_hash in historical.items())
cleanup = {"status": "removed-matching-owned-test-files-preserved-failed-oracle", "removed": removed,
    "preserved_historical_files": len(historical), "marker": bind(oracle),
    "evidence_files": [bind(path) for path, _ in rows + receipts], "process_audit": bind(RUN / "process-final-audit.json"),
    "recursive_delete_performed": False, "global_direct_writes": False}
with (RUN / "cleanup.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(cleanup, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": record["status"], "callback_pairs": len(pairs), "receipts": len(receipts),
    "removed": len(removed), "preserved": len(historical), "process_union": len(audit["tracked"]), "live": 0}))
