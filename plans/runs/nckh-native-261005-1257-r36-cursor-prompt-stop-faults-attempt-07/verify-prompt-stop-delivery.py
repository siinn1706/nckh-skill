"""Bind native observations without treating injected failures as enforcement."""

import importlib.util
import json
import re
from datetime import datetime
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owned_prompt_stop_delivery", RUN / "cursor-prompt-stop-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
REPORT = probe.WORK / "plans/reports/delivery-261005-1257-r36-cursor-prompt-stop-faults.json"
assert not REPORT.exists() and not (RUN / "native-prompt-stop-summary.json").exists()
preparation = probe.read(RUN / "preparation.json")
definition = probe.read(RUN / "definitions/session.json")
assert preparation["maximum_prompt_submissions"] == preparation["maximum_model_turns"] == 10
assert definition["timeout_seconds"] == 20 and definition["runner_timeout_seconds"] == 5
assert definition["timeout_injection_seconds"] == 24
assert probe.digest_file(probe.CONFIG) == definition["config_sha256"]
terminal_paths = sorted((RUN / "terminal").glob("*.json"))
submissions = sorted((RUN / "submissions").glob("*.json"))
assert len(submissions) == 10
terminal_records = [probe.read(path) for path in terminal_paths]
submission_records = [probe.read(path) for path in submissions]


def submission_responses(row):
    if "prompt_write" in row:
        return row["prompt_write"], row["enter_write"]
    assert row["prompt_submissions"] == 1
    return row["prompt_text_response"], row["separate_Enter_response"]


responses = [row["response"] for row in terminal_records]
responses += [response for row in submission_records for response in submission_responses(row)]
ansi = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
render = "\n".join(ansi.sub("", row["output"]) for row in responses)
assert "Grok 4.7 500K Extra High" in render and "Run Everything" in render
limits = [{"response_index": index, "original_token_count": row.get("original_token_count"),
           "output_characters": len(row["output"])} for index, row in enumerate(responses)
          if "truncated" in row["output"].lower() or row.get("original_token_count", 0) > 40000]
cases = []
callbacks = []
for expected, submitted in zip(preparation["cases"], submission_records):
    assert submitted["case"]["index"] == expected["index"]
    assert submitted["case"]["prompt"] == expected["prompt"]
    prompt_response, enter_response = submission_responses(submitted)
    assert prompt_response["session_id"] == enter_response["session_id"] == 78282
    path = RUN / "attempts" / (expected["attempt"] + ".json")
    attempt = probe.read(path)
    control = probe.read(RUN / "controls" / f"{expected['index']:02d}.json")
    assert attempt["ready_for_next_case"] and attempt["selected_callback_count"] == 1
    assert attempt["source_lock_hash"] == probe.EXPECTED
    for binding in attempt["callbacks"] + attempt["policy_receipts"]:
        assert probe.digest_file(probe.WORK / binding["path"]) == binding["sha256"]
    native = [binding["receipt"] for binding in attempt["callbacks"]]
    assert all(row["control_sha256"] == control["control_sha256"] for row in native)
    assert all(row["native_version"] == "2026.09.15-d2fe57e" for row in native)
    assert all(row["workspace_contains_selected_project"] for row in native)
    assert all(row["event"] in ("beforeSubmitPrompt", "stop") for row in native)
    selected = next(row for row in native if row["event"] == expected["event"])
    assert selected["fault_origin"] == "controller-injection-after-genuine-callback"
    reply = bool(re.search(r"(?:^|\n)[ \t]*" + re.escape(expected["marker"]) + r"[ \t]*\r?(?:\n|$)", render))
    admission = attempt.get("native_admission_rejection")
    if admission:
        assert expected["index"] == 1 and not reply and attempt["stop_callback_count"] == 0
        assert selected["runner_output"]["continue"] is False
        outcome = "native-prompt-rejected-no-model-reply-observed"
    else:
        assert reply and attempt["stop_callback_count"] == 1
        outcome = ("model-reply-observed-despite-selected-prompt-fault" if expected["event"] == "beforeSubmitPrompt"
                   else "model-reply-precedes-selected-stop-fault-no-extra-stop-callback")
    elapsed = None
    if expected["mode"] == "timeout":
        assert selected["status"] in ("completed", "intentional-test-sleep-twenty-four-seconds")
        if selected.get("completed_at"):
            elapsed = (datetime.fromisoformat(selected["completed_at"]) - datetime.fromisoformat(selected["started_at"])).total_seconds()
            assert elapsed >= 24
    cases.append({**expected, "observation": probe.bind(path), "control": probe.bind(RUN / "controls" / f"{expected['index']:02d}.json"),
                  "selected_callback": selected, "native_outcome": outcome, "model_reply_observed": reply,
                  "observer_elapsed_seconds": elapsed, "policy_receipts": attempt["policy_receipts"]})
    callbacks.extend(attempt["callbacks"])
