"""Bounded, standalone lookup of explicitly licensed snapshot resources."""

import argparse
import csv
import hashlib
import io
import json
import math
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from core.owned_resources import read_pack, validate_owned_source
from core.research_io import ArtifactReader, ResearchLimits
from core.schema import validate_record
LICENSES = {"MIT", "Apache-2.0", "BSD-3-Clause", "CC-BY-4.0", "CC-BY-SA-4.0"}
SNAPSHOT_KINDS = {"git-commit", "mediawiki-oldid", "pmcid-snapshot", "api-snapshot",
                  "dataset-archive", "swe-bench-task", "normalized-bundle",
                  "reference-snapshot"}
PRIVATE_SWE_KEYS = {"problem_statement", "patch", "test_patch", "issue_body",
                    "dataset_row", "code_fixture", "code", "body", "issue_text_reference"}
TASK_METADATA_KEYS = {"source_id", "locator", "domain", "consumer", "language", "genre",
                      "metadata_only", "reference_only", "task", "code_fixture_metadata",
                      "license", "retrieval", "provenance", "limitations"}


def strict_json(value):
    def unique_keys(pairs):
        result = {}
        for key, item in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = item
        return result

    def reject_constant(item):
        raise ValueError(f"nonfinite JSON constant: {item}")

    def finite_float(item):
        result = float(item)
        if not math.isfinite(result):
            raise ValueError("nonfinite JSON number")
        return result

    return json.loads(value, object_pairs_hook=unique_keys, parse_constant=reject_constant,
                      parse_float=finite_float)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def member(root, relative):
    if (not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative
            or any(part in {"", ".", ".."} for part in relative.split("/")) or relative.startswith("/")):
        raise ValueError("invalid resource path")
    path = root.joinpath(*relative.split("/"))
    for parent in [path, *path.parents]:
        if parent.is_symlink() or getattr(parent, "is_junction", lambda: False)():
            raise ValueError("linked resource path")
    if not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError("resource or declared dependency is unavailable")
    return path


def _verified_bytes(root, relative, expected_hash, error, reader=None):
    member(root, relative)
    data = (reader or ArtifactReader(root)).binding({"path": relative, "sha256": expected_hash})
    if digest(data) != expected_hash:
        raise ValueError(error)
    return data


