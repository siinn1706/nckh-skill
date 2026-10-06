"""Retain current native Stop callbacks, policy decisions and declared faults."""

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
PRIOR = RUN.parent / "nckh-native-261006-0253-r37-codex-posttool-controls-attempt-47"
EXPECTED = "629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb"
MARKER = b"NCKH_NATIVE_FILE_ORACLE\n"
MESSAGE = b"ORACLE_ATTEMPT_FINISHED"
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
    runtime_path = PRIOR / "codex-posttool-runtime.py"
    runtime = runtime_path.read_text(encoding="utf8").replace(
        ".nckh-native-codex-posttool-controls-47", ".nckh-native-codex-stop-controls-48")
    runtime = runtime.replace("selected_event='PostToolUse'", "selected_event='Stop'")
    needle = '    atomic_json(EVIDENCE / "control.json", {"attempt": attempt, "selected_event": selected_event, "mode": mode,'
    assert runtime.count(needle) == 1
    snapshot = '''    context_snapshot = RUN / "context-preimages" / (attempt + ".json")
    context_snapshot.parent.mkdir(parents=True, exist_ok=True)
    with context_snapshot.open("xb") as stream:
        stream.write((EVIDENCE / "context-allow.json").read_bytes())
'''
    runtime = runtime.replace(needle, snapshot + needle)
    observer_path = PRIOR / "codex-file-observer.py"
    observer = observer_path.read_text(encoding="utf8")
    needle = '    record["native_stop_hook_active"] = native.get("stop_hook_active")'
    assert observer.count(needle) == 1
    observer = observer.replace(needle, needle + '''
    if args.event == "Stop":
        last_message = native.get("last_assistant_message")
        record["native_last_assistant_message_type"] = type(last_message).__name__
        if isinstance(last_message, str):
            message_bytes = last_message.encode("utf8")
            record["native_last_assistant_message_bytes"] = len(message_bytes)
            record["native_last_assistant_message_sha256"] = sha(message_bytes)
''')
    for name, source in (("codex-stop-runtime.py", runtime), ("codex-file-observer.py", observer)):
        target = RUN / name
        compile(source, str(target), "exec")
        with target.open("x", encoding="utf8") as stream:
            stream.write(source)
    for name in ("owned-cli-command.py", "model-medium-grant.json"):
        with (RUN / name).open("xb") as stream:
            stream.write((PRIOR / name).read_bytes())
    audit = (PRIOR / "audit-owned-processes.ps1").read_text(encoding="utf8")
    audit = audit.replace("nckh-native-261006-0330-r37-agy-tool-route-inspection-attempt-46", PRIOR.name).replace("2018", "2164")
    with (RUN / "audit-owned-processes.ps1").open("x", encoding="utf8") as stream:
        stream.write(audit)
    save_new(RUN / "controller-adaptation.json", {
        "source_runtime": bind(runtime_path), "source_observer": bind(observer_path),
        "runtime": bind(RUN / "codex-stop-runtime.py"), "observer": bind(RUN / "codex-file-observer.py"),
        "source_kit_modified": False, "controller": bind(Path(__file__)),
        "changes": ["select genuine Stop callback", "bounded hash-only last_assistant_message witness",
            "retain raw per-case context bytes before invocation", "distinct evidence and marker namespaces"],
        "observed_payload_basis": bind(PRIOR / "attempts/posttool-allow.json"),
        "payload_fields_used": ["last_assistant_message", "stop_hook_active"],
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    })
    print(json.dumps({"status": "prepared-controller", "event": "Stop", "model_prompts": 0}), flush=True)


