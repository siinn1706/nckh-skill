import copy
import hashlib
import json
import unittest

from core.paths import temporary_tree
from core.research_io import ArtifactReader, ResearchLimits
from core.schema import ContractError
from core.statistics import paired_difference_summary, validate_statistical_analysis


def analysis_plan():
    """Deterministic contract fixture; no observed or human-gold result."""
    return {
        "schema_version": 1, "task_id": "fixture-comparison", "stage": "plan",
        "protocol": {"path": "protocol.md", "sha256": "a" * 64},
        "question": "What is the paired descriptive difference?", "estimand": "candidate minus baseline",
        "population": "declared fixture incidents",
        "unit": {"kind": "incident", "mapping_field": "incident_id", "observation_ids": ["w1", "w2"], "independent_ids": ["i1", "i2"],
                 "independent_n": 2, "nesting": [{"observation_id": "w1", "independent_id": "i1"},
                                                  {"observation_id": "w2", "independent_id": "i2"}],
                 "independence_evidence": "fixture represents distinct incidents"},
        "inputs": [], "design": {"claim_type": "descriptive", "dependence": "independent",
                                  "identification_evidence": "", "rationale": "exact incident pairing"},
        "estimator": {"name": "mean paired difference", "required_assumptions": ["independence"],
                      "rationale": "question is descriptive"},
        "assumptions": [{"id": "independence", "requirement": "distinct incidents", "status": "pending",
                         "evidence_or_reason": "", "limitations": []}],
        "effect": {"metric": "difference", "contrast": "candidate-baseline", "scale": "original"},
        "missingness": {"policy": "retain missing and failures in denominator", "rationale": "avoid success-only selection"},
        "uncertainty": {"method": "iid-bootstrap", "unit": "incident", "replications": 100,
                        "status": "planned", "reason": ""},
        "multiplicity": {"family": ["primary"], "policy": "one prespecified contrast", "rationale": "single question"},
        "comparison": {"mode": "paired", "baseline_units": ["i1", "i2"], "candidate_units": ["i1", "i2"], "reason": ""},
        "stopping": {"rule": "all frozen units; keep failed attempts", "frozen_at": "2026-10-06T09:00:00+07:00", "amendments": []},
        "seed": {"status": "specified", "value": 42, "reason": ""},
        "denominators": {"total": 2, "completed": 2, "failed": 0, "missing": 0}, "runs": [], "outputs": [],
        "result": {"status": "planned", "estimate": None, "standard_error": None,
                   "interval_lower": None, "interval_upper": None}, "failures": [],
        "limitations": ["fixture only; no actual data/run or independent scientific review"],
    }


