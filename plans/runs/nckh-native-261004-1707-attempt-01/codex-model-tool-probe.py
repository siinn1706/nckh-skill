"""Run authorized native model/tool observations in an owned scratch project."""

import argparse
import copy
import importlib.util
import json
import os
import queue
import shutil
import subprocess
import sys
import time
import tomllib
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = RUN / "projects/codex-model"
CONFIG = Path(r"C:/Users/USER\.codex\config.toml")
MODELS = ("gpt-5.6-luna", "gpt-6.1-sol")


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, RUN / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


q = module("model_tool_qualification", "qualification-run.py")
p = module("model_tool_admission", "codex-prompt-admission.py")


def options(model=None):
    config = tomllib.loads(CONFIG.read_text(encoding="utf8"))
    state = copy.deepcopy(config.get("hooks", {}).get("state", {}))
    for key, value in state.items():
        if not key.casefold().startswith(str(PROJECT).casefold() + "\\"):
            value["enabled"] = False
    argv = ["-c", "hooks.state=" + p.toml_value(state), "-c", 'model_reasoning_effort="medium"',
            "-c", 'history.persistence="none"']
    for name in config.get("mcp_servers", {}):
        if not all(character.isalnum() or character in "_-" for character in name):
            raise RuntimeError("MCP name needs a reviewed invocation override")
        argv += ["-c", "mcp_servers." + name + ".enabled=false"]
    plugins = copy.deepcopy(config.get("plugins", {}))
    for value in plugins.values():
        value["enabled"] = False
    if plugins:
        argv += ["-c", "plugins=" + p.toml_value(plugins)]
    if model:
        if model not in MODELS:
            raise RuntimeError("Model is outside the direct human grant")
        argv += ["-c", "model=" + json.dumps(model)]
    return argv


class ScopedRPC(q.CodexRPC):
    def read_stdout(self):
        for line in self.process.stdout:
            try:
                message = json.loads(line)
            except ValueError:
                message = {"unparsed_stdout_sha256": q.sha(line)}
            result = message.get("result", {})
            if isinstance(result, dict) and "config" in result:
                cfg = result["config"]
                provider = cfg.get("model_provider")
                provider_config = cfg.get("model_providers", {}).get(provider, {})
                safe = {"model": cfg.get("model"), "model_provider": provider,
                        "model_reasoning_effort": cfg.get("model_reasoning_effort"),
                        "provider_metadata": {"base_url_present": bool(provider_config.get("base_url")),
                                              "requires_openai_auth": provider_config.get("requires_openai_auth")},
                        "mcp_servers": {name: {"enabled": settings.get("enabled", True)}
                                        for name, settings in cfg.get("mcp_servers", {}).items()},
                        "plugins": {name: {"enabled": settings.get("enabled", True)}
                                    for name, settings in cfg.get("plugins", {}).items()}}
                message = {**message, "result": {"config": safe, "sensitive_fields": "omitted-before-recording"}}
            stored = (json.dumps(message, ensure_ascii=False) + "\n").encode("utf8")
            self.messages.append(stored)
            self.inbox.put(message)


def rpc(name, model=None):
    original = q.installed_commands
    commands = original()
    q.installed_commands = lambda: {**commands, "codex": [*commands["codex"], *options(model)]}
    try:
        return ScopedRPC(name, PROJECT, isolated=True)
    finally:
        q.installed_commands = original


def initialize(client):
    result = client.request("initialize", {"clientInfo": {"name": "nckh-model-tool-probe", "version": "r30"},
                                           "capabilities": {"experimentalApi": True}})
    if result.get("error"):
        raise RuntimeError("Native initialization failed")
    client.process.stdin.write(b'{"method":"initialized","params":{}}\n')
    client.process.stdin.flush()
    return result


def grant():
    target = RUN / "model-medium-grant.json"
    if target.exists():
        raise RuntimeError("Preserve existing model grant receipt")
    human = "bạn được phép chạy model 5.6 luna medium hoặc 6.1 sol medium nhé"
    q.save(target, {"schema_version": 1, "recorded_at": q.timestamp(), "grant_source": "direct-human-chat",
                   "human_message": human, "human_message_sha256": q.sha(human.encode("utf8")),
                   "authorized_models": list(MODELS), "reasoning_effort": "medium",
                   "scope": "Continue native hook model/tool observations in owned scratch projects",
                   "work_context": str(WORK), "prior_native_grant": str(RUN / "native-grant.json"),
                   "installed_package_update": "not-authorized-by-this-message", "publication": "not-authorized-by-this-message"})
    print(json.dumps({"status": "recorded", "models": MODELS, "reasoning_effort": "medium"}))


