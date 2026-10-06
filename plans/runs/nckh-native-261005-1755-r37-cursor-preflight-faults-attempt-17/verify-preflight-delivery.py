"""Verify revision-bound native observations without closing the full matrix."""

import importlib.util
import json
from datetime import datetime
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("preflight_delivery_runtime", RUN / "cursor-preflight-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
prep = probe.read(RUN / "preparation.json")
definition = probe.read(RUN / "definitions/session.json")
assert definition["config"]["hooks"]["preToolUse"][0]["timeout"] == 20
assert definition["config"]["hooks"]["preToolUse"][0]["failClosed"]
assert all(h[0]["timeout"] == 5 for e,h in definition["config"]["hooks"].items() if e not in {"preToolUse", "postToolUseFailure"})
metadata = probe.read(RUN / "native-metadata.json")
params = {p["id"]: p["value"] for p in metadata["selected_model"]["parameters"]}
assert metadata["selected_model"]["modelId"] == "grok-4.7" and params["context"] == "500k"
assert params["reasoning_effort"] == "xhigh" and params["fast"] == "false"
rows = []
all_ids = []
for number in range(1,6):
    case_path = RUN / f"case-{number}.json"
    case = probe.read(case_path)
    assert case["selected_observers_terminal"] and case["model_reply_marker_observed"]
    assert case["fixture_unchanged"] and case["fixture_after_sha256"] == prep["before_sha256"]
    assert case["prompt_retries"] == 0 and case["fault_origin"] == "controller-injection-after-genuine-callback"
    assert len(case["observations"]) == 1
    callback = case["observations"][0]["record"]
    assert callback["native_tool_name"] == "Read" and callback["native_version"] == metadata["version"]
    assert callback["native_path_fields"]["file_path"] == str(probe.contained(probe.PROJECT, prep["relative"]))
    assert callback["native_tool_use_id"] and callback["reported_event"] == "preToolUse"
    all_ids.append(callback["native_tool_use_id"])
    selected = [f["record"] for f in case["native_failures"] if f["record"].get("selected_path_matches")]
    for failure in selected:
        assert failure["native_tool_use_id"] == callback["native_tool_use_id"]
        assert failure["native_tool_name"] == "Read" and failure["native_version"] == metadata["version"]
        assert failure["failure_type"] == "permission_denied" and failure["workspace_contains_selected_project"]
    for collection in ("observations", "policy_receipts", "direct_receipts", "native_failures", "terminal"):
        for entry in case[collection]:
            assert probe.digest_file(probe.WORK / entry["path"]) == entry["sha256"]
    elapsed = None
    if callback.get("completed_at"):
        elapsed = (datetime.fromisoformat(callback["completed_at"]) - datetime.fromisoformat(callback["started_at"])).total_seconds()
    rows.append({"index": number, "mode": case["case"]["mode"], "case": probe.bind(case_path),
        "callback": case["observations"][0]["path"], "native_tool_use_id": callback["native_tool_use_id"],
        "observer_status": callback["status"], "observer_elapsed_seconds": elapsed,
        "runner_output": callback.get("runner_output", "not-invoked"),
        "selected_native_denial_count": len(selected), "native_selected_errors": [f["scrubbed_selected_error"] for f in selected],
        "selected_read_post_receipts": case["actual_selected_read_post_receipts"],
        "degraded_receipts_without_context_hash": len(case["degraded_without_context_hash"]),
        "marker_observed": True, "fixture_unchanged": True, "terminal_truncated": case["terminal_truncated"]})
assert len(set(all_ids)) == 5
cleanup = probe.read(RUN / "cleanup.json")
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 26 and not cleanup["config_callable"]
assert all(r["sha256"] == r["current_sha256"] for r in cleanup["protected_global_config"])
assert probe.read(RUN / "final-process-audit.json")["matching_count"] == 0
assert probe.read(RUN / "final-process-audit.json")["tracked_live_count"] == 0
assert probe.read(RUN / "terminal-final-observation.json")["response"]["exit_code"] == 1
assert probe.read(RUN / "collector-attempt-01-failure.json")["native_prompt_retries"] == 0
summary = {"status": "verified-five-native-preToolUse-Read-fault-observations", "source_revision": 37,
    "source_lock_hash": probe.EXPECTED, "native_version": metadata["version"], "surface": "cursor-cli",
    "model": probe.MODEL, "prompt_submissions": 5, "observed_model_reply_markers": 5, "distinct_native_tool_ids": 5,
    "rows": rows, "callback_scope": "Five genuine preToolUse/Read callbacks; explicit faults applied after native callback",
    "fault_origin": "controller-injection-after-genuine-callback", "preflight_timeout_seconds": 20,
    "inner_runner_timeout_seconds": 5, "timeout_injection_seconds": 24, "other_packaged_handler_timeout_seconds": 5,
    "diagnostic_timeout_seconds": 10, "preflight_handler_kind": "instrumented fault observer; default 20s/failClosed retained",
    "unsupported_scope": prep["unsupported_scope"], "private_Write_gate": "unqualified",
    "cleanup_removed_members": 26, "historical_members_preserved": cleanup["historical_members_unchanged"],
    "cleanup": probe.bind(RUN / "cleanup.json"), "process_audit": probe.bind(RUN / "final-process-audit.json"),
    "terminal_exit": probe.bind(RUN / "terminal-final-observation.json"), "definition": probe.bind(RUN / "definitions/session.json"),
    "collector_failure": probe.bind(RUN / "collector-attempt-01-failure.json"), "verifier": probe.bind(Path(__file__)),
    "degraded_receipt_limit": "Parse failure receipts omit context_hash; correlate via selected genuine callback/control/runner and native failure ID",
    "protected_global_configs_unchanged": True, "global_direct_write": False,
    "cli_owned_state_hash_changed": cleanup["global_cli_hash_before"] != cleanup["global_cli_hash_after"],
    "cli_state_fields": "not-inferred-from-hashes", "billing_backend_attestation": "not-observed",
    "native_tool_return_content": "not-retained", "plan_tasks": "44/45", "full_native_gate": "unchecked",
    "owner_acceptance": "accepted-exact-r29-VI-EN-only", "installed_update": "not-performed",
    "scientific_stable_release": "pending", "publication": "not-performed"}
target = probe.WORK / "plans/reports/delivery-261005-1755-r37-cursor-preflight-faults.json"
assert not target.exists() and not (RUN / "native-preflight-summary.json").exists()
probe.atomic_json(RUN / "native-preflight-summary.json", summary)
with target.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": summary["status"], "prompts": 5,
    "denials": [r["selected_native_denial_count"] for r in rows], "full_native_gate": "unchecked"}))
