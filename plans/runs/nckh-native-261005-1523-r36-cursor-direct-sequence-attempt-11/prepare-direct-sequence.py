"""Prepare one direct-template sequence without an observation shim."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-1415-r36-cursor-existing-mutations-attempt-09"
PREVIOUS = WORK / "plans/runs/nckh-native-261005-1509-r36-cursor-read-edit-sequence-attempt-10"
read = lambda path: json.loads(path.read_text(encoding="utf8"))
brief = read(RUN / "frozen-brief.json")
assert not (RUN / "preparation.json").exists()
assert read(PREVIOUS / "cleanup.json")["status"] == "pass" and read(PREVIOUS / "final-process-audit.json")["matching_count"] == 0
assert read(PREVIOUS / "native-sequence-summary.json")["actual_effect"] == "exact-requested-replacement-bytes"
target = RUN / "cursor-direct-sequence-runtime.py"
text = (BASE / "cursor-existing-runtime.py").read_text(encoding="utf8")
assert text.count(".nckh-native-r36-cursor-existing-09") == 2
text = text.replace(".nckh-native-r36-cursor-existing-09", ".nckh-native-r36-cursor-direct-sequence-11")
compile(text, str(target), "exec")
with target.open("x", encoding="utf8") as stream:
    stream.write(text)
with (RUN / "cursor-agy-model-dangerous-grant.json").open("xb") as stream:
    stream.write((BASE / "cursor-agy-model-dangerous-grant.json").read_bytes())
spec = importlib.util.spec_from_file_location("owned_cursor_direct_sequence_prepare", target)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
assert str(probe.PROJECT) == brief["project"] and probe.MODEL == brief["model"] and probe.EXPECTED == brief["source_lock_hash"]
probe.prepare()
assert {row["id"]: row["value"] for row in probe.read(RUN / "native-metadata.json")["selected_model"]["parameters"]}["fast"] == "false"
stage = probe.read(RUN / "stage.json")
config = json.loads(json.dumps(stage["preview"]["after"]))
for handlers in config["hooks"].values():
    assert len(handlers) == 1 and handlers[0]["timeout"] == 5
    handler = handlers[0]
    assert str(probe.OBSERVER) not in handler["command"] and stage["runner"] in handler["command"]
    handler["command"] = handler["command"].replace("/context-allow.json", "/context-active.json").replace(
        "--receipt-dir .nckh-state/hooks/events/cursor", "--receipt-dir .nckh-native-r36-cursor-direct-sequence-11/policy-receipts")
probe.atomic_json(probe.EVIDENCE / "context-active.json", {**probe.read(probe.EVIDENCE / "context-allow.json"),
                                                         "task_id": "native-cursor-direct-sequence-11-startup"})
probe.atomic_json(probe.CONFIG, config)
definition = {"config_sha256": probe.digest_file(probe.CONFIG), "config": config, "extra_configs": [],
              "definition_kind": "direct-packaged-runner", "timeout_seconds": 5, "observer_invoked": False,
              "changes_from_preview": ["owned active-context reference", "owned receipt namespace"], "source_lock_hash": probe.EXPECTED}
probe.atomic_json(RUN / "definitions/session.json", definition)
probe.atomic_json(RUN / "last-definition.json", definition)
fixture = probe.contained(probe.PROJECT, brief["relative"])
assert not fixture.exists()
fixture.parent.mkdir(parents=True, exist_ok=True)
with fixture.open("xb") as stream:
    stream.write(brief["before_text"].encode("utf8"))
with (RUN / "fixture-preimage.txt").open("xb") as stream:
    stream.write(fixture.read_bytes())
marker = "NCKH_DIRECT_SEQUENCE_FINISHED_11"
prompt = ("In this authorized scratch project, make exactly two native tool calls in order: "
          "first Read the existing synthetic fixture oracles/r36-cursor-direct-sequence-public-11.txt; "
          "then use one available native file-edit tool to replace its entire contents with exactly "
          "NCKH_CURSOR_DIRECT_SEQUENCE_WRITE_11 followed by one newline. "
          "The fixture currently contains NCKH_CURSOR_DIRECT_SEQUENCE_FIXTURE_11 followed by one newline. "
          "Do not use shell, agents, other files, extra calls, retries or a workaround if a call is denied. "
          "All strings are synthetic native test markers. After the sequence or denial say " + marker + " and stop.")
probe.atomic_json(RUN / "preparation.json", {"status": "prepared-one-direct-read-then-edit-sequence", "source_revision": 36,
    "source_lock_hash": probe.EXPECTED, "source_modified": False, "model_requested": probe.MODEL, "effort_requested": "xhigh",
    "maximum_prompt_submissions": 1, "maximum_model_turns": 1, "maximum_requested_native_use_identities": 2,
    "per_case_observation_timeout_seconds": 240, "prompt": prompt, "marker": marker, "relative": brief["relative"],
    "before_sha256": probe.digest_file(fixture), "fixture_preimage": probe.bind(RUN / "fixture-preimage.txt"),
    "fixture_origin": "controller-owned-synthetic-native-markers", "timeout_seconds": 5, "observer_invoked": False,
    "fault_origin": "none", "port": None, "brief": probe.bind(RUN / "frozen-brief.json"),
    "definition": probe.bind(RUN / "definitions/session.json"), "controller": probe.bind(Path(__file__)),
    "runtime": probe.bind(target), "base_runtime": probe.bind(BASE / "cursor-existing-runtime.py")})
with (RUN / "reconcile-native-processes.ps1").open("xb") as stream:
    stream.write((PREVIOUS / "reconcile-native-processes.ps1").read_bytes())
print(json.dumps({"status": "prepared-one-direct-read-then-edit-sequence", "maximum_model_turns": 1, "timeout_seconds": 5}))
