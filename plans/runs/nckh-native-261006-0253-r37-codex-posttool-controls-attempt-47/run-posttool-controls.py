"""Observe current packaged post-tool policy and faults on one native patch per case."""

import argparse
import hashlib
import importlib.util
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = RUN.parent / "nckh-native-261006-0125-r37-codex-patch-faults-attempt-40"
PRIOR = RUN.parent / "nckh-native-261006-0330-r37-agy-tool-route-inspection-attempt-46"
EXPECTED = "629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb"
MARKER = b"NCKH_NATIVE_FILE_ORACLE\n"
MODES = ("allow", "policy-deny", "malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec")
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}

def save_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def setup():
    source_path = BASE / "codex-patch-runtime.py"
    source = source_path.read_text(encoding="utf8")
    source = source.replace(".nckh-native-codex-patch-faults", ".nckh-native-codex-posttool-controls-47")
    needle = "    target.parent.mkdir(parents=True, exist_ok=True)\n        shutil.copyfile"
    # Match the actual staged-file indentation, then refuse collisions before any copy.
    needle = "        target.parent.mkdir(parents=True, exist_ok=True)\n        shutil.copyfile"
    assert source.count(needle) == 1
    source = source.replace(needle, "        assert not target.exists(), 'Preserve staged-file collision'\n" + needle)
    source = source.replace("def observe(mode, relative, attempt):", "def observe(mode, relative, attempt, selected_event='PostToolUse'):")
    needle = '    atomic_json(EVIDENCE / "control.json", {"attempt": attempt, "selected_event": "PreToolUse", "mode": mode})'
    assert source.count(needle) == 1
    replacement = '''    context = read(EVIDENCE / "context-allow.json")
    context["artifact_sha256"] = hashlib.sha256(b"NCKH_NATIVE_FILE_ORACLE\\n").hexdigest()
    context["artifact"] = {"path": relative, "sha256": context["artifact_sha256"]}
    atomic_json(EVIDENCE / "context-allow.json", context)
    definition["context_hashes"]["context-allow.json"] = digest_file(EVIDENCE / "context-allow.json")
    atomic_json(RUN / "definition.json", definition)
    atomic_json(EVIDENCE / "control.json", {"attempt": attempt, "selected_event": selected_event, "mode": mode,
        "marker_relative": relative, "expected_marker_sha256": context["artifact_sha256"]})'''
    source = source.replace(needle, replacement)
    target = RUN / "codex-posttool-runtime.py"
    assert not target.exists()
    compile(source, str(target), "exec")
    target.write_text(source, encoding="utf8")
    observer_path = BASE / "codex-file-observer.py"
    observer = observer_path.read_text(encoding="utf8")
    needle = "try:\n    native = json.loads(data)"
    assert observer.count(needle) == 1
    replacement = '''marker_relative = control["marker_relative"]
marker = args.project / marker_relative
marker.resolve().relative_to(args.project.resolve())
record["marker_exists_at_callback_start"] = marker.is_file()
if marker.is_file():
    assert marker.stat().st_size <= 256
    record["marker_at_callback_start_sha256"] = sha(marker.read_bytes())
record["controller_expected_marker_sha256"] = control["expected_marker_sha256"]
try:
    native = json.loads(data)
    record["native_stop_hook_active"] = native.get("stop_hook_active")'''
    observer = observer.replace(needle, replacement)
    target = RUN / "codex-file-observer.py"
    assert not target.exists()
    compile(observer, str(target), "exec")
    target.write_text(observer, encoding="utf8")
    for name, source_path in (
        ("owned-cli-command.py", PRIOR / "owned-cli-command.py"),
        ("model-medium-grant.json", BASE / "model-medium-grant.json"),
    ):
        target = RUN / name
        assert not target.exists()
        target.write_bytes(source_path.read_bytes())
    audit = (PRIOR / "audit-owned-processes.ps1").read_text(encoding="utf8")
    audit = audit.replace("nckh-native-261006-0300-r37-cursor-workspace-unsupported-event-attempt-45", PRIOR.name).replace("2008", "2018")
    audit = audit.replace("plans\\runs\\nckh-native-261005-0005-r34-attempt-01\\projects\\agy-model",
        "plans\\runs\\nckh-native-261005-0658-r34-codex-file-attempt-01\\project-02")
    with (RUN / "audit-owned-processes.ps1").open("x", encoding="utf8") as stream:
        stream.write(audit)
    save_new(RUN / "controller-adaptation.json", {
        "source_runtime": bind(BASE / "codex-patch-runtime.py"), "source_observer": bind(observer_path),
        "adapted_runtime": bind(RUN / "codex-posttool-runtime.py"), "adapted_observer": bind(RUN / "codex-file-observer.py"),
        "source_kit_modified": False,
        "changes": ["selected event PostToolUse", "prospective synthetic marker binding", "bounded synthetic marker snapshot at callback start",
            "staging collisions refused", "same native-trusted project/inline definitions", "seven independent modes; no model retries"],
        "timestamp_utc": datetime.now(timezone.utc).isoformat(), "controller": bind(Path(__file__)),
    })
    print(json.dumps({"status": "prepared-controller", "model_prompts": 0, "event": "PostToolUse"}), flush=True)

