"""Reconcile actual gate receipts and deliver the experimental candidate."""
import hashlib
import json
from pathlib import Path
import sys
from datetime import datetime, timezone

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
KIT = WORK / "nckh-kit"
sys.path.insert(0, str(KIT))
from core.build import verify_source_lock, verify_bundle
from core.paths import digest_record, digest_file

def read(path): return json.loads(path.read_text(encoding="utf-8-sig"))
def save(name, value):
    with (RUN / name).open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2) + "\n")
def bind(path): return {"path": path.relative_to(WORK).as_posix(), "sha256": digest_file(path)}

lock = verify_source_lock(KIT)
approved = read(RUN / "p7-approved-freeze-attempt-03.json")
assert digest_record(lock) == approved["source_lock_hash"]
gates = read(RUN / "p7-local-gates.json")
assert gates["status"] == "pass" and gates["source_lock_hash"] == digest_record(lock)
deterministic = read(RUN / "p7-deterministic-attempt-02.json")
assert deterministic["status"] == "pass" and deterministic["deterministic"]["status"] == "pass"
suite = deterministic["deterministic"]
assert deterministic["source_lock_hash"] == digest_record(lock)
assert suite["process"]["source_lock_hash"] == digest_record(lock)
assert suite["process"]["post_source_lock_hash"] == digest_record(lock)
assert all(row["source_lock_hash"] == digest_record(lock) and row["post_source_lock_hash"] == digest_record(lock) for row in gates["commands"])
gate_record = next(row for row in gates["commands"] if row["name"] == "deterministic")
assert gate_record == suite["process"] == read(RUN / "p7-command-deterministic-attempt-02.json")
assert gate_record["argv"] == suite["command"]
assert gate_record["exit_status"] == suite["exit_status"] == 0
assert gate_record["output"] == suite["output"] and gate_record["output_sha256"] == suite["output_sha256"]
assert suite["complete_inventory_match"] and suite["no_exclusions"]
assert suite["passed"] + suite["skipped"] == suite["tests"]
assert digest_file(RUN / suite["output"]) == suite["output_sha256"]
extracted = read(RUN / "p7-extracted-qualification.json")
assert len(extracted["packages"]) == 16 and len(extracted["installer_previews"]) == 8
assert all(row["verdict"] == "pass" for row in extracted["packages"])
cleanup = read(RUN / "p7-temp-cleanup.json")
assert cleanup["removed"] and not Path(cleanup["root"]).exists()
timeout_cleanup = read(RUN / "p7-timeout-temp-cleanup.json")
assert timeout_cleanup["removed"] and all(not Path(root).exists() for root in timeout_cleanup["roots"])
catalog = read(KIT / "core/registry/catalog/skills.json")
resources = read(KIT / "core/registry/catalog/resources.json")
identities = {row["id"] for row in catalog["skills"]}
assert len(identities) == 43 and len(resources["resources"]) == 13
packages = []
for row in extracted["packages"]:
    root = Path(row["source"])
    manifest = verify_bundle(root)
    assert digest_file(root / "manifest.json") == row["manifest_sha256"]
    assert manifest["source_lock_hash"] == digest_record(lock)
    assert {item["id"] for item in manifest["skills"]} == identities
    assert all(not item["source_path"].startswith(("plans/", "pilot-data/", "pilot-output/", "evals/results/")) for item in manifest["files"])
    packages.append({**row, "manifest": bind(root / "manifest.json")})
protected = read(RUN / "protected-hashes.json")
checked = 0
for group in ("source", "installed", "historical_lock_hashes"):
    for name, expected in protected[group].items():
        path = KIT / name if group == "source" else KIT / "core/registry/source-lock/history" / name if group == "historical_lock_hashes" else Path(name)
        assert digest_file(path) == expected, str(path)
        checked += 1
assert digest_file(WORK / ".nckh-state/ownership.json") == protected["ownership_file_sha256"]
checked += 1
inventory = read(RUN / "migration-inventory.json")
assert digest_file(Path(inventory["archived_public_verifier"]["path"])) == inventory["archived_public_verifier"]["sha256"]
for row in inventory["current_consumers"]:
    row["sha256"] = digest_file(KIT / row["path"])
save("migration-inventory-v2.json", {"previous_inventory": bind(RUN / "migration-inventory.json"),
    "current_source_consumers": inventory["current_consumers"], "source_lock_hash": digest_record(lock),
    "identities": 43, "base_cases": 172, "resources": 13, "bindings": sum(len(row["consumers"]) for row in resources["resources"]),
    "archived_public_verifier": inventory["archived_public_verifier"]})
