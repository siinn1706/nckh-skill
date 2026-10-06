import copy
import unittest

from core.aiops import evaluate_predictions, ranking_metrics, validate_aiops_evaluation
from core.paths import temporary_tree
from core.schema import ContractError
from tests.research.test_datasets import save_fixture
from tests.research.test_datasets import dataset_fixture, split_fixture
from tests.research.test_statistics import analysis_plan


def protocol_fixture(root, task="forecasting"):
    """Deterministic protocol fixtures, never benchmark/native execution evidence."""
    reference = save_fixture(root, "input.json", {"fixture": True})
    record = {"schema_version": 1, "task_id": "fixture-task", "stage": "protocol", "task": task,
        "benchmark": {"source_id": "fixture", "release": "1", "suite": "fixture", "system": "fixture", "rights": "local-use-cleared",
                      "rights_reference": "deterministic fixture", "limitations": ["not actual benchmark data"]},
        "inputs": [{"kind": kind, "reference": reference} for kind in ("dataset", "split", "telemetry", "analysis")],
        "modalities": ["tabular"], "independent_unit": "fixture unit", "sample_ids": ["s1", "s2"], "evaluation_partition": "test",
        "gold": {"access": "evaluation-only", "kind": "fixture oracle", "references": [reference], "reason": "fixture only"},
        "baselines": [{"id": "naive", "role": "baseline", "input_policy": "equal fixture inputs", "budget": 1, "rationale": "fixed"}],
        "fitting": {"preprocessing": "train", "threshold": "validation", "selection": "validation"},
        "metrics": [{"id": {"rca": "hit@k", "anomaly": "recall", "forecasting": "mae", "retrieval": "ndcg@k", "agent": "success-rate"}[task],
                     "unit": "fixture", "denominator_policy": "completed-with-coverage" if task == "forecasting" else "all-issued", "definition": "frozen"}],
        "budget": {"seconds": 10, "attempts": 1, "provider_calls": 0, "egress": "none"},
        "stochastic": {"applicability": "deterministic", "seeds": [], "repeats": 0, "reason": "fixed"},
        "policies": {"ties": "stable-id" if task in {"rca", "retrieval"} else "not-applicable", "unknown": "report", "no_answer": "abstain", "no_relevant": "undefined-with-coverage",
                     "failures": "all-issued coverage", "availability": "preceding observations"},
        "rca": [], "anomaly": [], "forecasting": [], "retrieval": [], "agent": [],
        "predictions": [], "results": [], "runs": [], "failures": [], "limitations": ["fixture"]}
    record[task] = [{"rca": {"cause_unit": "service", "k": 1, "topology_provenance": "fixture", "causal_claim": "annotation-agreement",
                             "identification_evidence": "", "competing_explanations": ["symptom"]},
        "anomaly": {"label_unit": "event", "tolerance": 1, "false_alert_exposure": 10, "exposure_unit": "hours",
                    "score_kind": "binary", "calibration_evidence": "", "duplicate_alert_policy": "one event row"},
        "forecasting": {"horizon": 1, "origin_policy": "rolling", "value_field": "value", "scale": "fixture", "aggregation": "MAE",
                        "covariates": [], "pretraining_overlap": "not-applicable"},
        "retrieval": {"corpus": reference, "qrels": reference, "relevance_scale": [0, 1, 2], "k": 2,
                      "documents": [{"id": "d1", "available_at": 1, "query_at": 2}], "stages": ["retrieve"], "generation_support": [], "duplicate_policy": "unique IDs"},
        "agent": {"environment": "offline-replay", "grants": ["fixture task"], "tools": ["read"], "reset": "fixture", "workload": "fixture",
                  "fault": "none", "oracle": "fixture", "gold_access": "evaluation-only", "retrieved_authority": "untrusted-data", "actions": [],
                  "observation_action_interface": "fixture", "retries": 0, "timeout": 1, "cost_coverage": "no provider"}}[task]]
    return record


def prediction(sample="s1", **changes):
    row = {"sample_id": sample, "baseline": "naive", "status": "completed", "prediction": 8, "target": 10, "ranking": [],
           "accepted": [], "ties": [], "relevance": {}, "origin": 1, "target_time": 2, "available_at": 1, "delay": None, "reason": ""}
    row.update(changes)
    return row


