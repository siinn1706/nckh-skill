"""Bind terminal local delivery and fresh scoped native evidence without full-gate closure."""

import json
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
ROOT = WORK / "nckh-kit"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
from core.build import verify_bundle, verify_source_lock
from core.paths import atomic_json, digest_file, digest_record

EXPECTED = "629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb"
read = lambda p: json.loads(p.read_text(encoding="utf8"))
bind = lambda p: {"path": p.relative_to(WORK).as_posix(), "sha256": digest_file(p)}
REPORT = WORK / "plans/reports/delivery-261005-1640-r37-local-native-checkpoint.json"
assert not REPORT.exists()
lock = verify_source_lock(ROOT)
assert lock["revision"] == "37" and len(lock["files"]) == 281 and digest_record(lock) == EXPECTED
pipeline = read(RUN / "revalidation-summary.json")
assert pipeline["status"] == "completed-local-checks-native-retest-pending" and pipeline["source_unchanged"]
assert pipeline["source_lock_hash"] == EXPECTED and pipeline["global_deadline_seconds"] is None
assert [r["name"] for r in pipeline["stages"]] == ["deterministic", "build", "archive", "smoke", "preview", "preservation"]
assert all(r["exit_status"] == 0 and r["process_cleanup"] == "owned-process-group-closed" for r in pipeline["stages"])
for r in pipeline["stages"]:
    command_record = read(WORK / r["receipt"])
    stem = (WORK / r["receipt"]).with_suffix("")
    assert digest_file(Path(str(stem) + ".stdout")) == command_record["stdout_sha256"]
    assert digest_file(Path(str(stem) + ".stderr")) == command_record["stderr_sha256"]
suite = read(RUN / "deterministic-r37-attempt-02-suite.json")
assert suite["successful"] and suite["tests"] == 192 and len(suite["skipped"]) == 1
assert not suite["errors"] and not suite["failures"]
context = read(RUN / "delivery-context.json")
assert context["status"] == "built" and len(context["artifacts"]) == 16 and context["source_lock_hash"] == EXPECTED
archive = read(RUN / "archive-summary.json")
assert archive["status"] == "pass" and len(archive["artifacts"]) == 16 and archive["source_lock_hash"] == EXPECTED
for row in archive["artifacts"]:
    assert digest_file(Path(row["archive"])) == row["archive_sha256"]
    manifest = verify_bundle(Path(row["extracted"]))
    assert manifest["source_lock_hash"] == EXPECTED and len(manifest["skills"]) == 39
    if row["host"] == "cursor":
        prefix = manifest["hooks"]["projection_root"]
        roots = [""] + ([prefix + "/"] if prefix != "not-projected" else [])
        for projected in roots:
            template = read(Path(row["extracted"]) / (projected + "hooks/templates/cursor.json"))
            assert template["config"]["hooks"]["preToolUse"][0]["timeout"] == 20
    assert manifest["resource_access"] == row["variant"].split("-", 1)[0]
smoke = read(RUN / "smoke-summary.json")
assert smoke["status"] == "pass" and len(smoke["bundles"]) == 16 and smoke["source_lock_hash"] == EXPECTED
counts = {"resource_reads": sum(r["resource_reads"] for r in smoke["bundles"]),
          "off_no_read_observations": sum(r["writer_disabled_observations"] for r in smoke["bundles"]),
          "hook_projections": sum(r["hook_projections_exercised"] for r in smoke["bundles"])}