class StatisticsTests(unittest.TestCase):
    def setUp(self):
        self.plan = analysis_plan()

    def invalid(self, change):
        change(self.plan)
        with self.assertRaises(ContractError):
            validate_statistical_analysis(self.plan)

    def test_plan_accepts_pending_assumptions_without_inventing_result(self):
        self.assertEqual(validate_statistical_analysis(self.plan)["scientific_acceptance"], "pending")

    def test_plan_rejects_observed_zero_as_well_as_nonzero_results(self):
        for value in (0, 1):
            record = copy.deepcopy(self.plan)
            record["result"]["estimate"] = value
            with self.assertRaises(ContractError):
                validate_statistical_analysis(record)

    def test_repeated_windows_do_not_inflate_independent_n(self):
        self.plan["unit"]["nesting"][1]["independent_id"] = "i1"
        self.plan["unit"]["independent_ids"] = ["i1"]
        self.invalid(lambda r: r["unit"].update(independent_n=2))

    def test_time_or_cluster_dependence_rejects_iid_uncertainty(self):
        for dependence in ("temporal", "clustered", "unknown"):
            record = copy.deepcopy(self.plan)
            record["design"]["dependence"] = dependence
            with self.assertRaises(ContractError):
                validate_statistical_analysis(record)

    def test_pairing_requires_same_actual_independent_membership(self):
        self.invalid(lambda r: r["comparison"].update(candidate_units=["i1"]))

    def test_estimator_cannot_omit_its_assumption(self):
        self.invalid(lambda r: r.update(assumptions=[]))

    def test_failed_or_missing_denominators_cannot_disappear(self):
        self.invalid(lambda r: r["denominators"].update(completed=1))

    def test_multiplicity_and_stopping_policies_are_required(self):
        self.invalid(lambda r: r["multiplicity"].update(rationale=""))

    def test_amendments_cannot_rewrite_prior_chronology(self):
        self.invalid(lambda r: r["stopping"].update(amendments=[{
            "at": "2026-10-05T09:00:00+07:00", "reason": "fixture", "previous_rule": "old", "new_rule": "new"}]))

    def test_deterministic_not_applicable_seed_requires_reason(self):
        self.plan["seed"] = {"status": "not-applicable", "value": None, "reason": "fixed arithmetic"}
        self.assertEqual(validate_statistical_analysis(self.plan)["contract"], "pass")
        self.invalid(lambda r: r["seed"].update(reason=""))

    def test_unknown_fields_and_nonfinite_values_fail(self):
        self.invalid(lambda r: r.update(secret_field="not admitted"))
        self.plan = analysis_plan()
        self.invalid(lambda r: r["result"].update(estimate=float("nan")))

    def readout(self, root):
        record = copy.deepcopy(self.plan)
        def binding(name):
            path = root / name
            path.write_text("deterministic fixture artifact; not a real run", encoding="utf-8")
            return {"path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        record.update(stage="readout", protocol=binding("protocol.md"),
                      inputs=[{"kind": "dataset", "reference": binding("dataset.json")},
                              {"kind": "split", "reference": binding("split.json")}],
                      runs=[binding("run.json")], outputs=[binding("results.json")])
        from tests.research.test_datasets import dataset_fixture, split_fixture, save_fixture
        data = dataset_fixture(root)
        data["task_id"] = record["task_id"]
        split = split_fixture(root, data)
        split["task_id"] = record["task_id"]
        record["inputs"] = [{"kind": "dataset", "reference": save_fixture(root, "dataset.json", data)},
                            {"kind": "split", "reference": save_fixture(root, "split.json", split)}]
        record["unit"].update(observation_ids=["s5", "s6"], independent_ids=["i5", "i6"],
                              nesting=[{"observation_id": "s5", "independent_id": "i5"}, {"observation_id": "s6", "independent_id": "i6"}])
        record["comparison"].update(baseline_units=["i5", "i6"], candidate_units=["i5", "i6"])
        record["runs"] = [save_fixture(root, "run.json", {"schema_version": 1, "task_id": record["task_id"],
                         "status": "completed-unreviewed", "inputs": [row["reference"] for row in record["inputs"]], "evidence": "deterministic fixture, not real execution"})]
        record["result"].update(status="computed", estimate=0)
        record["uncertainty"].update(method="descriptive-only", status="not-applicable", reason="no interval claimed")
        output = {"schema_version": 1, "task_id": record["task_id"], "result": record["result"], "denominators": record["denominators"]}
        path = root / "results.json"
        path.write_text(json.dumps(output), encoding="utf-8")
        record["outputs"][0]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.bind_run_outputs(root, record)
        return record

    def bind_run_outputs(self, root, record):
        from tests.research.test_datasets import save_fixture
        run = json.loads((root / "run.json").read_text())
        run["outputs"] = [{"kind": "statistics", "reference": ref, "count": 1} for ref in record["outputs"]]
        record["runs"] = [save_fixture(root, "run.json", run)]

    def test_readout_binds_actual_files_and_preserves_zero(self):
        with temporary_tree() as root:
            record = self.readout(root)
            self.assertEqual(validate_statistical_analysis(record, project=root)["contract"], "pass")
            (root / "results.json").write_text("changed fixture", encoding="utf-8")
            with self.assertRaisesRegex(ContractError, "stale"):
                validate_statistical_analysis(record, project=root)

    def test_readout_without_actual_run_cannot_pass(self):
        self.plan["stage"] = "readout"
        with self.assertRaises(ContractError):
            validate_statistical_analysis(self.plan)

    def test_uncertainty_cannot_promote_unverified_estimator_assumptions(self):
        with temporary_tree() as root:
            record = self.readout(root)
            record["uncertainty"].update(status="computed", method="iid-standard-error")
            record["result"]["standard_error"] = 0
            output = {"schema_version": 1, "task_id": record["task_id"], "result": record["result"], "denominators": record["denominators"]}
            (root / "results.json").write_text(json.dumps(output), encoding="utf-8")
            record["outputs"][0]["sha256"] = hashlib.sha256((root / "results.json").read_bytes()).hexdigest()
            self.bind_run_outputs(root, record)
            with self.assertRaisesRegex(ContractError, "assumptions"):
                validate_statistical_analysis(record, project=root)

    def test_readout_values_cannot_differ_from_bound_actual_result(self):
        with temporary_tree() as root:
            record = self.readout(root)
            record["result"]["estimate"] = 100
            with self.assertRaisesRegex(ContractError, "bound actual"):
                validate_statistical_analysis(record, project=root)

    def test_readout_rejects_replacement_result_absent_from_run(self):
        from tests.research.test_datasets import save_fixture
        with temporary_tree() as root:
            record = self.readout(root)
            record["result"]["estimate"] = 7
            record["outputs"] = [save_fixture(root, "replacement.json", {"schema_version": 1, "task_id": record["task_id"],
                "result": record["result"], "denominators": record["denominators"]})]
            with self.assertRaisesRegex(ContractError, "actual run output"):
                validate_statistical_analysis(record, project=root)

    def test_causal_readout_requires_identification_evidence(self):
        with temporary_tree() as root:
            record = self.readout(root)
            record["design"]["claim_type"] = "causal"
            with self.assertRaisesRegex(ContractError, "identification"):
                validate_statistical_analysis(record, project=root)

    def test_descriptive_pairing_does_not_make_missing_zero(self):
        result = paired_difference_summary({"i1": 2, "i2": 3}, {"i1": 2, "i2": 3})
        self.assertEqual(result["mean_difference"], 0)
        self.assertEqual(result["uncertainty"], "not-computed")
        for candidate in ({"i1": 2}, {"i1": None, "i2": 3}):
            with self.assertRaises(ContractError):
                paired_difference_summary({"i1": 2, "i2": 3}, candidate)

    def test_finite_inputs_cannot_emit_infinite_derived_difference(self):
        with self.assertRaisesRegex(ContractError, "finite"):
            paired_difference_summary({"i1": -1e308}, {"i1": 1e308})

    def test_additional_readout_output_cannot_bypass_record_budget(self):
        from tests.research.test_datasets import save_fixture
        with temporary_tree() as root:
            record = self.readout(root)
            record["outputs"].append(save_fixture(root, "many.json", list(range(10000))))
            with self.assertRaisesRegex(ContractError, "record budget"):
                validate_statistical_analysis(record, reader=ArtifactReader(root, ResearchLimits(records=1000)))

    def test_readout_rejects_wrong_dataset_task_mapping_or_plaintext_run(self):
        from tests.research.test_datasets import save_fixture
        with temporary_tree() as root:
            for change in ("task", "membership", "run"):
                record = self.readout(root)
                if change == "task":
                    record["task_id"] = "other-task"
                elif change == "membership":
                    record["unit"]["nesting"][0]["independent_id"] = "i6"
                else:
                    (root / "run.json").write_text("plain fixture text", encoding="utf-8")
                    record["runs"][0]["sha256"] = hashlib.sha256((root / "run.json").read_bytes()).hexdigest()
                with self.assertRaises(ContractError):
                    validate_statistical_analysis(record, project=root)