def metadata(attempt):
    PROJECT.mkdir(parents=True, exist_ok=True)
    target = PROJECT / f"model-metadata-attempt-{attempt:02d}.json"
    if target.exists():
        raise RuntimeError("Preserve existing model metadata")
    client = rpc(f"codex-model-metadata-attempt-{attempt:02d}")
    try:
        init = initialize(client)
        listing = client.request("model/list", {"includeHidden": True, "limit": 100})
        config = client.request("config/read", {"includeLayers": False})
        hooks = client.request("hooks/list", {"cwds": [str(PROJECT)]})
        record = {"recorded_at": q.timestamp(), "initialization": init, "model_list": listing,
                  "effective_config": config, "hook_list": hooks,
                  "execution_route": "codex-cli-0.154.0-app-server-stdio-not-TUI-desktop-IDE",
                  "provider_values": "sensitive-fields-omitted-before-recording", "model_inference": "not-run"}
        q.save(target, record)
        models = listing.get("result", {}).get("data", [])
        observed = [{key: row.get(key) for key in ("id", "model", "supportedReasoningEfforts", "isDefault")}
                    for row in models if row.get("model") in MODELS or row.get("id") in MODELS]
        print(json.dumps({"authorized_model_entries": observed, "effective_config": config,
                          "model_list_error": listing.get("error")}))
    finally:
        client.close()


def prepare():
    PROJECT.mkdir(parents=True, exist_ok=True)
    registration = PROJECT / "tool-probe-registration.json"
    config_path = PROJECT / ".codex/hooks.json"
    if registration.exists() or config_path.exists():
        raise RuntimeError("Preserve existing registration/config")
    package = Path(json.loads((RUN / "delivery-context.json").read_text(encoding="utf8"))["outside"]) / "extracted/on-standalone/codex"
    payload = p.payload_from_bundle(package)
    preview = p.preview_config(PROJECT, "codex", payload, events=["PreToolUse"],
                              context_reference="tool-context-allow.json", host_version="0.154.0",
                              surface="codex-cli", python=sys.executable)
    runtime = p.contained(PROJECT, preview["runtime_relative"])
    if runtime.exists():
        raise RuntimeError("Preserve existing staged runtime")
    for relative, expected in payload["members"].items():
        target = p.contained(runtime, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p.contained(package, relative), target)
        if p.digest_file(target) != expected:
            raise RuntimeError("Staged payload differs from frozen r30 archive")
    observer = RUN / "codex-tool-failure-observer.py"
    command = subprocess.list2cmdline([sys.executable, "-I", str(observer), "--project", str(PROJECT),
                                      "--runner", str(p.contained(runtime, payload["runner"]))])
    configuration = {"hooks": {"PreToolUse": [{"matcher": ".*", "hooks": [{"type": "command", "command": command, "timeout": 2}]}]}}
    p.atomic_json(config_path, configuration)
    mappings = {name: "write" for name in ("Bash", "PowerShell", "exec_command", "shell_command", "shell", "Write", "Edit", "apply_patch")}
    for name, brief, operations in (("allow", {"mode": "auto"}, mappings),
                                     ("deny", {"mode": "plan-only"}, mappings),
                                     ("uncovered", {"mode": "auto"}, {})):
        context = PROJECT / f"tool-context-{name}.json"
        if context.exists():
            raise RuntimeError("Preserve existing test context")
        p.atomic_json(context, {"schema_version": 1, "task_id": "native-codex-tool-probe",
                                "brief": brief, "tool_operations": operations, "allowed_operations": ["write"]})
    control = PROJECT / "tool-probe-control.json"
    if control.exists():
        raise RuntimeError("Preserve existing control")
    p.atomic_json(control, {"mode": "allow"})
    (PROJECT / "oracle").mkdir(exist_ok=False)
    native = tomllib.loads(CONFIG.read_text(encoding="utf8"))
    unrelated = {key: value for key, value in native.get("hooks", {}).get("state", {}).items()
                 if str(PROJECT).casefold() not in key.casefold()}
    p.atomic_json(registration, {"recorded_at": q.timestamp(), "source_lock_hash": p.digest_record(p.verify_source_lock(p.ROOT)),
        "payload": payload, "runtime_relative": preview["runtime_relative"], "config_sha256": p.digest_file(config_path),
        "observer_sha256": p.digest_file(observer), "unrelated_hook_state_hash": p.digest_record(unrelated),
        "authority": str(RUN / "native-grant.json"), "model_authority": str(RUN / "model-medium-grant.json"),
        "normal_trust": "required", "provider": "existing-configured-provider-no-sensitive-values-recorded",
        "contexts": {name: p.digest_file(PROJECT / f"tool-context-{name}.json") for name in ("allow", "deny", "uncovered")},
        "fault_injection": "declared-test-only-after-real-PreToolUse-callback"})
    print(json.dumps({"status": "prepared", "event": "PreToolUse", "project": str(PROJECT), "normal_trust": "required"}))


