"""Prepare instrumented native hooks for one genuine interactive CLI turn."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-1122-r36-cursor-acp-turns-attempt-04"
target = RUN / "cursor-interactive-runtime.py"
assert not target.exists()
text = (BASE / "cursor-acp-runtime.py").read_text(encoding="utf8")
old = 'EVIDENCE = PROJECT / ".nckh-native-r36-cursor-acp-04"'
new = 'EVIDENCE = PROJECT / ".nckh-native-r36-cursor-interactive-05"'
assert text.count(old) == 1
text = text.replace(old, new).replace(
    'context_reference=".nckh-native-r36-cursor-acp-04/context-allow.json"',
    'context_reference=".nckh-native-r36-cursor-interactive-05/context-allow.json"')
compile(text, str(target), "exec")
with target.open("x", encoding="utf8") as stream:
    stream.write(text)
for name in ("cursor-file-observer.py", "cursor-agy-model-dangerous-grant.json"):
    with (RUN / name).open("xb") as stream:
        stream.write((BASE / name).read_bytes())
spec = importlib.util.spec_from_file_location("r36_interactive_setup", target)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.prepare()
stage = probe.read(RUN / "stage.json")
fixture = probe.contained(probe.PROJECT, "oracles/r36-cursor-interactive-read-05.txt")
assert not fixture.exists()
fixture.parent.mkdir(parents=True, exist_ok=True)
fixture.write_bytes(b"NCKH_CURSOR_SYNTHETIC_READ_FIXTURE\n")
control = {"mode": "allow", "attempt": "interactive-public-read", "selected_event": "preToolUse"}
probe.atomic_json(probe.EVIDENCE / "probe-control.json", control)
config = json.loads(json.dumps(stage["preview"]["after"]))
for event, handlers in config["hooks"].items():
    assert len(handlers) == 1
    handlers[0]["command"] = subprocess.list2cmdline([sys.executable, "-I", str(probe.OBSERVER),
        "--host", "cursor", "--event", event, "--project", str(probe.PROJECT),
        "--evidence", str(probe.EVIDENCE), "--runner", stage["runner"]])
    handlers[0]["timeout"] = 20
probe.atomic_json(probe.CONFIG, config)
record = {"status": "prepared-one-interactive-model-turn", "config_sha256": probe.digest_file(probe.CONFIG),
    "extra_configs": [], "config": config, "definition_kind": "instrumented-native-test",
    "timeout_seconds": 20, "runner_timeout_seconds": 5, "fault_origin": "none",
    "source_lock_hash": probe.EXPECTED, "attempt": control["attempt"], "mode": "allow"}
probe.atomic_json(RUN / "definitions/interactive-public-read.json", record)
probe.atomic_json(RUN / "last-definition.json", record)
probe.atomic_json(RUN / "preparation.json", {"status": record["status"], "maximum_model_turns": 1,
    "source_revision": 36, "source_lock_hash": probe.EXPECTED, "source_modified": False,
    "model_requested": probe.MODEL, "effort_requested": "xhigh", "port": None,
    "controller": probe.bind(Path(__file__)), "base_controller": probe.bind(BASE / "cursor-acp-runtime.py"),
    "fixture_relative": fixture.relative_to(probe.PROJECT).as_posix(), "fixture_sha256": probe.digest_file(fixture),
    "prompt": "Use the native Read tool exactly once to read oracles/r36-cursor-interactive-read-05.txt in this authorized scratch project. This file contains a synthetic test marker only. Do not use a shell, another tool, agents, inspect another file, retry, or work around a denial. After the one attempted Read say ORACLE_ATTEMPT_FINISHED and stop."})
print(json.dumps({"status": record["status"], "source_modified": False, "maximum_model_turns": 1}))