class ResearchReadTests(unittest.TestCase):
    def test_record_limit_rejects_before_json_decode_or_array_allocation(self):
        from unittest.mock import patch
        with temporary_tree() as root:
            path = root / "many.json"
            path.write_text('[{"id":1},{"id":2}]', encoding="utf-8")
            reference = {"path": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            with patch("core.research_io.json.loads", side_effect=AssertionError("must not parse")):
                with self.assertRaisesRegex(ContractError, "record budget"):
                    ArtifactReader(root, ResearchLimits(records=1)).bound_json(reference)
            with patch("core.research_io.json.JSONDecoder.raw_decode", side_effect=AssertionError("must not allocate rows")):
                with self.assertRaisesRegex(ContractError, "record budget"):
                    ArtifactReader(root, ResearchLimits(records=1)).rows(reference)

    def test_per_file_and_aggregate_caps_apply_before_parse(self):
        with temporary_tree() as root:
            (root / "large.json").write_bytes(b"x" * 11)
            reader = ArtifactReader(root, ResearchLimits(file_bytes=10, aggregate_bytes=15))
            with self.assertRaisesRegex(ContractError, "per-file"):
                reader.json("large.json")
            self.assertEqual(reader.bytes_read, 0)
            (root / "a.json").write_bytes(b"12345678")
            (root / "b.json").write_bytes(b"12345678")
            reader.read("a.json")
            with self.assertRaisesRegex(ContractError, "aggregate"):
                reader.read("b.json")
            self.assertEqual(reader.bytes_read, 8)

    def test_duplicate_fields_and_nonfinite_json_are_rejected(self):
        with temporary_tree() as root:
            for data in ('{"x":1,"x":2}', '{"x":NaN}'):
                (root / "fixture.json").write_text(data, encoding="utf-8")
                with self.assertRaises(ContractError):
                    ArtifactReader(root).json("fixture.json")

    def test_traversal_and_record_output_limits_are_rejected(self):
        with temporary_tree() as root:
            reader = ArtifactReader(root, ResearchLimits(records=1, output_bytes=10))
            with self.assertRaises(ContractError):
                reader.read("../outside.json")
            reader.count(1)
            with self.assertRaises(ContractError):
                reader.count(1)
            with self.assertRaises(ContractError):
                reader.output({"oversized": "fixture"})


if __name__ == "__main__":
    unittest.main()
