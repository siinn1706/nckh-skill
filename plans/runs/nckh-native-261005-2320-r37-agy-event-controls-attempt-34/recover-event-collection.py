"""Reconcile a partial collection without rerunning or changing its frozen oracles."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = WORK / "plans/runs/nckh-native-261005-0005-r34-attempt-01/projects/agy-model"
EVIDENCE = PROJECT / ".nckh-native-r37-agy-event-controls-34"
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {"path": p.relative_to(WORK).as_posix(), "sha256": sha(p)}
brief = read(RUN / "frozen-brief.json")
summary = read(RUN / "native-event-summary.json")
failure = read(RUN / "native-event-failure.json")
assert summary["status"] == "running" and len(summary["results"]) == failure["completed_cases"] == 23
assert failure["error"] == "Observed hook child still running; stop dependent turns"
assert read(RUN / "orphan-inspection.json")["count"] == 0
assert read(RUN / "process-final-audit.json")["tracked_live_count"] == 0
results = []
for index, case in enumerate(brief["cases"]):
    path = RUN / "attempts" / (case["name"] + ".json")
    if not path.exists():
        break
    attempt = read(path)
    assert attempt["process_exited"] and attempt["exit_code"] == 0
    callbacks = sorted((EVIDENCE / "observations" / case["name"] / case["event"]).glob("*.json"))
    policies = sorted((EVIDENCE / "policy-receipts" / case["name"] / case["event"]).glob("*.json"))
    target = PROJECT / case["fixture"]
    result = dict(summary["results"][index]) if index < len(summary["results"]) else {
        "attempt": case["name"], "event": case["event"], "mode": case["mode"], "receipt": bind(path),
        "native_terminal_states": [t["state"] for t in attempt["terminal_tools"]], "native_exit_code": attempt["exit_code"],
        "exact_revised_bytes": target.read_bytes() == bytes.fromhex(case["requested_hex"]),
        "exact_unchanged_bytes": target.read_bytes() == bytes.fromhex(case["initial_hex"]),
        "final_marker_observed": any(f.get("event") == "result" and f["result"].get("response", "").strip() ==
                                     "ORACLE_ATTEMPT_FINISHED" for f in attempt["native_frames"]),
        "process_exited": True, "timing_scope": "after final model response; native tool already occurred"}
    result.update(selected_callback_count=len(callbacks), selected_policy_bindings=[bind(p) for p in policies],
        selected_policy_decisions=[read(p)["decision"] for p in policies],
        reconciled_callback_bindings=[bind(p) for p in sorted((EVIDENCE / "observations" / case["name"]).glob("*/*.json"))],
        child_reconciliation="original per-turn receipt" if (RUN / "commands" / ("agy-tools-" + case["name"] +
            ".child-reconciliation.json")).exists() else "original wait failed; later exact-identity inspection and final union audit zero",
        status="recorded-native-callback-after-process-reconciliation")
    results.append(result)
assert len(results) == 24
output = {"status": "recorded-24-native-event-cases-with-original-child-wait-failure", "source_revision": 37,
    "source_lock_hash": brief["source_lock_hash"], "model_turns": 24, "model_retries": 0,
    "results": results, "frozen_brief": bind(RUN / "frozen-brief.json"), "original_summary": bind(RUN / "native-event-summary.json"),
    "original_failure": bind(RUN / "native-event-failure.json"), "original_collection_command": "exit 1 retained",
    "not_run_cases": [c["name"] for c in brief["cases"][24:]], "full_native_gate": "unchecked",
    "recovery": "read-only reconciliation after observed descendants exited; no taskkill or model resubmission",
    "process_audit": bind(RUN / "process-final-audit.json"), "recovery_controller": bind(Path(__file__))}
with (RUN / "native-event-recovery.json").open("x", encoding="utf8") as stream:
    json.dump(output, stream, ensure_ascii=False, indent=2)
print(json.dumps({"status": output["status"], "actual_turns": 24, "not_run_cases": output["not_run_cases"]}))
