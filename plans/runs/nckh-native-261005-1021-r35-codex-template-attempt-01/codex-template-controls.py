"""Observe direct packaged template5s hooks in an already trusted scratch project."""

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-0710-r35-attempt-01/native-codex-file"
spec = importlib.util.spec_from_file_location("codex_template_native_base", BASE / "codex-native-files.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.RUN = RUN
probe.EVIDENCE = probe.PROJECT / ".nckh-native-r35-codex-template-01"
probe.DELIVERY = WORK / "plans/runs/nckh-native-261005-0710-r35-attempt-01"
probe.OBSERVER = RUN / "codex-file-observer.py"
probe.base.RUN = RUN
probe.base.PROJECT = probe.PROJECT
probe.base.q.RUN = RUN


def options():
    control = probe.read(probe.EVIDENCE / "control.json")
    definition = probe.read(RUN / "definition.json")
    context = "context-deny.json" if control["mode"] == "policy-deny" else "context-allow.json"
    groups = {}
    for event in probe.EVENTS:
        command = subprocess.list2cmdline([sys.executable, "-I", definition["runner"],
            "--host", "codex", "--event", event, "--project", str(probe.PROJECT),
            "--context", (probe.EVIDENCE.relative_to(probe.PROJECT) / context).as_posix(),
            "--receipt-dir", probe.EVIDENCE.relative_to(probe.PROJECT).as_posix()
            + "/policy-receipts/" + control["attempt"] + "/" + event])
        groups[event] = [{"matcher": ".*", "hooks": [{"type": "command", "timeout": 5, "command": command}]}]
    binding = {"hooks": groups, "timeout_seconds": 5, "definition_kind": "direct-packaged-runner",
        "source_lock_hash": probe.EXPECTED, "observer_invoked": False, "fault_origin": "none",
        "context_reference": (probe.EVIDENCE.relative_to(probe.PROJECT) / context).as_posix()}
    path = RUN / "definitions" / (control["attempt"] + ".json")
    assert not path.exists()
    probe.atomic_json(path, binding)
    argv = probe.base.options(probe.MODEL) + ["--dangerously-bypass-hook-trust", "-c", 'approval_policy="never"',
        "-c", 'sandbox_mode="danger-full-access"']
    for event, group in groups.items():
        argv += ["-c", "hooks." + event + "=" + probe.base.p.toml_value(group)]
    return argv


if __name__ == "__main__":
    assert not (RUN / "preparation.json").exists()
    shutil.copyfile(BASE / "codex-file-observer.py", probe.OBSERVER)
    probe.atomic_json(RUN / "preparation.json", {"maximum_model_turns": 3,
        "source_revision": 35, "source_lock_hash": probe.EXPECTED, "source_modified": False,
        "model_requested": probe.MODEL, "effort_requested": "medium", "timeout_seconds": 5,
        "observer_invoked": False, "fault_origin": "none", "existing_trusted_project": str(probe.PROJECT),
        "base_controller": probe.bind(BASE / "codex-native-files.py"), "controller": probe.bind(Path(__file__))})
    probe.prepare()
    probe.native_options = options
    historical = {p.relative_to(probe.PROJECT).as_posix(): probe.digest_file(p)
        for p in probe.PROJECT.rglob("*") if p.is_file() and not p.is_relative_to(probe.EVIDENCE)
        and "/.nckh-state/hooks/" not in p.as_posix()}
    probe.atomic_json(RUN / "historical-project-preimage.json", {"members": historical})
    results = []
    try:
        for mode, relative, attempt in (("allow", "oracles/r35-codex-template-allow.txt", "template-write-allow"),
            ("policy-deny", "oracles/r35-codex-template-deny.txt", "template-write-deny"),
            ("allow", "private/r35-codex-template-private.txt", "template-write-private")):
            row = probe.observe(mode, relative, attempt)
            definition = RUN / "definitions" / (attempt + ".json")
            policies = [{**probe.bind(p), "receipt": probe.read(p)} for p in sorted(
                (probe.EVIDENCE / "policy-receipts" / attempt).glob("*/*.json"))]
            results.append({"attempt": attempt, "receipt": probe.bind(RUN / "attempts" / (attempt + ".json")),
                "definition": probe.bind(definition), "policy_receipts": policies,
                "marker_created": row["marker_exists"], "observer_invoked": False, "fault_origin": "none"})
            probe.atomic_json(RUN / "direct-template-summary.json", {"status": "running", "results": results,
                "source_revision": 35, "source_lock_hash": probe.EXPECTED})
            preflight = [p["receipt"] for p in policies if p["receipt"].get("phase") == "preflight"]
            assert preflight, "No genuine preflight receipt; preserve native evidence"
            if mode == "policy-deny" or relative.startswith("private/"):
                assert not row["marker_exists"], "Denied marker created; preserve failure"
            else:
                assert row["marker_exists"], "Allow marker absent; preserve native failure"
        probe.atomic_json(RUN / "direct-template-summary.json", {"status": "recorded-native-direct-template-controls",
            "results": results, "source_revision": 35, "source_lock_hash": probe.EXPECTED,
            "timeout_seconds": 5, "observer_invoked": False, "fault_origin": "none", "source_modified": False})
    finally:
        probe.cleanup()
        assert all(probe.digest_file(probe.contained(probe.PROJECT, relative)) == expected
            for relative, expected in historical.items())
