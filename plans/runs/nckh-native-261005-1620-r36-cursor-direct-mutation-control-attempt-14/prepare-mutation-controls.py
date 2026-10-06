"""Stage two explicit native mutation controls after the direct Read timing result."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-1610-r36-cursor-direct-timeout-control-attempt-13"
read = lambda p: json.loads(p.read_text(encoding="utf8"))
assert not (RUN / "preparation.json").exists()
assert read(BASE / "cleanup.json")["status"] == "pass" and read(BASE / "final-process-audit.json")["matching_count"] == 0
runtime = RUN / "cursor-direct-mutation-runtime.py"
source = (BASE / "cursor-direct-timeout-runtime.py").read_text(encoding="utf8")
assert source.count(".nckh-native-r36-cursor-direct-timeout-13") == 2
source = source.replace(".nckh-native-r36-cursor-direct-timeout-13", ".nckh-native-r36-cursor-direct-mutation-14")
compile(source, str(runtime), "exec")
with runtime.open("x", encoding="utf8") as stream:
    stream.write(source)
for name in ("cursor-agy-model-dangerous-grant.json", "reconcile-native-processes.ps1"):
    with (RUN / name).open("xb") as stream:
        stream.write((BASE / name).read_bytes())
spec = importlib.util.spec_from_file_location("owned_direct_mutation_prepare", runtime)
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
        "--receipt-dir .nckh-state/hooks/events/cursor", "--receipt-dir .nckh-native-r36-cursor-direct-mutation-14/policy-receipts")
    if event == "preToolUse":
        handler["timeout"] = 20
relative = "oracles/r36-cursor-direct-mutation-control-14.txt"
logger = RUN / "native-failure-observer.py"
logger_text = (BASE / "native-failure-observer.py").read_text(encoding="utf8")
assert 'native.get("tool_name") == "Read"' in logger_text
logger_text = logger_text.replace('native.get("tool_name") == "Read"', 'native.get("tool_name") in {"Read", "Write", "Edit", "StrReplace"}')
logger_text = logger_text.replace("selected_read_path_matches", "selected_path_matches").replace("scrubbed_selected_read_error", "scrubbed_selected_error")
compile(logger_text, str(logger), "exec")
with logger.open("x", encoding="utf8") as stream:
    stream.write(logger_text)
config["hooks"]["postToolUseFailure"] = [{"type": "command", "command": subprocess.list2cmdline([
    sys.executable, "-X", "utf8", "-B", str(logger), "--evidence", str(probe.EVIDENCE),
    "--project", str(probe.PROJECT), "--selected-relative", relative]), "timeout": 10}]
probe.atomic_json(probe.EVIDENCE / "context-active.json", {**read(probe.EVIDENCE / "context-allow.json"),
                                                        "task_id": "native-cursor-direct-mutation-14-startup"})
probe.atomic_json(probe.CONFIG, config)
definition = {"config_sha256": probe.digest_file(probe.CONFIG), "config": config, "extra_configs": [],
    "definition_kind": "direct-packaged-runner-preToolUse20s-mutation-controls", "preToolUse_timeout_seconds": 20,
    "other_packaged_timeout_seconds": 5, "diagnostic_event": "postToolUseFailure", "diagnostic_timeout_seconds": 10,
    "diagnostic_logger": probe.bind(logger), "observer_invoked_for_packaged_events": False,
    "source_lock_hash": probe.EXPECTED, "source_default_unchanged": True}
probe.atomic_json(RUN / "definitions/session.json", definition)
probe.atomic_json(RUN / "last-definition.json", definition)
fixture = probe.contained(probe.PROJECT, relative)
assert not fixture.exists()
fixture.parent.mkdir(parents=True, exist_ok=True)
with fixture.open("xb") as stream:
    stream.write(b"NCKH_CURSOR_DIRECT20_BEFORE_14\n")
with (RUN / "fixture-preimage.txt").open("xb") as stream:
    stream.write(fixture.read_bytes())
cases = []
for name, mode, text, marker in (("allow", "auto", "NCKH_CURSOR_DIRECT20_ALLOWED_14", "NCKH_DIRECT_MUTATION_ALLOWED_FINISHED_14"),
                                 ("deny", "plan-only", "NCKH_CURSOR_DIRECT20_DENIED_14", "NCKH_DIRECT_MUTATION_DENIED_FINISHED_14")):
    prompt = ("First use the native Read tool on " + relative + ". Then use one available native file-edit operation "
              "to replace the complete file contents with exactly " + text + " followed by one newline. "
              "This authorized scratch file contains only a synthetic test marker. Do not use shell, another file, agents, "
              "retry, or work around a failure or denial. After the attempted edit say " + marker + " and stop.")
    cases.append({"case": name, "mode": mode, "prompt": prompt, "marker": marker, "requested_bytes": text + "\n",
                  "requested_native_tool_use_identities_maximum": 2})
brief = {"source_revision": 36, "source_lock_hash": probe.EXPECTED, "model": probe.MODEL, "effort": "xhigh",
    "project": str(probe.PROJECT), "relative": relative, "fixture_origin": "controller-owned-synthetic-native-markers",
    "maximum_model_turns": 2, "maximum_prompt_submissions": 2, "cases": cases, "per_case_observation_timeout_seconds": 240,
    "preToolUse_timeout_seconds": 20, "other_packaged_timeout_seconds": 5,
    "purpose": "verify direct20s public write effect and plan-only Write prevention before deciding a source timeout repair",
    "base_read_control": probe.bind(BASE / "native-timeout-summary.json"), "port": None}
probe.atomic_json(RUN / "frozen-brief.json", brief)
probe.atomic_json(RUN / "preparation.json", {**brief, "status": "prepared-two-direct20s-mutation-controls",
    "source_modified": False, "source_default_unchanged": True, "before_sha256": probe.digest_file(fixture),
    "fixture_preimage": probe.bind(RUN / "fixture-preimage.txt"), "definition": probe.bind(RUN / "definitions/session.json"),
    "controller": probe.bind(Path(__file__)), "runtime": probe.bind(runtime), "brief": probe.bind(RUN / "frozen-brief.json")})
print(json.dumps({"status": "prepared-two-direct20s-mutation-controls", "maximum_model_turns": 2, "source_modified": False}))
