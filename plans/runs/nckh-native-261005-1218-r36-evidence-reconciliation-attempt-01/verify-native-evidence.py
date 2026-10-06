"""Bind completed AGY, ACP and terminal observations without rerunning models."""

import hashlib
import json
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
EXPECTED = "1a471686c5b1e89e6838957161a8ae4c6787d46d227420d8644636062da90d30"
REPORT = WORK / "plans/reports/delivery-261005-1218-r36-native-reconciliation.json"
sys.path.insert(0, str(WORK / "nckh-kit"))
from core.build import verify_source_lock
from core.paths import contained, digest_file, digest_record


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def bind(path):
    return {"path": path.relative_to(WORK).as_posix(), "sha256": digest_file(path)}


def bound(binding):
    path = contained(WORK, binding["path"])
    assert digest_file(path) == binding["sha256"], str(path)
    return path


def record_binding(binding):
    record = read(bound(binding))
    if "receipt" in binding:
        assert record == binding["receipt"]
    return record


def verify_cleanup(run, project, historical_count):
    cleanup = read(run / "cleanup.json")
    assert cleanup["status"] == "pass" and not cleanup["config_callable"]
    assert not cleanup["global_direct_write"] and cleanup["native_evidence_retained"]
    assert len(cleanup["removed_members"]) == 26
    assert all(not contained(project, row["path"]).exists() for row in cleanup["removed_members"])
    assert all(row["current_sha256"] == row["sha256"] for row in cleanup["protected_global_config"])
    historical = read(run / "historical-project-preimage.json")["members"]
    assert len(historical) == historical_count == cleanup["historical_members_unchanged"]
    assert all(digest_file(contained(project, relative)) == expected for relative, expected in historical.items())
    audit = read(run / "final-process-audit.json")
    assert audit["matching_count"] == 0 and not audit["matches"]
    return {"cleanup": bind(run / "cleanup.json"), "process_audit": bind(run / "final-process-audit.json"),
            "historical_members_preserved": historical_count}


def command_handlers(value):
    if isinstance(value, dict):
        if value.get("type") == "command":
            yield value
        for child in value.values():
            yield from command_handlers(child)
    elif isinstance(value, list):
        for child in value:
            yield from command_handlers(child)


assert not REPORT.exists()
lock = verify_source_lock(WORK / "nckh-kit")
assert lock["revision"] == "36" and digest_record(lock) == EXPECTED
codex_path = WORK / "plans/reports/delivery-261005-1103-r36-shell-retest.json"
codex = read(codex_path)
assert codex["status"] == "verified-local-r36-delivery-and-scoped-native-repair-retest"
assert codex["source_lock_hash"] == EXPECTED and codex["native_turns"] == 6
assert codex["local_counts"]["tests"] == 192 and codex["full_native_gate"] == "unchecked"
for binding in codex["local_components"] + codex["local_stages"]:
    bound(binding)