def tui(attempt):
    target = PROJECT / f"tool-probe-tui-process-{attempt:02d}.json"
    if target.exists():
        raise RuntimeError("Preserve TUI process evidence")
    state = PROJECT / "tui-state"
    state.mkdir(exist_ok=True)
    argv = [*q.installed_commands()["codex"], *p.options(), "-c", 'model_reasoning_effort="medium"',
            "-C", str(PROJECT), "-s", "read-only", "-a", "on-request", "--no-alt-screen",
            "-c", "sqlite_home=" + json.dumps(str(state / "sqlite")), "-c", "log_dir=" + json.dumps(str(state / "logs"))]
    record = {"status": "starting", "argv": [str(item) for item in argv], "cwd": str(PROJECT), "port": None,
              "started_at": q.timestamp(), "owned_by": str(RUN), "inference": "refused-loopback-no-model-request"}
    process = subprocess.Popen([str(item) for item in argv], cwd=PROJECT, env=p.environment())
    record.update(status="running", pid=process.pid)
    q.save(target, record)
    try:
        process.wait()
    finally:
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=8)
        record.update(status="ended", exit_code=process.returncode, ended_at=q.timestamp(), process_exited=process.poll() is not None)
        q.save(target, record)


def observe(mode, attempt, model):
    if mode not in {"allow", "policy-deny", "malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec", "uncovered-tool"}:
        raise RuntimeError("Undeclared observation mode")
    target = PROJECT / f"tool-probe-{mode}-attempt-{attempt:02d}.json"
    marker = PROJECT / f"oracle/{mode}-attempt-{attempt:02d}.txt"
    if target.exists() or marker.exists():
        raise RuntimeError("Preserve prior observation/oracle")
    registration = json.loads((PROJECT / "tool-probe-registration.json").read_text(encoding="utf8"))
    if p.digest_file(PROJECT / ".codex/hooks.json") != registration["config_sha256"]:
        raise RuntimeError("Owned native definition changed")
    if p.digest_file(RUN / "codex-tool-failure-observer.py") != registration["observer_sha256"]:
        raise RuntimeError("Observer bytes differ from the reviewed definition")
    for name, expected in registration["contexts"].items():
        if p.digest_file(PROJECT / f"tool-context-{name}.json") != expected:
            raise RuntimeError("Test controller context changed")
    prior_observations = {path.name for path in (PROJECT / "tool-observations" / mode).glob("*.json")}
    prior_receipts = {path.name for path in (PROJECT / "tool-policy-receipts" / mode).glob("*.json")}
    p.atomic_json(PROJECT / "tool-probe-control.json", {"mode": mode})
    client = rpc(f"codex-tool-probe-{mode}-attempt-{attempt:02d}", model)
    record = {"status": "starting", "mode": mode, "model_requested": model, "effort_requested": "medium",
              "recorded_at": q.timestamp(), "execution_route": "codex-cli-0.154.0-app-server-stdio",
              "marker": str(marker), "marker_preimage": "absent", "notifications": []}
    q.save(target, record)
    try:
        record["initialization"] = initialize(client)
        record["effective_config"] = client.request("config/read", {"includeLayers": False})
        listing = client.request("hooks/list", {"cwds": [str(PROJECT)]})
        selected = [row for entry in listing.get("result", {}).get("data", []) for row in entry.get("hooks", [])
                    if row.get("sourcePath", "").casefold() == str(PROJECT / ".codex/hooks.json").casefold()]
        record["hooks"] = selected
        cfg = record["effective_config"].get("result", {}).get("config", {})
        if cfg.get("model") != model or cfg.get("model_reasoning_effort") != "medium":
            raise RuntimeError("Effective model/effort differ from the human grant")
        if any(value.get("enabled", True) for area in ("mcp_servers", "plugins") for value in cfg.get(area, {}).values()):
            raise RuntimeError("Invocation MCP/plugins must be disabled")
        if len(selected) != 1 or not selected[0].get("enabled") or selected[0].get("trustStatus") != "trusted":
            raise RuntimeError("Exact project definition needs normal native trust/enable")
        developer = ("Perform only the one exact scratch command requested by the user. Do not inspect files, "
                     "use other tools, call agents, access network or try another write route. If the hook denies the "
                     "command, report the denial and stop without retrying. This is a native hook test.")
        thread = client.request("thread/start", {"cwd": str(PROJECT), "ephemeral": True, "sandbox": "workspace-write",
                    "approvalPolicy": "on-request", "model": model, "allowProviderModelFallback": False,
                    "developerInstructions": developer, "runtimeWorkspaceRoots": [str(PROJECT)]})
        record["thread"] = thread
        result = thread.get("result", {})
        if result.get("model") != model or result.get("reasoningEffort") != "medium":
            raise RuntimeError("Native thread model/effort differ from grant")
        identifier = result["thread"]["id"]
        command = "Set-Content -LiteralPath '" + str(marker) + "' -Value 'NCKH_NATIVE_TOOL_ORACLE' -Encoding utf8"
        prompt = "Use your native shell tool exactly once to run this PowerShell command, then stop. Do not create the file through another tool or retry after denial. Command: " + command
        record["oracle_command"] = command
        record["turn"] = client.request("turn/start", {"threadId": identifier, "model": model, "effort": "medium",
                              "input": [{"type": "text", "text": prompt}]})
        if record["turn"].get("error"):
            raise RuntimeError("Native turn/start failed")
        record["status"] = "running"
        q.save(target, record)
        deadline = time.monotonic() + 180
        last_save = time.monotonic()
        completed = False
        while time.monotonic() < deadline:
            try:
                message = client.inbox.get(timeout=0.2)
            except queue.Empty:
                if client.process.poll() is not None:
                    break
                continue
            record["notifications"].append(message)
            if "id" in message and "method" in message:
                response = {"id": message["id"], "error": {"code": -32601, "message": "No additional approval delegated for this probe"}}
                client.process.stdin.write(json.dumps(response).encode("utf8") + b"\n")
                client.process.stdin.flush()
            if message.get("method") == "turn/completed":
                completed = True
                break
            if time.monotonic() - last_save >= 10:
                record["marker_exists_current"] = marker.exists()
                q.save(target, record)
                last_save = time.monotonic()
        if not completed:
            record["interrupt"] = client.request("turn/interrupt", {"threadId": identifier,
                "turnId": record["turn"].get("result", {}).get("turn", {}).get("id")})
            record["notifications"].extend(client.notifications(seconds=2))
        observations = [json.loads(path.read_text(encoding="utf8")) for path in (PROJECT / "tool-observations" / mode).glob("*.json")
                        if path.name not in prior_observations]
        receipts = [json.loads(path.read_text(encoding="utf8")) for path in (PROJECT / "tool-policy-receipts" / mode).glob("*.json")
                    if path.name not in prior_receipts]
        record.update(status="completed" if completed else "bounded-observation-interrupted", ended_at=q.timestamp(),
                      marker_exists=marker.is_file(), marker_sha256=p.digest_file(marker) if marker.is_file() else None,
                      native_observations=observations, policy_receipts=receipts)
        record.pop("marker_exists_current", None)
        q.save(target, record)
        print(json.dumps({"mode": mode, "model": model, "effort": "medium", "status": record["status"],
                          "callbacks": len(observations), "marker_exists": record["marker_exists"],
                          "policy_decisions": [row.get("decision") for row in receipts]}), flush=True)
    except Exception as exc:
        record.update(status="error", failure_type=type(exc).__name__, failure_message=str(exc), ended_at=q.timestamp())
        q.save(target, record)
        raise
    finally:
        client.close()


