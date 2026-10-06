"""Bounded task protocols and descriptive evaluation, without benchmark execution."""

import math

from core.datasets import validate_dataset_manifest, validate_split_manifest
from core.research_io import ArtifactReader, finite_number, receipt_outputs, unique_ids
from core.schema import ContractError, validate_record
from core.statistics import validate_statistical_analysis
from core.telemetry import validate_telemetry_manifest


TASKS = {"rca", "anomaly", "forecasting", "retrieval", "agent"}
METRICS = {"rca": {"hit@k", "mrr"}, "anomaly": {"precision", "recall", "false-alert-rate", "mean-delay"},
           "forecasting": {"mae"}, "retrieval": {"recall@k", "mrr", "ndcg@k"}, "agent": {"success-rate"}}


def ranking_metrics(ranking, accepted, *, k, ties=(), relevance=None):
    """Stable-ID tie handling and first accepted rank; no causal interpretation."""
    ranked = unique_ids(ranking, "ranked candidates")
    gold = unique_ids(accepted, "accepted answers")
    if type(k) is not int or k <= 0:
        raise ContractError("ranking k must be a positive integer")
    tied = set()
    for group in ties:
        ids = unique_ids(group, "tie group")
        if len(group) < 2 or not ids <= ranked or tied & ids:
            raise ContractError("tie groups must contain disjoint actual candidates")
        positions = [ranking.index(item) for item in group]
        ordered = ranking[min(positions):max(positions) + 1]
        if len(ordered) != len(group) or ordered != sorted(group):
            raise ContractError("tie groups require contiguous stable-ID order")
        tied |= ids
    first = next((i for i, item in enumerate(ranking, 1) if item in gold), None)
    hits = len(set(ranking[:k]) & gold)
    result = {"hit@k": float(hits > 0) if gold else None, "mrr": (1 / first if first else 0.0) if gold else None,
              "recall@k": hits / len(gold) if gold else None, "ndcg@k": None}
    if relevance is not None:
        if set(relevance) != gold:
            raise ContractError("graded relevance must cover the exact accepted answers")
        if any(finite_number(value, "relevance grade") < 0 or value > 30 for value in relevance.values()):
            raise ContractError("relevance grades must be bounded nonnegative values")
        def dcg(values): return sum((2 ** grade - 1) / math.log2(i + 2) for i, grade in enumerate(values))
        ideal = dcg(sorted(relevance.values(), reverse=True)[:k])
        result["ndcg@k"] = dcg([relevance.get(item, 0) for item in ranking[:k]]) / ideal if ideal else None
    return result


