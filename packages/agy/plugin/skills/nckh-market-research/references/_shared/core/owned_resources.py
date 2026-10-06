"""Typed, bounded authored reference records and contribution provenance."""

import re

from core.paths import contained
from core.research_io import ArtifactReader, unique_ids
from core.schema import ContractError, validate_record


PACK_KINDS = {"R-statistical-recipes": "statistical-recipe", "R-telemetry-dictionary": "telemetry-field",
              "R-aiops-benchmark-cards": "benchmark-card", "R-aiops-evaluation-recipes": "evaluation-recipe"}
COMMON_FIELDS = {"id", "kind", "title", "domain", "consumer", "language", "genre", "source_ids", "limitations"}
KIND_FIELDS = {
    "statistical-recipe": {"estimand", "independent_unit", "assumptions", "estimator", "uncertainty", "reporting", "stopping"},
    "telemetry-field": {"signal", "field", "unit_policy", "time_policy", "aggregation", "correlation", "quality"},
    "benchmark-card": {"benchmark", "suite", "task", "modalities", "label_semantics", "rights_gate", "split_policy", "execution_gate"},
    "evaluation-recipe": {"task", "baselines", "metrics", "ties", "no_answer", "failure_policy", "leakage", "trust"},
}
ARRAY_FIELDS = {"consumer", "source_ids", "limitations", "assumptions", "reporting", "modalities", "baselines", "metrics", "leakage"}
OWNED_SOURCE_KEYS = {"repository", "version", "as_of", "license", "license_path", "license_sha256", "notice_path", "notice_sha256",
                     "redistribution", "review_reference", "sha256", "version_kind", "rights_scope", "license_kind"}


def validate_owned_provenance(record, artifact_hash, *, record_ids=None):
    validate_record("owned-resource-provenance", record)
    if record["artifact_sha256"] != artifact_hash:
        raise ContractError("owned authored artifact hash differs from provenance")
    ids = unique_ids(record["record_ids"], "authored record IDs")
    if not ids or record_ids is not None and ids != set(record_ids):
        raise ContractError("owned provenance requires exact actual authored record membership")
    sources = unique_ids([row["source_id"] for row in record["contributions"]], "source contributions")
    if not sources:
        raise ContractError("authored reference requires reviewed source contributions")
    covered = set()
    for contribution in record["contributions"]:
        selected = unique_ids(contribution["record_ids"], "contribution records")
        if not selected or not selected <= ids:
            raise ContractError("source contribution must name actual authored records")
        covered |= selected
        commit = contribution["upstream_commit"]
        if commit is None:
            if not contribution["unknown_reason"] or contribution["version_kind"] == "git-commit":
                raise ContractError("unknown upstream commit requires snapshot kind and explicit reason")
        elif not isinstance(commit, str) or not re.fullmatch(r"[a-f0-9]{40}", commit):
            raise ContractError("upstream commit must be verified full hash or null")
        if contribution["version_kind"] == "git-commit" and contribution["version_or_snapshot"] != commit:
            raise ContractError("contribution version differs from verified commit")
    if covered != ids:
        raise ContractError("source contributions do not cover exact authored records")
    for ref in (record["rights_record"], record["attribution_record"]):
        if not ref["path"].startswith("core/profiles/resources/"):
            raise ContractError("authored notice must stay in its reviewed resource namespace")
    return record


def validate_owned_source(resource):
    source = resource["source"]
    if (set(source) != OWNED_SOURCE_KEYS or resource["copied_vs_reauthored"] != "reauthored-with-sources"
            or source["license"] != "owned-local-package" or source["redistribution"] != "local-package-only"
            or source["rights_scope"] != "local-package-only" or source["version_kind"] != "owned-authored"
            or source["license_kind"] != "owned-rights-record"):
        raise ContractError("owned reference cannot disguise copied/snapshot bytes or upstream rights")
    record = validate_owned_provenance(resource.get("owned_provenance"), source["sha256"])
    if (record["authoring_version"] != source["version"] or record["as_of"] != source["as_of"]
            or record["rights_record"] != {"path": source["license_path"], "sha256": source["license_sha256"]}
            or record["attribution_record"] != {"path": source["notice_path"], "sha256": source["notice_sha256"]}):
        raise ContractError("owned source and authored provenance/notice bindings differ")
    return record


def validate_pack_rows(resource, rows):
    if resource["resource_id"] not in PACK_KINDS:
        raise ContractError("no reviewed authored reader for this resource")
    expected_kind = PACK_KINDS[resource["resource_id"]]
    ids = []
    contribution_map = {row["source_id"]: set(row["record_ids"]) for row in resource["owned_provenance"]["contributions"]}
    for row in rows:
        if not isinstance(row, dict) or row.get("kind") != expected_kind or set(row) != COMMON_FIELDS | KIND_FIELDS[expected_kind]:
            raise ContractError("authored reference has unknown/private fields or wrong typed record")
        for name, value in row.items():
            if name in ARRAY_FIELDS:
                if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item.strip() for item in value):
                    raise ContractError("authored array fields require bounded nonempty strings")
                unique_ids(value, "authored " + name)
            elif not isinstance(value, str) or not value.strip():
                raise ContractError("authored fields require actual nonempty reference text")
        if (row["domain"] != resource["domain"] or row["language"] != resource["locale"] or row["genre"] != resource["genre"]
                or not set(row["consumer"]) <= set(resource["consumers"])):
            raise ContractError("authored row applicability differs from exact registered context")
        if set(row["source_ids"]) != {source for source, members in contribution_map.items() if row["id"] in members}:
            raise ContractError("authored row source IDs differ from contribution bindings")
        ids.append(row["id"])
    unique_ids(ids, "actual authored records")
    validate_owned_provenance(resource["owned_provenance"], resource["source"]["sha256"], record_ids=ids)
    if {consumer for row in rows for consumer in row["consumer"]} != set(resource["consumers"]):
        raise ContractError("every registered authored consumer requires applicable records")
    return rows


def read_pack(resource, project, *, reader=None):
    reader = reader or ArtifactReader(project)
    data = reader.binding({"path": resource["path"], "sha256": resource["source"]["sha256"]})
    rows = []
    for line in data.decode("utf-8-sig").splitlines():
        if not line.strip():
            raise ContractError("authored JSONL cannot contain blank records")
        rows.append(reader.parse(line))
    return validate_pack_rows(resource, rows)
