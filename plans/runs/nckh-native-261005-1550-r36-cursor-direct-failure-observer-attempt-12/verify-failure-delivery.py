"""Bind a genuine native timeout to the selected Read and preserve its limits."""

import importlib.util
import json
from datetime import datetime
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owned_cursor_failure_delivery", RUN / "cursor-direct-failure-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
REPORT = probe.WORK / "plans/reports/delivery-261005-1550-r36-cursor-direct-failure-observer.json"
assert not REPORT.exists() and not (RUN / "native-failure-summary.json").exists()
prep = probe.read(RUN / "preparation.json")
control = probe.read(RUN / "control.json")
definition = probe.read(RUN / "definitions/session.json")
intent = probe.read(RUN / "prompt-intent.json")
assert prep["maximum_prompt_submissions"] == prep["maximum_model_turns"] == 1
assert intent["prompt"] == prep["prompt"] and intent["session_id"] == 91233
assert probe.digest_file(probe.CONFIG) == definition["config_sha256"]
assert probe.digest_file(probe.EVIDENCE / "context-active.json") == control["context_file_sha256"]
assert definition["timeout_seconds"] == 5 and not definition["observer_invoked_for_packaged_events"]
policies = [{**probe.bind(p), "receipt": probe.read(p)} for p in sorted((probe.EVIDENCE / "policy-receipts").glob("*.json"))
            if p.relative_to(probe.EVIDENCE).as_posix() not in control["receipt_preimage"]]
assert len(policies) == 3
assert sorted(p["receipt"]["phase"] for p in policies) == ["advisory", "preflight", "stop"]
assert all(p["receipt"]["context_hash"] == control["context_file_sha256"] for p in policies)
pre = next(p for p in policies if p["receipt"]["phase"] == "preflight")
neutral = {"schema_version": 1, "phase": "preflight", "host": "cursor", "tool": "Read", "paths": [prep["relative"]],
           "session_key": pre["receipt"]["session_key"], "task_key": pre["receipt"]["task_key"],
           "artifact_sha256": pre["receipt"]["artifact_sha256"], "stop_active": False}
assert probe.digest_record(neutral) == pre["receipt"]["event_hash"] and pre["receipt"]["decision"] == "allow"
failures = [{**probe.bind(p), "record": probe.read(p)} for p in sorted((probe.EVIDENCE / "native-failures").glob("*.json"))]
assert len(failures) == 1
failure = failures[0]["record"]
assert failure["reported_event"] == "postToolUseFailure" and failure["native_version"] == "2026.09.15-d2fe57e"
assert failure["selected_read_path_matches"] and failure["workspace_contains_selected_project"]
assert failure["native_tool_name"] == "Read" and failure["failure_type"] == "permission_denied"
assert "Hook script timed out after 5000ms" in failure["scrubbed_selected_read_error"]
assert "--event preToolUse" in failure["scrubbed_selected_read_error"] and "fail closed" in failure["scrubbed_selected_read_error"]
assert failure["fault_origin"] == "none" and not failure["policy_invoked"] and not failure["full_transcript_read"]
fixture = probe.contained(probe.PROJECT, prep["relative"])
assert fixture.read_bytes() == (RUN / "fixture-preimage.txt").read_bytes()
assert probe.digest_file(fixture) == prep["before_sha256"]
with (RUN / "fixture-after.txt").open("xb") as stream:
    stream.write(fixture.read_bytes())
terminal = [probe.bind(RUN / name) for name in ("terminal-launch.json", "terminal-startup.json", "terminal-prompt.json",
            "terminal-enter.json", "terminal-poll-01.json", "terminal-stop-request.json", "terminal-stop-request-02.json")]
poll = probe.read(RUN / "terminal-poll-01.json")
assert "  " + prep["marker"] + "\u001b[K" in poll["output"]
assert probe.read(RUN / "terminal-prompt.json")["session_id"] == probe.read(RUN / "terminal-enter.json")["session_id"] == 91233
exit_record = probe.read(RUN / "terminal-final-observation.json")["response"]
assert exit_record["exit_code"] == 1 and "session_id" not in exit_record
audit = probe.read(RUN / "final-process-audit.json")
assert audit["matching_count"] == audit["tracked_live_count"] == 0
force = probe.read(RUN / "process-stop-force.json")
assert force["exit_code"] == 0 and force["root_pid"] == 32696
assert all(p["current"] is None or datetime.fromisoformat(p["current"]) == datetime.fromisoformat(p["expected"])
           for p in force["identity_checks"])
