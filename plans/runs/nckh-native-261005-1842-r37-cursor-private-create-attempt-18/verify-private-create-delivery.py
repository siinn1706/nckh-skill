"""Verify the observed Read denial and retain the separate native Write gap."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("private_create_delivery", RUN / "cursor-private-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
case = probe.read(RUN / "case-private.json")
prep = probe.read(RUN / "preparation.json")
assert case["status"] == "private-create-unqualified"
assert case["private_block_count"] == case["selected_native_denial_count"] == 0
assert not case["private_before_exists"] and not case["private_after_exists"]
assert case["requested_creation_effect_absent"] and case["final_marker_observed"]
assert not probe.contained(probe.PROJECT, prep["write_relative"]).exists()
selected = [f for f in case["native_failures"] if f["record"]["selected_path_matches"]]
assert len(selected) == 1
native = selected[0]["record"]
assert native["native_tool_name"] == "Read" and native["native_tool_use_id"]
assert native["native_version"] == probe.read(RUN / "native-metadata.json")["version"]
assert native["scrubbed_selected_error"] == "private-holdout-credential-path"
assert native["failure_type"] == "permission_denied" and native["fault_origin"] == "none"
assert native["workspace_contains_selected_project"]
matches = [m for m in case["neutral_tool_matches"] if m["policy"]["receipt"]["phase"] == "preflight"
    and m["neutral_matches"] == [{"tool": "Read", "relative": prep["write_relative"]}]]
assert len(matches) == 1 and matches[0]["policy"]["receipt"]["decision"] == "block"
assert matches[0]["policy"]["receipt"]["reason_codes"] == ["private-holdout-credential-path"]
assert not any(m["policy"]["receipt"]["phase"] == "pre-delivery" for m in case["neutral_tool_matches"])
for entry in case["policies"] + case["native_failures"] + case["terminal"]:
    assert probe.digest_file(probe.WORK / entry["path"]) == entry["sha256"]
definition = probe.read(RUN / "definitions/session.json")
assert definition["packaged_default_timing_used"]
assert definition["config"]["hooks"]["preToolUse"][0]["timeout"] == 20
assert definition["config"]["hooks"]["preToolUse"][0]["failClosed"]
cleanup = probe.read(RUN / "cleanup.json")
history = probe.read(RUN / "historical-project-preimage.json")["members"]
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 26
assert cleanup["historical_members_unchanged"] == len(history) and not cleanup["config_callable"]
assert all(probe.digest_file(probe.contained(probe.PROJECT, relative)) == expected for relative, expected in history.items())
assert all(r["current_sha256"] == r["sha256"] for r in cleanup["protected_global_config"])
audit = probe.read(RUN / "final-process-audit.json")
assert audit["matching_count"] == audit["tracked_live_count"] == 0
terminal = probe.read(RUN / "terminal-final-observation.json")["response"]
assert isinstance(terminal["exit_code"], int) and "session_id" not in terminal
assert probe.read(RUN / "process-stop-force.json")["exit_code"] == 0
summary = {"status": "verified-private-create-request-blocked-at-Read-Write-unqualified", "source_revision": 37,
    "source_lock_hash": probe.EXPECTED, "model_turns": 1, "prompt_submissions": 1, "model": probe.MODEL,
    "actual_native_denied_tool": "Read", "requested_creation_effect_absent": True,
    "native_private_Write_denial": "unqualified", "original_case_status_retained": case["status"],
    "original_case": probe.bind(RUN / "case-private.json"), "native_version": native["native_version"],
    "native_tool_use_id": native["native_tool_use_id"], "denial_reason": native["scrubbed_selected_error"],
    "case_policies": len(case["policies"]), "final_marker_observed": case["final_marker_observed"],
    "stop_receipt_observed": any(p["receipt"]["phase"] == "stop" for p in case["policies"]),
    "absent_target_before_and_after": True, "native_Write_callback_observed": False,
    "preflight_timeout_seconds": 20, "other_packaged_timeout_seconds": 5, "diagnostic_timeout_seconds": 10,
    "definition": probe.bind(RUN / "definitions/session.json"), "preparation": probe.bind(RUN / "preparation.json"),
    "cleanup": probe.bind(RUN / "cleanup.json"), "process_audit": probe.bind(RUN / "final-process-audit.json"),
    "terminal_exit": probe.bind(RUN / "terminal-final-observation.json"), "terminal_exit_code": terminal["exit_code"],
    "verifier": probe.bind(Path(__file__)), "raw_terminal_truncated": case["terminal_truncated"],
    "raw_native_tool_return_content": "not-retained", "global_direct_write": False,
    "protected_global_configs_unchanged": True,
    "cli_owned_state_hash_changed": cleanup["global_cli_hash_before"] != cleanup["global_cli_hash_after"],
    "CLI_owned_state_fields": "not-inferred-from-hashes", "historical_members_preserved": len(history), "removed_members": 26,
    "agy_observation": probe.bind(RUN / "agy-window-continuation-observation.json"),
    "agy_scope": "running without an AGY-owned targetable window; no app input; access/unlock grants retained",
    "plan_tasks": "44/45", "full_native_gate": "unchecked", "owner_acceptance": "exact-r29-VI-EN-only",
    "installed_update": "not-performed", "publication": "not-performed", "scientific_stable_release": "pending"}
target = probe.WORK / "plans/reports/delivery-261005-1842-r37-cursor-private-create.json"
assert not target.exists() and not (RUN / "native-private-summary.json").exists()
probe.atomic_json(RUN / "native-private-summary.json", summary)
with target.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": summary["status"], "history_preserved": len(history), "full_native_gate": "unchecked"}))
