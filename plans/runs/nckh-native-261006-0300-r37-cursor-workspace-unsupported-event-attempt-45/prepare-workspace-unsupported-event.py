"""Freeze a startup-only observation of a genuine event absent from the kit codec."""

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PRIOR = RUN.parent / "nckh-native-261006-0110-r37-cursor-private-search-attempt-39"
HELPERS = RUN.parent / "nckh-native-261006-0240-r37-cursor-workspace-duplicates-attempt-44"
PROJECT = WORK / "plans/runs/nckh-native-261005-0128-r34-cursor-events-attempt-02/projects/main"
EVIDENCE = PROJECT / ".nckh-native-cursor-workspace-unsupported-45"
CONFIG = PROJECT / ".cursor/hooks.json"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()

def write_new(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")

audit = read(RUN / "process-preflight-audit.json")
assert audit["matching_count"] == audit["tracked_live_count"] == 0 and len(audit["tracked"]) == 1803
assert PROJECT.is_dir() and not CONFIG.exists() and not EVIDENCE.exists()
vendor = Path(r"C:/Users/USER\AppData\Local\cursor-agent\versions\2026.09.15-d2fe57e")
assert sha(vendor / "index.js") == read(RUN.parent / "nckh-native-261006-0200-r37-cursor-workspace-route-inspection-attempt-42/verified-workspace-route-inspection.json")["vendor_source_sha256"]
selected = read(Path(r"C:/Users/USER\.cursor\cli-config.json"))["selectedModel"]
assert selected["modelId"] == "grok-4.7"
assert {row["id"]: row["value"] for row in selected["parameters"]} == {"context": "500k", "reasoning_effort": "xhigh", "fast": "false"}
stage = read(PRIOR / "stage.json")
lock = read(WORK / "nckh-kit/core/registry/source-lock/source-lock.json")
sys.path.insert(0, str(WORK / "nckh-kit"))
from core.paths import digest_record
assert digest_record(lock) == stage["source_lock_hash"]
historical = {path.relative_to(PROJECT).as_posix(): sha(path) for path in PROJECT.rglob("*") if path.is_file()}
write_new(RUN / "historical-project-preimage.json", {"members": historical})
for name in ("owned-cli-command.py", "capture-native-processes.ps1"):
    target = RUN / name
    assert not target.exists()
    shutil.copyfile(HELPERS / name, target)
monitor = (HELPERS / "monitor-native-session.py").read_text(encoding="utf8")
assert monitor.count("native-cursor-workspace-duplicates.process-tree.json") == 1
with (RUN / "monitor-native-session.py").open("x", encoding="utf8") as stream:
    stream.write(monitor.replace("native-cursor-workspace-duplicates.process-tree.json", "native-cursor-workspace-unsupported.process-tree.json"))
EVIDENCE.mkdir()
package = Path(stage["package"])
owned = []
for relative, expected in stage["payload"]["members"].items():
    target = EVIDENCE / "runtime" / relative
    target.resolve().relative_to(PROJECT.resolve())
    assert not target.exists() and sha(package / relative) == expected
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(package / relative, target)
    assert sha(target) == expected
    owned.append({"path": target.relative_to(PROJECT).as_posix(), "sha256": expected})
runner = EVIDENCE / "runtime" / stage["payload"]["runner"]
for name, source in (
    ("lifecycle-observer.py", PRIOR / "cursor-file-observer.py"),
    ("workspace-startup-observer.py", HELPERS / "workspace-startup-observer.py"),
    ("workspace-codec-observer.py", RUN / "workspace-codec-observer.py"),
):
    target = EVIDENCE / name
    shutil.copyfile(source, target)
    owned.append({"path": target.relative_to(PROJECT).as_posix(), "sha256": sha(target)})
write_new(EVIDENCE / "context-allow.json", {"schema_version": 1, "task_id": "native-cursor-workspace-unsupported",
    "brief": {"mode": "auto"}, "tool_operations": {}, "allowed_operations": []})
write_new(EVIDENCE / "probe-control.json", {"mode": "duplicate", "attempt": "workspace-unsupported", "selected_event": "sessionStart"})
plugin = EVIDENCE / "plugin"
write_new(plugin / ".cursor-plugin/plugin.json", {"name": "nckh-cursor-workspace-unsupported-probe", "version": "0.0.0", "hooks": "./hooks/hooks.json"})

def handler(script, args):
    return {"command": subprocess.list2cmdline([sys.executable, "-X", "utf8", "-B", str(EVIDENCE / script), *args]), "timeout": 5}

def lifecycle(source):
    return handler("lifecycle-observer.py", ["--host", "cursor", "--event", "sessionStart", "--project", str(PROJECT),
        "--evidence", str(EVIDENCE), "--runner", str(runner), "--callback-source", source])

plugin_hooks = {"version": 1, "hooks": {"sessionStart": [lifecycle("plugin")]}}
write_new(plugin / "hooks/hooks.json", plugin_hooks)
config = {"version": 1, "hooks": {
    "workspaceOpen": [
        handler("workspace-codec-observer.py", ["--project", str(PROJECT), "--evidence", str(EVIDENCE), "--runner", str(runner)]),
        handler("workspace-startup-observer.py", ["--project", str(PROJECT), "--plugin", str(plugin), "--evidence", str(EVIDENCE)]),
    ],
    "sessionStart": [lifecycle("project")],
}}
write_new(CONFIG, config)
for target in (EVIDENCE / "context-allow.json", EVIDENCE / "probe-control.json", plugin / ".cursor-plugin/plugin.json", plugin / "hooks/hooks.json", CONFIG):
    owned.append({"path": target.relative_to(PROJECT).as_posix(), "sha256": sha(target)})
protected = [Path(r"C:/Users/USER") / relative for relative in (".cursor/hooks.json", ".cursor/mcp.json", ".cursor/plugins/installed_plugins.json", ".cursor/plugins/settings.json")]
argv = [str(vendor / "node.exe"), str(vendor / "index.js"), "--force", "--trust", "--sandbox", "disabled", "--workspace", str(PROJECT)]
compiled = []
for path in list(RUN.glob("*.py")) + list((EVIDENCE / "runtime").rglob("*.py")):
    compile(path.read_text(encoding="utf8"), str(path), "exec")
    compiled.append(str(path))
definition = {
    "status": "prepared-startup-only-genuine-kit-unsupported-event", "source_revision": 37,
    "source_lock_hash": stage["source_lock_hash"], "project": str(PROJECT), "evidence": str(EVIDENCE),
    "model": "grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]", "selected_model": selected,
    "argv": argv, "plugin_loading_route": "workspaceOpen output only; no --plugin-dir argument",
    "model_prompts": 0, "maximum_model_turns": 0, "maximum_prompt_submissions": 0, "maximum_tool_requests": 0,
    "startup_observation_seconds": 15, "normal_exit": "/exit",
    "oracle": {
        "unsupported_event": "actual workspaceOpen native payload forwarded unchanged with --event workspaceOpen",
        "fault_origin": "none", "expected_runner_exit": 3, "expected_runner_output": {},
        "expected_receipt_status": "degraded-failed", "expected_decision": "block",
        "expected_reason_codes": ["hook-input-or-context-invalid"],
        "expected_receipt_event_hash": "SHA256 of actual native input bytes; no decoded context/phase claimed",
        "expected_workspace_handlers": 2, "expected_sessionStart_handlers": 2, "expected_policy_receipts": 2,
        "expected_native_startup": "separate owned route diagnostic and project/plugin lifecycle pair after workspace callback failure",
        "retain_differing_outcomes": True,
    },
    "event_scope": "host-known event unsupported by kit codec; unknown-host-event admission remains unqualified",
    "hook_timeout_seconds": 5, "runner_timeout_seconds": 5,
    "config": config, "plugin_hooks": plugin_hooks, "owned_files": owned, "historical_files": len(historical),
    "protected_configs": [{"path": str(path), "sha256": sha(path) if path.is_file() else None} for path in protected],
    "global_cli_preimage_sha256": sha(Path(r"C:/Users/USER\.cursor\cli-config.json")), "global_direct_writes": False,
    "vendor_source_sha256": sha(vendor / "index.js"), "controller_sha256": sha(Path(__file__)),
    "python_files_compiled_in_memory": len(compiled), "full_native_gate": "unchecked",
}
write_new(RUN / "preparation.json", definition)
write_new(RUN / "frozen-brief.json", definition)
print(json.dumps({"status": definition["status"], "owned_files": len(owned), "historical_files": len(historical),
    "compiled_python_files": len(compiled), "model_prompts": 0, "maximum_model_turns": 0}))
