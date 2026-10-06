"""Bind the new native observations without regrading historical verification."""

import json
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
ROOT = WORK / "nckh-kit"
PROJECT = RUN / "projects/codex"
REPORT = WORK / "plans/reports/delivery-261004-1707-r30-prompt-admission.json"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from core.build import verify_source_lock
from core.paths import atomic_json, digest_file, digest_record


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


if REPORT.exists():
    raise RuntimeError("Preserve the prior checkpoint")
lock = verify_source_lock(ROOT)
source_hash = digest_record(lock)
if source_hash != "55a4b60779228f3be3ae42d7691a49dec1df1b4e6f26139a32435aa1914562e1":
    raise RuntimeError("Source drifted from verified r30")
registration = read(PROJECT / "prompt-admission-registration.json")
block = read(PROJECT / "prompt-admission-observe-attempt-01.json")
advisory = read(PROJECT / "prompt-admission-observe-allow-attempt-01.json")
metadata = {number: read(PROJECT / f"prompt-admission-metadata-attempt-{number:02d}.json") for number in (2, 3, 4, 5)}
cleanup = read(PROJECT / "prompt-admission-cleanup.json")
process_audit = read(RUN / "process-audit-prompt-admission.json")
definition_hash = "sha256:3e7a2b1e996f1a2d7dc937ad7a1cff0616934538d428eaa204f0e88692be40b2"
for number, trust, enabled in ((2, "untrusted", True), (3, "trusted", True), (4, "trusted", False)):
    rows = metadata[number]["hooks"]
    if len(rows) != 1 or (rows[0]["currentHash"], rows[0]["trustStatus"], rows[0]["enabled"]) != (definition_hash, trust, enabled):
        raise RuntimeError("Native trust-state sequence differs from observations")
if metadata[5]["hooks"]:
    raise RuntimeError("Project hooks remain callable after cleanup")


def events(record, method):
    return [row for row in record["notifications"] if row.get("method") == method]


block_hooks = events(block, "hook/completed")
block_turns = events(block, "turn/completed")
advisory_hooks = events(advisory, "hook/completed")
if len(block_hooks) != 1 or block_hooks[0]["params"]["run"]["status"] != "blocked":
    raise RuntimeError("Native block response is absent")
if len(block_turns) != 1 or block_turns[0]["params"]["turn"]["items"] != []:
    raise RuntimeError("Native block did not complete an empty-items turn")
if len(advisory_hooks) != 1 or advisory_hooks[0]["params"]["run"]["status"] != "completed":
    raise RuntimeError("Advisory hook did not complete")
if not events(advisory, "error") or events(advisory, "turn/completed"):
    raise RuntimeError("Advisory observation differs from partial network-failure record")
for item in (block, advisory):
    if item["source_lock_hash"] != source_hash or any(row["enabled"] for row in item["global_hooks"]) or any(item["mcp_enabled"].values()):
        raise RuntimeError("Native probe isolation/source differs from its receipt")
if cleanup["status"] != "pass" or not cleanup["config_absent"] or not cleanup["runtime_absent"] or len(cleanup["removed_members"]) != 26:
    raise RuntimeError("Matching cleanup is incomplete")
if process_audit["matching_count"] != 0:
    raise RuntimeError("Run processes still appear in live audit")
configuration = tomllib.loads(Path(r"C:/Users/USER\.codex\config.toml").read_text(encoding="utf8"))
unrelated = {key: value for key, value in configuration.get("hooks", {}).get("state", {}).items()
             if str(PROJECT).casefold() not in key.casefold()}
if digest_record(unrelated) != registration["unrelated_native_hook_state_hash"]:
    raise RuntimeError("Unrelated native hook state drifted")
if digest_file(PROJECT / "prompt-admission-context.json") != registration["context_sha256"]:
    raise RuntimeError("Block context was not restored")
process_receipts = sorted((RUN / "commands").glob("codex-prompt-admission-*.json"))
process_receipts += [PROJECT / "prompt-admission-tui-process.json"]
process_receipts += sorted(PROJECT.glob("prompt-admission-tui-process-attempt-*.json"))
if any(not read(path).get("process_exited") for path in process_receipts):
    raise RuntimeError("An owned native process lacks completed exit evidence")