def _verify_source(resource, root, reader=None):
    reader = reader or ArtifactReader(root)
    source = resource["source"]
    kind = resource["source_kind"]
    mode = resource.get("copied_vs_reauthored", "verbatim-upstream")
    if kind == "owned-reference":
        validate_owned_source(resource)
        for dependency in resource["requires"]:
            member(root, dependency)
        for ref in (resource["owned_provenance"]["rights_record"], resource["owned_provenance"]["attribution_record"]):
            _verified_bytes(root, ref["path"], ref["sha256"], "owned notice drift", reader)
        return _verified_bytes(root, resource["path"], source["sha256"], "authored artifact drift", reader)
    if "owned_provenance" in resource or not {"upstream_path", "upstream_license_path"} <= source.keys():
        raise ValueError("legacy resource cannot hide its upstream provenance")
    if mode not in {"verbatim-upstream", "normalized-with-lineage", "metadata-only-reference"}:
        raise ValueError("unknown resource transformation")
    if source["license"] not in LICENSES:
        raise ValueError("resource rights/provenance unresolved")
    if kind == "copied-upstream":
        if (source["license"] not in {"MIT", "Apache-2.0"} or mode != "verbatim-upstream"
                or source.get("license_kind", "verbatim-upstream") != "verbatim-upstream"
                or source["redistribution"] != "permitted-with-notices"
                or not re.fullmatch(r"[a-f0-9]{40}", source["version"])):
            raise ValueError("legacy resource rights/provenance unresolved")
    elif kind == "retrieved-snapshot":
        if source.get("version_kind") not in SNAPSHOT_KINDS:
            raise ValueError("snapshot resource version kind unresolved")
        if source.get("rights_scope") not in {"redistributable", "reference-only"}:
            raise ValueError("snapshot resource rights scope unresolved")
        if source["rights_scope"] == "reference-only" and mode != "metadata-only-reference":
            raise ValueError("reference-only snapshot cannot package source content")
        expected_redistribution = ("reference-only" if source["rights_scope"] == "reference-only"
                                   else "permitted-with-notices")
        if source["redistribution"] != expected_redistribution:
            raise ValueError("snapshot redistribution does not match rights scope")
        if mode == "verbatim-upstream":
            if source.get("upstream_sha256") != source["sha256"]:
                raise ValueError("verbatim snapshot artifact and upstream hashes differ")
        else:
            upstreams = source.get("upstream_sha256s", [])
            if not upstreams or source.get("upstream_sha256") not in upstreams:
                raise ValueError("normalized snapshot upstream hashes are incomplete")
            lineage_hashes = set()
            for lineage in source.get("lineage", []):
                upstream_hash = lineage.get("upstream_sha256", lineage.get("sha256"))
                lineage_hashes.add(upstream_hash)
            if set(upstreams) - lineage_hashes:
                raise ValueError("normalized snapshot lineage is missing an upstream hash")
            if mode == "metadata-only-reference" and source["rights_scope"] != "reference-only":
                raise ValueError("metadata-only reference must remain reference-only")
        if not source.get("retrieved_at") or not source.get("retrieval_timezone"):
            raise ValueError("snapshot retrieval timestamp is incomplete")
    else:
        raise ValueError("unknown resource source kind")
    for dependency in resource["requires"]:
        member(root, dependency)
    for path_key, hash_key in [("license_path", "license_sha256"), ("notice_path", "notice_sha256")]:
        if source[path_key]:
            _verified_bytes(root, source[path_key], source[hash_key], "resource license/attribution drift", reader)
    for lineage in source.get("lineage", []):
        if lineage.get("path"):
            if lineage["path"] not in resource["requires"]:
                raise ValueError("lineage path is not an explicit resource dependency")
            _verified_bytes(root, lineage["path"], lineage["sha256"], "resource lineage drift", reader)
    data = _verified_bytes(root, resource["path"], source["sha256"],
                           "resource hash differs from reviewed source", reader)
    return data


def _source_provenance(resource, source, locator, record_hash, transform):
    if resource["source_kind"] == "owned-reference":
        return {**resource["owned_provenance"], "resource_id": resource["resource_id"], "record_sha256": record_hash,
                "transformation": transform, "limitations": resource.get("limitations", [])}
    upstreams = source.get("upstream_sha256s", [source.get("upstream_sha256", source["sha256"])])
    return {
        "resource_id": resource["resource_id"],
        "repository": source["repository"],
        "version": source["version"],
        "version_kind": source.get("version_kind", "git-commit"),
        "source_path": source["upstream_path"],
        "source_locator": locator,
        "source_sha256": source["sha256"],
        "upstream_sha256": source.get("upstream_sha256", upstreams[0]),
        "upstream_sha256s": upstreams,
        "artifact_sha256": source["sha256"],
        "copied_vs_reauthored": resource.get("copied_vs_reauthored", "verbatim-upstream"),
        "as_of": source["as_of"],
        "retrieved_at": source.get("retrieved_at"),
        "retrieval_timezone": source.get("retrieval_timezone"),
        "license": source["license"],
        "rights_scope": source.get("rights_scope", "redistributable"),
        "redistribution": source["redistribution"],
        "record_sha256": record_hash,
        "lineage": source.get("lineage", []),
        "transformation": transform,
        "limitations": resource.get("limitations", []),
    }