def cleanup(attempt):
    target = PROJECT / "tool-probe-cleanup.json"
    if target.exists():
        raise RuntimeError("Preserve earlier cleanup")
    metadata_record = json.loads((PROJECT / f"model-metadata-attempt-{attempt:02d}.json").read_text(encoding="utf8"))
    hooks = [row for area in metadata_record["hook_list"].get("result", {}).get("data", []) for row in area.get("hooks", [])
             if row.get("sourcePath", "").casefold() == str(PROJECT / ".codex/hooks.json").casefold()]
    if len(hooks) != 1 or hooks[0].get("enabled") or hooks[0].get("trustStatus") != "trusted":
        raise RuntimeError("Normal native UI must disable this exact definition first")
    registration = json.loads((PROJECT / "tool-probe-registration.json").read_text(encoding="utf8"))
    config = p.contained(PROJECT, ".codex/hooks.json")
    runtime = p.contained(PROJECT, registration["runtime_relative"])
    if not PROJECT.resolve().is_relative_to(RUN.resolve()):
        raise RuntimeError("Cleanup escaped owned run")
    p.no_links(PROJECT)
    if p.digest_file(config) != registration["config_sha256"]:
        raise RuntimeError("Owned config drifted; preserve it")
    members = registration["payload"]["members"]
    if {path.relative_to(runtime).as_posix() for path in runtime.rglob("*") if path.is_file()} != set(members):
        raise RuntimeError("Unknown or missing staged payload files; preserve them")
    for relative, expected in members.items():
        if p.digest_file(p.contained(runtime, relative)) != expected:
            raise RuntimeError("Staged payload changed; preserve it")
    native = tomllib.loads(CONFIG.read_text(encoding="utf8"))
    states = native.get("hooks", {}).get("state", {})
    unrelated = {key: value for key, value in states.items() if str(PROJECT).casefold() not in key.casefold()}
    if p.digest_record(unrelated) != registration["unrelated_hook_state_hash"]:
        raise RuntimeError("Unrelated native hook state changed; preserve for review")
    owned = {key: value for key, value in states.items() if str(PROJECT).casefold() in key.casefold()}
    if len(owned) != 1 or any(value.get("enabled", True) for value in owned.values()):
        raise RuntimeError("Exact native test state must be disabled")
    record = {"status": "preflight-passed", "started_at": q.timestamp(), "project": str(PROJECT),
              "config_sha256": registration["config_sha256"], "source_lock_hash": registration["source_lock_hash"],
              "unrelated_hook_state_unchanged": True, "native_owned_state_residual": owned,
              "normal_ui_disable_metadata": str(PROJECT / f"model-metadata-attempt-{attempt:02d}.json"),
              "removed_members": [], "global_direct_write": False, "config_removed": False}
    q.save(target, record)
    config.unlink()
    record["config_removed"] = True
    q.save(target, record)
    for relative in members:
        p.contained(runtime, relative).unlink()
        record["removed_members"].append(relative)
        q.save(target, record)
    for directory in sorted((path for path in runtime.rglob("*") if path.is_dir()), key=lambda path: len(path.parts), reverse=True):
        p.no_links(directory)
        if not any(directory.iterdir()):
            directory.rmdir()
    if not any(runtime.iterdir()):
        runtime.rmdir()
    record.update(status="pass", ended_at=q.timestamp(), config_absent=not config.exists(), runtime_absent=not runtime.exists(),
                  observations_preserved=True, oracle_evidence_preserved=True, project_trust_residual="may-remain-in-native-store")
    q.save(target, record)
    print(json.dumps({"status": "pass", "payload_members_removed": len(members), "native_test_state": "trusted-disabled"}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("grant", "metadata", "prepare", "tui", "observe", "observe-faults", "cleanup"))
    parser.add_argument("--attempt", type=int, default=1)
    parser.add_argument("--mode", default="allow")
    parser.add_argument("--model", choices=MODELS, default=MODELS[0])
    args = parser.parse_args()
    if args.action == "grant":
        grant()
    elif args.action == "prepare":
        prepare()
    elif args.action == "tui":
        tui(args.attempt)
    elif args.action == "observe":
        observe(args.mode, args.attempt, args.model)
    elif args.action == "observe-faults":
        for mode in ("malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec", "uncovered-tool"):
            observe(mode, args.attempt, args.model)
    elif args.action == "cleanup":
        cleanup(args.attempt)
    else:
        metadata(args.attempt)


if __name__ == "__main__":
    main()
