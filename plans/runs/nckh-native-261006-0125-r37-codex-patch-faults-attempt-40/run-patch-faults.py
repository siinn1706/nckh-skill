"""Observe file-tool failure paths using the existing native-trusted scratch project."""

import argparse
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-0710-r35-attempt-01/native-codex-file"
PRIOR = WORK / "plans/runs/nckh-native-261006-0110-r37-cursor-private-search-attempt-39"
EXPECTED = "629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb"
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime():
    probe = load("patch_fault_runtime", RUN / "codex-patch-runtime.py")
    owned = load("patch_fault_owned", RUN / "owned-cli-command.py")
    owned.RUN = RUN
    probe.base.q.run_command = owned.run_command
    return probe, owned


def setup():
    source = (BASE / "codex-native-files.py").read_text(encoding="utf8")
    source = source.replace("4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255", EXPECTED)
    source = source.replace(".nckh-native-r35-file", ".nckh-native-codex-patch-faults")
    source = source.replace('"source_revision": 35', '"source_revision": 37')
    source = source.replace('"native-codex-file-r35"', '"native-codex-file-control"')
    source = source.replace('timeout=240)', 'timeout=None)')
    receipt_fields = '"model_requested": MODEL, "effort_requested": "medium", "requested_native_tool": "apply_patch",'
    assert source.count(receipt_fields) == 1
    source = source.replace(receipt_fields, receipt_fields + '\n        "requested_patch_sha256": hashlib.sha256(patch.encode()).hexdigest(),')
    needle = 'atomic_json(EVIDENCE / "control.json", {"attempt": attempt, "selected_event": "PreToolUse", "mode": mode})'
    assert source.count(needle) == 1
    package = r"C:/Users/USER\.codex\visualizations\2026\10\04\01a104fc-f969-7f43-b1e0-1a6774f0e0c8\nckh-hooks-r37-1640-attempt-02\extracted\on-standalone\codex"
    begin = source.index('    pipeline = read(DELIVERY / "revalidation-summary.json")')
    end = source.index('    historical = ', begin)
    source = source[:begin] + source[end:]
    needle = '    package = Path(read(DELIVERY / "delivery-context.json")["outside"]) / "extracted/on-standalone/codex"'
    assert source.count(needle) == 1
    source = source.replace(needle, "    package = Path(" + repr(package) + ")")
    target = RUN / "codex-patch-runtime.py"
    assert not target.exists()
    compile(source, str(target), "exec")
    target.write_text(source, encoding="utf8")
    for name, original in (
        ("codex-file-observer.py", BASE / "codex-file-observer.py"),
        ("owned-cli-command.py", PRIOR / "owned-cli-command.py"),
        ("model-medium-grant.json", WORK / "plans/runs/nckh-native-261004-1707-attempt-01/model-medium-grant.json")):
        assert not (RUN / name).exists()
        (RUN / name).write_bytes(original.read_bytes())


def reconcile_children(owned):
    expected = {}
    for path in (RUN / "commands").glob("*.process-tree.json"):
        for row in read(path)["processes"]:
            expected[str(row["pid"]) + ":" + str(row["creation_filetime_ticks"])] = row
    started = time.monotonic()
    while True:
        live = [row for row in expected.values() if owned.creation_ticks(row["pid"]) == row["creation_filetime_ticks"]]
        if not live:
            return len(expected)
        if time.monotonic() - started > 30:
            raise RuntimeError("Observed descendant remains live; retain and reconcile before another native turn")
        time.sleep(0.25)


def cases():
    probe, owned = runtime()
    audit = read(RUN / "process-preflight-audit.json")
    assert audit["matching_count"] == audit["tracked_live_count"] == 0
    modes = ["malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec"]
    probe.check_source()
    version, stdout, stderr = owned.run_command("codex-version", probe.base.q.installed_commands()["codex"] + ["--version"], cwd=probe.PROJECT)
    assert version["exit_code"] == 0 and stdout.decode("utf8").strip() == "codex-cli 0.154.0"
    probe.atomic_json(RUN / "frozen-brief.json", {
        "source_revision": 37, "source_lock_hash": EXPECTED, "model": "gpt-5.6-luna", "effort": "medium",
        "surface": "codex-cli-exec", "version": "0.154.0", "event": "PreToolUse", "tool": "apply_patch",
        "modes": modes, "maximum_model_turns": 5, "maximum_requested_native_tools": 5, "model_retries": 0,
        "oracle": "One genuine matching patch callback per case; record native blocked/failed/completed state and exact marker outcome without regrading; no retries or alternate tools",
        "predicted_marker": {mode: mode != "malformed-input" for mode in modes},
        "fault_origin": "controller-injection-after-genuine-native-callback", "outer_timeout_seconds": 5,
        "inner_timeout_seconds": 5, "injected_sleep_seconds": 8, "whole_turn_deadline": None,
        "trust_route": "existing native-persisted workspace key reused; inline invocation hook trust bypass",
        "new_trust_keys": "not-authorized; global hashes must remain exact", "controller": probe.bind(Path(__file__))})
    probe.prepare()
    results = []
    try:
        for mode in modes:
            attempt = "patch-" + mode
            relative = "oracles/" + attempt + ".txt"
            row = probe.observe(mode, relative, attempt)
            selected = [c for c in row["native_callbacks"] if c["event"] == "PreToolUse"]
            exact = len(selected) == 1 and selected[0].get("native_tool_name") == "apply_patch"
            exact = exact and selected[0].get("native_command_sha256") == row["requested_patch_sha256"]
            tracked = reconcile_children(owned)
            results.append({"mode": mode, "attempt": attempt, "marker_exists": row["marker_exists"],
                "pretool_callbacks": len(selected), "actual_tool": selected[0].get("native_tool_name") if selected else None,
                "receipt": probe.bind(RUN / "attempts" / (attempt + ".json")), "tracked_identities": tracked,
                "process_exit": row["exit_code"]})
            probe.atomic_json(RUN / "native-patch-fault-summary.json", {"status": "running", "results": results,
                "source_lock_hash": EXPECTED, "full_native_gate": "unchecked"})
            assert exact, "Frozen native tool/callback oracle failed; preserve and stop batch"
        probe.atomic_json(RUN / "native-patch-fault-summary.json", {"status": "recorded-five-native-patch-faults",
            "results": results, "source_revision": 37, "source_lock_hash": EXPECTED, "full_native_gate": "unchecked"})
    finally:
        reconcile_children(owned)
        probe.cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["setup", "cases"])
    setup() if parser.parse_args().action == "setup" else cases()