def _protocol_invariants(record):
    task = record["task"]
    for branch in TASKS:
        if len(record[branch]) != (1 if branch == task else 0):
            raise ContractError("exactly one applicable task protocol is required")
    if not record["independent_unit"] or not record["modalities"]:
        raise ContractError("actual modality and independent unit must be explicit")
    unique_ids(record["modalities"], "evaluation modalities")
    samples = unique_ids(record["sample_ids"], "evaluation samples")
    if not samples:
        raise ContractError("evaluation cannot have empty expected membership")
    if record["gold"]["access"] == "unavailable" and record["gold"]["references"]:
        raise ContractError("unavailable gold cannot claim actual oracle references")
    baselines = unique_ids([row["id"] for row in record["baselines"]], "evaluation baselines")
    if not baselines or not any(row["role"] == "baseline" for row in record["baselines"]):
        raise ContractError("evaluation requires an explicit baseline")
    for row in record["baselines"]:
        if row["budget"] < 0:
            raise ContractError("baseline budget cannot be negative")
    metric_ids = unique_ids([row["id"] for row in record["metrics"]], "evaluation metrics")
    if not metric_ids or not metric_ids <= METRICS[task]:
        raise ContractError("metrics must have task-specific supported definitions")
    if any(record["budget"][name] < 0 for name in ("seconds", "attempts", "provider_calls")):
        raise ContractError("evaluation limits cannot be negative")
    stochastic = record["stochastic"]
    if stochastic["applicability"] == "deterministic":
        if stochastic["seeds"] or stochastic["repeats"] != 0 or not stochastic["reason"]:
            raise ContractError("deterministic methods cannot invent seeds/replications")
    elif not stochastic["seeds"] or len(set(stochastic["seeds"])) != len(stochastic["seeds"]) or stochastic["repeats"] <= 0:
        raise ContractError("stochastic evaluation requires actual unique seeds and repetitions")
    if task in {"rca", "retrieval"}:
        if record["policies"]["ties"] != "stable-id" or record[task][0]["k"] <= 0:
            raise ContractError("ranking requires positive k and explicit stable-ID tie handling")
    elif record["policies"]["ties"] != "not-applicable":
        raise ContractError("non-ranking task cannot declare ranking ties")
    if task == "rca":
        branch = record[task][0]
        if branch["causal_claim"] == "identified" and not branch["identification_evidence"]:
            raise ContractError("topology/correlation/annotation cannot alone identify cause")
    elif task == "anomaly":
        branch = record[task][0]
        if branch["tolerance"] < 0 or branch["false_alert_exposure"] <= 0:
            raise ContractError("anomaly tolerance and actual false-alert exposure must be defined")
        if branch["score_kind"] == "calibrated-probability" and not branch["calibration_evidence"]:
            raise ContractError("scores require evidence before probability calibration claims")
    elif task == "forecasting":
        branch = record[task][0]
        if branch["horizon"] <= 0:
            raise ContractError("forecasting requires a positive horizon")
        for covariate in branch["covariates"]:
            if covariate["available_at"] > covariate["decision_at"]:
                raise ContractError("future covariate leakage at forecast origin")
    elif task == "retrieval":
        branch = record[task][0]
        unique_ids([row["id"] for row in branch["documents"]], "corpus documents")
        if (not branch["relevance_scale"] or len(set(branch["relevance_scale"])) != len(branch["relevance_scale"])
                or any(value < 0 or value > 30 for value in branch["relevance_scale"])):
            raise ContractError("retrieval requires bounded relevance scale")
        if any(row["available_at"] > row["query_at"] for row in branch["documents"]):
            raise ContractError("future corpus document leakage")
        if "generate" in branch["stages"] and not branch["generation_support"]:
            raise ContractError("generation requires separate bound source-support evidence")
    elif task == "agent":
        branch = record[task][0]
        if branch["timeout"] <= 0:
            raise ContractError("agent timeout must be bounded and positive")
        if branch["environment"] == "authorized-disposable" and not branch["grants"]:
            raise ContractError("disposable environment requires explicit task grants")
        tools = unique_ids(branch["tools"], "agent tools")
        for action in branch["actions"]:
            if action["authorized"] and (action["source"] != "task-grant" or action["tool"] not in tools):
                raise ContractError("retrieved data cannot grant agent tool authority")
    return samples, baselines


