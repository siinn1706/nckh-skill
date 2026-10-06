"""Explicit resource dependencies and pinned third-party rights for local candidates."""

import json
import math
import re
from pathlib import Path

from core.paths import contained, digest_file, unique_paths
from core.schema import ContractError, validate_record
from core.owned_resources import read_pack, validate_owned_provenance, validate_owned_source
from core.research_io import ArtifactReader


REGISTRY_PATH = "core/registry/catalog/resources.json"
FORMATS = {"json": ".json", "csv": ".csv", "jsonl": ".jsonl", "svg": ".svg",
           "markdown": ".md", "xml": ".xml", "zip": ".zip"}
LICENSES = {"MIT", "Apache-2.0", "BSD-3-Clause", "CC-BY-4.0", "CC-BY-SA-4.0"}
VERSION_KINDS = {"git-commit", "mediawiki-oldid", "pmcid-snapshot", "api-snapshot",
                 "dataset-archive", "swe-bench-task", "normalized-bundle",
                 "reference-snapshot"}
COPY_MODES = {"verbatim-upstream", "normalized-with-lineage", "metadata-only-reference", "reauthored-with-sources"}


def _load_json(path):
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ContractError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def reject_constant(value):
        raise ContractError(f"nonfinite JSON constant: {value}")

    def finite_float(value):
        result = float(value)
        if not math.isfinite(result):
            raise ContractError("nonfinite JSON number")
        return result

    return json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=unique_keys, parse_constant=reject_constant,
                      parse_float=finite_float)


def registry(root, *, check_files=True):
    path = contained(root, REGISTRY_PATH)
    if not path.exists():
        return {"schema_version": 1, "resources": []}
    reader = ArtifactReader(root)
    record = validate_record("resource-registry", reader.json(REGISTRY_PATH))
    unique_paths(r["resource_id"] for r in record["resources"])
    unique_paths(r["path"] for r in record["resources"])
    catalog = reader.json("core/registry/catalog/skills.json")
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
        source = resource["source"]
        _validate_source(resource)
        documented = {source["license_path"], source["notice_path"],
                      *(item["path"] for item in source.get("lineage", []) if item.get("path"))}
        for relative in members:
            if relative not in resource_paths | documented | {resource["reader"], REGISTRY_PATH}:
                raise ContractError("data dependency requires its own resource/rights record")
            if not relative.startswith(("skills/", "core/profiles/resources/", "scripts/", "core/registry/catalog/")):
                raise ContractError("resource cannot package evaluation/private or unrelated data")
            target = contained(root, relative)
            if check_files and not target.is_file():
                raise ContractError(f"resource member missing: {relative}")
        if check_files:
            reader.binding({"path": resource["path"], "sha256": source["sha256"]})
            reader.binding({"path": source["license_path"], "sha256": source["license_sha256"]})
            if resource["source_kind"] == "owned-reference":
                read_pack(resource, root, reader=reader)
        if source["license_path"] not in resource["requires"]:
            raise ContractError("resource license must be an explicit dependency")
        if source["notice_path"]:
            if source["notice_path"] not in resource["requires"]:
                raise ContractError("resource attribution must be an explicit dependency")
            if check_files and digest_file(contained(root, source["notice_path"])) != source["notice_sha256"]:
                raise ContractError("resource attribution drift")
        elif source["notice_sha256"]:
            raise ContractError("notice hash has no notice path")
        for lineage in source.get("lineage", []):
            relative = lineage.get("path")
            if not relative:
                continue
            if relative not in resource["requires"]:
                raise ContractError("lineage path must be an explicit resource dependency")
            if check_files and digest_file(contained(root, relative)) != lineage["sha256"]:
                raise ContractError("lineage bytes changed")
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


def _provenance_row(resource, source, upstream_path, upstream_sha256, *, artifact_sha256=None,
                    copied_vs_reauthored=None, upstream_sha256s=None):
    row = {"source_kind": resource["source_kind"], "repository": source["repository"],
           "version": source["version"], "upstream_path": upstream_path,
           "upstream_sha256": upstream_sha256, "as_of": source["as_of"],
           "license": source["license"], "license_path": source["license_path"],
           "license_sha256": source["license_sha256"], "notice_path": source["notice_path"],
           "notice_sha256": source["notice_sha256"], "redistribution": source["redistribution"],
           "review_reference": source["review_reference"]}
    mode = copied_vs_reauthored or resource.get("copied_vs_reauthored", "verbatim-upstream")
    if mode != "verbatim-upstream":
        row["copied_vs_reauthored"] = mode
        row["artifact_sha256"] = artifact_sha256 or upstream_sha256
        if upstream_sha256s:
            row["upstream_sha256s"] = list(upstream_sha256s)
    for key in ["version_kind", "rights_scope", "retrieved_at", "retrieval_timezone", "lineage"]:
        if key in source:
            row[key] = source[key]
    return row