assert sum(row["model_reply_observed"] for row in cases) == 9
assert len({binding["receipt"]["native_session_hash"] for binding in callbacks}) == 1
startup = [{**probe.bind(path), "receipt": probe.read(path)} for path in sorted((probe.EVIDENCE / "observations/startup").rglob("*.json"))]
assert len(startup) == 1 and startup[0]["receipt"]["event"] == "sessionStart"
exit_record = probe.read(RUN / "terminal-final-observation.json")
assert "exit_code" in exit_record["response"] and "session_id" not in exit_record["response"]
audit = probe.read(RUN / "final-process-audit.json")
assert audit["matching_count"] == 0 and not audit["matches"]
graceful = probe.read(RUN / "process-stop-graceful.json")
forced = probe.read(RUN / "process-stop-force.json")
assert graceful["root_pid"] == forced["root_pid"] == 53576
assert graceful["exit_code"] != 0 and forced["exit_code"] == 0
assert all(row["current"] is None or datetime.fromisoformat(row["current"]) == datetime.fromisoformat(row["expected"])
           for row in forced["identity_checks"])
probe.cleanup()
cleanup = probe.read(RUN / "cleanup.json")
assert cleanup["status"] == "pass" and not cleanup["config_callable"]
assert all(not probe.contained(probe.PROJECT, row["path"]).exists() for row in cleanup["removed_members"])
record = {"status": "verified-native-cursor-prompt-stop-fault-observations", "source_revision": 36,
          "source_lock_hash": probe.EXPECTED, "source_modified": False, "surface": "cursor-cli-interactive-terminal",
          "version": "2026.09.15-d2fe57e", "model_requested": probe.MODEL, "effort_requested": "xhigh",
          "prompt_submissions": 10, "observed_model_replies": 9, "native_admission_rejections": 1,
          "case_count": 10, "cases": cases, "startup_callbacks": startup,
          "total_case_callbacks": len(callbacks), "definition": probe.bind(RUN / "definitions/session.json"),
          "preparation": probe.bind(RUN / "preparation.json"), "submissions": [probe.bind(path) for path in submissions],
          "terminal": [probe.bind(path) for path in terminal_paths], "terminal_capture_limits": limits,
          "terminal_capture": "bounded-harness-chunks; redraw-frame-count-is-not-model-turn-count",
          "terminal_exit": probe.bind(RUN / "terminal-final-observation.json"), "terminal_exit_code": exit_record["response"]["exit_code"],
          "process_audit": probe.bind(RUN / "final-process-audit.json"), "cleanup": probe.bind(RUN / "cleanup.json"),
          "graceful_stop": probe.bind(RUN / "process-stop-graceful.json"), "force_stop": probe.bind(RUN / "process-stop-force.json"),
          "initial_stop_refusal": probe.bind(RUN / "process-stop-identity-refusal.json"),
          "identity_diagnostics": probe.bind(RUN / "process-identity-diagnostics.json"),
          "identity_refusal_cause": "PowerShell JSON date coercion caused a string comparison mismatch; exact UTC identity reverified before taskkill",
          "verification_attempt": probe.bind(RUN / "verification-attempt-01.json"),
          "submission_shape_reconciliation": "both recorded controller key variants accepted; original submissions unchanged",
          "historical_members_preserved": cleanup["historical_members_unchanged"],
          "global_cli_hash_unchanged": cleanup["global_cli_hash_before"] == cleanup["global_cli_hash_after"],
          "production_template_timing": "unqualified-by-this-instrumented-fault-observation",
          "unsupported_codec": "controller-selected-unknown-event; not-native-unsupported-tool-evidence",
          "fault_origin": "controller-injection-after-genuine-native-callback", "full_native_gate": "unchecked",
          "backend_attestation": "not-observed", "billing": "not-observed", "verifier": probe.bind(Path(__file__))}
probe.atomic_json(RUN / "native-prompt-stop-summary.json", record)
with REPORT.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": record["status"], "cases": len(cases), "observed_model_replies": 9,
                  "case_callbacks": len(callbacks), "historical_preserved": record["historical_members_preserved"]}))