def evaluate_predictions(record, rows):
    """Recompute frozen descriptive metrics; failed/missing units retain coverage."""
    task = record["task"]
    samples, baselines = _protocol_invariants(record)
    expected_fields = {"sample_id", "baseline", "status", "prediction", "target", "ranking", "accepted", "ties", "relevance",
                       "origin", "target_time", "available_at", "delay", "reason"}
    by_baseline = {name: [] for name in baselines}
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != expected_fields:
            raise ContractError("prediction rows require exact canonical fields")
        if (any(not isinstance(row[name], str) for name in ("sample_id", "baseline", "status", "reason"))
                or any(not isinstance(row[name], list) for name in ("ranking", "accepted", "ties")) or not isinstance(row["relevance"], dict)):
            raise ContractError("prediction identity/ranking/oracle types are invalid")
        key = (row["baseline"], row["sample_id"])
        if key in seen or key[0] not in baselines or key[1] not in samples:
            raise ContractError("prediction membership duplicate or outside frozen evaluation")
        seen.add(key)
        if row["status"] not in {"completed", "failed", "unknown", "abstained"}:
            raise ContractError("unsupported prediction outcome")
        if row["status"] != "completed" and (not row["reason"] or row["prediction"] is not None or row["ranking"]):
            raise ContractError("failed/unknown/abstained predictions need reason and no claimed prediction")
        if task == "retrieval":
            branch = record[task][0]
            documents = {item["id"] for item in branch["documents"]}
            if not (unique_ids(row["ranking"], "ranked documents") | unique_ids(row["accepted"], "accepted documents")) <= documents:
                raise ContractError("retrieval ranking/gold outside frozen corpus documents")
            if any(type(value) not in {int, float} or value not in branch["relevance_scale"] for value in row["relevance"].values()):
                raise ContractError("retrieval relevance grade outside frozen scale")
        by_baseline[key[0]].append(row)
    if seen != {(baseline, sample) for baseline in baselines for sample in samples}:
        raise ContractError("missing prediction units must be explicit outcome rows")
    result = {}
    for baseline, values in sorted(by_baseline.items()):
        completed = [row for row in values if row["status"] == "completed"]
        counts = {"total": len(values), "completed": len(completed), "failed": sum(row["status"] == "failed" for row in values),
                  "unknown": sum(row["status"] in {"unknown", "abstained"} for row in values)}
        metrics = {}
        coverage = {}
        if task == "forecasting":
            errors = []
            for row in completed:
                for name in ("origin", "target_time", "available_at"):
                    finite_number(row[name], name)
                if row["available_at"] > row["origin"] or row["target_time"] - row["origin"] != record[task][0]["horizon"]:
                    raise ContractError("prediction origin/availability/horizon leakage")
                errors.append(finite_number(abs(finite_number(row["prediction"]) - finite_number(row["target"])), "derived error"))
            metrics["mae"] = finite_number(sum(value / len(errors) for value in errors), "derived MAE") if errors else None
        elif task in {"rca", "retrieval"}:
            individual = [ranking_metrics(row["ranking"], row["accepted"], k=record[task][0]["k"], ties=row["ties"],
                          relevance=row["relevance"] if task == "retrieval" else None) for row in completed]
            for metric in METRICS[task]:
                scores = [value[metric] for value in individual if value[metric] is not None]
                undefined = len(individual) - len(scores)
                policy = next((item["denominator_policy"] for item in record["metrics"] if item["id"] == metric), "all-issued")
                denominator = counts["total"] if policy == "all-issued" else len(completed)
                metrics[metric] = sum(scores) / denominator if denominator and (scores or record["policies"]["no_relevant"] == "zero") else None
                if undefined and record["policies"]["no_relevant"] == "undefined-with-coverage":
                    metrics[metric] = None
                coverage[metric] = {"defined": len(scores), "undefined": undefined, "failed_or_unknown": counts["total"] - len(individual)}
        elif task == "anomaly":
            if any(type(row["target"]) is not bool for row in values):
                raise ContractError("anomaly denominator requires known binary oracle labels for every issued unit")
            for row in completed:
                if type(row["prediction"]) is not bool or type(row["target"]) is not bool:
                    raise ContractError("anomaly evaluation requires frozen binary labels/alerts")
                if row["delay"] is not None and finite_number(row["delay"], "detection delay") < 0:
                    raise ContractError("detection delay cannot be negative")
                if record[task][0]["label_unit"] != "point" and row["prediction"] and row["target"]:
                    origin = finite_number(row["origin"], "event start")
                    end = finite_number(row["target_time"], "event end")
                    alert = finite_number(row["available_at"], "alert time")
                    if (end < origin or alert < origin or alert > end + record[task][0]["tolerance"]
                            or row["delay"] != alert - origin):
                        raise ContractError("event detection delay/window differs from frozen tolerance")
            tp = sum(row["prediction"] and row["target"] for row in completed)
            fp = sum(row["prediction"] and not row["target"] for row in completed)
            positives = sum(row["target"] is True for row in values)
            delays = [row["delay"] for row in completed if row["prediction"] and row["target"] and row["delay"] is not None]
            metrics = {"precision": tp / (tp + fp) if tp + fp else None, "recall": tp / positives if positives else None,
                       "false-alert-rate": fp / record[task][0]["false_alert_exposure"], "mean-delay": sum(delays) / len(delays) if delays else None}
        else:
            if any(type(row["prediction"]) is not bool for row in completed):
                raise ContractError("agent task oracle outcome must be an actual boolean")
            policy = record["metrics"][0]["denominator_policy"]
            denominator = counts["total"] if policy == "all-issued" else len(completed)
            metrics["success-rate"] = sum(row["prediction"] for row in completed) / denominator if denominator else None
        selected = {}
        for metric in record["metrics"]:
            value = metrics[metric["id"]]
            if task == "forecasting" and metric["denominator_policy"] == "all-issued" and counts["completed"] != counts["total"]:
                value = None
            selected[metric["id"]] = value
            coverage.setdefault(metric["id"], {"defined": len(completed), "undefined": 0, "failed_or_unknown": counts["total"] - len(completed)})
            if value is not None:
                finite_number(value, "derived task metric")
        result[baseline] = {"counts": counts, "metrics": selected, "metric_coverage": {key: coverage[key] for key in selected}}
    return {"schema_version": 1, "task_id": record["task_id"], "task": task, "baselines": result}


