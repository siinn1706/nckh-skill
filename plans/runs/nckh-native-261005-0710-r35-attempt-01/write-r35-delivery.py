"""Bind actual local delivery and native file receipts without broad qualification."""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
ROOT = WORK / "nckh-kit"
NATIVE = RUN / "native-codex-file"
OPS = RUN / "native-codex-patch-ops"
FILE = RUN.parent / "nckh-native-261005-0658-r34-codex-file-attempt-01"
CX = RUN.parent / "nckh-native-261005-0052-r34-codex-attempt-01"
REPORT = WORK / "plans/reports/delivery-261005-0710-r35-patch-retest"
EXPECTED = "4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
from core.build import verify_source_lock
from core.paths import atomic_json, digest_file, digest_record

read = lambda path: json.loads(path.read_text(encoding="utf8"))
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": digest_file(path)}
if REPORT.with_suffix(".json").exists() or REPORT.with_suffix(".md").exists():
    raise RuntimeError("Preserve the earlier delivery report")
assert digest_record(verify_source_lock(ROOT)) == EXPECTED
pipeline = read(RUN / "revalidation-summary.json")
assert pipeline["status"] == "completed-local-checks-native-retest-pending" and pipeline["source_unchanged"]
assert len(pipeline["stages"]) == 6 and all(row["exit_status"] == 0 for row in pipeline["stages"])
components = {name: read(RUN / name) for name in ("deterministic-r35-attempt-01.json", "archive-summary.json",
    "smoke-summary.json", "installer-previews.json", "final-preservation.json")}
assert all(row["status"] == "pass" and row["source_lock_hash"] == EXPECTED for row in components.values())
suite = components["deterministic-r35-attempt-01.json"]
assert suite["deterministic"]["successful"] and suite["source_unchanged"]
assert (suite["source_files_pinned"], suite["identities"], suite["skill_cases"], suite["required_families"]) == (281, 39, 156, 19)
context = read(RUN / "delivery-context.json")
assert len(context["artifacts"]) == len(components["archive-summary.json"]["artifacts"]) == 16
for row in components["archive-summary.json"]["artifacts"]:
    assert digest_file(Path(row["archive"])) == row["archive_sha256"]
smoke = components["smoke-summary.json"]["bundles"]
assert len(smoke) == 16 and all(row["status"] == "pass" and row["project_unchanged"] for row in smoke)
previews = components["installer-previews.json"]["surfaces"]
assert len(previews) == 8 and all(row["entries"] == 45 and row["project_unchanged"] for row in previews)
native = read(NATIVE / "native-file-summary.json")
assert native["status"] == "recorded-native-file-attempts" and native["source_lock_hash"] == EXPECTED
assert len(native["results"]) == 4
cleanup = read(NATIVE / "cleanup.json")
assert cleanup["status"] == "pass" and not cleanup["config_callable"]
assert cleanup["global_config_unchanged"] and cleanup["global_hook_unchanged"] and cleanup["new_project_trust_keys"] == 0
audit = read(RUN / "final-process-audit.json")
assert audit["status"] == "pass" and not audit["matching_task_processes"]
rows = []
for result in native["results"]:
    path = WORK / result["receipt"]["path"]
    assert digest_file(path) == result["receipt"]["sha256"]
    attempt = read(path)
    assert attempt["process_exited"] and attempt["exit_code"] == 0 and attempt["invalid_stdout_lines"] == 0
    callbacks = [row for row in attempt["native_callbacks"] if row["event"] == "PreToolUse"]
    assert len(callbacks) == 1 and callbacks[0]["native_tool_name"] == "apply_patch"
    patch = "*** Begin Patch\n*** Add File: " + attempt["marker_relative"] + "\n+NCKH_NATIVE_FILE_ORACLE\n*** End Patch"
    assert callbacks[0]["native_command_sha256"] == hashlib.sha256(patch.encode()).hexdigest()
    assert callbacks[0]["runner_exited"] and callbacks[0]["fault_origin"] == "none"
    completed = [frame["item"] for frame in attempt["native_frames"] if frame.get("type") == "item.completed"
        and frame.get("item", {}).get("type") == "file_change" and frame["item"].get("status") == "completed"]
    policy = [row for row in attempt["policy_receipts"] if "/PreToolUse/" in row["path"]]
    assert len(policy) == 1
    rows.append({**result, "native_tool": "apply_patch", "native_command_matches_requested_patch": True,
        "completed_file_change_items": len(completed), "policy": policy[0],
        "model_requested": attempt["model_requested"], "effort_requested": attempt["effort_requested"],
        "native_models": sorted({row.get("native_model") for row in attempt["native_callbacks"] if row.get("native_model")}),
        "callbacks": attempt["callbacks"], "command_receipt": attempt["command_receipt"]})
