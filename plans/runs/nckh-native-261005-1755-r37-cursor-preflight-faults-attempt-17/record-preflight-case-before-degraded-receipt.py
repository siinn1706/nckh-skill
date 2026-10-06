"""Select and collect explicit faults; preserve actual native response and limits."""

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("preflight_case_runtime", RUN / "cursor-preflight-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
action, number = sys.argv[1:]
case = next(c for c in probe.read(RUN / "preparation.json")["cases"] if c["index"] == int(number))
prep = probe.read(RUN / "preparation.json")
fixture = probe.contained(probe.PROJECT, prep["relative"])
assert probe.digest_file(probe.CONFIG) == probe.read(RUN / "definitions/session.json")["config_sha256"]
control_path = RUN / ("control-" + number + ".json")
if action == "select":
    assert not control_path.exists()
    if int(number) > 1:
        previous = probe.read(RUN / ("case-" + str(int(number)-1) + ".json"))
        assert previous["selected_observers_terminal"] and previous["model_reply_marker_observed"]
    context = {**probe.read(probe.EVIDENCE / "context-allow.json"), "task_id": "native-cursor-preflight-17-" + number}
    probe.atomic_json(probe.EVIDENCE / "context-allow.json", context)
    probe.atomic_json(probe.EVIDENCE / "probe-control.json", {"mode": case["mode"], "attempt": case["attempt"], "selected_event": "preToolUse"})
    control = {"selected_at": datetime.now(timezone.utc).isoformat(), "case": case,
        "context_sha256": probe.digest_file(probe.EVIDENCE / "context-allow.json"),
        "probe_control_sha256": probe.digest_file(probe.EVIDENCE / "probe-control.json"),
        "failure_preimage": [p.name for p in sorted((probe.EVIDENCE / "native-failures").glob("*.json"))],
        "direct_preimage": [p.name for p in sorted((probe.EVIDENCE / "direct-policy-receipts").glob("*.json"))],
        "before_sha256": probe.digest_file(fixture), "prompt_submissions_maximum": 1,
        "session_id": probe.read(RUN / "native-process-ownership.json")["session_id"]}
    probe.atomic_json(control_path, control)
    probe.atomic_json(RUN / ("prompt-intent-" + number + ".json"), control)
    print(json.dumps({"index": int(number), "prompt": case["prompt"], "session_id": control["session_id"]}))
elif action == "collect":
    target = RUN / ("case-" + number + ".json")
    assert not target.exists()
    control = probe.read(control_path)
    assert control["probe_control_sha256"] == probe.digest_file(probe.EVIDENCE / "probe-control.json")
    observations = [{**probe.bind(p), "record": probe.read(p)} for p in sorted(
        (probe.EVIDENCE / "observations" / case["attempt"] / "preToolUse").glob("*.json"))]
    terminal_statuses = {"completed", "intentional-test-crash-exit-17", "intentional-test-malformed-output"}
    observers_terminal = bool(observations) and all(o["record"]["status"] in terminal_statuses for o in observations)
    assert observers_terminal, "Keep selected context unchanged until the injected observer has completed or exited"
    for observation in observations:
        r = observation["record"]
        assert r["control_sha256"] == control["probe_control_sha256"] and r["fault_selected"]
        assert r["native_version"] == probe.read(RUN / "native-metadata.json")["version"]
        assert r["workspace_contains_selected_project"] and r["reported_event"] == "preToolUse"
        assert r["fault_origin"] == "controller-injection-after-genuine-callback"
    policies = [{**probe.bind(p), "receipt": probe.read(p)} for p in sorted(
        (probe.EVIDENCE / "policy-receipts" / case["attempt"] / "preToolUse").glob("*.json"))]
    direct = [{**probe.bind(p), "receipt": probe.read(p)} for p in sorted((probe.EVIDENCE / "direct-policy-receipts").glob("*.json"))
              if p.name not in control["direct_preimage"]]
    assert all(p["receipt"].get("context_hash") == control["context_sha256"] for p in policies + direct)
    failures = [{**probe.bind(p), "record": probe.read(p)} for p in sorted((probe.EVIDENCE / "native-failures").glob("*.json"))
                if p.name not in control["failure_preimage"]]
    selected_failures = [f for f in failures if f["record"].get("selected_path_matches") and f["record"].get("native_tool_name") == "Read"]
    post_matches = []
    for p in direct:
        r = p["receipt"]
        if r["phase"] != "pre-delivery":
            continue
        neutral = {"schema_version": 1, "phase": r["phase"], "host": "cursor", "tool": "Read", "paths": [prep["relative"]],
            "session_key": r["session_key"], "task_key": r["task_key"], "artifact_sha256": r["artifact_sha256"], "stop_active": False}
        if probe.digest_record(neutral) == r["event_hash"]:
            post_matches.append(p)
    terminals = [{**probe.bind(p), "response": probe.read(p)} for p in sorted(RUN.glob("terminal-case-" + number + "-poll-*.json"))]
    marker = any("  " + case["marker"] + "\u001b[K" in t["response"].get("output", "") for t in terminals)
    record = {"status": "collected-actual-native-preflight-fault", "case": case, "source_revision": 37,
        "source_lock_hash": probe.EXPECTED, "control": probe.bind(control_path), "observations": observations,
        "selected_observers_terminal": observers_terminal, "policy_receipts": policies, "direct_receipts": direct,
        "native_failures": failures, "selected_native_read_failures": len(selected_failures),
        "actual_selected_read_post_receipts": len(post_matches), "model_reply_marker_observed": marker,
        "fixture_before_sha256": control["before_sha256"], "fixture_after_sha256": probe.digest_file(fixture),
        "fixture_unchanged": probe.digest_file(fixture) == control["before_sha256"],
        "terminal": [{k:v for k,v in t.items() if k != "response"} for t in terminals],
        "terminal_truncated": any(t["response"].get("original_token_count", 0) > 4000 or
                                  t["response"].get("output", "").startswith("Warning: truncated output") for t in terminals),
        "fault_origin": "controller-injection-after-genuine-callback", "native_preflight_timeout_seconds": 20,
        "observer_runner_timeout_seconds": 5, "unsupported_scope": prep["unsupported_scope"],
        "prompt_retries": 0, "full_native_gate": "unchecked"}
    probe.atomic_json(target, record)
    print(json.dumps({"index": int(number), "mode": case["mode"], "callbacks": len(observations),
        "selected_native_read_failures": len(selected_failures), "actual_read_post_receipts": len(post_matches),
        "marker_observed": marker, "fixture_unchanged": record["fixture_unchanged"]}))
else:
    raise ValueError("Unknown action")
