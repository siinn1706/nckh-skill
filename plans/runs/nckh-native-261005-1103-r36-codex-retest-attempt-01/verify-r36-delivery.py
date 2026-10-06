"""Bind completed local stages and real native outcomes to the frozen revision."""

import json
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
DELIVERY = WORK / "plans/runs/nckh-native-261005-1050-r36-shell-guard-attempt-02"
PROJECT = WORK / "plans/runs/nckh-native-261005-0658-r34-codex-file-attempt-01/project-02"
EXPECTED = "1a471686c5b1e89e6838957161a8ae4c6787d46d227420d8644636062da90d30"
REPORT = WORK / "plans/reports/delivery-261005-1103-r36-shell-retest.json"
sys.path.insert(0, str(WORK / "nckh-kit"))
from core.build import verify_source_lock
from core.paths import contained, digest_file, digest_record

read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": digest_file(path)}


def bound(binding):
    path = contained(WORK, binding["path"])
    assert digest_file(path) == binding["sha256"]
    return path


assert not REPORT.exists()
lock = verify_source_lock(WORK / "nckh-kit")
assert lock["revision"] == "36" and digest_record(lock) == EXPECTED
pipeline = read(DELIVERY / "revalidation-summary.json")
assert pipeline["status"] == "completed-local-checks-native-retest-pending"
assert pipeline["source_lock_hash"] == EXPECTED and pipeline["source_unchanged"]
assert [s["name"] for s in pipeline["stages"]] == ["deterministic", "build", "archive", "smoke", "preview", "preservation"]
stage_bindings = []
for row in pipeline["stages"]:
    assert row["exit_status"] == 0 and row["process_cleanup"] == "owned-process-group-closed"
    path = contained(WORK, row["receipt"])
    stage = read(path)
    assert stage["source_lock_hash"] == EXPECTED and stage["exit_status"] == 0
    assert digest_file(path.with_suffix(".stdout")) == stage["stdout_sha256"]
    assert digest_file(path.with_suffix(".stderr")) == stage["stderr_sha256"]
    stage_bindings.append(bind(path))
suite = read(DELIVERY / "deterministic-r36-attempt-01-suite.json")
assert suite["successful"] and suite["tests"] == 192 and not suite["failures"] and not suite["errors"]
assert len(suite["skipped"]) == 1 and "symlink" in suite["skipped"][0]["reason"]
archive = read(DELIVERY / "archive-summary.json")
smoke = read(DELIVERY / "smoke-summary.json")
previews = read(DELIVERY / "installer-previews.json")
preservation = read(DELIVERY / "final-preservation.json")
assert all(r["status"] == "pass" and r["source_lock_hash"] == EXPECTED for r in (archive, smoke, previews, preservation))
assert len(archive["artifacts"]) == len(smoke["bundles"]) == 16
for item in archive["artifacts"]:
    assert digest_file(Path(item["archive"])) == item["archive_sha256"]
    assert Path(item["extracted"]).is_dir()
assert all(row["status"] == "pass" and row["project_unchanged"] for row in smoke["bundles"])
counts = {"tests": suite["tests"], "skipped": len(suite["skipped"]), "archives_extractions": len(archive["artifacts"]),
    "resource_reads": sum(r["resource_reads"] for r in smoke["bundles"]),
    "writer_disabled_no_read": sum(r["writer_disabled_observations"] for r in smoke["bundles"]),
    "hook_projections": sum(r["hook_projections_exercised"] for r in smoke["bundles"]),
    "installer_previews": len(previews["surfaces"]), "protected_hashes": preservation["protected_hashes_checked"]}
assert counts == {"tests": 192, "skipped": 1, "archives_extractions": 16, "resource_reads": 216,
    "writer_disabled_no_read": 48, "hook_projections": 24, "installer_previews": 8, "protected_hashes": 509}