actual = {row["attempt"]: row for row in rows}
for name, decision, marker in (("r35-file-allow-01", "allow", True), ("r35-file-policy-deny-01", "block", False),
    ("r35-file-protected-01", "block", False), ("r35-file-uncovered-01", "manual", True)):
    assert actual[name]["policy"]["decision"] == decision and actual[name]["marker"] is marker
    assert bool(actual[name]["completed_file_change_items"]) is marker
assert "private-holdout-credential-path" in actual["r35-file-protected-01"]["policy"]["reason_codes"]
operations = read(OPS / "native-patch-ops-summary.json")
assert operations["status"] == "recorded-native-patch-operations" and operations["source_lock_hash"] == EXPECTED
assert len(operations["results"]) == 8
operation_cleanup = read(OPS / "cleanup.json")
assert operation_cleanup["status"] == "pass" and operation_cleanup["global_config_unchanged"]
assert operation_cleanup["global_hook_unchanged"] and operation_cleanup["new_project_trust_keys"] == 0
operation_rows = []
for row in operations["results"]:
    path = WORK / row["receipt"]["path"]
    assert digest_file(path) == row["receipt"]["sha256"]
    item = read(path)
    assert item["process_exited"] and item["exit_code"] == 0 and item["invalid_stdout_lines"] == 0
    callbacks = [callback for callback in item["native_callbacks"] if callback["event"] == "PreToolUse"]
    assert len(callbacks) == 1 and callbacks[0]["native_tool_name"] == "apply_patch"
    assert callbacks[0]["native_command_sha256"] == item["patch_sha256"] and callbacks[0]["fault_origin"] == "none"
    assert callbacks[0]["runner_exited"] and item["after"] == item["expected_after"]
    assert len(item["pretool_policies"]) == 1
    policy = item["pretool_policies"][0]
    assert policy["decision"] == ("block" if row["expected_denial"] else "allow")
    assert bool(item["completed_file_changes"]) is not row["expected_denial"]
    if row["expected_denial"]:
        assert item["after"] == item["before"] and item["expected_reason"] in policy["reason_codes"]
    operation_rows.append({**row, "native_command_matches_requested_patch": True, "policy": policy,
        "completed_file_change_items": len(item["completed_file_changes"]), "callbacks": item["callbacks"],
        "command_receipt": item["command_receipt"]})
record = {"status": "local-delivery-and-native-patch-retest-recorded-full-native-gate-open",
    "schema_version": 1, "recorded_at": datetime.now(timezone.utc).isoformat(), "source_revision": 35,
    "source_lock_hash": EXPECTED, "source_unchanged": True, "components": [bind(RUN / name) for name in components],
    "pipeline": bind(RUN / "revalidation-summary.json"), "native_file_cases": rows, "native_cleanup": bind(NATIVE / "cleanup.json"),
    "native_patch_operations": operation_rows, "operation_cleanup": bind(OPS / "cleanup.json"),
    "process_audit": bind(RUN / "final-process-audit.json"), "native_version": "0.154.0", "native_surface": "codex-cli-exec",
    "local_counts": {"tests": suite["deterministic"]["tests"], "skipped": len(suite["deterministic"]["skipped"]),
        "archives_extractions": 16, "resource_reads": sum(row["resource_reads"] for row in smoke),
        "writer_disabled_no_read": sum(row["writer_disabled_observations"] for row in smoke),
        "hook_projections": sum(row["hook_projections_exercised"] for row in smoke), "installer_previews": 8,
        "protected_hashes": components["final-preservation.json"]["protected_hashes_checked"]},
    "historical_failure": bind(WORK / "plans/reports/delivery-261005-0658-r34-codex-file-failure.json"),
    "trust_correction": bind(CX / "trust-report-correction.json"), "cleanup_helper_review": bind(FILE / "cleanup-helper-review.json"),
    "backend_attestation": "not-observed", "billing": "not-observed", "independent_review": "not-run; inline review",
    "owner_acceptance": "exact two r29 samples retained", "installed_revision": 25, "installed_update": "not-performed",
    "native_checkbox": "unchecked", "plan_progress": "44/45", "stable_scientific_release": "pending"}
