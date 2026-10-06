"""Prepare one source-backed plugin prompt/stop compatibility observation."""

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-1900-r37-cursor-project-plugin-duplicate-attempt-19"
INSPECT = WORK / "plans/runs/nckh-native-261005-1923-r37-cursor-plugin-routing-inspection-attempt-20"
read = lambda path: json.loads(path.read_text(encoding="utf8"))
assert not (RUN / "preparation.json").exists()
assert read(BASE / "cleanup.json")["status"] == "pass"
assert read(BASE / "final-process-audit.json")["matching_count"] == 0
assert read(RUN / "process-preflight.json")["matching_count"] == read(RUN / "process-preflight.json")["tracked_live_count"] == 0
hypothesis = read(INSPECT / "routing-hypothesis.json")
index = Path(read(INSPECT / "cursor-hook-source-excerpts.json")["source"])
assert hashlib.sha256(index.read_bytes()).hexdigest() == hypothesis["vendor_index_sha256"]
runtime = RUN / "cursor-alias-runtime.py"
original = (BASE / "cursor-duplicate-runtime.py").read_text(encoding="utf8")
source = original.replace(".nckh-native-r37-cursor-duplicate-19", ".nckh-native-r37-cursor-plugin-alias-21")
assert source != original
compile(source, str(runtime), "exec")
with runtime.open("x", encoding="utf8") as stream:
    stream.write(source)
for name in ("capture-native-processes.ps1", "reconcile-native-processes.ps1", "cursor-agy-model-dangerous-grant.json", "cursor-file-observer.py"):
    with (RUN / name).open("xb") as stream:
        stream.write((BASE / name).read_bytes())
spec = importlib.util.spec_from_file_location("alias_runtime", runtime)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.prepare()
stage = read(RUN / "stage.json")
context = read(probe.EVIDENCE / "context-allow.json")
context["task_id"] = "native-cursor-r37-plugin-alias-controls-21"
probe.atomic_json(probe.EVIDENCE / "context-allow.json", context)
probe.atomic_json(probe.EVIDENCE / "probe-control.json", {"mode": "duplicate", "attempt": "alias-session", "selected_event": "beforeSubmitPrompt",
    "fault_origin": "none", "purpose": "Actual project/plugin prompt/stop callbacks via documented alias definitions"})
observer = RUN / "cursor-file-observer.py"
config = json.loads(json.dumps(stage["preview"]["after"]))
for event, handlers in config["hooks"].items():
    assert len(handlers) == 1 and handlers[0]["timeout"] == (20 if event == "preToolUse" else 5)
    handlers[0]["command"] = subprocess.list2cmdline([sys.executable, "-X", "utf8", "-B", str(observer),
        "--host", "cursor", "--event", event, "--project", str(probe.PROJECT), "--evidence", str(probe.EVIDENCE),
        "--runner", stage["runner"], "--callback-source", "project"])
plugin = probe.EVIDENCE / "plugin"
manifest = {"name": "nckh-native-hook-alias-control", "version": "1.0.0",
    "description": "Owned prompt and stop compatibility qualification fixture", "hooks": "./hooks/hooks.json"}
plugin_hooks = {}
for alias, event in (("UserPromptSubmit", "beforeSubmitPrompt"), ("Stop", "stop")):
    handler = json.loads(json.dumps(config["hooks"][event][0]))
    handler["command"] = handler["command"].removesuffix("--callback-source project") + "--callback-source plugin"
    assert handler["timeout"] == 5 and handler["type"] == "command"
    plugin_hooks[alias] = [{"matcher": "*", "hooks": [handler]}]
plugin_config = {"hooks": plugin_hooks}
probe.atomic_json(plugin / ".cursor-plugin/plugin.json", manifest)
probe.atomic_json(plugin / "hooks/hooks.json", plugin_config)
probe.atomic_json(probe.CONFIG, config)
extras = [{"path": p.relative_to(probe.PROJECT).as_posix(), "sha256": probe.digest_file(p)}
    for p in (plugin / ".cursor-plugin/plugin.json", plugin / "hooks/hooks.json")]
definition = {"config_sha256": probe.digest_file(probe.CONFIG), "config": config, "extra_configs": extras,
    "plugin_config": plugin_config, "plugin_manifest": manifest, "plugin_relative": plugin.relative_to(probe.PROJECT).as_posix(),
    "definition_kind": "native-project-plugin-prompt-stop-alias-observers", "selected_events": ["beforeSubmitPrompt", "stop"],
    "preToolUse_timeout_seconds": 20, "other_packaged_timeout_seconds": 5, "inner_runner_timeout_seconds": 5,
    "observer": probe.bind(observer), "source_lock_hash": probe.EXPECTED, "fault_origin": "none", "packaged_runner_unchanged": True,
    "plugin_kind": "minimal controller plugin with two compatibility definitions; not full kit plugin installation",
    "hypothesis": probe.bind(INSPECT / "routing-hypothesis.json")}
probe.atomic_json(RUN / "definitions/session.json", definition)
probe.atomic_json(RUN / "last-definition.json", definition)
prompt = "Use no tools, commands, agents, files or follow-up requests. Reply exactly NCKH_PLUGIN_ALIAS_FINISHED_21 and stop."
prepared = {"status": "prepared-one-native-plugin-prompt-stop-alias-control", "source_revision": 37, "source_lock_hash": probe.EXPECTED,
    "project": str(probe.PROJECT), "package": stage["package"], "plugin": str(plugin), "model": probe.MODEL,
    "effort": "xhigh", "port": None, "prompt": prompt, "marker": "NCKH_PLUGIN_ALIAS_FINISHED_21",
    "maximum_model_turns": 1, "maximum_prompt_submissions": 1, "maximum_requested_native_tools": 0,
    "selected_events": ["beforeSubmitPrompt", "stop"], "fault_origin": "none", "hypothesis": probe.bind(INSPECT / "routing-hypothesis.json"),
    "definition": probe.bind(RUN / "definitions/session.json"), "context_sha256": probe.digest_file(probe.EVIDENCE / "context-allow.json"),
    "control_sha256": probe.digest_file(probe.EVIDENCE / "probe-control.json"), "runtime": probe.bind(runtime),
    "controller": probe.bind(Path(__file__)), "global_direct_write": False, "installed_update": "not-performed",
    "oracle": hypothesis["oracle"], "official_reference": hypothesis["official_reference"]}
probe.atomic_json(RUN / "preparation.json", prepared)
probe.atomic_json(RUN / "frozen-brief.json", prepared)
print(json.dumps({"status": prepared["status"], "plugin": str(plugin), "maximum_model_turns": 1, "requested_tools": 0}))
