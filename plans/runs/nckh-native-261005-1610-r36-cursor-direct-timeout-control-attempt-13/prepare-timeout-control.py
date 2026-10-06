"""Declare one direct Read with only the preToolUse timing bound changed."""

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-1550-r36-cursor-direct-failure-observer-attempt-12"
read = lambda p: json.loads(p.read_text(encoding="utf8"))
assert not (RUN / "preparation.json").exists()
assert read(BASE / "cleanup.json")["status"] == "pass"
assert read(BASE / "final-process-audit.json")["matching_count"] == 0
original = read(BASE / "preparation.json")
runtime = RUN / "cursor-direct-timeout-runtime.py"
source = (BASE / "cursor-direct-failure-runtime.py").read_text(encoding="utf8")
assert source.count(".nckh-native-r36-cursor-direct-failure-12") == 2
source = source.replace(".nckh-native-r36-cursor-direct-failure-12", ".nckh-native-r36-cursor-direct-timeout-13")
compile(source, str(runtime), "exec")
with runtime.open("x", encoding="utf8") as stream:
    stream.write(source)
for name in ("cursor-agy-model-dangerous-grant.json", "native-failure-observer.py", "reconcile-native-processes.ps1"):
    with (RUN / name).open("xb") as stream:
        stream.write((BASE / name).read_bytes())
spec = importlib.util.spec_from_file_location("owned_timeout_control_prepare", runtime)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.prepare()
stage = read(RUN / "stage.json")
config = json.loads(json.dumps(stage["preview"]["after"]))
for event, handlers in config["hooks"].items():
    assert len(handlers) == 1 and handlers[0]["timeout"] == 5
    handler = handlers[0]
    assert str(probe.OBSERVER) not in handler["command"] and stage["runner"] in handler["command"]
    handler["command"] = handler["command"].replace("/context-allow.json", "/context-active.json").replace(
        "--receipt-dir .nckh-state/hooks/events/cursor", "--receipt-dir .nckh-native-r36-cursor-direct-timeout-13/policy-receipts")
    if event == "preToolUse":
        handler["timeout"] = 20
logger = RUN / "native-failure-observer.py"
config["hooks"]["postToolUseFailure"] = [{"type": "command", "command": subprocess.list2cmdline([
    sys.executable, "-X", "utf8", "-B", str(logger), "--evidence", str(probe.EVIDENCE),
    "--project", str(probe.PROJECT), "--selected-relative", original["relative"]]), "timeout": 10}]
probe.atomic_json(probe.EVIDENCE / "context-active.json", {**read(probe.EVIDENCE / "context-allow.json"),
                                                        "task_id": "native-cursor-direct-timeout-13-startup"})
probe.atomic_json(probe.CONFIG, config)
definition = {"config_sha256": probe.digest_file(probe.CONFIG), "config": config, "extra_configs": [],
    "definition_kind": "direct-packaged-runner-preToolUse20s-control", "preToolUse_timeout_seconds": 20,
    "other_packaged_timeout_seconds": 5, "diagnostic_event": "postToolUseFailure", "diagnostic_timeout_seconds": 10,
    "diagnostic_logger": probe.bind(logger), "observer_invoked_for_packaged_events": False,
    "source_lock_hash": probe.EXPECTED, "changes_from_native12": ["preToolUse timeout5s to20s",
        "new owned context task identity and receipt namespace; unchanged synthetic Read path"],
    "source_default_unchanged": True}
probe.atomic_json(RUN / "definitions/session.json", definition)
probe.atomic_json(RUN / "last-definition.json", definition)
fixture = probe.contained(probe.PROJECT, original["relative"])
assert probe.digest_file(fixture) == original["before_sha256"]
with (RUN / "fixture-preimage.txt").open("xb") as stream:
    stream.write(fixture.read_bytes())
prompt = original["prompt"].replace("NCKH_DIRECT_FAILURE_FINISHED_12", "NCKH_DIRECT_TIMEOUT_FINISHED_13")
preparation = {**original, "status": "prepared-declared-direct20s-preToolUse-control", "prompt": prompt,
    "marker": "NCKH_DIRECT_TIMEOUT_FINISHED_13", "timeout_seconds": 20, "source_default_unchanged": True,
    "fixture_preimage": probe.bind(RUN / "fixture-preimage.txt"), "controller": probe.bind(Path(__file__)),
    "runtime": probe.bind(runtime), "base_runtime": probe.bind(BASE / "cursor-direct-failure-runtime.py"),
    "definition": probe.bind(RUN / "definitions/session.json"), "base_observation": probe.bind(BASE / "native-failure-summary.json")}
preparation.pop("brief", None)
probe.atomic_json(RUN / "frozen-brief.json", {"experiment": "direct-preToolUse-timing-control", "base": probe.bind(BASE / "native-failure-summary.json"),
    "source_lock_hash": probe.EXPECTED, "model": probe.MODEL, "project": str(probe.PROJECT), "relative": original["relative"],
    "maximum_model_turns": 1, "maximum_prompt_submissions": 1, "maximum_requested_native_use_identities": 1,
    "observation_timeout_seconds": 240, "preToolUse_timeout_seconds": 20, "other_packaged_timeout_seconds": 5,
    "purpose": "qualify one bounded timing candidate after an actual native5s timeout; do not overwrite the failure or production default"})
preparation["brief"] = probe.bind(RUN / "frozen-brief.json")
probe.atomic_json(RUN / "preparation.json", preparation)
print(json.dumps({"status": preparation["status"], "maximum_model_turns": 1, "source_modified": False}))
