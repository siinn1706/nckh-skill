"""Probe a native prompt hook while the inference endpoint is refused loopback."""

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
ROOT = WORK / "nckh-kit"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from core.build import verify_source_lock
from core.hook_config import payload_from_bundle, preview_config
from core.paths import atomic_json, contained, digest_file, digest_record, no_links

project = RUN / "projects/codex"
plan_path = project / "prompt-admission-registration.json"


def toml_value(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{" + ", ".join(json.dumps(key) + "=" + toml_value(item) for key, item in value.items()) + "}"
    raise RuntimeError("Unsupported override value")


def options():
    config = tomllib.loads(Path(r"C:/Users/USER\.codex\config.toml").read_text(encoding="utf8"))
    argv = []
    hook_state = config.get("hooks", {}).get("state", {})
    for key, value in hook_state.items():
        if key.casefold().startswith(str(Path(r"C:/Users/USER\.codex\hooks.json")).casefold() + ":"):
            value["enabled"] = False
    argv += ["-c", "hooks.state=" + toml_value(hook_state)]
    for name in config.get("mcp_servers", {}):
        if not all(character.isalnum() or character in "_-" for character in name):
            raise RuntimeError("MCP name requires an explicit reviewed override")
        argv += ["-c", "mcp_servers." + name + ".enabled=false"]
    argv += ["-c", 'model_provider="nckh_native_refused"',
             "-c", 'model_providers.nckh_native_refused.name="NCKH refused loopback"',
             "-c", 'model_providers.nckh_native_refused.base_url="http://127.0.0.1:9/v1"',
             "-c", 'model_providers.nckh_native_refused.requires_openai_auth=false',
             "-c", 'model_providers.nckh_native_refused.wire_api="responses"',
             "-c", 'model_providers.nckh_native_refused.request_max_retries=0',
             "-c", 'model_providers.nckh_native_refused.stream_max_retries=0',
             "-c", 'history.persistence="none"']
    return argv


def environment():
    result = dict(os.environ, HTTP_PROXY="http://127.0.0.1:9", HTTPS_PROXY="http://127.0.0.1:9", ALL_PROXY="http://127.0.0.1:9")
    for name in ("OPENAI_API_KEY", "CODEX_API_KEY", "ACCESS_TOKEN"):
        result.pop(name, None)
    return result


def prepare():
    if plan_path.exists() or (project / ".codex/hooks.json").exists():
        raise RuntimeError("Preserve existing registration or user config")
    package = Path(json.loads((RUN / "delivery-context.json").read_text(encoding="utf8"))["outside"]) / "extracted/on-standalone/codex"
    payload = payload_from_bundle(package)
    context = contained(project, "prompt-admission-context.json")
    if context.exists():
        raise RuntimeError("Preserve existing context")
    atomic_json(context, {"schema_version": 1, "task_id": "native-codex-prompt-block-only", "references": [{} for _ in range(33)]})
    preview = preview_config(project, "codex", payload, events=["UserPromptSubmit"],
                             context_reference="prompt-admission-context.json", host_version="0.154.0", surface="codex-cli", python=sys.executable)
    runtime = contained(project, preview["runtime_relative"])
    for relative, expected in payload["members"].items():
        target = contained(runtime, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(contained(package, relative), target)
        if digest_file(target) != expected:
            raise RuntimeError("Staged payload differs from extracted r30 package")
    config_path = contained(project, ".codex/hooks.json")
    atomic_json(config_path, preview["after"])
    configuration = tomllib.loads(Path(r"C:/Users/USER\.codex\config.toml").read_text(encoding="utf8"))
    unrelated = {key: value for key, value in configuration.get("hooks", {}).get("state", {}).items()
                 if str(project).casefold() not in key.casefold()}
    atomic_json(plan_path, {"preview": preview, "config_sha256": digest_file(config_path), "payload": payload,
        "source_lock_hash": digest_record(verify_source_lock(ROOT)), "source_revision": "30",
        "context_sha256": digest_file(context), "unrelated_native_hook_state_hash": digest_record(unrelated),
        "provider": "refused-loopback-no-successful-inference", "authority": str(RUN / "native-grant.json"),
        "normal_trust": "required-not-bypassed", "production_apply": "not-called"})
    executable = json.loads((RUN / "host-inventory.json").read_text(encoding="utf8"))["hosts"]["codex"]["executable"]
    state = project / "prompt-admission-state"
    state.mkdir(exist_ok=True)
    tui = [executable, *options(), "-C", str(project), "-s", "read-only", "-a", "on-request", "--no-alt-screen",
           "-c", "sqlite_home=" + json.dumps(str(state / "sqlite")), "-c", "log_dir=" + json.dumps(str(state / "logs"))]
    atomic_json(project / "prompt-admission-tui-argv.json", tui)
    print(json.dumps({"status": "prepared", "project": str(project), "event": "UserPromptSubmit", "inference_endpoint": "refused-loopback"}))


def tui(attempt):
    original = json.loads((project / "prompt-admission-tui-argv.json").read_text(encoding="utf8"))
    argv = [original[0], *options(), *original[original.index("-C"):]]
    atomic_json(project / f"prompt-admission-tui-argv-attempt-{attempt:02d}.json", argv)
    record_path = project / f"prompt-admission-tui-process-attempt-{attempt:02d}.json"
    if record_path.exists():
        raise RuntimeError("Preserve existing TUI process receipt")
    record = {"status": "starting", "argv": argv, "cwd": str(project), "port": None,
              "started_at": datetime.now(timezone.utc).isoformat(), "owned_by": str(RUN)}
    process = subprocess.Popen(argv, cwd=project, env=environment())
    record.update(pid=process.pid, status="running")
    atomic_json(record_path, record)
    try:
        result = process.wait()
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        record.update(status="ended", exit_code=process.returncode,
                      ended_at=datetime.now(timezone.utc).isoformat(), process_exited=process.poll() is not None)
        atomic_json(record_path, record)
    sys.exit(result)


def probe(action, attempt):
    spec = importlib.util.spec_from_file_location("native_qualification", RUN / "qualification-run.py")
    qualification = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(qualification)
    installed = qualification.installed_commands()
    qualification.installed_commands = lambda: {**installed, "codex": [*installed["codex"], *options()]}
    receipt_directory = project / ".nckh-state/hooks/events/codex"
    prior_receipts = {path.name for path in receipt_directory.glob("*.json")}
    child_environment = environment()
    previous = dict(os.environ)
    try:
        os.environ.clear()
        os.environ.update(child_environment)
        rpc = qualification.CodexRPC(f"codex-prompt-admission-{action}-attempt-{attempt:02d}", project, isolated=True)
    finally:
        os.environ.clear()
        os.environ.update(previous)
    try:
        initialized = rpc.request("initialize", {"clientInfo": {"name": "nckh-prompt-admission", "title": "NCKH prompt admission", "version": "r30"},
                                                 "capabilities": {"experimentalApi": True}})
        rpc.process.stdin.write(b'{"method":"initialized","params":{}}\n')
        rpc.process.stdin.flush()
        listing = rpc.request("hooks/list", {"cwds": [str(project)]})
        selected = [row for entry in listing.get("result", {}).get("data", []) for row in entry.get("hooks", [])
                    if row.get("sourcePath", "").casefold() == str(project / ".codex/hooks.json").casefold()]
        global_hooks = [row for entry in listing.get("result", {}).get("data", []) for row in entry.get("hooks", [])
                        if row.get("sourcePath", "").casefold() == str(Path(r"C:/Users/USER\.codex\hooks.json")).casefold()]
        effective = rpc.request("config/read", {"includeLayers": False})
        mcp = effective.get("result", {}).get("config", {}).get("mcp_servers", {})
        record = {"initialization_error": initialized.get("error"), "hooks": selected, "provider": "refused-loopback",
                  "source_lock_hash": json.loads(plan_path.read_text(encoding="utf8"))["source_lock_hash"],
                  "context_sha256": digest_file(project / "prompt-admission-context.json"),
                  "global_hooks": [{key: row.get(key) for key in ("id", "enabled", "trustStatus", "currentHash")} for row in global_hooks],
                  "mcp_enabled": {name: settings.get("enabled", True) for name, settings in mcp.items()},
                  "config_read_error": effective.get("error"), "hooks_list_error": listing.get("error")}
        if action.startswith("observe"):
            if listing.get("error") or effective.get("error") or any(row.get("enabled") for row in global_hooks) or any(record["mcp_enabled"].values()):
                raise RuntimeError("Invocation must confirm global hooks and MCP servers are disabled")
            if len(selected) != 1 or selected[0]["trustStatus"] != "trusted" or not selected[0]["enabled"]:
                raise RuntimeError("Exact project UserPromptSubmit must be reviewed and trusted in normal host UI")
            thread = rpc.request("thread/start", {"cwd": str(project), "ephemeral": True, "sandbox": "read-only", "approvalPolicy": "on-request"})
            identifier = thread.get("result", {}).get("thread", {}).get("id")
            if not identifier:
                raise RuntimeError("Native thread/start did not return a thread")
            turn = rpc.request("turn/start", {"threadId": identifier,
                "input": [{"type": "text", "text": "Native prompt admission probe. Do not run tools."}]})
            notifications = rpc.notifications(seconds=8)
            record.update(thread=thread, turn=turn, notifications=notifications,
                          policy_receipts=[json.loads(path.read_text(encoding="utf8")) for path in
                                           receipt_directory.glob("*.json")],
                          new_policy_receipts=[json.loads(path.read_text(encoding="utf8")) for path in
                                               receipt_directory.glob("*.json") if path.name not in prior_receipts])
        qualification.save(project / f"prompt-admission-{action}-attempt-{attempt:02d}.json", record)
        print(json.dumps({"action": action, "hooks": [{key: row.get(key) for key in
                          ("eventName", "enabled", "trustStatus", "currentHash")} for row in selected],
                          "policy_receipts": len(record.get("policy_receipts", [])), "initialization_error": record["initialization_error"]}))
    finally:
        rpc.close()


def observe_allow(attempt):
    context = project / "prompt-admission-context.json"
    original = context.read_bytes()
    registration = json.loads(plan_path.read_text(encoding="utf8"))
    if digest_file(context) != registration["context_sha256"]:
        raise RuntimeError("Owned block context drifted; preserve it")
    preimage = project / "prompt-admission-context-block-preimage.json"
    if preimage.exists():
        raise RuntimeError("Preserve existing context preimage")
    preimage.write_bytes(original)
    atomic_json(context, {"schema_version": 1, "task_id": "native-codex-prompt-advisory-only", "references": []})
    expected = digest_file(context)
    try:
        probe("observe-allow", attempt)
    finally:
        if digest_file(context) != expected:
            raise RuntimeError("Context changed during the native probe; preserve for review")
        context.write_bytes(original)


def cleanup():
    receipt = project / "prompt-admission-cleanup.json"
    if receipt.exists():
        raise RuntimeError("Preserve existing cleanup receipt")
    registration = json.loads(plan_path.read_text(encoding="utf8"))
    metadata = json.loads((project / "prompt-admission-metadata-attempt-04.json").read_text(encoding="utf8"))
    if len(metadata["hooks"]) != 1 or metadata["hooks"][0]["enabled"]:
        raise RuntimeError("Normal native UI must disable the exact project hook before cleanup")
    configuration = tomllib.loads(Path(r"C:/Users/USER\.codex\config.toml").read_text(encoding="utf8"))
    unrelated = {key: value for key, value in configuration.get("hooks", {}).get("state", {}).items()
                 if str(project).casefold() not in key.casefold()}
    if digest_record(unrelated) != registration["unrelated_native_hook_state_hash"]:
        raise RuntimeError("Unrelated hook state changed; preserve for review")
    no_links(project)
    if not project.resolve().is_relative_to(RUN.resolve()):
        raise RuntimeError("Cleanup escaped its owned run")
    config = contained(project, ".codex/hooks.json")
    if digest_file(config) != registration["config_sha256"]:
        raise RuntimeError("Owned config changed; preserve it")
    payload = registration["payload"]
    runtime = contained(project, registration["preview"]["runtime_relative"])
    members = payload["members"]
    if {path.relative_to(runtime).as_posix() for path in runtime.rglob("*") if path.is_file()} != set(members):
        raise RuntimeError("Staged payload has unknown or missing files; preserve it")
    for relative, expected in members.items():
        if digest_file(contained(runtime, relative)) != expected:
            raise RuntimeError("Staged payload drifted; preserve it")
    record = {"status": "preflight-passed", "started_at": datetime.now(timezone.utc).isoformat(),
              "project": str(project), "runtime": str(runtime), "config_sha256": registration["config_sha256"],
              "source_lock_hash": digest_record(verify_source_lock(ROOT)), "unrelated_hook_state_unchanged": True,
              "definition_trust_residual": "three-project-test-hashes-trusted-but-disabled",
              "project_trust_residual": "may-remain-in-normal-host-store", "removed_members": [],
              "config_removed": False, "global_direct_write": False}
    atomic_json(receipt, record)
    config.unlink()
    record["config_removed"] = True
    atomic_json(receipt, record)
    for relative in members:
        contained(runtime, relative).unlink()
        record["removed_members"].append(relative)
        atomic_json(receipt, record)
    for directory in sorted((path for path in runtime.rglob("*") if path.is_dir()), key=lambda path: len(path.parts), reverse=True):
        no_links(directory)
        if not any(directory.iterdir()):
            directory.rmdir()
    if not any(runtime.iterdir()):
        runtime.rmdir()
    record.update(status="pass", ended_at=datetime.now(timezone.utc).isoformat(),
                  context_preserved=True, receipts_preserved=True, config_absent=not config.exists(), runtime_absent=not runtime.exists())
    atomic_json(receipt, record)
    print(json.dumps({"status": record["status"], "config_removed": record["config_removed"],
                      "payload_members_removed": len(record["removed_members"]), "unrelated_hook_state_unchanged": True}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("prepare", "tui", "metadata", "observe", "observe-allow", "cleanup"))
    parser.add_argument("--attempt", type=int, default=2)
    arguments = parser.parse_args()
    action = arguments.action
    if action == "prepare":
        prepare()
    elif action == "tui":
        tui(arguments.attempt)
    elif action == "observe-allow":
        observe_allow(arguments.attempt)
    elif action == "cleanup":
        cleanup()
    else:
        probe(action, arguments.attempt)


if __name__ == "__main__":
    main()
