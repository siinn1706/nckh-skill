"""Bind genuine AGY observations without upgrading missing tool routes."""

import json
import sys
from collections import Counter
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(WORK / "nckh-kit"))
from core.build import verify_source_lock
from core.paths import contained, digest_file, digest_record

EXPECTED = "4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255"
PROJECT = WORK / "plans/runs/nckh-native-261005-0005-r34-attempt-01/projects/agy-model"
REPORT = WORK / "plans/reports/delivery-261005-0838-r35-agy-tools.json"
BATCHES = (
    ("nckh-native-261005-0838-r35-agy-tools-attempt-01", 3, "final-process-audit.json"),
    ("nckh-native-261005-0844-r35-agy-tools-attempt-02", 2, "final-process-audit.json"),
    ("nckh-native-261005-0848-r35-agy-tools-attempt-03", 2, "process-audit-final.json"),
    (RUN.name, 2, "process-audit-final.json"),
)


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def bind(path):
    return {"path": path.relative_to(WORK).as_posix(), "sha256": digest_file(path)}


def bound(record):
    path = contained(WORK, record["path"])
    assert digest_file(path) == record["sha256"], record["path"]
    return path


def create_json(path, value):
    with path.open("x", encoding="utf8", newline="\n") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def snapshot(path):
    if path.is_dir():
        return {member.relative_to(path).as_posix(): digest_file(member) for member in path.rglob("*") if member.is_file()}
    return {"file": digest_file(path)} if path.is_file() else {}


