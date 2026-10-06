"""Capture real file-tool effects and permission responses; never invent outcomes."""

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = WORK / "plans/runs/nckh-native-261005-0128-r34-cursor-events-attempt-02/projects/main"
EVIDENCE = PROJECT / ".nckh-native-r35-cursor-write-faults-02"
DELIVERY = WORK / "plans/runs/nckh-native-261005-0710-r35-attempt-01"
OBSERVER = RUN / "cursor-file-observer.py"
CONFIG = PROJECT / ".cursor/hooks.json"
MODEL = "grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]"
EXPECTED = "4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255"
EVENTS = ("sessionStart", "beforeSubmitPrompt", "preToolUse", "postToolUse", "stop")
qspec = importlib.util.spec_from_file_location("cursor_file_q", WORK / "plans/runs/nckh-native-261004-1707-attempt-01/qualification-run.py")
q = importlib.util.module_from_spec(qspec)
qspec.loader.exec_module(q)
q.RUN = RUN
sys.path.insert(0, str(WORK / "nckh-kit"))
sys.dont_write_bytecode = True
from core.build import verify_source_lock
from core.hook_config import payload_from_bundle, preview_config
from core.paths import atomic_json, contained, digest_file, digest_record

read = lambda path: json.loads(path.read_text(encoding="utf8"))
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": digest_file(path)}
GLOBAL_PATHS = [Path(r"C:/Users/USER") / relative for relative in
    (".cursor/hooks.json", ".cursor/mcp.json", ".cursor/plugins/installed_plugins.json", ".cursor/plugins/settings.json")]
GLOBAL_CLI = Path(r"C:/Users/USER\.cursor\cli-config.json")


def check_source():
    assert digest_record(verify_source_lock(WORK / "nckh-kit")) == EXPECTED


def prepare():
    check_source()
    assert PROJECT.is_dir() and not CONFIG.exists() and not EVIDENCE.exists()
    cfg = read(GLOBAL_CLI)
    selected = cfg["selectedModel"]
    params = {row["id"]: row["value"] for row in selected["parameters"]}
    assert selected["modelId"] == "grok-4.7" and params["context"] == "500k" and params["reasoning_effort"] == "xhigh"
    assert read(DELIVERY / "revalidation-summary.json")["status"] == "completed-local-checks-native-retest-pending"
    historical = {path.relative_to(PROJECT).as_posix(): digest_file(path) for path in PROJECT.rglob("*") if path.is_file()}
    atomic_json(RUN / "historical-project-preimage.json", {"members": historical})
    EVIDENCE.mkdir()
    version_record, stdout, stderr = q.run_command("cursor-file-version", q.installed_commands()["cursor"] + ["--version"], cwd=PROJECT)
    assert version_record["exit_code"] == 0
    version = stdout.decode("utf8").strip()
    protected = [{"path": str(path), "sha256": digest_file(path) if path.is_file() else None} for path in GLOBAL_PATHS]
    atomic_json(RUN / "native-metadata.json", {"version": version, "selected_model": selected, "command_model": MODEL,
        "effort_requested": "xhigh", "protected_config": protected, "global_cli_sha256": digest_file(GLOBAL_CLI),
        "global_hooks": "existing enabled native environment; no documented CLI isolation flag in prior help",
        "global_direct_write": False, "backend_attestation": "not-observed", "billing": "not-observed"})
    package = Path(read(DELIVERY / "delivery-context.json")["outside"]) / "extracted/on-standalone/cursor"
    payload = payload_from_bundle(package)
    preview = preview_config(PROJECT, "cursor", payload, context_reference=".nckh-native-r35-cursor-write-faults-02/context-allow.json",
        events=list(EVENTS), host_version=version, surface="cursor-cli", python=sys.executable)
    runtime = contained(PROJECT, preview["runtime_relative"])
    staged = []
    for relative, expected in payload["members"].items():
        target = contained(runtime, relative)
        assert not target.exists()
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(contained(package, relative), target)
        assert digest_file(target) == expected
        staged.append({"path": target.relative_to(PROJECT).as_posix(), "sha256": expected})
    mapping = {"Write": "write", "Edit": "write", "StrReplace": "write", "Read": "read", "Shell": "write"}
    for name, mode, operations in (("allow", "auto", mapping), ("deny", "plan-only", mapping), ("uncovered", "auto", {})):
        atomic_json(EVIDENCE / ("context-" + name + ".json"), {"schema_version": 1, "task_id": "native-cursor-file-r35",
            "brief": {"mode": mode}, "tool_operations": operations, "allowed_operations": ["write", "read"]})
    atomic_json(RUN / "stage.json", {"staged_members": staged, "runner": str(contained(runtime, payload["runner"])),
        "payload": payload, "package": str(package), "preview": preview, "source_lock_hash": EXPECTED,
        "observer_sha256": digest_file(OBSERVER), "contexts": {path.name: digest_file(path) for path in EVIDENCE.glob("context-*.json")}})
    atomic_json(RUN / "ownership.json", {"owner": "/root", "port": None, "source_revision": 35,
        "source_lock_hash": EXPECTED, "project": str(PROJECT), "evidence": str(EVIDENCE), "model": MODEL,
        "effort": "xhigh", "controller": bind(Path(__file__)), "observer": bind(OBSERVER),
        "native_grant": bind(WORK / "plans/runs/nckh-native-261004-1707-attempt-01/native-grant.json"),
        "dangerous_grant": bind(RUN / "cursor-agy-model-dangerous-grant.json"), "installed_update": "not-performed"})
    print(json.dumps({"status": "prepared", "version": version, "payload_members": len(staged)}), flush=True)


