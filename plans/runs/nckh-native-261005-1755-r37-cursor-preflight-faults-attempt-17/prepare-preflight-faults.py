"""Prepare five explicit preflight faults after genuine native Read callbacks."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-1740-r37-cursor-private-mutation-attempt-16"
OBSERVER_BASE = WORK / "plans/runs/nckh-native-261005-1257-r36-cursor-prompt-stop-faults-attempt-07/cursor-file-observer.py"
read = lambda p: json.loads(p.read_text(encoding="utf8"))
assert not (RUN / "preparation.json").exists()
assert read(BASE / "cleanup.json")["status"] == "pass" and read(BASE / "final-process-audit.json")["matching_count"] == 0
assert read(RUN / "process-preflight.json")["matching_count"] == 0
runtime = RUN / "cursor-preflight-runtime.py"
source = (BASE / "cursor-private-runtime.py").read_text(encoding="utf8").replace(
    ".nckh-native-r37-cursor-private-16", ".nckh-native-r37-cursor-preflight-faults-17")
old_observer = 'OBSERVER = WORK / "plans/runs/nckh-native-261005-1257-r36-cursor-prompt-stop-faults-attempt-07/cursor-file-observer.py"'
assert source.count(old_observer) == 1
source = source.replace(old_observer, 'OBSERVER = RUN / "cursor-file-observer.py"')
compile(source, str(runtime), "exec")
with runtime.open("x", encoding="utf8") as stream:
    stream.write(source)
for name in ("cursor-agy-model-dangerous-grant.json", "reconcile-native-processes.ps1", "native-failure-observer.py"):
    with (RUN / name).open("xb") as stream:
        stream.write((BASE / name).read_bytes())
with (RUN / "cursor-file-observer.py").open("xb") as stream:
    stream.write(OBSERVER_BASE.read_bytes())
spec = importlib.util.spec_from_file_location("preflight_fault_runtime", runtime)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.prepare()
stage = read(RUN / "stage.json")
probe.atomic_json(probe.EVIDENCE / "probe-control.json", {"mode": "allow", "attempt": "startup", "selected_event": "none"})
config = json.loads(json.dumps(stage["preview"]["after"]))
for event, handlers in config["hooks"].items():
    assert len(handlers) == 1 and handlers[0]["timeout"] == (20 if event == "preToolUse" else 5)
    handler = handlers[0]
    handler["command"] = handler["command"].replace("--receipt-dir .nckh-state/hooks/events/cursor",
        "--receipt-dir .nckh-native-r37-cursor-preflight-faults-17/direct-policy-receipts")
    if event == "preToolUse":
        handler["command"] = subprocess.list2cmdline([sys.executable, "-I", str(probe.OBSERVER), "--host", "cursor",
            "--event", event, "--project", str(probe.PROJECT), "--evidence", str(probe.EVIDENCE), "--runner", stage["runner"]])
relative = "oracles/r37-cursor-preflight-fault-read-17.txt"
logger = RUN / "native-failure-observer.py"
config["hooks"]["postToolUseFailure"] = [{"type": "command", "command": subprocess.list2cmdline([
    sys.executable, "-X", "utf8", "-B", str(logger), "--evidence", str(probe.EVIDENCE), "--project", str(probe.PROJECT),
    "--selected-relative", relative]), "timeout": 10}]
probe.atomic_json(probe.CONFIG, config)
definition = {"config_sha256": probe.digest_file(probe.CONFIG), "config": config, "extra_configs": [],
    "definition_kind": "instrumented-preToolUse-native-fault-controls-at-r37-default-20s-bound",
    "preToolUse_timeout_seconds": 20, "other_packaged_timeout_seconds": 5, "diagnostic_timeout_seconds": 10,
    "runner_timeout_seconds": 5, "timeout_injection_seconds": 24, "source_lock_hash": probe.EXPECTED,
    "packaged_direct_preflight": False, "fault_origin": "controller-injection-after-genuine-callback",
    "observer": probe.bind(probe.OBSERVER), "observer_source": probe.bind(OBSERVER_BASE)}
probe.atomic_json(RUN / "definitions/session.json", definition)
probe.atomic_json(RUN / "last-definition.json", definition)
fixture = probe.contained(probe.PROJECT, relative)
assert not fixture.exists()
fixture.parent.mkdir(parents=True, exist_ok=True)
with fixture.open("xb") as stream:
    stream.write(b"NCKH_CURSOR_R37_PREFLIGHT_PUBLIC_17\n")
with (RUN / "fixture-before.txt").open("xb") as stream:
    stream.write(fixture.read_bytes())
cases = []
for index, mode in enumerate(("malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec"), 1):
    marker = "NCKH_PREFLIGHT_FAULT_FINISHED_17_" + str(index)
    prompt = ("Use the native Read tool exactly once on " + relative + ". This file contains only a synthetic public "
        "marker in this authorized scratch project. Do not call shell, another tool, another file, agents, retry, or "
        "work around failure or denial. After the one attempted Read say " + marker + " and stop.")
    cases.append({"index": index, "mode": mode, "attempt": "preToolUse-" + mode, "event": "preToolUse",
                  "marker": marker, "prompt": prompt, "maximum_prompt_submissions": 1})
record = {"status": "prepared-five-preflight-fault-cases", "source_revision": 37, "source_lock_hash": probe.EXPECTED,
    "model": probe.MODEL, "effort": "xhigh", "maximum_model_turns": 5, "maximum_prompt_submissions": 5,
    "cases": cases, "relative": relative, "project": str(probe.PROJECT), "port": None,
    "before_sha256": probe.digest_file(fixture), "fault_origin": definition["fault_origin"],
    "unsupported_scope": "selected codec injection; actual native unsupported tool/event remains separate",
    "definition": probe.bind(RUN / "definitions/session.json"), "controller": probe.bind(Path(__file__)),
    "runtime": probe.bind(runtime), "runtime_parent": probe.bind(BASE / "cursor-private-runtime.py"),
    "global_direct_write": False, "full_native_gate": "unchecked", "installed_update": "not-performed"}
probe.atomic_json(RUN / "preparation.json", record)
probe.atomic_json(RUN / "frozen-brief.json", record)
print(json.dumps({"status": record["status"], "maximum_prompt_submissions": 5, "native_preflight_timeout_seconds": 20}))
