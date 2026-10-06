"""Verify current Write post-tool observations against their frozen scope."""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = WORK / "plans/runs/nckh-native-261005-0128-r34-cursor-events-attempt-02/projects/main"
EVIDENCE = PROJECT / ".nckh-native-r37-cursor-posttool-controls-52"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path":path.relative_to(WORK).as_posix(),"sha256":sha(path)}
hash_bytes = lambda data: hashlib.sha256(data).hexdigest()

def bound(reference):
    path = WORK / reference["path"]
    assert sha(path) == reference["sha256"], "Bound evidence changed"
    return path

frozen = read(RUN / "frozen-brief.json")
metadata = read(RUN / "native-metadata.json")
stage = read(RUN / "stage.json")
definition = read(RUN / "definitions/session.json")
audit = read(RUN / "process-final-audit.json")
cleanup = read(RUN / "cleanup.json")
assert frozen["maximum_model_turns"] == len(frozen["cases"]) == 7 and frozen["model_retries"] == 0
assert read(RUN / "terminal-exit-poll-01.json")["exit_code"] == read(RUN / "monitor-exit.json")["exit_code"] == 0
monitor = read(RUN / "commands/native-cursor-posttool.process-tree.json")
assert monitor["status"] == "root-exited-or-reused" and not monitor["capture_errors"] and monitor["temporal_parent_identity"]
assert audit["matching_count"] == audit["tracked_live_count"] == 0 and not audit["legacy_raw_union_used_as_ownership"]
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 33 and not cleanup["config_callable"]
historical = read(RUN / "historical-project-preimage.json")["members"]
assert cleanup["historical_members_unchanged"] == len(historical)
assert all(sha(PROJECT / relative) == expected for relative,expected in historical.items())
assert all(not (PROJECT / row["path"]).exists() for row in cleanup["removed_members"])
assert all(row["current_sha256"] == row["sha256"] for row in cleanup["protected_global_config"])
assert read(RUN / "final-source-check.json")["source_lock_hash"] == frozen["source_lock_hash"]
for event, handlers in definition["config"]["hooks"].items():
    assert len(handlers) == 1 and handlers[0]["timeout"] == (20 if event == "preToolUse" else 5)
    if event in {"preToolUse","postToolUse"}:
        assert handlers[0]["matcher"] == "^Write$"
