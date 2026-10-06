"""Observe native Cursor faults and diagnose duplicate command identity without editing the kit."""

import argparse
import importlib.util
import json
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PRIOR = RUN.parent / "nckh-native-261005-0005-r34-attempt-01"
spec = importlib.util.spec_from_file_location("cursor_previous_probe", PRIOR / "cursor-agy-native-probe.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.RUN = RUN
probe.qualification.RUN = RUN
probe.OBSERVER = RUN / "cursor-native-observer.py"
current_project = RUN / "projects/main"
probe.project_for = lambda host: current_project
sys.path.insert(0, str(WORK / "nckh-kit"))
sys.dont_write_bytecode = True
from core.build import verify_source_lock
from core.paths import contained, digest_record

read = lambda path: json.loads(path.read_text(encoding="utf8"))
bind = lambda path: {"path": str(path.relative_to(RUN)), "sha256": probe.sha(path.read_bytes())}
source_check = probe.assert_source
register_original = probe.register


def assert_source():
    source_check()
    if digest_record(verify_source_lock(WORK / "nckh-kit")) != probe.EXPECTED_LOCK:
        raise RuntimeError("Pinned source differs; preserve native attempt instead of running a new revision")


probe.assert_source = assert_source


def register(host, mode, attempt):
    project, definition = register_original(host, mode, attempt)
    if attempt == "duplicate-distinct-command-01":
        plugin_hooks = project / "native-probe-plugin/hooks/hooks.json"
        probe.save(project / "definitions/duplicate-distinct-command-setup-preimage.json", {
            "definition": definition, "plugin_hooks": read(plugin_hooks), **bind(plugin_hooks)})
        config = read(plugin_hooks)
        for handler in config["hooks"][probe.SELECTED[host]]:
            handler["command"] += " --callback-source plugin"
        probe.save(plugin_hooks, config)
        definition["extra_configs"] = [
            {"path": item["path"], "sha256": probe.sha((project / item["path"]).read_bytes())}
            for item in definition["extra_configs"]]
        definition["duplicate_command_identity"] = "distinct observer source argument; identical packaged policy/receipt scope"
        probe.save(project / "definitions" / (attempt + ".json"), definition)
        probe.save(project / "last-definition.json", definition)
    return project, definition


probe.register = register


def summarize(attempt, selected_event=None):
    path = current_project / "attempts" / (attempt + ".json")
    record = read(path)
    command_receipt = Path(record["command_receipt"])
    raw_path = command_receipt.with_name(command_receipt.stem + ".stdout.txt")
    frames = []
    for line in raw_path.read_text(encoding="utf8").splitlines():
        try:
            frames.append(json.loads(line))
        except ValueError:
            pass
    callbacks = [(current_project / relative, read(current_project / relative)) for relative in record["observations"]]
    selected = [(target, row) for target, row in callbacks if row["event"] == selected_event]
    policies = sorted((current_project / "policy-receipts" / attempt / (selected_event or "preToolUse")).glob("*.json"))
    tools = []
    for frame in frames:
        if frame.get("type") != "tool_call" or frame.get("subtype") != "completed":
            continue
        call = frame.get("tool_call", {})
        for key, value in call.items():
            if not key.endswith("ToolCall") or not isinstance(value, dict):
                continue
            result = value.get("result", {})
            tools.append({"kind": key, "tool_call_id": call.get("toolCallId"),
                "result_keys": sorted(result), "result": result})
    return {"attempt": attempt, "event": selected_event, "mode": record["mode"], "status": record["status"],
        "exit_code": record["exit_code"], "process_exited": record["process_exited"],
        "oracle_created": record["oracle_created"], "oracle_sha256": record["oracle_sha256"],
        "oracle_retained": record["oracle_retained"], "attempt_binding": bind(path), "command_binding": bind(command_receipt),
        "invalid_stdout_lines": record["invalid_stdout_lines"], "completed_tool_items": tools,
        "callback_counts": {event: sum(row["event"] == event for _, row in callbacks) for event in probe.EVENTS["cursor"]},
        "native_model_ids": sorted({row["native_model_id"] for _, row in callbacks if row.get("native_model_id")}),
        "native_versions": sorted({row["native_version"] for _, row in callbacks if row.get("native_version")}),
        "selected_callback_count": len(selected), "callbacks": [
            {**bind(target), **{key: row.get(key) for key in ("event", "callback_source", "status", "started_at", "completed_at",
                "runner_exit_code", "native_tool_name", "native_tool_use_id", "native_model_id", "native_model_params",
                "runner_output", "fault_origin", "fault_selected")}} for target, row in callbacks],
        "selected_policy_receipts": [{**bind(target), "decision": read(target).get("decision")} for target in policies],
        "backend_model_attestation": "not-observed", "billing": "not-observed"}


def safe_cleanup(project):
    global current_project
    current_project = project
    stage = read(project / "stage.json")
    for item in stage["staged_members"]:
        path = contained(project, Path(item["path"]).as_posix())
        if not path.is_file() or probe.sha(path.read_bytes()) != item["sha256"]:
            raise RuntimeError("Owned member differs; preserve all files")
    config = contained(project, probe.TARGETS["cursor"])
    if config.is_file():
        definition = read(project / "last-definition.json")
        if probe.sha(config.read_bytes()) != definition["config_sha256"]:
            raise RuntimeError("Owned config differs; preserve")
        for item in definition["extra_configs"]:
            path = contained(project, Path(item["path"]).as_posix())
            if probe.sha(path.read_bytes()) != item["sha256"]:
                raise RuntimeError("Owned plugin differs; preserve")
    probe.cleanup("cursor")
    cleanup = read(project / "cleanup.json")
    if cleanup["config_callable"] or any(not row["unchanged"] for row in cleanup["protected_native_config"]):
        raise RuntimeError("Native protected state changed; retain evidence for review")


def batch():
    global current_project
    assert_source()
    probe.native_metadata()
    probe.save(RUN / "ownership.json", {"owner": "/root", "source_revision": 34, "source_lock_hash": probe.EXPECTED_LOCK,
        "model_requested": probe.MODELS["cursor"], "effort_requested": "xhigh", "dangerous_flags": ["--force", "--trust", "--sandbox disabled"],
        "work_context": str(WORK), "port": None, "global_plugin_install": "not-performed", "installed_update": "not-performed",
        "grant": bind(RUN / "cursor-agy-model-dangerous-grant.json"),
        "prior_probe": {"path": str((PRIOR / "cursor-agy-native-probe.py").relative_to(WORK)),
            "sha256": probe.sha((PRIOR / "cursor-agy-native-probe.py").read_bytes())},
        "observer": bind(probe.OBSERVER), "controller": bind(Path(__file__))})
    results = []
    projects = []
    unavailable_events = []
    summary_path = RUN / "native-summary.json"

    def save_summary(status, error=None):
        probe.save(summary_path, {"status": status, "source_revision": 34, "source_lock_hash": probe.EXPECTED_LOCK,
            "surface": "cursor-cli-print", "model_requested": probe.MODELS["cursor"], "effort_requested": "xhigh",
            "results": results, "unobserved_events": unavailable_events, "error": error,
            "native_gate": "remaining events/tools/IDE surface remain pending", "production_timing": "unqualified",
            "global_hooks": "existing configured native hooks remain enabled; no CLI isolation flag in observed help"})

    def observe(mode, attempt, event="preToolUse"):
        probe.SELECTED["cursor"] = event
        probe.observe("cursor", mode, attempt)
        result = summarize(attempt, event)
        results.append(result)
        save_summary("running")
        print(json.dumps({"attempt": attempt, "event": event, "mode": mode, "marker": result["oracle_created"],
            "selected_callbacks": result["selected_callback_count"], "tool_results": [row["result_keys"] for row in result["completed_tool_items"]]}), flush=True)
        if not result["process_exited"]:
            raise RuntimeError("Native process remains; reconcile before another attempt")
        return result

    save_summary("running")
    try:
        current_project = RUN / "projects/main"
        probe.prepare("cursor")
        projects.append(current_project)
        baseline = observe("allow", "allow-01")
        if not baseline["oracle_created"] or len(baseline["completed_tool_items"]) != 1:
            raise RuntimeError("Native baseline did not perform exactly one marker command; retain missing-route evidence")
        unavailable_events.extend(event for event, count in baseline["callback_counts"].items() if count == 0)
        observe("policy-deny", "policy-deny-01")
        observe("uncovered-tool", "uncovered-tool-01")
        for event in probe.EVENTS["cursor"]:
            if event in unavailable_events:
                continue
            for fault in ("malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec"):
                result = observe(fault, event.lower() + "-" + fault + "-01", event)
                if not result["selected_callback_count"]:
                    raise RuntimeError("Previously observed event missing; preserve and stop that route")
        for name in ("same-command", "distinct-command"):
            current_project = RUN / ("projects/duplicate-" + name)
            probe.SELECTED["cursor"] = "preToolUse"
            probe.prepare("cursor")
            projects.append(current_project)
            observe("duplicate", "duplicate-" + name + "-01")
        save_summary("recorded-native-cursor-events")
    except BaseException as error:
        save_summary("incomplete", {"type": type(error).__name__, "message": str(error)})
        raise
    finally:
        for project in projects:
            safe_cleanup(project)


parser = argparse.ArgumentParser()
parser.add_argument("action", choices=["batch"])
args = parser.parse_args()
batch()
