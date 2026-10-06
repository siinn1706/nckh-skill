"""Verify four search attempts while keeping model refusals and native errors distinct."""

import hashlib
import json
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = WORK / "plans/runs/nckh-native-261005-0005-r34-attempt-01/projects/agy-model"
sys.path.insert(0, str(WORK / "nckh-kit"))
from core.build import verify_source_lock
from core.paths import contained, digest_record

read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {"path": p.relative_to(WORK).as_posix(), "sha256": sha(p)}


def bound(row):
    path = contained(WORK, row["path"])
    assert sha(path) == row["sha256"]
    return path


summary = read(RUN / "native-tool-summary.json")
brief = read(bound(summary["frozen_brief"]))
assert summary["status"] == "recorded-four-native-agy-search-tool-outcomes" and summary["model_turns"] == 4
assert len(brief["cases"]) == len(summary["results"]) == brief["maximum_model_turns"] == 4
assert summary["model_retries"] == 0 and brief["all_hook_timeouts_seconds"] == 5
assert digest_record(verify_source_lock(WORK / "nckh-kit")) == brief["source_lock_hash"]
rows = []
for case, result in zip(brief["cases"], summary["results"]):
    assert case["name"] == result["attempt"] and result["status"] == "failed-frozen-tool-oracle-retained"
    attempt_path = bound(result["receipt"])
    attempt = read(attempt_path)
    command = read(bound(attempt["command"]))
    assert command["process_exited"] and attempt["process_exited"] and command["exit_code"] == attempt["exit_code"] == 0
    assert command["timeout_seconds"] is None and command["capture_errors"] == []
    argv = command["command"]
    assert "--dangerously-skip-permissions" in argv and argv[argv.index("--model") + 1] == "gemini-3.8-flash-medium"
    assert argv[argv.index("--effort") + 1] == "medium" and argv[argv.index("--print-timeout") + 1] == "0"
    target = contained(PROJECT, case["target"])
    fixture = contained(PROJECT, case["fixture"])
    assert str(target) in argv[-1] and case["tool"] in argv[-1]
    assert fixture.read_bytes() == bytes.fromhex(case["expected_hex"])
    assert attempt["before"] == attempt["after"]
    command_name = "agy-tools-" + case["name"]
    stdout = RUN / "commands" / (command_name + ".stdout.txt")
    stderr = RUN / "commands" / (command_name + ".stderr.txt")
    assert sha(stdout) == command["stdout_sha256"] and sha(stderr) == command["stderr_sha256"]
    frames = [json.loads(s) for s in stdout.read_text(encoding="utf8").splitlines()]
    assert frames == attempt["native_frames"]
    init = [f for f in frames if f.get("event") == "init"]
    final = [f for f in frames if f.get("event") == "result"]
    assert len(init) == len(final) == 1
    assert init[0]["init"]["model"] == "gemini-3.8-flash-medium" and init[0]["init"]["permission_mode"] == "always-proceed"
    assert Path(init[0]["init"]["cwd"]).resolve() == PROJECT.resolve()
    assert final[0]["result"]["num_turns"] == 1 and final[0]["result"]["status"] == "SUCCESS"
    conversation = init[0]["conversation_id"]
    assert final[0]["result"]["conversation_id"] == conversation
    terminal = [f["step_update"] for f in frames if f.get("event") == "step_update" and f["step_update"].get("step_type") ==
                "tool" and f["step_update"].get("state") in ("DONE", "ERROR")]
    assert terminal == attempt["terminal_tools"] and len(terminal) <= 1
    error = None
    if terminal:
        assert terminal[0]["tool_name"] == case["tool"] and terminal[0]["conversation_id"] == conversation
        error = terminal[0]["tool_info"].get("error", {}).get("message")
    policies = [read(bound(p)) for p in attempt["policy_receipts"]]
    preflight = [p for p in policies if p["phase"] == "preflight"]
    pre_delivery = [p for p in policies if p["phase"] == "pre-delivery"]
    assert not preflight and not pre_delivery
    kind = "genuine-native-unknown-tool" if terminal and terminal[0]["state"] == "ERROR" and error and "unknown tool" in error else \
           "model-only-no-native-tool" if not terminal else "other-native-outcome-unqualified"
    rows.append({"attempt": case["name"], "tool": case["tool"], "private": case["private"],
        "conversation_id": conversation, "observation": kind, "native_error": error,
        "native_tool_count": len(terminal), "preflight_count": 0, "pre_delivery_count": 0, "fixture_unchanged": True,
        "enforcement": "unqualified", "original_oracle": result["status"], "receipt": bind(attempt_path)})
assert len({r["conversation_id"] for r in rows}) == 4
cleanup = read(RUN / "cleanup.json")
audit = read(RUN / "process-final-audit.json")
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 26 and not cleanup["config_callable"]
assert all(r["sha256"] == r["current_sha256"] for r in cleanup["protected_global_config"])
assert audit["matching_count"] == audit["tracked_live_count"] == 0 and not audit["process_stop_performed"]
output = {"status": "verified-four-native-search-attempts-with-failed-oracles", "source_revision": 37,
    "source_lock_hash": brief["source_lock_hash"], "host": "agy-cli", "host_version": "1.2.17",
    "model_observed": "gemini-3.8-flash-medium", "effort_requested": "medium", "model_turns": 4, "model_retries": 0,
    "results": rows, "genuine_unknown_tool_count": sum(r["observation"] == "genuine-native-unknown-tool" for r in rows),
    "model_only_count": sum(r["observation"] == "model-only-no-native-tool" for r in rows), "full_native_gate": "unchecked",
    "source_modified": False, "summary": bind(RUN / "native-tool-summary.json"), "frozen_brief": bind(RUN / "frozen-brief.json"),
    "cleanup": bind(RUN / "cleanup.json"), "process_audit": bind(RUN / "process-final-audit.json"), "verifier": bind(Path(__file__))}
with (RUN / "verified-search-delivery.json").open("x", encoding="utf8") as stream:
    json.dump(output, stream, ensure_ascii=False, indent=2)
print(json.dumps({"status": output["status"], "genuine_unknown_tool_count": output["genuine_unknown_tool_count"],
                  "model_only_count": output["model_only_count"], "tracked_identities": len(audit["tracked"])}))