assert definition["config"]["hooks"]["preToolUse"][0]["failClosed"]
runner_hash = next(row["sha256"] for row in stage["staged_members"] if row["path"].endswith("/hooks/runner.py"))
terminals = sorted(RUN.glob("terminal-*.json"))
outputs = [read(path).get("output",read(path).get("result",{}).get("output","")) for path in terminals]
cleaned = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]","","\n".join(outputs))
cleaned = re.sub(r"\x1b\][^\x07]*\x07","",cleaned)
assert "Grok 4.7 500K Extra High" in read(RUN / "terminal-start.json")["output"] and "Run Everything" in read(RUN / "terminal-start.json")["output"]
startup = sorted((EVIDENCE / "observations/startup").glob("*/*.json"))
startup_receipts = sorted((EVIDENCE / "policy-receipts/startup").glob("*/*.json"))
assert len(startup) == len(startup_receipts) == 1 and read(startup[0])["event"] == "sessionStart"
callbacks_total, receipts_total = 1,1
ids, sessions, results = [],[],[]
for case in frozen["cases"]:
    record_path = RUN / "cases" / (case["attempt"]+".json")
    record = read(record_path)
    assert record["status"] == "recorded-current-Write-posttool-observation" and record["marker_exact"] and record["selected_observers_terminal"]
    selected = read(bound(record["selected"]))
    assert selected["prompt"] == case["prompt"] and selected["expected_hex"] == case["expected_hex"]
    prompt_path = RUN / ("terminal-"+str(case["index"]).zfill(2)+"-prompt-text.json")
    assert read(prompt_path)["prompt"] == case["prompt"]
    assert re.search(r"(?:^|\n)  "+re.escape(case["marker"])+r"\r?\n",cleaned), "Missing actual final marker"
    callbacks = [read(bound(reference)) for reference in record["callbacks"]]
    receipts = [read(bound(reference)) for reference in record["policy_receipts"]]
    assert len(callbacks) == 4 and {row["event"] for row in callbacks} == {"beforeSubmitPrompt","preToolUse","postToolUse","stop"}
    assert len({row["native_session_hash"] for row in callbacks}) == 1
    pre = next(row for row in callbacks if row["event"] == "preToolUse")
    post = next(row for row in callbacks if row["event"] == "postToolUse")
    assert pre["native_tool_use_id"] == post["native_tool_use_id"] and pre["native_tool_use_id"]
    assert pre["marker_at_callback_start_sha256"] == case["before_sha256"]
    assert post["marker_exists_at_callback_start"] and post["marker_at_callback_start_sha256"] == case["expected_sha256"]
    assert (bound(record["marker_after"])).read_bytes() == bytes.fromhex(case["expected_hex"])
    selected_receipts = [row for ref,row in zip(record["policy_receipts"],receipts) if "/postToolUse/" in ref["path"]]
    for row in callbacks:
        assert row["runner_sha256"] == runner_hash and row["control_sha256"] == selected["control_sha256"]
        assert row["reported_event"] == row["event"] and row["native_version"] == metadata["version"] and row["callback_source"] == "project"
        assert row["workspace_contains_selected_project"] and row["observer_creation_filetime_ticks"]
        assert row["native_model"] == ("grok-4.7" if row["event"] in {"preToolUse","postToolUse"} else "grok-4.7-xhigh")
        assert row["native_model_id"] is None and row["native_model_params"] is None
        assert row["fault_origin"] == ("controller-injection-after-genuine-callback" if row["event"] == "postToolUse" and case["mode"] not in {"allow","policy-deny"} else "none")
        if row["event"] != "postToolUse":
            assert row["status"] == "completed" and row["runner_exit_code"] == 0 and row["runner_exited"]
    for row in (pre,post):
        assert row["native_tool_name"] == "Write"
        assert (PROJECT / row["native_path_fields"]["file_path"]).resolve() == (PROJECT / case["relative"]).resolve()
    mode = case["mode"]
    if mode in {"malformed-output","crash"}:
        assert not selected_receipts
        assert post["status"] == ("intentional-test-malformed-output" if mode == "malformed-output" else "intentional-test-crash-exit-17")
    elif mode == "timeout":
        assert post["status"] in {"completed","intentional-test-sleep-eight-seconds"}
        assert len(selected_receipts) <= 1
        if selected_receipts:
            assert post["status"] == "completed" and post["runner_exited"] and post["runner_exit_code"] == 0
            assert selected_receipts[0]["decision"] == "advisory" and selected_receipts[0]["reason_codes"] == ["delivery-bindings-current-review-separate"]
    else:
        assert len(selected_receipts) == 1
        expected = {"allow":("advisory","delivery-bindings-current-review-separate"),
                    "policy-deny":("block","bounded-input-exceeded"),
                    "malformed-input":("block","hook-input-or-context-invalid"),
                    "unsupported-codec":("block","hook-input-or-context-invalid")}[mode]
        assert selected_receipts[0]["decision"] == expected[0] and selected_receipts[0]["reason_codes"] == [expected[1]]
        if mode in {"malformed-input","unsupported-codec"}:
            assert selected_receipts[0]["status"] == "degraded-failed"
            assert selected_receipts[0]["event_hash"] == (hash_bytes(b"{") if mode == "malformed-input" else post["input_sha256"])
    ids.append(pre["native_tool_use_id"])
    sessions.append(pre["native_session_hash"])
    callbacks_total += len(callbacks)
    receipts_total += len(receipts)
    results.append({"mode":mode,"case":bind(record_path),"marker_before_post":True,"marker_exact":True,
        "native_tool_use_id":pre["native_tool_use_id"],"post_status":post["status"],"wire":post.get("runner_output"),
        "selected_policy":selected_receipts[0]["decision"] if selected_receipts else None,
        "selected_policy_receipts":len(selected_receipts),"prevention_or_rollback":"unqualified",
        "late_post_receipt":mode == "timeout" and bool(selected_receipts)})
assert len(set(ids)) == 7 and len(set(sessions)) == 1 and callbacks_total == 29
result = {"status":"verified-seven-current-native-Write-posttool-observations","timestamp_utc":datetime.now(timezone.utc).isoformat(),
    "source_revision":37,"source_lock_hash":frozen["source_lock_hash"],"surface":frozen["surface"],"version":metadata["version"],
    "model_turns":7,"requested_native_Writes":7,"native_Write_ids":ids,"callback_count":callbacks_total,"policy_receipt_count":receipts_total,
    "model_selection":"existing Grok4.7/500k/xhigh/fastfalse and native startup display","backend_parameters_attestation":"not-observed",
    "results":results,"all_markers_before_selected_post":True,"prevention_or_rollback":"unqualified",
    "unsupported_event_scope":"injected codec selector only; genuine unknown-host-event remains unqualified","scientific_QA":"unverified",
    "native_exit_code":0,"monitor_exit_code":0,"temporal_process_capture":True,"qualified_process_union":len(audit["tracked"]),
    "owned_processes_live":0,"preexisting_apps_preserved":27,"legacy_raw_union_used_as_ownership":False,
    "cleanup":bind(RUN / "cleanup.json"),"process_audit":bind(RUN / "process-final-audit.json"),"historical_preserved":len(historical),
    "protected_global_configs_unchanged":True,"CLI_owned_state_hash_changed":cleanup["global_cli_hash_before"] != cleanup["global_cli_hash_after"],
    "global_direct_writes":False,"source_kit_modified":False,"full_native_gate":"unchecked","review":"inline; no independent reviewer",
    "frozen_brief":bind(RUN / "frozen-brief.json"),"source_check":bind(RUN / "final-source-check.json"),"verifier":bind(Path(__file__)),
    "terminal":[bind(path) for path in terminals],"terminal_truncated":any("truncated output" in value for value in outputs)}
with (RUN / "verified-posttool-observations.json").open("x",encoding="utf8") as stream:
    stream.write(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"status":result["status"],"turns":7,"Writes":7,"callbacks":callbacks_total,"receipts":receipts_total,
    "qualified_process_union":len(audit["tracked"]),"live":0,"monitor_exit":0}))
