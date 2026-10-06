"""Explicit resource dependencies and pinned third-party rights for local candidates."""

import json
import re
from pathlib import Path

from core.paths import contained, digest_file, unique_paths
from core.schema import ContractError, validate_record


REGISTRY_PATH = "core/registry/catalog/resources.json"
FORMATS = {"json": ".json", "csv": ".csv", "jsonl": ".jsonl", "svg": ".svg", "markdown": ".md"}


def registry(root, *, check_files=True):
    path = contained(root, REGISTRY_PATH)
    if not path.exists():
        return {"schema_version": 1, "resources": []}
    record = validate_record("resource-registry", json.loads(path.read_text(encoding="utf-8")))
    unique_paths(r["resource_id"] for r in record["resources"])
    unique_paths(r["path"] for r in record["resources"])
    catalog = json.loads(contained(root, "core/registry/catalog/skills.json").read_text(encoding="utf-8"))
    identities = {row["id"] for row in catalog["skills"]}
    resource_paths = {row["path"] for row in record["resources"]}
    for resource in record["resources"]:
        if (not resource["consumers"] or not set(resource["consumers"]) <= identities
                or len(set(resource["consumers"])) != len(resource["consumers"])):
            raise ContractError("resource consumer missing, duplicate or unknown")
        if Path(resource["path"]).suffix != FORMATS[resource["format"]]:
            raise ContractError("resource format/path mismatch")
        members = [resource["path"], resource["reader"], *resource["requires"]]
        unique_paths(members)
        for relative in members:
            if Path(relative).suffix in {".csv", ".jsonl", ".svg"} and relative not in resource_paths:
                raise ContractError("data dependency requires its own resource/rights record")
            if not relative.startswith(("skills/", "core/profiles/resources/", "scripts/", "core/registry/catalog/")):
                raise ContractError("resource cannot package evaluation/private or unrelated data")
            target = contained(root, relative)
            if check_files and not target.is_file():
                raise ContractError(f"resource member missing: {relative}")
        source = resource["source"]
        if not re.fullmatch(r"[a-f0-9]{40}", source["version"]):
            raise ContractError("resource requires a full upstream commit")
        if check_files:
            if digest_file(contained(root, resource["path"])) != source["sha256"]:
                raise ContractError("resource differs from reviewed source bytes")
            if digest_file(contained(root, source["license_path"])) != source["license_sha256"]:
                raise ContractError("resource license drift")
        if source["license_path"] not in resource["requires"]:
            raise ContractError("resource license must be an explicit dependency")
        if source["notice_path"]:
            if source["notice_path"] not in resource["requires"]:
                raise ContractError("resource attribution must be an explicit dependency")
            if check_files and digest_file(contained(root, source["notice_path"])) != source["notice_sha256"]:
                raise ContractError("resource attribution drift")
        elif source["notice_sha256"]:
            raise ContractError("notice hash has no notice path")
        if resource["dependency"] not in {"required", "optional"}:
            raise ContractError("unknown resource dependency treatment")
    return record


def resource_members(root):
    return {relative for row in registry(root)["resources"]
            for relative in [row["path"], row["reader"], *row["requires"]]}


def resource_edges(root, identity=None):
    edges = {}
    for resource in registry(root)["resources"]:
        if identity is not None and identity not in resource["consumers"]:
            continue
        edges[resource["path"]] = [resource["reader"], *resource["requires"]]
    return edges


def resource_provenance(root):
    provenance = {}
    for resource in registry(root)["resources"]:
        source = resource["source"]
        for path, upstream, digest in [
                (resource["path"], source["upstream_path"], source["sha256"]),
                (source["license_path"], source["upstream_license_path"], source["license_sha256"])]:
            row = {"source_kind": "copied-upstream", "repository": source["repository"],
                   "version": source["version"], "upstream_path": upstream, "upstream_sha256": digest,
                   "as_of": source["as_of"], "license": source["license"],
                   "license_path": source["license_path"], "license_sha256": source["license_sha256"],
                   "notice_path": source["notice_path"], "notice_sha256": source["notice_sha256"],
                   "redistribution": source["redistribution"], "review_reference": source["review_reference"]}
            if path in provenance and provenance[path] != row:
                raise ContractError("conflicting provenance for one resource member")
            provenance[path] = row
    return provenance


def verify_provenance(root, relative, pin, files, *, check_files=False):
    if pin.get("rights") == "owned-local-package":
        if set(pin) != {"sha256", "rights"}:
            raise ContractError("owned content cannot conceal third-party provenance")
        return
    if set(pin) != {"sha256", "rights", "provenance"} or pin["rights"] != "copied-upstream":
        raise ContractError("unknown copied content rights record")
    provenance = validate_record("resource-provenance", pin["provenance"])
    if provenance["upstream_sha256"] != pin["sha256"]:
        raise ContractError("copied bytes must retain the original full hash")
    for path_key, hash_key in [("license_path", "license_sha256"), ("notice_path", "notice_sha256")]:
        path = provenance[path_key]
        if not path:
            if provenance[hash_key]:
                raise ContractError("notice hash without path")
            continue
        contained(root, path)
        if files.get(path, {}).get("sha256") != provenance[hash_key]:
            raise ContractError("missing or mismatched pinned license/attribution")
        if check_files and digest_file(contained(root, path)) != provenance[hash_key]:
            raise ContractError("license/attribution bytes changed")
    contained(root, relative)
