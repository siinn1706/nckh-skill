"""Record actual read-only baseline observations before the research upgrade."""

import hashlib
import json
import platform
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

WORK = Path(__file__).resolve().parents[3]
KIT = WORK / "nckh-kit"
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(KIT))
from core.build import verify_source_lock
from core.evaluation import validate_cases
from core.paths import digest_record


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(name, value):
    path = RUN / name
    if path.exists():
        raise RuntimeError(f"Preserve existing observation: {path}")
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


lock_path = KIT / "core/registry/source-lock/source-lock.json"
before = sha(lock_path)
lock = verify_source_lock(KIT)
catalog = read(KIT / "core/registry/catalog/skills.json")
resources = read(KIT / "core/registry/catalog/resources.json")
summary = validate_cases(KIT)
new_owners = ["nckh-dataset", "nckh-statistics", "nckh-telemetry", "nckh-aiops"]
identities = sorted(row["id"] for row in catalog["skills"])
case_ids = sorted(case["id"] for path in (KIT / "evals/cases").glob("*/*.json")
                  for case in read(path).get("cases", []) if read(path).get("skill_id"))
families = read(KIT / "evals/cases/required-families.json")["families"]
ownership = read(WORK / ".nckh-state/ownership.json")
installed = {}
for item in ownership["items"].values():
    root = Path(item["physical_path"])
    if root.is_dir():
        for path in root.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                installed[str(path)] = sha(path)
    elif root.is_file():
        installed[str(root)] = sha(root)
protected = {rel: pin["sha256"] for rel, pin in lock["files"].items()
             if rel.startswith(("skills/marketing/", "skills/core/nckh-humanwrite/",
                                "skills/core/nckh-paperwrite/", "skills/core/nckh-write/",
                                "skills/core/nckh-taste/", "skills/core/nckh-visuals/", "hooks/"))
             or rel in {"core/hook_policy.py", "core/hook_config.py", "core/guards.py"}}
planning = WORK / "plans/261005-0036-nckh-devops-aiops-research-upgrade"
save("baseline.json", {
    "schema_version": 1, "observed_at": datetime.now(timezone.utc).isoformat(),
    "timezone": "Asia/Saigon", "work_root": str(WORK), "kit_root": str(KIT), "run_root": str(RUN),
    "environment": {"python": platform.python_version(), "platform": platform.platform()},
    "source_revision": lock["revision"], "source_lock_file_sha256": before,
    "source_lock_canonical_sha256": digest_record(lock), "pins": len(lock["files"]),
    "approved_baseline_identities": identities, "baseline_case_ids": case_ids,
    "required_family_ids": sorted(x["id"] for x in families),
    "resources": [{"id": r["resource_id"], "path": r["path"], "sha256": sha(KIT / r["path"])}
                  for r in resources["resources"]],
    "target_identities": sorted(identities + new_owners),
    "target_case_ids": sorted(case_ids + [owner + ":" + kind for owner in new_owners
                                          for kind in ("positive", "negative", "outcome", "failure")]),
    "structural_check": summary,
    "handoff": {"delivery": "plans/reports/delivery-261006-0758-default-advisory-hooks.md",
                "delivery_sha256": sha(WORK / "plans/reports/delivery-261006-0758-default-advisory-hooks.md"),
                "old_native_gate": "pending, preserved independently; 44/45 old plan",
                "user_steering": "Quick subagent native check, then upgrade; do not exhaust full old native matrix",
                "quick_native_gate": "pending"},
    "plan_input_hashes": {p.name: sha(p) for p in planning.glob("*.md")},
    "source_edit_admission": "pending quick-native result",
})
save("protected-hashes.json", {"source": protected, "installed": installed,
                              "ownership_file_sha256": sha(WORK / ".nckh-state/ownership.json"),
                              "historical_lock_hashes": {p.name: sha(p) for p in
                                 (KIT / "core/registry/source-lock/history").glob("*.json")}})

scientific = read(WORK / "plans/reports/source-manifest-261005-0036-scientific.json")
selected = []
for row in scientific["selected_static_evidence"]:
    path = WORK / "resources" / row["path"]
    observed = sha(path) if path.exists() else None
    selected.append({**row, "observed_sha256": observed,
                     "integrity": "pass" if observed == row["sha256"] else "drift-or-missing",
                     "disposition": "read-only reference; independently author bounded contracts; no script execution"})