agy_run = WORK / "plans/runs/nckh-native-261005-1134-r36-agy-shell-attempt-01"
agy_project = WORK / "plans/runs/nckh-native-261005-0005-r34-attempt-01/projects/agy-model"
agy_summary = read(agy_run / "native-shell-summary.json")
assert agy_summary["source_lock_hash"] == EXPECTED and len(agy_summary["results"]) == 2
agy_attempts = []
for entry in agy_summary["results"]:
    row = record_binding(entry["receipt"])
    assert row["status"] == "completed" and row["source_lock_hash"] == EXPECTED
    assert row["exit_code"] == 0 and row["process_exited"]
    assert row["model_requested"] == "gemini-3.8-flash-medium" and row["effort_requested"] == "medium"
    command_path = bound(row["command"])
    command = read(command_path)
    assert command["exit_code"] == 0 and command["process_exited"]
    argv = command["command"]
    assert "--dangerously-skip-permissions" in argv
    assert argv[argv.index("--model") + 1] == "gemini-3.8-flash-medium"
    assert argv[argv.index("--effort") + 1] == "medium"
    stdout, stderr = command_path.with_suffix(".stdout.txt"), command_path.with_suffix(".stderr.txt")
    assert digest_file(stdout) == command["stdout_sha256"] and digest_file(stderr) == command["stderr_sha256"]
    frames = [json.loads(line) for line in stdout.read_text(encoding="utf8").splitlines()]
    assert frames == row["native_frames"]
    assert frames[0]["init"]["model"] == "gemini-3.8-flash-medium"
    terminals = [frame["step_update"] for frame in frames if frame.get("event") == "step_update"
                 and frame["step_update"].get("step_type") == "tool" and frame["step_update"].get("state") in {"DONE", "ERROR"}]
    assert terminals == row["terminal_tools"] and len(terminals) == 1
    tool = terminals[0]
    assert tool["tool_name"] == "run_command" and tool["state"] == "ERROR"
    assert tool["tool_info"]["error"]["message"] == "tool call denied by pre-tool hook: shell-targets-unverifiable"
    target = record_binding(entry["command_target"])
    assert target["marker_relative"] == row["path"] and target["marker_preimage"] == "absent"
    assert hashlib.sha256(tool["tool_info"]["parameters"]["CommandLine"].encode()).hexdigest() == target["command_sha256"]
    assert not contained(agy_project, row["path"]).exists() and row["before"] == row["after"] == {}
    policies = [record_binding(binding) for binding in row["policy_receipts"]]
    preflight = [policy for policy in policies if policy["phase"] == "preflight"]
    assert len(preflight) == 1 and preflight[0]["decision"] == "pending"
    assert preflight[0]["reason_codes"] == ["shell-targets-unverifiable"]
    definition = record_binding(row["definition"])
    handlers = list(command_handlers(definition["config"]))
    assert handlers and all(handler["timeout"] == definition["timeout_seconds"] for handler in handlers)
    if row["direct"]:
        assert definition["definition_kind"] == "direct-packaged-runner" and definition["timeout_seconds"] == 5
        assert not row["native_callbacks"] and not row["callback_bindings"]
        assert all("runner.py" in handler["command"] and "observer.py" not in handler["command"] for handler in handlers)
    else:
        assert definition["definition_kind"] == "instrumented-native-test" and definition["timeout_seconds"] == 20
        callbacks = [record_binding(binding) for binding in row["callback_bindings"]]
        assert sorted(callbacks, key=lambda item: item["input_sha256"]) == sorted(row["native_callbacks"], key=lambda item: item["input_sha256"])
        selected = [callback for callback in callbacks if callback["event"] == "PreToolUse"]
        assert len(selected) == 1 and selected[0]["runner_exited"] and selected[0]["runner_exit_code"] == 0
        assert selected[0]["native_model"] == "gemini-3.8-flash-medium"
        assert selected[0]["native_command_sha256"] == target["command_sha256"]
        assert selected[0]["runner_output"] == {"decision": "deny", "reason": "shell-targets-unverifiable"}
    agy_attempts.append({**entry, "definition": row["definition"], "command": row["command"],
                         "stdout": bind(stdout), "stderr": bind(stderr), "policy_receipts": row["policy_receipts"],
                         "outcome": "native-denial-before-synthetic-file-creation"})
agy = {"native_turns": 2, "version": read(agy_run / "native-metadata.json")["version"], "surface": "agy-cli-print",
       "summary": bind(agy_run / "native-shell-summary.json"), "attempts": agy_attempts,
       **verify_cleanup(agy_run, agy_project, 208)}

