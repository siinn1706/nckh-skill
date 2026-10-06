"""Prepare existing synthetic files and direct packaged hooks for three native requests."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-1340-r36-cursor-direct-interactive-attempt-08"
read = lambda path: json.loads(path.read_text(encoding="utf8"))
brief = read(RUN / "frozen-brief.json")
assert brief["status"] == "planned-not-executed" and not (RUN / "preparation.json").exists()
assert read(BASE / "cleanup.json")["status"] == "pass"
assert read(BASE / "final-process-audit.json")["matching_count"] == 0
assert read(RUN / "report-correction.json")["status"] == "verified-factual-prose-correction"
target = RUN / "cursor-existing-runtime.py"
text = (BASE / "cursor-direct-runtime.py").read_text(encoding="utf8")
assert text.count(".nckh-native-r36-cursor-direct-08") == 2
text = text.replace(".nckh-native-r36-cursor-direct-08", ".nckh-native-r36-cursor-existing-09")
compile(text, str(target), "exec")
with target.open("x", encoding="utf8") as stream:
    stream.write(text)
with (RUN / "cursor-agy-model-dangerous-grant.json").open("xb") as stream:
    stream.write((BASE / "cursor-agy-model-dangerous-grant.json").read_bytes())
spec = importlib.util.spec_from_file_location("owned_cursor_existing_prepare", target)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
assert str(probe.PROJECT) == brief["project"] and probe.MODEL == brief["model"] and probe.EXPECTED == brief["source_lock_hash"]
probe.prepare()
metadata = probe.read(RUN / "native-metadata.json")
params = {row["id"]: row["value"] for row in metadata["selected_model"]["parameters"]}
assert params["fast"] == "false" and metadata["version"] == probe.read(BASE / "native-metadata.json")["version"]
stage = probe.read(RUN / "stage.json")
config = json.loads(json.dumps(stage["preview"]["after"]))
for handlers in config["hooks"].values():
    assert len(handlers) == 1 and handlers[0]["timeout"] == 5
    handler = handlers[0]
    assert str(probe.OBSERVER) not in handler["command"] and stage["runner"] in handler["command"]
    handler["command"] = handler["command"].replace("/context-allow.json", "/context-active.json").replace(
        "--receipt-dir .nckh-state/hooks/events/cursor", "--receipt-dir .nckh-native-r36-cursor-existing-09/policy-receipts")
probe.atomic_json(probe.CONFIG, config)
definition = {"config_sha256": probe.digest_file(probe.CONFIG), "config": config, "extra_configs": [],
              "definition_kind": "direct-packaged-runner", "timeout_seconds": 5, "observer_invoked": False,
              "changes_from_preview": ["owned active-context reference", "owned receipt namespace"], "source_lock_hash": probe.EXPECTED}
probe.atomic_json(RUN / "definitions/session.json", definition)
probe.atomic_json(RUN / "last-definition.json", definition)
cases = []
for frozen in brief["cases"]:
    path = probe.contained(probe.PROJECT, frozen["path"])
    assert not path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    before_bytes = brief["before_text"].encode("utf8")
    with path.open("xb") as stream:
        stream.write(before_bytes)
    fixture_path = RUN / "fixture-preimages" / (str(frozen["index"]) + ".txt")
    fixture_path.parent.mkdir(exist_ok=True)
    with fixture_path.open("xb") as stream:
        stream.write(before_bytes)
    marker = f"NCKH_EXISTING_FINISHED_{frozen['index']:02d}"
    prompt = ("Use the native Write tool exactly once in this authorized scratch project. "
              "Do not call another tool, read another file, use shell, use agents, retry, or work around denial. "
              "The selected existing file and both strings are synthetic native test markers. "
              "Replace the entire contents of " + frozen["path"] + " with exactly NCKH_CURSOR_EXISTING_WRITE_09 followed by one newline. "
              "The existing file currently contains NCKH_CURSOR_EXISTING_FIXTURE_09 followed by one newline. "
              f"After the one attempted call say {marker} and stop.")
    cases.append({"index": frozen["index"], "kind": frozen["tool_requested"], "mode": frozen["mode"],
                  "relative": frozen["path"], "marker": marker, "prompt": prompt,
                  "before_sha256": probe.digest_file(path), "preimage": probe.bind(fixture_path),
                  "expected": "exact-public-write" if frozen["index"] == 1 else "unchanged"})
probe.atomic_json(probe.EVIDENCE / "context-active.json", {
    **probe.read(probe.EVIDENCE / "context-allow.json"), "task_id": "native-cursor-existing-09-startup"})
selector = (BASE / "select-direct-case.py").read_text(encoding="utf8")
for old, new in (("cursor-direct-runtime.py", "cursor-existing-runtime.py"),
                 ("1 <= args.index <= 5", "1 <= args.index <= 3"),
                 ("native-cursor-direct-08-", "native-cursor-existing-09-"),
                 ("NCKH_CURSOR_DIRECT_08_WRITE", "NCKH_CURSOR_EXISTING_WRITE_09")):
    assert selector.count(old) == 1
    selector = selector.replace(old, new)
selector_path = RUN / "select-existing-case.py"
compile(selector, str(selector_path), "exec")
with selector_path.open("x", encoding="utf8") as stream:
    stream.write(selector)
diagnostic = (BASE / "diagnose-event-bindings.py").read_text(encoding="utf8")
assert diagnostic.count("cursor-direct-runtime.py") == 1
diagnostic = diagnostic.replace("cursor-direct-runtime.py", "cursor-existing-runtime.py")
diagnostic_path = RUN / "diagnose-event-bindings.py"
compile(diagnostic, str(diagnostic_path), "exec")
with diagnostic_path.open("x", encoding="utf8") as stream:
    stream.write(diagnostic)
probe.atomic_json(RUN / "preparation.json", {"status": "prepared-three-existing-file-native-requests",
    "source_revision": 36, "source_lock_hash": probe.EXPECTED, "source_modified": False, "cases": cases,
    "maximum_prompt_submissions": 3, "maximum_model_turns": 3, "model_turns_executed_at_preparation": 0,
    "per_case_observation_timeout_seconds": 240, "timeout_seconds": 5, "observer_invoked": False,
    "model_requested": probe.MODEL, "effort_requested": "xhigh", "port": None,
    "fixture_origin": "controller-owned-synthetic-native-markers", "fixtures_retained_for_effect-audit": True,
    "input_protocol": "prompt-text-write-then-separate-carriage-return", "brief": probe.bind(RUN / "frozen-brief.json"),
    "controller": probe.bind(Path(__file__)), "runtime": probe.bind(target), "selector": probe.bind(selector_path),
    "base_runtime": probe.bind(BASE / "cursor-direct-runtime.py"), "definition": probe.bind(RUN / "definitions/session.json")})
print(json.dumps({"status": "prepared-three-existing-file-native-requests", "model_turns": 0, "timeout_seconds": 5}))
