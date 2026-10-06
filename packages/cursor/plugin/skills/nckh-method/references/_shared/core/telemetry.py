"""Observed telemetry semantics, correlation and join-quality invariants."""

from collections import Counter

from core.research_io import ArtifactReader, finite_number, unique_ids
from core.schema import ContractError, validate_record


def validate_telemetry_manifest(record, *, project=None, reader=None):
    validate_record("telemetry-manifest", record)
    modalities = unique_ids(record["modalities"], "telemetry modalities")
    signals = {row["id"]: row for row in record["signals"]}
    if len(signals) != len(record["signals"]) or any(row["modality"] not in modalities for row in signals.values()):
        raise ContractError("signals require exact unique IDs and actually available modalities")
    clock = record["time"]
    if clock["tolerance"] < 0 or clock["skew"] < 0:
        raise ContractError("clock skew and alignment tolerance cannot be negative")
    if clock["alignment"] == "measured":
        if clock["origin"] == "unknown" or not clock["timezone"] or not clock["precision"] or clock["skew"] > clock["tolerance"]:
            raise ContractError("measured alignment requires actual origin/zone/precision within tolerance")
    elif not clock["reason"]:
        raise ContractError("unknown/not-applicable clock alignment requires a reason")
    if record["semantic_conventions"]["status"] == "unknown" and not record["semantic_conventions"]["reason"]:
        raise ContractError("unknown convention status requires an explicit reason")
    for signal in signals.values():
        if signal["unit_status"] == "unknown":
            if not signal["reason"] or signal["source_unit"] != signal["normalized_unit"]:
                raise ContractError("unknown units must remain unknown with reason; no invented conversion")
        elif not signal["source_unit"] or not signal["normalized_unit"]:
            raise ContractError("known unit mapping cannot use blank units")
        if signal["source_unit"] != signal["normalized_unit"] and not signal["conversion"]:
            raise ContractError("changed units require actual conversion code/config/factor lineage")
        if signal["source_type"] == "counter" and not signal["monotonic"]:
            raise ContractError("cumulative counters require monotonic semantics with explicit resets")
        if signal["aggregation"] in {"delta", "rate"} and signal["source_type"] != "counter":
            raise ContractError("counter delta/rate cannot be silently applied to gauge/event signals")
        if signal["source_type"] == "unknown" and not signal["reason"]:
            raise ContractError("unknown signal type requires a reason")
    if record["stage"] in {"metadata", "not-applicable"}:
        if record["outputs"] or record["quality"]["samples"] or record["joins"] or record["normalization"]:
            raise ContractError("unobserved telemetry cannot claim normalized samples or completed joins")
        if record["stage"] == "not-applicable" and (not record["reason"] or modalities or signals or record["sources"]):
            raise ContractError("not-applicable telemetry must preserve reason and absent operational modalities")
        return {"stage": record["stage"], "contract": "pass", "observed_modalities": []}
    if not project and reader is None:
        raise ContractError("normalized telemetry requires an actual contained project")
    if not record["sources"] or len(record["outputs"]) != 1 or not modalities:
        raise ContractError("normalization requires actual source/output/modality bindings")
    reader = reader or ArtifactReader(project)
    for reference in record["sources"]:
        reader.binding(reference)
    for signal in signals.values():
        for conversion in signal["conversion"]:
            reader.binding(conversion["code"])
            reader.binding(conversion["config"])
            finite_number(conversion["factor"], "conversion factor")
    rows = reader.rows(record["outputs"][0])
    if len(record["normalization"]) != 1:
        raise ContractError("normalized telemetry requires explicit normalization lineage")
    transform = record["normalization"][0]
    if transform["inputs"] != record["sources"] or transform["outputs"] != record["outputs"]:
        raise ContractError("normalization inputs/outputs differ from bound telemetry")
    reader.binding(transform["code"])
    reader.binding(transform["config"])
    raw_rows = [row for ref in transform["inputs"] for row in reader.rows(ref)]
    source_rows = len(raw_rows)
    if (source_rows != transform["input_rows"] or len(rows) != transform["output_rows"]
            or transform["output_rows"] + transform["dropped_rows"] != source_rows):
        raise ContractError("normalization counts do not reconcile actual canonical rows")
    if not rows or len(rows) != record["quality"]["samples"]:
        raise ContractError("actual telemetry sample count differs from manifest or is empty")
    expected = {"id", "signal_id", "timestamp", "value", "unit", "resource_id", "trace_id", "span_id"}
    by_id = {}
    duplicate = set()
    missing = zeros = 0
    observed_modalities = set()
    correlation_missing = set()
    traces = {}
    signal_values = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != expected or row["signal_id"] not in signals:
            raise ContractError("canonical telemetry fields/signal binding mismatch")
        if not isinstance(row["id"], str) or not row["id"].strip():
            raise ContractError("telemetry sample ID must be nonempty")
        if row["id"] in by_id:
            duplicate.add(row["id"])
        by_id[row["id"]] = row
        signal = signals[row["signal_id"]]
        observed_modalities.add(signal["modality"])
        if row["unit"] != signal["normalized_unit"]:
            raise ContractError("sample unit differs from explicit normalized signal mapping")
        if row["timestamp"] is None:
            if clock["alignment"] == "measured":
                raise ContractError("measured alignment cannot contain unknown timestamps")
        else:
            finite_number(row["timestamp"], "timestamp")
        if row["value"] is None:
            missing += 1
        else:
            if signal["modality"] == "logs":
                if not isinstance(row["value"], str):
                    raise ContractError("log event body must remain actual untrusted text")
            else:
                finite_number(row["value"], "telemetry value")
                zeros += row["value"] == 0
        for name in ("resource_id", "trace_id", "span_id"):
            if not isinstance(row[name], str):
                raise ContractError("correlation identity must be a string; blank is unknown")
            if name in record["correlation"]["required_keys"] and not row[name]:
                correlation_missing.add(row["id"])
        if row["span_id"]:
            if not row["trace_id"] or row["span_id"] in traces and traces[row["span_id"]] != row["trace_id"]:
                raise ContractError("span identity has missing/conflicting trace reference")
            traces[row["span_id"]] = row["trace_id"]
    if observed_modalities != modalities:
        raise ContractError("declared telemetry modality has no actual samples")
    quality = record["quality"]
    if missing != quality["missing"] or zeros != quality["zeros"]:
        raise ContractError("missing telemetry is not zero; actual quality counts differ")
    if duplicate != set(quality["duplicate_ids"]) or duplicate:
        raise ContractError("duplicate/conflicting sample IDs require quarantine before normalization")
    if correlation_missing != unique_ids(record["correlation"]["missing_ids"], "missing correlation IDs"):
        raise ContractError("actual missing correlation IDs must be reported")
    if record["correlation"]["duplicate_ids"]:
        raise ContractError("duplicate correlation identities require resolution/quarantine")
    if len({row["resource_id"] for row in rows}) > record["sampling"]["cardinality_limit"]:
        raise ContractError("actual telemetry resource cardinality exceeds frozen limit")
    actual_resets = {signal_id: set() for signal_id, signal in signals.items() if signal["source_type"] == "counter"}
    for row in raw_rows:
        if not isinstance(row, dict) or set(row) != expected or row["signal_id"] not in signals:
            raise ContractError("raw telemetry requires canonical identity/value/time mapping")
        if row["signal_id"] in actual_resets:
            if row["value"] is not None:
                finite_number(row["value"], "raw counter")
            if row["timestamp"] is not None:
                finite_number(row["timestamp"], "raw counter timestamp")
            if row["value"] is not None and row["timestamp"] is not None:
                signal_values.setdefault((row["signal_id"], row["resource_id"]), []).append(row)
    for (signal_id, _), values in signal_values.items():
        ordered = sorted(values, key=lambda row: row["timestamp"])
        if len({row["timestamp"] for row in ordered}) != len(ordered):
            raise ContractError("counter order is ambiguous at repeated resource timestamps")
        actual_resets[signal_id].update(after["id"] for before, after in zip(ordered, ordered[1:]) if after["value"] < before["value"])
    for signal_id, resets in actual_resets.items():
        if resets != unique_ids(signals[signal_id]["resets"], "counter reset IDs"):
            raise ContractError("actual cumulative counter resets differ from declared lineage")
    for join in record["joins"]:
        left = unique_ids(join["left_ids"], "join left IDs")
        right = unique_ids(join["right_ids"], "join right IDs")
        if not left <= by_id.keys() or not right <= by_id.keys():
            raise ContractError("join refers to unobserved telemetry IDs")
        left_counts = Counter()
        right_counts = Counter()
        pair_ids = set()
        for pair in join["pairs"]:
            key = (pair["left"], pair["right"])
            if key in pair_ids or key[0] not in left or key[1] not in right:
                raise ContractError("join pair is duplicated or outside declared membership")
            pair_ids.add(key)
            ltime, rtime = by_id[key[0]]["timestamp"], by_id[key[1]]["timestamp"]
            if ltime is None or rtime is None:
                raise ContractError("unknown time cannot be silently aligned in a join")
            delta = abs(ltime - rtime)
            if pair["delta"] != delta or delta > join["tolerance"] or join["tolerance"] < 0:
                raise ContractError("actual join time delta exceeds or differs from explicit tolerance")
            left_counts[key[0]] += 1
            right_counts[key[1]] += 1
        cardinality = join["cardinality"]
        if (cardinality in {"one-to-one", "many-to-one"} and any(value > 1 for value in left_counts.values())
                or cardinality in {"one-to-one", "one-to-many"} and any(value > 1 for value in right_counts.values())):
            raise ContractError("actual join cardinality violates frozen rule")
        if cardinality == "many-to-many" and not join["many_to_many_allowed"]:
            raise ContractError("many-to-many join is forbidden without explicit task rationale")
        if (join["retained"] != len(pair_ids) or join["unmatched_left"] != len(left - left_counts.keys())
                or join["unmatched_right"] != len(right - right_counts.keys())
                or join["dropped"] != join["unmatched_left"] + join["unmatched_right"]):
            raise ContractError("join retained/dropped/unmatched counts do not reconcile")
    return {"stage": "normalized", "contract": "pass", "samples": len(rows),
            "observed_modalities": sorted(observed_modalities), "root_cause": "not-inferred"}
