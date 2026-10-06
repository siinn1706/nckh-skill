"""Bind native observations without treating lifecycle or post-tool faults as prevention."""

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = WORK / "plans/runs/nckh-native-261005-0005-r34-attempt-01/projects/agy-model"
EVIDENCE = PROJECT / ".nckh-native-r37-agy-event-controls-34"
sys.path.insert(0, str(WORK / "nckh-kit"))
from core.build import verify_source_lock
from core.paths import contained, digest_record

EXPECTED = "629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb"
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {"path": p.relative_to(WORK).as_posix(), "sha256": sha(p)}


def bound(row):
    path = contained(WORK, row["path"])
    assert sha(path) == row["sha256"], path
    return path


assert not (RUN / "verified-event-delivery.json").exists()
assert digest_record(verify_source_lock(WORK / "nckh-kit")) == EXPECTED
summary = read(RUN / "native-event-summary.json")
brief = read(bound(summary["frozen_brief"]))
assert summary["status"] == "recorded-native-agy-event-controls"
assert summary["model_turns"] == len(summary["results"]) == len(brief["cases"]) == 28
assert summary["model_retries"] == 0 and brief["maximum_model_turns"] == 28
assert brief["outer_handler_timeout_seconds"] == brief["inner_runner_timeout_seconds"] == 5
assert brief["timeout_injection_seconds"] == 8
bound(brief["controller"])
bound(brief["observer"])
stage = read(RUN / "stage.json")
for name, expected in stage["contexts"].items():
    assert sha(EVIDENCE / name) == expected
counts = {}
records = []
for case, result in zip(brief["cases"], summary["results"]):
    assert (case["name"], case["event"], case["mode"]) == (result["attempt"], result["event"], result["mode"])
    attempt_path = bound(result["receipt"])
    attempt = read(attempt_path)
    assert attempt["source_revision"] == 37 and attempt["source_lock_hash"] == EXPECTED and not attempt["direct"]
    command_path = bound(attempt["command"])
    command = read(command_path)
    assert command["process_exited"] and attempt["process_exited"] and command["capture_errors"] == []
    assert command["timeout_seconds"] is None and command["exit_code"] == attempt["exit_code"]
    argv = command["command"]
    assert argv[0] == r"C:/Users/USER\AppData\Local\agy\bin\agy.exe"
    assert "--dangerously-skip-permissions" in argv and argv[argv.index("--model") + 1] == "gemini-3.8-flash-medium"
    assert argv[argv.index("--effort") + 1] == "medium" and argv[argv.index("--print-timeout") + 1] == "0"
    fixture = contained(PROJECT, case["fixture"])
    assert str(fixture) in argv[-1] and json.dumps(bytes.fromhex(case["requested_hex"]).decode()) in argv[-1]
    command_name = "agy-tools-" + case["name"]
    stdout = RUN / "commands" / (command_name + ".stdout.txt")
    stderr = RUN / "commands" / (command_name + ".stderr.txt")
    assert sha(stdout) == command["stdout_sha256"] and sha(stderr) == command["stderr_sha256"]
    frames = [json.loads(line) for line in stdout.read_text(encoding="utf8").splitlines()]
    assert frames == attempt["native_frames"]
    initialization = [f for f in frames if f.get("event") == "init"]
    final = [f for f in frames if f.get("event") == "result"]
    assert len(initialization) == 1 and len(final) <= 1
    init = initialization[0]
    assert init["init"]["model"] == "gemini-3.8-flash-medium" and init["init"]["permission_mode"] == "always-proceed"
    assert Path(init["init"]["cwd"]).resolve() == PROJECT.resolve()
    conversation = init["conversation_id"]
    terminal = [f["step_update"] for f in frames if f.get("event") == "step_update" and
                f["step_update"].get("step_type") == "tool" and f["step_update"].get("state") in ("DONE", "ERROR")]
    assert terminal == attempt["terminal_tools"] and len(terminal) <= 1
    for tool in terminal:
        assert tool["tool_name"] == "write_to_file" and tool["conversation_id"] == conversation
        assert Path(tool["tool_info"]["parameters"]["TargetFile"]).resolve() == fixture.resolve()
    callbacks = [read(bound(r)) for r in attempt["callback_bindings"]]
    assert callbacks == attempt["native_callbacks"]
    selected = [c for c in callbacks if c["event"] == case["event"]]
    assert len(selected) == result["selected_callback_count"]
    for callback in callbacks:
        assert callback["workspace_contains_selected_project"]
        assert callback["native_session_hash"] == hashlib.sha256(conversation.encode()).hexdigest()
        counts[callback["event"]] = counts.get(callback["event"], 0) + 1
        if callback["event"] in ("PreToolUse", "PostToolUse"):
            assert terminal and callback["native_step_idx"] == terminal[0]["step_index"]
            assert callback["native_tool_name"] == "write_to_file"
            assert Path(callback["native_path_fields"]["TargetFile"]).resolve() == fixture.resolve()
    policies = [read(bound(p)) for p in result["selected_policy_bindings"]]
    assert result["selected_policy_decisions"] == [p["decision"] for p in policies]
    if selected and case["mode"] == "policy-deny":
        assert policies and all(p["decision"] == "block" and p["reason_codes"] == ["bounded-input-exceeded"] for p in policies)
    if selected and case["mode"] == "malformed-input":
        assert policies and all(p["status"] == "degraded-failed" and p["decision"] == "block" for p in policies)
    if case["mode"] in ("crash", "malformed-output"):
        assert not policies
    definition = read(bound(attempt["definition"]))
    assert definition["timeout_seconds"] == 5 and definition["definition_kind"] == "instrumented-native-test"
    assert all(h["timeout"] == 5 for g in definition["config"].values() for e in
               ("PreInvocation", "PreToolUse", "PostToolUse", "PostInvocation", "Stop") for r in g[e] for h in r.get("hooks", [r]))
    unchanged = fixture.read_bytes() == bytes.fromhex(case["initial_hex"])
    revised = fixture.read_bytes() == bytes.fromhex(case["requested_hex"])
    assert unchanged == result["exact_unchanged_bytes"] and revised == result["exact_revised_bytes"] and (unchanged or revised)
    assert attempt["after"] == {"file": sha(fixture)}
    assert read(RUN / "commands" / (command_name + ".child-reconciliation.json"))["same_process_live"] == 0
    native_log = RUN / "attempts" / (case["name"] + ".native.log")
    native_hook_errors = [line for line in native_log.read_text(encoding="utf8", errors="replace").splitlines()
                          if "hook" in line.casefold() and case["event"] in line and
                          any(word in line.casefold() for word in ("failed", "error", "exit status"))]
    durations = [(datetime.fromisoformat(c["completed_at"]) - datetime.fromisoformat(c["started_at"])).total_seconds()
                 for c in selected if "completed_at" in c]
    records.append({"attempt": case["name"], "event": case["event"], "mode": case["mode"], "conversation_id": conversation,
        "selected_callback_count": len(selected), "selected_policy_decisions": result["selected_policy_decisions"],
        "selected_callback_durations_seconds": durations, "native_hook_errors": native_hook_errors,
        "native_terminal_states": [t["state"] for t in terminal], "fixture_unchanged": unchanged,
        "fixture_exact_revised": revised, "native_exit_code": attempt["exit_code"],
        "final_marker_observed": result["final_marker_observed"], "timing_scope": result["timing_scope"],
        "callback_qualified": bool(selected), "receipt": bind(attempt_path), "command": bind(command_path),
        "native_log": bind(native_log)})
