"""Prepare one bounded sequence with genuine callback metadata and a byte oracle."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-1415-r36-cursor-existing-mutations-attempt-09"
read = lambda path: json.loads(path.read_text(encoding="utf8"))
brief = read(RUN / "frozen-brief.json")
assert not (RUN / "preparation.json").exists()
assert read(BASE / "cleanup.json")["status"] == "pass" and read(BASE / "final-process-audit.json")["matching_count"] == 0
target = RUN / "cursor-read-edit-runtime.py"
text = (BASE / "cursor-existing-runtime.py").read_text(encoding="utf8")
assert text.count(".nckh-native-r36-cursor-existing-09") == 2
text = text.replace(".nckh-native-r36-cursor-existing-09", ".nckh-native-r36-cursor-read-edit-10")
compile(text, str(target), "exec")
with target.open("x", encoding="utf8") as stream:
    stream.write(text)
with (RUN / "cursor-agy-model-dangerous-grant.json").open("xb") as stream:
    stream.write((BASE / "cursor-agy-model-dangerous-grant.json").read_bytes())
spec = importlib.util.spec_from_file_location("owned_cursor_read_edit_prepare", target)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
assert str(probe.PROJECT) == brief["project"] and probe.MODEL == brief["model"] and probe.EXPECTED == brief["source_lock_hash"]
probe.prepare()
metadata = probe.read(RUN / "native-metadata.json")
assert {row["id"]: row["value"] for row in metadata["selected_model"]["parameters"]}["fast"] == "false"
stage = probe.read(RUN / "stage.json")
config = json.loads(json.dumps(stage["preview"]["after"]))
for event, handlers in config["hooks"].items():
    assert len(handlers) == 1 and handlers[0]["timeout"] == 5
    handler = handlers[0]
    handler["command"] = subprocess.list2cmdline([sys.executable, "-X", "utf8", "-B", str(probe.OBSERVER),
        "--host", "cursor", "--event", event, "--project", str(probe.PROJECT), "--evidence", str(probe.EVIDENCE),
        "--runner", stage["runner"]])
    handler["timeout"] = 20
probe.atomic_json(probe.EVIDENCE / "probe-control.json", {"mode": "allow", "attempt": "read-edit-10", "selected_event": None,
                                                        "fault_origin": "none", "maximum_requested_tool_calls": 2})
probe.atomic_json(probe.CONFIG, config)
definition = {"config_sha256": probe.digest_file(probe.CONFIG), "config": config, "extra_configs": [],
              "definition_kind": "instrumented-native-callback-observer", "outer_timeout_seconds": 20,
              "packaged_runner_timeout_seconds": 5, "observer_invoked": True, "fault_origin": "none",
              "changes_from_preview": ["owned bounded callback observer", "instrumented outer timeout20s"],
              "source_lock_hash": probe.EXPECTED, "observer": probe.bind(probe.OBSERVER)}
probe.atomic_json(RUN / "definitions/session.json", definition)
probe.atomic_json(RUN / "last-definition.json", definition)
fixture = probe.contained(probe.PROJECT, brief["relative"])
assert not fixture.exists()
fixture.parent.mkdir(parents=True, exist_ok=True)
before = brief["before_text"].encode("utf8")
with fixture.open("xb") as stream:
    stream.write(before)
with (RUN / "fixture-preimage.txt").open("xb") as stream:
    stream.write(before)
marker = "NCKH_READ_EDIT_FINISHED_10"
prompt = ("In this authorized scratch project, make exactly two native tool calls in order: "
          "first Read the existing synthetic fixture oracles/r36-cursor-read-edit-public-10.txt; "
          "then use one available native file-edit tool to replace its entire contents with exactly "
          "NCKH_CURSOR_READ_EDIT_WRITE_10 followed by one newline. "
          "The fixture currently contains NCKH_CURSOR_READ_EDIT_FIXTURE_10 followed by one newline. "
          "Do not use shell, agents, other files, extra calls, retries or a workaround if a call is denied. "
          "All strings are synthetic native test markers. After the sequence or denial say " + marker + " and stop.")
probe.atomic_json(RUN / "preparation.json", {"status": "prepared-one-read-then-edit-control", "source_revision": 36,
    "source_lock_hash": probe.EXPECTED, "source_modified": False, "model_requested": probe.MODEL, "effort_requested": "xhigh",
    "maximum_prompt_submissions": 1, "maximum_model_turns": 1, "maximum_requested_tool_calls": 2,
    "per_case_observation_timeout_seconds": 240, "prompt": prompt, "marker": marker, "relative": brief["relative"],
    "before_sha256": probe.digest_file(fixture), "fixture_origin": "controller-owned-synthetic-native-markers",
    "fixture_preimage": probe.bind(RUN / "fixture-preimage.txt"), "outer_timeout_seconds": 20,
    "packaged_runner_timeout_seconds": 5, "observer_invoked": True, "fault_origin": "none", "port": None,
    "brief": probe.bind(RUN / "frozen-brief.json"), "definition": probe.bind(RUN / "definitions/session.json"),
    "controller": probe.bind(Path(__file__)), "runtime": probe.bind(target), "base_runtime": probe.bind(BASE / "cursor-existing-runtime.py")})
print(json.dumps({"status": "prepared-one-read-then-edit-control", "maximum_model_turns": 1, "requested_tool_calls": 2}))
