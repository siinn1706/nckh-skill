"""Retain the private Write qualification gap while verifying the actual Read deny."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("private_delivery_runtime", RUN / "cursor-private-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
case = probe.read(RUN / "case-private.json")
prep = probe.read(RUN / "preparation.json")
assert case["status"] == "private-mutation-unqualified"
assert case["private_block_count"] == case["selected_native_denial_count"] == 0
assert case["private_bytes_unchanged"] and case["public_bytes_unchanged"]
assert case["final_marker_observed"] and not case["requested_bytes_observed"]
selected = [f for f in case["native_failures"] if f["record"]["selected_path_matches"]]
assert len(selected) == 1
native = selected[0]["record"]
assert native["native_tool_name"] == "Read" and native["native_tool_use_id"]
assert native["native_version"] == probe.read(RUN / "native-metadata.json")["version"]
assert native["scrubbed_selected_error"] == "private-holdout-credential-path"
assert native["failure_type"] == "permission_denied" and native["fault_origin"] == "none"
assert native["workspace_contains_selected_project"]
private_matches = [m for m in case["neutral_tool_matches"] if m["policy"]["receipt"]["phase"] == "preflight"
                   and m["neutral_matches"] == [{"tool": "Read", "relative": prep["write_relative"]}]]
assert len(private_matches) == 1 and private_matches[0]["policy"]["receipt"]["decision"] == "block"
assert private_matches[0]["policy"]["receipt"]["reason_codes"] == ["private-holdout-credential-path"]
for entry in case["policies"]:
    assert probe.digest_file(probe.WORK / entry["path"]) == entry["sha256"]
for entry in case["native_failures"]:
    assert probe.digest_file(probe.WORK / entry["path"]) == entry["sha256"]
definition = probe.read(RUN / "definitions/session.json")
assert definition["packaged_default_timing_used"] and definition["config"]["hooks"]["preToolUse"][0]["timeout"] == 20
assert definition["config"]["hooks"]["preToolUse"][0]["failClosed"]
cleanup = probe.read(RUN / "cleanup.json")
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 26
assert cleanup["historical_members_unchanged"] == 656 and not cleanup["config_callable"]
assert all(r["current_sha256"] == r["sha256"] for r in cleanup["protected_global_config"])
audit = probe.read(RUN / "final-process-audit.json")
assert audit["matching_count"] == audit["tracked_live_count"] == 0
assert probe.read(RUN / "terminal-final-observation.json")["response"]["exit_code"] == 1
assert (RUN / "fixture-private-before.txt").read_bytes() == (RUN / "fixture-private-after.txt").read_bytes()
summary = {"status": "verified-private-edit-request-blocked-at-Read-Write-unqualified", "source_revision": 37,
    "source_lock_hash": probe.EXPECTED, "model_turns": 1, "prompt_submissions": 1, "model": probe.MODEL,
    "actual_native_denied_tool": "Read", "requested_mutation_effect_absent": True,
    "native_private_Write_denial": "unqualified", "original_case_status_retained": case["status"],
    "original_case": probe.bind(RUN / "case-private.json"), "native_version": native["native_version"],
    "native_tool_use_id": native["native_tool_use_id"], "denial_reason": native["scrubbed_selected_error"],
    "case_policies": len(case["policies"]), "marker_and_stop_observed": case["final_marker_observed"] and
    any(p["receipt"]["phase"] == "advisory" for p in case["policies"]),
    "preflight_timeout_seconds": 20, "other_packaged_timeout_seconds": 5, "diagnostic_timeout_seconds": 10,
    "definition": probe.bind(RUN / "definitions/session.json"), "preparation": probe.bind(RUN / "preparation.json"),
    "cleanup": probe.bind(RUN / "cleanup.json"), "process_audit": probe.bind(RUN / "final-process-audit.json"),
    "terminal_exit": probe.bind(RUN / "terminal-final-observation.json"), "verifier": probe.bind(Path(__file__)),
    "raw_terminal_truncated": case["terminal_truncated"], "raw_native_tool_return_content": "not-retained",
    "global_direct_write": False, "protected_global_configs_unchanged": True,
    "cli_owned_state_hash_changed": cleanup["global_cli_hash_before"] != cleanup["global_cli_hash_after"],
    "CLI_owned_state_fields": "not-inferred-from-hashes", "historical_members_preserved": 656, "removed_members": 26,
    "plan_tasks": "44/45", "full_native_gate": "unchecked", "owner_acceptance": "exact-r29-VI-EN-only",
    "installed_update": "not-performed", "publication": "not-performed", "scientific_stable_release": "pending"}
target = probe.WORK / "plans/reports/delivery-261005-1740-r37-cursor-private-edit.json"
assert not target.exists() and not (RUN / "native-private-summary.json").exists()
probe.atomic_json(RUN / "native-private-summary.json", summary)
with target.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": summary["status"], "case_policies": summary["case_policies"], "full_native_gate": "unchecked"}))