save("p7-final-preservation.json", {"protected_hashes_checked": checked, "mismatches": 0, "installed_ownership_unchanged": True,
    "legacy_formats": extracted["legacy"], "temp_cleanup": bind(RUN / "p7-temp-cleanup.json"),
    "timeout_temp_cleanup": bind(RUN / "p7-timeout-temp-cleanup.json"), "owned_live": 0})
reads = sum(row.get("actual_resource_reads", 0) + row.get("actual_plugin_resource_reads", 0) for row in packages)
candidate = {"schema_version": 1, "recorded_at": datetime.now(timezone.utc).isoformat(), "status": "experimental-delivered",
    "revision": lock["revision"], "pins": len(lock["files"]), "source_lock_hash": digest_record(lock),
    "source_lock_file_sha256": digest_file(KIT / "core/registry/source-lock/source-lock.json"), "identities": 43, "base_cases": 172,
    "required_families": 19, "resources": 13, "resource_consumer_bindings": sum(len(row["consumers"]) for row in resources["resources"]),
    "supplemental_domain_scenarios": 12, "deterministic_tests": deterministic["deterministic"]["tests"],
    "deterministic_passed": suite["passed"], "deterministic_skipped": suite["skipped"], "deterministic_skip_cases": suite["skip_cases"],
    "deterministic_duration_seconds": suite["duration_seconds"],
    "deterministic_command": suite["command"], "deterministic_entrypoint": suite["entrypoint"],
    "isolated_resource_reads": reads, "isolated_research_checker_runs": sum(row.get("isolated_checker") == "pass" for row in packages),
    "installer_previews": 8, "packages": packages, "protected_hashes_checked": checked, "owned_live": 0,
    "quick_native_hooks": "Genuine bounded Codex advisory callback checked before upgrade; old full-native gate remains separate",
    "pilot": {"observations": 26, "original_test_predictions": 6, "supplemental_outcomes": 52, "supplemental_completed": 49, "supplemental_unknown": 3,
        "scope": "Retrospective dependent single-country series; original values preserved; independent Fraction arithmetic; no CI/causal/blind efficacy/generalization claim"},
    "pending": {"semantic_agent_routes": "unverified", "native_full": "pending separately; old plan44/45", "owner": "pending",
        "scientific": "pending", "provider_paid": "not-authorized", "stable_public": "not-authorized", "real_install_migration": "not-authorized"},
    "cost": "unknown/unmeasured; provider unused", "release_rights": "local-package-only",
    "evidence": [bind(RUN / name) for name in ("p7-local-gates.json", "p7-deterministic-attempt-02.json", "p7-extracted-qualification.json",
        "p7-final-preservation.json", "paperwrite-evidence-handoff-v2.json")],
    "reviews": [bind(WORK / "plans/reports" / name) for name in ("review-261006-research-contracts-p2-p3.md",
        "review-261006-owned-resource-provenance.md", "review-261006-experiment-graph-and-pilot.md", "review-261006-research-integration-p7.md")],
    "retained_failures": [bind(RUN / name) for name in ("p7-pinned-tests-attempt-01.txt", "p7-deterministic.json", "p7-core-count-diagnostic-attempt-01.txt")],
    "rollback": "Installed skills/ownership and archive remain unchanged; retain r38/r39 lock history and original runs; any later candidate repair needs new freeze and affected receipts"}
