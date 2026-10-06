"""Bind native same-input callback pairs and keep unknown-event scope explicit."""

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = WORK / "plans/runs/nckh-native-261005-0005-r34-attempt-01/projects/agy-model"
sys.path.insert(0, str(WORK / "nckh-kit"))
from core.build import verify_source_lock
from core.paths import contained, digest_record

read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {"path": p.relative_to(WORK).as_posix(), "sha256": sha(p)}


def bound(row):
    path = contained(WORK, row["path"])
    assert sha(path) == row["sha256"], path
    return path


summary = read(RUN / "native-duplicate-summary.json")
brief = read(bound(summary["frozen_brief"]))
assert summary["status"] == "recorded-native-agy-duplicate-and-config-admission"
assert summary["model_turns"] == len(summary["results"]) == len(brief["cases"]) == 2 and summary["model_retries"] == 0
assert digest_record(verify_source_lock(WORK / "nckh-kit")) == brief["source_lock_hash"]
assert brief["outer_handler_timeout_seconds"] == brief["inner_runner_timeout_seconds"] == 5
bound(brief["controller"])
bound(brief["observer"])
bound(brief["model_inventory_reused"])
events = ("PreInvocation", "PreToolUse", "PostToolUse", "PostInvocation", "Stop")
records = []
for case, result in zip(brief["cases"], summary["results"]):
    assert case["name"] == result["attempt"] and case["kind"] == result["kind"]
    attempt_path = bound(result["receipt"])
    attempt = read(attempt_path)
    command = read(bound(attempt["command"]))
    assert command["exit_code"] == attempt["exit_code"] == 0 and command["process_exited"] and attempt["process_exited"]
    assert command["timeout_seconds"] is None and command["capture_errors"] == []
    argv = command["command"]
    assert "--dangerously-skip-permissions" in argv and argv[argv.index("--model") + 1] == "gemini-3.8-flash-medium"
    assert argv[argv.index("--effort") + 1] == "medium" and argv[argv.index("--print-timeout") + 1] == "0"
    target = contained(PROJECT, case["fixture"])
    assert str(target) in argv[-1] and json.dumps(bytes.fromhex(case["requested_hex"]).decode()) in argv[-1]
    stdout = RUN / "commands" / ("agy-tools-" + case["name"] + ".stdout.txt")
    stderr = RUN / "commands" / ("agy-tools-" + case["name"] + ".stderr.txt")
    assert sha(stdout) == command["stdout_sha256"] and sha(stderr) == command["stderr_sha256"]
    frames = [json.loads(s) for s in stdout.read_text(encoding="utf8").splitlines()]
    assert frames == attempt["native_frames"]
    initialization = [f for f in frames if f.get("event") == "init"]
    final = [f for f in frames if f.get("event") == "result"]
    assert len(initialization) == len(final) == 1
    init = initialization[0]
    assert init["init"]["model"] == "gemini-3.8-flash-medium" and init["init"]["permission_mode"] == "always-proceed"
    assert Path(init["init"]["cwd"]).resolve() == PROJECT.resolve()
    conversation = init["conversation_id"]
    assert final[0]["result"]["conversation_id"] == conversation and final[0]["result"]["num_turns"] == 1
    assert final[0]["result"]["status"] == "SUCCESS" and final[0]["result"]["response"].strip() == "ORACLE_ATTEMPT_FINISHED"
    terminal = [f["step_update"] for f in frames if f.get("event") == "step_update" and
                f["step_update"].get("step_type") == "tool" and f["step_update"].get("state") in ("DONE", "ERROR")]
    assert len(terminal) == 1 and terminal == attempt["terminal_tools"]
    tool = terminal[0]
    assert tool["tool_name"] == "write_to_file" and tool["state"] == "DONE" and tool["conversation_id"] == conversation
    assert Path(tool["tool_info"]["parameters"]["TargetFile"]).resolve() == target.resolve()
    assert target.read_bytes() == bytes.fromhex(case["requested_hex"]) and result["exact_revised_bytes"]
    callbacks = [read(bound(p)) for p in result["callback_bindings"]]
    assert callbacks == [read(bound(p)) for p in attempt["callback_bindings"]]
    assert callbacks == attempt["native_callbacks"]
    for callback in callbacks:
        assert callback["fault_origin"] == "none" and callback["workspace_contains_selected_project"]
        assert callback["native_session_hash"] == hashlib.sha256(conversation.encode()).hexdigest()
        if callback["event"] in ("PreToolUse", "PostToolUse"):
            assert callback["native_tool_name"] == "write_to_file" and callback["native_step_idx"] == tool["step_index"]
            assert Path(callback["native_path_fields"]["TargetFile"]).resolve() == target.resolve()
    policies = [read(bound(p)) for p in result["policy_bindings"]]
    assert len(policies) == 5 and {p["phase"] for p in policies} == {"advisory", "preflight", "pre-delivery", "stop"}
    grouped = defaultdict(list)
    for callback in callbacks:
        grouped[(callback["event"], callback["input_sha256"])].append(callback)
    if case["kind"] == "project-plugin":
        assert len(callbacks) == 14 and len(grouped) == 7
        assert all(len(pair) == 2 and {c["callback_source"] for c in pair} == {"project", "plugin"} for pair in grouped.values())
        assert all(sum(c["event"] == event for c in callbacks) == (4 if "Invocation" in event else 2) for event in events)
        classification = "verified-five-event-project-plugin-duplicates-and-idempotent-receipts"
    else:
        definition = read(bound(attempt["definition"]))
        assert brief["unknown_config_event"] in next(iter(definition["config"].values()))
        assert len(callbacks) == 7 and all(c["callback_source"] == "project" for c in callbacks)
        assert result["callback_counts"][brief["unknown_config_event"]] == 0
        classification = "native-config-admission-observed-unknown-event-execution-unqualified"
    assert read(RUN / "commands" / ("agy-tools-" + case["name"] + ".child-reconciliation.json"))["same_process_live"] == 0
    records.append({"attempt": case["name"], "classification": classification, "conversation_id": conversation,
        "native_tool_count": 1, "native_step_index": tool["step_index"], "exact_revised_bytes": True,
        "callback_counts": result["callback_counts"], "same_input_groups": len(grouped), "policy_receipt_count": 5,
        "receipt": bind(attempt_path), "definition": attempt["definition"], "command": attempt["command"]})