timing = probe.read(RUN / "local-runner-timing.json")
assert len(timing["rows"]) == 3 and timing["not_native_timeout_qualification"] and timing["model_turns"] == 0
observation = {"policies": policies, "native_failures": failures, "neutral_preflight": neutral, "terminal": terminal,
               "final_marker_observed": True, "fixture_preimage": probe.bind(RUN / "fixture-preimage.txt"),
               "fixture_after": probe.bind(RUN / "fixture-after.txt"), "control": probe.bind(RUN / "control.json"),
               "prompt_intent": probe.bind(RUN / "prompt-intent.json"), "timestamp_utc": datetime.now().astimezone().isoformat()}
probe.atomic_json(RUN / "failure-observation.json", observation)
probe.cleanup()
probe.check_source()
cleanup = probe.read(RUN / "cleanup.json")
summary = {"status": "verified-native-direct5s-preToolUse-timeout-read-blocked", "source_revision": 36,
    "source_lock_hash": probe.EXPECTED, "source_modified": False, "surface": "cursor-cli-interactive-terminal",
    "version": failure["native_version"], "model_requested": probe.MODEL, "effort_requested": "xhigh",
    "model_turns": 1, "prompt_submissions": 1, "requested_tool": "Read", "native_tool_use_id": failure["native_tool_use_id"],
    "direct_packaged_timeout_seconds": 5, "after_failure_logger_timeout_seconds": 10,
    "fault_origin": "none", "packaged_event_observer_invoked": False,
    "case_policy_receipts": 3, "startup_policy_receipts": len(control["receipt_preimage"]),
    "preflight_decision": "allow", "neutral_preflight_hash_matches_selected_read": True,
    "native_tool_result": "permission_denied", "native_error": failure["scrubbed_selected_read_error"],
    "cause_scope": "actual native response for this selected Read only; earlier direct failures remain unqualified",
    "successful_read": False, "fixture_sha256_before": prep["before_sha256"],
    "fixture_sha256_after": probe.digest_file(fixture), "fixture_unchanged": True, "model_final_marker_observed": True,
    "postToolUse_receipts": 0, "pre_delivery_receipts": 0,
    "terminal_poll_truncated": poll.get("original_token_count", 0) > 12000 or poll["output"].startswith("Warning: truncated output"),
    "raw_model_frames": "not-retained", "full_transcript_read": False,
    "local_timing_seconds": [p["elapsed_seconds"] for p in timing["rows"]],
    "local_timing_scope": "three synthetic subprocess controls; does not explain native overhead or qualify timing",
    "observation": probe.bind(RUN / "failure-observation.json"), "preparation": probe.bind(RUN / "preparation.json"),
    "definition": probe.bind(RUN / "definitions/session.json"), "local_timing": probe.bind(RUN / "local-runner-timing.json"),
    "cleanup": probe.bind(RUN / "cleanup.json"), "process_audit": probe.bind(RUN / "final-process-audit.json"),
    "terminal_exit": probe.bind(RUN / "terminal-final-observation.json"), "terminal_exit_code": 1,
    "historical_members_preserved": cleanup["historical_members_unchanged"], "protected_global_configs_unchanged": True,
    "cli_state_hash_before": cleanup["global_cli_hash_before"], "cli_state_hash_after": cleanup["global_cli_hash_after"],
    "cli_state_hash_unchanged": cleanup["global_cli_hash_before"] == cleanup["global_cli_hash_after"], "global_direct_write": False,
    "agy_window_observation": probe.bind(RUN / "agy-window-continuation.json"), "full_native_gate": "unchecked",
    "backend_attestation": "not-observed", "billing": "not-observed", "verifier": probe.bind(Path(__file__))}
probe.atomic_json(RUN / "native-failure-summary.json", summary)
with REPORT.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": summary["status"], "historical_preserved": cleanup["historical_members_unchanged"],
                  "native_failure_count": 1, "source_modified": False}))