def forecast_readout_fixture(root):
    record = protocol_fixture(root)
    dataset = dataset_fixture(root)
    split = split_fixture(root, dataset)
    analysis = analysis_plan()
    analysis["task_id"] = record["task_id"]
    telemetry = {"schema_version": 1, "id": "fixture-none", "task_id": record["task_id"], "stage": "not-applicable",
        "reason": "tabular fixture", "modalities": [], "sources": [], "outputs": [], "normalization": [],
        "semantic_conventions": {"version": "none", "locator": "fixture", "status": "unknown", "reason": "none"},
        "time": {"origin": "unknown", "timezone": "", "precision": "", "alignment": "not-applicable", "skew": 0, "tolerance": 0, "reason": "none"},
        "signals": [], "sampling": {"policy": "none", "retention": "fixture", "cardinality_limit": 0, "limitations": ["fixture"]},
        "correlation": {"required_keys": [], "missing_ids": [], "duplicate_ids": []}, "joins": [],
        "quality": {"samples": 0, "missing": 0, "zeros": 0, "duplicate_ids": [], "gaps": [], "limitations": ["fixture"]}}
    record["inputs"] = [{"kind": kind, "reference": save_fixture(root, kind + ".json", value)}
                        for kind, value in (("dataset", dataset), ("split", split), ("telemetry", telemetry), ("analysis", analysis))]
    record.update(stage="readout", sample_ids=["s5", "s6"], predictions=[save_fixture(root, "predictions.json",
        [prediction("s5", target=5, target_time=50, origin=49, available_at=49),
         prediction("s6", target=6, target_time=60, origin=59, available_at=59)])])
    rows = __import__("json").loads((root / "predictions.json").read_text())
    record["results"] = [save_fixture(root, "results.json", evaluate_predictions(record, rows))]
    bind_fixture_run(root, record)
    return record


def bind_fixture_run(root, record):
    record["runs"] = [save_fixture(root, "run.json", {"task_id": record["task_id"], "status": "completed-unreviewed",
        "inputs": [row["reference"] for row in record["inputs"]], "scope": "fixture, not real run",
        "outputs": [{"kind": kind, "reference": ref, "count": count} for kind, refs, count in
            (("predictions", record["predictions"], len(record["sample_ids"])), ("metrics", record["results"], 1)) for ref in refs]})]