assert len({r["conversation_id"] for r in records}) == 2
cleanup = read(RUN / "cleanup.json")
plugin_cleanup = read(RUN / "plugin-cleanup.json")
audit = read(RUN / "process-final-audit.json")
assert cleanup["status"] == plugin_cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 26
assert len(plugin_cleanup["removed_members"]) == 2 and not cleanup["config_callable"]
assert all(r["sha256"] == r["current_sha256"] for r in cleanup["protected_global_config"])
assert audit["matching_count"] == audit["tracked_live_count"] == 0 and not audit["process_stop_performed"]
output = {"status": "verified-agy-five-event-duplicates-and-scoped-config-admission", "source_revision": 37,
    "source_lock_hash": brief["source_lock_hash"], "host": "agy-cli", "host_version": read(RUN / "native-metadata.json")["version"],
    "model_observed": "gemini-3.8-flash-medium", "effort_requested": "medium", "model_turns": 2, "model_retries": 0,
    "results": records, "instrumentation": "test observer; five-second outer/inner bounds; no fault injection",
    "unsupported_event_scope": "unknown configured name accepted during one native turn, zero unknown callbacks; unknown native event delivery unqualified",
    "full_native_gate": "unchecked", "source_modified": False, "global_plugin_install": False,
    "cleanup": bind(RUN / "cleanup.json"), "plugin_cleanup": bind(RUN / "plugin-cleanup.json"),
    "process_audit": bind(RUN / "process-final-audit.json"), "frozen_brief": bind(RUN / "frozen-brief.json"), "verifier": bind(Path(__file__))}
with (RUN / "verified-duplicate-delivery.json").open("x", encoding="utf8") as stream:
    json.dump(output, stream, ensure_ascii=False, indent=2)
print(json.dumps({"status": output["status"], "native_callbacks": 21, "matching_cleanup_members": 28,
                  "tracked_identities": len(audit["tracked"]), "full_native_gate": "unchecked"}))
