"""Run one public Read timing control with the user's exact Cursor model grant."""

import importlib.util
import json
import shutil
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-0818-r35-cursor-template-timing-attempt-01"
spec = importlib.util.spec_from_file_location("native_cursor_timing_base", BASE / "cursor-file-probes.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.RUN = RUN
probe.q.RUN = RUN
probe.EVIDENCE = probe.PROJECT / ".nckh-native-r35-cursor-immediate-diagnostic-01"
probe.OBSERVER = RUN / "cursor-immediate-hook.py"


def register(mode, attempt):
    assert mode == "allow"
    stage = probe.read(RUN / "stage.json")
    assert not probe.CONFIG.exists()
    config = json.loads(json.dumps(stage["preview"]["after"]))
    for event, handlers in config["hooks"].items():
        assert len(handlers) == 1 and handlers[0]["timeout"] == 5
        handlers[0]["command"] = " ".join((str(sys.executable), "-I", str(probe.OBSERVER),
            "--event", event, "--evidence", str(probe.EVIDENCE)))
    probe.atomic_json(probe.CONFIG, config)
    record = {"config_sha256": probe.digest_file(probe.CONFIG), "mode": mode, "attempt": attempt,
        "extra_configs": [], "config": config, "timeout_seconds": 5,
        "definition_kind": "immediate-diagnostic-only", "policy_invoked": False,
        "runner_invoked": False, "source_lock_hash": probe.EXPECTED,
        "diagnostic_callback": probe.bind(probe.OBSERVER)}
    probe.atomic_json(RUN / "definitions" / (attempt + ".json"), record)
    probe.atomic_json(RUN / "last-definition.json", record)
    return record


if __name__ == "__main__":
    assert not (RUN / "preparation.json").exists()
    shutil.copyfile(BASE / "cursor-agy-model-dangerous-grant.json", RUN / "cursor-agy-model-dangerous-grant.json")
    probe.atomic_json(RUN / "preparation.json", {"maximum_model_turns": 1,
        "purpose": "Separate immediate Python callback timing from NCKH policy processing",
        "timeout_seconds": 5, "source_modified": False, "model": probe.MODEL,
        "base_controller": probe.bind(BASE / "cursor-file-probes.py"), "controller": probe.bind(Path(__file__)),
        "public_read_only": True, "production_qualification": "not-established-by-diagnostic"})
    probe.prepare()
    probe.register = register
    target = probe.contained(probe.PROJECT, "oracles/r35-cursor-immediate-diagnostic-read.txt")
    assert not target.exists()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"NCKH_CURSOR_SYNTHETIC_READ_FIXTURE\n")
    try:
        row = probe.observe("Read", "allow", target.relative_to(probe.PROJECT).as_posix(), "immediate-read-allow")
        observations = [{**probe.bind(p), "receipt": probe.read(p)} for p in sorted(
            (probe.EVIDENCE / "immediate-observations").rglob("*.json"))]
        calls = row["completed_tool_calls"]
        response = calls[0]["tool_call"]["readToolCall"]["result"] if len(calls) == 1 else None
        probe.atomic_json(RUN / "diagnostic-summary.json", {"status": "recorded-native-timing-diagnostic",
            "attempt": probe.bind(RUN / "attempts/immediate-read-allow.json"), "native_result": response,
            "callbacks": observations, "source_revision": 35, "source_lock_hash": probe.EXPECTED,
            "source_modified": False, "fixture_unchanged": probe.digest_file(target) == row["before_sha256"],
            "scope": "Diagnostic control only; not production hook enforcement or timeout qualification"})
        print(json.dumps({"status": "recorded", "callbacks": len(observations), "native_result": response}), flush=True)
    finally:
        probe.cleanup()
