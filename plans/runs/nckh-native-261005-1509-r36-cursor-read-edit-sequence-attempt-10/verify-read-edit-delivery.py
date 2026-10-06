"""Bind genuine Read/Write callbacks and the successful synthetic byte mutation."""

import importlib.util
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owned_cursor_read_edit_delivery", RUN / "cursor-read-edit-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
REPORT = probe.WORK / "plans/reports/delivery-261005-1509-r36-cursor-read-edit-sequence.json"
assert not REPORT.exists() and not (RUN / "native-sequence-summary.json").exists()
record = probe.read(RUN / "sequence-observation.json")
preparation = probe.read(RUN / "preparation.json")
definition = probe.read(RUN / "definitions/session.json")
submission = probe.read(RUN / "submission.json")
metadata = probe.read(RUN / "native-metadata.json")
assert record["ready"] and record["expected_effect_observed"] and record["bytes_changed"]
assert record["native_pre_tool_names_in_order"] == ["Read", "Read", "Write"]
assert record["distinct_native_tool_use_id_count"] == 2 and record["requested_tool_call_bound_respected"]
assert preparation["maximum_prompt_submissions"] == preparation["maximum_model_turns"] == 1
assert submission["prompt"] == preparation["prompt"] and submission["prompt_write"]["session_id"] == submission["enter_write"]["session_id"] == 24526
assert probe.digest_file(probe.CONFIG) == definition["config_sha256"]
assert all(len(handlers) == 1 and handlers[0]["timeout"] == 20 for handlers in definition["config"]["hooks"].values())
assert definition["observer_invoked"] and definition["fault_origin"] == "none"
fixture = probe.contained(probe.PROJECT, preparation["relative"])
assert fixture.read_bytes() == (RUN / "fixture-after.txt").read_bytes() == probe.read(RUN / "frozen-brief.json")["requested_after_text"].encode("utf8")
assert probe.digest_file(fixture) == record["after_sha256"] != record["before_sha256"]
events = Counter()
for binding in record["native_observations"]:
    assert probe.digest_file(probe.WORK / binding["path"]) == binding["sha256"]
    native = binding["observation"]
    events[native["event"]] += 1
    assert native["status"] == "completed" and native["runner_exit_code"] == 0 and native["runner_exited"]
    assert native["fault_origin"] == "none" and not native["fault_selected"]
    assert native["workspace_contains_selected_project"] and native["native_version"] == metadata["version"]
    assert native["reported_event"] == native["event"]
    if native["event"] in ("preToolUse", "postToolUse"):
        assert len(native["native_path_fields"]) == 1
        assert all(Path(value).resolve() == fixture.resolve() for value in native["native_path_fields"].values())
assert dict(events) == {"beforeSubmitPrompt": 1, "postToolUse": 3, "preToolUse": 3, "sessionStart": 1, "stop": 1}
assert all(len(pair["post_callbacks"]) == 1 for pair in record["native_tool_pairs"])
pairs = record["native_tool_pairs"]
assert pairs[0]["tool_use_id"] != pairs[1]["tool_use_id"] == pairs[2]["tool_use_id"]
policy_rows = []
for binding in record["policies"]:
    assert probe.digest_file(probe.WORK / binding["path"]) == binding["sha256"]
    receipt = binding["receipt"]
    assert receipt["context_hash"] == probe.digest_file(probe.EVIDENCE / "context-allow.json")
    matches = []
    if receipt["phase"] in ("preflight", "pre-delivery"):
        for tool in ("Read", "Write"):
            event = {"schema_version": 1, "phase": receipt["phase"], "host": "cursor", "tool": tool,
                     "paths": [preparation["relative"]], "session_key": receipt["session_key"],
                     "task_key": receipt["task_key"], "artifact_sha256": receipt["artifact_sha256"], "stop_active": False}
            if probe.digest_record(event) == receipt["event_hash"]:
                matches.append(tool)
        assert len(matches) == 1
    policy_rows.append({"binding": binding, "neutral_tool_matches": matches,
                        "method": "bounded-neutral-hash-check-supported-by-native-tool-and-path-fields"})