def reconcile_children(owned):
    expected = {}
    for path in (RUN / "commands").glob("*.process-tree.json"):
        tree = read(path)
        assert not tree["capture_errors"]
        for row in tree["processes"]:
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
    assert audit["matching_count"] == audit["tracked_live_count"] == 0 and len(audit["tracked"]) == 2164
    probe = load("codex_stop_runtime", RUN / "codex-stop-runtime.py")
    owned = load("codex_stop_owned", RUN / "owned-cli-command.py")
    probe.base.q.run_command = owned.run_command
    probe.check_source()
    version, stdout, stderr = owned.run_command("codex-version", probe.base.q.installed_commands()["codex"] + ["--version"], cwd=probe.PROJECT)
    assert version["exit_code"] == 0 and stdout.decode("utf8").strip() == "codex-cli 0.154.0"
    assert read(RUN / "model-medium-grant.json")["reasoning_effort"] == "medium"
    save_new(RUN / "frozen-brief.json", {
        "source_revision": 37, "source_lock_hash": EXPECTED, "model": "gpt-5.6-luna", "effort": "medium",
        "surface": "codex-cli-exec", "version": "0.154.0", "event": "Stop", "tool": "apply_patch", "modes": list(MODES),
        "maximum_requested_model_turns": 7, "maximum_requested_native_tools": 7, "model_retries": 0,
        "marker_bytes_hex": MARKER.hex(), "final_message_sha256": hashlib.sha256(MESSAGE).hexdigest(),
        "normal_policy_expected": "advisory/writing-resource-advice-only; Stop codec wire is empty object",
        "deny_policy_expected": "block/bounded-input-exceeded from33 controller-owned empty reference records; Stop codec wire is empty object",
        "oracle": "one exact native patch; matching pre/post identities; Stop observes already-present exact marker; retain message hash and repeat flag from actual input",
        "fault_origin": "five controller injections after genuine native Stop callbacks; none for allow/policy-deny",
        "outer_timeout_seconds": 5, "inner_timeout_seconds": 5, "injected_sleep_seconds": 8, "whole_turn_deadline": None,
        "trust_route": "reuse existing trusted project; inline invocation hook-trust bypass", "global_direct_writes": False,
        "new_trust_keys": "not-authorized", "scientific_QA": "unverified; synthetic marker only",
        "native_hook_notifications": "observe only what retained exec output exposes", "controller": bind(Path(__file__)),
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
            attempt = "stop-" + mode
            relative = "oracles/r37-codex-" + attempt + ".txt"
            row = probe.observe(mode, relative, attempt, selected_event="Stop")
            tracked = reconcile_children(owned)
            observations = sorted((probe.EVIDENCE / "observations" / attempt).glob("*/*.json"))
            receipts = sorted((probe.EVIDENCE / "policy-receipts" / attempt).glob("*/*.json"))
            final = {"attempt": attempt, "mode": mode, "selected_event": "Stop", "source_revision": 37, "source_lock_hash": EXPECTED,
                "native_exit_snapshot": bind(RUN / "attempts" / (attempt + ".json")),
                "context_preimage": bind(RUN / "context-preimages" / (attempt + ".json")),
                "final_callbacks": [bind(path) for path in observations], "final_policy_receipts": [bind(path) for path in receipts],
                "tracked_identities": tracked, "processes_live": 0, "marker_relative": relative,
                "marker_exists": (probe.PROJECT / relative).is_file(),
                "marker_exact": (probe.PROJECT / relative).is_file() and (probe.PROJECT / relative).read_bytes() == MARKER,
                "completed_at_utc": datetime.now(timezone.utc).isoformat()}
            save_new(RUN / "final-attempts" / (attempt + ".json"), final)
            callbacks = [read(path) for path in observations]
            pre = [item for item in callbacks if item["event"] == "PreToolUse"]
            post = [item for item in callbacks if item["event"] == "PostToolUse"]
            stops = [item for item in callbacks if item["event"] == "Stop"]
            result = {"attempt": attempt, "mode": mode, "pre_callbacks": len(pre), "post_callbacks": len(post),
                "stop_callbacks": len(stops), "marker_exists": final["marker_exists"], "marker_exact": final["marker_exact"],
                "native_exit": row["exit_code"], "final_snapshot": bind(RUN / "final-attempts" / (attempt + ".json"))}
            results.append(result)
            probe.atomic_json(RUN / "native-stop-summary.json", {"status": "running", "results": results, "source_lock_hash": EXPECTED})
            print(json.dumps(result), flush=True)
            assert len(pre) == len(post) == 1 and all(item.get("native_tool_name") == "apply_patch" and
                item.get("native_command_sha256") == row["requested_patch_sha256"] for item in pre + post), "Unexpected tool route; stop dependent turns"
            assert row["exit_code"] == 0 and row["process_exited"], "Native invocation failed; retain evidence and stop batch"
            assert stops, "Missing genuine Stop callback; retain outcome and stop batch"
        probe.atomic_json(RUN / "native-stop-summary.json", {"status": "recorded-seven-current-native-stop-cases", "results": results,
            "source_revision": 37, "source_lock_hash": EXPECTED, "full_native_gate": "unchecked"})
    except Exception as error:
        probe.atomic_json(RUN / "native-stop-failure.json", {"error_type": type(error).__name__, "error": str(error),
            "completed_cases": len(results), "raw_evidence_retained": True})
        raise
    finally:
        reconcile_children(owned)
        probe.cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["setup", "cases"])
    setup() if parser.parse_args().action == "setup" else cases()
