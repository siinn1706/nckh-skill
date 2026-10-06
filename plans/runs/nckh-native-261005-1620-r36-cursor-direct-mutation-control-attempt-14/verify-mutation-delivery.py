"""Verify direct mutation and preventive denial; retain capture/controller failures."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owned_direct_mutation_delivery", RUN / "cursor-direct-mutation-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
REPORT = probe.WORK / "plans/reports/delivery-261005-1620-r36-cursor-direct-mutation-control.json"
assert not REPORT.exists() and not (RUN / "native-mutation-summary.json").exists()
prep = probe.read(RUN / "preparation.json")
assert prep["maximum_model_turns"] == prep["maximum_prompt_submissions"] == 2
definition = probe.read(RUN / "definitions/session.json")
assert probe.digest_file(probe.CONFIG) == definition["config_sha256"]
assert definition["preToolUse_timeout_seconds"] == 20 and definition["other_packaged_timeout_seconds"] == 5
assert not definition["observer_invoked_for_packaged_events"]
allow, deny = (probe.read(RUN / ("case-" + name + ".json")) for name in ("allow", "deny"))
assert allow["bytes_changed"] and allow["requested_bytes_observed"] and allow["final_marker_observed"]
assert not allow["native_failures"]
assert not deny["bytes_changed"] and not deny["requested_bytes_observed"] and deny["final_marker_observed"]
assert deny["before_sha256"] == deny["after_sha256"] == allow["after_sha256"]
fixture = probe.contained(probe.PROJECT, prep["relative"])
assert probe.digest_file(fixture) == deny["after_sha256"]
assert fixture.read_bytes() == (RUN / "fixture-allow-after.txt").read_bytes() == (RUN / "fixture-deny-before.txt").read_bytes() == (RUN / "fixture-deny-after.txt").read_bytes()
for row in (allow, deny):
    assert all(m["neutral_tool_matches"] for m in row["neutral_tool_matches"])
    assert any(p["receipt"]["phase"] == "stop" for p in row["policies"])
    for binding in row["policies"] + row["native_failures"] + row["terminal"] + [row["control"], row["fixture_after"]]:
        assert probe.digest_file(probe.WORK / binding["path"]) == binding["sha256"]
allowed_write = [m for m in allow["neutral_tool_matches"] if m["neutral_tool_matches"] == ["Write"]]
denied_write = [m for m in deny["neutral_tool_matches"] if m["neutral_tool_matches"] == ["Write"]]
assert sorted((m["policy"]["receipt"]["phase"], m["policy"]["receipt"]["decision"]) for m in allowed_write) == [("pre-delivery", "pending"), ("preflight", "allow")]
assert len(denied_write) == 1 and denied_write[0]["policy"]["receipt"]["phase"] == "preflight"
assert denied_write[0]["policy"]["receipt"]["decision"] == "block"
assert "plan-only-mutation" in denied_write[0]["policy"]["receipt"]["reason_codes"]
assert len(deny["native_failures"]) == 1
failure = deny["native_failures"][0]["record"]
assert failure["native_tool_name"] == "Write" and failure["selected_path_matches"] and failure["workspace_contains_selected_project"]
assert failure["failure_type"] == "permission_denied" and failure["scrubbed_selected_error"] == "plan-only-mutation"
assert failure["reported_event"] == "postToolUseFailure" and failure["native_version"] == "2026.09.15-d2fe57e"
assert not failure["policy_invoked"] and not failure["full_transcript_read"] and failure["fault_origin"] == "none"
assert probe.read(RUN / "final-process-audit.json")["matching_count"] == probe.read(RUN / "final-process-audit.json")["tracked_live_count"] == 0
assert probe.read(RUN / "terminal-final-observation.json")["response"]["exit_code"] == 1
assert len(allow["terminal_recording_losses"]) == 1 and deny["terminal_truncated"]
probe.cleanup()
probe.check_source()
cleanup = probe.read(RUN / "cleanup.json")
summary = {"status": "verified-direct-preToolUse20s-write-allow-and-plan-only-prevention", "source_revision": 36,
    "source_lock_hash": probe.EXPECTED, "source_modified": False, "source_default_unchanged": True,
    "surface": "cursor-cli-interactive-terminal", "version": failure["native_version"],
    "model_requested": probe.MODEL, "effort_requested": "xhigh", "model_turns": 2, "prompt_submissions": 2,
    "preToolUse_timeout_seconds": 20, "other_packaged_timeout_seconds": 5, "after_failure_logger_timeout_seconds": 10,
    "packaged_event_observer_invoked": False, "fault_origin": "none", "public_write": "exact-requested-bytes-observed",
    "plan_only_Write_prevention": "native-permission_denied-plan-only-mutation; file-byte-identical",
    "allow_before_sha256": allow["before_sha256"], "allow_after_sha256": allow["after_sha256"],
    "deny_before_sha256": deny["before_sha256"], "deny_after_sha256": deny["after_sha256"],
    "native_denied_tool_use_id": failure["native_tool_use_id"],
    "policy_native_ID_correlation": "neutral-event-hash binding; policy receipt itself omits native ID",
    "artifact_QA": "pending", "cases": [probe.bind(RUN / ("case-" + name + ".json")) for name in ("allow", "deny")],
    "terminal_capture_limitations": "one allow raw chunk lost after64KB save rejection; deny chunk truncated; retained native receipts/effects verified",
    "recording_failure": allow["terminal_recording_losses"][0],
    "controller_failures": [probe.bind(RUN / name) for name in ("collector-log-filter-failure.json", "collector-hash-interface-failure.json")],
    "controller_model_retries": 0, "preparation": probe.bind(RUN / "preparation.json"),
    "definition": probe.bind(RUN / "definitions/session.json"), "cleanup": probe.bind(RUN / "cleanup.json"),
    "process_audit": probe.bind(RUN / "final-process-audit.json"), "terminal_exit": probe.bind(RUN / "terminal-final-observation.json"),
    "terminal_exit_code": 1, "historical_members_preserved": cleanup["historical_members_unchanged"],
    "protected_global_configs_unchanged": True, "cli_state_hash_before": cleanup["global_cli_hash_before"],
    "cli_state_hash_after": cleanup["global_cli_hash_after"],
    "cli_state_hash_unchanged": cleanup["global_cli_hash_before"] == cleanup["global_cli_hash_after"], "global_direct_write": False,
    "scope": "direct20s public Write allow and plan-only Write deny; does not qualify private mutation or full event/surface/version matrix",
    "full_native_gate": "unchecked", "backend_attestation": "not-observed", "billing": "not-observed", "verifier": probe.bind(Path(__file__))}
probe.atomic_json(RUN / "native-mutation-summary.json", summary)
with REPORT.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": summary["status"], "historical_preserved": cleanup["historical_members_unchanged"], "source_modified": False}))
