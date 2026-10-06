"""Verify the failed baseline evidence and its limits; do not regrade the frozen seven-case oracle."""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN=Path(__file__).resolve().parent
WORK=RUN.parents[2]
PROJECT=WORK / "plans/runs/nckh-native-261005-0128-r34-cursor-events-attempt-02/projects/main"
EVIDENCE=PROJECT / ".nckh-native-r37-cursor-posttool-controls-52"
read=lambda path:json.loads(path.read_text(encoding="utf-8-sig"))
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
bind=lambda path:{"path":path.relative_to(WORK).as_posix(),"sha256":sha(path)}
def bound(reference):
    path=WORK / reference["path"]
    assert sha(path) == reference["sha256"]
    return path
sealed=read(RUN / "failed-baseline-observation.json")
frozen=read(RUN / "frozen-brief.json")
metadata=read(RUN / "native-metadata.json")
stage=read(RUN / "stage.json")
audit=read(RUN / "process-final-audit.json")
cleanup=read(RUN / "cleanup.json")
assert sealed["status"] == "recorded-failed-first-posttool-baseline" and sealed["model_turns"] == sealed["native_Write_requests"] == 1
assert sealed["native_exit_code"] == 0 and sealed["monitor_exit_code"] == 1 and not sealed["original_oracle_regraded"]
assert len(frozen["cases"]) == 7 and len(list((RUN / "selected").glob("*.json"))) == 1
case=frozen["cases"][0]
selected=read(RUN / "selected" / (case["attempt"]+".json"))
runner_hash=next(row["sha256"] for row in stage["staged_members"] if row["path"].endswith("/hooks/runner.py"))
callbacks=[read(bound(ref)) for ref in sealed["callbacks"]]
policies=[read(bound(ref)) for ref in sealed["policy_receipts"]]
assert len(callbacks) == len(policies) == 4
assert {row["event"] for row in callbacks} == {"beforeSubmitPrompt","preToolUse","postToolUse","stop"}
assert len({row["native_session_hash"] for row in callbacks}) == 1
for row in callbacks:
    assert row["runner_sha256"] == runner_hash and row["control_sha256"] == selected["control_sha256"]
    assert row["reported_event"] == row["event"] and row["native_version"] == metadata["version"]
    assert row["workspace_contains_selected_project"] and row["callback_source"] == "project"
    assert row["fault_origin"] == "none" and row["status"] == "completed" and row["runner_exit_code"] == 0 and row["runner_exited"]
    assert row["observer_creation_filetime_ticks"]