class AIOpsTests(unittest.TestCase):
    def test_actual_fixture_graph_readout_reconciles_targets_and_metrics(self):
        with temporary_tree() as root:
            record = forecast_readout_fixture(root)
            self.assertEqual(validate_aiops_evaluation(record, project=root)["units"], 2)
            result = __import__("json").loads((root / "results.json").read_text())
            result["baselines"]["naive"]["metrics"]["mae"] += 1
            record["results"] = [save_fixture(root, "results.json", result)]
            bind_fixture_run(root, record)
            with self.assertRaisesRegex(ContractError, "oracle"):
                validate_aiops_evaluation(record, project=root)

    def test_readout_rejects_target_time_and_partition_substitution(self):
        with temporary_tree() as root:
            for change in ("target", "target_time", "partition"):
                record = forecast_readout_fixture(root)
                rows = __import__("json").loads((root / "predictions.json").read_text())
                if change == "partition":
                    record["evaluation_partition"] = "validation"
                else:
                    rows[0][change] += 1
                    record["predictions"] = [save_fixture(root, "predictions.json", rows)]
                with self.assertRaises(ContractError):
                    validate_aiops_evaluation(record, project=root)

    def test_readout_rejects_plaintext_run_receipt(self):
        import hashlib
        with temporary_tree() as root:
            record = forecast_readout_fixture(root)
            (root / "run.json").write_text("fixture plain text")
            record["runs"][0]["sha256"] = hashlib.sha256((root / "run.json").read_bytes()).hexdigest()
            with self.assertRaises(ContractError):
                validate_aiops_evaluation(record, project=root)

    def test_no_relevant_ranking_query_keeps_undefined_coverage(self):
        with temporary_tree() as root:
            record = protocol_fixture(root, "retrieval")
            record["retrieval"][0]["documents"][0]["id"] = "a"
            rows = [prediction(ranking=["a"], accepted=["a"], relevance={"a": 1}), prediction("s2", ranking=[], accepted=[], relevance={})]
            result = evaluate_predictions(record, rows)["baselines"]["naive"]
            self.assertIsNone(result["metrics"]["ndcg@k"])
            self.assertEqual(result["metric_coverage"]["ndcg@k"]["undefined"], 1)
            record["policies"]["no_relevant"] = "zero"
            self.assertEqual(evaluate_predictions(record, rows)["baselines"]["naive"]["metrics"]["ndcg@k"], 0.5)

    def test_rca_empty_gold_obeys_explicit_no_relevant_policy(self):
        with temporary_tree() as root:
            record = protocol_fixture(root, "rca")
            record["metrics"][0]["id"] = "mrr"
            rows = [prediction(accepted=[], ranking=["a"]), prediction("s2", accepted=[], ranking=[])]
            result = evaluate_predictions(record, rows)["baselines"]["naive"]
            self.assertIsNone(result["metrics"]["mrr"])
            self.assertEqual(result["metric_coverage"]["mrr"]["undefined"], 2)
            record["policies"]["no_relevant"] = "zero"
            self.assertEqual(evaluate_predictions(record, rows)["baselines"]["naive"]["metrics"]["mrr"], 0)

    def test_ranking_denominator_policy_preserves_failure_coverage(self):
        with temporary_tree() as root:
            for task in ("rca", "retrieval"):
                record = protocol_fixture(root, task)
                record["metrics"][0]["id"] = "mrr"
                rows = [prediction(accepted=["d1"], ranking=["d1"], relevance={"d1": 1}),
                        prediction("s2", status="failed", prediction=None, reason="fixture timeout")]
                for metric in record["metrics"]:
                    metric["denominator_policy"] = "completed-with-coverage"
                result = evaluate_predictions(record, rows)["baselines"]["naive"]
                self.assertEqual(result["metrics"]["mrr"], 1)
                self.assertEqual(result["metric_coverage"]["mrr"]["failed_or_unknown"], 1)
                for metric in record["metrics"]:
                    metric["denominator_policy"] = "all-issued"
                self.assertEqual(evaluate_predictions(record, rows)["baselines"]["naive"]["metrics"]["mrr"], 0.5)

    def test_retrieval_rejects_outside_corpus_and_scale(self):
        with temporary_tree() as root:
            record = protocol_fixture(root, "retrieval")
            for changes in ({"ranking": ["outside"]}, {"accepted": ["outside"], "relevance": {"outside": 1}}, {"relevance": {"d1": 3}}):
                rows = [prediction(accepted=["d1"], ranking=["d1"], relevance={"d1": 1})]
                rows[0].update(changes)
                rows.append(prediction("s2", accepted=["d1"], ranking=["d1"], relevance={"d1": 1}))
                with self.assertRaisesRegex(ContractError, "frozen"):
                    evaluate_predictions(record, rows)

    def test_readout_rejects_replacement_predictions_or_metrics_not_in_run(self):
        with temporary_tree() as root:
            for key in ("predictions", "results"):
                record = forecast_readout_fixture(root)
                data = __import__("json").loads((root / record[key][0]["path"]).read_text())
                record[key] = [save_fixture(root, "replacement-" + key + ".json", data)]
                with self.assertRaisesRegex(ContractError, "completed run outputs"):
                    validate_aiops_evaluation(record, project=root)

    def test_all_five_protocol_branches_validate(self):
        with temporary_tree() as root:
            for task in ("rca", "anomaly", "forecasting", "retrieval", "agent"):
                self.assertEqual(validate_aiops_evaluation(protocol_fixture(root, task))["stage"], "protocol")

    def test_protocol_has_exactly_one_branch_and_no_results(self):
        with temporary_tree() as root:
            record = protocol_fixture(root)
            record["forecasting"] = []
            with self.assertRaisesRegex(ContractError, "applicable"):
                validate_aiops_evaluation(record)
            record = protocol_fixture(root)
            record["runs"] = record["gold"]["references"]
            with self.assertRaisesRegex(ContractError, "protocol"):
                validate_aiops_evaluation(record)

    def test_annotation_and_topology_do_not_identify_cause(self):
        with temporary_tree() as root:
            record = protocol_fixture(root, "rca")
            record["rca"][0]["causal_claim"] = "identified"
            with self.assertRaisesRegex(ContractError, "identify"):
                validate_aiops_evaluation(record)

    def test_ranking_multiple_gold_ties_and_no_relevant(self):
        result = ranking_metrics(["a", "b", "c"], ["b", "c"], k=2, ties=[["a", "b"]], relevance={"b": 2, "c": 1})
        self.assertEqual(result["mrr"], 0.5)
        self.assertEqual(result["recall@k"], 0.5)
        self.assertAlmostEqual(result["ndcg@k"], (3 / __import__("math").log2(3)) / (3 + 1 / __import__("math").log2(3)))
        self.assertIsNone(ranking_metrics([], [], k=1, relevance={})["ndcg@k"])
        with self.assertRaisesRegex(ContractError, "stable-ID"):
            ranking_metrics(["b", "a"], ["a"], k=1, ties=[["a", "b"]])

    def test_forecast_actual_errors_and_coverage(self):
        with temporary_tree() as root:
            record = protocol_fixture(root)
            rows = [prediction(), prediction("s2", prediction=16, target=10)]
            result = evaluate_predictions(record, rows)["baselines"]["naive"]
            self.assertEqual(result["metrics"]["mae"], 4)
            rows[1].update(status="failed", prediction=None, reason="timeout")
            result = evaluate_predictions(record, rows)["baselines"]["naive"]
            self.assertEqual(result["counts"], {"total": 2, "completed": 1, "failed": 1, "unknown": 0})
            self.assertEqual(result["metrics"]["mae"], 2)
            record["metrics"][0]["denominator_policy"] = "all-issued"
            self.assertIsNone(evaluate_predictions(record, rows)["baselines"]["naive"]["metrics"]["mae"])

    def test_missing_and_duplicate_prediction_units_rejected(self):
        with temporary_tree() as root:
            record = protocol_fixture(root)
            for rows in ([prediction()], [prediction(), prediction()]):
                with self.assertRaises(ContractError):
                    evaluate_predictions(record, rows)

    def test_future_horizon_covariate_and_corpus_leakage(self):
        with temporary_tree() as root:
            record = protocol_fixture(root)
            for changes in ({"available_at": 2}, {"target_time": 3}):
                with self.assertRaisesRegex(ContractError, "leakage"):
                    evaluate_predictions(record, [prediction(**changes), prediction("s2")])
            record["forecasting"][0]["covariates"] = [{"id": "future", "available_at": 3, "decision_at": 2}]
            with self.assertRaisesRegex(ContractError, "future"):
                validate_aiops_evaluation(record)
            record = protocol_fixture(root, "retrieval")
            record["retrieval"][0]["documents"][0]["available_at"] = 3
            with self.assertRaisesRegex(ContractError, "corpus"):
                validate_aiops_evaluation(record)

    def test_threshold_test_fit_and_calibration_claim_rejected(self):
        with temporary_tree() as root:
            record = protocol_fixture(root, "anomaly")
            record["fitting"]["threshold"] = "test"
            with self.assertRaises(ContractError):
                validate_aiops_evaluation(record)
            record = protocol_fixture(root, "anomaly")
            record["anomaly"][0]["score_kind"] = "calibrated-probability"
            with self.assertRaisesRegex(ContractError, "calibration"):
                validate_aiops_evaluation(record)

    def test_agent_failure_denominator_and_retrieved_instruction_authority(self):
        with temporary_tree() as root:
            record = protocol_fixture(root, "agent")
            rows = [prediction(prediction=True), prediction("s2", prediction=None, status="failed", reason="timeout")]
            self.assertEqual(evaluate_predictions(record, rows)["baselines"]["naive"]["metrics"]["success-rate"], 0.5)
            record["agent"][0]["actions"] = [{"tool": "read", "authorized": True, "source": "retrieved-data"}]
            with self.assertRaisesRegex(ContractError, "authority"):
                validate_aiops_evaluation(record)

    def test_anomaly_event_denominators_delay_and_duplicate_coverage(self):
        with temporary_tree() as root:
            record = protocol_fixture(root, "anomaly")
            rows = [prediction(prediction=True, target=True, delay=1, available_at=2), prediction("s2", prediction=False, target=True)]
            self.assertEqual(evaluate_predictions(record, rows)["baselines"]["naive"]["metrics"]["recall"], 0.5)
            rows[0]["delay"] = -1
            with self.assertRaisesRegex(ContractError, "negative"):
                evaluate_predictions(record, rows)


if __name__ == "__main__":
    unittest.main()
