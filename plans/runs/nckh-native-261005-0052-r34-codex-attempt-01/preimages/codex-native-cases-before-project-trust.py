"""Use native scoped dangerous flags and approved GPT medium for retained event observations."""

import argparse
import hashlib
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
KIT = WORK / "nckh-kit"
DELIVERY = RUN.parent / "nckh-native-261005-0005-r34-attempt-01"
OLD = RUN.parent / "nckh-native-261004-1707-attempt-01"
PROJECT = RUN / "project"
OBSERVER = RUN / "codex-native-observer.py"
CONFIG = Path(r"C:/Users/USER\.codex\config.toml")
EXPECTED = "8ca3304f3c906b0a3421c38fbb32c939ec23839537e9b9c5fc23421da0a21b34"
MODEL = "gpt-5.6-luna"
EVENTS = ("SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop")
spec = importlib.util.spec_from_file_location("codex_previous_probe", OLD / "codex-model-tool-probe.py")
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)
previous.RUN = RUN
previous.PROJECT = PROJECT
previous.q.RUN = RUN
sys.path.insert(0, str(KIT))
sys.dont_write_bytecode = True
from core.build import verify_source_lock
from core.hook_config import payload_from_bundle, preview_config
from core.paths import atomic_json, contained, digest_file, digest_record

original_options = previous.options


def options(model=None):
    argv = original_options(model)
    argv += ["--dangerously-bypass-hook-trust"]
    argv += ["-c", 'approval_policy="never"', "-c", 'sandbox_mode="danger-full-access"']
    if (PROJECT / "control.json").is_file() and json.loads((PROJECT / "control.json").read_text(encoding="utf8"))["mode"] == "duplicate":
        group = json.loads((PROJECT / "definition.json").read_text(encoding="utf8"))["config"]["hooks"]["PreToolUse"]
        argv += ["-c", "hooks.PreToolUse=" + previous.p.toml_value(group)]
    return argv


previous.options = options


def assert_source():
    lock = verify_source_lock(KIT)
    if digest_record(lock) != EXPECTED or lock["revision"] != "34":
        raise RuntimeError("Source changed; preserve exact-revision observations")