def resource_provenance(root):
    provenance = {}
    for resource in registry(root)["resources"]:
        source = resource["source"]
        if resource["source_kind"] == "owned-reference":
            provenance[resource["path"]] = resource["owned_provenance"]
            continue
        lineage = source.get("lineage", [])
        mode = resource.get("copied_vs_reauthored", "verbatim-upstream")
        upstreams = source.get("upstream_sha256s", [])
        main_upstream = source.get("upstream_sha256", upstreams[0] if upstreams else source["sha256"])
        entries = [(resource["path"], source["upstream_path"], main_upstream,
                    source["sha256"], mode, upstreams)]
        if source.get("license_kind", "verbatim-upstream") == "verbatim-upstream":
            entries.append((source["license_path"], source["upstream_license_path"], source["license_sha256"],
                            source["license_sha256"], "verbatim-upstream", None))
        entries.extend((item["path"], item["locator"], item.get("upstream_sha256", item["sha256"]),
                        item["sha256"], mode, [item.get("upstream_sha256", item["sha256"])])
                       for item in lineage if item.get("path"))
        for path, upstream, digest, artifact, entry_mode, entry_upstreams in entries:
            row = _provenance_row(resource, source, upstream, digest, artifact_sha256=artifact,
                                  copied_vs_reauthored=entry_mode, upstream_sha256s=entry_upstreams)
            if path in provenance and provenance[path] != row:
                raise ContractError("conflicting provenance for one resource member")
            provenance[path] = row
    return provenance


def verify_provenance(root, relative, pin, files, *, check_files=False):
    if pin.get("rights") == "owned-local-package":
        if set(pin) != {"sha256", "rights"}:
            raise ContractError("owned content cannot conceal third-party provenance")
        return
    if pin.get("rights") == "owned-reference":
        if set(pin) != {"sha256", "rights", "provenance"}:
            raise ContractError("owned reference requires explicit contribution provenance")
        provenance = validate_owned_provenance(pin["provenance"], pin["sha256"])
        for ref in (provenance["rights_record"], provenance["attribution_record"]):
            contained(root, ref["path"])
            if files.get(ref["path"], {}).get("sha256") != ref["sha256"] or files[ref["path"]].get("rights") != "owned-local-package":
                raise ContractError("owned reference notice must bind actual original owned bytes")
            if check_files and digest_file(contained(root, ref["path"])) != ref["sha256"]:
                raise ContractError("owned reference rights/attribution drift")
        contained(root, relative)
        return
    if set(pin) != {"sha256", "rights", "provenance"} or pin["rights"] != "copied-upstream":
        raise ContractError("unknown copied content rights record")
    provenance = validate_record("resource-provenance", pin["provenance"])
    mode = provenance.get("copied_vs_reauthored", "verbatim-upstream")
    if provenance["source_kind"] == "copied-upstream" and (
            provenance["license"] not in {"MIT", "Apache-2.0"}
            or not re.fullmatch(r"[a-f0-9]{40}", provenance["version"])
            or mode != "verbatim-upstream"
            or provenance["redistribution"] != "permitted-with-notices"):
        raise ContractError("legacy copied provenance requires original commit/license/bytes")
    if provenance["source_kind"] == "retrieved-snapshot":
        scope = provenance.get("rights_scope")
        expected = "reference-only" if scope == "reference-only" else "permitted-with-notices"
        if (provenance.get("version_kind") not in VERSION_KINDS
                or scope not in {"redistributable", "reference-only"}
                or provenance["redistribution"] != expected
                or scope == "reference-only" and mode != "metadata-only-reference"
                or mode == "metadata-only-reference" and scope != "reference-only"
                or not provenance.get("retrieved_at") or not provenance.get("retrieval_timezone")):
            raise ContractError("snapshot provenance has unresolved version/rights/retrieval")
    if mode == "verbatim-upstream":
        if provenance["upstream_sha256"] != pin["sha256"]:
            raise ContractError("copied bytes must retain the original full hash")
    elif mode in {"normalized-with-lineage", "metadata-only-reference"}:
        if provenance.get("artifact_sha256") != pin["sha256"]:
            raise ContractError("normalized bytes must retain their packaged artifact hash")
        upstreams = provenance.get("upstream_sha256s", [])
        if provenance["upstream_sha256"] not in upstreams:
            raise ContractError("normalized provenance must retain its upstream hash list")
        lineage_hashes = {item.get("upstream_sha256", item["sha256"])
                          for item in provenance.get("lineage", [])}
        if not set(upstreams) <= lineage_hashes:
            raise ContractError("normalized provenance is missing upstream lineage")
    else:
        raise ContractError("unknown copied content transformation")
    for lineage in provenance.get("lineage", []):
        path = lineage.get("path")
        if not path:
            continue
        target = contained(root, path)
        member = files.get(path, {})
        if member.get("sha256") != lineage["sha256"]:
            raise ContractError("missing or mismatched pinned lineage")
        if lineage["kind"] in {"source-response", "archive-member"} and (
                member.get("rights") != "copied-upstream"
                or member.get("provenance", {}).get("upstream_sha256")
                != lineage.get("upstream_sha256", lineage["sha256"])):
            raise ContractError("packaged upstream lineage requires matching third-party provenance")
        if check_files and digest_file(target) != lineage["sha256"]:
            raise ContractError("packaged lineage bytes changed")
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


