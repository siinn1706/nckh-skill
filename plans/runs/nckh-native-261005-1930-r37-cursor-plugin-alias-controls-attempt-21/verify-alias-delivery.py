"""Verify retained native observations without upgrading missing plugin callbacks."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("alias_delivery_runtime", RUN / "cursor-alias-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
case = probe.read(RUN / "case-alias.json")
prep = probe.read(RUN / "preparation.json")
stage = probe.read(RUN / "stage.json")
definition = probe.read(RUN / "definitions/session.json")
version = probe.read(RUN / "native-metadata.json")["version"]
assert case["status"] == "native-plugin-alias-controls-partial"
assert case["final_marker_observed"] and case["unexpected_tool_callbacks"] == 0
assert case["model_prompt_retries"] == case["selected_event_context_missing_receipts"] == 0
assert len(case["callbacks"]) == len(case["policies"]) == 3
assert [row["event"] for row in case["events"]] == ["beforeSubmitPrompt", "stop"]
runner_hashes = [row["sha256"] for row in stage["staged_members"] if row["path"].endswith("/hooks/runner.py")]
assert len(runner_hashes) == 1
sessions = set()
for callback in case["callbacks"]:
    observation = callback["observation"]
    assert observation["status"] == "completed" and observation["runner_exited"]
    assert observation["runner_exit_code"] == 0 and observation["fault_origin"] == "none"
    assert observation["callback_source"] == "project" and observation["mode"] == "duplicate"
    assert observation["reported_event"] == observation["event"]
    assert observation["native_version"] == version and observation["native_model"] == "grok-4.7-xhigh"
    assert observation["runner_sha256"] == runner_hashes[0]
    assert observation["control_sha256"] == prep["control_sha256"]
    assert observation["workspace_contains_selected_project"]
    assert observation["native_tool_name"] is None and observation["native_tool_use_id"] is None
    assert probe.digest_file(probe.WORK / callback["path"]) == callback["sha256"]
    sessions.add(observation["native_session_hash"])
assert len(sessions) == 1
for record in case["policies"] + case["terminal"]:
    assert probe.digest_file(probe.WORK / record["path"]) == record["sha256"]
for policy in case["policies"]:
    assert policy["receipt"]["context_hash"] == prep["context_sha256"]
    assert policy["receipt"]["decision"] == "advisory" and policy["receipt"]["side_effects"] == "none"
for row in case["events"]:
    assert row["callback_count"] == 1 and row["source_counts"] == {"project": 1, "plugin": 0}
    assert not row["native_pair_verified"] and not row["single_policy_receipt_verified"]
    assert len(row["policy_receipts"]) == 1 and row["status"] == "alias-duplicate-unqualified"
for event, handlers in definition["config"]["hooks"].items():
    assert len(handlers) == 1 and handlers[0]["timeout"] == (20 if event == "preToolUse" else 5)
assert definition["config"]["hooks"]["preToolUse"][0]["failClosed"]
assert set(definition["plugin_config"]["hooks"]) == {"UserPromptSubmit", "Stop"}
for groups in definition["plugin_config"]["hooks"].values():
    assert len(groups) == 1 and groups[0]["matcher"] == "*"
    handlers = groups[0]["hooks"]
    assert len(handlers) == 1 and handlers[0]["timeout"] == 5
    assert handlers[0]["type"] == "command" and "--callback-source plugin" in handlers[0]["command"]
assert definition["packaged_runner_unchanged"] and definition["fault_origin"] == "none"
for record in (prep["hypothesis"], prep["definition"], prep["controller"], prep["runtime"]):
    assert probe.digest_file(probe.WORK / record["path"]) == record["sha256"]
wrapper = probe.read(RUN / "terminal-alias-poll-01.json")
raw = probe.read(RUN / "terminal-alias-poll-02.json")
assert wrapper["response"] == raw
assert "  " + prep["marker"] + "\u001b[K" in raw["output"]
assert case["terminal_truncated"] and raw["original_token_count"] > 4000
terminal = probe.read(RUN / "terminal-native-exit-poll-01.json")
assert terminal["exit_code"] == 0 and "session_id" not in terminal
cleanup = probe.read(RUN / "cleanup.json")
history = probe.read(RUN / "historical-project-preimage.json")["members"]
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 28
assert not cleanup["config_callable"] and cleanup["historical_members_unchanged"] == len(history)
assert all(probe.digest_file(probe.contained(probe.PROJECT, path)) == value for path, value in history.items())
assert all(row["current_sha256"] == row["sha256"] for row in cleanup["protected_global_config"])
assert all(not probe.contained(probe.PROJECT, row["path"]).exists() for row in cleanup["removed_members"])
audit = probe.read(RUN / "final-process-audit.json")
assert audit["matching_count"] == audit["tracked_live_count"] == 0
refusal = probe.read(RUN / "post-exit-cleanup-refusal.json")
assert refusal["native_exit_code"] == 0 and refusal["controller_exit_code"] == 1
assert refusal["taskkill_reached"] is False
summary = {
    "status": "verified-native-alias-control-two-plugin-cells-unqualified",
    "source_revision": 37, "source_lock_hash": probe.EXPECTED, "native_version": version,
    "surface": "cursor-cli", "model": probe.MODEL, "effort_requested": "xhigh",
    "model_turns": 1, "prompt_submissions": 1, "model_prompt_retries": 0,
    "requested_native_tools": 0, "selected_tool_callbacks": 0, "fault_origin": "none",
    "native_callback_count": 3, "policy_receipt_count": 3,
    "selected_events": [row["event"] for row in case["events"]],
    "qualified_duplicate_events": [], "unqualified_duplicate_events": [row["event"] for row in case["events"]],
    "event_results": [{key: value for key, value in row.items() if key not in {"callbacks", "policy_receipts"}} for row in case["events"]],
    "session_start": "one-project-callback; plugin-sessionStart-not-configured-in-this-control",
    "final_marker_observed": True, "original_case_status_retained": case["status"],
    "original_case": probe.bind(RUN / "case-alias.json"), "preparation": probe.bind(RUN / "preparation.json"),
    "definition": probe.bind(RUN / "definitions/session.json"), "frozen_hypothesis": prep["hypothesis"],
    "cleanup": probe.bind(RUN / "cleanup.json"), "process_audit": probe.bind(RUN / "final-process-audit.json"),
    "terminal_exit": probe.bind(RUN / "terminal-native-exit-poll-01.json"), "terminal_exit_code": 0,
    "post_exit_cleanup_refusal": probe.bind(RUN / "post-exit-cleanup-refusal.json"),
    "terminal_wrapper_reconciliation": probe.bind(RUN / "terminal-wrapper-reconciliation.json"),
    "preparation_observation_reconciliation": probe.bind(RUN / "preparation-terminal-reconciliation.json"),
    "verifier": probe.bind(Path(__file__)), "preflight_timeout_seconds": 20,
    "other_handler_timeout_seconds": 5, "inner_runner_timeout_seconds": 5,
    "handler_kind": "bounded project/plugin observers forwarding genuine payload to verified packaged runner",
    "plugin_kind": "minimal local compatibility control; nested UserPromptSubmit and Stop definitions",
    "raw_terminal_truncated": case["terminal_truncated"], "native_tool_return_content": "not-applicable-no-selected-tool-callback",
    "protected_global_configs_unchanged": True, "global_direct_write": False,
    "cli_owned_state_hash_changed": cleanup["global_cli_hash_before"] != cleanup["global_cli_hash_after"],
    "CLI_owned_state_fields": "not-inferred-from-hashes", "historical_members_preserved": len(history), "removed_members": 28,
    "hypothesis_result": "No plugin callback observed for either alias in this invocation; cause remains unverified",
    "scope_limit": "Missing callbacks do not establish unsupported behavior for all versions/surfaces; native19 is not regraded",
    "plan_tasks": "44/45", "full_native_gate": "unchecked", "owner_acceptance": "exact-r29-VI-EN-only",
    "installed_update": "not-performed", "publication": "not-performed", "scientific_stable_release": "pending",
}
target = probe.WORK / "plans/reports/delivery-261005-1930-r37-cursor-plugin-alias-controls.json"
assert not target.exists() and not (RUN / "native-alias-summary.json").exists()
probe.atomic_json(RUN / "native-alias-summary.json", summary)
with target.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": summary["status"], "callback_count": 3, "policy_receipt_count": 3,
    "historical_preserved": len(history), "native_exit_code": 0, "full_native_gate": "unchecked"}))
