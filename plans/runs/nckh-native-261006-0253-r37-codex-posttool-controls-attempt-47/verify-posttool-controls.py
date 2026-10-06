"""Verify actual patch/callback/byte evidence and retain the limits of post-tool checks."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = WORK / "plans/runs/nckh-native-261005-0658-r34-codex-file-attempt-01/project-02"
EVIDENCE = PROJECT / ".nckh-native-codex-posttool-controls-47"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
hash_bytes = lambda value: hashlib.sha256(value).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}

def bound(reference):
    path = WORK / reference["path"]
    assert sha(path) == reference["sha256"], "Bound file changed"
    return path

frozen = read(RUN / "frozen-brief.json")
summary = read(RUN / "native-posttool-summary.json")
definition = read(RUN / "definition.json")
cleanup = read(RUN / "cleanup.json")
audit = read(RUN / "process-final-audit.json")
assert read(RUN / "controller-poll-02.json")["exit_code"] == 0
assert summary["status"] == "recorded-seven-current-native-posttool-cases"
assert len(summary["results"]) == 7 and [row["mode"] for row in summary["results"]] == frozen["modes"]
assert audit["matching_count"] == audit["tracked_live_count"] == 0
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 26
assert cleanup["global_config_unchanged"] and cleanup["global_hook_unchanged"] and cleanup["new_project_trust_keys"] == 0
assert not cleanup["config_callable"]
for member in cleanup["removed_members"]:
    assert not (PROJECT / member["path"]).exists()
history = read(RUN / "historical-project-preimage.json")["members"]
assert len(history) == cleanup["historical_project_members_unchanged"] == 538
assert all(sha(PROJECT / relative) == expected for relative, expected in history.items())
runner_hash = next(row["sha256"] for row in definition["staged_members"] if row["path"].endswith("/hooks/runner.py"))
for groups in definition["hooks"].values():
    assert len(groups) == len(groups[0]["hooks"]) == 1 and groups[0]["hooks"][0]["timeout"] == 5
expected_marker = bytes.fromhex(frozen["expected_marker_hex"])
expected_hash = hash_bytes(expected_marker)
last_context = (EVIDENCE / "context-allow.json").read_bytes()
last_relative = read(EVIDENCE / "context-allow.json")["artifact"]["path"]
deny_hash = sha(EVIDENCE / "context-deny.json")
assert len(read(EVIDENCE / "context-deny.json")["references"]) == 33
verified = []
callback_count = receipt_count = 0
for result in summary["results"]:
    final = read(bound(result["final_snapshot"]))
    native_snapshot = read(bound(final["native_exit_snapshot"]))
    assert native_snapshot["process_exited"] and native_snapshot["exit_code"] == 0 and native_snapshot["invalid_stdout_lines"] == 0
    command = read(bound(native_snapshot["command_receipt"]))
    assert command["exit_code"] == 0 and command["process_exited"] and command["timeout_seconds"] is None
    assert not command["capture_errors"] and not command["owned_handle_stop_performed"]
    assert 'model_reasoning_effort="medium"' in command["command"] and '--dangerously-bypass-hook-trust' in command["command"]
    assert '--dangerously-bypass-approvals-and-sandbox' in command["command"]
    callbacks = [read(bound(reference)) for reference in final["final_callbacks"]]
    receipts = [read(bound(reference)) for reference in final["final_policy_receipts"]]
    assert len(callbacks) == 5 and {row["event"] for row in callbacks} == {"SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop"}
    assert all(row["reported_event"] == row["event"] and row["native_model"] == "gpt-5.6-luna" and row["runner_sha256"] == runner_hash for row in callbacks)
    pre = next(row for row in callbacks if row["event"] == "PreToolUse")
    post = next(row for row in callbacks if row["event"] == "PostToolUse")
    assert pre["native_tool_name"] == post["native_tool_name"] == "apply_patch"
    assert pre["native_command_sha256"] == post["native_command_sha256"] == native_snapshot["requested_patch_sha256"]
    assert pre["native_tool_use_id"] == post["native_tool_use_id"] and isinstance(pre["native_tool_use_id"], str)
    assert pre["native_turn_id"] == post["native_turn_id"] and pre["native_session_hash"] == post["native_session_hash"]
    assert pre["marker_exists_at_callback_start"] is False and post["marker_exists_at_callback_start"] is True
    assert post["marker_at_callback_start_sha256"] == post["controller_expected_marker_sha256"] == expected_hash
    marker = PROJECT / final["marker_relative"]
    assert marker.read_bytes() == expected_marker and final["marker_exact"]
    frames = native_snapshot["native_frames"]
    assert sum(frame.get("type") == "turn.started" for frame in frames) == sum(frame.get("type") == "turn.completed" for frame in frames) == 1
    assert any(frame.get("item", {}).get("type") == "agent_message" and frame["item"].get("text") == "ORACLE_ATTEMPT_FINISHED" for frame in frames)
    changes = [frame["item"] for frame in frames if frame.get("type") == "item.completed" and frame.get("item", {}).get("type") == "file_change"]
    assert len(changes) == 1 and changes[0]["status"] == "completed" and len(changes[0]["changes"]) == 1
    assert changes[0]["changes"][0]["kind"] == "add" and Path(changes[0]["changes"][0]["path"]).resolve() == marker.resolve()
    pre_receipts = [row for row in receipts if row.get("phase") == "preflight"]
    assert len(pre_receipts) == 1 and pre_receipts[0]["decision"] == "allow"
    selected_receipts = [(reference, row) for reference, row in zip(final["final_policy_receipts"], receipts)
        if "/PostToolUse/" in reference["path"]]
    mode = result["mode"]
    policy = None
    if mode in {"malformed-output", "timeout", "crash"}:
        assert len(selected_receipts) == 0
        expected_status = {"malformed-output": "intentional-test-malformed-output", "timeout": "intentional-test-sleep-eight-seconds", "crash": "intentional-test-crash-exit-17"}[mode]
        assert post["status"] == expected_status
    else:
        assert len(selected_receipts) == 1 and post["status"] == "completed" and post["runner_exited"]
        policy = selected_receipts[0][1]
        expected_reason = {"allow": "delivery-bindings-current-review-separate", "policy-deny": "bounded-input-exceeded",
            "malformed-input": "hook-input-or-context-invalid", "unsupported-codec": "hook-input-or-context-invalid"}[mode]
        assert policy["reason_codes"] == [expected_reason]
        assert policy["decision"] == ("advisory" if mode == "allow" else "block")
        if mode in {"allow", "policy-deny", "malformed-input"}:
            assert post["runner_exit_code"] == 0 and post["runner_output"] == {"hookSpecificOutput": {
                "hookEventName": "PostToolUse", "additionalContext": expected_reason}}
        else:
            assert post["runner_exit_code"] == 3 and post["runner_output"] == {}
        if mode == "allow":
            old_token = json.dumps(last_relative).encode()
            new_token = json.dumps(final["marker_relative"]).encode()
            assert last_context.count(old_token) == 1
            derived = last_context.replace(old_token, new_token)
            assert hash_bytes(derived) == policy["context_hash"]
            assert policy["artifact_sha256"] == expected_hash
        if mode == "policy-deny":
            assert policy["context_hash"] == deny_hash
        if mode == "malformed-input":
            assert policy["status"] == "degraded-failed" and policy["event_hash"] == hash_bytes(b"{")
        if mode == "unsupported-codec":
            assert policy["status"] == "degraded-failed" and policy["event_hash"] == post["input_sha256"]
    callback_count += len(callbacks)
    receipt_count += len(receipts)
    verified.append({
        "attempt": result["attempt"], "mode": mode, "native_patch_completed": True, "marker_exact": True,
        "marker_present_before_selected_callback": True, "native_tool_use_id": pre["native_tool_use_id"],
        "selected_callback_status": post["status"], "selected_policy_receipts": len(selected_receipts),
        "selected_decision": policy["decision"] if policy else None, "selected_reason_codes": policy["reason_codes"] if policy else [],
        "selected_wire": post.get("runner_output"), "fault_origin": post["fault_origin"],
        "final_snapshot": result["final_snapshot"], "post_callback": next(reference for reference in final["final_callbacks"] if read(WORK / reference["path"])["event"] == "PostToolUse"),
    })
assert callback_count == 35 and receipt_count == 32
record = {
    "status": "verified-current-Codex-posttool-patch-controls-and-fault-observations", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "source_revision": 37, "source_lock_hash": frozen["source_lock_hash"], "version": "0.154.0", "surface": "codex-cli-exec",
    "model_requested": "gpt-5.6-luna", "effort_requested": "medium", "backend_model_effort_attestation": "not-observed",
    "native_callback_model": "gpt-5.6-luna", "model_turns": 7, "actual_native_patches": 7, "callbacks": callback_count,
    "policy_receipts": receipt_count, "results": verified, "marker_bytes_hex": expected_marker.hex(),
    "posttool_prevention_or_rollback": "not-established; exact mutation already present at every selected callback entry",
    "native_hook_notification_states": "not-exposed-by-retained-exec-JSON; native completed file_change/turn items observed",
    "timeout_observation": "configured outer5s/sleeper8s; final selected observer remains sleep record, no selected receipt; no live owned descendants",
    "context_hash_verification": "normal expected context derived from retained last-case bytes and frozen single artifact.path change; deny context observed directly",
    "scientific_QA": "unverified; synthetic prospective marker binding is not scientific evidence",
    "unsupported_event_scope": "selected codec injection after genuine PostToolUse callback; unknown-host-event delivery unqualified",
    "frozen_brief": bind(RUN / "frozen-brief.json"), "summary": bind(RUN / "native-posttool-summary.json"),
    "cleanup": bind(RUN / "cleanup.json"), "process_audit": bind(RUN / "process-final-audit.json"),
    "process_union_identities": len(audit["tracked"]), "processes_live": 0, "process_stop_performed": False,
    "historical_files_preserved": len(history), "global_direct_writes": False, "new_project_trust_keys": 0,
    "global_config_and_hook_hashes_unchanged": True, "full_native_gate": "unchecked", "review": "inline; no independent reviewer",
    "verifier": bind(Path(__file__)),
}
with (RUN / "verified-posttool-observations.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": record["status"], "turns": 7, "patches": 7, "callbacks": callback_count, "receipts": receipt_count,
    "cleanup_members": 26, "historical_preserved": len(history), "process_union": len(audit["tracked"]), "live": 0}))
