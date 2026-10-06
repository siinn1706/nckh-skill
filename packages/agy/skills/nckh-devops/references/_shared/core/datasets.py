"""Scientific intake lineage and actual-membership split invariants."""

from datetime import datetime
import csv
import io

from core.research_io import ArtifactReader, finite_number, unique_ids
from core.schema import ContractError, validate_record


def validate_dataset_manifest(record, *, project=None, reader=None):
    validate_record("dataset-manifest", record)
    unique_ids([row["id"] for row in record["sources"]], "dataset sources")
    unique_ids([row["name"] for row in record["fields"]], "dataset fields")
    unique_ids(record["modalities"], "dataset modalities")
    counts = record["counts"]
    if counts["retained"] + counts["excluded"] + counts["quarantined"] != counts["raw"]:
        raise ContractError("raw/retained/excluded/quarantine counts do not reconcile")
    if len(record["quarantine"]) != counts["quarantined"]:
        raise ContractError("quarantine requires preserved original locator/hash/reason for each row")
    labels = record["labels"]
    if labels["feature_fields"]:
        raise ContractError("gold labels must not enter scientific feature fields")
    if labels["access"] == "none" and (labels["references"] or not labels["reason"]):
        raise ContractError("label absence requires an actual scope reason")
    if labels["access"] == "protected-evaluation-only" and (not labels["provenance"] or not labels["references"]):
        raise ContractError("protected labels require actual source/access references")
    if record["release"]["status"] == "redistributable" and any(source["rights"] != "redistributable" for source in record["sources"]):
        raise ContractError("unresolved/local-only rights cannot authorize dataset redistribution")
    for field in record["fields"]:
        if not field["unit"] and not field["unknown_reason"]:
            raise ContractError("blank/unknown units require a reason; units are not inferred")
    if record["stage"] == "metadata":
        if record["raw"] or record["raw_layout"] or record["normalized"] or record["sample_index"] or record["transforms"]:
            raise ContractError("metadata-only intake cannot claim acquired or transformed artifacts")
        return {"stage": "metadata", "data_acceptance": "pending", "samples": []}
    if not project and reader is None:
        raise ContractError("curated dataset requires an actual contained project")
    if (not record["sources"] or any(source["rights"] == "pending" or source["access"] == "metadata-only"
                                     or not source["rights_reference"] for source in record["sources"])):
        raise ContractError("curation requires cleared selected-source access and rights")
    if not record["raw"] or len(record["normalized"]) != 1 or len(record["sample_index"]) != 1 or not record["transforms"]:
        raise ContractError("curation requires raw, normalized, actual sample index and transformation lineage")
    reader = reader or ArtifactReader(project)
    layouts = {row["path"]: row for row in record["raw_layout"]}
    if len(layouts) != len(record["raw_layout"]) or set(layouts) != {row["path"] for row in record["raw"]}:
        raise ContractError("raw layout must cover exact acquired paths")
    raw_counts = {}
    for reference in record["raw"]:
        layout = layouts[reference["path"]]
        if layout["format"] == "canonical-json-array":
            count = len(reader.rows(reference))
        elif layout["format"] == "worldbank-api-v2":
            data = reader.bound_json(reference)
            if not isinstance(data, list) or len(data) != 2 or not isinstance(data[1], list):
                raise ContractError("invalid World Bank API v2 layout")
            count = len(data[1])
            reader.count(count)
        else:
            data = reader.binding(reference).decode("utf-8-sig")
            count = 0
            if layout["format"] == "csv":
                source = csv.reader(io.StringIO(data))
                header = next(source, None)
                if not header or len(set(header)) != len(header):
                    raise ContractError("CSV needs unique actual header fields")
                for row in source:
                    reader.count(1)
                    if len(row) != len(header):
                        raise ContractError("raw CSV row width conflicts with header")
                    count += 1
            else:
                for line in io.StringIO(data):
                    if not line.strip():
                        raise ContractError("raw JSONL cannot contain ambiguous blank rows")
                    reader.count(1)
                    reader.parse(line)
                    count += 1
        if count != layout["rows"]:
            raise ContractError("declared raw count differs from actual acquired rows")
        raw_counts[reference["sha256"]] = count
    if sum(raw_counts.values()) != counts["raw"]:
        raise ContractError("actual total raw row count differs from manifest")
    rows = reader.rows(record["normalized"][0])
    samples = reader.rows(record["sample_index"][0])
    fields = {field["name"]: field for field in record["fields"]}
    types = {"string": str, "integer": int, "number": (int, float), "boolean": bool}
    missing = dict.fromkeys(fields, 0)
    zeros = dict.fromkeys(fields, 0)
    for row in rows:
        if not isinstance(row, dict) or set(row) != set(fields):
            raise ContractError("normalized fields do not match the frozen field schema")
        for name, field in fields.items():
            value = row[name]
            if any(type(value) is type(token) and value == token for token in field["missing_tokens"]):
                missing[name] += 1
                continue
            expected = types[field["type"]]
            if not isinstance(value, expected) or field["type"] in {"number", "integer"} and type(value) is bool:
                raise ContractError("normalized value violates frozen type/missingness policy")
            if field["type"] in {"number", "integer"}:
                finite_number(value, name)
                zeros[name] += value == 0
    if "sample_id" not in fields:
        raise ContractError("normalized dataset needs canonical sample_id")
    ids = unique_ids([row["sample_id"] for row in rows], "normalized samples")
    protected = {ref["sha256"] for ref in labels["references"]}
    public_inputs = {ref["sha256"] for ref in record["raw"] + record["normalized"] + record["sample_index"]}
    if protected & public_inputs:
        raise ContractError("protected gold cannot alias feature/data artifacts")
    for reference in labels["references"]:
        reader.binding(reference)
    expected_sample_fields = {"sample_id", "entity_id", "incident_id", "group_id", "time_start", "time_end"}
    for row in samples:
        if not isinstance(row, dict) or set(row) != expected_sample_fields:
            raise ContractError("canonical sample index requires exact identity/interval fields")
        for name in ("entity_id", "incident_id", "group_id"):
            if not isinstance(row[name], str):
                raise ContractError("sample index identity must be a string, blank when unknown")
        for name in ("time_start", "time_end"):
            if row[name] is not None:
                finite_number(row[name], name)
        if (row["time_start"] is None) != (row["time_end"] is None) or row["time_start"] is not None and row["time_start"] > row["time_end"]:
            raise ContractError("sample time interval is incomplete or reversed")
    if unique_ids([row["sample_id"] for row in samples], "sample index") != ids or len(rows) != counts["retained"]:
        raise ContractError("actual normalized/sample membership/count differs from manifest")
    reports = {row["field"]: row for row in record["missingness"]}
    if len(reports) != len(record["missingness"]) or set(reports) != set(fields):
        raise ContractError("missingness report requires exact field membership")
    if any(reports[name]["missing"] != missing[name] or reports[name]["zero"] != zeros[name] for name in fields):
        raise ContractError("actual missing and zero counts must remain distinct and reconcile")
    available = raw_counts
    for transform in record["transforms"]:
        reader.binding(transform["code"])
        reader.binding(transform["config"])
        if not transform["inputs"] or not transform["outputs"]:
            raise ContractError("transform requires actual input/output bindings")
        for reference in transform["inputs"] + transform["outputs"]:
            reader.binding(reference)
        if any(len(reader.rows(reference)) != transform["output_rows"] for reference in transform["outputs"]):
            raise ContractError("actual intermediate/output row count differs from transformation lineage")
        if (any(ref["sha256"] not in available for ref in transform["inputs"])
                or sum(available[ref["sha256"]] for ref in transform["inputs"]) != transform["input_rows"]
                or transform["output_rows"] + transform["excluded_rows"] + transform["quarantined_rows"] != transform["input_rows"]):
            raise ContractError("transform input/output/count lineage differs from actual bound artifacts")
        for reference in transform["outputs"]:
            available[reference["sha256"]] = transform["output_rows"]
    if any(available.get(ref["sha256"]) != counts["retained"] for ref in record["normalized"]):
        raise ContractError("normalized result lacks reviewed transformation lineage")
    return {"stage": "curated", "contract": "pass", "samples": samples, "data_acceptance": "pending"}


