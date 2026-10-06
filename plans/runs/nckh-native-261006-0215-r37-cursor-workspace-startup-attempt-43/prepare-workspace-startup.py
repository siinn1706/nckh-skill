"""Stage a distinct startup observation inside the existing owned scratch project."""

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PRIOR = RUN.parent / "nckh-native-261006-0110-r37-cursor-private-search-attempt-39"
PROJECT = WORK / "plans/runs/nckh-native-261005-0128-r34-cursor-events-attempt-02/projects/main"
EVIDENCE = PROJECT / ".nckh-native-cursor-workspace-startup-43"
CONFIG = PROJECT / ".cursor/hooks.json"
MODEL = "grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()

def write_new(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")


audit = read(RUN / "process-preflight-audit.json")
assert audit["matching_count"] == audit["tracked_live_count"] == 0
assert PROJECT.is_dir() and not CONFIG.exists() and not EVIDENCE.exists()
vendor = Path(r"C:/Users/USER\AppData\Local\cursor-agent\versions\2026.09.15-d2fe57e")
assert sha(vendor / "index.js") == read(RUN.parent / "nckh-native-261006-0200-r37-cursor-workspace-route-inspection-attempt-42/verified-workspace-route-inspection.json")["vendor_source_sha256"]
selected = read(Path(r"C:/Users/USER\.cursor\cli-config.json"))["selectedModel"]
assert selected["modelId"] == "grok-4.7"
assert {row["id"]: row["value"] for row in selected["parameters"]} == {"context": "500k", "reasoning_effort": "xhigh", "fast": "false"}
historical = {path.relative_to(PROJECT).as_posix(): sha(path) for path in PROJECT.rglob("*") if path.is_file()}
write_new(RUN / "historical-project-preimage.json", {"members": historical})
stage = read(PRIOR / "stage.json")
package = Path(stage["package"])
EVIDENCE.mkdir()
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
    ("workspace-startup-observer.py", RUN / "workspace-startup-observer.py"),
):
    target = EVIDENCE / name
    shutil.copyfile(source, target)
    owned.append({"path": target.relative_to(PROJECT).as_posix(), "sha256": sha(target)})
write_new(EVIDENCE / "context-allow.json", {"schema_version": 1, "task_id": "native-cursor-workspace-route",
    "brief": {"mode": "auto"}, "tool_operations": {}, "allowed_operations": []})
write_new(EVIDENCE / "probe-control.json", {"mode": "duplicate", "attempt": "startup-only", "selected_event": "sessionStart"})
plugin = EVIDENCE / "plugin"
write_new(plugin / ".cursor-plugin/plugin.json", {"name": "nckh-cursor-workspace-probe", "version": "0.0.0", "hooks": "./hooks/hooks.json"})
def lifecycle(event, source):
    return {"command": subprocess.list2cmdline([sys.executable, "-X", "utf8", "-B", str(EVIDENCE / "lifecycle-observer.py"),
        "--host", "cursor", "--event", event, "--project", str(PROJECT), "--evidence", str(EVIDENCE),
        "--runner", str(runner), "--callback-source", source]), "timeout": 5}
plugin_hooks = {"version": 1, "hooks": {event: [lifecycle(event, "plugin")] for event in ("sessionStart", "beforeSubmitPrompt", "stop")}}
write_new(plugin / "hooks/hooks.json", plugin_hooks)
config = {"version": 1, "hooks": {
    "workspaceOpen": [{"command": subprocess.list2cmdline([sys.executable, "-X", "utf8", "-B", str(EVIDENCE / "workspace-startup-observer.py"),
        "--project", str(PROJECT), "--plugin", str(plugin), "--evidence", str(EVIDENCE)]), "timeout": 5}],
    "sessionStart": [lifecycle("sessionStart", "project")],
}}
write_new(CONFIG, config)
for target in (EVIDENCE / "context-allow.json", EVIDENCE / "probe-control.json", plugin / ".cursor-plugin/plugin.json", plugin / "hooks/hooks.json", CONFIG):
    owned.append({"path": target.relative_to(PROJECT).as_posix(), "sha256": sha(target)})
protected = [Path(r"C:/Users/USER") / relative for relative in (".cursor/hooks.json", ".cursor/mcp.json", ".cursor/plugins/installed_plugins.json", ".cursor/plugins/settings.json")]
argv = [str(vendor / "node.exe"), str(vendor / "index.js"), "--force", "--trust", "--sandbox", "disabled", "--workspace", str(PROJECT)]
definition = {
    "status": "prepared-distinct-workspace-startup-observation", "source_revision": 37, "source_lock_hash": stage["source_lock_hash"],
    "project": str(PROJECT), "evidence": str(EVIDENCE), "model": MODEL, "selected_model": selected,
    "argv": argv, "plugin_loading_route": "workspaceOpen output only; no --plugin-dir argument",
    "model_prompts": 0, "maximum_model_turns": 0, "maximum_prompt_submissions": 0, "maximum_tool_requests": 0,
    "observation": "Wait for interactive readiness and a bounded 12-second startup observation window; then native /exit",
    "oracle": "Genuine workspaceOpen callback with exact workspace and returned owned plugin path; genuine plugin sessionStart callback from this route. Missing callbacks remain unqualified, not unsupported.",
    "fault_origin": "none", "hook_timeout_seconds": 5, "runner_timeout_seconds": 5,
    "workspace_handler": "controller-owned route diagnostic; not a packaged codec event", "config": config,
    "plugin_hooks": plugin_hooks, "owned_files": owned, "historical_files": len(historical),
    "protected_configs": [{"path": str(path), "sha256": sha(path) if path.is_file() else None} for path in protected],
    "global_cli_preimage_sha256": sha(Path(r"C:/Users/USER\.cursor\cli-config.json")), "global_direct_writes": False,
    "vendor_source_sha256": sha(vendor / "index.js"), "controller_sha256": sha(Path(__file__)),
    "full_native_gate": "unchecked",
}
write_new(RUN / "preparation.json", definition)
write_new(RUN / "frozen-brief.json", definition)
print(json.dumps({"status": definition["status"], "owned_files": len(owned), "historical_files": len(historical), "model_prompts": 0}))
