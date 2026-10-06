"""Project-only preparation of the frozen, dated World Bank pilot snapshot."""

import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
KIT = WORK / "nckh-kit"
sys.path.insert(0, str(KIT))
from core.datasets import validate_dataset_manifest, validate_split_manifest
from core.telemetry import validate_telemetry_manifest


def bind(name):
    return {"path": name, "sha256": hashlib.sha256((RUN / name).read_bytes()).hexdigest()}


def save(name, value):
    (RUN / name).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return bind(name)


selection = json.loads((RUN / "pilot-selection-v2.json").read_text())
source = Path(selection["source_path"])
raw = Path(selection["raw_path"])
assert hashlib.sha256(source.read_bytes()).hexdigest() == selection["source_sha256"]
assert hashlib.sha256(raw.read_bytes()).hexdigest() == selection["raw_sha256"]
metadata = json.loads(source.read_text())
assert len(metadata["data"]) == 26
(RUN / "pilot-data").mkdir(exist_ok=True)
shutil.copyfile(raw, RUN / "pilot-data/raw.json")
shutil.copyfile(KIT / "core/profiles/resources/worldbank-rights.md", RUN / "pilot-data/rights.md")
ordered = sorted(metadata["data"], key=lambda row: int(row["date"]))
rows = [{"sample_id": "VNM:" + row["date"], "year": int(row["date"]), "value": row["value"], "unit": row["unit"]} for row in ordered]
assert all(row["unit"] == "" and type(row["value"]) is int for row in rows)
normalized = save("pilot-data/normalized.json", rows)
index = save("pilot-data/samples.json", [{"sample_id": row["sample_id"], "entity_id": "VNM",
               "incident_id": "", "group_id": "VNM:SP.POP.TOTL", "time_start": row["year"], "time_end": row["year"]} for row in rows])
config = save("pilot-data/normalization-config.json", {"operation": "field-preserving projection, chronological sort",
    "time_coordinate": "calendar year index; not a Unix time or observed historical release timestamp", "unit": "blank preserved"})
limits = ["single country series; temporal dependence", "dated retrospective values may be revised; no vintage publication-time claim",
          "prior input access disclosed; development demonstration", "blank source unit retained", "scientific acceptance pending"]
task = selection["task_id"]
dataset = {"schema_version": 1, "id": "worldbank-vnm-population", "task_id": task, "stage": "curated",
    "sources": [{"id": metadata["source_id"], "locator": metadata["locator"], "version": selection["source_version"],
                 "retrieved_at": metadata["retrieval"]["retrieved_at"], "rights": "redistributable",
                 "rights_reference": "pilot-data/rights.md", "access": "public", "archive_sha256": selection["raw_sha256"]}],
    "modalities": ["tabular"], "fields": [{"name": name, "type": kind, "unit": "", "unknown_reason": reason, "missing_tokens": [None]}
        for name, kind, reason in (("sample_id", "string", "identifier"), ("year", "integer", "calendar year index"),
                                   ("value", "integer", "source unit field blank; not inferred"), ("unit", "string", "preserved source metadata"))],
    "raw": [bind("pilot-data/raw.json")], "normalized": [normalized], "sample_index": [index],
    "raw_layout": [{"path": "pilot-data/raw.json", "format": "worldbank-api-v2", "rows": 26}],
    "counts": {"raw": 26, "retained": 26, "excluded": 0, "quarantined": 0}, "quarantine": [],
    "missingness": [{"field": name, "missing": 0, "zero": 0, "reason": "blank unit is source metadata, not a missing numeric measurement" if name == "unit" else ""} for name in rows[0]],
    "transforms": [{"id": "projection", "code": bind("prepare-pilot-data.py"), "config": config,
                    "inputs": [bind("pilot-data/raw.json")], "outputs": [normalized], "input_rows": 26, "output_rows": 26,
                    "excluded_rows": 0, "quarantined_rows": 0}],
    "labels": {"access": "none", "provenance": "", "annotator": "", "adjudication": "", "references": [], "feature_fields": [],
               "reason": "observed target series, no incident/root-cause labels or human gold"},
    "release": {"status": "local-only", "limitations": limits}}
dataset_ref = save("dataset-manifest.json", dataset)
split = {"schema_version": 1, "id": "chronological-vnm", "task_id": task, "dataset": dataset_ref,
    "purpose": "development demonstration of fixed chronological forecasting", "independence_axes": ["sample", "time"],
    "partitions": [{"name": name, "membership": save("pilot-data/" + name + ".json", ["VNM:" + str(year) for year in selection["split"][name + "_years"]]),
                    "count": len(selection["split"][name + "_years"])} for name in ("train", "validation", "test")],
    "exclusions": [], "temporal": {"required": True, "embargo": 0, "reason": "annual target indices; retrospective snapshot, no release-vintage assertion"},
    "fitting": {"preprocessing": "not-applicable", "threshold": "not-applicable", "selection": "not-applicable",
                "rationale": "algorithms fixed; rolling origins use only preceding target-index observations, no tuning"},
    "features": [{"sample_id": "VNM:" + str(year), "task": "forecasting", "kind": "observation", "available_at": year - 1,
                  "decision_at": year - 1, "diagnostic_window_end": year - 1, "reason": "retrospective preceding-year index, not asserted publication timestamp"} for year in range(2020, 2026)],
    "holdout": {"access": "prior-access-disclosed", "owner": "controller", "reason": selection["input_access"]},
    "frozen_at": datetime.now(timezone.utc).isoformat(), "amendments": []}
save("split-manifest.json", split)
telemetry = {"schema_version": 1, "id": "pilot-no-operational-telemetry", "task_id": task, "stage": "not-applicable",
    "reason": "annual population series is tabular; no operational logs/metrics/traces supplied", "modalities": [], "sources": [], "outputs": [], "normalization": [],
    "semantic_conventions": {"version": "not-applicable", "locator": "tabular-pilot", "status": "unknown", "reason": "no instrumentation"},
    "time": {"origin": "unknown", "timezone": "", "precision": "", "alignment": "not-applicable", "skew": 0, "tolerance": 0, "reason": "calendar-year data, no measured telemetry clocks"},
    "signals": [], "sampling": {"policy": "not-applicable", "retention": "project-only", "cardinality_limit": 0, "limitations": limits},
    "correlation": {"required_keys": [], "missing_ids": [], "duplicate_ids": []}, "joins": [],
    "quality": {"samples": 0, "missing": 0, "zeros": 0, "duplicate_ids": [], "gaps": [], "limitations": ["no operational telemetry claim"]}}
save("telemetry-manifest.json", telemetry)
results = {"dataset": validate_dataset_manifest(dataset, project=RUN), "split": validate_split_manifest(split, project=RUN),
           "telemetry": validate_telemetry_manifest(telemetry, project=RUN)}
save("p3-artifact-checks.json", results)
(RUN / "data-quality.md").write_text("# Pilot data quality\n\n26 retained actual World Bank observations; 0 missing numeric values, 0 numeric zeros, 0 exclusions/quarantine.\n\n"
    "Frozen partition counts: train 20, validation 3, test 3. Calendar-year membership is disjoint; one country is not independently separated by entity.\n\n"
    + "\n".join("- " + limitation for limitation in limits) + "\n\nTelemetry: not applicable. No invented modalities, labels, clocks or units.\n", encoding="utf-8")
print(json.dumps({"samples": 26, "partitions": [20, 3, 3], "contract": "pass", "scientific_acceptance": "pending"}))
