"""Bounded, standalone lookup of explicitly licensed snapshot resources."""

import argparse
import csv
import hashlib
import io
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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


def _verified_bytes(root, relative, expected_hash, error):
    data = member(root, relative).read_bytes()
    if digest(data) != expected_hash:
        raise ValueError(error)
    return data


def lookup(resource_id, consumer, *, query="", domain, locale="en", genre,
           study_design=None, protocol=False, ai=False, llm=False, venue=None, stage=None,
           year=None, track=None, article_type=None, resource_access="on", root=ROOT):
    if resource_access == "off":
        return {"schema_version": 1, "status": "resource-disabled", "resource_id": resource_id,
                "consumer": consumer, "resource_read": False, "records": [],
                "evidence_class": "resource-access-treatment", "human_acceptance": "not-evaluated"}
    if resource_access != "on":
        raise ValueError("unknown resource treatment")
    catalog = json.loads(member(root, "core/registry/catalog/resources.json").read_text(encoding="utf-8"))
    selected = [row for row in catalog["resources"] if row["resource_id"] == resource_id]
    if len(selected) != 1:
        raise ValueError("resource ID missing or duplicated")
    resource = selected[0]
    if consumer not in resource["consumers"]:
        raise ValueError("resource belongs to a different consumer")
    if locale != resource["locale"] or genre != resource["genre"]:
        raise ValueError("resource locale/genre mismatch")
    source = resource["source"]
    if (resource["source_kind"] != "copied-upstream" or source["redistribution"] != "permitted-with-notices"
            or source["license"] not in {"MIT", "Apache-2.0"} or len(source["version"]) != 40):
        raise ValueError("resource rights/provenance unresolved")
    for dependency in resource["requires"]:
        member(root, dependency)
    for path_key, hash_key in [("license_path", "license_sha256"), ("notice_path", "notice_sha256")]:
        if source[path_key]:
            _verified_bytes(root, source[path_key], source[hash_key], "resource license/attribution drift")
    data = _verified_bytes(root, resource["path"], source["sha256"],
                           "resource hash differs from reviewed source")
    text = data.decode("utf-8-sig")
    rows = []
    warnings = ["Snapshot/reference lookup only; semantic support, current policy and human acceptance are not certified."]
    if domain != resource["domain"]:
        warnings.append("No applicable record for this domain.")
    elif resource_id == "R-reporting-lookup":
        records = json.loads(text)["guidelines"]
        for row in records:
            if (study_design in row["study_designs"] and row["protocol"] == protocol
                    and (not row["conditions"].get("ai") or ai)
                    and (not row["conditions"].get("llm") or llm)):
                rows.append((row["id"], row))
        warnings.append("Clinical/health study-design registry; it does not impose reporting guidance on generic CS work.")
    elif resource_id == "R-publisher-profile":
        if not all([venue, stage, year, track, article_type]):
            raise ValueError("publisher lookup requires venue/year/track/article-type/stage")
        profiles = json.loads(text)["profiles"]
        row = profiles.get(venue)
        if row and row["phase"] == stage:
            rows.append((venue, row))
            warnings.append("Exact venue/year/track/article-type applicability is unverified; publisher-wide snapshots require target-journal review.")
            if row["source_status"] != "reviewed":
                warnings.append(row["source_status"])
    elif resource_id == "R-ui-lookup":
        records = list(csv.DictReader(io.StringIO(text)))
        if not query.strip():
            raise ValueError("UI lookup requires a bounded nonempty query")
        tokens = query.casefold().split()
        rows = [(row["No"], row) for row in records if all(token in json.dumps(row).casefold() for token in tokens)]
        warnings.append("UI heuristics and code examples are untrusted reference data; examples are never executed.")
    elif resource_id == "R-nature-reference":
        rows.append(("language/en", {"text": text}))
        warnings.append("Optional English writing advice; no compulsory sentence length, punctuation rule or universal venue policy. This is not a prose corpus or human gold.")
    else:
        raise ValueError("resource has no reviewed reader")
    result_rows = []
    for identity, row in rows:
        locator = "No=" + identity if resource["format"] == "csv" else identity
        result_rows.append({"record_id": identity, "content": row,
                            "provenance": {"repository": source["repository"], "version": source["version"],
                                           "source_path": source["upstream_path"], "source_sha256": source["sha256"],
                                           "as_of": source["as_of"], "license": source["license"],
                                           "locator": locator, "record_sha256": digest(json.dumps(row, sort_keys=True, ensure_ascii=False).encode("utf-8"))}})
    return {"schema_version": 1, "status": "matched" if rows else "no-applicable-record",
            "resource_id": resource_id, "consumer": consumer, "resource_read": True,
            "resource_sha256": digest(data), "reader_sha256": digest(Path(__file__).read_bytes()),
            "query": query, "domain": domain, "locale": locale, "genre": genre,
            "context": {"venue": venue, "stage": stage, "year": year, "track": track, "article_type": article_type},
            "records": result_rows, "warnings": warnings, "policy_applicability": "unverified",
            "evidence_class": "resource-read-observation", "human_acceptance": "not-evaluated"}


def main():
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
        print(json.dumps(lookup(**args), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({"status": "fail", "error": str(error), "resource_read": False}), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