write_pre = [row for row in policy_rows if row["neutral_tool_matches"] == ["Write"] and row["binding"]["receipt"]["phase"] == "preflight"]
assert len(write_pre) == 1 and write_pre[0]["binding"]["receipt"]["decision"] == "allow"
delivery_policies = [row for row in policy_rows if row["binding"]["receipt"]["phase"] == "pre-delivery"]
assert len(delivery_policies) == 2 and all(row["binding"]["receipt"]["decision"] == "pending" for row in delivery_policies)
exit_record = probe.read(RUN / "terminal-final-observation.json")
assert "exit_code" in exit_record["response"] and "session_id" not in exit_record["response"]
audit = probe.read(RUN / "final-process-audit.json")
assert audit["matching_count"] == audit["tracked_live_count"] == 0
forced = probe.read(RUN / "process-stop-force.json")
assert forced["root_pid"] == 42004 and forced["exit_code"] == 0
assert all(row["current"] is None or datetime.fromisoformat(row["current"]) == datetime.fromisoformat(row["expected"]) for row in forced["identity_checks"])
correction = {"status": "callback-count-versus-native-use-identity-reconciled", "model_retries": 0,
              "original_collector": probe.bind(RUN / "collector-preimages/inspect-read-edit.py"),
              "corrected_collector": probe.bind(RUN / "inspect-read-edit.py"),
              "native_pre_callbacks": 3, "distinct_native_tool_use_ids": 2,
              "shared_identity": "second Read and Write use the same native tool_use_id",
              "pairing_contract": "match both native tool_use_id and native tool name"}
probe.atomic_json(RUN / "collector-correction.json", correction)
probe.cleanup()
cleanup = probe.read(RUN / "cleanup.json")
summary = {"status": "verified-instrumented-native-read-write-sequence-and-byte-mutation", "source_revision": 36,
    "source_lock_hash": probe.EXPECTED, "source_modified": False, "surface": "cursor-cli-interactive-terminal",
    "version": metadata["version"], "model_requested": probe.MODEL, "effort_requested": "xhigh", "selected_model": metadata["selected_model"],
    "model_turns": 1, "prompt_submissions": 1, "native_callback_count": sum(events.values()), "native_events": dict(events),
    "native_pre_tool_names_in_order": record["native_pre_tool_names_in_order"], "distinct_native_tool_use_id_count": 2,
    "native_tool_pairs": record["native_tool_pairs"], "before_sha256": record["before_sha256"], "after_sha256": record["after_sha256"],
    "actual_effect": "exact-requested-replacement-bytes", "actual_native_write": "observed-with-paired-pre-post-callbacks",
    "policy_rows": policy_rows, "policy_receipt_count": len(record["policies"]), "pre_delivery_QA": "pending-artifact-final-bytes-missing-or-stale",
    "observer_invoked": True, "outer_timeout_seconds": 20, "packaged_runner_timeout_seconds": 5, "fault_origin": "none",
    "direct_template5s_qualification": "not-established-by-this-instrumented-sequence",
    "historical_single_Write_failures": "preserved-unregraded; sequence-and-outer-timing-both-differ",
    "raw_model_tool_call_frames": "not-captured", "raw_tool_result_bytes": "not-retained", "terminal_scope": "bounded-harness-chunks; first observation chunk truncated",
    "sequence": probe.bind(RUN / "sequence-observation.json"), "collector_correction": probe.bind(RUN / "collector-correction.json"),
    "definition": probe.bind(RUN / "definitions/session.json"), "preparation": probe.bind(RUN / "preparation.json"),
    "cleanup": probe.bind(RUN / "cleanup.json"), "process_audit": probe.bind(RUN / "final-process-audit.json"),
    "terminal_exit": probe.bind(RUN / "terminal-final-observation.json"), "terminal_exit_code": exit_record["response"]["exit_code"],
    "historical_members_preserved": cleanup["historical_members_unchanged"], "protected_global_configs_unchanged": True,
    "cli_state_hash_before": cleanup["global_cli_hash_before"], "cli_state_hash_after": cleanup["global_cli_hash_after"],
    "cli_state_hash_unchanged": cleanup["global_cli_hash_before"] == cleanup["global_cli_hash_after"], "global_direct_write": False,
    "full_native_gate": "unchecked", "backend_attestation": "not-observed", "billing": "not-observed", "verifier": probe.bind(Path(__file__))}
probe.atomic_json(RUN / "native-sequence-summary.json", summary)
with REPORT.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": summary["status"], "native_callbacks": sum(events.values()), "native_use_ids": 2,
                  "policy_receipts": len(record["policies"]), "actual_write": True,
                  "after_sha256": record["after_sha256"], "historical_preserved": cleanup["historical_members_unchanged"]}))
