"""Statistical plan/readout invariants, without choosing a universal estimator."""

from datetime import datetime

from core.paths import digest_record
from core.datasets import validate_dataset_manifest, validate_split_manifest
from core.research_io import ArtifactReader, finite_number, receipt_outputs, unique_ids
from core.schema import ContractError, validate_record


IID_METHODS = {"iid-bootstrap", "iid-standard-error", "iid-t-interval"}


def _date(value):
    try:
        date = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if date.tzinfo is None:
            raise ValueError("timezone missing")
        return date
    except (ValueError, AttributeError) as error:
        raise ContractError("statistical chronology requires a timezone-aware date") from error


def validate_statistical_analysis(record, *, project=None, reader=None):
    validate_record("statistical-analysis", record)
    unit = record["unit"]
    observations = unique_ids(unit["observation_ids"], "observation units")
    independent = unique_ids(unit["independent_ids"], "independent units")
    if unit["independent_n"] != len(independent):
        raise ContractError("independent n must equal actual independent-unit membership")
    nesting = unit["nesting"]
    if (len(nesting) != len(observations) or {row["observation_id"] for row in nesting} != observations
            or any(row["independent_id"] not in independent for row in nesting)):
        raise ContractError("every observation requires one actual independent-unit mapping")
    if observations and {row["independent_id"] for row in nesting} != independent:
        raise ContractError("declared independent units have no observations")
    counts = record["denominators"]
    if counts["total"] != len(observations) or counts["completed"] + counts["failed"] + counts["missing"] != counts["total"]:
        raise ContractError("completed/failed/missing denominators must reconcile actual units")
    uncertainty = record["uncertainty"]
    dependence = record["design"]["dependence"]
    if uncertainty["method"] in IID_METHODS and (dependence != "independent" or not unit["independence_evidence"]):
        raise ContractError("IID uncertainty cannot ignore cluster/time dependence")
    if uncertainty["unit"] != unit["kind"]:
        raise ContractError("uncertainty must use the declared independent unit")
    if uncertainty["status"] == "not-applicable" and not uncertainty["reason"]:
        raise ContractError("not-applicable uncertainty requires a reason")
    if uncertainty["method"] in {"bootstrap", "iid-bootstrap", "cluster-bootstrap", "block-bootstrap", "monte-carlo"} and uncertainty["replications"] <= 0:
        raise ContractError("resampling/simulation requires an actual replication count")
    assumptions = record["assumptions"]
    ids = unique_ids([row["id"] for row in assumptions], "assumptions")
    required = unique_ids(record["estimator"]["required_assumptions"], "required estimator assumptions")
    if not required <= ids:
        raise ContractError("estimator assumptions missing from analysis plan")
    for row in assumptions:
        if row["status"] in {"assessed", "not-applicable"} and not row["evidence_or_reason"]:
            raise ContractError("assumption status requires actual evidence or applicability reason")
    comparison = record["comparison"]
    left = unique_ids(comparison["baseline_units"], "baseline comparison units")
    right = unique_ids(comparison["candidate_units"], "candidate comparison units")
    if comparison["mode"] == "paired" and (not left or left != right):
        raise ContractError("paired comparisons require exactly matching independent units")
    if comparison["mode"] == "none" and (left or right or not comparison["reason"]):
        raise ContractError("no comparison requires an applicability reason and no paired memberships")
    if not (left | right) <= independent:
        raise ContractError("comparison contains units outside the declared analysis population")
    multiplicity = record["multiplicity"]
    unique_ids(multiplicity["family"], "comparison family")
    if not multiplicity["policy"] or not multiplicity["rationale"]:
        raise ContractError("multiplicity requires a frozen policy and rationale")
    frozen = _date(record["stopping"]["frozen_at"])
    previous = frozen
    for amendment in record["stopping"]["amendments"]:
        current = _date(amendment["at"])
        if current < previous or not amendment["reason"]:
            raise ContractError("stopping amendments must preserve chronology and reason")
        previous = current
    if record["seed"]["status"] == "not-applicable":
        if record["seed"]["value"] is not None or not record["seed"]["reason"]:
            raise ContractError("deterministic seed must be not-applicable with a reason")
    elif type(record["seed"]["value"]) is not int:
        raise ContractError("stochastic analyses require the actual integer seed")
    result = record["result"]
    for name in ("estimate", "standard_error", "interval_lower", "interval_upper"):
        if result[name] is not None:
            finite_number(result[name], name)
    if result["standard_error"] is not None and result["standard_error"] < 0:
        raise ContractError("standard error cannot be negative")
    bounds = (result["interval_lower"], result["interval_upper"])
    if (bounds[0] is None) != (bounds[1] is None) or bounds[0] is not None and bounds[0] > bounds[1]:
        raise ContractError("uncertainty interval bounds are incomplete or reversed")
    if record["stage"] == "plan":
        if (result["status"] != "planned" or uncertainty["status"] == "computed"
                or any(result[name] is not None for name in result if name != "status") or record["runs"] or record["outputs"]):
            raise ContractError("analysis plans cannot contain observed results or invented run receipts")
    else:
        if len(record["inputs"]) != 2 or {row["kind"] for row in record["inputs"]} != {"dataset", "split"}:
            raise ContractError("readout requires both dataset and split bindings")
        if not record["runs"] or not record["outputs"] or not project and reader is None:
            raise ContractError("readout requires actual project/run/output bindings")
        reader = reader or ArtifactReader(project)
        reader.binding(record["protocol"])
        parents = {row["kind"]: reader.bound_json(row["reference"]) for row in record["inputs"]}
        if any(parent.get("task_id") != record["task_id"] for parent in parents.values()):
            raise ContractError("statistical readout task differs from dataset/split task")
        dataset = validate_dataset_manifest(parents["dataset"], project=project, reader=reader)
        validate_split_manifest(parents["split"], project=project, reader=reader)
        dataset_ref = next(row["reference"] for row in record["inputs"] if row["kind"] == "dataset")
        if parents["split"]["dataset"] != dataset_ref:
            raise ContractError("analysis dataset differs from split parent")
        samples = {row["sample_id"]: row for row in dataset["samples"]}
        if not observations <= samples.keys() or any(samples[row["observation_id"]][unit["mapping_field"]] != row["independent_id"] for row in nesting):
            raise ContractError("analysis observations/independent mapping differ from actual dataset")
        run_outputs = set()
        for row in record["runs"]:
            run = reader.bound_json(row)
            outputs = receipt_outputs(run, record["task_id"], [item["reference"] for item in record["inputs"]])
            if run["status"] == "completed-unreviewed" or result["status"] == "failed":
                run_outputs |= outputs
        expected = {"schema_version": 1, "task_id": record["task_id"], "result": result, "denominators": counts}
        matched = False
        for row in record["outputs"]:
            output = reader.bound_json(row)
            if ("statistics", row["path"], row["sha256"]) not in run_outputs:
                raise ContractError("statistical readout must bind actual run output")
            matched = matched or digest_record(output) == digest_record(expected)
        if not matched:
            raise ContractError("readout estimate and denominators must match a bound actual statistical output")
        if counts["failed"] and not record["failures"]:
            raise ContractError("failed observations require preserved failure reasons")
        if result["status"] == "computed" and (result["estimate"] is None or counts["completed"] == 0):
            raise ContractError("computed readout requires actual estimate and completed observations")
        if result["status"] == "failed" and not record["failures"]:
            raise ContractError("failed calculation requires a preserved failure reason")
        if result["status"] not in {"computed", "failed"}:
            raise ContractError("readout requires computed or preserved failed result")
        if uncertainty["status"] == "computed":
            if any(row["status"] != "assessed" for row in assumptions if row["id"] in required):
                raise ContractError("inferential readout cannot promote pending/violated estimator assumptions")
            if bounds[0] is None and result["standard_error"] is None:
                raise ContractError("computed uncertainty requires an actual interval or standard error")
        if record["design"]["claim_type"] == "causal" and not record["design"]["identification_evidence"]:
            raise ContractError("causal readout requires design/identification evidence")
    return {"stage": record["stage"], "independent_n": len(independent),
            "contract": "pass", "scientific_acceptance": "pending"}


def paired_difference_summary(baseline, candidate):
    """Descriptive candidate-minus-baseline summary, not an inferential interval."""
    if not baseline or set(baseline) != set(candidate):
        raise ContractError("paired measurements need exactly matching nonempty unit keys")
    differences = {key: finite_number(candidate[key], "candidate") - finite_number(baseline[key], "baseline")
                   for key in sorted(baseline)}
    for value in differences.values():
        finite_number(value, "derived paired difference")
    mean = finite_number(sum(value / len(differences) for value in differences.values()), "derived paired mean")
    return {"n": len(differences), "differences": differences,
            "mean_difference": mean,
            "uncertainty": "not-computed", "scope": "descriptive paired measurements"}
