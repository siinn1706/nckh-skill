"""Verify actual file changes and preserve fail-open observations."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("fault_controller", RUN / "run-patch-faults.py")
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)
probe, owned = controller.runtime()
probe.check_source()
read = controller.read
frozen = read(RUN / "frozen-brief.json")
summary = read(RUN / "native-patch-fault-summary.json")
definition = read(RUN / "definition.json")
cleanup = read(RUN / "cleanup.json")
audit = read(RUN / "process-final-audit.json")
assert summary["status"] == "recorded-five-native-patch-faults"
assert len(summary["results"]) == 5 and [r["mode"] for r in summary["results"]] == frozen["modes"]
assert read(RUN / "controller-poll-03.json")["exit_code"] == 0
assert audit["matching_count"] == audit["tracked_live_count"] == 0
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 26
assert cleanup["new_project_trust_keys"] == 0 and cleanup["global_config_unchanged"] and cleanup["global_hook_unchanged"]
assert not cleanup["config_callable"]
assert all(not probe.contained(probe.PROJECT, row["path"]).exists() for row in cleanup["removed_members"])
history = read(RUN / "historical-project-preimage.json")["members"]
assert len(history) == cleanup["historical_project_members_unchanged"]
assert all(probe.digest_file(probe.contained(probe.PROJECT, p)) == h for p, h in history.items())
for groups in definition["hooks"].values():
    assert len(groups) == 1 and len(groups[0]["hooks"]) == 1 and groups[0]["hooks"][0]["timeout"] == 5
runner_hashes = [r["sha256"] for r in definition["staged_members"] if r["path"].endswith("/hooks/runner.py")]
assert len(runner_hashes) == 1
verified = []
callback_count = policy_count = 0
for result in summary["results"]:
    case_path = probe.WORK / result["receipt"]["path"]
    assert probe.digest_file(case_path) == result["receipt"]["sha256"]
    case = read(case_path)
    assert case["source_lock_hash"] == probe.EXPECTED and case["source_revision"] == 37
    assert case["process_exited"] and case["exit_code"] == 0 and case["invalid_stdout_lines"] == 0
    assert case["model_requested"] == "gpt-5.6-luna" and case["effort_requested"] == "medium"
    command_path = probe.WORK / case["command_receipt"]["path"]
    assert probe.digest_file(command_path) == case["command_receipt"]["sha256"]
    command = read(command_path)
    assert command["exit_code"] == 0 and command["process_exited"] and command["timeout_seconds"] is None
    assert command["capture_errors"] == [] and not command["owned_handle_stop_performed"]
    assert '--dangerously-bypass-hook-trust' in command["command"]
    assert '--dangerously-bypass-approvals-and-sandbox' in command["command"]
    assert 'model_reasoning_effort="medium"' in command["command"]
    frames = case["native_frames"]
    assert sum(f.get("type") == "turn.started" for f in frames) == 1
    assert sum(f.get("type") == "turn.completed" for f in frames) == 1
    assert any(f.get("item", {}).get("type") == "agent_message" and f["item"].get("text") == "ORACLE_ATTEMPT_FINISHED" for f in frames)
    changes = [f["item"] for f in frames if f.get("type") == "item.completed" and f.get("item", {}).get("type") == "file_change"]
    actual = []
    for callback in case["callbacks"]:
        path = probe.WORK / callback["path"]
        assert probe.digest_file(path) == callback["sha256"]
        obs = read(path)
        assert obs["reported_event"] == obs["event"] and obs["native_model"] == "gpt-5.6-luna"
        assert obs["runner_sha256"] == runner_hashes[0]
        actual.append(obs)
    pre = [o for o in actual if o["event"] == "PreToolUse"]
    post = [o for o in actual if o["event"] == "PostToolUse"]
    assert len(pre) == 1 and pre[0]["native_tool_name"] == "apply_patch" and pre[0]["native_tool_use_id"]
    assert pre[0]["native_command_sha256"] == case["requested_patch_sha256"]
    assert pre[0]["fault_origin"] == "controller-after-genuine-callback" and pre[0]["selected"]
    assert len({o["native_session_hash"] for o in actual}) == 1
    receipts = []
    for policy in case["policy_receipts"]:
        path = probe.WORK / policy["path"]
        assert probe.digest_file(path) == policy["sha256"]
        receipts.append({**policy, "receipt": read(path)})
    before = len(changes) == 0 and len(post) == 0 and not probe.contained(probe.PROJECT, case["marker_relative"]).exists()
    if case["mode"] == "malformed-input":
        assert before and not case["marker_exists"]
        assert pre[0]["runner_output"]["hookSpecificOutput"]["permissionDecision"] == "deny"
        native_outcome = "deny-output; no completed file change, no marker, no post callback"
    else:
        assert len(changes) == len(post) == 1 and case["marker_exists"]
        assert changes[0]["status"] == "completed" and len(changes[0]["changes"]) == 1
        change = changes[0]["changes"][0]
        marker = probe.contained(probe.PROJECT, case["marker_relative"])
        assert change["kind"] == "add" and Path(change["path"]).resolve() == marker.resolve()
        assert marker.read_bytes() == b"NCKH_NATIVE_FILE_ORACLE\n" and probe.digest_file(marker) == case["marker_sha256"]
        assert post[0]["native_tool_use_id"] == pre[0]["native_tool_use_id"]
        native_outcome = "one completed native file change and exact marker despite selected hook fault"
    if case["mode"] == "crash":
        assert pre[0]["status"] == "intentional-test-crash-exit-17"
    elif case["mode"] == "malformed-output":
        assert pre[0]["status"] == "intentional-test-malformed-output"
    elif case["mode"] == "timeout":
        assert pre[0]["status"] == "intentional-test-sleep-eight-seconds"
        assert not any('/PreToolUse/' in r["path"] for r in receipts)
    elif case["mode"] == "unsupported-codec":
        assert pre[0]["runner_exit_code"] == 3 and pre[0]["runner_output"] == {}
        assert any('/PreToolUse/' in r["path"] and r["decision"] == "block" for r in receipts)
    callback_count += len(actual)
    policy_count += len(receipts)
    verified.append({"mode": case["mode"], "receipt": probe.bind(case_path), "native_outcome": native_outcome,
        "native_tool_use_id": pre[0]["native_tool_use_id"], "actual_command_matches_patch": True,
        "marker_exists": case["marker_exists"], "completed_file_changes": len(changes), "post_callbacks": len(post),
        "native_callbacks": [{**r, "observation": o} for r,o in zip(case["callbacks"], actual)], "policy_receipts": receipts,
        "command_receipt": probe.bind(command_path)})
assert callback_count == 24 and policy_count == 21
record = {"status": "verified-five-native-codex-patch-fault-observations", "source_revision": 37,
    "source_lock_hash": probe.EXPECTED, "native_version": "0.154.0", "surface": "codex-cli-exec",
    "model_requested": "gpt-5.6-luna", "effort_requested": "medium", "callback_models": ["gpt-5.6-luna"],
    "backend_effort_attestation": "not-observed", "model_turns": 5, "prompt_submissions": 5, "model_retries": 0,
    "actual_native_tool_requests": 5, "callback_count": callback_count, "policy_receipt_count": policy_count,
    "cases": verified, "fault_origin": "controller-after-genuine-native-PreToolUse",
    "outer_timeout_seconds": 5, "inner_timeout_seconds": 5, "injected_sleep_seconds": 8,
    "host_hook_notification_status": "not present in retained exec JSON; actual file effects and native callbacks verified",
    "scope_limit": "canonical public add-file apply_patch; genuine unsupported native event not tested; injection distinct",
    "unsupported_codec_result": "deterministic block receipt and empty native output/exit3; native patch still completes",
    "timeout_result": "observer sleep snapshot retained; no preflight policy receipt; patch completes",
    "full_native_gate": "unchecked", "plan_tasks": "44/45", "source_update": "not-performed",
    "installed_update": "not-performed", "publication": "not-performed", "new_trust_keys": 0,
    "cleanup": probe.bind(RUN / "cleanup.json"), "removed_members": 26, "historical_preserved": len(history),
    "process_audit": probe.bind(RUN / "process-final-audit.json"), "tracked_identities": len(audit["tracked"]),
    "matching_live": 0, "tracked_live": 0, "global_configs_unchanged": True,
    "AGY_readonly_help": probe.bind(RUN / "commands/agy-cli-help.json"), "AGY_help_model_prompts": 0,
    "review": "inline; no independent reviewer", "verifier": probe.bind(Path(__file__))}
assert not (RUN / "verified-patch-fault-delivery.json").exists()
probe.atomic_json(RUN / "verified-patch-fault-delivery.json", record)
print(json.dumps({"status": record["status"], "turns":5, "callbacks":24, "receipts":21,
    "native_file_changes":4, "tracked":len(audit["tracked"]), "full_native_gate":"unchecked"}), flush=True)
