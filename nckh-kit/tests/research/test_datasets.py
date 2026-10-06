import copy
import hashlib
import json
import unittest

from core.datasets import validate_dataset_manifest, validate_split_manifest
from core.paths import temporary_tree
from core.research_io import ArtifactReader, ResearchLimits
from core.schema import ContractError


def save_fixture(root, name, value):
    path = root / name
    path.write_text(json.dumps(value), encoding="utf-8")
    return {"path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def dataset_fixture(root):
    """Bounded deterministic rows, never observed telemetry or human gold."""
    rows = [{"sample_id": f"s{i}", "value": 0 if i == 1 else None if i == 2 else i} for i in range(1, 7)]
    normalized = save_fixture(root, "normalized.json", rows)
    index = [{"sample_id": f"s{i}", "entity_id": f"e{i}", "incident_id": f"i{i}", "group_id": f"g{i}",
              "time_start": i * 10, "time_end": i * 10 + 1} for i in range(1, 7)]
    raw = save_fixture(root, "raw.json", rows)
    config = save_fixture(root, "config.json", {"fixture": "identity transform"})
    code = save_fixture(root, "code.json", {"fixture": "identity transform source observation"})
    return {"schema_version": 1, "id": "fixture-data", "task_id": "fixture-task", "stage": "curated",
            "sources": [{"id": "fixture", "locator": "deterministic-test-fixture", "version": "1",
                         "retrieved_at": "2026-10-06T09:00:00+07:00", "rights": "local-use-cleared",
                         "rights_reference": "fixture-only; not a real data grant", "access": "supplied-private", "archive_sha256": raw["sha256"]}],
            "modalities": ["tabular"], "fields": [{"name": "sample_id", "type": "string", "unit": "", "unknown_reason": "identifier", "missing_tokens": []},
                                                       {"name": "value", "type": "number", "unit": "fixture-unit", "unknown_reason": "", "missing_tokens": [None]}],
            "raw": [raw], "normalized": [normalized], "sample_index": [save_fixture(root, "samples.json", index)],
            "raw_layout": [{"path": raw["path"], "format": "canonical-json-array", "rows": 6}],
            "counts": {"raw": 6, "retained": 6, "excluded": 0, "quarantined": 0}, "quarantine": [],
            "missingness": [{"field": "sample_id", "missing": 0, "zero": 0, "reason": ""}, {"field": "value", "missing": 1, "zero": 1, "reason": "fixture missing value"}],
            "transforms": [{"id": "identity", "code": code, "config": config, "inputs": [raw], "outputs": [normalized],
                            "input_rows": 6, "output_rows": 6, "excluded_rows": 0, "quarantined_rows": 0}],
            "labels": {"access": "none", "provenance": "", "annotator": "", "adjudication": "", "references": [], "feature_fields": [], "reason": "fixture contains no gold"},
            "release": {"status": "local-only", "limitations": ["deterministic fixture"]}}


def split_fixture(root, dataset):
    return {"schema_version": 1, "id": "fixture-split", "task_id": "fixture-task",
            "dataset": save_fixture(root, "dataset.json", dataset), "purpose": "deterministic leakage checks",
            "independence_axes": ["sample", "incident", "time"],
            "partitions": [{"name": name, "membership": save_fixture(root, name + ".json", ids), "count": len(ids)}
                           for name, ids in (("train", ["s1", "s2"]), ("validation", ["s3", "s4"]), ("test", ["s5", "s6"]))],
            "exclusions": [], "temporal": {"required": True, "embargo": 0, "reason": "chronological fixture"},
            "fitting": {"preprocessing": "train", "threshold": "validation", "selection": "validation", "rationale": "protected test"},
            "features": [{"sample_id": "s5", "task": "forecasting", "kind": "observation", "available_at": 49,
                          "decision_at": 49, "diagnostic_window_end": 50, "reason": "preceding observation"}],
            "holdout": {"access": "development", "owner": "fixture", "reason": "fixture already known"},
            "frozen_at": "2026-10-06T09:00:00+07:00", "amendments": []}


class DatasetTests(unittest.TestCase):
    def test_empty_intermediate_cannot_claim_six_transformed_rows(self):
        with temporary_tree() as root:
            record = dataset_fixture(root)
            first = copy.deepcopy(record["transforms"][0])
            first["outputs"] = [save_fixture(root, "intermediate.json", [])]
            second = copy.deepcopy(record["transforms"][0])
            second["id"] = "second"
            second["inputs"] = first["outputs"]
            record["transforms"] = [first, second]
            with self.assertRaisesRegex(ContractError, "intermediate"):
                validate_dataset_manifest(record, project=root)

    def test_nested_jsonl_records_cannot_bypass_preallocation_budget(self):
        with temporary_tree() as root:
            record = dataset_fixture(root)
            (root / "nested.jsonl").write_text("\n".join(json.dumps([0] * 2000) for _ in range(6)) + "\n", encoding="utf-8")
            raw = {"path": "nested.jsonl", "sha256": hashlib.sha256((root / "nested.jsonl").read_bytes()).hexdigest()}
            record["raw"] = [raw]
            record["raw_layout"] = [{"path": raw["path"], "format": "jsonl", "rows": 6}]
            record["transforms"][0]["inputs"] = [raw]
            with self.assertRaisesRegex(ContractError, "record budget"):
                validate_dataset_manifest(record, reader=ArtifactReader(root, ResearchLimits(records=1000)))

    def test_declared_counts_cannot_hide_empty_raw_or_protected_gold_alias(self):
        with temporary_tree() as root:
            record = dataset_fixture(root)
            raw = save_fixture(root, "empty.json", [])
            record["raw"] = [raw]
            record["raw_layout"] = [{"path": raw["path"], "format": "canonical-json-array", "rows": 6}]
            with self.assertRaisesRegex(ContractError, "raw count"):
                validate_dataset_manifest(record, project=root)
            record = dataset_fixture(root)
            record["labels"].update(access="protected-evaluation-only", provenance="fixture", references=record["normalized"])
            with self.assertRaisesRegex(ContractError, "alias"):
                validate_dataset_manifest(record, project=root)

    def test_forecast_origin_cannot_follow_the_actual_target_interval(self):
        with temporary_tree() as root:
            record = split_fixture(root, dataset_fixture(root))
            record["features"][0].update(available_at=55, decision_at=60)
            with self.assertRaisesRegex(ContractError, "origin"):
                validate_split_manifest(record, project=root)

    def test_actual_membership_and_missing_zero_reconcile(self):
        with temporary_tree() as root:
            record = dataset_fixture(root)
            self.assertEqual(len(validate_dataset_manifest(record, project=root)["samples"]), 6)
            record["missingness"][1]["zero"] = 0
            with self.assertRaisesRegex(ContractError, "missing and zero"):
                validate_dataset_manifest(record, project=root)

    def test_unresolved_rights_keep_acquisition_gate_closed(self):
        with temporary_tree() as root:
            record = dataset_fixture(root)
            record["sources"][0]["rights"] = "pending"
            with self.assertRaisesRegex(ContractError, "rights"):
                validate_dataset_manifest(record, project=root)
            record.update(stage="metadata", raw=[], raw_layout=[], normalized=[], sample_index=[], transforms=[])
            self.assertEqual(validate_dataset_manifest(record)["data_acceptance"], "pending")

    def test_duplicate_or_conflicting_samples_cannot_silently_overwrite(self):
        with temporary_tree() as root:
            record = dataset_fixture(root)
            rows = json.loads((root / "normalized.json").read_text())
            rows[1]["sample_id"] = "s1"
            record["normalized"] = [save_fixture(root, "conflict.json", rows)]
            with self.assertRaisesRegex(ContractError, "unique"):
                validate_dataset_manifest(record, project=root)

    def test_unknown_unit_cannot_be_guessed_or_omit_reason(self):
        with temporary_tree() as root:
            record = dataset_fixture(root)
            record["fields"][1].update(unit="", unknown_reason="")
            with self.assertRaisesRegex(ContractError, "units"):
                validate_dataset_manifest(record, project=root)

    def test_gold_feature_and_unlicensed_release_fail(self):
        with temporary_tree() as root:
            record = dataset_fixture(root)
            record["labels"]["feature_fields"] = ["root_cause"]
            with self.assertRaisesRegex(ContractError, "gold"):
                validate_dataset_manifest(record, project=root)
            record["labels"]["feature_fields"] = []
            record["release"]["status"] = "redistributable"
            with self.assertRaisesRegex(ContractError, "redistribution"):
                validate_dataset_manifest(record, project=root)

    def test_transform_config_and_count_drift_invalidate_data(self):
        with temporary_tree() as root:
            record = dataset_fixture(root)
            record["transforms"][0]["output_rows"] = 5
            with self.assertRaisesRegex(ContractError, "lineage"):
                validate_dataset_manifest(record, project=root)
            record["transforms"][0]["output_rows"] = 6
            (root / "config.json").write_text("changed fixture config", encoding="utf-8")
            with self.assertRaisesRegex(ContractError, "stale"):
                validate_dataset_manifest(record, project=root)

    def test_aggregate_bounds_cover_many_individually_small_inputs(self):
        with temporary_tree() as root:
            record = dataset_fixture(root)
            reader = ArtifactReader(root, ResearchLimits(file_bytes=10000, aggregate_bytes=600))
            with self.assertRaisesRegex(ContractError, "aggregate"):
                validate_dataset_manifest(record, project=root, reader=reader)


class SplitTests(unittest.TestCase):
    def test_exact_incident_time_split_passes(self):
        with temporary_tree() as root:
            record = split_fixture(root, dataset_fixture(root))
            self.assertEqual(validate_split_manifest(record, project=root)["members"], 6)

    def test_distinct_hashes_do_not_hide_actual_membership_overlap(self):
        with temporary_tree() as root:
            record = split_fixture(root, dataset_fixture(root))
            record["partitions"][2]["membership"] = save_fixture(root, "overlap.json", ["s2", "s6"])
            self.assertNotEqual(record["partitions"][0]["membership"]["sha256"], record["partitions"][2]["membership"]["sha256"])
            with self.assertRaisesRegex(ContractError, "overlaps"):
                validate_split_manifest(record, project=root)

    def test_distinct_rows_cannot_hide_shared_incident(self):
        with temporary_tree() as root:
            dataset = dataset_fixture(root)
            samples = json.loads((root / "samples.json").read_text())
            samples[4]["incident_id"] = "i1"
            dataset["sample_index"] = [save_fixture(root, "shared-incident.json", samples)]
            record = split_fixture(root, dataset)
            with self.assertRaisesRegex(ContractError, "incident"):
                validate_split_manifest(record, project=root)

    def test_interval_overlap_and_embargo_are_actual_not_hash_only(self):
        with temporary_tree() as root:
            record = split_fixture(root, dataset_fixture(root))
            record["temporal"]["embargo"] = 10
            with self.assertRaisesRegex(ContractError, "embargo"):
                validate_split_manifest(record, project=root)

    def test_future_features_and_gold_leakage_fail(self):
        with temporary_tree() as root:
            record = split_fixture(root, dataset_fixture(root))
            record["features"][0]["available_at"] = 51
            with self.assertRaisesRegex(ContractError, "unavailable"):
                validate_split_manifest(record, project=root)
            record["features"][0].update(available_at=49, kind="gold-label")
            with self.assertRaisesRegex(ContractError, "gold"):
                validate_split_manifest(record, project=root)

    def test_rca_frozen_incident_window_is_permitted(self):
        with temporary_tree() as root:
            record = split_fixture(root, dataset_fixture(root))
            record["features"][0].update(task="rca", available_at=55, decision_at=60, diagnostic_window_end=60,
                                         reason="authorized incident-window observation; not a gold label")
            self.assertEqual(validate_split_manifest(record, project=root)["contract"], "pass")

    def test_test_fitted_transform_or_threshold_is_rejected(self):
        with temporary_tree() as root:
            record = split_fixture(root, dataset_fixture(root))
            for field in ("preprocessing", "threshold", "selection"):
                altered = copy.deepcopy(record)
                altered["fitting"][field] = "test"
                with self.assertRaises(ContractError):
                    validate_split_manifest(altered, project=root)


if __name__ == "__main__":
    unittest.main()