save("experimental-candidate.json", candidate)
report = WORK / ("plans/reports/delivery-261006-research-upgrade-r" + lock["revision"] + ".md")
with report.open("x", encoding="utf-8") as stream:
    stream.write(f"""# Bàn giao research upgrade r{lock['revision']}

Status: experimental-delivered; phạm vi cook hoàn tất, các gate scientific/native/owner/provider/stable/public giữ riêng.

## Candidate và kiểm tra thực

| Hạng mục | Kết quả |
|---|---|
| Source | r{lock['revision']}, {len(lock['files'])} pins; canonical SHA-256 `{digest_record(lock)}` |
| Identity/cases | 43 identities, 172 base IDs; 19 required families; historical148/224 và writer256+20 được giữ |
| Resources | 13 groups, 35 consumer bindings; bốn authored packs14 records; public contract ON |
| Deterministic | {candidate['deterministic_tests']} tests hoàn tất trong{suite['duration_seconds']}giây: {suite['passed']} pass, {suite['skipped']} skip với lý do ghi trong receipt; exit0 trên hash hiện tại |
| Fresh packages | 16 bundles: four hosts × standalone/plugin × ON/internal OFF; ON delivery8 bundles |
| Relocation | {reads} actual isolated resource reads; {candidate['isolated_research_checker_runs']} isolated research checker runs; OFF no-read |
| Installer | Eight explicit-package read-only previews; source/target user bytes preserved |
| Preservation | {checked} protected hashes, zero mismatch; original format1/2 bundles verify unchanged; owned external temp removed |

Chi tiết và exact artifact hashes ở [candidate](../runs/nckh-upgrade-261006-0850-attempt-01/experimental-candidate.json), [local gates](../runs/nckh-upgrade-261006-0850-attempt-01/p7-local-gates.json), [deterministic](../runs/nckh-upgrade-261006-0850-attempt-01/p7-deterministic-attempt-02.json), [extracted qualification](../runs/nckh-upgrade-261006-0850-attempt-01/p7-extracted-qualification.json), [preservation](../runs/nckh-upgrade-261006-0850-attempt-01/p7-final-preservation.json) và [migration inventory](../runs/nckh-upgrade-261006-0850-attempt-01/migration-inventory-v2.json).

## Research chain và pilot

Bốn owner mới: dataset, statistics, telemetry, AIOps; method/cook/devops giữ design/lifecycle/environment. Read-only checker bind actual data/split/rights/code/config/environment/attempt outputs; không thực thi manifest argv. Review sửa exact run-output binding, denominator/no-gold/corpus policies, simulation freeze và distinct retry routes.

Actual World Bank Vietnam snapshot26 observations2000–2025; train20/validation3/test3. Original processPID31900 exit0, six predictions, fixed naive/drift and independent Fraction endpoint oracle. Descriptive mean drift-minus-naive absolute-error contrast `-270039.7598265261`. Supplemental actual processPID23416 exit0 báo cáo mọi partition với52 outcomes49completed3explicitunknown; original6test values unchanged. Independent_n1, dependent retrospective series, blank source units, prior access và vintage/availability limits được giữ. Không CI/p-value, causal/generalization/blind efficacy hoặc incident RCA claim. [Pilot readout](../runs/nckh-upgrade-261006-0850-attempt-01/pilot-readout.md), [partition supplement](../runs/nckh-upgrade-261006-0850-attempt-01/partition-supplement-output.json) và [paperwrite handoff](../runs/nckh-upgrade-261006-0850-attempt-01/paperwrite-evidence-handoff-v2.json).

## Native và pending gates

[Quick genuine Codex hooks check](verification-261006-0850-quick-native-hooks.md) theo chỉ đạo user quan sát advisory callback `{{}}`/exit0 và sandbox chặn benign mutation. Đây là bounded check trước upgrade; full qualification của plan cũ44/45 vẫn riêng. Twelve supplemental domain routes là static expected declarations, không observed semantic routing. Human/owner/scientific/full-native/provider/stable/public và real install/migration chưa được cấp verdict từ delivery này. CPU/peak memory/provider cost unknown, provider unused.

## Failures, repair và cleanup

Original failed attempts/counsel được giữ. First r39 pinned78 run có2fails2errors: stale36/13 counts, missing fixture catalog và bytecode writes. [Counsel](counsel-261006-pinned-regression-failure.md), eight focused tests và114domain tests đóng sửa trước corrective r40 freeze. Public deterministic runner trên r40 bị ngắt ở900giây, verdict timeout-unknown; focused diagnostic xác nhận exact Core count16≠12. [Timeout counsel](counsel-261006-deterministic-timeout.md) và independent source review cho phép chỉ sửa expected count16, giữ qualification/preservation/empty-index assertions. Full/package descendants hiện tại dùng r{lock['revision']} hashes. Full discovery suite chạy qua task-local observable Popen command với verbose output, không exclusions hoặc deadline900giây; public runner được giữ nguyên, timeout cũ không bị ghi đè. Validator/rights/post-smoke checks không bị nới. [Integration review](review-261006-research-integration-p7.md) và [experiment re-review](review-261006-experiment-graph-and-pilot.md) giữ lịch sử findings và source fingerprints.

Actual owned child handles đều reaped; không background server/port/provider/cluster. Archive/extract tại owned host temp ngoài workspace, separate CWD, Python isolated và PYTHONPATH unset; receipt/hashes được giữ trước exact unchanged-owned cleanup. Installed source/ownership và archived publication verifier không đổi. Local-package-only experimental candidate; không publish hoặc upgrade global install.
""")
print(json.dumps({"candidate": str(RUN / "experimental-candidate.json"), "report": str(report), "tests": candidate["deterministic_tests"], "reads": reads}))
