"""Observe each selected AGY event under declared faults after genuine callbacks."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("event_native_probe", RUN / "cursor-agy-native-probe.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
project = RUN / "projects/agy-event-faults"
probe.project_for = lambda host: project if host == "agy" else probe.RUN / "projects" / (host + "-model")
probe.assert_source()
package = Path(json.loads((RUN / "native-package-chains.json").read_text(encoding="utf8"))["packages"][0]["extracted"])
if package.name != "agy":
    raise RuntimeError("Select the verified AGY native archive explicitly")
probe.prepare("agy", package)
events = {"PreInvocation": "pre-invocation", "PreToolUse": "pre-tool-use", "PostToolUse": "post-tool-use",
          "PostInvocation": "post-invocation", "Stop": "stop"}
faults = ("malformed-input", "malformed-output", "timeout", "crash", "unsupported-codec")
results = []
summary_path = RUN / "agy-native-event-fault-summary.json"


def save_summary(status, error=None):
    probe.save(summary_path, {"status": status, "source_revision": 34, "source_lock_hash": probe.EXPECTED_LOCK,
        "project": str(project), "model_requested": probe.MODELS["agy"], "effort": "medium",
        "permission_mode": "dangerously-skip-permissions", "requested_events": list(events), "requested_faults": list(faults),
        "results": results, "error": error, "native_gate": "other host/surface gates remain open",
        "fault_origin": "explicit controller injection after genuine host callback; not host-generated malformed events",
        "effect_timing": "post events run after the native tool; existing oracle is not evidence of a prevention failure",
        "backend_model_attestation": "not-observed", "billing": "not-observed"})


save_summary("running")
try:
    for event, prefix in events.items():
        probe.SELECTED["agy"] = event
        for mode in faults:
            attempt = prefix + "-" + mode + "-01"
            probe.observe("agy", mode, attempt)
            path = project / "attempts" / (attempt + ".json")
            record = json.loads(path.read_text(encoding="utf8"))
            callbacks = [(project / relative, json.loads((project / relative).read_text(encoding="utf8")))
                         for relative in record["observations"]]
            selected = [(item, row) for item, row in callbacks if row["event"] == event and row["fault_selected"]]
            policies = sorted((project / "policy-receipts" / attempt / event).glob("*.json"))
            result = {"event": event, "fault": mode, "attempt": attempt, "native_command_status": record["status"],
                "exit_code": record["exit_code"], "process_exited": record["process_exited"],
                "oracle_created": record["oracle_created"], "oracle_retained": record["oracle_retained"],
                "selected_native_callback_count": len(selected), "selected_event_observed": bool(selected),
                "callback_outcomes": [{"path": str(item.relative_to(project)), "sha256": probe.sha(item.read_bytes()),
                    "status": row["status"], "runner_exit_code": row.get("runner_exit_code"),
                    "runner_output": row.get("runner_output"), "fault_origin": row["fault_origin"]} for item, row in selected],
                "policy_receipts": [{"path": str(item.relative_to(project)), "sha256": probe.sha(item.read_bytes())} for item in policies],
                "attempt_receipt": str(path.relative_to(RUN)), "attempt_sha256": probe.sha(path.read_bytes()),
                "command_receipt": record["command_receipt"], "invalid_stdout_lines": record["invalid_stdout_lines"]}
            results.append(result)
            save_summary("running")
            print(json.dumps({"event": event, "fault": mode, "callback_count": len(selected),
                              "oracle_created": record["oracle_created"], "native_exit": record["exit_code"]}), flush=True)
            if not selected:
                raise RuntimeError("Requested event produced no genuine callback; preserve evidence instead of repeating the missing route")
    save_summary("recorded-genuine-callbacks")
except BaseException as error:
    save_summary("incomplete", {"type": type(error).__name__, "message": str(error)})
    raise
finally:
    probe.cleanup("agy")
