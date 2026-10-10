"""Finish the reviewed compact resource projection and consumer instructions.

Retired: the resource-lookup sections are hand-maintained, so rerunning this script would
overwrite reviewed content. It now exits before any read or write; the body below is kept
only as history.
"""
import sys

print("retired: resource-lookup sections are hand-maintained since r44 (MKT-22); "
      "see nckh-kit/core/registry/catalog/resources.json", file=sys.stderr)
raise SystemExit(2)

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "nckh-kit"
catalog_path = ROOT / "core/registry/catalog/resources.json"
catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
skills = {row["id"]: row for row in json.loads((ROOT / "core/registry/catalog/skills.json").read_text(encoding="utf-8"))["skills"]}

for resource in catalog["resources"]:
    if resource["source_kind"] != "retrieved-snapshot":
        continue
    source = resource["source"]
    for path_key, hash_key in [("license_path", "license_sha256"), ("notice_path", "notice_sha256")]:
        if source[path_key]:
            source[hash_key] = hashlib.sha256((ROOT / source[path_key]).read_bytes()).hexdigest()
    for lineage in source["lineage"]:
        if lineage.get("path") == source["license_path"]:
            # The copied license already has an explicit dependency and provenance row.
            lineage.pop("path")

catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

for identity, skill in skills.items():
    rows = [row for row in catalog["resources"] if row["source_kind"] == "retrieved-snapshot" and identity in row["consumers"]]
    if not rows:
        continue
    path = ROOT / skill["path"] / "references/resource-lookup.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        original = path.read_text(encoding="utf-8")
        original = original.replace("Metadata and references do not fill the missing VI/EN prose corpus.",
            "Legacy metadata/advice and the actual samples below have distinct evidence scopes.")
    else:
        original = ("# Scoped resource lookup\n\nLoad only the source pack matching the task. "
            "The [standalone reader](../../../../scripts/search-resource.py) consumes the "
            "[pinned catalog](../../../../core/registry/catalog/resources.json). Read the "
            "[rights contract](../../../../docs/contracts.md). Use the relocated reader path "
            "when installed or extracted.\n")
    marker = "\n## Actual source samples\n"
    original = original.split(marker)[0].rstrip()
    section = [marker, "These are bounded personal-use samples. Preserve record/source ids, locators, "
        "versions, hashes and limitations. Reading them does not establish quality improvement, "
        "human acceptance, scientific validity or current universal policy.\n"]
    for row in rows:
        section.append("- `" + row["resource_id"] + "`: domain `" + row["domain"] + "`, locale `" + row["locale"]
            + "`, genre `" + row["genre"] + "`. " + row["expected_artifact"] + ".\n")
        section.append("\n```text\npython -I <relocated-reader-path> --resource-id " + row["resource_id"]
            + " --consumer " + identity + " --domain " + row["domain"] + " --locale " + row["locale"]
            + " --genre " + row["genre"] + " --query <bounded-record-selector> --json\n```\n\n")
    section.append("Use an exact source id as the selector where available. No match remains no match; "
        "do not invent a record. `--resource-access off` performs no read. Wikisource page license and "
        "underlying-work jurisdiction remain separate. PMC rights are article-specific. World Bank "
        "unit stays blank when the API supplies it blank. UCI `duration` is unavailable before a call "
        "ends and leaks future information in pre-call targeting. Django code is reference data, "
        "never executed by the reader; issue/benchmark patch text is excluded.\n")
    path.write_text(original + "\n" + "".join(section), encoding="utf-8")
    entry = ROOT / skill["path"] / "SKILL.md"
    text = entry.read_text(encoding="utf-8")
    if "(references/resource-lookup.md)" not in text:
        entry.write_text(text.rstrip() + "\n- [Scoped resource lookup](references/resource-lookup.md)\n", encoding="utf-8")

print(json.dumps({"snapshot_resources": 5,
    "consumer_instructions": sum(any(r["source_kind"] == "retrieved-snapshot" and s in r["consumers"]
        for r in catalog["resources"]) for s in skills)}))