def _record(resource, source, identity, content, locator, transform):
    encoded = json.dumps(content, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    record_hash = digest(encoded)
    return {"record_id": identity, "content": content, "record_sha256": record_hash,
            "provenance": _source_provenance(resource, source, locator, record_hash, transform)}


def _base_result(resource_id, consumer, query, domain, locale, genre):
    return {"schema_version": 2, "status": "no-applicable-record", "resource_id": resource_id,
            "consumer": consumer, "resource_read": False, "query": query, "domain": domain,
            "locale": locale, "genre": genre, "records": [], "warnings": [],
            "policy_applicability": "unverified", "evidence_class": "resource-read-observation",
            "human_acceptance": "not-evaluated"}


def _jsonl_records(resource, source, data, query, reader=None):
    try:
        rows = [(reader.parse(line) if reader else strict_json(line)) for line in data.decode("utf-8-sig").splitlines() if line.strip()]
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("JSONL snapshot is not valid UTF-8 JSONL") from error
    records = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError("JSONL snapshot contains a non-object record")
        if resource.get("copied_vs_reauthored") == "metadata-only-reference":
            if set(row) - TASK_METADATA_KEYS:
                raise ValueError("metadata-only reference contains unreviewed/private fields")
            stack = [row]
            while stack:
                value = stack.pop()
                if isinstance(value, dict):
                    if PRIVATE_SWE_KEYS.intersection(value):
                        raise ValueError("metadata-only reference contains private fields")
                    stack.extend(value.values())
                elif isinstance(value, list):
                    stack.extend(value)
        if row.get("actual_passage") is False:
            continue
        haystack = json.dumps(row, ensure_ascii=False, sort_keys=True).casefold()
        if query.strip() and not all(token.casefold() in haystack for token in query.split()):
            continue
        identity = str(row.get("source_id") or row.get("id") or index)
        locator = row.get("locator", source["upstream_path"])
        records.append(_record(resource, source, identity, row, locator,
                               "JSONL-record-selection; catalog rows with actual_passage=false are excluded"))
    return records


def lookup(resource_id, consumer, *, query="", domain, locale="en", genre,
           study_design=None, protocol=False, ai=False, llm=False, venue=None, stage=None,
           year=None, track=None, article_type=None, resource_access="on", root=ROOT, limits=None):
    if resource_access == "off":
        result = {"schema_version": 2, "status": "resource-disabled", "resource_id": resource_id,
                "consumer": consumer, "resource_read": False, "records": [],
                "evidence_class": "resource-access-treatment", "human_acceptance": "not-evaluated"}
        ArtifactReader(root, limits).output(result)
        return result
    if resource_access != "on":
        raise ValueError("unknown resource treatment")
    if len(query.encode("utf-8")) > 4096 or len(query.casefold().split()) > 64:
        raise ValueError("selector query exceeds trusted token/byte limits")
    member(root, "core/registry/catalog/resources.json")
    reader = ArtifactReader(root, limits)
    skills = validate_record("catalog", reader.json("core/registry/catalog/skills.json"))["skills"]
    identities = [row["id"] for row in skills]
    if len(identities) != len(set(identities)) or consumer not in identities:
        raise ValueError("resource consumer is absent from current exact catalog")
    catalog = validate_record("resource-registry", reader.json("core/registry/catalog/resources.json"))
    selected = [row for row in catalog["resources"] if row["resource_id"] == resource_id]
    if len(selected) != 1:
        raise ValueError("resource ID missing or duplicated")
    resource = selected[0]
    if consumer not in resource["consumers"]:
        raise ValueError("resource belongs to a different consumer")
    if locale != resource["locale"] or genre != resource["genre"]:
        raise ValueError("resource locale/genre mismatch")
    result = _base_result(resource_id, consumer, query, domain, locale, genre)
    result["warnings"] = ["Snapshot/reference lookup only; semantic support, current policy and human acceptance are not certified.",
                           *resource.get("limitations", [])]
    if domain != resource["domain"]:
        result["warnings"].append("No applicable record for this domain.")
        reader.output(result)
        return result
    source = resource["source"]
    data = _verify_source(resource, root, reader)
    result.update({"resource_read": True, "resource_sha256": digest(data),
                   "reader_sha256": digest(Path(__file__).read_bytes()),
                   "context": {"venue": venue, "stage": stage, "year": year, "track": track,
                               "article_type": article_type}})
    if resource["source_kind"] == "owned-reference":
        rows = read_pack(resource, root, reader=reader)
        tokens = query.casefold().split()
        result["records"] = [_record(resource, source, row["id"], row, row["id"], "typed-authored-reference-selection")
            for row in rows if consumer in row["consumer"] and all(token in json.dumps(row, sort_keys=True).casefold() for token in tokens)]
    elif resource_id == "R-reporting-lookup":
        text = data.decode("utf-8-sig")
        records = strict_json(text)["guidelines"]
        rows = [(row["id"], row) for row in records
                if (study_design in row["study_designs"] and row["protocol"] == protocol
                    and (not row["conditions"].get("ai") or ai)
                    and (not row["conditions"].get("llm") or llm))]
        result["warnings"].append("Clinical/health study-design registry; it does not impose reporting guidance on generic CS work.")
        result["records"] = [_record(resource, source, identity, row, identity,
                                       "JSON-guideline-row-selection") for identity, row in rows]
    elif resource_id == "R-publisher-profile":
        if not all([venue, stage, year, track, article_type]):
            raise ValueError("publisher lookup requires venue/year/track/article-type/stage")
        profiles = strict_json(data.decode("utf-8-sig"))["profiles"]
        row = profiles.get(venue)
        rows = [(venue, row)] if row and row["phase"] == stage else []
        result["warnings"].append("Exact venue/year/track/article-type applicability is unverified; publisher-wide snapshots require target-journal review.")
        if row and row["phase"] == stage and row["source_status"] != "reviewed":
            result["warnings"].append(row["source_status"])
        result["records"] = [_record(resource, source, identity, row, identity,
                                       "JSON-publisher-profile-stage-selection") for identity, row in rows]
    elif resource_id == "R-ui-lookup":
        if not query.strip():
            raise ValueError("UI lookup requires a bounded nonempty query")
        records = list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))
        tokens = query.casefold().split()
        rows = [(row["No"], row) for row in records if all(token in json.dumps(row).casefold() for token in tokens)]
        result["warnings"].append("UI heuristics and code examples are untrusted reference data; examples are never executed.")
        result["records"] = [_record(resource, source, identity, row, "No=" + identity,
                                       "CSV-row-token-selection") for identity, row in rows]
    elif resource_id == "R-nature-reference":
        content = {"text": data.decode("utf-8-sig")}
        result["records"] = [_record(resource, source, "language/en", content, "language/en",
                                       "UTF-8-markdown-read")]
        result["warnings"].append("Optional English writing advice; no compulsory sentence length, punctuation rule or universal venue policy. This is not a prose corpus or human gold.")
    elif resource["format"] == "jsonl":
        result["records"] = _jsonl_records(resource, source, data, query, reader)
    else:
        raise ValueError("resource has no reviewed reader")
    result["status"] = "matched" if result["records"] else "no-applicable-record"
    reader.output(result)
    return result


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resource-id", required=True)
    parser.add_argument("--consumer", required=True)
    parser.add_argument("--query", default="")
    parser.add_argument("--domain", required=True)
    parser.add_argument("--locale", default="en")
    parser.add_argument("--genre", required=True)
    parser.add_argument("--resource-access", choices=["on", "off"], default="on")
    parser.add_argument("--study-design")
    parser.add_argument("--protocol", action="store_true")
    parser.add_argument("--ai", action="store_true")
    parser.add_argument("--llm", action="store_true")
    for name in ["venue", "stage", "year", "track", "article-type"]:
        parser.add_argument("--" + name)
    parser.add_argument("--json", action="store_true")
    args = vars(parser.parse_args())
    args.pop("json")
    try:
        result = lookup(**args)
        sys.stdout.write(ArtifactReader(ROOT).output(result, newline=True).decode("utf-8"))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({"status": "fail", "error": str(error), "resource_read": False}, ensure_ascii=False), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())

