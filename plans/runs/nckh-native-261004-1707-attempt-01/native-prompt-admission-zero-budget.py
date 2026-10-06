"""Observe Claude prompt admission with no model/provider spending."""

import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
ROOT = WORK / "nckh-kit"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from core.build import verify_bundle, verify_source_lock
from core.hook_config import payload_from_bundle, preview_config
from core.paths import atomic_json, contained, digest_file, digest_record
from core.processes import run_owned_command

base = RUN / "prompt-admission-zero-budget"
if base.exists():
    raise RuntimeError("Preserve existing native attempt")
base.mkdir()
archive = json.loads((RUN / "native-claude-archive.json").read_text(encoding="utf8"))
package = Path(archive["extracted"])
manifest = verify_bundle(package)
lock = verify_source_lock(ROOT)
source_hash = digest_record(lock)
if manifest["source_lock_hash"] != source_hash or lock["revision"] != "30":
    raise RuntimeError("Probe must bind the unchanged r30 candidate")
payload = payload_from_bundle(package)
results = []
for case in ("policy-block", "malformed-context"):
    project = base / case
    project.mkdir()
    context = {"schema_version": 1, "task_id": "native-prompt-admission-only", "references": [{} for _ in range(33)]}
    if case == "malformed-context":
        context = {"schema_version": 1}
    atomic_json(project / "context.json", context)
    preview = preview_config(project, "claude", payload, events=["UserPromptSubmit"], context_reference="context.json",
                             host_version="2.1.272", surface="claude-code", python=sys.executable)
    atomic_json(project / "registration-preview.json", preview)
    runtime = contained(project, preview["runtime_relative"])
    for relative, expected in payload["members"].items():
        destination = contained(runtime, relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(contained(package, relative), destination)
        if digest_file(destination) != expected:
            raise RuntimeError("Staged payload differs from archive")
    if case == "malformed-context":
        # The controller corrupts only its test context after the valid config preview.
        (project / "context.json").write_bytes(b"{")
    config_path = contained(project, ".claude/settings.local.json")
    atomic_json(config_path, preview["after"])
    config_hash = digest_file(config_path)
    atomic_json(project / "registered-definition.json", {"config": preview["after"], "config_sha256": config_hash,
        "definition_hash": digest_record(preview["after"]["hooks"]["UserPromptSubmit"][0]),
        "payload_closure_hash": payload["closure_hash"], "source_lock_hash": source_hash,
        "registration_method": "human-granted-disposable-test-bootstrap", "production_apply": "not-called"})
    state = project / "native-state"
    state.mkdir()
    argv = [r"C:/Users/USER\.local\bin\claude.exe", "--print", "--permission-mode", "plan",
            "--max-budget-usd", "0", "--no-session-persistence", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
            "--setting-sources", "project,local", "--settings", str(config_path), "--output-format", "json",
            "--debug-file", str(project / "native-debug.log"), "Native prompt admission probe. Do not run tools."]
    name = "native-claude-prompt-zero-budget-" + case
    stdout, stderr, receipt = (RUN / "commands" / (name + suffix) for suffix in (".stdout", ".stderr", ".json"))
    record = {"argv": argv, "cwd": str(project), "status": "starting", "started_at": datetime.now(timezone.utc).isoformat(),
              "owner": "/root", "source_lock_hash": source_hash, "configured_max_budget_usd": 0,
              "egress": "loopback-refused-proxy", "port": None}

    def started(pid):
        record.update(pid=pid, status="running")
        atomic_json(receipt, record)

    environment = dict(os.environ, CLAUDE_CONFIG_DIR=str(state), CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1",
                       HTTP_PROXY="http://127.0.0.1:9", HTTPS_PROXY="http://127.0.0.1:9", ALL_PROXY="http://127.0.0.1:9")
    for variable in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "CLAUDE_CODE_OAUTH_TOKEN"):
        environment.pop(variable, None)
    previous = dict(os.environ)
    try:
        os.environ.clear()
        os.environ.update(environment)
        outcome = run_owned_command(argv, project, b"", stdout, stderr, timeout=45, on_started=started)
    finally:
        os.environ.clear()
        os.environ.update(previous)
    record.update(outcome, ended_at=datetime.now(timezone.utc).isoformat(), stdout_sha256=digest_file(stdout),
                  stderr_sha256=digest_file(stderr))
    atomic_json(receipt, record)
    policies = [json.loads(path.read_text(encoding="utf8")) for path in
                (project / ".nckh-state/hooks/events/claude").glob("*.json")]
    row = {"case": case, "host_exit": outcome["exit_status"], "process_status": outcome["status"],
           "policy_receipts": policies, "native_callback_count": len(policies),
           "stdout": stdout.read_text(encoding="utf8", errors="replace"),
           "stderr": stderr.read_text(encoding="utf8", errors="replace"),
           "cleanup": {"config_removed": False, "removed_payload_members": [], "conflicts": [],
                       "processes": outcome["process_cleanup"]}, "configured_max_budget_usd": 0,
           "preToolUse_coverage": "not-exercised"}
    if config_path.is_file() and digest_file(config_path) == config_hash:
        config_path.unlink()
        row["cleanup"]["config_removed"] = True
    else:
        row["cleanup"]["conflicts"].append("config")
    if row["cleanup"]["config_removed"]:
        for relative, expected in payload["members"].items():
            member = contained(runtime, relative)
            if member.is_file() and digest_file(member) == expected:
                member.unlink()
                row["cleanup"]["removed_payload_members"].append(relative)
            else:
                row["cleanup"]["conflicts"].append(relative)
        for directory in sorted((path for path in runtime.rglob("*") if path.is_dir()), key=lambda path: len(path.parts), reverse=True):
            if not any(directory.iterdir()):
                directory.rmdir()
        if not any(runtime.iterdir()):
            runtime.rmdir()
    results.append(row)
    atomic_json(RUN / "native-prompt-admission-zero-budget.json", {"schema_version": 1,
        "recorded_at": record["ended_at"], "source_lock_hash": source_hash, "source_revision": "30",
        "host": "claude", "surface": "claude-code", "version": "2.1.272", "event": "UserPromptSubmit",
        "evidence_class": "native-prompt-admission-probe", "results": results, "provider_success": "none-observed",
        "native_preventive_matrix": "pending"})
    print(json.dumps({"case": case, "exit": outcome["exit_status"], "callbacks": len(policies),
                      "cleanup_conflicts": row["cleanup"]["conflicts"]}), flush=True)