def register(mode, attempt):
    stage = read(RUN / "stage.json")
    assert digest_file(OBSERVER) == stage["observer_sha256"]
    assert all(digest_file(EVIDENCE / name) == expected for name, expected in stage["contexts"].items())
    assert all(digest_file(contained(PROJECT, row["path"])) == row["sha256"] for row in stage["staged_members"])
    if CONFIG.exists():
        assert digest_file(CONFIG) == read(RUN / "last-definition.json")["config_sha256"]
    atomic_json(EVIDENCE / "probe-control.json", {"mode": mode, "attempt": attempt, "selected_event": "preToolUse", "selected_tool": "Write"})
    handlers = {}
    for event in EVENTS:
        command = subprocess.list2cmdline([sys.executable, "-I", str(OBSERVER), "--host", "cursor", "--event", event,
            "--project", str(PROJECT), "--evidence", str(EVIDENCE), "--runner", stage["runner"]])
        item = {"type": "command", "command": command, "timeout": 2 if mode == "timeout" and event == "preToolUse" else 20}
        if event == "preToolUse":
            item["failClosed"] = True
        if event == "stop":
            item["loop_limit"] = 1
        handlers[event] = [item]
    if mode == "timeout":
        base_handler = handlers["preToolUse"][0]
        handlers["preToolUse"] = [{**base_handler, "matcher": "^Read$", "timeout": 20},
            {**base_handler, "matcher": "^Write$", "timeout": 2}]
    atomic_json(CONFIG, {"version": 1, "hooks": handlers})
    extras = []
    if mode == "duplicate":
        plugin = EVIDENCE / "plugin"
        manifest, hooks = plugin / ".cursor-plugin/plugin.json", plugin / "hooks/hooks.json"
        assert not manifest.exists() and not hooks.exists()
        atomic_json(manifest, {"name": "nckh-native-file-probe", "version": "0.0.0", "hooks": "./hooks/hooks.json"})
        plugin_handler = {**handlers["preToolUse"][0], "command": handlers["preToolUse"][0]["command"] + " --callback-source plugin"}
        atomic_json(hooks, {"version": 1, "hooks": {"preToolUse": [plugin_handler]}})
        extras = [{"path": path.relative_to(PROJECT).as_posix(), "sha256": digest_file(path)} for path in (manifest, hooks)]
    record = {"config_sha256": digest_file(CONFIG), "mode": mode, "attempt": attempt, "extra_configs": extras,
        "source_lock_hash": EXPECTED, "observer_sha256": digest_file(OBSERVER)}
    atomic_json(RUN / "definitions" / (attempt + ".json"), record)
    atomic_json(RUN / "last-definition.json", record)
    return record


