"""Stage ten bounded native prompt/stop fault cases in the approved scratch project."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-1225-r36-cursor-interactive-attempt-06"
target = RUN / "cursor-prompt-stop-runtime.py"
assert not target.exists()
text = (BASE / "cursor-interactive-runtime.py").read_text(encoding="utf8")
assert text.count(".nckh-native-r36-cursor-interactive-06") == 2
text = text.replace(".nckh-native-r36-cursor-interactive-06", ".nckh-native-r36-cursor-prompt-stop-07")
compile(text, str(target), "exec")
with target.open("x", encoding="utf8") as stream:
    stream.write(text)
observer = (BASE / "cursor-file-observer.py").read_text(encoding="utf8")
assert observer.count("time.sleep(8)") == 1
observer = observer.replace("time.sleep(8)", "time.sleep(24)").replace(
    "intentional-test-sleep-eight-seconds", "intentional-test-sleep-twenty-four-seconds")
compile(observer, str(RUN / "cursor-file-observer.py"), "exec")
with (RUN / "cursor-file-observer.py").open("x", encoding="utf8") as stream:
    stream.write(observer)
with (RUN / "cursor-agy-model-dangerous-grant.json").open("xb") as stream:
    stream.write((BASE / "cursor-agy-model-dangerous-grant.json").read_bytes())
spec = importlib.util.spec_from_file_location("owned_prompt_stop_prepare", target)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.prepare()
stage = probe.read(RUN / "stage.json")
probe.atomic_json(probe.EVIDENCE / "probe-control.json", {
    "mode": "allow", "attempt": "startup", "selected_event": "none"})
config = json.loads(json.dumps(stage["preview"]["after"]))
for event, handlers in config["hooks"].items():
    assert len(handlers) == 1
    handlers[0]["command"] = subprocess.list2cmdline([
        sys.executable, "-I", str(probe.OBSERVER), "--host", "cursor", "--event", event,
        "--project", str(probe.PROJECT), "--evidence", str(probe.EVIDENCE), "--runner", stage["runner"]])
    handlers[0]["timeout"] = 20
probe.atomic_json(probe.CONFIG, config)
definition = {"status": "prepared-ten-interactive-fault-cases", "config_sha256": probe.digest_file(probe.CONFIG),
    "extra_configs": [], "config": config, "definition_kind": "instrumented-native-fault-test",
    "timeout_seconds": 20, "runner_timeout_seconds": 5, "timeout_injection_seconds": 24,
    "source_lock_hash": probe.EXPECTED, "attempt": "startup", "mode": "allow"}
probe.atomic_json(RUN / "definitions/session.json", definition)
probe.atomic_json(RUN / "last-definition.json", definition)
cases = []
for event in ("beforeSubmitPrompt", "stop"):
    for mode in ("malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec"):
        index = len(cases) + 1
        marker = f"NCKH_PROMPT_STOP_ORACLE_{index:02d}"
        cases.append({"index": index, "attempt": event + "-" + mode, "event": event, "mode": mode,
            "marker": marker, "maximum_prompt_submissions": 1,
            "prompt": f"Reply exactly {marker} and stop. Do not call any tool, inspect files, run commands, use agents, or change any file. This is an authorized synthetic native callback test."})
probe.atomic_json(RUN / "preparation.json", {"status": definition["status"], "maximum_model_turns": len(cases),
    "maximum_prompt_submissions": len(cases), "per_case_observation_timeout_seconds": 240,
    "source_revision": 36, "source_lock_hash": probe.EXPECTED, "source_modified": False,
    "model_requested": probe.MODEL, "effort_requested": "xhigh", "port": None,
    "controller": probe.bind(Path(__file__)), "base_controller": probe.bind(BASE / "cursor-interactive-runtime.py"),
    "observer": probe.bind(probe.OBSERVER), "definition": probe.bind(RUN / "definitions/session.json"),
    "input_protocol": "prompt-text-write-then-separate-carriage-return", "cases": cases})
print(json.dumps({"status": definition["status"], "maximum_model_turns": len(cases), "timeout_injection_seconds": 24}))