pre=next(row for row in callbacks if row["event"] == "preToolUse")
post=next(row for row in callbacks if row["event"] == "postToolUse")
assert pre["native_tool_use_id"] == post["native_tool_use_id"] == sealed["native_tool_use_id"]
assert pre["marker_at_callback_start_sha256"] == case["before_sha256"]
actual=bound(sealed["actual_marker"]).read_bytes()
assert actual.hex() == sealed["actual_marker_hex"] and actual != bytes.fromhex(case["expected_hex"])
assert hashlib.sha256(actual).hexdigest() == post["marker_at_callback_start_sha256"]
assert actual.endswith(b"\r\r\n") and bytes.fromhex(case["expected_hex"]).endswith(b"\r\n")
assert post["runner_output"] == {"additional_context":"artifact-final-bytes-missing-or-stale"}
selected_receipts=[row for reference,row in zip(sealed["policy_receipts"],policies) if "/postToolUse/" in reference["path"]]
assert len(selected_receipts) == 1 and selected_receipts[0]["decision"] == "pending"
assert selected_receipts[0]["reason_codes"] == ["artifact-final-bytes-missing-or-stale"]
startup=sorted((EVIDENCE / "observations/startup").glob("*/*.json"))
startup_policies=sorted((EVIDENCE / "policy-receipts/startup").glob("*/*.json"))
assert len(startup) == len(startup_policies) == 1
assert read(startup[0])["event"] == "sessionStart" and read(startup[0])["status"] == "completed"
terminal_paths=sorted(RUN.glob("terminal-*.json"))
outputs=[read(path).get("output",read(path).get("result",{}).get("output","")) for path in terminal_paths]
cleaned=re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]","","\n".join(outputs))
assert re.search(r"(?:^|\n)  "+re.escape(case["marker"])+r"\r?\n",cleaned)
assert "Grok 4.7 500K Extra High" in read(RUN / "terminal-start.json")["output"] and "Run Everything" in read(RUN / "terminal-start.json")["output"]
assert read(RUN / "terminal-exit-poll-01.json")["exit_code"] == 0 and read(RUN / "monitor-exit.json")["exit_code"] == 1
assert audit["matching_count"] == audit["tracked_live_count"] == 0 and not audit["legacy_raw_union_used_as_ownership"]
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 33 and not cleanup["config_callable"]
historical=read(RUN / "historical-project-preimage.json")["members"]
assert cleanup["historical_members_unchanged"] == len(historical)
assert all(sha(PROJECT / relative) == expected for relative,expected in historical.items())
assert all(not (PROJECT / row["path"]).exists() for row in cleanup["removed_members"])
assert all(row["current_sha256"] == row["sha256"] for row in cleanup["protected_global_config"])
exit_check=read(RUN / "verified-process-exit-state-control.json")
assert exit_check["status"] == "verified-real-owned-process-exit-state-control" and exit_check["legacy_times_can_remain_queryable"]
assert exit_check["after_with_handle_retained"]["status"] == "terminated" and exit_check["actual_process_exit_code"] == 0
result={"status":"verified-failed-native52-baseline-observation","timestamp_utc":datetime.now(timezone.utc).isoformat(),
    "source_revision":37,"source_lock_hash":frozen["source_lock_hash"],"version":metadata["version"],
    "model_turns":1,"native_Write_requests":1,"callbacks":5,"policy_receipts":5,"dependent_cases_unstarted":6,
    "frozen_byte_oracle":"failed-preserved","actual_marker_tail_hex":"0d0d0a","expected_marker_tail_hex":"0d0a",
    "native_post_policy":"pending/artifact-final-bytes-missing-or-stale","native_post_wire":post["runner_output"],
    "marker_changed_before_post":True,"native_tool_use_id":pre["native_tool_use_id"],
    "native_input_content":"not-retained; field name content observed; normalizer origin unqualified",
    "normal_advisory_scope":"unqualified for this frozen CRLF request","prevention_or_rollback":"unqualified",
    "native_exit_code":0,"monitor_exit_code":1,"continuous_monitor_success":False,
    "monitor_failure_cause":"closing-race supported inference; creation times alone do not prove active process",
    "qualified_process_union":len(audit["tracked"]),"owned_processes_live":0,"preexisting_apps_preserved":27,
    "cleanup_removed":33,"historical_preserved":len(historical),"protected_global_configs_unchanged":True,
    "CLI_owned_state_hash_changed":cleanup["global_cli_hash_before"] != cleanup["global_cli_hash_after"],
    "global_direct_writes":False,"source_kit_modified":False,"full_native_gate":"unchecked","review":"inline",
    "sealed_case":bind(RUN / "failed-baseline-observation.json"),"cleanup":bind(RUN / "cleanup.json"),
    "process_audit":bind(RUN / "process-final-audit.json"),"exit_state_control":bind(RUN / "verified-process-exit-state-control.json"),
    "frozen_brief":bind(RUN / "frozen-brief.json"),"verifier":bind(Path(__file__)),
    "terminal":[bind(path) for path in terminal_paths],"terminal_truncated":any("truncated output" in value for value in outputs)}
with (RUN / "verified-baseline-failure-observation.json").open("x",encoding="utf8") as stream:
    stream.write(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"status":result["status"],"turns":1,"callbacks":5,"receipts":5,"unstarted":6,
    "qualified_union":len(audit["tracked"]),"owned_live":0,"frozen_oracle":"failed-preserved","monitor_exit":1}))
