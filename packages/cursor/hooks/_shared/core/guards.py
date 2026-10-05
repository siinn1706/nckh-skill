"""Structural guards. Semantic entailment and human quality remain reviewer-owned."""

import json
import math
from pathlib import Path

from core.paths import contained, digest_file
from core.schema import ContractError, _json_equal, validate_record


FACT_DIMENSIONS = {"numbers", "units", "denominators", "negation", "modality",
                   "certainty", "population", "time", "causality", "terminology",
                   "citations", "limitations"}


def writer_request(action, *, args=(), explicit_target=None, brief_locale=None, draft_locale=None):
    """Normalize declared skill arguments; hosts do not gain a new CLI parser."""
    owners = {"polish": "nckh-humanwrite", "translate": "nckh-humanwrite",
              "outline": "nckh-paperwrite", "section": "nckh-paperwrite",
              "argument": "nckh-paperwrite", "reporting": "nckh-paperwrite",
              "revision-response": "nckh-paperwrite"}
    if action not in owners:
        raise ContractError("writer action needs a known owner or explicit clarification")
    if not set(args) <= {"--en", "--vi"} or len(args) != len(set(args)):
        raise ContractError("unsupported or duplicate writer arguments")
    if set(args) == {"--en", "--vi"}:
        return {"status": "conflict-no-write", "owner": owners[action], "output_locale": None}
    locale = args[0][2:] if args else next((value for value in
        (explicit_target, brief_locale, draft_locale) if value in {"en", "vi", "bilingual"}), None)
    return {"status": "resolved" if locale else "ask-one-question-no-write",
            "owner": owners[action], "output_locale": locale}


def factual_delta(before, after, *, protected_before=(), protected_after=()):
    if not FACT_DIMENSIONS <= before.keys() or not FACT_DIMENSIONS <= after.keys():
        raise ContractError("complete declared factual slots are required; extraction is not certified")
    changes = {key: {"before": before[key], "after": after[key]}
               for key in sorted(FACT_DIMENSIONS) if before[key] != after[key]}
    if protected_before != protected_after:
        changes["protected_regions"] = {"before": protected_before, "after": protected_after}
    return {"status": "pending-evidence" if changes else "declared-slots-preserved",
            "changes": changes, "semantic_fidelity": "unverified"}


def check_claim_bundle(claim, evidence, sources, *, exact_quote=False):
    """Validate bindings, never infer semantic support from a DOI or a hash."""
    if claim["verdict"] != "supported" or not claim["evidence_ids"]:
        return "pending"
    for evidence_id in claim["evidence_ids"]:
        item = evidence.get(evidence_id)
        if item is None:
            return "pending"
        source = sources.get(item["source_id"])
        if source is None or item["source_sha256"] != source["sha256"]:
            return "stale"
        if source["status"] != "current" or source["access"] not in {"full-text", "user-supplied"}:
            return "pending"
        if not item.get("locator", {}).get("value") or not item.get("context"):
            return "pending"
        if source.get("edition") != item.get("edition"):
            return "stale"
        if exact_quote and (item.get("ocr") == "unverified" or
                            item.get("ocr") == "visual-checked" and not item.get("visual_check_reference")):
            return "pending"
    return "bindings-valid-support-still-reviewer-owned"


def ranking_known(ranking):
    return bool(ranking and all(ranking.get(key) for key in
                ["system", "category", "metric_year", "as_of", "evidence_reference"])
                and ranking.get("quartile") in {"Q1", "Q2", "Q3", "Q4"})


def active_venue(profiles):
    if len(profiles) != 1:
        raise ContractError("one active venue profile; do not union rules")
    profile = profiles[0]
    if not all(profile.get(key) for key in ["venue_id", "venue_type", "year", "track", "article_type", "revision"]):
        raise ContractError("venue identity/year/track/article type/revision are required")
    return profile


def check_visual_receipt(receipt, files):
    required = {"source", "data", "artifact", "render", "manifest"}
    if not required <= files.keys() or not required <= receipt.get("hashes", {}).keys():
        return "pending"
    if not all(receipt.get(key) for key in ["viewer_version", "font_version", "qa_run_reference"]):
        return "pending"
    if any(digest_file(path) != receipt["hashes"][kind] for kind, path in files.items()):
        return "stale"
    return "hashes-current-native-and-scientific-gates-separate"