assert not REPORT.exists(), "Retain the existing report"
assert digest_record(verify_source_lock(WORK / "nckh-kit")) == EXPECTED
attempts = []
batches = []
classification_counts = Counter()
for name, expected_count, audit_name in BATCHES:
    base = WORK / "plans/runs" / name
    metadata = read(base / "native-metadata.json")
    assert metadata["version"] == "1.2.16" and metadata["model_requested"] == "gemini-3.8-flash-medium"
    cleanup = read(base / "cleanup.json")
    assert cleanup["status"] == "pass" and cleanup["config_callable"] is False
    assert len(cleanup["removed_members"]) == 26
    assert all(not contained(PROJECT, member["path"]).exists() for member in cleanup["removed_members"])
    assert all(row["sha256"] == row["current_sha256"] for row in cleanup["protected_global_config"])
    historical = read(base / "historical-project-preimage.json")["members"]
    assert all(digest_file(contained(PROJECT, path)) == expected for path, expected in historical.items())
    audit = read(base / audit_name)
    assert not audit.get("matches", []) and audit.get("matching_count", 0) == 0
    summary = read(base / "native-tool-summary.json")
    assert len(summary["results"]) == expected_count
    for result in summary["results"]:
        path = bound(result["receipt"])
        row = read(path)
        assert row["source_revision"] == 35 and row["source_lock_hash"] == EXPECTED
        assert row["status"] == "completed" and row["process_exited"] and row["exit_code"] == 0
        assert row["model_requested"] == "gemini-3.8-flash-medium" and row["effort_requested"] == "medium"
        command_path = bound(row["command"])
        command = read(command_path)
        assert command["status"] == "completed" and command["process_exited"] and command["exit_code"] == 0
        argv = command["command"]
        assert "--dangerously-skip-permissions" in argv
        assert argv[argv.index("--model") + 1] == "gemini-3.8-flash-medium"
        assert argv[argv.index("--effort") + 1] == "medium"
        stdout = command_path.with_suffix(".stdout.txt")
        stderr = command_path.with_suffix(".stderr.txt")
        assert digest_file(stdout) == command["stdout_sha256"] and digest_file(stderr) == command["stderr_sha256"]
        frames = [json.loads(line) for line in stdout.read_text(encoding="utf8").splitlines()]
        assert frames == row["native_frames"]
        terminal = [frame["step_update"] for frame in frames if frame.get("event") == "step_update"
            and frame.get("step_update", {}).get("step_type") == "tool"
            and frame["step_update"].get("state") in {"DONE", "ERROR"}]
        assert terminal == row["terminal_tools"]
        definition = read(bound(row["definition"]))
        assert definition["source_lock_hash"] == EXPECTED
        assert digest_record(definition["config"]) == digest_record(read(base / "definitions" / (row["attempt"] + ".json"))["config"])
        for binding, callback in zip(row["callback_bindings"], row["native_callbacks"], strict=True):
            assert read(bound(binding)) == callback
        for policy in row["policy_receipts"]:
            assert read(bound(policy)) == policy["receipt"]
        target = contained(PROJECT, row["path"])
        assert snapshot(target) == row["after"], row["attempt"]
        pretool = [callback for callback in row["native_callbacks"] if callback["event"] == "PreToolUse"]
        preflight = [policy["receipt"] for policy in row["policy_receipts"] if policy["receipt"].get("phase") == "preflight"]
        tool = row["expected_tool"]
        error = terminal[0].get("tool_info", {}).get("error", {}).get("message", "") if terminal else None
        if not terminal:
            assert row["before"] == row["after"] and not pretool and not preflight
            classification = "no-native-tool-attempt-prevention-unverified"
        elif error and ("unknown tool: \"" + tool + "\"") in error:
            assert len(terminal) == 1 and terminal[0]["state"] == "ERROR"
            assert row["before"] == row["after"] and not pretool and not preflight
            classification = "native-cli-tool-unavailable-prevention-unverified"
        else:
            assert len(terminal) == 1 and terminal[0]["tool_name"] == tool
            assert len(preflight) == 1
            parameters = terminal[0]["tool_info"]["parameters"]
            assert Path(parameters["TargetFile"]).resolve() == target.resolve()
            if row["direct"]:
                assert not row["native_callbacks"]
                assert definition["definition_kind"] == "direct-packaged-runner" and definition["timeout_seconds"] == 5
                handlers = [handler for group in definition["config"].values() for event in
                    ("PreInvocation", "PreToolUse", "PostToolUse", "PostInvocation", "Stop")
                    for entry in group.get(event, []) for handler in entry.get("hooks", [entry])]
                assert handlers and all(handler["timeout"] == 5 and "observer" not in handler["command"] for handler in handlers)
                assert row["before"] == {}
            else:
                assert len(pretool) == 1 and pretool[0]["native_tool_name"] == tool
                assert Path(pretool[0]["native_path_fields"]["TargetFile"]).resolve() == target.resolve()
            if row["expected_deny"]:
                reason = "plan-only-mutation" if row["direct"] else "private-holdout-credential-path"
                assert preflight[0]["decision"] == "block" and reason in preflight[0]["reason_codes"]
                assert terminal[0]["state"] == "ERROR" and reason in error and row["before"] == row["after"]
                assert not row["direct"] or not target.exists()
                classification = "native-policy-denial-before-requested-write"
            else:
                assert preflight[0]["decision"] == "allow" and terminal[0]["state"] == "DONE"
                assert target.read_bytes() in (b"NCKH_AGY_REVISED\n", b"NCKH_AGY_REVISED\r\n", b"NCKH_AGY_REVISED")
                assert row["before"] != row["after"]
                classification = "native-write-completed"
        classification_counts[classification] += 1
        attempts.append({"run": name, "attempt": row["attempt"], "tool": tool, "classification": classification,
            "receipt": bind(path), "command": row["command"], "stdout": bind(stdout), "stderr": bind(stderr),
            "native_log": bind(base / "attempts" / (row["attempt"] + ".native.log")),
            "definition": row["definition"], "native_error": error, "direct_packaged_runner": row["direct"],
            "before": row["before"], "after": row["after"], "native_terminal_tools": terminal,
            "events_observed": dict(Counter(callback["event"] for callback in row["native_callbacks"])),
            "pretool_callbacks": pretool, "callback_bindings": row["callback_bindings"],
            "policy_receipts": row["policy_receipts"], "fault_origin": row["fault_origin"]})
    batches.append({"run": name, "summary": bind(base / "native-tool-summary.json"),
        "summary_status_retained": summary["status"], "cleanup": bind(base / "cleanup.json"),
        "process_audit": bind(base / audit_name), "removed_members": len(cleanup["removed_members"]),
        "historical_members_preserved": len(historical), "protected_global_config": cleanup["protected_global_config"],
        "metadata": bind(base / "native-metadata.json"), "ownership": bind(base / "ownership.json"),
        "terminal_reconciliation": bind(base / "terminal-reconciliation.json") if (base / "terminal-reconciliation.json").exists() else None})
assert len(attempts) == 9
assert dict(classification_counts) == {"native-write-completed": 2,
    "native-policy-denial-before-requested-write": 2, "native-cli-tool-unavailable-prevention-unverified": 3,
    "no-native-tool-attempt-prevention-unverified": 2}
assert digest_record(verify_source_lock(WORK / "nckh-kit")) == EXPECTED
create_json(REPORT, {"status": "recorded-native-agy-tool-and-template-observations-full-native-gate-open",
    "evidence_class": "genuine-native-cli-observations", "source_revision": 35, "source_lock_hash": EXPECTED,
    "host": "agy", "surface": "agy-cli", "version": "1.2.16", "model_requested": "gemini-3.8-flash-medium",
    "effort_requested": "medium", "backend_attestation": "not-observed", "billing": "not-observed",
    "native_turns": len(attempts), "classifications": dict(classification_counts), "batches": batches,
    "attempts": attempts, "review": "inline", "full_native_gate": "unchecked", "plan_progress": "44/45",
    "source_modified": False, "global_direct_write": False, "installed_r25_update": False,
    "verifier": bind(Path(__file__))})
print(json.dumps({"status": "verified-and-bound", "native_turns": len(attempts),
    "classifications": dict(classification_counts), "removed_members": sum(batch["removed_members"] for batch in batches)}))
