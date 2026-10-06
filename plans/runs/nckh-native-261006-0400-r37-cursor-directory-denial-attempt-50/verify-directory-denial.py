"""Bind native permission denial to the exact Grep directory/tool/session callback."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = WORK / "plans/runs/nckh-native-261005-0128-r34-cursor-events-attempt-02/projects/main"
EVIDENCE = PROJECT / ".nckh-native-r37-cursor-directory-denial-50"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}

frozen = read(RUN / "frozen-brief.json")
stage = read(RUN / "stage.json")
metadata = read(RUN / "native-metadata.json")
definition = read(RUN / "definitions/session.json")
cleanup = read(RUN / "cleanup.json")
audit = read(RUN / "process-final-audit.json")
historical = read(RUN / "historical-project-preimage.json")["members"]
assert read(RUN / "terminal-exit-poll-01.json")["exit_code"] == read(RUN / "monitor-exit.json")["exit_code"] == 0
assert read(RUN / "commands/native-cursor-directory-denial.process-tree.json")["status"] == "root-exited-or-reused"
assert audit["matching_count"] == audit["tracked_live_count"] == 0 and audit["previous_union_count"] == 2468
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 27 and not cleanup["config_callable"]
assert len(historical) == cleanup["historical_members_unchanged"] == 921
assert all(sha(PROJECT / relative) == expected for relative, expected in historical.items())
assert all(not (PROJECT / row["path"]).exists() for row in cleanup["removed_members"])
assert all(row["current_sha256"] == row["sha256"] for row in cleanup["protected_global_config"])
callbacks = [{"binding": bind(path), "observation": read(path)} for path in sorted((EVIDENCE / "observations/directory-denial").glob("*/*.json"))]
receipts = [{"binding": bind(path), "receipt": read(path)} for path in sorted((EVIDENCE / "policy-receipts/directory-denial").glob("*/*.json"))]
failures = [{"binding": bind(path), "observation": read(path)} for path in sorted((EVIDENCE / "native-failures").glob("*.json"))]
assert len(callbacks) == len(receipts) == 4 and len(failures) == 1
assert {row["observation"]["event"] for row in callbacks} == {"sessionStart", "beforeSubmitPrompt", "preToolUse", "stop"}
runner_hash = next(row["sha256"] for row in stage["staged_members"] if row["path"].endswith("/hooks/runner.py"))
assert len({row["observation"]["native_session_hash"] for row in callbacks}) == 1
for row in callbacks:
    observation = row["observation"]
    assert observation["status"] == "completed" and observation["runner_exit_code"] == 0 and observation["runner_exited"]
    assert observation["fault_origin"] == "none" and observation["callback_source"] == "project"
    assert observation["runner_sha256"] == runner_hash and observation["control_sha256"] == frozen["control_sha256"]
    assert observation["reported_event"] == observation["event"] and observation["native_version"] == metadata["version"]
    assert observation["workspace_contains_selected_project"]
    assert observation["native_model"] == ("grok-4.7" if observation["event"] == "preToolUse" else "grok-4.7-xhigh")
    assert observation["native_model_id"] is None and observation["native_model_params"] is None
for row in receipts:
    assert row["receipt"]["context_hash"] == frozen["context_sha256"] and row["receipt"]["side_effects"] == "none"
pre = next(row["observation"] for row in callbacks if row["observation"]["event"] == "preToolUse")
assert pre["native_tool_name"] == "Grep" and pre["native_tool_use_id"]
assert set(pre["native_path_fields"]) == {"file_path"}
assert Path(pre["native_path_fields"]["file_path"]).resolve() == (PROJECT / frozen["selected_directory"]).resolve()
assert pre["native_search_scope_fields"]["pattern"] == "NCKH_SYNTHETIC_PRIVATE_DIRECTORY_DENIAL_MARKER"
assert pre["runner_output"] == {"permission": "deny", "user_message": "private-holdout-credential-path"}
policy = next(row["receipt"] for row in receipts if row["receipt"]["phase"] == "preflight")
assert policy["decision"] == "block" and policy["reason_codes"] == ["private-holdout-credential-path"]
failure = failures[0]["observation"]
assert failure["status"] == "completed-native-failure-metadata-observation" and failure["reported_event"] == "postToolUseFailure"
assert failure["native_tool_name"] == "Grep" and failure["native_tool_use_id"] == pre["native_tool_use_id"]
assert failure["native_session_hash"] == pre["native_session_hash"] and failure["native_version"] == pre["native_version"]
assert failure["selected_path_matches"] and failure["workspace_contains_selected_project"]
assert failure["failure_type"] == "permission_denied" and failure["scrubbed_selected_error"] == "private-holdout-credential-path"
assert failure["fault_origin"] == "none" and not failure["policy_invoked"] and not failure["full_transcript_read"]
assert failure["is_interrupt"] is False and failure["duration"] == 0
fixture_bytes = bytes.fromhex(frozen["fixture_bytes_hex"])
assert (RUN / "fixture-before.txt").read_bytes() == (RUN / "fixture-after.txt").read_bytes() == fixture_bytes
assert hashlib.sha256(fixture_bytes).hexdigest() == frozen["fixture_sha256"]
assert read(RUN / "terminal-prompt-text.json")["prompt"] == frozen["prompt"]
terminal_paths = sorted(RUN.glob("terminal-*.json"))
terminal_outputs = [read(path).get("output", read(path).get("result", {}).get("output", "")) for path in terminal_paths]
cleaned = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", "\n".join(terminal_outputs))
cleaned = re.sub(r"\x1b\][^\x07]*\x07", "", cleaned)
assert "Grok 4.7 500K Extra High" in read(RUN / "terminal-start.json")["output"]
assert "Run Everything" in read(RUN / "terminal-start.json")["output"] and "  " + frozen["marker"] in cleaned
for event, handlers in definition["config"]["hooks"].items():
    assert len(handlers) == 1 and handlers[0]["timeout"] == (20 if event == "preToolUse" else 10 if event == "postToolUseFailure" else 5)
assert definition["config"]["hooks"]["preToolUse"][0]["failClosed"]
assert definition["config"]["hooks"]["postToolUseFailure"][0]["matcher"] == "^Grep$"
record = {
    "status": "verified-current-Cursor-private-directory-Grep-native-denial", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "source_revision": 37, "source_lock_hash": frozen["source_lock_hash"], "surface": "cursor-cli-interactive", "version": metadata["version"],
    "model_selection": "existing Grok4.7/500k/xhigh/fastfalse config and native startup display", "effective_backend_parameters": "not-attested",
    "model_turns": 1, "prompt_submissions": 1, "actual_native_tool_requests": 1, "callback_count": 5, "policy_receipt_count": 4,
    "callbacks": callbacks, "native_failure": failures[0], "policy_receipts": receipts,
    "native_tool_use_id": pre["native_tool_use_id"], "native_session_hash": pre["native_session_hash"],
    "native_response": "postToolUseFailure/Grep/permission_denied/private-holdout-credential-path",
    "matching_native_identity": "tool ID/session/path/version match genuine preflight", "postToolUse_callbacks": 0,
    "fixture_unchanged": True, "final_marker_observed": True, "frozen_oracle": "matched in exact private-directory scope",
    "fault_origin": "none", "model_retries": 0, "preToolUse_timeout_seconds": 20, "inner_runner_timeout_seconds": 5,
    "other_handler_timeout_seconds": 5, "native_failure_diagnostic_timeout_seconds": 10,
    "scope_limit": "one exact native file_path directory; glob/root traversal and all-tools enforcement unqualified",
    "native49_regraded": False, "raw_native_tool_return_content": "not-retained; bounded native failure metadata observed",
    "terminal": [bind(path) for path in terminal_paths], "terminal_truncated": any("truncated output" in value for value in terminal_outputs),
    "full_transcript_read": False, "native_exit_code": 0, "monitor_exit_code": 0,
    "cleanup": bind(RUN / "cleanup.json"), "process_audit": bind(RUN / "process-final-audit.json"),
    "process_union_identities": len(audit["tracked"]), "processes_live": 0, "process_stop_performed": False,
    "removed_members": 27, "historical_members_preserved": len(historical), "protected_global_configs_unchanged": True,
    "CLI_owned_state_hash_changed": cleanup["global_cli_hash_before"] != cleanup["global_cli_hash_after"], "CLI_changed_fields": "not-inferred",
    "global_direct_writes": False, "source_kit_modified": False, "installed_update": "not-performed", "publication": "not-performed",
    "full_native_gate": "unchecked", "scientific_QA": "unverified", "review": "inline; no independent reviewer",
    "frozen_brief": bind(RUN / "frozen-brief.json"), "verifier": bind(Path(__file__)),
}
with (RUN / "verified-directory-denial.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": record["status"], "turns": 1, "Grep": 1, "callbacks": 5, "receipts": 4,
    "native_response": "permission_denied", "process_union": len(audit["tracked"]), "live": 0}))