def _visual_file(project, reference):
    if not isinstance(reference, dict) or set(reference) != {"path", "sha256"}:
        raise ContractError("visual file needs its exact path/hash reference")
    path = contained(project, reference["path"])
    if not path.is_file() or path.stat().st_size > 1048576 or digest_file(path) != reference["sha256"]:
        raise ContractError("visual source/run/code/output missing, oversized or stale")
    return path


def _visual_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ContractError("duplicate visual source key")
            result[key] = value
        return result
    def reject(value):
        raise ContractError("nonfinite visual source")
    def finite_float(value):
        number = float(value)
        if not math.isfinite(number):
            raise ContractError("nonfinite visual source number")
        return number
    text = path.read_text(encoding="utf8")
    return ([json.loads(line, object_pairs_hook=unique, parse_constant=reject, parse_float=finite_float) for line in text.splitlines() if line.strip()]
            if path.suffix == ".jsonl" else json.loads(text, object_pairs_hook=unique, parse_constant=reject, parse_float=finite_float))


def _visual_pointer(record, pointer):
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ContractError("source-to-mark mapping needs a JSON pointer")
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        record = record[int(token)] if isinstance(record, list) else record[token]
    return record


def check_visual_purpose(brief, *, project=None, sources=None):
    """Synchronous read-only preflight. Hash consistency cannot prove source truth."""
    def result(decision, code):
        return {"decision": decision, "reason_code": code, "evidence_class": "deterministic",
                "coverage": "controlled-preflight" if project is not None else "instruction-only",
                "scientific_acceptance": "pending", "native_acceptance": "unverified"}
    purpose = brief.get("visual_purpose") if isinstance(brief, dict) else None
    if not isinstance(purpose, dict):
        return result("pending", "visual-purpose-missing")
    if purpose.get("artifact_role") in {"ad", "banner", "logo", "thumbnail", "generic-artwork", "branding"}:
        return result("block", "non-research-generation")
    try:
        validate_record("brief", brief)
        for field in ("purpose_question", "research_object", "artifact_role", "evidence_ids"):
            if not purpose[field] or isinstance(purpose[field], str) and not purpose[field].strip():
                return result("pending", "visual-purpose-incomplete")
        if project is None or not sources or not set(purpose["evidence_ids"]) <= sources.keys():
            return result("pending", "visual-evidence-missing")
        if len(purpose["evidence_ids"]) != len(set(purpose["evidence_ids"])):
            raise ContractError("duplicate visual evidence ID")
        records = {}
        for identity in purpose["evidence_ids"]:
            source = sources[identity]
            if not source.get("rights") or source["rights"] in {"unknown", "restricted", "pending"}:
                return result("block", "visual-rights-missing")
            if source.get("access") not in {"public-data", "full-text", "user-supplied", "owned-run"} or not source.get("locator"):
                return result("pending", "visual-source-access-missing")
            path = _visual_file(project, source["file"])
            records[identity] = _visual_json(path)
        kind, origin = purpose["kind"], purpose["data_origin"]
        if kind == "chart" and origin not in {"observed", "derived", "computational", "simulation"}:
            raise ContractError("chart has no valid data origin")
        if origin in {"derived", "computational", "simulation"}:
            computation = purpose.get("computation")
            if not computation or purpose["non_evidentiary_label"] != "not observed measurements":
                return result("pending", "computed-origin-label-or-run-missing")
            for name in ("model", "version", "run_locator"):
                if not computation.get(name):
                    raise ContractError("computation model/version/locator missing")
            for name in ("code", "source", "transform", "output", "run_receipt"):
                _visual_file(project, computation[name])
            run = _visual_json(_visual_file(project, computation["run_receipt"]))
            if (run.get("status") != "completed-unreviewed" or run.get("exit_status") != 0
                    or run.get("code_sha256") != computation["code"]["sha256"]
                    or run.get("source_sha256") != computation["source"]["sha256"]
                    or run.get("transform_sha256") != computation["transform"]["sha256"]
                    or run.get("output_sha256") != computation["output"]["sha256"]
                    or run.get("parameters") != computation["parameters"]
                    or not run.get("command") or not run.get("cleanup")):
                raise ContractError("computation receipt/output binding is stale or incomplete")
            if not any(sources[identity]["file"] == computation["output"] for identity in purpose["evidence_ids"]):
                raise ContractError("computed mark source is not the verified run output")
            if not purpose["uncertainty"] and not purpose["uncertainty_not_applicable_reason"]:
                return result("pending", "visual-uncertainty-missing")
        if kind == "illustration" and purpose["non_evidentiary_label"] != "illustrative/non-evidentiary":
            return result("pending", "illustration-label-missing")
        marks = purpose["source_to_mark"]
        if (not marks or len(marks) != len(purpose["required_marks"])
                or {mark["mark_id"] for mark in marks} != set(purpose["required_marks"])
                or len(purpose["required_marks"]) != len(set(purpose["required_marks"]))):
            raise ContractError("every unique value, label and arrow needs a source-to-mark mapping")
        for mark in marks:
            identity = mark["evidence_id"]
            if identity not in records or mark["source_sha256"] != sources[identity]["file"]["sha256"]:
                raise ContractError("mark source/evidence mismatch")
            if mark["origin"] in {"inference", "illustration"}:
                if (mark["origin"] == "inference" and mark["mark_id"] not in purpose["inference_labels"]
                        or mark["origin"] == "illustration" and not purpose["non_evidentiary_label"]):
                    return result("pending", "visual-inference-label-missing")
                _visual_pointer(records[identity], mark["pointer"])
            else:
                expected_origin = "observed-field" if origin == "observed" else "calculation-output"
                if mark["origin"] != expected_origin or sources[identity].get("data_origin") != origin:
                    raise ContractError("observed/computed mark origin differs from its source")
                if not _json_equal(_visual_pointer(records[identity], mark["pointer"]), mark["value"]):
                    raise ContractError("mark value differs from actual source bytes")
            for field in ("unit", "denominator"):
                pointer = mark[field + "_pointer"]
                if pointer:
                    if not _json_equal(_visual_pointer(records[identity], pointer), mark[field]):
                        raise ContractError("mark unit/denominator differs from its source")
                elif mark[field] not in {"", None}:
                    raise ContractError("unit/denominator lacks a source field")
        return result("allow", "visual-purpose-and-mark-bindings-current")
    except (ContractError, OSError, ValueError, KeyError, TypeError, IndexError, OverflowError, RecursionError):
        return result("block", "visual-preflight-invalid-or-stale")


