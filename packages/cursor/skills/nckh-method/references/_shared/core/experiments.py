"""Read-only experiment graphs, drift checks and preserved process observations."""
from datetime import datetime

from core.aiops import validate_aiops_evaluation
from core.datasets import validate_dataset_manifest, validate_split_manifest
from core.paths import contained
from core.research_io import ArtifactReader, ResearchLimits, finite_number, unique_ids
from core.schema import ContractError, validate, validate_record
from core.statistics import validate_statistical_analysis
from core.telemetry import validate_telemetry_manifest

PARENTS = {"dataset", "split", "telemetry", "analysis", "evaluation"}
TERMINAL = {"completed-unreviewed", "failed", "cancelled"}
REF_SCHEMA = {"type": "object", "additionalProperties": False, "properties": {"path": {"type": "string", "minLength": 1},
    "sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"}}, "required": ["path", "sha256"]}

def date(value):
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if result.tzinfo is None:
            raise ValueError("timezone absent")
        return result
    except (AttributeError, ValueError) as error:
        raise ContractError("experiment chronology requires timezone-aware timestamps") from error

def manifest_bindings(record):
    return [record["protocol"], record["environment"], *[row["reference"] for row in record["inputs"]],
            *record["code"], *record["config"], *record["artifacts"], *record["simulation"]["parameters"]]

def validate_run_receipt(record, manifest, manifest_reference, *, project, reader=None):
    validate_record("research-run-receipt", record)
    reader = reader or ArtifactReader(project)
    if record["task_id"] != manifest["task_id"] or record["manifest"] != manifest_reference or record["environment"] != manifest["environment"]:
        raise ContractError("run identity/manifest/environment differs from frozen experiment")
    input_paths = unique_ids([ref["path"] for ref in record["inputs"]], "run input paths")
    expected = {ref["path"]: ref["sha256"] for ref in manifest_bindings(manifest)}
    if input_paths != set(expected) or any(ref["sha256"] != expected[ref["path"]] for ref in record["inputs"]):
        raise ContractError("run must bind every exact frozen input, code, config and environment")
    for ref in [manifest_reference, *record["inputs"]]:
        reader.binding(ref)
    if record["output_semantics"] != manifest["output_semantics"]:
        raise ContractError("simulation/computation labels differ from frozen protocol")
    started = date(record["started_at"]) if record["started_at"] is not None else None
    ended = date(record["ended_at"]) if record["ended_at"] is not None else None
    process = record["process"]
    status = record["status"]
    if started and started < date(manifest["frozen_at"]):
        raise ContractError("run predates frozen protocol")
    if ended and (started is None or ended < started):
        raise ContractError("run end precedes actual start")
    if status == "scheduled":
        if started or ended or record["exit_code"] is not None or process["pid"] is not None or record["outputs"] or record["stdout"] is not None or record["stderr"] is not None or process["cleanup"] != "not-started":
            raise ContractError("scheduled receipt cannot invent process/output observations")
        if any(value is not None for name, value in record["resources"].items() if name != "coverage"):
            raise ContractError("scheduled receipt cannot invent resource measurements")
    else:
        if (not started or type(process["pid"]) is not int or process["pid"] <= 0 or type(process["parent_pid"]) is not int
                or process["parent_pid"] <= 0 or date(process["identity_started_at"]) != started or not record["argv"]):
            raise ContractError("observed run requires exact process/start/argv identity")
        if status == "running":
            if ended or record["exit_code"] is not None or process["cleanup"] != "running" or record["reconciliation"]["status"] != "pending":
                raise ContractError("running process cannot claim terminal cleanup")
        else:
            if (not ended or type(record["exit_code"]) is not int or process["cleanup"] != "exited"
                    or not process["evidence"] or record["reconciliation"]["status"] != "reaped"):
                raise ContractError("terminal run requires observed exit and reconciled process cleanup")
            if record["stdout"] is None or record["stderr"] is None:
                raise ContractError("terminal run must retain actual stdout/stderr bytes")
            if status == "completed-unreviewed" and (record["exit_code"] != 0 or record["failure_reason"]):
                raise ContractError("completed-unreviewed requires zero exit and no concealed failure")
            if status in {"failed", "cancelled"} and not record["failure_reason"]:
                raise ContractError("failed/cancelled attempt requires a retained reason")
    reconciled = date(record["reconciliation"]["observed_at"])
    if ended and reconciled < ended:
        raise ContractError("cleanup observation predates terminal process")
    for ref in (record["stdout"], record["stderr"]):
        if ref is not None:
            validate(ref, REF_SCHEMA)
            reader.binding(ref)
    for name, value in record["resources"].items():
        if name != "coverage" and value is not None and finite_number(value, name) < 0:
            raise ContractError("resource measurements cannot be negative")
    if record["resources"]["provider_cost"] is not None:
        raise ContractError("offline run does not observe provider costs; leave unknown")
    if started and ended and record["resources"]["wall_seconds"] is not None:
        if abs((ended - started).total_seconds() - record["resources"]["wall_seconds"]) > 1:
            raise ContractError("wall duration differs from observed chronology")
    outputs = unique_ids([row["reference"]["path"] for row in record["outputs"]], "actual output paths")
    allowed = {row["path"]: row["kind"] for row in manifest["expected_outputs"] if row.get("attempt_id", record["attempt_id"]) == record["attempt_id"]}
    if not allowed:
        raise ContractError("run attempt has no frozen expected output route")
    if not outputs <= allowed.keys() or status == "completed-unreviewed" and outputs != allowed.keys():
        raise ContractError("actual outputs differ from complete frozen expected artifact paths")
    for row in record["outputs"]:
        ref = row["reference"]
        if row["kind"] != allowed[ref["path"]] or ref["path"] in input_paths:
            raise ContractError("output kind/input alias differs from frozen graph")
        data = reader.bound_json(ref) if row["kind"] != "readout" else reader.binding(ref)
        actual_count = len(data) if row["kind"] == "predictions" and isinstance(data, list) else 1
        if row["count"] != actual_count:
            raise ContractError("run output count differs from actual artifact cardinality")
    return {"contract": "pass", "status": status, "scientific_acceptance": "pending"}

