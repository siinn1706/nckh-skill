"""Observe documented project/plugin duplication and unknown config-event admission."""

import argparse
import hashlib
import importlib.util
import json
import time
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-2340-r37-agy-stop-faults-attempt-36"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


probe = load("agy_duplicate_runtime", BASE / "agy-cli-runtime.py")
owned = load("agy_duplicate_owned", BASE / "owned-cli-command.py")
owned.RUN = RUN
probe.RUN = probe.q.RUN = RUN
probe.EVIDENCE = probe.PROJECT / ".nckh-native-r37-agy-duplicate-admission-37"
probe.OBSERVER = RUN / "agy-tool-observer.py"
probe.q.run_command = owned.run_command
probe.q.installed_commands = lambda: {"agy": [r"C:/Users/USER\AppData\Local\agy\bin\agy.exe"]}
PLUGIN = probe.PROJECT / ".agents/plugins/nckh-r37-native-duplicate37"
ORIGINAL_REGISTER = probe.register
active_case = None
SOURCE = b"NCKH_AGY_DUP_INITIAL\n"
REVISED = b"NCKH_AGY_DUP_REVISED\n"
UNKNOWN = "NckhUnsupportedNativeEvent"


def setup():
    rows = []
    for name in ("agy-tool-observer.py", "cursor-agy-model-dangerous-grant.json", "cli-route-user-decision.json",
                 "audit-owned-processes.ps1"):
        source = BASE / name
        target = RUN / name
        assert not target.exists()
        content = source.read_text(encoding="utf8")
        if name.endswith(".ps1"):
            content = content.replace("nckh-native-261005-2335-r37-agy-search-controls-attempt-35", BASE.name).replace(
                "prior native35 union audit", "prior native36 union audit")
        target.write_text(content, encoding="utf8")
        rows.append({"source": probe.bind(source), "target": probe.bind(target)})
    probe.atomic_json(RUN / "controller-adaptation.json", {"source_modified": False, "changes": rows,
        "scope": "two independent native cases in existing granted scratch; no global plugin install", "controller": probe.bind(Path(__file__))})


def register(attempt, deny_mode=False, direct=False):
    assert active_case and attempt == active_case["name"] and not deny_mode and not direct
    ORIGINAL_REGISTER(attempt, False, False)
    probe.atomic_json(probe.EVIDENCE / "probe-control.json", {"attempt": attempt,
        "mode": "duplicate" if active_case["kind"] == "project-plugin" else "allow", "selected_event": "PreToolUse",
        "allow_context": "context-allow.json", "deny_context": "context-deny.json"})
    definition = probe.read(RUN / "last-definition.json")
    group = next(iter(definition["config"].values()))
    if active_case["kind"] == "project-plugin":
        assert not PLUGIN.exists()
        plugin_group = json.loads(json.dumps(group))
        for event in probe.EVENTS:
            for row in plugin_group[event]:
                for handler in row.get("hooks", [row]):
                    handler["command"] += " --callback-source plugin"
        probe.atomic_json(PLUGIN / "plugin.json", {"name": "nckh-r37-native-duplicate37", "description": "Owned disposable native duplicate test"})
        probe.atomic_json(PLUGIN / "hooks.json", {"nckh-r37-native-plugin37": plugin_group})
        members = [{"path": p.relative_to(probe.PROJECT).as_posix(), "sha256": probe.digest_file(p)} for p in
                   (PLUGIN / "plugin.json", PLUGIN / "hooks.json")]
        probe.atomic_json(RUN / "plugin-definition.json", {"kind": "project-workspace-plugin", "members": members,
            "config": plugin_group, "global_install": False, "model_prompt": False})
    else:
        assert not (PLUGIN / "plugin.json").exists() and not (PLUGIN / "hooks.json").exists()
        handler = json.loads(json.dumps(group["Stop"][0]))
        assert "--event Stop" in handler["command"]
        handler["command"] = handler["command"].replace("--event Stop", "--event " + UNKNOWN)
        group[UNKNOWN] = [handler]
        probe.atomic_json(probe.CONFIG, definition["config"])
        definition["config_sha256"] = probe.digest_file(probe.CONFIG)
    definition["kind"] = active_case["kind"]
    probe.atomic_json(RUN / "definitions" / (attempt + ".json"), definition)
    probe.atomic_json(RUN / "last-definition.json", definition)


probe.register = register


def descendants(command_name):
    rows = probe.read(RUN / "commands" / (command_name + ".process-tree.json"))["processes"]
    begin = time.monotonic()
    while any(owned.creation_ticks(r["pid"]) == r["creation_filetime_ticks"] for r in rows):
        assert time.monotonic() - begin < 90, "Observed descendant still alive; stop dependent cases"
        time.sleep(0.25)
    probe.atomic_json(RUN / "commands" / (command_name + ".child-reconciliation.json"), {
        "same_process_live": 0, "wait_seconds": round(time.monotonic() - begin, 3), "process_stop_performed": False})