def _validate_source(resource):
    source = resource["source"]
    kind = resource["source_kind"]
    mode = resource["copied_vs_reauthored"]
    if kind == "owned-reference":
        validate_owned_source(resource)
        return
    if "owned_provenance" in resource or mode == "reauthored-with-sources":
        raise ContractError("legacy copied/snapshot source cannot be relabeled as authored")
    if not {"upstream_path", "upstream_license_path"} <= source.keys():
        raise ContractError("legacy resource requires original upstream path/license")
    if mode not in COPY_MODES:
        raise ContractError("unknown resource transformation")
    if source["license"] not in LICENSES:
        raise ContractError("resource rights/provenance unresolved")
    if kind == "copied-upstream":
        if (source["license"] not in {"MIT", "Apache-2.0"}
                or source.get("license_kind", "verbatim-upstream") != "verbatim-upstream"
                or mode != "verbatim-upstream" or source["redistribution"] != "permitted-with-notices"
                or not re.fullmatch(r"[a-f0-9]{40}", source["version"])):
            raise ContractError("legacy resource requires a full upstream commit and notices")
        return
    if kind != "retrieved-snapshot":
        raise ContractError("unknown resource source kind")
    if source.get("version_kind") not in VERSION_KINDS:
        raise ContractError("snapshot resource requires a supported version kind")
    if source.get("rights_scope") not in {"redistributable", "reference-only"}:
        raise ContractError("snapshot resource requires an explicit rights scope")
    if source["rights_scope"] == "reference-only" and mode != "metadata-only-reference":
        raise ContractError("reference-only snapshot cannot package source content")
    if source["rights_scope"] == "reference-only" and source["redistribution"] != "reference-only":
        raise ContractError("reference-only resource cannot claim redistribution")
    if source["rights_scope"] == "redistributable" and source["redistribution"] != "permitted-with-notices":
        raise ContractError("redistributable resource requires notices")
    if mode == "verbatim-upstream":
        if source.get("upstream_sha256") != source["sha256"]:
            raise ContractError("verbatim snapshot must retain separate matching upstream/artifact hashes")
    else:
        upstreams = source.get("upstream_sha256s", [])
        if not upstreams or source.get("upstream_sha256") not in upstreams:
            raise ContractError("normalized snapshot requires upstream raw hashes")
        lineage_hashes = {item.get("upstream_sha256", item["sha256"])
                          for item in source.get("lineage", [])}
        if not set(upstreams) <= lineage_hashes:
            raise ContractError("normalized snapshot lineage is missing an upstream hash")
        if mode == "metadata-only-reference" and source["rights_scope"] != "reference-only":
            raise ContractError("metadata-only reference must remain reference-only")
    if not source.get("retrieved_at") or not source.get("retrieval_timezone"):
        raise ContractError("snapshot resource requires retrieval timestamp and timezone")