def require_operation(operation, *, grant, backup_reference=None):
    if operation not in grant:
        raise ContractError(f"operation outside actual grant: {operation}")
    if operation in {"schema-change", "data-change"} and not backup_reference:
        raise ContractError("backup required before schema/data change")


def xia_mode(flags):
    allowed = {"--compare": "report-only", "--port": "plan-only", "--improve": "plan-only"}
    if len(flags) > 1 or any(flag not in allowed for flag in flags):
        raise ContractError("unsupported or conflicting Xia mode")
    return allowed[flags[0]] if flags else "plan-only"


def metric(numerator, denominator, *, time_range, population):
    if denominator is None or denominator <= 0 or numerator < 0 or numerator > denominator:
        raise ContractError("valid actual numerator/denominator required")
    if not time_range or not population:
        raise ContractError("time range and population required")
    return {"rate": numerator / denominator, "numerator": numerator,
            "denominator": denominator, "time_range": time_range,
            "population": population, "causal_lift": "unverified"}


def experiment_design(design):
    fields = {"hypothesis", "unit", "randomization", "allocation", "primary_metric",
              "denominator", "guardrails", "sample_rationale", "stopping", "analysis"}
    if not fields <= design.keys() or not all(design[key] for key in fields):
        raise ContractError("complete experiment assumptions/protocol required")
    if design["stopping"] == "first-significant-p-value":
        raise ContractError("unplanned peeking cannot establish a stopping rule")
    return "protocol-recorded-statistical-review-pending"
