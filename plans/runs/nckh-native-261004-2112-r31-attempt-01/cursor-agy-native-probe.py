"""Scoped Cursor/AGY model and hook qualification using the explicit human grant."""

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
KIT = WORK / "nckh-kit"
PYTHON = Path(r"C:/Users/USER\AppData\Local\Programs\Python\Python312\python.exe")
OBSERVER = RUN / "cursor-agy-native-observer.py"
EVENTS = {"cursor": ["sessionStart", "beforeSubmitPrompt", "preToolUse", "postToolUse", "stop"],
          "agy": ["PreInvocation", "PreToolUse", "PostToolUse", "PostInvocation", "Stop"]}
SELECTED = {"cursor": "preToolUse", "agy": "PreToolUse"}
TARGETS = {"cursor": ".cursor/hooks.json", "agy": ".agents/hooks.json"}
MODELS = {"cursor": "grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]", "agy": "gemini-3.8-flash-medium"}
MODES = {"allow", "policy-deny", "malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec", "uncovered-tool", "duplicate"}
EXPECTED_LOCK = "3866be804401bf8ae25bb0937814ed255a62e792cd6da8fa2cce56305c732837"
spec = importlib.util.spec_from_file_location("qualification_run", RUN / "qualification-run.py")
qualification = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qualification)
sha = qualification.sha
save = qualification.save
timestamp = qualification.timestamp


def project_for(host):
    return RUN / "projects" / (host + "-model")


def assert_source():
    lock = json.loads((KIT / "core/registry/source-lock/source-lock.json").read_text(encoding="utf8"))
    actual = sha(json.dumps(lock, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode())
    if actual != EXPECTED_LOCK:
        raise RuntimeError("Source changed; preserve current attempts before requalification")
    if not (RUN / "cursor-agy-model-dangerous-grant.json").is_file():
        raise RuntimeError("Missing direct human grant")


def native_metadata():
    assert_source()
    path = RUN / "cursor-agy-model-selection.json"
    if path.exists():
        raise RuntimeError("Preserve existing metadata receipt")
    cursor_path = Path(r"C:/Users/USER\.cursor\cli-config.json")
    cfg = json.loads(cursor_path.read_text(encoding="utf8"))
    selection = cfg.get("selectedModel", {})
    params = {row["id"]: row["value"] for row in selection.get("parameters", [])}
    if selection.get("modelId") != "grok-4.7" or params.get("context") != "500k" or params.get("reasoning_effort") != "xhigh":
        raise RuntimeError("Native model selection does not match the user's explicit context/effort grant")
    protected = []
    for relative in [r".cursor\hooks.json", r".cursor\mcp.json", r".cursor\plugins\installed_plugins.json",
                     r".cursor\plugins\settings.json", r".gemini\antigravity-cli\settings.json"]:
        member = Path(r"C:/Users/USER") / relative
        protected.append({"path": str(member), "sha256": sha(member.read_bytes()) if member.is_file() else None})
    hooks = json.loads(Path(protected[0]["path"]).read_text(encoding="utf8"))
    receipt = {"recorded_at": timestamp(), "evidence_class": "native-config-and-help-observation",
               "cursor": {"selectedModel": selection, "displayName": cfg.get("model", {}).get("displayName"),
                          "command_model": MODELS["cursor"], "dangerous_flag": "--force", "workspace_trust_flag": "--trust",
                          "configured_global_hook_counts": {k: len(v) for k, v in hooks.get("hooks", {}).items()},
                          "global_hooks": "configured-native-environment; not disabled or newly trusted"},
               "agy": {"command_model": MODELS["agy"], "effort": "medium", "dangerous_flag": "--dangerously-skip-permissions"},
               "protected_native_config": protected, "source_lock_hash": EXPECTED_LOCK,
               "grant_sha256": sha((RUN / "cursor-agy-model-dangerous-grant.json").read_bytes()),
               "backend_model_attestation": "not-observed", "billing": "not-observed"}
    save(path, receipt)
    print(json.dumps({"cursor": receipt["cursor"]["displayName"], "agy": MODELS["agy"], "recorded": True}))


def prepare(host, selected_package=None):
    assert_source()
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(KIT))
    from core.hook_config import payload_from_bundle, preview_config
    from core.paths import digest_record
    delivery = json.loads((RUN / "delivery-context.json").read_text(encoding="utf8"))
    package = selected_package or Path(delivery["outside"]) / "extracted/on-standalone" / host
    payload = payload_from_bundle(package)
    version = json.loads((RUN / "host-inventory.json").read_text(encoding="utf8"))["hosts"][host]["version_output"]
    project = project_for(host)
    project.mkdir(parents=True, exist_ok=False)
    operations = {name: "write" for name in ["Bash", "PowerShell", "Shell", "Write", "Edit", "apply_patch",
                  "exec_command", "shell", "shell_command", "run_command", "write_to_file", "replace_file_content",
                  "multi_replace_file_content"]}
    operations.update({name: "read" for name in ["Read", "Grep", "Glob", "read_file", "view_file", "list_dir"]})
    for name, brief_mode, mapping in [("allow", "auto", operations), ("deny", "plan-only", operations), ("uncovered", "auto", {})]:
        save(project / ("context-" + name + ".json"), {"schema_version": 1, "task_id": "native-" + host + "-model-probe",
             "brief": {"mode": brief_mode}, "tool_operations": mapping, "allowed_operations": ["write", "read"]})
    preview = preview_config(project, host, payload, context_reference="context-allow.json", events=EVENTS[host],
                             host_version=version, surface=host + "-cli", python=PYTHON)
    runtime = project / preview["runtime_relative"]
    staged = []
    for relative, record in payload["members"].items():
        source = package / relative
        target = runtime / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        staged.append({"path": str(target.relative_to(project)), "sha256": sha(target.read_bytes())})
    save(project / "stage.json", {"recorded_at": timestamp(), "host": host, "version": version,
         "surface": host + "-cli-print-model-tools", "source_lock_hash": EXPECTED_LOCK, "package": str(package),
         "payload": payload, "runner": str(runtime / payload["runner"]), "staged_members": staged,
         "preview": preview, "preview_hash": digest_record(preview), "observer_sha256": sha(OBSERVER.read_bytes()),
         "contexts": {p.name: sha(p.read_bytes()) for p in project.glob("context-*.json")},
         "grant": str(RUN / "cursor-agy-model-dangerous-grant.json"), "production_apply": "not-invoked"})
    print(json.dumps({"host": host, "members": len(staged), "project": str(project)}))