def observe(kind, mode, relative, attempt):
    check_source()
    path = contained(PROJECT, relative)
    before = digest_file(path) if path.is_file() else None
    target = RUN / "attempts" / (attempt + ".json")
    assert not target.exists()
    definition = register(mode, attempt)
    command = q.installed_commands()["cursor"]
    if mode == "duplicate":
        command += ["--plugin-dir", str(EVIDENCE / "plugin")]
    prompt = ("Use the native " + kind + " file tool exactly once in this authorized scratch project. "
        "Do not use shell/terminal, any other tool, inspect other files, call agents, retry or work around denial. "
        "These files contain synthetic test markers only. After the one attempted call say ORACLE_ATTEMPT_FINISHED and stop. "
        + ("Write exactly NCKH_CURSOR_FILE_ORACLE followed by a newline to " if kind == "Write" else "Read ") + relative)
    command += ["--print", "--force", "--trust", "--sandbox", "disabled", "--workspace", str(PROJECT),
        "--model", MODEL, "--output-format", "stream-json", prompt]
    atomic_json(target, {"status": "running", "attempt": attempt, "kind": kind, "mode": mode,
        "source_lock_hash": EXPECTED, "before_sha256": before, "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest()})
    outcome, stdout, stderr = q.run_command("cursor-file-" + attempt, command, cwd=PROJECT, timeout=270)
    frames, invalid = [], 0
    for line in stdout.decode("utf8").splitlines():
        try:
            frames.append(json.loads(line))
        except ValueError:
            invalid += 1
    callbacks = sorted((EVIDENCE / "observations" / attempt).glob("*/*.json"))
    policies = sorted((EVIDENCE / "policy-receipts" / attempt / "preToolUse").glob("*.json"))
    completed = [frame for frame in frames if frame.get("type") == "tool_call" and frame.get("subtype") == "completed"]
    after = digest_file(path) if path.is_file() else None
    record = {"status": outcome["status"], "attempt": attempt, "kind": kind, "mode": mode, "path": relative,
        "source_revision": 35, "source_lock_hash": EXPECTED, "before_sha256": before, "after_sha256": after,
        "file_exists": path.is_file(), "process_exited": outcome["process_exited"], "exit_code": outcome["exit_code"],
        "native_frames": frames, "completed_tool_calls": completed, "invalid_stdout_lines": invalid,
        "native_callbacks": [read(path) for path in callbacks], "callback_bindings": [bind(path) for path in callbacks],
        "policy_receipts": [{**bind(path), "decision": read(path)["decision"], "reason_codes": read(path)["reason_codes"]} for path in policies],
        "model_requested": MODEL, "effort_requested": "xhigh", "definition": bind(RUN / "definitions" / (attempt + ".json")),
        "command_receipt": bind(RUN / "commands" / ("cursor-file-" + attempt + ".json")),
        "fault_origin": "controller-after-genuine-callback" if mode in {"malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec"} else "none",
        "backend_attestation": "not-observed", "billing": "not-observed"}
    atomic_json(target, record)
    selected = [row for row in record["native_callbacks"] if row["event"] == "preToolUse"]
    print(json.dumps({"attempt": attempt, "tool_requested": kind, "pretool_callbacks": len(selected),
        "actual_tools": [row["native_tool_name"] for row in selected], "file_exists": path.is_file(),
        "decisions": [row["decision"] for row in record["policy_receipts"]]}), flush=True)
    assert outcome["process_exited"], "Reconcile owned process before another native attempt"
    return record


def cleanup():
    stage = read(RUN / "stage.json")
    definition = read(RUN / "last-definition.json")
    metadata = read(RUN / "native-metadata.json")
    globals_after = [{**row, "current_sha256": digest_file(Path(row["path"])) if Path(row["path"]).is_file() else None} for row in metadata["protected_config"]]
    assert all(row["current_sha256"] == row["sha256"] for row in globals_after)
    for row in metadata["protected_config"]:
        global_path = Path(row["path"])
        if global_path.is_file():
            text = global_path.read_text(encoding="utf8").casefold().replace("\\\\", "\\")
            assert str(OBSERVER).casefold() not in text and stage["runner"].casefold() not in text
    owned = [{"path": ".cursor/hooks.json", "sha256": definition["config_sha256"]}, *definition["extra_configs"], *stage["staged_members"]]
    assert all(digest_file(contained(PROJECT, row["path"])) == row["sha256"] for row in owned)
    for row in owned:
        contained(PROJECT, row["path"]).unlink()
    historical = read(RUN / "historical-project-preimage.json")["members"]
    assert all(digest_file(contained(PROJECT, relative)) == expected for relative, expected in historical.items())
    atomic_json(RUN / "cleanup.json", {"status": "pass", "removed_members": owned, "config_callable": CONFIG.exists(),
        "historical_members_unchanged": len(historical), "protected_global_config": globals_after,
        "global_cli_hash_before": metadata["global_cli_sha256"], "global_cli_hash_after": digest_file(GLOBAL_CLI),
        "global_direct_write": False, "native_workspace_state": "CLI-owned state may remain", "native_evidence_retained": True})
    print(json.dumps({"status": "cleaned", "removed": len(owned), "historical_preserved": len(historical)}), flush=True)


if __name__ == "__main__":
    assert not (RUN / "native-file-summary.json").exists()
    prepare()
    results = []
    try:
        for mode in ("timeout", "crash", "unsupported-codec"):
            relative = "oracles/r35-cursor-write-stage-02-" + mode + ".txt"
            attempt = "write-stage-02-" + mode
            assert not contained(PROJECT, relative).exists()
            row = observe("Write", mode, relative, attempt)
            results.append({"attempt": attempt, "kind": "Write", "mode": mode, "fault_target_tool": "Write",
                "receipt": bind(RUN / "attempts" / (attempt + ".json"))})
            atomic_json(RUN / "native-file-summary.json", {"status": "running", "results": results, "source_lock_hash": EXPECTED})
            callbacks = [c for c in row["native_callbacks"] if c["event"] == "preToolUse"]
            selected = [c for c in callbacks if c.get("fault_selected")]
            assert selected and all(c["native_tool_name"] == "Write" for c in selected), "Write-stage fault not reached; retain evidence"
            assert all(not c.get("fault_selected") for c in callbacks if c["native_tool_name"] == "Read")
            assert row["before_sha256"] is None and row["after_sha256"] is None, "Unexpected native file creation; retain failure"
        atomic_json(RUN / "native-file-summary.json", {"status": "recorded-native-cursor-write-stage-faults", "results": results,
            "source_revision": 35, "source_lock_hash": EXPECTED, "fault_target_tool": "Write"})
    finally:
        cleanup()