def validate_aiops_evaluation(record, *, project=None, reader=None):
    validate_record("aiops-evaluation", record)
    _protocol_invariants(record)
    inputs = record["inputs"]
    if len(inputs) != 4 or {row["kind"] for row in inputs} != {"dataset", "split", "telemetry", "analysis"}:
        raise ContractError("evaluation requires exact dataset/split/telemetry/analysis bindings")
    if record["stage"] == "protocol":
        if record["predictions"] or record["results"] or record["runs"] or record["failures"]:
            raise ContractError("protocol cannot claim actual predictions/results/runs")
        return {"contract": "pass", "stage": "protocol", "scientific_acceptance": "pending"}
    if not project and reader is None or len(record["predictions"]) != 1 or len(record["results"]) != 1 or not record["runs"]:
        raise ContractError("readout requires actual project/predictions/results/run bindings")
    if record["benchmark"]["rights"] == "metadata-only" or record["gold"]["access"] != "evaluation-only":
        raise ContractError("readout requires selected input rights and evaluation-only oracle access")
    reader = reader or ArtifactReader(project)
    bound = {row["kind"]: reader.bound_json(row["reference"]) for row in inputs}
    if any(value.get("task_id") != record["task_id"] for value in bound.values()):
        raise ContractError("evaluation input task identities disagree")
    dataset = validate_dataset_manifest(bound["dataset"], project=project, reader=reader)
    validate_split_manifest(bound["split"], project=project, reader=reader)
    validate_telemetry_manifest(bound["telemetry"], project=project, reader=reader)
    validate_statistical_analysis(bound["analysis"], project=project, reader=reader)
    references = {row["kind"]: row["reference"] for row in inputs}
    if bound["split"]["dataset"] != references["dataset"]:
        raise ContractError("evaluation dataset differs from split parent")
    sample_index = {row["sample_id"]: row for row in dataset["samples"]}
    partition = record["evaluation_partition"]
    selected = set(sample_index) if partition == "development-all" else set(reader.rows(next(row["membership"] for row in bound["split"]["partitions"] if row["name"] == partition)))
    if set(record["sample_ids"]) != selected:
        raise ContractError("evaluation sample membership differs from actual selected partition")
    for ref in record["gold"]["references"]:
        reader.binding(ref)
    run_outputs = set()
    for ref in record["runs"]:
        run = reader.bound_json(ref)
        outputs = receipt_outputs(run, record["task_id"], [row["reference"] for row in inputs])
        if run["status"] == "completed-unreviewed":
            run_outputs |= outputs
    if not {(kind, ref["path"], ref["sha256"]) for kind, refs in (("predictions", record["predictions"]), ("metrics", record["results"])) for ref in refs} <= run_outputs:
        raise ContractError("evaluation predictions/metrics must bind actual completed run outputs")
    if record["task"] == "retrieval":
        branch = record["retrieval"][0]
        if record["gold"]["references"] != [branch["qrels"]]:
            raise ContractError("retrieval oracle must bind the exact qrels snapshot")
        for ref in [branch["corpus"], branch["qrels"]] + branch["generation_support"]:
            reader.binding(ref)
    rows = reader.rows(record["predictions"][0])
    if record["task"] == "forecasting":
        targets = {row["sample_id"]: row[record["forecasting"][0]["value_field"]] for row in reader.rows(bound["dataset"]["normalized"][0])}
        if any(row["target"] != targets.get(row["sample_id"]) for row in rows):
            raise ContractError("forecast target differs from actual observed dataset")
        if any(row["target_time"] != sample_index[row["sample_id"]]["time_start"] for row in rows):
            raise ContractError("forecast target time differs from actual sample index")
    else:
        if len(record["gold"]["references"]) != 1:
            raise ContractError("task readout requires one canonical actual oracle row binding")
        oracle_rows = reader.rows(record["gold"]["references"][0])
        oracle = {}
        for row in oracle_rows:
            if not isinstance(row, dict) or set(row) != {"sample_id", "target", "accepted", "relevance", "origin", "target_time"}:
                raise ContractError("canonical oracle fields differ from task contract")
            if row["sample_id"] in oracle:
                raise ContractError("duplicate oracle unit")
            oracle[row["sample_id"]] = row
        if set(oracle) != selected:
            raise ContractError("oracle membership differs from frozen partition")
        for row in rows:
            gold = oracle[row["sample_id"]]
            if any(row[name] != gold[name] for name in gold if name != "sample_id"):
                raise ContractError("prediction gold/target fields differ from bound oracle")
            if record["task"] == "agent" and row["status"] == "completed" and row["prediction"] != gold["target"]:
                raise ContractError("agent success differs from actual task oracle")
    expected = evaluate_predictions(record, rows)
    if reader.bound_json(record["results"][0]) != expected:
        raise ContractError("bound metrics/denominators differ from actual prediction oracle")
    failed = {row["sample_id"] for row in rows if row["status"] == "failed"}
    if failed != {row["sample_id"] for row in record["failures"]}:
        raise ContractError("failed prediction reasons must preserve actual failed membership")
    return {"contract": "pass", "stage": "readout", "units": len(record["sample_ids"]), "scientific_acceptance": "pending"}