assert len({r["conversation_id"] for r in records}) == 28
cleanup = read(RUN / "cleanup.json")
audit = read(RUN / "process-final-audit.json")
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 26 and not cleanup["config_callable"]
assert all(r["sha256"] == r["current_sha256"] for r in cleanup["protected_global_config"])
assert audit["matching_count"] == audit["tracked_live_count"] == 0 and not audit["process_stop_performed"]
assert not (PROJECT / ".agents/hooks.json").exists()
output = {"status": "verified-native-agy-event-observations", "source_revision": 37, "source_lock_hash": EXPECTED,
    "host": "agy-cli", "host_version": read(RUN / "native-metadata.json")["version"], "model_observed": "gemini-3.8-flash-medium",
    "effort_requested": "medium", "permission_mode_observed": "always-proceed", "model_turns": 28, "model_retries": 0,
    "event_case_count": len(records), "results": records, "observed_callback_counts": counts,
    "instrumentation": "test observer with five-second outer and inner bounds; faults after genuine callback",
    "effect_limit": "lifecycle block is advisory-only; post-tool mutation persistence does not establish preventive enforcement",
    "unsupported_event_scope": "injected codec event only", "duplicate_scope": "ordinary lifecycle repetition; controlled duplicate still pending",
    "full_native_gate": "unchecked", "source_modified": False, "global_controller_config_write": False,
    "backend_attestation": "not-observed", "summary": bind(RUN / "native-event-summary.json"),
    "frozen_brief": bind(RUN / "frozen-brief.json"), "cleanup": bind(RUN / "cleanup.json"),
    "process_audit": bind(RUN / "process-final-audit.json"), "verifier": bind(Path(__file__))}
with (RUN / "verified-event-delivery.json").open("x", encoding="utf8") as stream:
    json.dump(output, stream, ensure_ascii=False, indent=2)
print(json.dumps({"status": output["status"], "model_turns": 28, "callbacks": counts,
                  "tracked_identities": len(audit["tracked"]), "full_native_gate": "unchecked"}))
