"""Verify real Cursor callbacks, preserve terminal limits and remove owned hooks."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owned_cursor_interactive", RUN / "cursor-interactive-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
REPORT = probe.WORK / "plans/reports/delivery-261005-1225-r36-cursor-interactive.json"
assert not REPORT.exists() and not (RUN / "native-interactive-summary.json").exists()
preparation = probe.read(RUN / "preparation.json")
definition = probe.read(RUN / "definitions/interactive-public-read.json")
assert preparation["maximum_model_turns"] == 1
assert preparation["input_protocol"] == "prompt-text-write-then-separate-carriage-return"
assert definition["definition_kind"] == "instrumented-native-test"
assert definition["timeout_seconds"] == 20 and definition["runner_timeout_seconds"] == 5
assert probe.digest_file(probe.CONFIG) == definition["config_sha256"]
terminal = probe.read(RUN / "terminal-observations.json")
assert sum(row["operation"] == "enter-exact-prepared-prompt-without-control-character" for row in terminal) == 1
assert sum(row["operation"] == "submit-pending-prompt-with-separate-Enter" for row in terminal) == 1
assert any("Grok 4.7 500K Extra High" in row["response"]["output"] for row in terminal)
assert any("\x1b[14;1H  ORACLE_ATTEMPT_FINISHED" in row["response"]["output"] for row in terminal)
last = probe.read(RUN / "terminal-final-observation.json")
assert last["response"]["exit_code"] == 1 and "session_id" not in last["response"]
audit = probe.read(RUN / "final-process-audit.json")
assert audit["matching_count"] == 0 and not audit["matches"]
stop = probe.read(RUN / "process-stop-force.json")
assert stop["root_pid"] == 57824 and stop["exit_code"] == 0
assert all(row["current"] is None or row["current"] == row["expected"] for row in stop["identity_checks"])
fixture = probe.contained(probe.PROJECT, preparation["fixture_relative"])
assert probe.digest_file(fixture) == preparation["fixture_sha256"]
callbacks = [{**probe.bind(path), "receipt": probe.read(path)} for path in sorted((probe.EVIDENCE / "observations").rglob("*.json"))]
policies = [{**probe.bind(path), "receipt": probe.read(path)} for path in sorted((probe.EVIDENCE / "policy-receipts").rglob("*.json"))]
assert len(callbacks) == len(policies) == 5
expected_events = {"sessionStart", "beforeSubmitPrompt", "preToolUse", "postToolUse", "stop"}
by_event = {binding["receipt"]["event"]: binding["receipt"] for binding in callbacks}
assert set(by_event) == expected_events
assert all(row["runner_exited"] and row["runner_exit_code"] == 0 and row["fault_origin"] == "none" for row in by_event.values())
assert all(row["native_version"] == "2026.09.15-d2fe57e" for row in by_event.values())
assert len({row["native_session_hash"] for row in by_event.values()}) == 1
for event in ("preToolUse", "postToolUse"):
    row = by_event[event]
    assert row["native_tool_name"] == "Read" and row["native_model"] == "grok-4.7"
    assert row["native_path_fields"] == {"file_path": str(fixture)}
assert by_event["preToolUse"]["native_tool_use_id"] == by_event["postToolUse"]["native_tool_use_id"]
assert by_event["preToolUse"]["runner_output"] == {}
for event in ("sessionStart", "beforeSubmitPrompt", "stop"):
    assert by_event[event]["native_model"] == "grok-4.7-xhigh"
policy_by_event = {Path(binding["path"]).parent.name: binding["receipt"] for binding in policies}
assert set(policy_by_event) == expected_events
assert policy_by_event["preToolUse"]["decision"] == "allow"
assert policy_by_event["preToolUse"]["reason_codes"] == ["declared-route-checks-current"]
assert policy_by_event["postToolUse"]["decision"] == "pending"
assert policy_by_event["postToolUse"]["reason_codes"] == ["artifact-final-bytes-missing-or-stale"]
assert policy_by_event["stop"]["decision"] == "advisory"
probe.cleanup()
cleanup = probe.read(RUN / "cleanup.json")
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 26
assert not cleanup["config_callable"] and not cleanup["global_direct_write"]
assert all(not probe.contained(probe.PROJECT, row["path"]).exists() for row in cleanup["removed_members"])
record = {"status": "verified-native-cursor-interactive-read-and-five-callbacks", "source_revision": 36,
    "source_lock_hash": probe.EXPECTED, "source_modified": False, "native_turns": 1,
    "surface": "cursor-cli-interactive-terminal", "version": "2026.09.15-d2fe57e",
    "model_requested": probe.MODEL, "effort_requested": "xhigh",
    "native_model_label": "Grok 4.7 500K Extra High · MAX", "native_permission_label": "Run Everything",
    "native_callback_models": {event: row["native_model"] for event, row in by_event.items()},
    "callbacks": callbacks, "policy_receipts": policies, "definition": probe.bind(RUN / "definitions/interactive-public-read.json"),
    "fixture": {"path": preparation["fixture_relative"], "sha256": preparation["fixture_sha256"], "unchanged": True},
    "read_result": "genuine-paired-native-Read-callbacks; exact-tool-return-content-not-retained-by-observer",
    "final_reply": "ORACLE_ATTEMPT_FINISHED observed in terminal render",
    "terminal": probe.bind(RUN / "terminal-observations.json"),
    "terminal_capture": "bounded-harness-chunks; observe-native-turn chunk truncated by harness",
    "terminal_exit": probe.bind(RUN / "terminal-final-observation.json"), "terminal_exit_code": 1,
    "process_tree": probe.bind(RUN / "process-tree-before-turn.json"),
    "graceful_stop": probe.bind(RUN / "process-stop-graceful.json"), "force_stop": probe.bind(RUN / "process-stop-force.json"),
    "process_cleanup": "owned-tree-force-stopped-after-graceful-refusal", "process_audit": probe.bind(RUN / "final-process-audit.json"),
    "cleanup": probe.bind(RUN / "cleanup.json"), "historical_members_preserved": cleanup["historical_members_unchanged"],
    "native_global_cli_hash_unchanged": cleanup["global_cli_hash_before"] == cleanup["global_cli_hash_after"],
    "production_template_timing": "unqualified-by-this-instrumented-observation",
    "prompt_stop_failure_matrix": "pending", "full_native_gate": "unchecked",
    "backend_attestation": "not-observed", "billing": "not-observed", "verifier": probe.bind(Path(__file__))}
probe.atomic_json(RUN / "native-interactive-summary.json", record)
with REPORT.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": record["status"], "native_turns": 1, "callbacks": 5,
    "historical_preserved": record["historical_members_preserved"], "full_native_gate": "unchecked"}))
