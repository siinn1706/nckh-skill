"""Verify observed duplicate events and preserve absent plugin callback cells."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("duplicate_delivery_runtime", RUN / "cursor-duplicate-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
case = probe.read(RUN / "case-duplicate.json")
prep = probe.read(RUN / "preparation.json")
stage = probe.read(RUN / "stage.json")
definition = probe.read(RUN / "definitions/session.json")
assert case["status"] == "native-project-plugin-duplicate-partial"
assert case["fixture_unchanged"] and case["final_marker_observed"]
assert (RUN / "fixture-before.txt").read_bytes() == (RUN / "fixture-after.txt").read_bytes()
assert probe.contained(probe.PROJECT, prep["selected_relative"]).read_bytes() == (RUN / "fixture-before.txt").read_bytes()
qualified = [r["event"] for r in case["events"] if r["single_policy_receipt_verified"]]
unqualified = [r["event"] for r in case["events"] if not r["single_policy_receipt_verified"]]
assert qualified == ["sessionStart", "preToolUse", "postToolUse"]
assert unqualified == ["beforeSubmitPrompt", "stop"]
version = probe.read(RUN / "native-metadata.json")["version"]
runner_expected = [r["sha256"] for r in stage["staged_members"] if Path(r["path"]).as_posix().endswith("/hooks/runner.py")]
assert len(runner_expected) == 1
for c in case["callbacks"]:
    obs = c["observation"]
    assert obs["status"] == "completed" and obs["runner_exit_code"] == 0 and obs["runner_exited"]
    assert obs["fault_origin"] == "none" and obs["mode"] == "duplicate"
    assert obs["native_version"] == version and obs["runner_sha256"] == runner_expected[0]
    assert obs["control_sha256"] == prep["control_sha256"]
    assert probe.digest_file(probe.WORK / c["path"]) == c["sha256"]
for p in case["policies"] + case["terminal"]:
    assert probe.digest_file(probe.WORK / p["path"]) == p["sha256"]
assert len(case["callbacks"]) == 8 and len(case["policies"]) == 5
for row in case["events"]:
    callbacks = [c["observation"] for c in case["callbacks"] if c["observation"]["event"] == row["event"]]
    assert len(row["policy_receipts"]) == 1
    if row["event"] in qualified:
        assert row["source_counts"] == {"project": 1, "plugin": 1} and row["native_pair_verified"]
        left, right = callbacks
        assert all(left.get(k) == right.get(k) for k in (
            "native_session_hash", "native_tool_use_id", "native_tool_name", "input_sha256", "runner_output"))
    else:
        assert row["source_counts"] == {"project": 1, "plugin": 0} and not row["native_pair_verified"]
    if row["event"] in {"preToolUse", "postToolUse"}:
        assert all(c["native_tool_name"] == "Read" and c["native_tool_use_id"] for c in callbacks)
        assert all(Path(c["native_path_fields"]["file_path"]).resolve() ==
            probe.contained(probe.PROJECT, prep["selected_relative"]).resolve() for c in callbacks)
        assert all(c["workspace_contains_selected_project"] for c in callbacks)
for config in (definition["config"], definition["plugin_config"]):
    for event, handlers in config["hooks"].items():
        assert len(handlers) == 1 and handlers[0]["timeout"] == (20 if event == "preToolUse" else 5)
    assert config["hooks"]["preToolUse"][0]["failClosed"]
assert definition["packaged_runner_unchanged"] and definition["fault_origin"] == "none"
cleanup = probe.read(RUN / "cleanup.json")
history = probe.read(RUN / "historical-project-preimage.json")["members"]
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 28 and not cleanup["config_callable"]
assert cleanup["historical_members_unchanged"] == len(history)
assert all(probe.digest_file(probe.contained(probe.PROJECT, relative)) == expected for relative, expected in history.items())
assert all(r["current_sha256"] == r["sha256"] for r in cleanup["protected_global_config"])
assert all(not probe.contained(probe.PROJECT, r["path"]).exists() for r in definition["extra_configs"])
audit = probe.read(RUN / "final-process-audit.json")
assert audit["matching_count"] == audit["tracked_live_count"] == 0
terminal = probe.read(RUN / "terminal-final-observation.json")["response"]
assert isinstance(terminal["exit_code"], int) and "session_id" not in terminal
tool_ids = sorted({c["observation"]["native_tool_use_id"] for c in case["callbacks"]
    if c["observation"].get("native_tool_use_id")})
assert len(tool_ids) == 1
summary = {"status": "verified-three-native-project-plugin-duplicate-events-two-plugin-cells-unqualified",
    "source_revision": 37, "source_lock_hash": probe.EXPECTED, "model": probe.MODEL, "native_version": version,
    "surface": "cursor-cli", "model_turns": 1, "prompt_submissions": 1, "fault_origin": "none",
    "native_callback_count": 8, "policy_receipt_count": 5, "qualified_duplicate_events": qualified,
    "unqualified_duplicate_events": unqualified, "native_tool_ids": tool_ids, "actual_native_tool": "Read",
    "fixture_unchanged": True, "final_marker_observed": True, "original_case_status_retained": case["status"],
    "original_case": probe.bind(RUN / "case-duplicate.json"), "preparation": probe.bind(RUN / "preparation.json"),
    "definition": probe.bind(RUN / "definitions/session.json"), "cleanup": probe.bind(RUN / "cleanup.json"),
    "process_audit": probe.bind(RUN / "final-process-audit.json"), "terminal_exit": probe.bind(RUN / "terminal-final-observation.json"),
    "terminal_exit_code": terminal["exit_code"], "verifier": probe.bind(Path(__file__)),
    "preflight_timeout_seconds": 20, "other_handler_timeout_seconds": 5, "inner_runner_timeout_seconds": 5,
    "handler_kind": "bounded project/plugin observers forwarding genuine payload to verified packaged runner",
    "plugin_kind": definition["plugin_kind"], "raw_terminal_truncated": case["terminal_truncated"],
    "native_tool_return_content": "not-retained", "artifact_QA": "pending-separate-from-native-callbacks",
    "global_direct_write": False, "protected_global_configs_unchanged": True,
    "cli_owned_state_hash_changed": cleanup["global_cli_hash_before"] != cleanup["global_cli_hash_after"],
    "CLI_owned_state_fields": "not-inferred-from-hashes", "historical_members_preserved": len(history), "removed_members": 28,
    "scope_limit": "No plugin callback observed for beforeSubmitPrompt/stop in this invocation; no general unsupported claim or regrade",
    "plan_tasks": "44/45", "full_native_gate": "unchecked", "owner_acceptance": "exact-r29-VI-EN-only",
    "installed_update": "not-performed", "publication": "not-performed", "scientific_stable_release": "pending"}
target = probe.WORK / "plans/reports/delivery-261005-1900-r37-cursor-project-plugin-duplicate.json"
assert not target.exists() and not (RUN / "native-duplicate-summary.json").exists()
probe.atomic_json(RUN / "native-duplicate-summary.json", summary)
with target.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": summary["status"], "qualified_events": qualified, "unqualified_events": unqualified,
    "history_preserved": len(history), "full_native_gate": "unchecked"}))