assert counts == {"resource_reads": 216, "off_no_read_observations": 48, "hook_projections": 24}
previews = read(RUN / "installer-previews.json")
assert previews["status"] == "pass" and len(previews["surfaces"]) == 8 and previews["source_lock_hash"] == EXPECTED
preservation = read(RUN / "final-preservation.json")
assert preservation["status"] == "pass" and preservation["protected_hashes_checked"] == 509
assert preservation["source_lock_hash"] == EXPECTED and len(preservation["legacy_bundles"]) == 4
assert preservation["installed_update"] == "not-performed" and preservation["installed_revision"] == "25"
native_run = WORK / "plans/runs/nckh-native-261005-1700-r37-cursor-packaged-controls-attempt-15"
native = read(native_run / "native-packaged-summary.json")
assert native["status"] == "verified-fresh-r37-packaged-write-allow-and-plan-only-prevention"
assert native["source_revision"] == 37 and native["source_lock_hash"] == EXPECTED and native["packaged_default_timing_used"]
assert native["model_turns"] == native["prompt_submissions"] == 2
model_metadata = read(native_run / "native-metadata.json")
parameters = {p["id"]: p["value"] for p in model_metadata["selected_model"]["parameters"]}
assert model_metadata["selected_model"]["modelId"] == "grok-4.7"
assert parameters["context"] == "500k" and parameters["reasoning_effort"] == "xhigh" and parameters["fast"] == "false"
assert native["protected_global_configs_unchanged"] and not native["global_direct_write"]
assert read(native_run / "cleanup.json")["status"] == "pass"
assert read(native_run / "final-process-audit.json")["matching_count"] == read(native_run / "final-process-audit.json")["tracked_live_count"] == 0
audit = read(RUN / "final-process-audit-corrected.json")
assert audit["status"] == "pass" and audit["matching_count"] == audit["tracked_live_count"] == 0
assert not audit["root_still_live"] and not audit["process_stop_performed"]
assert audit["original_audit_sha256"] == digest_file(RUN / "final-process-audit.json")
assert read(RUN / "checkpoint-verifier-attempt-01-failure.json")["exit_code"] == 1
assert read(RUN / "terminal-final-observation.json")["response"]["exit_code"] == 0
assert digest_record(verify_source_lock(ROOT)) == EXPECTED
source_run = WORK / "plans/runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-01"
summary = {"status": "verified-r37-local-and-scoped-packaged-native-checkpoint", "source_revision": 37,
    "source_lock_hash": EXPECTED, "pins": 281, "changed_pins": read(source_run / "source-checkpoint.json")["changed_pins"],
    "focused_config_runner_tests": 17, "deterministic_tests": 192, "skipped_tests": suite["skipped"],
    "archives_extractions": 16, **counts, "installer_previews": 8, "protected_hashes": 509, "legacy_bundles": 4,
    "source_checkpoint": bind(source_run / "source-checkpoint.json"), "review": bind(source_run / "inline-review.json"),
    "pipeline": bind(RUN / "revalidation-summary.json"), "pipeline_original_native_pending_preserved": True,
    "deterministic": bind(RUN / "deterministic-r37-attempt-02-suite.json"), "archives": bind(RUN / "archive-summary.json"),
    "smoke": bind(RUN / "smoke-summary.json"), "previews": bind(RUN / "installer-previews.json"),
    "preservation": bind(RUN / "final-preservation.json"), "process_audit": bind(RUN / "final-process-audit-corrected.json"),
    "process_audit_original": bind(RUN / "final-process-audit.json"),
    "verifier_previous_failure": bind(RUN / "checkpoint-verifier-attempt-01-failure.json"),
    "process_audit_correction": "Original audit matched its own shell; corrected executable/identity filter has zero owned matches",
    "terminal_exit": bind(RUN / "terminal-final-observation.json"), "native_summary": bind(native_run / "native-packaged-summary.json"),
    "native_scope": "fresh r37 Cursor public Write effect and plan-only preventive Write denial; full native gate unchecked",
    "native_model": native["model_requested"], "backend_attestation": "not-observed", "billing": "not-observed",
    "native_cleanup_removed": 26, "native_historical_preserved": native["historical_members_preserved"],
    "terminal_limits": native["terminal_capture_limitations"], "full_native_gate": "unchecked", "plan_tasks": "44/45",
    "owner_acceptance": "accepted-exact-r29-VI-EN-samples-only", "installed_revision": 25, "installed_update": "not-performed",
    "scientific": "pending", "stable_release": "pending", "publication": "not-performed", "global_direct_write": False,
    "agy_window": bind(RUN / "agy-window-final-observation.json"), "Claude_model_effort": "selection-pending",
    "setup_failure": bind(source_run / "pipeline-setup-failure.json"), "verifier": bind(Path(__file__))}
atomic_json(RUN / "verified-checkpoint.json", summary)
with REPORT.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": summary["status"], "tests": 192, "archives": 16, **counts, "full_native_gate": "unchecked"}))
