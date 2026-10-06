"""Collect actual tool and policy observations without assuming the requested tool ran."""

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("uncovered_search_case", RUN / "cursor-uncovered-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
prep = probe.read(RUN / "preparation.json")
assert probe.digest_file(probe.CONFIG) == probe.read(RUN / "definitions/session.json")["config_sha256"]
assert probe.digest_file(probe.EVIDENCE / "context-uncovered.json") == prep["context_sha256"]
assert probe.digest_file(probe.EVIDENCE / "probe-control.json") == prep["control_sha256"]
if sys.argv[1] == "select":
    owner = probe.read(RUN / "native-process-ownership.json")
    assert not (RUN / "prompt-intent-search.json").exists()
    control = {"selected_at": datetime.now(timezone.utc).isoformat(), "session_id": owner["session_id"],
        "prompt": prep["prompt"], "expected_tool": prep["expected_native_tool"], "context_sha256": prep["context_sha256"],
        "maximum_prompt_submissions": 1, "maximum_requested_native_tools": 1, "fault_origin": "none"}
    probe.atomic_json(RUN / "prompt-intent-search.json", control)
    print(json.dumps({"prompt": prep["prompt"], "session_id": owner["session_id"]}))
elif sys.argv[1] == "collect":
    assert not (RUN / "case-uncovered-search.json").exists()
    callbacks = [{**probe.bind(p), "observation": probe.read(p)} for p in sorted(
        (probe.EVIDENCE / "observations/uncovered-search").glob("*/*.json"))]
    policies = [{**probe.bind(p), "receipt": probe.read(p)} for p in sorted(
        (probe.EVIDENCE / "policy-receipts/uncovered-search").glob("*/*.json"))]
    assert all(c["observation"]["control_sha256"] == prep["control_sha256"] and c["observation"]["fault_origin"] == "none" for c in callbacks)
    pre = [c["observation"] for c in callbacks if c["observation"]["event"] == "preToolUse"]
    post = [c["observation"] for c in callbacks if c["observation"]["event"] == "postToolUse"]
    native_pair = len(pre) == len(post) == 1
    if native_pair:
        left, right = pre[0], post[0]
        native_pair = all(row["status"] == "completed" and row["runner_exited"] and row["runner_exit_code"] == 0
            and row["native_tool_name"] == prep["expected_native_tool"] and row["native_tool_use_id"]
            and row["native_version"] == probe.read(RUN / "native-metadata.json")["version"]
            and row["workspace_contains_selected_project"] for row in (left, right))
        native_pair = native_pair and all(left.get(key) == right.get(key) for key in ("native_tool_use_id", "native_tool_name", "native_session_hash"))
        native_pair = native_pair and all(any(Path(value).resolve() == probe.contained(probe.PROJECT, prep["selected_relative"]).resolve()
            for value in row["native_path_fields"].values()) for row in (left, right))
    pre_policy = [p for p in policies if Path(p["path"]).parent.name == "preToolUse"]
    manual = len(pre_policy) == 1 and pre_policy[0]["receipt"].get("context_hash") == prep["context_sha256"]
    manual = manual and pre_policy[0]["receipt"].get("decision") == "manual" and pre_policy[0]["receipt"].get("reason_codes") == ["tool-route-uncovered"]
    no_deny = len(pre) == 1 and isinstance(pre[0].get("runner_output"), dict) and pre[0]["runner_output"].get("permission") != "deny"
    fixture = probe.contained(probe.PROJECT, prep["selected_relative"])
    unchanged = fixture.is_file() and probe.digest_file(fixture) == prep["fixture_sha256"]
    if fixture.is_file():
        (RUN / "fixture-after.txt").write_bytes(fixture.read_bytes())
    terminals = [{**probe.bind(p), "response": probe.read(p)} for p in sorted(RUN.glob("terminal-search-poll-*.json"))]
    marker = any("  " + prep["marker"] + "\u001b[K" in t["response"].get("output", "") for t in terminals)
    qualified = native_pair and manual and no_deny and unchanged and marker
    case = {"status": "verified-native-uncovered-search-manual-route" if qualified else "native-uncovered-search-unqualified",
        "source_revision": 37, "source_lock_hash": probe.EXPECTED, "model": probe.MODEL, "fault_origin": "none",
        "callbacks": callbacks, "policies": policies, "actual_tools": sorted({c["observation"]["native_tool_name"] for c in callbacks if c["observation"].get("native_tool_name")}),
        "preflight_count": len(pre), "post_count": len(post), "expected_native_tool_pair_verified": bool(native_pair),
        "manual_policy_verified": bool(manual), "native_deny_output_absent": bool(no_deny), "fixture_unchanged": unchanged,
        "final_marker_observed": marker, "terminal": [{key:value for key,value in t.items() if key != "response"} for t in terminals],
        "terminal_truncated": any(t["response"].get("original_token_count", 0) > 4000 or t["response"].get("output", "").startswith("Warning: truncated output") for t in terminals),
        "model_prompt_retries": 0, "original_oracle": prep["oracle"], "scope_limit": prep["scope_limit"], "full_native_gate": "unchecked"}
    probe.atomic_json(RUN / "case-uncovered-search.json", case)
    print(json.dumps({key:value for key,value in case.items() if key not in {"callbacks", "policies", "terminal", "model", "source_lock_hash", "original_oracle"}}))
else:
    raise ValueError("Unknown action")