save("rights-ledger.json", {
    "schema_version": 1, "selected_static_files": selected,
    "local_sources": [{"id": s["source_id"], "repository": s["declared_repository"],
                       "version_kind": "local-archive-snapshot", "commit": None,
                       "snapshot": s["metadata_snapshot_sha256"], "root_license": s["root_license"],
                       "root_license_does_not_clear_nested_components": True,
                       "anchors": [{**a, "observed_sha256": sha(Path(s["local_path"]) / a["path"])}
                                   for a in s["anchors"] if "LICENSE" in a["path"] or "NOTICE" in a["path"]],
                       "adoption": "independently-authored-with-source-contributions; copied bytes require individual notice"}
                      for s in scientific["sources"]],
    "no_copy": ["ClaudeKit proprietary/confidential source", "unresolved office assets/prompts/code",
                "CC-BY-NC-SA what-if-oracle", "RCAEval CausalRCA/RUN unlicensed implementations"],
    "primary_sources": [
        {"id": "RCAEval", "locator": "https://github.com/phamquiluan/RCAEval", "observed_at": "2026-10-06",
         "purpose": "benchmark metadata", "rights": "mixed licenses; per-component gate; no code/data acquired"},
        {"id": "AIOpsLab", "locator": "https://github.com/microsoft/AIOpsLab", "observed_at": "2026-10-06",
         "purpose": "environment/action/reset/cleanup method anatomy", "rights": "MIT reference; no cluster/code execution"},
        {"id": "OpenTelemetry", "locator": "https://opentelemetry.io/docs/concepts/semantic-conventions/",
         "observed_at": "2026-10-06", "version": "1.44.0 observed in official docs navigation",
         "purpose": "bounded field dictionary", "rights": "reference-only until selected file/license/hash closure"}],
})
save("ownership-map.json", {
    "schema_version": 1, "execution": "sequential controller; native checker owns separate disposable run",
    "routes": {"nckh-research": "discovery/search/screening/appraisal", "nckh-method": "design/protocol/identification",
               "nckh-dataset": "scientific intake/selection/labels/splits", "nckh-telemetry": "signals/time/units/joins",
               "nckh-statistics": "estimand/unit/analysis/inference", "nckh-aiops": "task-specific scientific evaluation",
               "nckh-cook": "approved implementation/execution lifecycle", "nckh-devops": "environment/process/cleanup",
               "nckh-data": "DB/schema/migration", "nckh-analytics": "marketing KPIs", "nckh-experiment": "marketing A/B",
               "nckh-debug": "code/runtime failure diagnosis"},
    "schema_names": ["dataset-manifest", "split-manifest", "statistical-analysis", "telemetry-manifest",
                     "aiops-evaluation", "experiment-manifest", "research-run-receipt", "owned-resource-provenance"],
    "shared_queue": ["P2 domain files", "P3 domain files", "P4 domain files", "P5 catalog/profile/base cases",
                     "P5 resources/readers/provenance", "P6 artifact checker/pilot", "P7 integration/review/freeze/checks"],
    "constraints": ["stdlib core", "closed supported schema subset", "no provider/collector/orchestrator",
                    "resource ON public, OFF internal", "no implementation source freeze before P7"]})
save("pilot-selection.json", {
    "schema_version": 1, "status": "metadata selection; acquisition not executed",
    "primary_candidate": {"source": "BARO 0.0.4 metric sample linked by RCAEval download_data",
                          "url": "https://github.com/phamquiluan/baro/releases/download/0.0.4/simple_data.csv",
                          "modality": "metrics only; no invented logs/traces", "max_bytes": 1048576,
                          "tasks": ["local descriptive RCA ranking", "chronological forecast baseline"],
                          "grant": "pending exact download/local computation approval",
                          "rights": "pending selected release-asset license binding",
                          "gold": "not assumed from README example; independent annotation gate"},
    "permissible_offline_candidate": {"source": "existing World Bank VNM population snapshot",
                                     "path": "nckh-kit/core/profiles/resources/worldbank-series.jsonl",
                                     "bytes": (KIT / "core/profiles/resources/worldbank-series.jsonl").stat().st_size,
                                     "sha256": sha(KIT / "core/profiles/resources/worldbank-series.jsonl"),
                                     "rights": "existing CC-BY-4.0 source/notice record, verify before use",
                                     "task": "one-step chronological naive forecast on actual observed values",
                                     "scope": "supplied scientific project route allowed by plan; not incident telemetry",
                                     "unknowns": ["unit field blank retained", "single population series; no independent system efficacy claim"]},
    "local_operations": ["bounded read/hash", "owned project copy with provenance", "stdlib baseline calculation",
                         "actual prediction/metric receipts", "hash/denominator/drift checks"],
    "excluded": ["install dependency", "model/provider", "cloud/cluster/fault injection", "cross-workspace access",
                 "source/dist pilot data or private labels", "public release"],
})
for name in (".agentkit-state", ".agentkit-runtime"):
    db = WORK / "plans" / name / "plans/plans.db"
    if db.exists():
        with sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True) as src:
            with sqlite3.connect(RUN / f"{name[1:]}-before.sqlite") as dst:
                src.backup(dst)
if sha(lock_path) != before:
    raise RuntimeError("Source changed during baseline observation")
print(json.dumps({"revision": lock["revision"], "pins": len(lock["files"]), "identities": len(identities),
                  "base_cases": len(case_ids), "families": len(families), "resources": len(resources["resources"]),
                  "installed_protected_files": len(installed), "selected_source_files": len(selected),
                  "source_integrity": "pass", "source_edit_admission": "pending quick-native result"}))
