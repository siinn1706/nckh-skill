"""Select controller context and bind actual effects without retrying model turns."""

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owned_direct_mutation_case", RUN / "cursor-direct-mutation-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
action, name = sys.argv[1:]
prep = probe.read(RUN / "preparation.json")
case = next(c for c in prep["cases"] if c["case"] == name)
fixture = probe.contained(probe.PROJECT, prep["relative"])
assert probe.digest_file(probe.CONFIG) == probe.read(RUN / "definitions/session.json")["config_sha256"]
if action == "select":
    assert not (RUN / f"control-{name}.json").exists()
    if name == "deny":
        assert (RUN / "case-allow.json").is_file()
    context = {**probe.read(probe.EVIDENCE / ("context-allow.json" if name == "allow" else "context-deny.json")),
               "task_id": "native-cursor-direct-mutation-14-" + name}
    policy_preimage = [p.name for p in sorted((probe.EVIDENCE / "policy-receipts").glob("*.json"))]
    failure_preimage = [p.name for p in sorted((probe.EVIDENCE / "native-failures").glob("*.json"))]
    probe.atomic_json(probe.EVIDENCE / "context-active.json", context)
    with (RUN / f"fixture-{name}-before.txt").open("xb") as stream:
        stream.write(fixture.read_bytes())
    control = {"selected_at": datetime.now(timezone.utc).isoformat(), "context": context,
        "context_file_sha256": probe.digest_file(probe.EVIDENCE / "context-active.json"),
        "policy_preimage": policy_preimage, "failure_preimage": failure_preimage,
        "before_sha256": probe.digest_file(fixture), "fixture_before": probe.bind(RUN / f"fixture-{name}-before.txt"),
        "case": case, "session_id": 66223}
    probe.atomic_json(RUN / f"control-{name}.json", control)
    probe.atomic_json(RUN / f"prompt-intent-{name}.json", {"timestamp_utc": control["selected_at"], "prompt": case["prompt"],
        "session_id": 66223, "case": name, "maximum_case_prompt_submissions": 1})
    print(json.dumps({"case": name, "prompt": case["prompt"], "before_sha256": control["before_sha256"]}))
elif action == "collect":
    assert not (RUN / f"case-{name}.json").exists()
    control = probe.read(RUN / f"control-{name}.json")
    assert probe.digest_file(probe.EVIDENCE / "context-active.json") == control["context_file_sha256"]
    policies = [{**probe.bind(p), "receipt": probe.read(p)} for p in sorted((probe.EVIDENCE / "policy-receipts").glob("*.json"))
                if p.name not in control["policy_preimage"]]
    assert all(p["receipt"].get("context_hash") == control["context_file_sha256"] for p in policies)
    failures = [{**probe.bind(p), "record": probe.read(p)} for p in sorted((probe.EVIDENCE / "native-failures").glob("*.json"))
                if p.name not in control["failure_preimage"]]
    matches = []
    for p in policies:
        r = p["receipt"]
        if r["phase"] not in {"preflight", "pre-delivery"}:
            continue
        tools = []
        for tool in ("Read", "Write", "Edit", "StrReplace", "Shell"):
            neutral = {"schema_version": 1, "phase": r["phase"], "host": "cursor", "tool": tool, "paths": [prep["relative"]],
                       "session_key": r["session_key"], "task_key": r["task_key"], "artifact_sha256": r["artifact_sha256"], "stop_active": False}
            if probe.digest_record(neutral) == r["event_hash"]:
                tools.append(tool)
        matches.append({"policy": p, "neutral_tool_matches": tools})
    terminals = [{**probe.bind(p), "response": probe.read(p)} for p in sorted(RUN.glob(f"terminal-{name}-poll-*.json"))
                 if "recording-failure" not in p.name]
    marker = any("  " + case["marker"] + "\u001b[K" in t["response"]["output"] for t in terminals)
    with (RUN / f"fixture-{name}-after.txt").open("xb") as stream:
        stream.write(fixture.read_bytes())
    after = probe.digest_file(fixture)
    record = {"case": name, "mode": case["mode"], "control": probe.bind(RUN / f"control-{name}.json"),
        "before_sha256": control["before_sha256"], "after_sha256": after,
        "requested_sha256": probe.digest_bytes(case["requested_bytes"].encode()), "bytes_changed": after != control["before_sha256"],
        "requested_bytes_observed": fixture.read_bytes() == case["requested_bytes"].encode(),
        "final_marker_observed": marker, "policies": policies, "native_failures": failures,
        "neutral_tool_matches": matches, "terminal": [{k:v for k,v in t.items() if k != "response"} for t in terminals],
        "fixture_after": probe.bind(RUN / f"fixture-{name}-after.txt"), "source_lock_hash": probe.EXPECTED,
        "terminal_recording_losses": [probe.bind(p) for p in sorted(RUN.glob(f"terminal-{name}-poll-*-recording-failure.json"))],
        "terminal_truncated": any(t["response"].get("original_token_count", 0) > 8000 or
                                  t["response"]["output"].startswith("Warning: truncated output") for t in terminals),
        "native_policy_ID_correlation": "bounded-neutral-event-hashes; direct policy receipt omits native tool-use ID"}
    probe.atomic_json(RUN / f"case-{name}.json", record)
    print(json.dumps({"case": name, "changed": record["bytes_changed"], "requested_bytes_observed": record["requested_bytes_observed"],
        "final_marker": marker, "tools": [(r["policy"]["receipt"]["phase"],r["neutral_tool_matches"],r["policy"]["receipt"]["decision"]) for r in matches],
        "failure_count": len(failures)}))
else:
    raise ValueError("unknown action")
