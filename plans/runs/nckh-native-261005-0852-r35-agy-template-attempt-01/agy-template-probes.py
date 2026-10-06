"""Run the two remaining direct packaged AGY template controls."""

import importlib.util
import json
import shutil
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-0848-r35-agy-tools-attempt-03"
spec = importlib.util.spec_from_file_location("agy_template_base", BASE / "agy-tool-probes.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.RUN = RUN
probe.q.RUN = RUN
probe.EVIDENCE = probe.PROJECT / ".nckh-native-r35-agy-template-01"
probe.OBSERVER = RUN / "agy-tool-observer.py"


if __name__ == "__main__":
    assert not (RUN / "preparation.json").exists()
    shutil.copyfile(BASE / "agy-tool-observer.py", probe.OBSERVER)
    shutil.copyfile(BASE / "cursor-agy-model-dangerous-grant.json", RUN / "cursor-agy-model-dangerous-grant.json")
    probe.atomic_json(RUN / "preparation.json", {
        "scope": "two direct packaged-runner template5s controls only",
        "earlier_tools_run": probe.bind(BASE / "native-tool-summary.json"),
        "base_controller": probe.bind(BASE / "agy-tool-probes.py"),
        "controller": probe.bind(Path(__file__)),
        "source_lock_hash": probe.EXPECTED,
        "model_requested": probe.MODEL,
        "effort_requested": "medium",
        "attempt_count_maximum": 2,
        "native_grant": "existing direct user grant in owned scratch project",
    })
    probe.prepare()
    ownership = probe.read(RUN / "ownership.json")
    ownership["controller"] = probe.bind(Path(__file__))
    ownership["base_controller"] = probe.bind(BASE / "agy-tool-probes.py")
    probe.atomic_json(RUN / "ownership.json", ownership)
    results = []
    try:
        for deny_mode in (False, True):
            attempt = "template-write-deny" if deny_mode else "template-write-allow"
            target = probe.contained(probe.PROJECT, "oracles/r35-agy-direct-" + attempt + ".txt")
            assert not target.exists()
            row = probe.observe("write_to_file", target, attempt,
                "TargetFile: " + str(target) + ". CodeContent: NCKH_AGY_REVISED. ",
                expected_deny=deny_mode, deny_mode=deny_mode, direct=True)
            results.append({"attempt": attempt, "receipt": probe.bind(RUN / "attempts" / (attempt + ".json"))})
            probe.atomic_json(RUN / "native-tool-summary.json", {"status": "running", "results": results,
                "source_lock_hash": probe.EXPECTED})
            assert len(row["terminal_tools"]) == 1 and row["terminal_tools"][0]["tool_name"] == "write_to_file"
            assert any(p["receipt"].get("phase") == "preflight" for p in row["policy_receipts"])
            if deny_mode:
                assert not target.exists() and row["terminal_tools"][0]["state"] == "ERROR"
            else:
                assert target.read_bytes() in {probe.REVISED_BYTES, probe.REVISED_BYTES.replace(b"\n", b"\r\n"), probe.REVISED_BYTES.rstrip(b"\n")}
                assert row["terminal_tools"][0]["state"] == "DONE"
        probe.atomic_json(RUN / "native-tool-summary.json", {"status": "recorded-native-agy-direct-template-controls",
            "results": results, "source_revision": 35, "source_lock_hash": probe.EXPECTED})
    finally:
        probe.cleanup()