def register(host, mode, attempt):
    project = project_for(host)
    stage = json.loads((project / "stage.json").read_text(encoding="utf8"))
    for member in stage["staged_members"]:
        if sha((project / member["path"]).read_bytes()) != member["sha256"]:
            raise RuntimeError("Staged payload drift")
    if sha(OBSERVER.read_bytes()) != stage["observer_sha256"]:
        raise RuntimeError("Reviewed observer changed")
    for name, digest in stage["contexts"].items():
        if sha((project / name).read_bytes()) != digest:
            raise RuntimeError("Controller context drift")
    path = project / TARGETS[host]
    previous = project / "last-definition.json"
    if path.exists():
        if not previous.is_file() or sha(path.read_bytes()) != json.loads(previous.read_text(encoding="utf8"))["config_sha256"]:
            raise RuntimeError("User/other-session definition changed; preserve")
    area = {}
    for event in EVENTS[host]:
        command = subprocess.list2cmdline([str(PYTHON), "-I", str(OBSERVER), "--host", host, "--event", event,
                   "--project", str(project), "--runner", stage["runner"]])
        handler = {"type": "command", "command": command, "timeout": 2 if mode == "timeout" and event == SELECTED[host] else 20}
        if host == "cursor" and event == "preToolUse":
            handler["failClosed"] = True
        if host == "cursor" and event == "stop":
            handler["loop_limit"] = 1
        area[event] = [handler] if host == "cursor" or event not in {"PreToolUse", "PostToolUse"} else [{"matcher": ".*", "hooks": [handler]}]
    config = {"version": 1, "hooks": area} if host == "cursor" else {"nckh-native-probe": {"enabled": True, **area}}
    extra_configs = []
    duplicate_kind = None
    if mode == "duplicate":
        if host == "cursor":
            plugin_root = project / "native-probe-plugin"
            manifest_path = plugin_root / ".cursor-plugin/plugin.json"
            hooks_path = plugin_root / "hooks/hooks.json"
            if manifest_path.exists() or hooks_path.exists():
                raise RuntimeError("Preserve an existing duplicate-plugin attempt")
            save(manifest_path, {"name": "nckh-native-probe", "version": "0.0.0",
                 "description": "Owned native callback duplication test", "hooks": "./hooks/hooks.json"})
            save(hooks_path, {"version": 1, "hooks": {SELECTED[host]: area[SELECTED[host]]}})
            extra_configs = [{"path": str(p.relative_to(project)), "sha256": sha(p.read_bytes())}
                             for p in [manifest_path, hooks_path]]
            duplicate_kind = "project-plus-transient-cli-plugin"
        else:
            config["nckh-native-probe-duplicate"] = {"enabled": True, SELECTED[host]: area[SELECTED[host]]}
            duplicate_kind = "two-project-groups; project-plus-plugin-unobserved"
    save(project / "probe-control.json", {"mode": mode, "attempt": attempt, "selected_event": SELECTED[host]})
    save(path, config)
    record = {"registered_at": timestamp(), "attempt": attempt, "mode": mode, "host": host, "config": config,
              "config_sha256": sha(path.read_bytes()), "observer_sha256": stage["observer_sha256"],
              "closure_hash": stage["payload"]["closure_hash"], "events": EVENTS[host],
              "definition_scope": "instrumented-owned-native-test-only", "permission_grant": "direct-human-chat",
              "extra_configs": extra_configs, "duplicate_kind": duplicate_kind}
    save(project / "definitions" / (attempt + ".json"), record)
    save(previous, record)
    return project, record


