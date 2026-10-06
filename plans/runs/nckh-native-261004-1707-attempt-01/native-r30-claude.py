"""Qualify only observable SessionStart paths without a model/provider turn."""

import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2] / "nckh-kit"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from core.build import verify_bundle, verify_source_lock
from core.hook_config import payload_from_bundle, preview_config
from core.paths import atomic_json, contained, digest_file, digest_record, no_links
from core.processes import run_owned_command

archive = json.loads((RUN / "native-claude-archive.json").read_text(encoding="utf8"))
package = Path(archive["extracted"])
manifest = verify_bundle(package)
source_hash = digest_record(verify_source_lock(ROOT))
if manifest["source_lock_hash"] != source_hash or manifest["host"] != "claude":
    raise RuntimeError("Native package must match the frozen reviewed candidate")
payload = payload_from_bundle(package)
grant = json.loads((RUN / "native-grant.json").read_text(encoding="utf8"))
if "register-test-definitions" not in grant["actions"]:
    raise RuntimeError("Native test bootstrap requires the human grant")
base = RUN / "projects-r30-attempt-02" / "claude"
if base.exists():
    raise RuntimeError("Preserve existing native attempt")
base.mkdir(parents=True)
records = []
modes = ("direct", "normal", "policy-block", "malformed-input", "malformed-output", "timeout", "crash",
         "unsupported-codec", "duplicate-project-plugin")
for mode in modes:
    project = base / mode
    project.mkdir()
    context = {"schema_version": 1, "task_id": "native-r30-session-start", "brief": {"mode": "auto"}}
    if mode == "policy-block":
        context["references"] = [{} for _ in range(33)]
    atomic_json(project / "context.json", context)
    preview = preview_config(project, "claude", payload, events=["SessionStart"], context_reference="context.json",
                             host_version="2.1.272", surface="claude-code", python=sys.executable)
    atomic_json(project / "registration-preview.json", preview)
    runtime = contained(project, preview["runtime_relative"])
    for relative, expected in payload["members"].items():
        destination = contained(runtime, relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(contained(package, relative), destination)
        if digest_file(destination) != expected:
            raise RuntimeError("Payload copy differs from the extracted package")
    runner = contained(runtime, payload["runner"])
    config = preview["after"]
    if mode != "direct":
        handler = {"type": "command", "command": sys.executable, "args": ["-I", str(RUN / "native-r30-observer.py"),
                   "--project", str(project), "--runner", str(runner), "--mode", mode],
                   "timeout": 1 if mode == "timeout" else 5}
        config = {"hooks": {"SessionStart": [{"matcher": ".*", "hooks": [handler]}]}}
    target = contained(project, ".claude/settings.local.json")
    atomic_json(target, config)
    owned = {target.relative_to(project).as_posix(): digest_file(target)}
    atomic_json(project / "registered-definition.json", {
        "registered_at": datetime.now(timezone.utc).isoformat(), "source_lock_hash": source_hash,
        "bundle_closure_hash": manifest["closure_hash"], "payload_closure_hash": payload["closure_hash"],
        "archive_sha256": archive["archive_sha256"], "config": config, "config_sha256": owned[target.relative_to(project).as_posix()],
        "definition_hash": digest_record(config["hooks"]["SessionStart"][0]),
        "registration_method": "human-granted-test-bootstrap", "production_apply": "not-called",
        "interactive_trust": "unobserved-init-only-with-explicit-project-settings"})
    state = project / "native-state"
    state.mkdir()
    argv = [r"C:/Users/USER\.local\bin\claude.exe", "--init-only", "--setting-sources", "project,local",
            "--settings", str(target), "--debug-file", str(project / "native-debug.log")]
    if mode == "duplicate-project-plugin":
        plugin = project / "duplicate-test-plugin"
        metadata = contained(plugin, ".claude-plugin/plugin.json")
        hooks = contained(plugin, "hooks/hooks.json")
        atomic_json(metadata, {"name": "nckh-native-duplicate-test", "version": "0.0.1"})
        atomic_json(hooks, config)
        owned[metadata.relative_to(project).as_posix()] = digest_file(metadata)
        owned[hooks.relative_to(project).as_posix()] = digest_file(hooks)
        argv += ["--plugin-dir", str(plugin)]
    environment = dict(os.environ, CLAUDE_CONFIG_DIR=str(state), CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1",
                       HTTP_PROXY="http://127.0.0.1:9", HTTPS_PROXY="http://127.0.0.1:9", ALL_PROXY="http://127.0.0.1:9")
    for variable in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "CLAUDE_CODE_OAUTH_TOKEN"):
        environment.pop(variable, None)
    name = "native-r30-claude-session-start-attempt-02-" + mode
    stdout, stderr, receipt_path = (RUN / "commands" / (name + suffix) for suffix in (".stdout", ".stderr", ".json"))
    command_record = {"argv": argv, "cwd": str(project), "started_at": datetime.now(timezone.utc).isoformat(),
                      "status": "starting", "source_lock_hash": source_hash, "owner": "/root", "port": None}

    def started(pid):
        command_record.update(pid=pid, status="running")
        atomic_json(receipt_path, command_record)

    # The outer process job owns host-created callback children, including the injected sleeper.
    original_environment = dict(os.environ)
    try:
        os.environ.clear()
        os.environ.update(environment)
        outcome = run_owned_command(argv, project, b"", stdout, stderr, timeout=45, on_started=started)
    finally:
        os.environ.clear()
        os.environ.update(original_environment)
    command_record.update(outcome, ended_at=datetime.now(timezone.utc).isoformat(),
                          stdout_sha256=digest_file(stdout), stderr_sha256=digest_file(stderr))
    atomic_json(receipt_path, command_record)
    observations = [json.loads(path.read_text(encoding="utf8")) for path in (project / "observations").glob("*.json")]
    policies = [json.loads(path.read_text(encoding="utf8")) for directory in
                (project / "policy-receipts", project / ".nckh-state/hooks/events/claude") for path in directory.glob("*.json")]
    removed, conflicts = [], []
    for relative, expected in owned.items():
        path = contained(project, relative)
        if path.is_file() and digest_file(path) == expected:
            path.unlink()
            removed.append(relative)
        else:
            conflicts.append(relative)
    row = {"mode": mode, "project": str(project), "host_exit": outcome["exit_status"],
           "command_status": outcome["status"], "observations": observations, "policy_receipts": policies,
           "callback_count": len(observations) if mode != "direct" else len(policies),
           "cleanup": {"removed_exact_owned_configs": removed, "conflicts": conflicts,
                       "processes": outcome["process_cleanup"], "payload": "retained-inert-for-evidence"},
           "preventive_tool_coverage": "not-exercised-no-model-turn"}
    records.append(row)
    atomic_json(RUN / "native-r30-claude-summary.json", {"source_lock_hash": source_hash,
                "host": "claude", "surface": "claude-code", "version": "2.1.272", "event": "SessionStart",
                "evidence_class": "native-startup-observation", "records": records,
                "native_prevention_qualification": "pending", "provider_turns": 0})
    print(json.dumps({"mode": mode, "exit": outcome["exit_status"], "callbacks": row["callback_count"],
                      "cleanup_conflicts": conflicts}), flush=True)
