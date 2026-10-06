"""Select one unsubmitted case; inspect real callbacks without fabricating outcomes."""

import argparse
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owned_prompt_stop_control", RUN / "cursor-prompt-stop-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
parser = argparse.ArgumentParser()
parser.add_argument("action", choices=("select", "inspect", "record"))
parser.add_argument("index", type=int)
parser.add_argument("--terminal-rejection", type=Path)
args = parser.parse_args()
preparation = probe.read(RUN / "preparation.json")
case = preparation["cases"][args.index - 1]
assert case["index"] == args.index and 1 <= args.index <= 10
target = RUN / "attempts" / (case["attempt"] + ".json")
probe.check_source()
assert probe.digest_file(probe.CONFIG) == probe.read(RUN / "definitions/session.json")["config_sha256"]
if args.action == "select":
    assert not target.exists() and not (RUN / "submissions" / f"{args.index:02d}.json").exists()
    if args.index > 1:
        previous = preparation["cases"][args.index - 2]
        assert probe.read(RUN / "attempts" / (previous["attempt"] + ".json"))["ready_for_next_case"]
    probe.atomic_json(probe.EVIDENCE / "probe-control.json", {
        "mode": case["mode"], "attempt": case["attempt"], "selected_event": case["event"]})
    probe.atomic_json(RUN / "controls" / f"{args.index:02d}.json", {
        **case, "selected_at": datetime.now(timezone.utc).isoformat(),
        "control_sha256": probe.digest_file(probe.EVIDENCE / "probe-control.json"),
        "definition": probe.bind(RUN / "definitions/session.json")})
    print(json.dumps({"status": "selected-unsubmitted-case", "index": args.index, "event": case["event"], "mode": case["mode"], "prompt": case["prompt"]}))
else:
    paths = sorted((probe.EVIDENCE / "observations" / case["attempt"]).rglob("*.json"))
    callbacks = [{**probe.bind(path), "receipt": probe.read(path)} for path in paths]
    policies = [{**probe.bind(path), "receipt": probe.read(path)} for path in sorted(
        (probe.EVIDENCE / "policy-receipts" / case["attempt"]).rglob("*.json"))]
    selected = [binding["receipt"] for binding in callbacks if binding["receipt"]["event"] == case["event"]]
    stop = [binding["receipt"] for binding in callbacks if binding["receipt"]["event"] == "stop"]
    assert len(selected) <= 1
    ready = bool(stop)
    if selected and case["mode"] == "timeout":
        elapsed = (datetime.now(timezone.utc) - datetime.fromisoformat(selected[0]["started_at"])).total_seconds()
        ready = ready and elapsed >= 26
    elif selected:
        ready = ready and selected[0]["status"] != "entered-from-native-host"
    rejection = None
    if args.terminal_rejection is not None:
        terminal_path = probe.contained(RUN, args.terminal_rejection.as_posix())
        terminal = probe.read(terminal_path)
        assert args.action == "record" and case["event"] == "beforeSubmitPrompt"
        assert len(selected) == 1 and not stop
        output = selected[0].get("runner_output", {})
        assert isinstance(output, dict) and output.get("continue") is False
        reason = output.get("user_message")
        assert reason and "\n  " + reason in terminal["response"]["output"]
        assert terminal["response"].get("session_id") == 78282
        rejection = {"status": "native-admission-rejection-observed", "reason": reason,
                     "terminal": probe.bind(terminal_path), "model_turns_verified": 0}
        ready = True
    record = {**case, "source_revision": 36, "source_lock_hash": probe.EXPECTED, "callbacks": callbacks,
              "policy_receipts": policies, "selected_callback_count": len(selected), "stop_callback_count": len(stop),
              "ready_for_next_case": ready, "observed_at": datetime.now(timezone.utc).isoformat()}
    record["native_admission_rejection"] = rejection
    if args.action == "record":
        assert not target.exists() and ready
        probe.atomic_json(target, record)
    print(json.dumps({"action": args.action, "index": args.index, "event": case["event"], "mode": case["mode"],
        "selected_callback_count": len(selected), "stop_callback_count": len(stop), "ready_for_next_case": ready,
        "callbacks": [{"event": binding["receipt"]["event"], "status": binding["receipt"]["status"],
            "runner_output": binding["receipt"].get("runner_output")} for binding in callbacks]}))