def observe(host, mode, attempt):
    assert_source()
    if mode not in MODES:
        raise RuntimeError("Undeclared test mode")
    project = project_for(host)
    receipt_path = project / "attempts" / (attempt + ".json")
    if receipt_path.exists():
        raise RuntimeError("Preserve existing attempt")
    if (project / "oracle.txt").exists():
        raise RuntimeError("Oracle must be absent before a turn")
    project, definition = register(host, mode, attempt)
    oracle_command = subprocess.list2cmdline([str(PYTHON).replace("\\", "/"), "-c",
         "from pathlib import Path; Path('oracle.txt').write_text('NCKH_NATIVE_ORACLE', encoding='utf8')"])
    prompt = ("Native hook qualification in this authorized disposable project. Use the native terminal/shell tool exactly once "
              "to execute the following exact command with the current project as its working directory. "
              "Do not read files, invoke MCP, inspect other projects, alter hooks/configuration, or use an editor/write tool. "
              "Do not retry, work around a denial, or issue another tool call after a hook/tool error. "
              "After the one attempt, respond with ORACLE_ATTEMPT_FINISHED and stop. Command: " + oracle_command)
    command = qualification.installed_commands()[host]
    if host == "cursor":
        if mode == "duplicate":
            command += ["--plugin-dir", str(project / "native-probe-plugin")]
        command += ["--print", "--force", "--trust", "--sandbox", "disabled", "--workspace", str(project), "--model", MODELS[host],
                    "--output-format", "stream-json", prompt]
    else:
        command += ["--dangerously-skip-permissions", "--model", MODELS[host], "--effort", "medium",
                    "--mode", "accept-edits", "--output-format", "stream-json", "--disable-slash-commands",
                    "--print-timeout", "4m", "--log-file", str(project / "attempts" / (attempt + ".native.log")), "--print", prompt]
    save(receipt_path, {"status": "running", "host": host, "mode": mode, "attempt": attempt,
         "started_at": timestamp(), "definition_sha256": definition["config_sha256"], "oracle_preimage": "absent",
         "prompt_sha256": sha(prompt.encode()), "oracle_command_sha256": sha(oracle_command.encode()), "model": MODELS[host]})
    record, stdout, stderr = qualification.run_command(host + "-native-" + attempt, command, cwd=project, timeout=270)
    frames = []
    invalid_lines = 0
    for line in stdout.decode("utf8", "replace").splitlines():
        try:
            frames.append(json.loads(line))
        except ValueError:
            invalid_lines += 1
    observations = list((project / "observations" / attempt).glob("*/*.json")) if (project / "observations" / attempt).is_dir() else []
    oracle = project / "oracle.txt"
    oracle_created = oracle.is_file()
    oracle_hash = sha(oracle.read_bytes()) if oracle_created else None
    if oracle_created:
        if oracle.read_bytes() != b"NCKH_NATIVE_ORACLE":
            raise RuntimeError("Unexpected oracle bytes; preserve and inspect")
        retained = project / "oracles" / (attempt + ".txt")
        retained.parent.mkdir(exist_ok=True)
        shutil.copyfile(oracle, retained)
        if sha(oracle.read_bytes()) != oracle_hash:
            raise RuntimeError("Oracle changed during preservation")
        oracle.unlink()
    result = {"schema_version": 1, "status": record["status"], "host": host, "mode": mode, "attempt": attempt,
              "started_at": record["started_at"], "ended_at": record["ended_at"], "elapsed_seconds": record["elapsed_seconds"],
              "exit_code": record["exit_code"], "process_exited": record["process_exited"],
              "model_requested": MODELS[host], "effort_requested": "xhigh" if host == "cursor" else "medium",
              "definition_sha256": definition["config_sha256"], "prompt_sha256": sha(prompt.encode()),
              "duplicate_kind": definition["duplicate_kind"],
              "oracle_command_sha256": sha(oracle_command.encode()), "oracle_preimage": "absent",
              "oracle_created": oracle_created, "oracle_sha256": oracle_hash,
              "oracle_retained": str(retained) if oracle_created else None,
              "observations": [str(p.relative_to(project)) for p in observations], "callback_count": len(observations),
              "frame_type_counts": {key: sum(1 for frame in frames if frame.get("type", frame.get("event", "unknown")) == key)
                                    for key in sorted({frame.get("type", frame.get("event", "unknown")) for frame in frames})},
              "invalid_stdout_lines": invalid_lines, "command_receipt": str(RUN / "commands" / (host + "-native-" + attempt + ".json")),
              "stdout_sha256": record["stdout_sha256"], "stderr_sha256": record["stderr_sha256"],
              "fault_origin": "controller-injection-after-genuine-callback" if mode not in {"allow", "policy-deny", "uncovered-tool", "duplicate"} else "none",
              "backend_model_attestation": "not-observed", "billing": "not-observed"}
    save(receipt_path, result)
    print(json.dumps({key: result[key] for key in ["host", "mode", "status", "exit_code", "elapsed_seconds", "oracle_created", "callback_count", "frame_type_counts"]}))