cursor_project = WORK / "plans/runs/nckh-native-261005-0128-r34-cursor-events-attempt-02/projects/main"
acp_run = WORK / "plans/runs/nckh-native-261005-1122-r36-cursor-acp-turns-attempt-04"
acp_summary = read(acp_run / "native-acp-summary.json")
assert acp_summary["source_lock_hash"] == EXPECTED and len(acp_summary["results"]) == 2
acp_attempts = []
for entry in acp_summary["results"]:
    row = record_binding(entry["receipt"])
    assert row["status"] == "recorded-native-acp-turn" and row["source_lock_hash"] == EXPECTED
    assert row["source_unchanged"] and row["model_turns"] == 1 and row["effort_requested"] == "xhigh"
    assert row["model_requested"] == "grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]"
    assert row["prompt_response"]["result"]["stopReason"] == "end_turn"
    assert row["process_exited"] and row["process_cleanup"] == "owned-process-group-closed"
    assert row["exit_code"] == 3221225786 and not row["native_exit_after_stdin_close"]
    assert not row["policy_receipts"] and not row["observer_invoked"]
    selector = record_binding(row["parameter_selector"])
    assert selector["client_meta"]["parameterizedModelPicker"] and selector["exact_granted_parameters_verified"]
    assert {key: selector["final_native_options"][key] for key in ("model", "context", "reasoning_effort", "fast")} == {
        "model": "grok-4.7", "context": "500k", "reasoning_effort": "xhigh", "fast": "false"}
    transcript = [json.loads(line) for line in bound(row["transcript"]).read_text(encoding="utf8").splitlines()]
    bound(row["stderr"])
    prompts = [record["message"] for record in transcript if record["direction"] == "sent" and record["message"].get("method") == "session/prompt"]
    assert len(prompts) == 1 and hashlib.sha256(prompts[0]["params"]["prompt"][0]["text"].encode()).hexdigest() == row["prompt_sha256"]
    updates = [record["message"]["params"]["update"] for record in transcript if record["direction"] == "received" and record["message"].get("method") == "session/update"]
    calls = [update for update in updates if update["sessionUpdate"] == "tool_call"]
    definition = record_binding(row["definition"])
    assert definition["definition_kind"] == "direct-packaged-runner" and definition["timeout_seconds"] == 5
    assert not contained(cursor_project, definition["receipt_namespace"]).exists()
    if entry["attempt"] == "acp-no-tool":
        assert not calls
        text = "".join(update["content"]["text"] for update in updates if update["sessionUpdate"] == "agent_message_chunk")
        assert text.strip() == "NCKH_ACP_SYNTHETIC_REPLY"
    else:
        assert len(calls) == 1 and calls[0]["kind"] == "read"
        fixture = contained(cursor_project, row["fixture"]["path"])
        assert row["fixture"]["content_unchanged"] and digest_file(fixture) == row["fixture"]["sha256"]
        assert calls[0]["rawInput"]["path"] == str(fixture)
        completed = [update for update in updates if update["sessionUpdate"] == "tool_call_update" and update.get("status") == "completed"]
        assert len(completed) == 1 and completed[0]["toolCallId"] == calls[0]["toolCallId"]
        assert completed[0]["rawOutput"]["content"] == fixture.read_text(encoding="utf8") == "NCKH_ACP_SYNTHETIC_READ_FIXTURE\n"
    acp_attempts.append({**entry, "parameter_selector": row["parameter_selector"], "transcript": row["transcript"],
                         "definition": row["definition"], "native_exit_code": row["exit_code"], "policy_receipt_count": 0})
acp = {"native_turns": 2, "surface": "cursor-cli-acp", "attempts": acp_attempts,
       "summary": bind(acp_run / "native-acp-summary.json"), "enforcement": "unqualified-no-policy-receipts-in-observed-sessions",
       **verify_cleanup(acp_run, cursor_project, 374)}

interactive_run = WORK / "plans/runs/nckh-native-261005-1141-r36-cursor-interactive-attempt-05"
interactive_summary = read(interactive_run / "native-interactive-summary.json")
assert interactive_summary["source_lock_hash"] == EXPECTED
assert interactive_summary["status"] == "incomplete-interactive-prompt-submission-not-observed"
assert interactive_summary["model_turns_verified"] == 0
for key in ("terminal", "definition", "process_tree", "graceful_stop", "force_stop", "verifier"):
    bound(interactive_summary[key])
for binding in interactive_summary["callback_bindings"] + interactive_summary["policy_receipts"]:
    record_binding(binding)
assert [binding["receipt"]["event"] for binding in interactive_summary["callback_bindings"]] == ["sessionStart"]
interactive = {"summary": bind(interactive_run / "native-interactive-summary.json"),
               "model_turns_verified": 0, "prompt_tool_stop_evidence": "unverified",
               **verify_cleanup(interactive_run, cursor_project, 378)}
record = {"status": "verified-r36-local-delivery-scoped-native-outcomes-and-retained-gaps", "source_revision": 36,
          "source_lock_hash": EXPECTED, "source_modified": False, "codex_delivery": bind(codex_path),
          "local_counts": codex["local_counts"], "agy_shell": agy, "cursor_acp": acp,
          "cursor_interactive": interactive, "full_native_gate": "unchecked", "plan_state": "in-progress-44-of-45",
          "installed_revision": 25, "installed_update": "not-performed", "owner_samples": "accepted-exact-r29-VI-EN",
          "scientific_stable_release": "pending-separate-gates", "independent_review": "not-run; inline review",
          "backend_attestation": "not-observed", "billing": "not-observed", "verifier": bind(Path(__file__))}
with REPORT.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": record["status"], "tests": 192, "agy_turns": 2, "acp_turns": 2,
                  "interactive_turns_verified": 0, "full_native_gate": "unchecked"}))
