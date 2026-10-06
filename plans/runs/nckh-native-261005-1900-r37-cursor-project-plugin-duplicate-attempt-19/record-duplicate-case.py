"""Record genuine project/plugin callbacks without inferring missing invocations."""

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("duplicate_case_runtime", RUN / "cursor-duplicate-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
prep = probe.read(RUN / "preparation.json")
owner = probe.read(RUN / "native-process-ownership.json")
assert probe.digest_file(probe.CONFIG) == probe.read(RUN / "definitions/session.json")["config_sha256"]
assert probe.digest_file(probe.EVIDENCE / "context-allow.json") == prep["context_sha256"]
assert probe.digest_file(probe.EVIDENCE / "probe-control.json") == prep["control_sha256"]
fixture = probe.contained(probe.PROJECT, prep["selected_relative"])
assert fixture.read_bytes() == (RUN / "fixture-before.txt").read_bytes()
if sys.argv[1] == "select":
    assert not (RUN / "control-duplicate.json").exists()
    control = {"selected_at": datetime.now(timezone.utc).isoformat(), "session_id": owner["session_id"],
        "context_sha256": prep["context_sha256"], "fixture_before_sha256": prep["fixture_before_sha256"],
        "prompt": prep["prompt"], "maximum_prompt_submissions": 1,
        "startup_callbacks_included": True, "fault_origin": "none"}
    probe.atomic_json(RUN / "control-duplicate.json", control)
    probe.atomic_json(RUN / "prompt-intent-duplicate.json", control)
    print(json.dumps({"prompt": prep["prompt"], "session_id": owner["session_id"]}))
elif sys.argv[1] == "collect":
    assert not (RUN / "case-duplicate.json").exists()
    callbacks = [{**probe.bind(p), "observation": probe.read(p)} for p in sorted(
        (probe.EVIDENCE / "observations/duplicate-session").glob("*/*.json"))]
    policies = [{**probe.bind(p), "receipt": probe.read(p)} for p in sorted(
        (probe.EVIDENCE / "policy-receipts/duplicate-session").glob("*/*.json"))]
    assert all(p["receipt"].get("context_hash") == prep["context_sha256"] for p in policies)
    assert all(c["observation"]["control_sha256"] == prep["control_sha256"] for c in callbacks)
    assert all(c["observation"]["fault_origin"] == "none" for c in callbacks)
    rows = []
    for event in prep["events"]:
        event_callbacks = [c for c in callbacks if c["observation"]["event"] == event]
        source_counts = {source: len([c for c in event_callbacks if c["observation"]["callback_source"] == source])
            for source in ("project", "plugin")}
        event_policies = [p for p in policies if Path(p["path"]).parent.name == event]
        equivalent = len(event_callbacks) == 2 and all(c["observation"]["status"] == "completed"
            and c["observation"].get("runner_exited") and c["observation"].get("runner_exit_code") == 0
            and c["observation"].get("reported_event") == event
            and c["observation"].get("native_version") == probe.read(RUN / "native-metadata.json")["version"]
            for c in event_callbacks)
        if equivalent:
            left, right = (c["observation"] for c in event_callbacks)
            equivalent = all(left.get(k) == right.get(k) for k in (
                "native_session_hash", "native_tool_use_id", "native_tool_name", "input_sha256", "runner_output"))
        native_pair = source_counts == {"project": 1, "plugin": 1} and equivalent
        idempotent = native_pair and len(event_policies) == 1
        rows.append({"event": event, "callback_count": len(event_callbacks), "source_counts": source_counts,
            "native_pair_verified": native_pair, "single_policy_receipt_verified": idempotent,
            "callbacks": [{k:v for k,v in c.items() if k != "observation"} for c in event_callbacks],
            "policy_receipts": [{k:v for k,v in p.items() if k != "receipt"} for p in event_policies],
            "status": "verified-native-project-plugin-duplicate" if idempotent else "duplicate-invocation-unqualified"})
    terminals = [{**probe.bind(p), "response": probe.read(p)} for p in sorted(RUN.glob("terminal-duplicate-poll-*.json"))]
    marker = any("  " + prep["marker"] + "\u001b[K" in t["response"].get("output", "") for t in terminals)
    with (RUN / "fixture-after.txt").open("xb") as stream:
        stream.write(fixture.read_bytes())
    status = "verified-five-native-project-plugin-duplicate-events" if all(r["single_policy_receipt_verified"] for r in rows) else "native-project-plugin-duplicate-partial"
    case = {"status": status, "source_revision": 37, "source_lock_hash": probe.EXPECTED, "events": rows,
        "callbacks": callbacks, "policies": policies, "model": probe.MODEL, "fault_origin": "none",
        "fixture_unchanged": fixture.read_bytes() == (RUN / "fixture-before.txt").read_bytes(),
        "final_marker_observed": marker, "control": probe.bind(RUN / "control-duplicate.json"),
        "native_owner": probe.bind(RUN / "native-process-ownership.json"), "model_prompt_retries": 0,
        "terminal": [{k:v for k,v in t.items() if k != "response"} for t in terminals],
        "terminal_truncated": any(t["response"].get("original_token_count", 0) > 4000 or
            t["response"].get("output", "").startswith("Warning: truncated output") for t in terminals),
        "native_tool_return_content": "not-retained", "full_native_gate": "unchecked"}
    probe.atomic_json(RUN / "case-duplicate.json", case)
    print(json.dumps({"status": status, "events": [{k:v for k,v in r.items() if k not in {"callbacks", "policy_receipts"}} for r in rows],
        "fixture_unchanged": case["fixture_unchanged"], "final_marker_observed": marker}))
else:
    raise ValueError("Unknown action")
