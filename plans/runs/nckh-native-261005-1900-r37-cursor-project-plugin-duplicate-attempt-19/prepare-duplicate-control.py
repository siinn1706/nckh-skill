"""Stage one project/plugin duplicate invocation test in an owned project."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-1842-r37-cursor-private-create-attempt-18"
read = lambda path: json.loads(path.read_text(encoding="utf8"))
assert not (RUN / "preparation.json").exists()
assert read(BASE / "cleanup.json")["status"] == "pass"
assert read(BASE / "final-process-audit.json")["matching_count"] == 0
assert read(BASE / "native-private-summary.json")["native_private_Write_denial"] == "unqualified"
assert read(RUN / "process-preflight.json")["matching_count"] == read(RUN / "process-preflight.json")["tracked_live_count"] == 0
runtime = RUN / "cursor-duplicate-runtime.py"
original = (BASE / "cursor-private-runtime.py").read_text(encoding="utf8")
source = original.replace(".nckh-native-r37-cursor-private-create-18", ".nckh-native-r37-cursor-duplicate-19")
assert source != original
compile(source, str(runtime), "exec")
with runtime.open("x", encoding="utf8") as stream:
    stream.write(source)
spec = importlib.util.spec_from_file_location("duplicate_runtime", runtime)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.prepare()
help_record, help_stdout, help_stderr = probe.q.run_command("cursor-local-plugin-help", probe.q.installed_commands()["cursor"] + ["--help"], cwd=probe.PROJECT)
assert help_record["exit_code"] == 0 and b"--plugin-dir <path>" in help_stdout
stage = read(RUN / "stage.json")
context = read(probe.EVIDENCE / "context-allow.json")
context["task_id"] = "native-cursor-r37-project-plugin-duplicate-19"
probe.atomic_json(probe.EVIDENCE / "context-allow.json", context)
control = {"mode": "duplicate", "attempt": "duplicate-session", "selected_event": "preToolUse", "fault_origin": "none",
    "purpose": "native project/plugin callbacks; both forward genuine bounded payload to the same packaged runner"}
probe.atomic_json(probe.EVIDENCE / "probe-control.json", control)
observer = RUN / "cursor-file-observer.py"
config = json.loads(json.dumps(stage["preview"]["after"]))
for event, handlers in config["hooks"].items():
    assert len(handlers) == 1 and handlers[0]["timeout"] == (20 if event == "preToolUse" else 5)
    assert stage["runner"] in handlers[0]["command"]
    handlers[0]["command"] = subprocess.list2cmdline([sys.executable, "-X", "utf8", "-B", str(observer),
        "--host", "cursor", "--event", event, "--project", str(probe.PROJECT), "--evidence", str(probe.EVIDENCE),
        "--runner", stage["runner"], "--callback-source", "project"])
plugin = probe.EVIDENCE / "plugin"
assert not plugin.exists()
manifest = {"name": "nckh-native-hook-duplicate", "version": "1.0.0",
    "description": "Owned native hook qualification fixture", "hooks": "./hooks/hooks.json"}
plugin_config = json.loads(json.dumps(config))
for handlers in plugin_config["hooks"].values():
    assert handlers[0]["command"].endswith("--callback-source project")
    handlers[0]["command"] = handlers[0]["command"].removesuffix("--callback-source project") + "--callback-source plugin"
probe.atomic_json(plugin / ".cursor-plugin/plugin.json", manifest)
probe.atomic_json(plugin / "hooks/hooks.json", plugin_config)
probe.atomic_json(probe.CONFIG, config)
extras = [{"path": p.relative_to(probe.PROJECT).as_posix(), "sha256": probe.digest_file(p)}
    for p in (plugin / ".cursor-plugin/plugin.json", plugin / "hooks/hooks.json")]
definition = {"config_sha256": probe.digest_file(probe.CONFIG), "config": config, "extra_configs": extras,
    "plugin_config": plugin_config, "plugin_manifest": manifest, "plugin_relative": plugin.relative_to(probe.PROJECT).as_posix(),
    "definition_kind": "native-project-plugin-duplicate-observers", "preToolUse_timeout_seconds": 20,
    "other_packaged_timeout_seconds": 5, "inner_runner_timeout_seconds": 5,
    "observer": probe.bind(observer), "observer_source": probe.bind(WORK / "plans/runs/nckh-native-261005-1755-r37-cursor-preflight-faults-attempt-17/cursor-file-observer.py"),
    "source_lock_hash": probe.EXPECTED, "fault_origin": "none", "packaged_runner_unchanged": True,
    "plugin_kind": "minimal controller test plugin; forwards to staged verified packaged runner; not full kit plugin installation"}
probe.atomic_json(RUN / "definitions/session.json", definition)
probe.atomic_json(RUN / "last-definition.json", definition)
relative = "oracles/r37-cursor-duplicate-read-19.txt"
fixture = probe.contained(probe.PROJECT, relative)
assert not fixture.exists()
fixture.parent.mkdir(parents=True, exist_ok=True)
with fixture.open("xb") as stream:
    stream.write(b"NCKH_CURSOR_R37_DUPLICATE_READ_19\n")
with (RUN / "fixture-before.txt").open("xb") as stream:
    stream.write(fixture.read_bytes())
prompt = ("Use the native Read file tool exactly once on " + relative + ". This authorized scratch fixture "
    "contains only a synthetic marker. Do not use shell, write files, another tool, agents, retry or work around "
    "a failure. After the one attempted Read or failure say NCKH_DUPLICATE_READ_FINISHED_19 and stop.")
prepared = {"status": "prepared-one-native-project-plugin-duplicate-control", "source_revision": 37, "source_lock_hash": probe.EXPECTED,
    "project": str(probe.PROJECT), "package": stage["package"], "plugin": str(plugin), "model": probe.MODEL,
    "effort": "xhigh", "port": None, "selected_relative": relative, "fixture_before_sha256": probe.digest_file(fixture),
    "prompt": prompt, "marker": "NCKH_DUPLICATE_READ_FINISHED_19", "maximum_model_turns": 1,
    "maximum_prompt_submissions": 1, "maximum_requested_native_tools": 1, "events": list(probe.EVENTS),
    "fixture_origin": "controller-owned-synthetic-marker-only", "fault_origin": "none",
    "definition": probe.bind(RUN / "definitions/session.json"), "context_sha256": probe.digest_file(probe.EVIDENCE / "context-allow.json"),
    "control_sha256": probe.digest_file(probe.EVIDENCE / "probe-control.json"), "runtime": probe.bind(runtime),
    "controller": probe.bind(Path(__file__)), "global_direct_write": False, "installed_update": "not-performed",
    "plugin_route": "installed CLI --plugin-dir; native support must be observed", "official_format_source": "https://cursor.com/docs/reference/plugins"}
probe.atomic_json(RUN / "preparation.json", prepared)
probe.atomic_json(RUN / "frozen-brief.json", prepared)
print(json.dumps({"status": prepared["status"], "plugin": str(plugin), "events": prepared["events"]}))