def cleanup_plugin():
    path = RUN / "plugin-definition.json"
    if not path.exists() or (RUN / "plugin-cleanup.json").exists():
        return
    members = probe.read(path)["members"]
    assert all(probe.digest_file(probe.contained(probe.PROJECT, row["path"])) == row["sha256"] for row in members)
    for row in members:
        probe.contained(probe.PROJECT, row["path"]).unlink()
    probe.atomic_json(RUN / "plugin-cleanup.json", {"status": "pass", "removed_members": members, "global_install": False})


def controls():
    global active_case
    assert probe.read(RUN / "process-preflight-audit.json")["tracked_live_count"] == 0
    assert probe.read(BASE / "model-admission.json")["model_admitted_in_current_inventory"]
    cases = [{"name": "project-plugin-duplicate", "kind": "project-plugin"},
             {"name": "unknown-config-event", "kind": "unknown-event-config"}]
    for case in cases:
        case["fixture"] = "oracles/r37-agy-duplicate37-" + case["name"] + ".txt"
        case.update(initial_hex=SOURCE.hex(), requested_hex=REVISED.hex())
    probe.atomic_json(RUN / "frozen-brief.json", {"source_revision": 37, "source_lock_hash": probe.EXPECTED,
        "cases": cases, "maximum_model_turns": 2, "model_retries": 0, "model": probe.MODEL, "effort": "medium",
        "dangerous": True, "outer_handler_timeout_seconds": 5, "inner_runner_timeout_seconds": 5,
        "model_inventory_reused": probe.bind(BASE / "model-admission.json"), "unknown_config_event": UNKNOWN,
        "unknown_scope": "native config admission only; no injected runner input/event and no assumption that host emits unknown event",
        "duplicate_oracle": "native project/plugin callbacks for same input, idempotent policy receipts, one actual tool execution",
        "controller": probe.bind(Path(__file__)), "observer": probe.bind(probe.OBSERVER), "global_plugin_install": False})
    probe.prepare()
    context = probe.read(probe.EVIDENCE / "context-allow.json")
    context["task_id"] = "native-agy-duplicate-admission-r37-37"
    probe.atomic_json(probe.EVIDENCE / "context-allow.json", context)
    stage = probe.read(RUN / "stage.json")
    stage["contexts"] = {p.name: probe.digest_file(p) for p in probe.EVIDENCE.glob("context-*.json")}
    probe.atomic_json(RUN / "stage.json", stage)
    summary = {"status": "running", "source_revision": 37, "source_lock_hash": probe.EXPECTED,
        "results": [], "frozen_brief": probe.bind(RUN / "frozen-brief.json"), "full_native_gate": "unchecked"}
    probe.atomic_json(RUN / "native-duplicate-summary.json", summary)
    try:
        for case in cases:
            active_case = case
            path = probe.contained(probe.PROJECT, case["fixture"])
            assert not path.exists()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(SOURCE)
            instructions = "TargetFile: " + str(path) + ". Overwrite: true. CodeContent must be decoded JSON " + json.dumps(
                REVISED.decode()) + ", with exactly one final LF byte. "
            row = probe.observe("write_to_file", path, case["name"], instructions, direct=False)
            descendants("agy-tools-" + case["name"])
            callbacks = sorted((probe.EVIDENCE / "observations" / case["name"]).glob("*/*.json"))
            policies = sorted((probe.EVIDENCE / "policy-receipts" / case["name"]).glob("*/*.json"))
            result = {"attempt": case["name"], "kind": case["kind"], "receipt": probe.bind(RUN / "attempts" / (case["name"] + ".json")),
                "callback_bindings": [probe.bind(p) for p in callbacks], "policy_bindings": [probe.bind(p) for p in policies],
                "native_states": [t["state"] for t in row["terminal_tools"]], "exact_revised_bytes": path.read_bytes() == REVISED,
                "callback_counts": {event: sum(probe.read(p)["event"] == event for p in callbacks) for event in (*probe.EVENTS, UNKNOWN)}}
            summary["results"].append(result)
            probe.atomic_json(RUN / "native-duplicate-summary.json", summary)
            print(json.dumps({k: result[k] for k in ("attempt", "native_states", "exact_revised_bytes", "callback_counts")}), flush=True)
            assert len(row["terminal_tools"]) <= 1 and all(t["tool_name"] == "write_to_file" for t in row["terminal_tools"])
            assert row["process_exited"], "Native process has not exited"
            cleanup_plugin()
        summary.update(status="recorded-native-agy-duplicate-and-config-admission", model_turns=2, model_retries=0)
        probe.atomic_json(RUN / "native-duplicate-summary.json", summary)
    except Exception as error:
        probe.atomic_json(RUN / "native-duplicate-failure.json", {"error_type": type(error).__name__, "error": str(error),
            "completed_cases": len(summary["results"]), "raw_evidence_retained": True})
        raise
    finally:
        cleanup_plugin()
        probe.cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["setup", "controls"])
    args = parser.parse_args()
    setup() if args.action == "setup" else controls()