atomic_json(REPORT.with_suffix(".json"), record)
counts = record["local_counts"]
table = "\n".join(f"| {row['attempt']} | {row['policy']['decision']} | {'Có' if row['marker'] else 'Không'} | {row['completed_file_change_items']} |" for row in rows)
operation_table = "\n".join(f"| {row['attempt']} | {row['policy']['decision']} | {row['completed_file_change_items']} | {'Không đổi' if row['expected_denial'] else 'Đúng thay đổi'} |" for row in operation_rows)
md = f"""# Delivery r35 — native patch-path repair

## Current candidate

Current **r35/281 pins**, canonical source-lock hash `{EXPECTED}`. [Structured bindings](./delivery-261005-0710-r35-patch-retest.json) bind actual local results, source/package/command/callback hashes, markers, cleanup and process audit. Plan remains **in-progress, 44/45**; the full native event/version/surface task stays unchecked.

## Local checks completed

| Check | Actual result |
|---|---|
| Deterministic | {counts['tests']} tests successful, {counts['skipped']} Windows symlink skip; {suite['deterministic']['seconds']:.3f} seconds |
| Inventory | Exact 39 identities / 156 base cases / 19 families / 9 resources |
| Packaging | Four reproducibility variants; 16 builds/archives/extractions |
| Extracted behavior | {counts['resource_reads']} resource reads; {counts['writer_disabled_no_read']} OFF writer no-read observations; {counts['hook_projections']} hook projections |
| Installer previews | Eight surfaces; each 39 skills + six agents; project bytes unchanged |
| Preservation | {counts['protected_hashes']} protected hashes; installed r25 and four legacy bundles retained |

The [pipeline receipt](../runs/nckh-native-261005-0710-r35-attempt-01/revalidation-summary.json) records six successful stages. Public resource access remains ON; OFF bundles are internal comparisons. Local counts do not provide scientific/human/full-native acceptance.

## Genuine native apply_patch retest

Codex CLI **0.154.0 exec**, GPT-5.6 Luna medium, dangerous native flags within the existing grant. The already trusted r34 file scratch project was reused with a new evidence namespace and verified r35 payload. No new workspace trust key or global hook/config bytes changed. Each PreToolUse callback reported `apply_patch` and an exact command hash matching the requested patch; no fault injection was used.

| Attempt | Policy | Marker created | Completed file-change items |
|---|---|---|---:|
{table}

The protected private-path attempt returned `private-holdout-credential-path`, with no completed file change and no marker. The following eight genuine attempts exercise update/delete/move and a mixed public/private add patch. Synthetic input files were created by the controller before native calls; actual before/after hashes, tool items and callbacks were retained.

| Native patch operation | Policy | Completed file-change items | Observed files |
|---|---|---:|---|
{operation_table}

Public update/delete/move performed the requested changes. Private update/delete, moves with a private source or destination, and mixed public/private add were blocked before any requested change. Native command hashes matched each requested patch exactly. These observations cover the tested canonical envelopes; shell targets, other tools and other surfaces retain their pending/manual status. Backend model/billing attestation was not observed.

[Historical r34 failure](./delivery-261005-0658-r34-codex-file-failure.md) retains the private marker and original receipts. R35 reads canonical patch headers; three regressions had 22 failures before repair and 12 focused tests passed afterward. The r34 failure has not been regraded.

## Trust correction and cleanup

[Trust correction](../runs/nckh-native-261005-0052-r34-codex-attempt-01/trust-report-correction.json) distinguishes native-persisted workspace trust from invocation-only hook-definition bypass; original report/helper/document preimages remain. The normal UI trust action was rejected and did not run, while the subsequent native CLI route did persist its own project trust.

[Cleanup helper review](../runs/nckh-native-261005-0658-r34-codex-file-attempt-01/cleanup-helper-review.json) found and repaired a static variable-shadowing defect that could direct a receipt write at the global hooks file. The global file retained its `hooks` structure; no overwrite was observed. The retained trace does not prove this defect caused the earlier CPU stall. Historical reconciliation receipts are unchanged.

[R35 native cleanup](../runs/nckh-native-261005-0710-r35-attempt-01/native-codex-file/cleanup.json) removed 26 matching payload files, retained native evidence, and verified {cleanup['historical_project_members_unchanged']} historical project member hashes plus raw global config/hook hashes. [Final process audit](../runs/nckh-native-261005-0710-r35-attempt-01/final-process-audit.json) found zero matching task processes. Review was inline; no independent reviewer is claimed.

[Operation cleanup](../runs/nckh-native-261005-0710-r35-attempt-01/native-codex-patch-ops/cleanup.json) separately removed its 26 matching payload members and verified {operation_cleanup['historical_project_members_unchanged']} historical project hashes plus unchanged raw global config/hook hashes. All fixtures, native outcomes and failures remain.

## Remaining requirements

Claude needs an owner-authorized model/effort for model/tool and other event observations. Codex project/plugin duplicate, shell targets and other tools, Cursor CLI prompt/stop/file routes and timeout diagnosis, remaining AGY tools/timing, and direct Desktop/IDE receipts remain pending. Production timing and stable/scientific/install/release acceptance are separate. Owner VI/EN acceptance remains bound to the exact two r29 samples.
"""
REPORT.with_suffix(".md").write_text(md, encoding="utf8", newline="\n")
print(json.dumps({"status": record["status"], "counts": counts, "native_cases": len(rows), "native_gate": "open"}))