bindings = [RUN / "native-grant.json", RUN / "owner-feedback.json", RUN / "native-prompt-admission-zero-budget.json",
            RUN / "process-audit-prompt-admission.json", PROJECT / "prompt-admission-registration.json",
            PROJECT / "prompt-admission-ui-trust.json", PROJECT / "prompt-admission-ui-disable.json",
            PROJECT / "prompt-admission-observe-attempt-01.json", PROJECT / "prompt-admission-observe-allow-attempt-01.json",
            PROJECT / "prompt-admission-cleanup.json", PROJECT / "prompt-admission-context-block-preimage.json",
            WORK / "plans/reports/delivery-261004-1707-r30-native-checkpoint.md",
            WORK / "plans/reports/delivery-261004-1707-r30-native-checkpoint.json"]
bindings += [PROJECT / f"prompt-admission-metadata-attempt-{number:02d}.json" for number in (2, 3, 4, 5)]
bindings += process_receipts
bindings += sorted((RUN / "commands").glob("codex-prompt-admission-*.stdout.jsonl"))
bindings += sorted((RUN / "commands").glob("codex-prompt-admission-*.stderr.txt"))
record = {
    "schema_version": 1, "recorded_at": datetime.now(timezone.utc).isoformat(),
    "status": "native-prompt-observations-recorded-full-qualification-pending", "plan_progress": {"done": 44, "total": 45},
    "source_revision": lock["revision"], "source_lock_hash": source_hash, "source_pins": len(lock["files"]),
    "source_changed": False, "local_suite_build_rerun": False, "owner_samples": "vi-en-accepted-unchanged",
    "host": "Codex CLI", "version": "0.154.0", "event": "UserPromptSubmit", "native_definition_hash": definition_hash,
    "block": {"policy_receipts": len(block["policy_receipts"]), "hook_status": "blocked",
              "turn_status": block_turns[0]["params"]["turn"]["status"], "turn_items": [],
              "tool_prevention_oracle": "not-exercised"},
    "advisory": {"new_policy_receipts": len(advisory["new_policy_receipts"]), "hook_status": "completed",
                 "turn_final_notification": "absent-in-eight-second-observation-window",
                 "error_notifications": events(advisory, "error"), "model_success": "none-observed"},
    "isolation": {"global_user_hooks_disabled": len(block["global_hooks"]), "configured_mcp_servers_disabled": block["mcp_enabled"],
                  "builtin_cua_repl_startup": "reported-ready-not-called", "provider_endpoint": "http://127.0.0.1:9/v1",
                  "fake_server_response_or_key": False, "unrelated_hook_state_unchanged": True},
    "cleanup": {"config_removed": True, "payload_members_removed": 26, "project_hooks_after": 0,
                "test_trust_hashes_residual": 3, "test_hashes_enabled": False, "project_trust": "may-remain",
                "contexts_preimages_receipts_preserved": True, "matching_processes": 0, "owned_process_receipts": len(process_receipts)},
    "retained_failures": {"initial_tui": "invalid-MCP-transport-from-quoted-dotted-override-before-hook-event",
                          "sandbox_metadata_attempt_01": "access-denied-before-native-initialize",
                          "claude_zero_budget": "argument-validation-0-callbacks"},
    "remaining": ["full-native-failure-matrix", "native-PreToolUse-tool-side-effect-oracle", "provider-host-scope-budget",
                  "Cursor-authentication", "AGY-eligibility-connectivity", "Desktop-IDE-live-event-evidence"],
    "handshake": {"initialized_notification_sent": True, "historical_absent_callbacks_cause": "not-established"},
    "evidence_bindings": [{"path": str(path.relative_to(WORK)), "sha256": digest_file(path)} for path in dict.fromkeys(bindings)]
}
atomic_json(REPORT, record)
print(json.dumps({"status": record["status"], "source_pins": record["source_pins"], "bindings": len(record["evidence_bindings"]),
                  "native_block": "observed", "native_advisory": "observed", "cleanup": "pass", "plan_done": 44}))
