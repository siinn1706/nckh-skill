"""Verify genuine Codex policy denial and direct runner definitions at template5s."""

import json
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = WORK / "plans/runs/nckh-native-261005-0658-r34-codex-file-attempt-01/project-02"
sys.path.insert(0, str(WORK / "nckh-kit"))
from core.build import verify_source_lock
from core.paths import contained, digest_file, digest_record

EXPECTED = "4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255"
REPORT = WORK / "plans/reports/delivery-261005-1021-r35-codex-template-controls.json"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": digest_file(path)}


def bound(record):
    path = contained(WORK, record["path"])
    assert digest_file(path) == record["sha256"]
    return path


assert not REPORT.exists()
assert digest_record(verify_source_lock(WORK / "nckh-kit")) == EXPECTED
summary = read(RUN / "direct-template-summary.json")
assert summary["status"] == "recorded-native-direct-template-controls" and len(summary["results"]) == 3
assert not summary["observer_invoked"] and summary["fault_origin"] == "none"
attempts = []
for entry in summary["results"]:
    row = read(bound(entry["receipt"]))
    assert row["source_revision"] == 35 and row["source_lock_hash"] == EXPECTED
    assert row["model_requested"] == "gpt-5.6-luna" and row["effort_requested"] == "medium"
    assert row["status"] == "completed" and row["process_exited"] and row["exit_code"] == 0
    assert row["native_callbacks"] == [] and row["callbacks"] == []
    command_path = bound(row["command_receipt"])
    command = read(command_path)
    assert command["status"] == "completed" and command["process_exited"] and command["exit_code"] == 0
    argv = command["command"]
    assert argv[argv.index("--model") + 1] == "gpt-5.6-luna"
    assert 'model_reasoning_effort="medium"' in argv
    assert "--dangerously-bypass-hook-trust" in argv and "--dangerously-bypass-approvals-and-sandbox" in argv
    stdout = command_path.with_suffix(".stdout.txt")
    stderr = command_path.with_suffix(".stderr.txt")
    assert digest_file(stdout) == command["stdout_sha256"] and digest_file(stderr) == command["stderr_sha256"]
    frames = [json.loads(line) for line in stdout.read_text(encoding="utf8").splitlines()]
    assert frames == row["native_frames"] and row["invalid_stdout_lines"] == 0
    assert sum(f["type"] == "turn.completed" for f in frames) == 1
    assert not any(f.get("type") in {"turn.failed", "error"} for f in frames)
    definition = read(bound(entry["definition"]))
    assert definition["definition_kind"] == "direct-packaged-runner" and definition["timeout_seconds"] == 5
    assert not definition["observer_invoked"] and definition["fault_origin"] == "none"
    for event, groups in definition["hooks"].items():
        assert "hooks." + event + "=" + __import__("json").dumps(None) not in argv
        assert any(value.startswith("hooks." + event + "=") and groups[0]["hooks"][0]["command"]
            .replace("\\", "\\\\") in value for value in argv)
        assert len(groups) == 1 and len(groups[0]["hooks"]) == 1
        handler = groups[0]["hooks"][0]
        assert handler["timeout"] == 5 and "observer.py" not in handler["command"] and "runner.py" in handler["command"]
    policies = [read(bound(p)) for p in entry["policy_receipts"]]
    assert all(read(bound(p)) == p["receipt"] for p in entry["policy_receipts"])
    preflight = [p for p in policies if p["phase"] == "preflight"]
    assert len(preflight) == 1
    marker = contained(PROJECT, row["marker_relative"])
    native_changes = [f["item"] for f in frames if f.get("type") == "item.completed"
        and f.get("item", {}).get("type") == "file_change"]
    denied = row["mode"] == "policy-deny" or row["marker_relative"].startswith("private/")
    if denied:
        reason = "plan-only-mutation" if row["mode"] == "policy-deny" else "private-holdout-credential-path"
        assert not marker.exists() and not native_changes
        assert preflight[0]["decision"] == "block" and reason in preflight[0]["reason_codes"]
        assert "Command blocked by PreToolUse hook: " + reason in stderr.read_text(encoding="utf8")
        outcome = "native-policy-denial-before-file-creation"
    else:
        assert marker.read_bytes() == b"NCKH_NATIVE_FILE_ORACLE\n" and digest_file(marker) == row["marker_sha256"]
        assert len(native_changes) == 1 and native_changes[0]["status"] == "completed"
        assert native_changes[0]["changes"] == [{"kind": "add", "path": str(marker)}]
        assert preflight[0]["decision"] == "allow"
        assert any(p["phase"] == "pre-delivery" and p["decision"] == "pending" for p in policies)
        outcome = "native-write-completed-with-pending-artifact-qa"
    attempts.append({**entry, "command": row["command_receipt"], "stdout": bind(stdout), "stderr": bind(stderr),
        "outcome": outcome, "events_with_policy_receipts": sorted({Path(p["path"]).parent.name for p in entry["policy_receipts"]})})
cleanup = read(RUN / "cleanup.json")
definition = read(RUN / "definition.json")
assert cleanup["status"] == "pass" and not cleanup["config_callable"] and len(cleanup["removed_members"]) == 26
assert cleanup["global_config_unchanged"] and cleanup["global_hook_unchanged"] and cleanup["new_project_trust_keys"] == 0
assert digest_file(Path(r"C:/Users/USER\.codex\config.toml")) == definition["global_config_sha256"]
assert digest_file(Path(r"C:/Users/USER\.codex\hooks.json")) == definition["global_hook_sha256"]
assert all(not contained(PROJECT, p["path"]).exists() for p in cleanup["removed_members"])
historical = read(RUN / "historical-project-preimage.json")["members"]
assert all(digest_file(contained(PROJECT, relative)) == expected for relative, expected in historical.items())
audit = read(RUN / "final-process-audit.json")
assert not audit["matches"] and audit["matching_count"] == 0
assert digest_record(verify_source_lock(WORK / "nckh-kit")) == EXPECTED
record = {"status": "verified-scoped-native-direct-template5s-controls", "source_revision": 35,
    "source_lock_hash": EXPECTED, "source_modified": False, "host": "codex", "surface": "codex-cli-exec",
    "version": "0.154.0", "native_turns": 3, "timeout_seconds": 5, "observer_invoked": False,
    "fault_origin": "none", "attempts": attempts, "full_native_gate": "unchecked",
    "timing_scope": "Three canonical apply_patch add-file turns only; failure matrix and other routes remain separate.",
    "summary": bind(RUN / "direct-template-summary.json"), "cleanup": bind(RUN / "cleanup.json"),
    "process_audit": bind(RUN / "final-process-audit.json"), "historical_members_preserved": len(historical),
    "global_config_unchanged": True, "global_hook_unchanged": True, "new_project_trust_keys": 0,
    "backend_attestation": "not-observed", "billing": "not-observed", "verifier": bind(Path(__file__)), "review": "inline"}
with REPORT.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": record["status"], "native_turns": 3, "removed_members": 26,
    "global_hashes_unchanged": True, "full_native_gate": "unchecked"}))