def validate_split_manifest(record, *, project=None, reader=None):
    validate_record("split-manifest", record)
    reader = reader or ArtifactReader(project)
    parent = reader.bound_json(record["dataset"])
    if parent.get("task_id") != record["task_id"]:
        raise ContractError("split task differs from dataset task")
    validated = validate_dataset_manifest(parent, project=project, reader=reader)
    samples = {row["sample_id"]: row for row in validated["samples"]}
    if not samples:
        raise ContractError("split requires actual nonempty curated sample membership")
    axes = unique_ids(record["independence_axes"], "independence axes")
    if "sample" not in axes:
        raise ContractError("all scientific partitions require sample disjointness")
    partitions = record["partitions"]
    if len(partitions) != 3 or {row["name"] for row in partitions} != {"train", "validation", "test"}:
        raise ContractError("exact train/validation/test partitions are required")
    seen = set()
    groups = {}
    intervals = {}
    for partition in partitions:
        membership = reader.rows(partition["membership"])
        ids = unique_ids(membership, "actual split membership")
        if not ids or len(ids) != partition["count"] or not ids <= samples.keys() or seen & ids:
            raise ContractError("actual split membership overlaps, is missing, empty or has wrong counts")
        seen |= ids
        for axis in axes - {"sample", "time"}:
            key = axis + "_id"
            values = {samples[sample][key] for sample in ids}
            if not all(values) or groups.get(axis, set()) & values:
                raise ContractError(f"actual {axis} identity overlaps or is unknown across partitions")
            groups.setdefault(axis, set()).update(values)
        times = [(samples[sample]["time_start"], samples[sample]["time_end"]) for sample in ids]
        if "time" in axes or record["temporal"]["required"]:
            if any(start is None or end is None for start, end in times):
                raise ContractError("chronological split cannot invent unknown time intervals")
            intervals[partition["name"]] = (min(start for start, _ in times), max(end for _, end in times))
    excluded = unique_ids([row["sample_id"] for row in record["exclusions"]], "split exclusions")
    if excluded & seen or seen | excluded != samples.keys():
        raise ContractError("all actual samples require exactly one partition or reasoned exclusion")
    embargo = finite_number(record["temporal"]["embargo"], "embargo")
    if embargo < 0:
        raise ContractError("temporal embargo cannot be negative")
    if intervals:
        for left, right in (("train", "validation"), ("validation", "test")):
            if intervals[left][1] + embargo >= intervals[right][0]:
                raise ContractError("actual partition intervals overlap or violate chronological embargo")
    for feature in record["features"]:
        if feature["sample_id"] not in samples or feature["kind"] == "gold-label":
            raise ContractError("feature membership is unknown or gold-label leakage")
        if feature["available_at"] > feature["decision_at"]:
            raise ContractError("feature was unavailable at the frozen task decision time")
        if feature["task"] == "forecasting" and (samples[feature["sample_id"]]["time_start"] is None
                or feature["decision_at"] >= samples[feature["sample_id"]]["time_start"]):
            raise ContractError("forecast origin must precede actual target interval")
        if feature["task"] == "rca" and feature["decision_at"] > feature["diagnostic_window_end"]:
            raise ContractError("RCA diagnostic observations exceed the frozen diagnostic window")
    try:
        previous = datetime.fromisoformat(record["frozen_at"].replace("Z", "+00:00"))
        if previous.tzinfo is None:
            raise ValueError("timezone missing")
        for amendment in record["amendments"]:
            at = datetime.fromisoformat(amendment["at"].replace("Z", "+00:00"))
            if at < previous or not amendment["invalidated"]:
                raise ValueError("amendment lacks chronology/invalidation")
            previous = at
    except (ValueError, TypeError) as error:
        raise ContractError("split freeze/amendments require timezone chronology and affected invalidations") from error
    return {"contract": "pass", "members": len(seen), "axes": sorted(axes), "data_acceptance": "pending"}