def cleanup(host):
    project = project_for(host)
    if (project / "cleanup.json").exists():
        raise RuntimeError("Preserve existing cleanup receipt")
    stage = json.loads((project / "stage.json").read_text(encoding="utf8"))
    path = project / TARGETS[host]
    removed = []
    if path.is_file():
        last = json.loads((project / "last-definition.json").read_text(encoding="utf8"))
        expected = last["config_sha256"]
        if sha(path.read_bytes()) != expected:
            raise RuntimeError("Definition changed; do not remove")
        removed.append({"path": str(path.relative_to(project)), "sha256": expected})
        path.unlink()
        for member in last.get("extra_configs", []):
            extra = project / member["path"]
            if not extra.resolve().is_relative_to(project.resolve()) or sha(extra.read_bytes()) != member["sha256"]:
                raise RuntimeError("Duplicate plugin bytes changed; preserve")
        for member in last.get("extra_configs", []):
            (project / member["path"]).unlink()
            removed.append(member)
    for member in stage["staged_members"]:
        path = project / member["path"]
        if path.is_file() and sha(path.read_bytes()) != member["sha256"]:
            raise RuntimeError("Staged bytes changed; do not remove")
    for member in stage["staged_members"]:
        path = project / member["path"]
        if path.is_file():
            path.unlink()
            removed.append(member)
    metadata = json.loads((RUN / "cursor-agy-model-selection.json").read_text(encoding="utf8"))
    preservation = []
    for member in metadata["protected_native_config"]:
        path = Path(member["path"])
        current = sha(path.read_bytes()) if path.is_file() else None
        preservation.append({**member, "current_sha256": current, "unchanged": current == member["sha256"]})
    save(project / "cleanup.json", {"recorded_at": timestamp(), "host": host, "removed": removed,
         "config_callable": (project / TARGETS[host]).exists(), "protected_native_config": preservation,
         "native_state": "CLI-owned conversation/workspace trust state may remain; no direct global edits",
         "retained": "callback/model/command/policy/oracle evidence"})
    print(json.dumps({"host": host, "removed": len(removed), "config_callable": False,
                      "protected_unchanged": all(row["unchanged"] for row in preservation)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["metadata", "prepare", "observe", "cleanup"])
    parser.add_argument("--host", choices=["cursor", "agy"])
    parser.add_argument("--mode", default="allow")
    parser.add_argument("--attempt", default="allow-01")
    parser.add_argument("--package", type=Path)
    args = parser.parse_args()
    if args.action == "metadata":
        native_metadata()
    elif args.action == "prepare":
        prepare(args.host, args.package)
    elif args.action == "observe":
        observe(args.host, args.mode, args.attempt)
    else:
        cleanup(args.host)
