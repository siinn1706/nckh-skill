"""Bind native fault observations and their qualification limits."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = RUN / "projects/codex"
ROOT = WORK / "nckh-kit"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from core.build import verify_source_lock
from core.paths import atomic_json, digest_file, digest_record

REPORT = WORK / "plans/reports/delivery-261004-1707-r30-prompt-failures.json"
if REPORT.exists():
    raise RuntimeError("Preserve previous native fault report")


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


lock = verify_source_lock(ROOT)
source_hash = digest_record(lock)
if source_hash != "55a4b60779228f3be3ae42d7691a49dec1df1b4e6f26139a32435aa1914562e1":
    raise RuntimeError("Source drifted from verified r30")
registration = read(PROJECT / "failure-probe-registration.json")
if registration["source_lock_hash"] != source_hash:
    raise RuntimeError("Registration used another source")
definition_hash = "sha256:083884235854b0985c5612fab601f099bf17bbe0d4a422667a3d967abe0aafa3"
expected = {"policy-deny": "blocked", "advisory": "completed", "malformed-input": "blocked",
            "malformed-output": "failed", "timeout": "failed", "crash": "failed", "unsupported-codec": "failed"}
cases = []
for name, status in expected.items():
    record = read(PROJECT / f"failure-probe-{name}.json")
    completed = [row for row in record["notifications"] if row.get("method") == "hook/completed"]
    if len(record["observations"]) != 1 or len(completed) != 1 or completed[0]["params"]["run"]["status"] != status:
        raise RuntimeError("Native callback/status differs: " + name)
    if record["hooks"][0]["currentHash"] != definition_hash or record["source_lock_hash"] != source_hash:
        raise RuntimeError("Native definition/source differs: " + name)
    if any(row["enabled"] for row in record["global_hooks"]) or any(record["mcp_enabled"].values()):
        raise RuntimeError("Invocation isolation differs: " + name)
    errors = [row for row in record["notifications"] if row.get("method") == "error"]
    turns = [row for row in record["notifications"] if row.get("method") == "turn/completed"]
    if status == "blocked":
        if len(turns) != 1 or turns[0]["params"]["turn"]["items"] != [] or errors:
            raise RuntimeError("Blocked prompt did not complete an empty-items turn")
    elif not errors:
        raise RuntimeError("Expected refused-provider continuation evidence is missing")
    cases.append({"name": name, "callbacks": 1, "native_hook_status": status,
                  "native_feedback": completed[0]["params"]["run"]["entries"],
                  "policy_receipts": record["policy_receipts"], "provider_error_notifications": len(errors),
                  "completed_turn_notifications": len(turns), "fault_after_real_callback": True,
                  "model_success": "none-observed", "tool_side_effect_oracle": "not-exercised"})
metadata = {number: read(PROJECT / f"failure-probe-metadata-{number:02d}.json") for number in (1, 2, 3, 4)}
for number, trust, enabled in ((1, "modified", False), (2, "trusted", True), (3, "trusted", False)):
    rows = metadata[number]["hooks"]
    if len(rows) != 1 or (rows[0]["currentHash"], rows[0]["trustStatus"], rows[0]["enabled"]) != (definition_hash, trust, enabled):
        raise RuntimeError("Native trust sequence differs")
if metadata[4]["hooks"]:
    raise RuntimeError("Project hooks still callable")
cleanup = read(PROJECT / "failure-probe-cleanup.json")
audit = read(RUN / "process-audit-prompt-failures-final.json")
if cleanup["status"] != "pass" or not cleanup["config_absent"] or not cleanup["runtime_absent"] or len(cleanup["removed_members"]) != 26:
    raise RuntimeError("Native fault cleanup is incomplete")
if audit["matching_count"] != 0:
    raise RuntimeError("Owned run processes remain")
if len(cleanup["native_owned_state_residual"]) != 3 or any(row["enabled"] for row in cleanup["native_owned_state_residual"].values()):
    raise RuntimeError("Native trust residual differs from three disabled keys")
process_receipts = sorted((RUN / "commands").glob("codex-prompt-failure-*.json"))
process_receipts += [PROJECT / f"prompt-admission-tui-process-attempt-{number:02d}.json" for number in (4, 5)]
if any(not read(path).get("process_exited") for path in process_receipts):
    raise RuntimeError("An owned process has no terminal exit evidence")
bindings = [PROJECT / "failure-probe-registration.json", PROJECT / "failure-probe-ui-trust.json",
            PROJECT / "failure-probe-ui-disable.json", PROJECT / "failure-probe-cleanup.json",
            RUN / "native-grant.json", RUN / "owner-feedback.json", RUN / "process-audit-prompt-failures.json",
            RUN / "process-audit-prompt-failures-final.json", RUN / "codex-prompt-failure-observer.py",
            WORK / "plans/reports/delivery-261004-1707-r30-prompt-admission.json"]
bindings += [PROJECT / f"failure-probe-{name}.json" for name in expected]
bindings += [PROJECT / f"failure-probe-metadata-{number:02d}.json" for number in (1, 2, 3, 4)]
bindings += process_receipts
bindings += sorted((RUN / "commands").glob("codex-prompt-failure-*.stdout.jsonl"))
bindings += sorted((RUN / "commands").glob("codex-prompt-failure-*.stderr.txt"))
bindings += sorted((PROJECT / "failure-observations").glob("*/*.json"))
bindings += sorted((PROJECT / "failure-policy-receipts").glob("*/*.json"))
result = {"schema_version": 1, "recorded_at": datetime.now(timezone.utc).isoformat(),
          "status": "native-prompt-fail-open-observed-qualification-pending", "goal_turn_classification": "progress",
          "source_revision": lock["revision"], "source_lock_hash": source_hash, "source_pins": len(lock["files"]),
          "source_changed": False, "full_suite_build_rerun": False, "plan_progress": {"done": 44, "total": 45},
          "host": "Codex CLI", "version": "0.154.0", "event": "UserPromptSubmit", "native_definition_hash": definition_hash,
          "execution_route": "installed-CLI-app-server-stdio-thread-start-turn-start", "trust_route": "normal-CLI-TUI",
          "callbacks": 7, "policy_receipts": sum(len(row["policy_receipts"]) for row in cases), "cases": cases,
          "fail_open_cases": [row["name"] for row in cases if row["native_hook_status"] == "failed"],
          "qualification": "inactive-manual-full-event-surface-tool-duplicate-evidence-pending",
          "native_unsupported_event_or_tool_claim": False,
          "cleanup": {"config_removed": True, "staged_payload_members_removed": 26, "project_hooks_after": 0,
                      "disabled_native_test_state_keys": 3, "trusted_hash_storage": "scalar-replaced-by-normal-UI",
                      "unrelated_hook_state_unchanged": cleanup["unrelated_hook_state_unchanged"],
                      "matching_run_processes": 0, "initial_audit_observed_own_inflight_metadata_probe": True},
          "next_required_inputs": ["provider-host-quota-or-budget", "account-surface-prerequisites"],
          "evidence_bindings": [{"path": str(path.relative_to(WORK)), "sha256": digest_file(path)} for path in dict.fromkeys(bindings)]}
atomic_json(REPORT, result)
print(json.dumps({"status": result["status"], "callbacks": result["callbacks"], "policy_receipts": result["policy_receipts"],
                  "fail_open_cases": result["fail_open_cases"], "cleanup": "pass", "bindings": len(result["evidence_bindings"])}))
