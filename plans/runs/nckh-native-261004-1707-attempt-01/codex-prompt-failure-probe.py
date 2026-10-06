"""Run declared native hook faults with inference refused at loopback."""

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
PROJECT = RUN / "projects/codex"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from core.build import verify_source_lock
from core.hook_config import payload_from_bundle, preview_config
from core.paths import atomic_json, contained, digest_file, digest_record, no_links


def module(name, path):
    specification = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(result)
    return result


base = module("prompt_base", RUN / "codex-prompt-admission.py")
qualification = module("native_qualification_failure", RUN / "qualification-run.py")
COMMANDS = qualification.installed_commands()
qualification.installed_commands = lambda: {**COMMANDS, "codex": [*COMMANDS["codex"], *base.options()]}
REGISTRATION = PROJECT / "failure-probe-registration.json"
MODES = ("policy-deny", "advisory", "malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec")


def read(path):
    return json.loads(path.read_text(encoding="utf8"))


def prepare():
    config = contained(PROJECT, ".codex/hooks.json")
    if REGISTRATION.exists() or config.exists():
        raise RuntimeError("Preserve existing registration/config")
    package = Path(read(RUN / "delivery-context.json")["outside"]) / "extracted/on-standalone/codex"
    payload = payload_from_bundle(package)
    preview = preview_config(PROJECT, "codex", payload, events=["UserPromptSubmit"],
        context_reference="prompt-admission-context.json", host_version="0.154.0", surface="codex-cli", python=sys.executable)
    runtime = contained(PROJECT, preview["runtime_relative"])
    if runtime.exists():
        raise RuntimeError("Preserve existing staged payload")
    for relative, expected in payload["members"].items():
        target = contained(runtime, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(contained(package, relative), target)
        if digest_file(target) != expected:
            raise RuntimeError("Payload differs from extracted r30")
    observer = RUN / "codex-prompt-failure-observer.py"
    command = subprocess.list2cmdline([sys.executable, "-I", str(observer), "--project", str(PROJECT),
                                      "--runner", str(contained(runtime, payload["runner"]))])
    configuration = {"hooks": {"UserPromptSubmit": [{"matcher": ".*", "hooks": [{"type": "command", "command": command, "timeout": 2}]}]}}
    atomic_json(config, configuration)
    for name, references in (("deny", [{} for _ in range(33)]), ("advisory", [])):
        context = PROJECT / f"failure-context-{name}.json"
        if context.exists():
            raise RuntimeError("Preserve existing fault context")
        atomic_json(context, {"schema_version": 1, "task_id": "native-codex-failure-probe", "references": references})
    control = PROJECT / "failure-probe-control.json"
    if control.exists():
        raise RuntimeError("Preserve existing control")
    atomic_json(control, {"mode": "policy-deny"})
    native_configuration = tomllib.loads(Path(r"C:/Users/USER\.codex\config.toml").read_text(encoding="utf8"))
    unrelated = {key: value for key, value in native_configuration.get("hooks", {}).get("state", {}).items()
                 if str(PROJECT).casefold() not in key.casefold()}
    atomic_json(REGISTRATION, {"source_lock_hash": digest_record(verify_source_lock(ROOT)), "payload": payload,
        "runtime_relative": preview["runtime_relative"], "config_sha256": digest_file(config),
        "observer_sha256": digest_file(observer), "unrelated_hook_state_hash": digest_record(unrelated),
        "authority": str(RUN / "native-grant.json"), "provider": "refused-loopback", "normal_trust": "required",
        "contexts": {name: digest_file(PROJECT / f"failure-context-{name}.json") for name in ("deny", "advisory")},
        "fault_injection": "declared-test-only-native-input-not-authored-host-output", "modes": MODES})
    print(json.dumps({"status": "prepared", "event": "UserPromptSubmit", "modes": list(MODES), "normal_trust": "required"}))


def rpc(name):
    child_environment = base.environment()
    previous = dict(os.environ)
    try:
        os.environ.clear()
        os.environ.update(child_environment)
        return qualification.CodexRPC("codex-prompt-failure-" + name, PROJECT, isolated=True)
    finally:
        os.environ.clear()
        os.environ.update(previous)


def inspect(client):
    initialization = client.request("initialize", {"clientInfo": {"name": "nckh-failure-probe", "version": "r30"},
                                                  "capabilities": {"experimentalApi": True}})
    client.process.stdin.write(b'{"method":"initialized","params":{}}\n')
    client.process.stdin.flush()
    listing = client.request("hooks/list", {"cwds": [str(PROJECT)]})
    hooks = [row for entry in listing.get("result", {}).get("data", []) for row in entry.get("hooks", [])]
    selected = [row for row in hooks if row.get("sourcePath", "").casefold() == str(PROJECT / ".codex/hooks.json").casefold()]
    global_hooks = [row for row in hooks if row.get("sourcePath", "").casefold() == str(Path(r"C:/Users/USER\.codex\hooks.json")).casefold()]
    effective = client.request("config/read", {"includeLayers": False})
    mcp = effective.get("result", {}).get("config", {}).get("mcp_servers", {})
    return {"initialization_error": initialization.get("error"), "hooks_list_error": listing.get("error"),
            "config_read_error": effective.get("error"), "hooks": selected,
            "global_hooks": [{key: row.get(key) for key in ("enabled", "trustStatus", "currentHash")} for row in global_hooks],
            "mcp_enabled": {name: settings.get("enabled", True) for name, settings in mcp.items()}}


def metadata(attempt):
    target = PROJECT / f"failure-probe-metadata-{attempt:02d}.json"
    if target.exists():
        raise RuntimeError("Preserve prior metadata")
    client = rpc(f"metadata-{attempt:02d}")
    try:
        record = inspect(client)
        atomic_json(target, record)
        print(json.dumps({"action": "metadata", "hooks": [{key: row.get(key) for key in
              ("eventName", "enabled", "trustStatus", "currentHash", "timeoutSec")} for row in record["hooks"]]}))
    finally:
        client.close()


def observe(mode):
    target = PROJECT / f"failure-probe-{mode}.json"
    if target.exists():
        raise RuntimeError("Preserve prior fault observation")
    registration = read(REGISTRATION)
    if digest_file(PROJECT / ".codex/hooks.json") != registration["config_sha256"] or digest_file(RUN / "codex-prompt-failure-observer.py") != registration["observer_sha256"]:
        raise RuntimeError("Fault definition/observer drifted")
    atomic_json(PROJECT / "failure-probe-control.json", {"mode": mode})
    client = rpc(mode)
    try:
        record = inspect(client)
        if any(record[key] for key in ("initialization_error", "hooks_list_error", "config_read_error")):
            raise RuntimeError("Native metadata error")
        if len(record["hooks"]) != 1 or record["hooks"][0]["trustStatus"] != "trusted" or not record["hooks"][0]["enabled"]:
            raise RuntimeError("Exact observer definition must be trusted/enabled in normal UI")
        if any(row["enabled"] for row in record["global_hooks"]) or any(record["mcp_enabled"].values()):
            raise RuntimeError("User hooks/configured MCP must be disabled by invocation")
        thread = client.request("thread/start", {"cwd": str(PROJECT), "ephemeral": True, "sandbox": "read-only", "approvalPolicy": "on-request"})
        identifier = thread.get("result", {}).get("thread", {}).get("id")
        if not identifier:
            raise RuntimeError("Native thread was not created")
        turn = client.request("turn/start", {"threadId": identifier,
            "input": [{"type": "text", "text": "Declared native prompt hook fault probe. Do not run tools."}]})
        notifications = client.notifications(seconds=10)
        record.update(mode=mode, source_lock_hash=registration["source_lock_hash"], thread=thread, turn=turn,
                      notifications=notifications, observer_sha256=registration["observer_sha256"],
                      observations=[read(path) for path in (PROJECT / "failure-observations" / mode).glob("*.json")],
                      policy_receipts=[read(path) for path in (PROJECT / "failure-policy-receipts" / mode).glob("*.json")],
                      inference_endpoint="refused-loopback", fault_conditions="declared-injection-after-native-callback")
        atomic_json(target, record)
        hook_runs = [row["params"]["run"] for row in notifications if row.get("method") == "hook/completed"]
        print(json.dumps({"mode": mode, "callbacks": len(record["observations"]), "hook_statuses": [row["status"] for row in hook_runs],
                          "policy_receipts": len(record["policy_receipts"])}), flush=True)
    finally:
        client.close()


def cleanup():
    target = PROJECT / "failure-probe-cleanup.json"
    if target.exists():
        raise RuntimeError("Preserve prior cleanup")
    registration = read(REGISTRATION)
    metadata_record = read(PROJECT / "failure-probe-metadata-03.json")
    if len(metadata_record["hooks"]) != 1 or metadata_record["hooks"][0]["enabled"]:
        raise RuntimeError("Exact observer hook must be disabled in normal native UI")
    native_configuration = tomllib.loads(Path(r"C:/Users/USER\.codex\config.toml").read_text(encoding="utf8"))
    unrelated = {key: value for key, value in native_configuration.get("hooks", {}).get("state", {}).items()
                 if str(PROJECT).casefold() not in key.casefold()}
    if digest_record(unrelated) != registration["unrelated_hook_state_hash"]:
        raise RuntimeError("Unrelated hook state drifted; preserve for review")
    no_links(PROJECT)
    if not PROJECT.resolve().is_relative_to(RUN.resolve()):
        raise RuntimeError("Cleanup escaped the owned run")
    config = contained(PROJECT, ".codex/hooks.json")
    runtime = contained(PROJECT, registration["runtime_relative"])
    payload = registration["payload"]
    if digest_file(config) != registration["config_sha256"]:
        raise RuntimeError("Config changed; preserve it")
    if {path.relative_to(runtime).as_posix() for path in runtime.rglob("*") if path.is_file()} != set(payload["members"]):
        raise RuntimeError("Payload has unknown or missing members; preserve it")
    for relative, expected in payload["members"].items():
        if digest_file(contained(runtime, relative)) != expected:
            raise RuntimeError("Payload drifted; preserve it")
    owned_state = {key: value for key, value in native_configuration.get("hooks", {}).get("state", {}).items()
                   if str(PROJECT).casefold() in key.casefold()}
    if any(value.get("enabled", True) for value in owned_state.values()):
        raise RuntimeError("A project test hook remains enabled")
    record = {"status": "preflight-passed", "started_at": datetime.now(timezone.utc).isoformat(),
              "project": str(PROJECT), "runtime": str(runtime), "removed_members": [], "config_removed": False,
              "config_sha256": registration["config_sha256"], "unrelated_hook_state_unchanged": True,
              "native_owned_state_residual": owned_state, "global_direct_write": False,
              "source_lock_hash": digest_record(verify_source_lock(ROOT))}
    atomic_json(target, record)
    config.unlink()
    record["config_removed"] = True
    atomic_json(target, record)
    for relative in payload["members"]:
        contained(runtime, relative).unlink()
        record["removed_members"].append(relative)
        atomic_json(target, record)
    for directory in sorted((path for path in runtime.rglob("*") if path.is_dir()), key=lambda path: len(path.parts), reverse=True):
        no_links(directory)
        if not any(directory.iterdir()):
            directory.rmdir()
    if not any(runtime.iterdir()):
        runtime.rmdir()
    record.update(status="pass", ended_at=datetime.now(timezone.utc).isoformat(),
                  config_absent=not config.exists(), runtime_absent=not runtime.exists(),
                  contexts_control_observations_and_receipts_preserved=True)
    atomic_json(target, record)
    print(json.dumps({"status": "pass", "config_removed": True, "payload_members_removed": len(record["removed_members"]),
                      "unrelated_hook_state_unchanged": True, "disabled_project_state_keys": len(owned_state)}))


parser = argparse.ArgumentParser()
parser.add_argument("action", choices=("prepare", "metadata", "observe", "observe-all", "cleanup"))
parser.add_argument("--attempt", type=int, default=1)
parser.add_argument("--mode", choices=MODES)
arguments = parser.parse_args()
if arguments.action == "prepare":
    prepare()
elif arguments.action == "metadata":
    metadata(arguments.attempt)
elif arguments.action == "observe-all":
    for mode in MODES:
        observe(mode)
elif arguments.action == "cleanup":
    cleanup()
else:
    if not arguments.mode:
        parser.error("observe requires --mode")
    observe(arguments.mode)