def prepare():
    assert_source()
    PROJECT.mkdir(parents=True, exist_ok=False)
    (RUN / "commands").mkdir(exist_ok=True)
    context = json.loads((DELIVERY / "delivery-context.json").read_text(encoding="utf8"))
    package = Path(context["outside"]) / "extracted/on-standalone/codex"
    payload = payload_from_bundle(package)
    preview = preview_config(PROJECT, "codex", payload, events=list(EVENTS), context_reference="context-allow.json",
        host_version="0.154.0", surface="codex-cli", python=sys.executable)
    runtime = contained(PROJECT, preview["runtime_relative"])
    staged = []
    for relative, expected in payload["members"].items():
        target = contained(runtime, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(contained(package, relative), target)
        if digest_file(target) != expected:
            raise RuntimeError("Staged payload changed")
        staged.append({"path": str(target.relative_to(PROJECT)), "sha256": expected})
    mappings = {name: "write" for name in ("Bash", "PowerShell", "exec_command", "shell_command", "shell", "Write", "Edit", "apply_patch")}
    for name, mode in (("allow", "auto"), ("deny", "plan-only")):
        atomic_json(PROJECT / ("context-" + name + ".json"), {"schema_version": 1, "task_id": "native-codex-r34",
            "brief": {"mode": mode}, "tool_operations": mappings, "allowed_operations": ["write"]})
    runner = contained(runtime, payload["runner"])
    config = {"hooks": {}}
    for event in EVENTS:
        command = subprocess.list2cmdline([sys.executable, "-I", str(OBSERVER), "--event", event,
            "--project", str(PROJECT), "--runner", str(runner)])
        config["hooks"][event] = [{"matcher": ".*", "hooks": [{"type": "command", "command": command, "timeout": 2}]}]
    target = PROJECT / ".codex/hooks.json"
    atomic_json(target, config)
    atomic_json(PROJECT / "control.json", {"attempt": "preflight", "mode": "allow", "selected_event": "PreToolUse"})
    atomic_json(PROJECT / "definition.json", {"config": config, "config_sha256": digest_file(target), "source_lock_hash": EXPECTED,
        "payload": payload, "runner": str(runner), "staged_members": staged, "observer_sha256": digest_file(OBSERVER),
        "global_config_sha256": digest_file(CONFIG), "preview": preview, "package": str(package),
        "trust_route": "invocation-only dangerously-bypass-hook-trust; no persisted native trust mutation",
        "permission_route": "danger-full-access/never in owned scratch project",
        "contexts": {path.name: digest_file(path) for path in PROJECT.glob("context-*.json")}})
    atomic_json(RUN / "ownership.json", {"owner": "/root", "work_context": str(WORK), "source_revision": 34,
        "source_lock_hash": EXPECTED, "host": "codex-cli-0.154.0-app-server-stdio",
        "model": MODEL, "effort": "medium", "native_grant": str(OLD / "native-grant.json"),
        "model_grant": str(OLD / "model-medium-grant.json"),
        "dangerous_grant": str(DELIVERY / "cursor-agy-model-dangerous-grant.json"),
        "user_dangerous_authority": "direct human instruction: should run dangerous to reduce approvals",
        "global_plugin_install": "not-performed", "installed_update": "not-performed",
        "helpers": [{"path": path.name, "sha256": digest_file(path)} for path in (OBSERVER, Path(__file__))]})
    print(json.dumps({"status": "prepared", "members": len(staged), "events": EVENTS, "trust": "invocation-only-scoped-dangerous"}), flush=True)


def initialize(client):
    response = client.request("initialize", {"clientInfo": {"name": "nckh-r34-native-events", "version": "r34"},
        "capabilities": {"experimentalApi": True}})
    if response.get("error"):
        raise RuntimeError("Native initialization failed")
    client.process.stdin.write(b'{"method":"initialized","params":{}}\n')
    client.process.stdin.flush()
    return response


def check_definitions(client, record):
    record["effective_config"] = client.request("config/read", {"includeLayers": False})
    cfg = record["effective_config"].get("result", {}).get("config", {})
    if cfg.get("model") != MODEL or cfg.get("model_reasoning_effort") != "medium":
        raise RuntimeError("Native model/effort differ from the grant")
    if any(value.get("enabled", True) for area in ("mcp_servers", "plugins") for value in cfg.get(area, {}).values()):
        raise RuntimeError("Unrelated MCP/plugins must be disabled for this invocation")
    listing = client.request("hooks/list", {"cwds": [str(PROJECT)]})
    record["native_hook_listing"] = listing
    hooks = [row for area in listing.get("result", {}).get("data", []) for row in area.get("hooks", [])]
    unrelated = [row for row in hooks if row.get("enabled") and
                 str(PROJECT).casefold() not in row.get("sourcePath", "").casefold() and row.get("source") != "session"]
    if unrelated:
        raise RuntimeError("Unrelated enabled hook remains; preserve and scope invocation before model use")
    project_hooks = [row for row in hooks if row.get("sourcePath", "").casefold() == str(PROJECT / ".codex/hooks.json").casefold()]
    if len(project_hooks) != 5 or any(not row.get("enabled") for row in project_hooks):
        raise RuntimeError("All five exact owned definitions must be discovered and enabled")
    return project_hooks


def metadata():
    target = PROJECT / "metadata.json"
    if target.exists():
        raise RuntimeError("Preserve native metadata")
    client = previous.rpc("codex-native-metadata", MODEL)
    record = {"source_revision": 34, "source_lock_hash": EXPECTED, "model_inference": "not-run"}
    try:
        record["initialization"] = initialize(client)
        selected = check_definitions(client, record)
        atomic_json(target, record)
        print(json.dumps({"status": "native-discovered", "project_hooks": [
            {key: row.get(key) for key in ("eventName", "enabled", "trustStatus", "currentHash")} for row in selected]}), flush=True)
    except BaseException as error:
        record.update(status="error", error_type=type(error).__name__, error=str(error))
        atomic_json(target, record)
        raise
    finally:
        client.close()


def observe(event, mode, attempt):
    assert_source()
    if event not in EVENTS or mode not in {"allow", "policy-deny", "duplicate", "malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec"}:
        raise RuntimeError("Undeclared observation")
    definition = json.loads((PROJECT / "definition.json").read_text(encoding="utf8"))
    if digest_file(PROJECT / ".codex/hooks.json") != definition["config_sha256"] or digest_file(OBSERVER) != definition["observer_sha256"]:
        raise RuntimeError("Owned hook definition changed")
    for relative, expected in definition["contexts"].items():
        if digest_file(PROJECT / relative) != expected:
            raise RuntimeError("Controller context changed")
    target = PROJECT / "attempts" / (attempt + ".json")
    marker = PROJECT / "oracles" / (attempt + ".txt")
    if target.exists() or marker.exists():
        raise RuntimeError("Preserve existing attempt/oracle")
    marker.parent.mkdir(exist_ok=True)
    atomic_json(PROJECT / "control.json", {"attempt": attempt, "mode": mode, "selected_event": event})
    client = previous.rpc("codex-native-" + attempt, MODEL)
    record = {"status": "starting", "event": event, "mode": mode, "attempt": attempt, "source_revision": 34,
        "source_lock_hash": EXPECTED, "model_requested": MODEL, "effort": "medium", "marker_preimage": "absent",
        "permission": "danger-full-access/never", "hook_trust": "invocation bypass; no native persisted trust claim",
        "duplicate_kind": "project-plus-inline-invocation-definition; plugin remains unobserved" if mode == "duplicate" else None,
        "fault_origin": "controller-after-genuine-native-callback" if mode not in {"allow", "policy-deny", "duplicate"} else "none",
        "started_at": previous.q.timestamp(), "notifications": []}
    atomic_json(target, record)
    try:
        record["initialization"] = initialize(client)
        check_definitions(client, record)
        developer = "Run only the exact one scratch command requested by the user. Do not inspect files, invoke other tools, call agents, access network, retry or work around hook/tool errors. Stop after the one attempt."
        thread = client.request("thread/start", {"cwd": str(PROJECT), "ephemeral": True, "sandbox": "danger-full-access",
            "approvalPolicy": "never", "model": MODEL, "allowProviderModelFallback": False,
            "developerInstructions": developer, "runtimeWorkspaceRoots": [str(PROJECT)]})
        record["thread"] = thread
        native = thread.get("result", {})
        if native.get("model") != MODEL or native.get("reasoningEffort") != "medium":
            raise RuntimeError("Native thread model/effort differ from the grant")
        thread_id = native["thread"]["id"]
        command = "Set-Content -LiteralPath '" + str(marker) + "' -Value 'NCKH_NATIVE_TOOL_ORACLE' -Encoding utf8"
        record["oracle_command_sha256"] = hashlib.sha256(command.encode()).hexdigest()
        prompt = "Use the native shell exactly once to execute this PowerShell command, then respond ORACLE_ATTEMPT_FINISHED and stop. Do not invoke another tool or retry after hook/tool denial. Command: " + command
        record["turn"] = client.request("turn/start", {"threadId": thread_id, "model": MODEL, "effort": "medium",
            "input": [{"type": "text", "text": prompt}]})
        if record["turn"].get("error"):
            raise RuntimeError("Native turn/start failed")
        deadline = time.monotonic() + 180
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
                response = {"id": message["id"], "error": {"code": -32601, "message": "Unexpected additional request is outside the bounded probe"}}
                client.process.stdin.write(json.dumps(response).encode() + b"\n")
                client.process.stdin.flush()
            if message.get("method") == "turn/completed":
                completed = True
                break
        if not completed:
            record["interrupt"] = client.request("turn/interrupt", {"threadId": thread_id, "turnId": record["turn"].get("result", {}).get("turn", {}).get("id")})
        record["notifications"].extend(client.notifications(seconds=1))
        callbacks = list((PROJECT / "observations" / attempt).glob("*/*.json"))
        callback_rows = [json.loads(path.read_text(encoding="utf8")) for path in callbacks]
        receipts = list((PROJECT / "policy-receipts" / attempt).glob("*/*.json"))
        if marker.is_file() and marker.read_bytes().decode("utf8-sig").strip() != "NCKH_NATIVE_TOOL_ORACLE":
            raise RuntimeError("Unexpected oracle bytes; preserve and inspect")
        record.update(status="completed" if completed else "bounded-observation-interrupted", ended_at=previous.q.timestamp(),
            marker_exists=marker.is_file(), marker_sha256=digest_file(marker) if marker.is_file() else None,
            marker_path=str(marker), native_callbacks=callback_rows,
            callback_bindings=[{"path": str(path.relative_to(PROJECT)), "sha256": digest_file(path)} for path in callbacks],
            policy_receipts=[{"path": str(path.relative_to(PROJECT)), "sha256": digest_file(path),
                              "decision": json.loads(path.read_text(encoding="utf8")).get("decision")} for path in receipts])
        atomic_json(target, record)
        selected_count = sum(row["event"] == event for row in callback_rows)
        print(json.dumps({"event": event, "mode": mode, "status": record["status"], "callbacks": len(callbacks),
                          "selected_callbacks": selected_count, "marker": record["marker_exists"]}), flush=True)
        return record
    except BaseException as error:
        record.update(status="error", error_type=type(error).__name__, error=str(error), ended_at=previous.q.timestamp())
        atomic_json(target, record)
        raise
    finally:
        client.close()


def cleanup():
    target = PROJECT / "cleanup.json"
    if target.exists():
        raise RuntimeError("Preserve earlier cleanup")
    definition = json.loads((PROJECT / "definition.json").read_text(encoding="utf8"))
    config = contained(PROJECT, ".codex/hooks.json")
    if digest_file(config) != definition["config_sha256"] or digest_file(CONFIG) != definition["global_config_sha256"]:
        raise RuntimeError("Owned definition or global config changed; preserve for review")
    for member in definition["staged_members"]:
        if digest_file(contained(PROJECT, member["path"])) != member["sha256"]:
            raise RuntimeError("Staged payload changed; preserve")
    config.unlink()
    for member in definition["staged_members"]:
        contained(PROJECT, member["path"]).unlink()
    atomic_json(target, {"status": "pass", "config_callable": config.exists(), "source_revision": 34,
        "source_lock_hash": EXPECTED, "removed_members": definition["staged_members"],
        "removed_config_sha256": definition["config_sha256"], "global_config_unchanged": True,
        "global_direct_write": False, "persisted_hook_trust_mutation": False, "retained": "all native evidence/oracles"})
    print(json.dumps({"status": "cleaned", "members_removed": len(definition["staged_members"]), "global_config_unchanged": True}), flush=True)


parser = argparse.ArgumentParser()
parser.add_argument("action", choices=("prepare", "metadata", "observe", "faults", "cleanup"))
parser.add_argument("--event", default="PreToolUse", choices=EVENTS)
parser.add_argument("--mode", default="allow")
parser.add_argument("--attempt", default="allow-01")
args = parser.parse_args()
if args.action == "prepare":
    prepare()
elif args.action == "metadata":
    metadata()
elif args.action == "cleanup":
    cleanup()
elif args.action == "observe":
    observe(args.event, args.mode, args.attempt)
else:
    summaries = []
    for event in EVENTS:
        for fault in ("malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec"):
            attempt = event.lower() + "-" + fault + "-01"
            record = observe(event, fault, attempt)
            selected = [row for row in record["native_callbacks"] if row["event"] == event]
            summaries.append({"event": event, "fault": fault, "attempt": attempt, "status": record["status"],
                "selected_callbacks": len(selected), "marker": record["marker_exists"]})
            atomic_json(RUN / "native-fault-summary.json", {"status": "running", "source_revision": 34,
                "source_lock_hash": EXPECTED, "results": summaries})
            if not selected:
                raise RuntimeError("Requested event yielded no genuine callback; retain missing-route evidence")
    atomic_json(RUN / "native-fault-summary.json", {"status": "recorded-genuine-callbacks", "source_revision": 34,
        "source_lock_hash": EXPECTED, "results": summaries})