def reconcile_children(owned):
    expected = {}
    for path in (RUN / "commands").glob("*.process-tree.json"):
        for row in read(path)["processes"]:
            expected[str(row["pid"]) + ":" + str(row["creation_filetime_ticks"])] = row
    started = last_notice = time.monotonic()
    while True:
        live = [row for row in expected.values() if owned.creation_ticks(row["pid"]) == row["creation_filetime_ticks"]]
        if not live:
            return len(expected)
        now = time.monotonic()
        if now - last_notice >= 20:
            print(json.dumps({"status": "verified-descendant-wait", "same_process_live": len(live),
                "elapsed_seconds": round(now - started, 3)}), flush=True)
            last_notice = now
        time.sleep(0.25)

def cases():
    audit = read(RUN / "process-preflight-audit.json")
    assert audit["matching_count"] == audit["tracked_live_count"] == 0 and len(audit["tracked"]) == 2018
    probe = load("codex_posttool_runtime", RUN / "codex-posttool-runtime.py")
    owned = load("codex_posttool_owned", RUN / "owned-cli-command.py")
    probe.base.q.run_command = owned.run_command
    probe.check_source()
    version, stdout, stderr = owned.run_command("codex-version", probe.base.q.installed_commands()["codex"] + ["--version"], cwd=probe.PROJECT)
    assert version["exit_code"] == 0 and stdout.decode("utf8").strip() == "codex-cli 0.154.0"
    assert read(RUN / "model-medium-grant.json")["reasoning_effort"] == "medium"
    save_new(RUN / "frozen-brief.json", {
        "source_revision": 37, "source_lock_hash": EXPECTED, "model": "gpt-5.6-luna", "effort": "medium",
        "surface": "codex-cli-exec", "version": "0.154.0", "event": "PostToolUse", "tool": "apply_patch", "modes": list(MODES),
        "maximum_model_turns": 7, "maximum_requested_native_tools": 7, "model_retries": 0,
        "expected_marker_hex": MARKER.hex(), "expected_marker_exists": {mode: True for mode in MODES},
        "normal_policy_expected": "advisory/delivery-bindings-current-review-separate; declared synthetic artifact bytes only",
        "deny_policy_expected": "block/bounded-input-exceeded from33 controller-owned empty reference records; advisory wire after mutation",
        "oracle": "one genuine matching patch pre/post call; exact mutation before selected post callback; preserve native states/failures/late callbacks without regrading",
        "fault_origin": "controller-injection-after-genuine-native-callback for five fault modes; none for allow/policy-deny",
        "outer_timeout_seconds": 5, "inner_timeout_seconds": 5, "injected_sleep_seconds": 8, "whole_turn_deadline": None,
        "trust_route": "reuse existing native workspace key; inline invocation hook-trust bypass", "new_trust_keys": "not-authorized",
        "global_direct_writes": False, "scientific_QA": "not-claimed; synthetic marker binding only", "controller": bind(Path(__file__)),
    })
    probe.prepare()
    denied = read(probe.EVIDENCE / "context-deny.json")
    denied["brief"]["mode"] = "auto"
    denied["references"] = [{} for _ in range(33)]
    probe.atomic_json(probe.EVIDENCE / "context-deny.json", denied)
    definition = read(RUN / "definition.json")
    definition["context_hashes"]["context-deny.json"] = probe.digest_file(probe.EVIDENCE / "context-deny.json")
    probe.atomic_json(RUN / "definition.json", definition)
    results = []
    try:
        for mode in MODES:
            attempt = "posttool-" + mode
            relative = "oracles/r37-codex-" + attempt + ".txt"
            row = probe.observe(mode, relative, attempt, selected_event="PostToolUse")
            tracked = reconcile_children(owned)
            observations = sorted((probe.EVIDENCE / "observations" / attempt).glob("*/*.json"))
            receipts = sorted((probe.EVIDENCE / "policy-receipts" / attempt).glob("*/*.json"))
            final = {
                "attempt": attempt, "mode": mode, "selected_event": "PostToolUse", "source_revision": 37, "source_lock_hash": EXPECTED,
                "native_exit_snapshot": bind(RUN / "attempts" / (attempt + ".json")),
                "final_callbacks": [bind(path) for path in observations], "final_policy_receipts": [bind(path) for path in receipts],
                "tracked_identities": tracked, "processes_live": 0, "marker_relative": relative,
                "marker_exists": (probe.PROJECT / relative).is_file(), "marker_exact": (probe.PROJECT / relative).is_file() and (probe.PROJECT / relative).read_bytes() == MARKER,
                "completed_at_utc": datetime.now(timezone.utc).isoformat(),
            }
            save_new(RUN / "final-attempts" / (attempt + ".json"), final)
            pre = [read(path) for path in observations if read(path)["event"] == "PreToolUse"]
            post = [read(path) for path in observations if read(path)["event"] == "PostToolUse"]
            result = {"attempt": attempt, "mode": mode, "pre_callbacks": len(pre), "post_callbacks": len(post),
                "marker_exists": final["marker_exists"], "marker_exact": final["marker_exact"], "native_exit": row["exit_code"],
                "final_snapshot": bind(RUN / "final-attempts" / (attempt + ".json"))}
            results.append(result)
            probe.atomic_json(RUN / "native-posttool-summary.json", {"status": "running", "results": results, "source_lock_hash": EXPECTED})
            print(json.dumps(result), flush=True)
            assert len(pre) <= 1 and len(post) <= 1 and all(item.get("native_tool_name") == "apply_patch" and
                item.get("native_command_sha256") == row["requested_patch_sha256"] for item in pre + post), "Unexpected tool route; stop dependent turns"
            assert row["exit_code"] == 0 and row["process_exited"], "Native invocation failure; preserve and stop batch"
        probe.atomic_json(RUN / "native-posttool-summary.json", {"status": "recorded-seven-current-native-posttool-cases", "results": results,
            "source_revision": 37, "source_lock_hash": EXPECTED, "full_native_gate": "unchecked"})
    except Exception as error:
        probe.atomic_json(RUN / "native-posttool-failure.json", {"error_type": type(error).__name__, "error": str(error),
            "completed_cases": len(results), "raw_evidence_retained": True})
        raise
    finally:
        reconcile_children(owned)
        probe.cleanup()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["setup", "cases"])
    action = parser.parse_args().action
    setup() if action == "setup" else cases()
