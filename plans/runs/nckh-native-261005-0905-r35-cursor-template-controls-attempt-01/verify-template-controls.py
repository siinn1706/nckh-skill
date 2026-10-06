"""Verify retained Cursor native template failures and their evidence bindings."""

import json
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-0818-r35-cursor-template-timing-attempt-01"
sys.dont_write_bytecode = True
sys.path.insert(0, str(WORK / "nckh-kit"))
from core.build import verify_source_lock
from core.paths import contained, digest_file, digest_record

EXPECTED = "4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255"
REPORT = WORK / "plans/reports/delivery-261005-0905-r35-cursor-template-controls.json"
PROJECT = WORK / "plans/runs/nckh-native-261005-0128-r34-cursor-events-attempt-02/projects/main"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": digest_file(path)}


def bound(record):
    path = contained(WORK, record["path"])
    assert digest_file(path) == record["sha256"]
    return path


assert not REPORT.exists()
assert digest_record(verify_source_lock(WORK / "nckh-kit")) == EXPECTED
attempts = []
batches = []
for base, expected_count in ((BASE, 1), (RUN, 3)):
    summary = read(base / "native-file-summary.json")
    assert len(summary["results"]) == expected_count
    cleanup = read(base / "cleanup.json")
    assert cleanup["status"] == "pass" and cleanup["config_callable"] is False
    assert len(cleanup["removed_members"]) == 26
    assert all(not contained(PROJECT, item["path"]).exists() for item in cleanup["removed_members"])
    assert all(item["sha256"] == item["current_sha256"] for item in cleanup["protected_global_config"])
    historical = read(base / "historical-project-preimage.json")["members"]
    assert all(digest_file(contained(PROJECT, relative)) == expected for relative, expected in historical.items())
    audit = read(base / "final-process-audit.json")
    assert not audit.get("matches", []) and audit.get("matching_count", 0) == 0
    for result in summary["results"]:
        path = bound(result["receipt"])
        row = read(path)
        assert row["source_revision"] == 35 and row["source_lock_hash"] == EXPECTED
        assert row["status"] == "completed" and row["process_exited"] and row["exit_code"] == 0
        assert row["model_requested"] == "grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]"
        assert row["effort_requested"] == "xhigh" and row["fault_origin"] == "none" and not row["observer_invoked"]
        command_path = bound(row["command_receipt"])
        command = read(command_path)
        argv = command["command"]
        assert command["status"] == "completed" and command["process_exited"] and command["exit_code"] == 0
        assert "--force" in argv and "--trust" in argv and argv[argv.index("--sandbox") + 1] == "disabled"
        assert argv[argv.index("--model") + 1] == row["model_requested"]
        stdout = command_path.with_suffix(".stdout.txt")
        stderr = command_path.with_suffix(".stderr.txt")
        assert digest_file(stdout) == command["stdout_sha256"] and digest_file(stderr) == command["stderr_sha256"]
        frames = [json.loads(line) for line in stdout.read_text(encoding="utf8").splitlines()]
        assert frames == row["native_frames"] and row["invalid_stdout_lines"] == 0
        completed = [frame for frame in frames if frame.get("type") == "tool_call" and frame.get("subtype") == "completed"]
        assert completed == row["completed_tool_calls"] and len(completed) == 1
        call = completed[0]["tool_call"]
        name = "readToolCall" if row["kind"] == "Read" else "editToolCall"
        assert name in call
        response = call[name]["result"]
        assert "success" not in response
        native_error = response.get("rejected", response.get("error", {}))
        reason = native_error.get("reason", native_error.get("message", native_error.get("errorMessage", "")))
        assert "Hook script timed out after 5000ms" in reason
        definition = read(bound(row["definition"]))
        assert definition["definition_kind"] == "direct-packaged-runner" and definition["timeout_seconds"] == 5
        assert all(handler["timeout"] == 5 and "observer" not in handler["command"]
            for handlers in definition["config"]["hooks"].values() for handler in handlers)
        for policy in row["policy_receipts"]:
            assert read(bound(policy)) == policy["receipt"]
        target = contained(PROJECT, row["path"])
        actual_hash = digest_file(target) if target.is_file() else None
        assert actual_hash == row["after_sha256"]
        if row["kind"] == "Read":
            assert actual_hash == row["before_sha256"] and target.read_bytes() == b"NCKH_CURSOR_SYNTHETIC_READ_FIXTURE\n"
        else:
            assert row["before_sha256"] is None and actual_hash is None
        attempts.append({"attempt": row["attempt"], "kind": row["kind"], "mode": row["mode"],
            "receipt": bind(path), "definition": row["definition"], "command": row["command_receipt"],
            "stdout": bind(stdout), "stderr": bind(stderr), "policy_receipts": row["policy_receipts"],
            "native_error": reason, "before_sha256": row["before_sha256"], "after_sha256": row["after_sha256"],
            "native_tool_id": call["toolCallId"], "outer_started_at_ms": call["startedAtMs"],
            "outer_completed_at_ms": call["completedAtMs"], "fault_origin": "none", "observer_invoked": False,
            "control_outcome": result.get("control_outcome", "native-error-write-control-unqualified")})
    batches.append({"run": base.name, "summary": bind(base / "native-file-summary.json"),
        "cleanup": bind(base / "cleanup.json"), "process_audit": bind(base / "final-process-audit.json"),
        "metadata": bind(base / "native-metadata.json"), "removed_members": len(cleanup["removed_members"]),
        "historical_members_preserved": len(historical), "protected_global_config": cleanup["protected_global_config"],
        "global_cli_hash_before": cleanup["global_cli_hash_before"], "global_cli_hash_after": cleanup["global_cli_hash_after"]})
assert len(attempts) == 4
assert digest_record(verify_source_lock(WORK / "nckh-kit")) == EXPECTED
record = {"status": "recorded-native-template5s-failures-full-native-gate-open", "source_revision": 35,
    "source_lock_hash": EXPECTED, "host": "cursor", "surface": "cursor-cli", "version": "2026.09.15-d2fe57e",
    "native_turns": 4, "new_native_turns": 3, "native_timeouts": 4, "timeout_seconds": 5,
    "fault_origin": "none", "observer_invoked": False, "timeout_root_cause": "unresolved",
    "timing_qualification": "unqualified", "source_modified": False, "backend_attestation": "not-observed",
    "billing": "not-observed", "attempts": attempts, "batches": batches,
    "verifier": bind(Path(__file__)),
    "failed_verifier_preimage": bind(RUN / "verify-template-controls.failed-preimage.py"),
    "collector_correction": "Read tool native error uses errorMessage; previous extraction only read reason/message. Historical native summary is preserved.",
    "review": "inline", "full_native_gate": "unchecked"}
with REPORT.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": "verified-native-timeouts", "new_native_turns": 3, "total_template_turns": 4,
    "removed_members": sum(batch["removed_members"] for batch in batches), "timing_qualification": "unqualified"}))
