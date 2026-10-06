"""Verify a declared direct timing candidate without promoting source defaults."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owned_direct_timeout_delivery", RUN / "cursor-direct-timeout-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
REPORT = probe.WORK / "plans/reports/delivery-261005-1610-r36-cursor-direct-timeout-control.json"
assert not REPORT.exists() and not (RUN / "native-timeout-summary.json").exists()
prep = probe.read(RUN / "preparation.json")
control = probe.read(RUN / "control.json")
definition = probe.read(RUN / "definitions/session.json")
assert probe.digest_file(probe.CONFIG) == definition["config_sha256"]
assert probe.digest_file(probe.EVIDENCE / "context-active.json") == control["context_file_sha256"]
assert definition["preToolUse_timeout_seconds"] == 20 and definition["other_packaged_timeout_seconds"] == 5
assert not definition["observer_invoked_for_packaged_events"] and definition["source_default_unchanged"]
intent = probe.read(RUN / "prompt-intent.json")
assert intent["prompt"] == prep["prompt"] and intent["session_id"] == 35458
policies = [{**probe.bind(p), "receipt": probe.read(p)} for p in sorted((probe.EVIDENCE / "policy-receipts").glob("*.json"))
            if p.relative_to(probe.EVIDENCE).as_posix() not in control["receipt_preimage"]]
assert len(policies) == 4
assert sorted(p["receipt"]["phase"] for p in policies) == ["advisory", "pre-delivery", "preflight", "stop"]
assert all(p["receipt"]["context_hash"] == control["context_file_sha256"] for p in policies)
matches = []
for p in policies:
    r = p["receipt"]
    if r["phase"] not in {"preflight", "pre-delivery"}:
        continue
    neutral = {"schema_version": 1, "phase": r["phase"], "host": "cursor", "tool": "Read", "paths": [prep["relative"]],
               "session_key": r["session_key"], "task_key": r["task_key"], "artifact_sha256": r["artifact_sha256"], "stop_active": False}
    assert probe.digest_record(neutral) == r["event_hash"]
    matches.append({"policy": probe.bind(probe.WORK / p["path"]), "neutral": neutral, "hash_matches": True})
pre = next(p["receipt"] for p in policies if p["receipt"]["phase"] == "preflight")
post = next(p["receipt"] for p in policies if p["receipt"]["phase"] == "pre-delivery")
assert pre["decision"] == "allow" and post["decision"] == "pending"
failures = list((probe.EVIDENCE / "native-failures").glob("*.json"))
assert not failures
fixture = probe.contained(probe.PROJECT, prep["relative"])
assert fixture.read_bytes() == (RUN / "fixture-preimage.txt").read_bytes()
assert probe.digest_file(fixture) == prep["before_sha256"]
with (RUN / "fixture-after.txt").open("xb") as stream:
    stream.write(fixture.read_bytes())
poll = probe.read(RUN / "terminal-poll-01.json")
assert "  " + prep["marker"] + "\u001b[K" in poll["output"]
assert poll.get("original_token_count", 0) <= 20000 and not poll["output"].startswith("Warning: truncated output")
assert probe.read(RUN / "terminal-final-observation.json")["response"]["exit_code"] == 1
audit = probe.read(RUN / "final-process-audit.json")
assert audit["matching_count"] == audit["tracked_live_count"] == 0
base = probe.WORK / "plans/runs/nckh-native-261005-1550-r36-cursor-direct-failure-observer-attempt-12"
assert probe.read(base / "stage.json")["payload"]["members"] == probe.read(RUN / "stage.json")["payload"]["members"]
assert probe.digest_file(base / "native-failure-observer.py") == probe.digest_file(RUN / "native-failure-observer.py")
observation = {"policies": policies, "neutral_hash_matches": matches, "failure_receipts": [],
    "fixture_after": probe.bind(RUN / "fixture-after.txt"), "control": probe.bind(RUN / "control.json"),
    "terminal": [probe.bind(p) for p in sorted(RUN.glob("terminal-*.json"))],
    "native_tool_use_id": "not-retained-direct-policy-receipts", "raw_tool_return_content": "not-retained"}
probe.atomic_json(RUN / "timeout-observation.json", observation)
probe.cleanup()
probe.check_source()
cleanup = probe.read(RUN / "cleanup.json")
summary = {"status": "verified-direct-preToolUse20s-read-pre-post-control", "source_revision": 36,
    "source_lock_hash": probe.EXPECTED, "source_modified": False, "source_default_unchanged": True,
    "surface": "cursor-cli-interactive-terminal", "version": probe.read(RUN / "native-metadata.json")["version"],
    "model_requested": probe.MODEL, "effort_requested": "xhigh", "model_turns": 1, "prompt_submissions": 1,
    "requested_tool": "Read", "preToolUse_timeout_seconds": 20, "other_packaged_timeout_seconds": 5,
    "diagnostic_failure_timeout_seconds": 10, "packaged_event_observer_invoked": False, "fault_origin": "none",
    "case_policy_receipts": 4, "startup_policy_receipts": len(control["receipt_preimage"]),
    "native_pre_post_read_hash_matches": 2, "native_failure_receipts": 0, "model_final_marker_observed": True,
    "fixture_unchanged": True, "artifact_QA": "pending", "native_tool_use_id": "not-retained",
    "raw_tool_return_content": "not-retained", "terminal_truncated": False,
    "scope": "one direct20s-preToolUse Read control; does not qualify mutation, all-event timing or host overhead cause",
    "base_failure": probe.bind(base / "native-failure-summary.json"), "observation": probe.bind(RUN / "timeout-observation.json"),
    "preparation": probe.bind(RUN / "preparation.json"), "definition": probe.bind(RUN / "definitions/session.json"),
    "cleanup": probe.bind(RUN / "cleanup.json"), "process_audit": probe.bind(RUN / "final-process-audit.json"),
    "terminal_exit": probe.bind(RUN / "terminal-final-observation.json"), "terminal_exit_code": 1,
    "historical_members_preserved": cleanup["historical_members_unchanged"], "protected_global_configs_unchanged": True,
    "cli_state_hash_before": cleanup["global_cli_hash_before"], "cli_state_hash_after": cleanup["global_cli_hash_after"],
    "cli_state_hash_unchanged": cleanup["global_cli_hash_before"] == cleanup["global_cli_hash_after"], "global_direct_write": False,
    "full_native_gate": "unchecked", "backend_attestation": "not-observed", "billing": "not-observed", "verifier": probe.bind(Path(__file__))}
probe.atomic_json(RUN / "native-timeout-summary.json", summary)
with REPORT.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": summary["status"], "historical_preserved": cleanup["historical_members_unchanged"], "source_modified": False}))