def validate_experiment_manifest(record, *, project, reader=None):
    validate_record("experiment-manifest", record)
    reader = reader or ArtifactReader(project)
    frozen_at = date(record["frozen_at"])
    if len(record["inputs"]) != 5 or {row["kind"] for row in record["inputs"]} != PARENTS:
        raise ContractError("experiment requires five exact scientific parent bindings")
    refs = manifest_bindings(record)
    unique_ids([ref["path"] for ref in refs], "frozen artifact paths")
    if not record["code"] or not record["config"] or not record["baselines"] or not record["metrics"] or not record["oracles"] or not record["grants"]:
        raise ContractError("experiment requires actual code/config/design/oracle/grant declarations")
    for name in ("baselines", "metrics", "oracles", "grants"):
        unique_ids(record[name], "experiment " + name)
    limits = reader.limits
    if any(record["limits"][name] > getattr(limits, name) for name in ("file_bytes", "aggregate_bytes", "records", "output_bytes")):
        raise ContractError("artifact cannot raise controller-trusted limits")
    reader.limits = ResearchLimits(**{name: min(getattr(limits, name), record["limits"][name]) for name in ("file_bytes", "aggregate_bytes", "records", "output_bytes")})
    if reader.bytes_read > reader.limits.aggregate_bytes or reader.records_read > reader.limits.records:
        raise ContractError("manifest already exceeds its lowered resource budget")
    paths = unique_ids([row["path"] for row in record["expected_outputs"]], "expected output paths")
    if not paths or paths & {ref["path"] for ref in refs}:
        raise ContractError("outputs cannot alias frozen inputs")
    scoped = ["attempt_id" in row for row in record["expected_outputs"]]
    if any(scoped) and not all(scoped):
        raise ContractError("expected outputs cannot mix shared and attempt-scoped routes")
    routes = {row.get("attempt_id") for row in record["expected_outputs"]}
    if len(routes) > record["limits"]["attempts"]:
        raise ContractError("expected output routes exceed frozen attempt limit")
    for attempt in routes:
        for kind in ("predictions", "metrics"):
            if sum(row["kind"] == kind and row.get("attempt_id") == attempt for row in record["expected_outputs"]) != 1:
                raise ContractError("each evaluation attempt requires exactly one predictions and metrics output")
    for path in paths:
        contained(project, path)
    for ref in refs:
        reader.binding(ref)
    parents = {row["kind"]: reader.bound_json(row["reference"]) for row in record["inputs"]}
    declared = {ref["path"]: ref["sha256"] for ref in refs}
    def check_nested(value):
        if isinstance(value, dict):
            if set(value) == {"path", "sha256"} and declared.get(value["path"]) != value["sha256"]:
                raise ContractError("frozen graph omits a scientific parent's transitive artifact binding")
            for item in value.values():
                check_nested(item)
        elif isinstance(value, list):
            for item in value:
                check_nested(item)
    check_nested(parents)
    rights_paths = {source["rights_reference"] for source in parents["dataset"]["sources"]} | {parents["evaluation"]["benchmark"]["rights_reference"]}
    if not rights_paths <= declared.keys():
        raise ContractError("frozen graph omits actual selected rights bytes")
    if any(value.get("task_id") != record["task_id"] for value in parents.values()):
        raise ContractError("scientific parent task identities disagree")
    validate_dataset_manifest(parents["dataset"], project=project, reader=reader)
    validate_split_manifest(parents["split"], project=project, reader=reader)
    validate_telemetry_manifest(parents["telemetry"], project=project, reader=reader)
    validate_statistical_analysis(parents["analysis"], project=project, reader=reader)
    validate_aiops_evaluation(parents["evaluation"], project=project, reader=reader)
    parent_refs = {row["kind"]: row["reference"] for row in record["inputs"]}
    if parents["split"]["dataset"] != parent_refs["dataset"] or {row["kind"]: row["reference"] for row in parents["evaluation"]["inputs"]} != {name: parent_refs[name] for name in PARENTS - {"evaluation"}}:
        raise ContractError("scientific graph parent lineage differs from experiment bindings")
    if set(record["baselines"]) != {row["id"] for row in parents["evaluation"]["baselines"]} or set(record["metrics"]) != {row["id"] for row in parents["evaluation"]["metrics"]}:
        raise ContractError("experiment baselines/metrics differ from frozen evaluation")
    simulation = record["simulation"]
    if record["output_semantics"] == "simulation":
        if (simulation["applicability"] != "simulation" or simulation["label"] != "simulation/not observed measurements"
                or type(simulation["seed"]) is not int or simulation["replications"] <= 0
                or any(not simulation[name] for name in ("generator", "parameters", "warmup", "conservation", "uncertainty", "validity_limits"))):
            raise ContractError("simulation requires actual generator/seed/parameters/replications and validity limits")
        for ref in simulation["parameters"]:
            reader.binding(ref)
    elif simulation["applicability"] != "not-used" or simulation["seed"] is not None or simulation["replications"] or simulation["parameters"]:
        raise ContractError("observed-input computation cannot invent simulation parameters")
    previous = frozen_at
    for amendment in record["amendments"]:
        at = date(amendment["at"])
        if at < previous:
            raise ContractError("amendments cannot rewrite chronology")
        reader.binding(amendment["previous_manifest"])
        previous = at
    if record["stage"] == "plan":
        if record["freeze"] is not None or record["receipts"] or record["outputs"]:
            raise ContractError("planned graph cannot invent actual runs or outputs")
        return {"contract": "pass", "stage": "plan", "execution": "not-run", "scientific_acceptance": "pending"}
    validate(record["freeze"], REF_SCHEMA)
    frozen = reader.bound_json(record["freeze"])
    if frozen.get("stage") != "plan" or any(record[key] != frozen.get(key) for key in record if key not in {"stage", "freeze", "receipts", "outputs"}):
        raise ContractError("readout changed frozen graph without a new protocol amendment")
    if not record["receipts"] or len(record["receipts"]) > record["limits"]["attempts"]:
        raise ContractError("readout requires bounded actual attempt receipts")
    runs = [reader.bound_json(ref) for ref in record["receipts"]]
    unique_ids([row["run_id"] for row in runs], "run IDs")
    unique_ids([row["attempt_id"] for row in runs], "attempt IDs")
    unique_ids([ref["path"] for ref in record["receipts"]], "receipt paths")
    for row, receipt_ref in zip(runs, record["receipts"]):
        validate_run_receipt(row, frozen, record["freeze"], project=project, reader=reader)
        if row["status"] not in TERMINAL:
            raise ContractError("readout cannot promote scheduled/running attempts")
        if row["status"] == "completed-unreviewed":
            outputs = {item["kind"]: item["reference"] for item in row["outputs"]}
            evaluation = {**parents["evaluation"], "stage": "readout", "predictions": [outputs["predictions"]],
                          "results": [outputs["metrics"]], "runs": [receipt_ref]}
            validate_aiops_evaluation(evaluation, project=project, reader=reader)
    output_refs = {ref["path"]: ref for ref in record["outputs"]}
    if len(output_refs) != len(record["outputs"]):
        raise ContractError("duplicate readout output bindings")
    observed = {}
    for run in runs:
        for row in run["outputs"]:
            ref = row["reference"]
            if ref["path"] in observed and observed[ref["path"]] != ref:
                raise ContractError("attempt outputs conflict; preserve each attempt at distinct paths")
            observed[ref["path"]] = ref
    if output_refs != observed:
        raise ContractError("readout must retain exact outputs of every actual attempt")
    return {"contract": "pass", "stage": "readout", "attempts": len(runs), "execution": "completed-unreviewed" if all(row["status"] == "completed-unreviewed" for row in runs) else "preserved-failures", "scientific_acceptance": "pending"}
