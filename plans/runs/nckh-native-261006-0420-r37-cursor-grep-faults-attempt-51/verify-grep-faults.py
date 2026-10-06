"""Verify genuine Grep failures and keep declared fault/late receipt provenance."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = WORK / "plans/runs/nckh-native-261005-0128-r34-cursor-events-attempt-02/projects/main"
EVIDENCE = PROJECT / ".nckh-native-r37-cursor-grep-faults-51"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
hash_bytes = lambda value: hashlib.sha256(value).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}


def bound(reference):
    path = WORK / reference["path"]
    assert sha(path) == reference["sha256"], "Bound evidence changed"
    return path


frozen = read(RUN / "frozen-brief.json")
stage = read(RUN / "stage.json")
metadata = read(RUN / "native-metadata.json")
definition = read(RUN / "definitions/session.json")
cleanup = read(RUN / "cleanup.json")
audit = read(RUN / "process-final-audit.json")
assert len(frozen["cases"]) == 5 and frozen["model_retries"] == 0
assert read(RUN / "terminal-exit-poll-01.json")["exit_code"] == read(RUN / "monitor-exit.json")["exit_code"] == 0
assert audit["matching_count"] == audit["tracked_live_count"] == 0 and audit["previous_union_count"] == 2592
assert read(RUN / "commands/native-cursor-grep-faults.process-tree.json")["status"] == "root-exited-or-reused"
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 27 and not cleanup["config_callable"]
historical = read(RUN / "historical-project-preimage.json")["members"]
assert cleanup["historical_members_unchanged"] == len(historical)
assert all(sha(PROJECT / relative) == expected for relative, expected in historical.items())
assert all(not (PROJECT / member["path"]).exists() for member in cleanup["removed_members"])
assert all(row["current_sha256"] == row["sha256"] for row in cleanup["protected_global_config"])
expected_bytes = bytes.fromhex(frozen["fixture_bytes_hex"])
assert (RUN / "fixture-before.txt").read_bytes() == (RUN / "fixture-after.txt").read_bytes() == expected_bytes
assert hash_bytes(expected_bytes) == frozen["fixture_sha256"]
runner_hash = next(row["sha256"] for row in stage["staged_members"] if row["path"].endswith("/hooks/runner.py"))
assert frozen["context_sha256"] == sha(EVIDENCE / "context-allow.json")
assert "Grep" not in read(EVIDENCE / "context-allow.json")["tool_operations"]
for event, handlers in definition["config"]["hooks"].items():
    assert len(handlers) == 1 and handlers[0]["timeout"] == (20 if event == "preToolUse" else 10 if event == "postToolUseFailure" else 5)
assert definition["config"]["hooks"]["preToolUse"][0]["failClosed"]
assert definition["config"]["hooks"]["postToolUseFailure"][0]["matcher"] == "^Grep$"
terminal_paths = sorted(RUN.glob("terminal-*.json"))
terminal_outputs = [read(path).get("output", read(path).get("result", {}).get("output", "")) for path in terminal_paths]
cleaned = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", "\n".join(terminal_outputs))
cleaned = re.sub(r"\x1b\][^\x07]*\x07", "", cleaned)
assert "Grok 4.7 500K Extra High" in read(RUN / "terminal-start.json")["output"]
assert "Run Everything" in read(RUN / "terminal-start.json")["output"]
startup_paths = sorted((EVIDENCE / "observations/startup").glob("*/*.json"))
startup_receipts = sorted((EVIDENCE / "policy-receipts/startup").glob("*/*.json"))
assert len(startup_paths) == len(startup_receipts) == 1
assert read(startup_paths[0])["event"] == "sessionStart" and read(startup_paths[0])["fault_origin"] == "none"
all_ids = []
all_sessions = []
verified = []
callback_count = 1
receipt_count = 1
for case in frozen["cases"]:
    path = RUN / "cases" / (case["attempt"] + ".json")
    record = read(path)
    assert record["status"] == "recorded-matching-native-Grep-failure" and record["selected_observer_terminal"] and record["fixture_unchanged"]
    selected = read(bound(record["selected"]))
    assert selected["context_sha256"] == frozen["context_sha256"] and selected["prompt"] == case["prompt"]
    prefix = "terminal-" + str(case["index"]).zfill(2)
    assert read(RUN / (prefix + "-prompt-text.json"))["prompt"] == case["prompt"]
    assert re.search(r"(?:^|\n)  " + re.escape(case["marker"]) + r"\r?\n", cleaned), "Missing actual isolated final marker"
    callbacks = [read(bound(reference)) for reference in record["callbacks"]]
    receipts = [read(bound(reference)) for reference in record["policy_receipts"]]
    failure = read(bound(record["native_failure"]))
    assert len(callbacks) == 3 and {row["event"] for row in callbacks} == {"beforeSubmitPrompt", "preToolUse", "stop"}
    assert len({row["native_session_hash"] for row in callbacks}) == 1
    pre = next(row for row in callbacks if row["event"] == "preToolUse")
    for row in callbacks:
        assert row["runner_sha256"] == runner_hash and row["control_sha256"] == selected["control_sha256"]
        assert row["reported_event"] == row["event"] and row["native_version"] == metadata["version"]
        assert row["workspace_contains_selected_project"] and row["callback_source"] == "project"
        assert row["native_model"] == ("grok-4.7" if row["event"] == "preToolUse" else "grok-4.7-xhigh")
        assert row["native_model_id"] is None and row["native_model_params"] is None
        assert row["fault_origin"] == ("controller-injection-after-genuine-callback" if row["event"] == "preToolUse" else "none")
        if row["event"] != "preToolUse":
            assert row["status"] == "completed" and row["runner_exit_code"] == 0 and row["runner_exited"]
    assert pre["native_tool_name"] == "Grep" and pre["native_tool_use_id"] and pre["mode"] == case["mode"]
    assert set(pre["native_path_fields"]) == {"file_path"}
    assert (PROJECT / pre["native_path_fields"]["file_path"]).resolve() == (PROJECT / frozen["selected_directory"]).resolve()
    assert pre["native_search_scope_fields"]["pattern"] == "NCKH_SYNTHETIC_PUBLIC_GREP_FAULT_MARKER"
    assert failure["reported_event"] == "postToolUseFailure" and failure["native_tool_name"] == "Grep"
    assert failure["native_tool_use_id"] == pre["native_tool_use_id"] and failure["native_session_hash"] == pre["native_session_hash"]
    assert failure["native_version"] == metadata["version"] and failure["failure_type"] == "permission_denied"
    assert failure["selected_path_matches"] and failure["workspace_contains_selected_project"]
    assert not failure["policy_invoked"] and not failure["full_transcript_read"] and failure["fault_origin"] == "none"
    assert failure["is_interrupt"] is False
    selected_receipts = [row for reference, row in zip(record["policy_receipts"], receipts) if "/preToolUse/" in reference["path"]]
    mode = case["mode"]
    if mode in {"malformed-output", "crash"}:
        assert not selected_receipts and pre["status"] == ("intentional-test-malformed-output" if mode == "malformed-output" else "intentional-test-crash-exit-17")
    elif mode == "timeout":
        assert pre["status"] in {"completed", "intentional-test-sleep-twenty-four-seconds"}
        assert len(selected_receipts) <= 1
        if selected_receipts:
            assert pre["status"] == "completed" and pre["runner_exit_code"] == 0 and pre["runner_output"] == {}
            assert selected_receipts[0]["decision"] == "manual" and selected_receipts[0]["reason_codes"] == ["tool-route-uncovered"]
            assert selected_receipts[0]["context_hash"] == frozen["context_sha256"]
    else:
        assert len(selected_receipts) == 1 and selected_receipts[0]["decision"] == "block"
        assert selected_receipts[0]["reason_codes"] == ["hook-input-or-context-invalid"] and selected_receipts[0]["status"] == "degraded-failed"
        assert selected_receipts[0]["event_hash"] == (hash_bytes(b"{") if mode == "malformed-input" else pre["input_sha256"])
        assert pre["runner_exit_code"] == (0 if mode == "malformed-input" else 3) and pre["runner_exited"]
    for row in receipts:
        if row.get("phase") != "preflight" and row.get("status") != "degraded-failed":
            assert row["context_hash"] == frozen["context_sha256"]
    all_ids.append(pre["native_tool_use_id"])
    all_sessions.append(pre["native_session_hash"])
    callback_count += len(callbacks) + 1
    receipt_count += len(receipts)
    verified.append({"attempt": case["attempt"], "mode": mode, "native_response": "permission_denied",
        "native_tool_use_id": pre["native_tool_use_id"], "scrubbed_native_error": failure["scrubbed_selected_error"],
        "selected_observer_status": pre["status"], "selected_wire": pre.get("runner_output"),
        "selected_policy_receipts": len(selected_receipts), "selected_policy_decision": selected_receipts[0]["decision"] if selected_receipts else None,
        "fixture_unchanged": True, "successful_post_callbacks": 0, "case": bind(path), "fault_origin": pre["fault_origin"],
        "late_receipt_does_not_override_native_failure": mode == "timeout" and bool(selected_receipts)})
assert len(set(all_ids)) == 5 and len(set(all_sessions)) == 1 and callback_count == 21
result = {"status": "verified-five-current-native-directory-Grep-preflight-fault-observations", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "source_revision": 37, "source_lock_hash": frozen["source_lock_hash"], "surface": "cursor-cli-interactive", "version": metadata["version"],
    "model_selection": "existing Grok4.7/500k/xhigh/fastfalse config and native startup display", "backend_parameters_attestation": "not-observed",
    "model_turns": 5, "prompt_submissions": 5, "actual_native_tool_requests": 5, "native_Grep_ids": all_ids,
    "callback_count": callback_count, "policy_receipt_count": receipt_count, "results": verified,
    "normal_route_scope": "context operation map has no Grep; normal public directory route manual, as separately observed49",
    "fault_scope": "five controller faults after genuine native preToolUse/Grep callbacks; native failure logger not injected",
    "unsupported_event_scope": "codec selector injection only; genuine unknown-host-event remains unqualified",
    "preToolUse_timeout_seconds": 20, "injected_sleep_seconds": 24, "inner_runner_timeout_seconds": 5,
    "other_handler_timeout_seconds": 5, "native_failure_diagnostic_timeout_seconds": 10,
    "fixture_unchanged": True, "successful_post_callbacks": 0, "raw_native_tool_return_content": "not-retained; bounded failure metadata observed",
    "terminal": [bind(path) for path in terminal_paths], "terminal_truncated": any("truncated output" in value for value in terminal_outputs),
    "startup_callback": bind(startup_paths[0]), "startup_receipt": bind(startup_receipts[0]),
    "native_exit_code": 0, "monitor_exit_code": 0, "cleanup": bind(RUN / "cleanup.json"), "process_audit": bind(RUN / "process-final-audit.json"),
    "process_union_identities": len(audit["tracked"]), "processes_live": 0, "process_stop_performed": False,
    "historical_members_preserved": len(historical), "removed_members": 27, "protected_global_configs_unchanged": True,
    "CLI_owned_state_hash_changed": cleanup["global_cli_hash_before"] != cleanup["global_cli_hash_after"], "CLI_changed_fields": "not-inferred",
    "global_direct_writes": False, "source_kit_modified": False, "scientific_QA": "unverified", "full_native_gate": "unchecked",
    "review": "inline; no independent reviewer", "frozen_brief": bind(RUN / "frozen-brief.json"), "verifier": bind(Path(__file__))}
with (RUN / "verified-grep-faults.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": result["status"], "turns": 5, "Grep": 5, "callbacks": callback_count, "receipts": receipt_count,
    "native_failure_type": "permission_denied", "process_union": len(audit["tracked"]), "live": 0}))
