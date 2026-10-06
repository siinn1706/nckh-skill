"""Verify retained native Stop observations without inventing hook notification states."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = WORK / "plans/runs/nckh-native-261005-0658-r34-codex-file-attempt-01/project-02"
EVIDENCE = PROJECT / ".nckh-native-codex-stop-controls-48"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
hash_bytes = lambda data: hashlib.sha256(data).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}


def bound(reference):
    path = WORK / reference["path"]
    assert sha(path) == reference["sha256"], "Bound evidence changed"
    return path


frozen = read(RUN / "frozen-brief.json")
summary = read(RUN / "native-stop-summary.json")
definition = read(RUN / "definition.json")
cleanup = read(RUN / "cleanup.json")
audit = read(RUN / "process-final-audit.json")
controller = read(RUN / "controller-terminal.json")
assert controller["exit_code"] == 0 and controller["session_id"] == 42269
assert summary["status"] == "recorded-seven-current-native-stop-cases"
assert len(summary["results"]) == 7 and [row["mode"] for row in summary["results"]] == frozen["modes"]
assert audit["matching_count"] == audit["tracked_live_count"] == 0 and audit["previous_union_count"] == 2164
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 26
assert cleanup["global_config_unchanged"] and cleanup["global_hook_unchanged"] and cleanup["new_project_trust_keys"] == 0
assert not cleanup["config_callable"]
for member in cleanup["removed_members"]:
    assert not (PROJECT / member["path"]).exists()
historical = read(RUN / "historical-project-preimage.json")["members"]
assert len(historical) == cleanup["historical_project_members_unchanged"]
assert all(sha(PROJECT / relative) == expected for relative, expected in historical.items())
runner_hash = next(row["sha256"] for row in definition["staged_members"] if row["path"].endswith("/hooks/runner.py"))
assert set(definition["hooks"]) == {"SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop"}
for groups in definition["hooks"].values():
    assert len(groups) == len(groups[0]["hooks"]) == 1 and groups[0]["hooks"][0]["timeout"] == 5
marker_bytes = bytes.fromhex(frozen["marker_bytes_hex"])
marker_hash = hash_bytes(marker_bytes)
deny_hash = sha(EVIDENCE / "context-deny.json")
assert len(read(EVIDENCE / "context-deny.json")["references"]) == 33
verified = []
callbacks_total = receipts_total = 0
for result in summary["results"]:
    final = read(bound(result["final_snapshot"]))
    snapshot = read(bound(final["native_exit_snapshot"]))
    context_path = bound(final["context_preimage"])
    assert snapshot["process_exited"] and snapshot["exit_code"] == 0 and snapshot["invalid_stdout_lines"] == 0
    command = read(bound(snapshot["command_receipt"]))
    assert command["exit_code"] == 0 and command["process_exited"] and command["timeout_seconds"] is None
    assert not command["capture_errors"] and not command["owned_handle_stop_performed"]
    assert 'model_reasoning_effort="medium"' in command["command"] and '--dangerously-bypass-hook-trust' in command["command"]
    assert '--dangerously-bypass-approvals-and-sandbox' in command["command"]
    callbacks = [read(bound(reference)) for reference in final["final_callbacks"]]
    receipts = [read(bound(reference)) for reference in final["final_policy_receipts"]]
    assert len(callbacks) == 5 and {row["event"] for row in callbacks} == set(definition["hooks"])
    assert all(row["reported_event"] == row["event"] and row["native_model"] == "gpt-5.6-luna" and row["runner_sha256"] == runner_hash for row in callbacks)
    pre = next(row for row in callbacks if row["event"] == "PreToolUse")
    post = next(row for row in callbacks if row["event"] == "PostToolUse")
    stop = next(row for row in callbacks if row["event"] == "Stop")
    assert pre["native_tool_name"] == post["native_tool_name"] == "apply_patch"
    assert pre["native_command_sha256"] == post["native_command_sha256"] == snapshot["requested_patch_sha256"]
    assert pre["native_tool_use_id"] == post["native_tool_use_id"] and isinstance(pre["native_tool_use_id"], str)
    assert pre["native_turn_id"] == post["native_turn_id"] == stop["native_turn_id"]
    assert pre["native_session_hash"] == post["native_session_hash"] == stop["native_session_hash"]
    assert not pre["marker_exists_at_callback_start"] and post["marker_exists_at_callback_start"] and stop["marker_exists_at_callback_start"]
    assert post["marker_at_callback_start_sha256"] == stop["marker_at_callback_start_sha256"] == marker_hash
    assert stop["native_stop_hook_active"] is False and stop["selected"]
    assert stop["native_last_assistant_message_type"] == "str" and stop["native_last_assistant_message_bytes"] <= 65536
    assert "last_assistant_message" in stop["input_fields"] and "stop_hook_active" in stop["input_fields"]
    marker = PROJECT / final["marker_relative"]
    assert marker.read_bytes() == marker_bytes and final["marker_exact"]
    frames = snapshot["native_frames"]
    assert sum(frame.get("type") == "turn.started" for frame in frames) == sum(frame.get("type") == "turn.completed" for frame in frames) == 1
    messages = [frame["item"] for frame in frames if frame.get("type") == "item.completed" and frame.get("item", {}).get("type") == "agent_message"]
    assert len(messages) == 1 and hash_bytes(messages[0]["text"].encode()) == frozen["final_message_sha256"]
    changes = [frame["item"] for frame in frames if frame.get("type") == "item.completed" and frame.get("item", {}).get("type") == "file_change"]
    assert len(changes) == 1 and changes[0]["status"] == "completed" and len(changes[0]["changes"]) == 1
    assert changes[0]["changes"][0]["kind"] == "add" and Path(changes[0]["changes"][0]["path"]).resolve() == marker.resolve()
    pre_receipts = [row for row in receipts if row.get("phase") == "preflight"]
    assert len(pre_receipts) == 1 and pre_receipts[0]["decision"] == "allow"
    selected_receipts = [(reference, row) for reference, row in zip(final["final_policy_receipts"], receipts) if "/Stop/" in reference["path"]]
    mode = result["mode"]
    policy = None
    if mode in {"malformed-output", "timeout", "crash"}:
        assert not selected_receipts
        assert stop["status"] == {"malformed-output": "intentional-test-malformed-output", "timeout": "intentional-test-sleep-eight-seconds",
            "crash": "intentional-test-crash-exit-17"}[mode]
    else:
        assert len(selected_receipts) == 1 and stop["status"] == "completed" and stop["runner_exited"]
        policy = selected_receipts[0][1]
        reason = {"allow": "writing-resource-advice-only", "policy-deny": "bounded-input-exceeded",
            "malformed-input": "hook-input-or-context-invalid", "unsupported-codec": "hook-input-or-context-invalid"}[mode]
        assert policy["reason_codes"] == [reason] and policy["decision"] == ("advisory" if mode == "allow" else "block")
        assert stop["runner_output"] == {} and stop["runner_exit_code"] == (3 if mode == "unsupported-codec" else 0)
        if mode == "allow":
            assert policy["context_hash"] == sha(context_path) and policy["artifact_sha256"] == marker_hash
        if mode == "policy-deny":
            assert policy["context_hash"] == deny_hash
        if mode in {"malformed-input", "unsupported-codec"}:
            assert policy["status"] == "degraded-failed" and policy["event_hash"] == (hash_bytes(b"{") if mode == "malformed-input" else stop["input_sha256"])
    verified.append({"attempt": result["attempt"], "mode": mode, "native_patch_completed": True, "marker_exact": True,
        "marker_present_at_Stop_entry": True, "stop_hook_active": stop["native_stop_hook_active"],
        "last_assistant_message_bytes": stop["native_last_assistant_message_bytes"],
        "last_assistant_message_sha256": stop["native_last_assistant_message_sha256"],
        "native_message_matches_final_frame": stop["native_last_assistant_message_sha256"] == frozen["final_message_sha256"],
        "selected_callback_status": stop["status"], "selected_policy_receipts": len(selected_receipts),
        "selected_decision": policy["decision"] if policy else None, "selected_reason_codes": policy["reason_codes"] if policy else [],
        "selected_wire": stop.get("runner_output"), "fault_origin": stop["fault_origin"], "final_snapshot": result["final_snapshot"],
        "Stop_callback": next(reference for reference in final["final_callbacks"] if read(WORK / reference["path"])["event"] == "Stop")})
    callbacks_total += len(callbacks)
    receipts_total += len(receipts)
assert callbacks_total == 35 and receipts_total == 32
record = {"status": "verified-current-Codex-stop-patch-controls-and-fault-observations", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "source_revision": 37, "source_lock_hash": frozen["source_lock_hash"], "version": "0.154.0", "surface": "codex-cli-exec",
    "model_requested": "gpt-5.6-luna", "effort_requested": "medium", "backend_model_effort_attestation": "not-observed",
    "native_callback_model": "gpt-5.6-luna", "model_turns": 7, "actual_native_patches": 7, "callbacks": callbacks_total,
    "policy_receipts": receipts_total, "results": verified, "marker_bytes_hex": marker_bytes.hex(),
    "Stop_policy_enforcement": "not-established; current Stop codec emits empty JSON for advisory and block decisions",
    "prevention_or_rollback": "not-established; exact mutation already present at every selected Stop callback entry",
    "native_hook_notification_states": "not-exposed-by-retained-exec-JSON; completed file_change/turn items observed",
    "timeout_observation": "outer5s/sleeper8s; final Stop observer remains sleep record with no selected receipt; no live owned descendants",
    "repeat_scope": "one Stop per turn with native stop_hook_active false; no actual repeat callback or repeated-reminder qualification",
    "scientific_QA": "unverified; synthetic marker binding only", "unknown_host_event": "unverified; selected codec injection only",
    "frozen_brief": bind(RUN / "frozen-brief.json"), "summary": bind(RUN / "native-stop-summary.json"), "cleanup": bind(RUN / "cleanup.json"),
    "process_audit": bind(RUN / "process-final-audit.json"), "process_union_identities": len(audit["tracked"]),
    "historical_files_preserved": len(historical), "processes_live": 0, "process_stop_performed": False,
    "global_direct_writes": False, "new_project_trust_keys": 0, "global_config_and_hook_hashes_unchanged": True,
    "full_native_gate": "unchecked", "review": "inline; no independent reviewer", "verifier": bind(Path(__file__))}
with (RUN / "verified-stop-observations.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": record["status"], "turns": 7, "patches": 7, "callbacks": callbacks_total, "receipts": receipts_total,
    "process_union": len(audit["tracked"]), "live": 0, "historical_preserved": len(historical)}))