assert preservation["installed_revision"] == "25" and preservation["installed_update"] == "not-performed"
assert len(preservation["legacy_bundles"]) == 4
summary = read(RUN / "native-retest-summary.json")
assert summary["status"] == "recorded-native-r36-shell-and-direct-file-controls" and len(summary["results"]) == 6
assert summary["source_lock_hash"] == EXPECTED and summary["full_native_gate"] == "unchecked"
attempts = []
for entry in summary["results"]:
    row = read(bound(entry["receipt"]))
    assert row["source_revision"] == 36 and row["source_lock_hash"] == EXPECTED
    assert row["model_requested"] == "gpt-5.6-luna" and row["effort_requested"] == "medium"
    assert row["status"] == "completed" and row["process_exited"] and row["exit_code"] == 0
    command_path = bound(row["command_receipt"])
    command = read(command_path)
    assert command["status"] == "completed" and command["process_exited"] and command["exit_code"] == 0
    argv = command["command"]
    assert argv[argv.index("--model") + 1] == "gpt-5.6-luna" and 'model_reasoning_effort="medium"' in argv
    assert "--dangerously-bypass-hook-trust" in argv and "--dangerously-bypass-approvals-and-sandbox" in argv
    stdout, stderr = command_path.with_suffix(".stdout.txt"), command_path.with_suffix(".stderr.txt")
    assert digest_file(stdout) == command["stdout_sha256"] and digest_file(stderr) == command["stderr_sha256"]
    frames = [json.loads(line) for line in stdout.read_text(encoding="utf8").splitlines()]
    assert frames == row["native_frames"]
    assert sum(f.get("type") == "turn.completed" for f in frames) == 1
    assert not any(f.get("type") in {"turn.failed", "error"} for f in frames)
    policies = entry.get("policy_receipts", row.get("policy_receipts"))
    assert policies and all(read(bound(p)) == p["receipt"] for p in policies)
    preflight = [p["receipt"] for p in policies if p["receipt"].get("phase") == "preflight"]
    assert len(preflight) == 1 and preflight[0]["decision"] == entry["expected_decision"]
    assert preflight[0]["reason_codes"] == [entry["expected_reason"]]
    marker = contained(PROJECT, row["marker_relative"])
    if entry["route"] == "observed-shell":
        callbacks = row["callbacks"]
        assert all(read(bound(c)) == c["receipt"] for c in callbacks)
        selected = [c["receipt"] for c in callbacks if c["receipt"]["event"] == "PreToolUse"]
        assert len(selected) == 1 and selected[0]["native_tool_name"] == "Bash"
        assert selected[0]["native_model"] == "gpt-5.6-luna" and selected[0]["runner_exited"]
        assert selected[0]["native_command_sha256"] == row["shell_command_sha256"]
        assert selected[0]["tool_input_fields"] == ["command"] and selected[0]["native_direct_path_fields"] == {}
        completed = [f["item"] for f in frames if f.get("type") == "item.completed"
            and f.get("item", {}).get("type") == "command_execution"]
        assert not any(item.get("status") == "completed" and item.get("exit_code") == 0 for item in completed)
        assert not marker.exists() and not row["marker_created"]
        outcome = "native-shell-denial-before-synthetic-file-creation"
    else:
        assert row["native_callbacks"] == [] and row["callbacks"] == [] and row["invalid_stdout_lines"] == 0
        definition = read(bound(entry["definition"]))
        assert definition["definition_kind"] == "direct-packaged-runner" and definition["timeout_seconds"] == 5
        assert not definition["observer_invoked"] and definition["fault_origin"] == "none"
        for event, groups in definition["hooks"].items():
            assert len(groups) == len(groups[0]["hooks"]) == 1
            handler = groups[0]["hooks"][0]
            assert handler["timeout"] == 5 and "runner.py" in handler["command"] and "observer.py" not in handler["command"]
            assert any(value.startswith("hooks." + event + "=") and handler["command"].replace("\\", "\\\\") in value for value in argv)
        changes = [f["item"] for f in frames if f.get("type") == "item.completed" and f.get("item", {}).get("type") == "file_change"]
        if entry["expected_decision"] == "allow":
            assert marker.read_bytes() == b"NCKH_NATIVE_FILE_ORACLE\n" and digest_file(marker) == row["marker_sha256"]
            assert len(changes) == 1 and changes[0]["status"] == "completed"
            assert changes[0]["changes"] == [{"kind": "add", "path": str(marker)}]
            assert any(p["receipt"].get("phase") == "pre-delivery" and p["receipt"]["decision"] == "pending" for p in policies)
            outcome = "native-direct-file-write-with-pending-artifact-qa"
        else:
            assert not marker.exists() and not changes and not row["marker_exists"]
            outcome = "native-direct-file-policy-denial-before-creation"
    if entry["expected_decision"] != "allow":
        assert "Command blocked by PreToolUse hook: " + entry["expected_reason"] in stderr.read_text(encoding="utf8")
    attempts.append({**entry, "command": row["command_receipt"], "stdout": bind(stdout), "stderr": bind(stderr),
        "outcome": outcome, "policy_receipts": policies})
cleanup = read(RUN / "cleanup.json")
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 26 and not cleanup["config_callable"]
assert cleanup["global_config_unchanged"] and cleanup["global_hook_unchanged"] and cleanup["new_project_trust_keys"] == 0
assert all(not contained(PROJECT, member["path"]).exists() for member in cleanup["removed_members"])
historical = read(RUN / "historical-project-preimage.json")["members"]
assert all(digest_file(contained(PROJECT, relative)) == expected for relative, expected in historical.items())
audit = read(RUN / "final-process-audit.json")
assert audit["matching_count"] == 0 and not audit["matches"]
record = {"status": "verified-local-r36-delivery-and-scoped-native-repair-retest", "source_revision": 36,
    "source_lock_hash": EXPECTED, "source_modified_during_delivery": False,
    "local_counts": counts, "local_stages": stage_bindings,
    "local_components": [bind(DELIVERY / name) for name in ("revalidation-summary.json", "deterministic-r36-attempt-01-suite.json",
        "archive-summary.json", "smoke-summary.json", "installer-previews.json", "final-preservation.json")],
    "native_turns": 6, "host": "codex", "surface": "codex-cli-exec", "version": "0.154.0",
    "model_requested": "gpt-5.6-luna", "effort_requested": "medium", "attempts": attempts,
    "historical_failure": bind(WORK / "plans/reports/delivery-261005-1042-r35-shell-target-failure.json"),
    "source_checkpoint": bind(WORK / "plans/runs/nckh-native-261005-1050-r36-shell-guard-attempt-01/source-checkpoint.json"),
    "repair_review": bind(WORK / "plans/reports/review-261005-1050-shell-target-guard.md"),
    "cleanup": bind(RUN / "cleanup.json"), "process_audit": bind(RUN / "final-process-audit.json"),
    "historical_members_preserved": len(historical), "full_native_gate": "unchecked",
    "independent_review": "not-run; inline review", "installed_revision": 25, "installed_update": "not-performed",
    "scientific_stable_release": "pending-separate-gates", "owner_samples": "accepted-exact-r29-VI-EN",
    "backend_attestation": "not-observed", "billing": "not-observed", "verifier": bind(Path(__file__))}
with REPORT.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": record["status"], "tests": 192, "native_turns": 6, "full_native_gate": "unchecked"}))
