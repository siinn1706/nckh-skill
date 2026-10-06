"""Verify actual directory callbacks and keep missing native failure evidence explicit."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = WORK / "plans/runs/nckh-native-261005-0128-r34-cursor-events-attempt-02/projects/main"
EVIDENCE = PROJECT / ".nckh-native-r37-cursor-directory-search-49"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}


def bound(reference):
    path = WORK / reference["path"]
    assert sha(path) == reference["sha256"], "Retained evidence hash changed"
    return path


frozen = read(RUN / "frozen-brief.json")
stage = read(RUN / "stage.json")
metadata = read(RUN / "native-metadata.json")
definition = read(RUN / "definitions/session.json")
cleanup = read(RUN / "cleanup.json")
audit = read(RUN / "process-final-audit.json")
history = read(RUN / "historical-project-preimage.json")["members"]
assert read(RUN / "terminal-exit-poll-01.json")["exit_code"] == read(RUN / "monitor-exit.json")["exit_code"] == 0
assert read(RUN / "commands/native-cursor-directory-search.process-tree.json")["status"] == "root-exited-or-reused"
assert audit["matching_count"] == audit["tracked_live_count"] == 0 and audit["previous_union_count"] == 2310
assert cleanup["status"] == "pass" and len(cleanup["removed_members"]) == 28 and not cleanup["config_callable"]
assert len(history) == cleanup["historical_members_unchanged"] == 899
assert all(sha(PROJECT / relative) == expected for relative, expected in history.items())
assert all(not (PROJECT / member["path"]).exists() for member in cleanup["removed_members"])
assert all(row["current_sha256"] == row["sha256"] for row in cleanup["protected_global_config"])
callbacks = [{"binding": bind(path), "observation": read(path)} for path in sorted((EVIDENCE / "observations/directory-search").glob("*/*.json"))]
receipts = [{"binding": bind(path), "receipt": read(path)} for path in sorted((EVIDENCE / "policy-receipts/directory-search").glob("*/*.json"))]
assert len(callbacks) == len(receipts) == 6
runner_hash = next(member["sha256"] for member in stage["staged_members"] if member["path"].endswith("/hooks/runner.py"))
assert len({row["observation"]["native_session_hash"] for row in callbacks}) == 1
for row in callbacks:
    observation = row["observation"]
    assert observation["status"] == "completed" and observation["runner_exit_code"] == 0 and observation["runner_exited"]
    assert observation["fault_origin"] == "none" and observation["callback_source"] == "project"
    assert observation["runner_sha256"] == runner_hash and observation["control_sha256"] == frozen["control_sha256"]
    assert observation["reported_event"] == observation["event"] and observation["native_version"] == metadata["version"]
    assert observation["workspace_contains_selected_project"]
    assert observation["native_model"] == ("grok-4.7" if observation["event"] in {"preToolUse", "postToolUse"} else "grok-4.7-xhigh")
    assert observation["native_model_id"] is None and observation["native_model_params"] is None
for row in receipts:
    assert row["receipt"]["context_hash"] == frozen["context_sha256"] and row["receipt"]["side_effects"] == "none"
pre = [row["observation"] for row in callbacks if row["observation"]["event"] == "preToolUse"]
post = [row["observation"] for row in callbacks if row["observation"]["event"] == "postToolUse"]
assert len(pre) == 2 and len(post) == 1 and all(row["native_tool_name"] == "Grep" for row in pre + post)
assert len({row["native_tool_use_id"] for row in pre}) == 2 and all(row["native_tool_use_id"] for row in pre)
public_fixture, private_fixture = frozen["fixtures"]
public = next(row for row in pre if row["native_path_fields"] == {"file_path": public_fixture["directory"]})
private = next(row for row in pre if row["native_path_fields"] == {"file_path": private_fixture["directory"]})
assert public["native_search_scope_fields"] == {"file_path": public_fixture["directory"], "pattern": public_fixture["pattern"]}
assert private["native_search_scope_fields"] == {"file_path": private_fixture["directory"], "pattern": private_fixture["pattern"]}
assert public["runner_output"] == {} and private["runner_output"] == {"permission": "deny", "user_message": "private-holdout-credential-path"}
assert post[0]["native_tool_use_id"] == public["native_tool_use_id"] and post[0]["native_path_fields"] == public["native_path_fields"]
assert not any(row["native_tool_use_id"] == private["native_tool_use_id"] for row in post)
pre_policies = [row["receipt"] for row in receipts if row["receipt"]["phase"] == "preflight"]
assert sorted((row["decision"], row["reason_codes"][0]) for row in pre_policies) == [
    ("block", "private-holdout-credential-path"), ("manual", "tool-route-uncovered")]
for fixture in frozen["fixtures"]:
    before = (RUN / (fixture["label"] + "-fixture-before.txt")).read_bytes()
    after = (RUN / (fixture["label"] + "-fixture-after.txt")).read_bytes()
    assert before == after == bytes.fromhex(fixture["bytes_hex"]) and hashlib.sha256(before).hexdigest() == fixture["sha256"]
assert read(RUN / "terminal-prompt-text.json")["prompt"] == frozen["prompt"]
terminal_paths = sorted(RUN.glob("terminal-*.json"))
terminal_outputs = [read(path).get("output", read(path).get("result", {}).get("output", "")) for path in terminal_paths]
cleaned = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", "\n".join(terminal_outputs))
cleaned = re.sub(r"\x1b\][^\x07]*\x07", "", cleaned)
assert "Grok 4.7 500K Extra High" in read(RUN / "terminal-start.json")["output"]
assert "Run Everything" in read(RUN / "terminal-start.json")["output"]
assert "  " + frozen["marker"] in cleaned
assert len([row for row in callbacks if row["observation"]["event"] == "beforeSubmitPrompt"]) == 1
assert len([row for row in callbacks if row["observation"]["event"] == "stop"]) == 1
for event, handlers in definition["config"]["hooks"].items():
    assert len(handlers) == 1 and handlers[0]["timeout"] == (20 if event == "preToolUse" else 5)
assert definition["config"]["hooks"]["preToolUse"][0]["failClosed"]
record = {
    "status": "verified-current-Cursor-directory-Grep-scopes-and-policy-observations", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "source_revision": 37, "source_lock_hash": frozen["source_lock_hash"], "version": metadata["version"], "surface": "cursor-cli-interactive",
    "model_selection": "existing Grok4.7/500k/xhigh/fastfalse config and native startup display", "effective_backend_parameters": "not-attested",
    "model_turns": 1, "prompt_submissions": 1, "actual_native_Grep_preflight_callbacks": 2, "public_post_callbacks": 1, "private_post_callbacks": 0,
    "callbacks": callbacks, "policy_receipts": receipts, "callback_count": 6, "receipt_count": 6,
    "public_preflight": "manual/tool-route-uncovered; native post callback observed",
    "private_preflight": "permission deny/private-holdout-credential-path; no successful post callback observed",
    "native_private_failure_notification": "unobserved; no postToolUseFailure logger in frozen definition and retained terminal has grouped rows without explicit denial",
    "private_native_enforcement": "unqualified without explicit native failure response; exact directory extraction and deny wire verified",
    "frozen_oracle": "partial: actual directory scopes, public pre/post, private deny wire/no post and unchanged fixtures observed; explicit native denial response missing",
    "glob_root_traversal_scope": "unqualified", "fault_origin": "none", "fixtures_unchanged": True, "final_marker_observed": True,
    "terminal": [bind(path) for path in terminal_paths], "terminal_truncated": any("truncated output" in value for value in terminal_outputs),
    "raw_native_tool_return_content": "not-retained", "full_transcript_read": False,
    "native_exit_code": 0, "monitor_exit_code": 0, "cleanup": bind(RUN / "cleanup.json"), "process_audit": bind(RUN / "process-final-audit.json"),
    "process_union_identities": len(audit["tracked"]), "processes_live": 0, "process_stop_performed": False,
    "removed_members": 28, "historical_members_preserved": len(history), "protected_global_configs_unchanged": True,
    "CLI_owned_state_hash_changed": cleanup["global_cli_hash_before"] != cleanup["global_cli_hash_after"], "CLI_changed_fields": "not-inferred",
    "global_direct_writes": False, "source_kit_modified": False, "installed_update": "not-performed", "publication": "not-performed",
    "full_native_gate": "unchecked", "review": "inline; no independent reviewer", "frozen_brief": bind(RUN / "frozen-brief.json"), "verifier": bind(Path(__file__)),
}
target = RUN / "verified-directory-observations.json"
with target.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": record["status"], "turns": 1, "Grep_pre": 2, "public_post": 1, "private_post": 0,
    "callbacks": 6, "receipts": 6, "frozen_oracle": "partial", "process_union": len(audit["tracked"]), "live": 0}))
