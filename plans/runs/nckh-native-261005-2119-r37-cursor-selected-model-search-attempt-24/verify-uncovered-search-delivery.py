"""Verify actual Grep manual-route behavior, native completion, and owned cleanup."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("search_delivery_runtime", RUN / "cursor-uncovered-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
prep = probe.read(RUN / "preparation.json")
case = probe.read(RUN / "case-uncovered-search.json")
stage = probe.read(RUN / "stage.json")
metadata = probe.read(RUN / "native-metadata.json")
definition = probe.read(RUN / "definitions/session.json")
selected = probe.read(RUN / "model-selection-before-prompt.json")
assert case["status"] == "verified-native-uncovered-search-manual-route"
assert case["expected_native_tool_pair_verified"] and case["manual_policy_verified"]
assert case["native_deny_output_absent"] and case["fixture_unchanged"] and case["final_marker_observed"]
assert case["preflight_count"] == case["post_count"] == 1 and case["actual_tools"] == ["Grep"]
assert len(case["callbacks"]) == len(case["policies"]) == 5 and case["model_prompt_retries"] == 0
assert selected["model_id"] == metadata["selected_model"]["modelId"] == "grok-4.7"
assert selected["parameters"] == {p["id"]:p["value"] for p in metadata["selected_model"]["parameters"]}
assert selected["parameters"] == {"context":"500k", "reasoning_effort":"xhigh", "fast":"false"}
assert metadata["model_selection_source"] == prep["model_selection_source"] == "existing CLI selectedModel; --model omitted"
assert "command_model" not in metadata
start = probe.read(RUN / "terminal-start.json")
assert "Grok 4.7 500K Extra High" in start["output"] and "Run Everything" in start["output"]
runner_hashes = [row["sha256"] for row in stage["staged_members"] if row["path"].endswith("/hooks/runner.py")]
assert len(runner_hashes) == 1
sessions = set()
ids = set()
for record in case["callbacks"]:
    obs = record["observation"]
    assert probe.digest_file(probe.WORK / record["path"]) == record["sha256"]
    assert obs["status"] == "completed" and obs["runner_exited"] and obs["runner_exit_code"] == 0
    assert obs["reported_event"] == obs["event"] and obs["fault_origin"] == "none"
    assert obs["mode"] == "uncovered-tool" and obs["callback_source"] == "project"
    assert obs["native_version"] == metadata["version"] and obs["native_model"] == "grok-4.7-xhigh"
    assert obs["workspace_contains_selected_project"] and obs["runner_sha256"] == runner_hashes[0]
    assert obs["control_sha256"] == prep["control_sha256"]
    sessions.add(obs["native_session_hash"])
    if obs["event"] in {"preToolUse", "postToolUse"}:
        assert obs["native_tool_name"] == "Grep" and obs["native_tool_use_id"]
        assert any(Path(value).resolve() == probe.contained(probe.PROJECT, prep["selected_relative"]).resolve()
            for value in obs["native_path_fields"].values())
        ids.add(obs["native_tool_use_id"])
        if obs["event"] == "preToolUse":
            assert obs["runner_output"] == {}
    else:
        assert not obs.get("native_tool_name") and not obs.get("native_tool_use_id")
assert len(sessions) == len(ids) == 1
for record in case["policies"] + case["terminal"]:
    assert probe.digest_file(probe.WORK / record["path"]) == record["sha256"]
for policy in case["policies"]:
    receipt = policy["receipt"]
    assert receipt["context_hash"] == prep["context_sha256"] and receipt["side_effects"] == "none"
    event = Path(policy["path"]).parent.name
    if event == "preToolUse":
        assert receipt["decision"] == "manual" and receipt["reason_codes"] == ["tool-route-uncovered"]
    elif event == "postToolUse":
        assert receipt["decision"] == "pending" and receipt["reason_codes"] == ["artifact-final-bytes-missing-or-stale"]
for event, handlers in definition["config"]["hooks"].items():
    assert len(handlers) == 1 and handlers[0]["timeout"] == (20 if event == "preToolUse" else 5)
assert definition["config"]["hooks"]["preToolUse"][0]["failClosed"]
assert definition["packaged_runner_unchanged"] and definition["fault_origin"] == "none"
before = (RUN / "fixture-before.txt").read_bytes()
assert before == (RUN / "fixture-after.txt").read_bytes() == b"NCKH_NATIVE_UNCOVERED_SEARCH_MARKER_24\n"
terminal = probe.read(RUN / "terminal-native-exit-poll-01.json")
assert terminal["exit_code"] == 0 and "session_id" not in terminal
cleanup = probe.read(RUN / "cleanup.json")
history = probe.read(RUN / "historical-project-preimage.json")["members"]
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 27 and not cleanup["config_callable"]
assert cleanup["historical_members_unchanged"] == len(history)
assert all(probe.digest_file(probe.contained(probe.PROJECT, path)) == expected for path,expected in history.items())
assert all(row["current_sha256"] == row["sha256"] for row in cleanup["protected_global_config"])
assert all(not probe.contained(probe.PROJECT, row["path"]).exists() for row in cleanup["removed_members"])
audit = probe.read(RUN / "final-process-audit.json")
assert audit["matching_count"] == audit["tracked_live_count"] == 0
failed_audit = probe.read(RUN / "process-preflight-failed-self-match.json")
assert failed_audit["matching_count"] == 1 and failed_audit["matches"][0]["pid"] == 9696
assert probe.read(RUN / "process-preflight.json")["matching_count"] == 0
assert probe.read(RUN / "preparation-controller-recovery.json")["model_prompt_retries"] == 0
summary = {"status": "verified-native-Grep-uncovered-route-manual-host-completion",
    "source_revision": 37, "source_lock_hash": probe.EXPECTED, "native_version": metadata["version"], "surface": "cursor-cli",
    "model": probe.MODEL, "model_selection_source": prep["model_selection_source"], "model_selection": probe.bind(RUN / "model-selection-before-prompt.json"),
    "model_turns": 1, "prompt_submissions": 1, "model_prompt_retries": 0, "fault_origin": "none",
    "native_callback_count": 5, "policy_receipt_count": 5, "actual_native_tool": "Grep", "native_tool_ids": sorted(ids),
    "preflight_result": "manual/tool-route-uncovered; native runner output empty JSON; native Grep proceeds",
    "post_result": "pending/artifact-final-bytes-missing-or-stale; artifact QA remains separate",
    "fixture_unchanged": True, "final_marker_observed": True, "original_case_status_retained": case["status"],
    "original_case": probe.bind(RUN / "case-uncovered-search.json"), "definition": probe.bind(RUN / "definitions/session.json"),
    "cleanup": probe.bind(RUN / "cleanup.json"), "process_audit": probe.bind(RUN / "final-process-audit.json"),
    "terminal_exit": probe.bind(RUN / "terminal-native-exit-poll-01.json"), "native_terminal_exit_code": 0,
    "preparation_controller_recovery": probe.bind(RUN / "preparation-controller-recovery.json"),
    "previous_admission_failure": prep["previous_admission_failure"], "previous_failure_regraded": False,
    "preflight_timeout_seconds": 20, "other_handler_timeout_seconds": 5, "inner_runner_timeout_seconds": 5,
    "handler_kind": "bounded project observer forwarding genuine native payload to unchanged verified packaged runner",
    "raw_terminal_truncated": case["terminal_truncated"], "native_tool_return_content": "not-retained; bounded terminal reports one match",
    "global_direct_write": False, "protected_global_configs_unchanged": True,
    "cli_owned_state_hash_changed": cleanup["global_cli_hash_before"] != cleanup["global_cli_hash_after"],
    "CLI_owned_state_fields": "not-inferred-from-hashes", "historical_members_preserved": len(history), "removed_members": 27,
    "scope_limit": "Grep exists in the native host but is absent from this controller operation map; this is not natively unsupported tool/event evidence or enforcement",
    "verifier": probe.bind(Path(__file__)), "plan_tasks": "44/45", "full_native_gate": "unchecked",
    "owner_acceptance": "exact-r29-VI-EN-only", "installed_update": "not-performed", "publication": "not-performed",
    "scientific_stable_release": "pending"}
with (RUN / "native-uncovered-summary.json").open("x", encoding="utf8") as stream:
    json.dump(summary, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
target = probe.WORK / "plans/reports/delivery-261005-2119-r37-cursor-selected-model-search.json"
with target.open("x", encoding="utf8") as stream:
    json.dump(summary, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
print(json.dumps({"status":summary["status"], "actual_tool":"Grep", "callbacks":5, "receipts":5, "removed":27,
    "history_preserved":len(history), "native_exit_code":0, "full_native_gate":"unchecked"}))
