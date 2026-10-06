"""Verify the admission failure separately from an unrun native tool oracle."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("admission_failure_runtime", RUN / "cursor-uncovered-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
terminal = probe.read(RUN / "terminal-ready-01.json")
case = probe.read(RUN / "case-uncovered-search.json")
cleanup = probe.read(RUN / "cleanup.json")
audit = probe.read(RUN / "final-process-audit.json")
failure = probe.read(RUN / "admission-controller-failure.json")
assert terminal["exit_code"] == 1 and "session_id" not in terminal
assert "Cannot use this model: " + probe.MODEL in terminal["output"]
assert not (RUN / "prompt-intent-search.json").exists() and not (RUN / "native-process-ownership.json").exists()
assert failure["prompt_submissions"] == failure["native_model_turns"] == 0
assert case["status"] == "native-uncovered-search-unqualified"
assert not case["callbacks"] and not case["policies"] and not case["actual_tools"]
assert case["fixture_unchanged"] and not case["final_marker_observed"]
assert (RUN / "fixture-before.txt").read_bytes() == (RUN / "fixture-after.txt").read_bytes()
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 27 and not cleanup["config_callable"]
history = probe.read(RUN / "historical-project-preimage.json")["members"]
assert cleanup["historical_members_unchanged"] == len(history)
assert all(probe.digest_file(probe.contained(probe.PROJECT, p)) == h for p,h in history.items())
assert all(row["current_sha256"] == row["sha256"] for row in cleanup["protected_global_config"])
assert audit["matching_count"] == 0 and audit["process_stop_performed"] is False
correlation = probe.read(RUN / "startup-process-ownership-correlation.json")
assert not correlation["strict_PID_and_UTC_string_matches"]
assert all(row["creation_utc"] < "2026-10-05T12:39:51Z" for row in correlation["unattributed_candidates"])
summary = {"status": "verified-model-admission-rejected-no-prompt-native-search-unqualified",
    "source_revision": 37, "source_lock_hash": probe.EXPECTED, "requested_model": probe.MODEL,
    "native_model_turns": 0, "prompt_submissions": 0, "native_callbacks": 0, "policy_receipts": 0,
    "native_terminal_exit_code": 1, "failure_class": "explicit-model-specifier-admission-rejection",
    "fixture_unchanged": True, "original_case_status_retained": case["status"],
    "original_case": probe.bind(RUN / "case-uncovered-search.json"), "terminal": probe.bind(RUN / "terminal-ready-01.json"),
    "controller_failures": probe.bind(RUN / "admission-controller-failure.json"),
    "cleanup": probe.bind(RUN / "cleanup.json"), "process_audit": probe.bind(RUN / "final-process-audit.json"),
    "historical_members_preserved": len(history), "removed_members": 27,
    "startup_process_correlation": probe.bind(RUN / "startup-process-ownership-correlation.json"),
    "startup_process_scope": "36 unowned startup candidates predate this launch; no process stopped or ownership invented",
    "native_root_ownership": "not-captured-before-exit; absent root is not assigned a PID",
    "protected_global_configs_unchanged": True, "global_direct_write": False,
    "scope_limit": "No native tool oracle ran; this failure does not regrade earlier successful granted model turns",
    "verifier": probe.bind(Path(__file__)), "plan_tasks": "44/45", "full_native_gate": "unchecked"}
with (RUN / "native-admission-summary.json").open("x", encoding="utf8") as stream:
    json.dump(summary, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
print(json.dumps({"status": summary["status"], "prompt_submissions": 0, "removed": 27, "history_preserved": len(history)}))
