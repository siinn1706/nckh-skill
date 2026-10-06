"""Bind native timing observations without qualifying production hook enforcement."""

import json
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
sys.path.insert(0, str(WORK / "nckh-kit"))
from core.build import verify_source_lock
from core.paths import contained, digest_file, digest_record

EXPECTED = "4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255"
REPORT = WORK / "plans/reports/delivery-261005-1021-r35-cursor-timing-diagnostic.json"
PROJECT = WORK / "plans/runs/nckh-native-261005-0128-r34-cursor-events-attempt-02/projects/main"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": digest_file(path)}


def bound(record):
    target = contained(WORK, record["path"])
    assert digest_file(target) == record["sha256"]
    return target


assert not REPORT.exists()
assert digest_record(verify_source_lock(WORK / "nckh-kit")) == EXPECTED
summary = read(RUN / "diagnostic-summary.json")
row = read(bound(summary["attempt"]))
command_path = bound(row["command_receipt"])
command = read(command_path)
assert command["status"] == "completed" and command["exit_code"] == 0 and command["process_exited"]
stdout = command_path.with_suffix(".stdout.txt")
stderr = command_path.with_suffix(".stderr.txt")
assert digest_file(stdout) == command["stdout_sha256"] and digest_file(stderr) == command["stderr_sha256"]
frames = [json.loads(line) for line in stdout.read_text(encoding="utf8").splitlines()]
assert frames == row["native_frames"] and row["invalid_stdout_lines"] == 0
calls = [f for f in frames if f.get("type") == "tool_call" and f.get("subtype") == "completed"]
assert calls == row["completed_tool_calls"] and len(calls) == 1
result = calls[0]["tool_call"]["readToolCall"]["result"]
assert result == summary["native_result"] and "success" not in result
reason = result["error"]["errorMessage"]
assert "Hook script timed out after 5000ms" in reason
assert str(RUN / "cursor-immediate-hook.py") in reason
definition = read(bound(row["definition"]))
assert definition["definition_kind"] == "immediate-diagnostic-only" and definition["timeout_seconds"] == 5
assert definition["runner_invoked"] is False and definition["policy_invoked"] is False
bound(definition["diagnostic_callback"])
assert set(definition["config"]["hooks"]) == {"sessionStart", "beforeSubmitPrompt", "preToolUse", "postToolUse", "stop"}
for handlers in definition["config"]["hooks"].values():
    assert len(handlers) == 1 and handlers[0]["timeout"] == 5
    assert str(RUN / "cursor-immediate-hook.py") in handlers[0]["command"]
    assert "runner.py" not in handlers[0]["command"]
callbacks = summary["callbacks"]
assert len(callbacks) == 2 and {c["receipt"]["event"] for c in callbacks} == {"sessionStart", "preToolUse"}
for binding in callbacks:
    receipt = read(bound(binding))
    assert receipt == binding["receipt"] and receipt["status"] == "interpreter-atexit-observed"
    assert receipt["reported_event"] == receipt["event"] and receipt["input_size"] <= 65537
    assert receipt["runner_invoked"] is False and receipt["policy_invoked"] is False
    assert 0 <= receipt["output_elapsed_seconds"] <= receipt["interpreter_elapsed_seconds"] < 0.01
    if receipt["event"] == "preToolUse":
        assert receipt["wire"] == {"permission": "allow"} and receipt["native_tool_name"] == "Read"
        assert receipt["native_tool_use_id"] == calls[0]["tool_call"]["toolCallId"]
fixture = contained(PROJECT, row["path"])
assert fixture.read_bytes() == b"NCKH_CURSOR_SYNTHETIC_READ_FIXTURE\n"
assert digest_file(fixture) == row["before_sha256"] == row["after_sha256"] and summary["fixture_unchanged"]
cleanup = read(RUN / "cleanup.json")
assert cleanup["status"] == "pass" and not cleanup["config_callable"] and len(cleanup["removed_members"]) == 26
for binding in cleanup["removed_members"]:
    assert not contained(PROJECT, binding["path"]).exists()
for relative, expected in read(RUN / "historical-project-preimage.json")["members"].items():
    assert digest_file(contained(PROJECT, relative)) == expected
assert all(c["sha256"] == c["current_sha256"] for c in cleanup["protected_global_config"])
audit = read(RUN / "final-process-audit.json")
assert audit["matching_count"] == 0 and not audit["matches"] and not audit["callback_and_cli_pid_recheck"]
assert row["model_requested"] == "grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]"
assert row["effort_requested"] == "xhigh" and not row["policy_receipts"]
assert digest_record(verify_source_lock(WORK / "nckh-kit")) == EXPECTED
record = {"status": "verified-native-timing-diagnostic-production-gate-open", "source_revision": 35,
    "source_lock_hash": EXPECTED, "source_modified": False, "native_turns": 1,
    "host": "cursor", "surface": "cursor-cli", "version": "2026.09.15-d2fe57e",
    "native_error": reason, "diagnostic_callback_invoked": True, "packaged_runner_invoked": False,
    "policy_invoked": False, "callback_counts": {"sessionStart": 1, "beforeSubmitPrompt": 0,
        "preToolUse": 1, "postToolUse": 0, "stop": 0}, "callbacks": callbacks,
    "inference": "The timeout is reproducible without NCKH policy processing; exact host execution/transport cause remains unresolved.",
    "collector_labels": "Inherited attempt observer_invoked=false denotes no original packaged-runner observer; the immediate diagnostic callback is explicitly bound here.",
    "production_timing": "unqualified", "full_native_gate": "unchecked", "attempt": summary["attempt"],
    "command": row["command_receipt"], "stdout": bind(stdout), "stderr": bind(stderr),
    "summary": bind(RUN / "diagnostic-summary.json"), "cleanup": bind(RUN / "cleanup.json"),
    "process_audit": bind(RUN / "final-process-audit.json"), "verifier": bind(Path(__file__)),
    "backend_attestation": "not-observed", "billing": "not-observed", "review": "inline"}
with REPORT.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": record["status"], "callbacks": 2, "native_timeouts": 1,
    "fixture_unchanged": True, "removed_members": 26}))
