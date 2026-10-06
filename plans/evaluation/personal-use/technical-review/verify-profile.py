"""Bounded read-only acceptance/package review; output is review evidence."""

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import sys

WORK = Path(__file__).resolve().parents[4]
ROOT = WORK / "nckh-kit"
OUT = Path(__file__).resolve().parent
LABEL = sys.argv[1] if len(sys.argv) > 1 else "initial"
if LABEL not in {"initial", "final"}:
    raise ValueError("snapshot label must be initial or final")
sys.path.insert(0, str(ROOT))

from core.acceptance import _load_json, load_profile, validate_profile
from core.build import LINK, closure, load_json, reference_path
from core.native import ROLES
from core.schema import ContractError


def rejected(call):
    try:
        call()
    except Exception as error:
        return {"rejected": True, "error_type": type(error).__name__, "error": str(error)}
    return {"rejected": False}


profile = load_profile(ROOT)
catalog = load_json(ROOT / "core/registry/catalog/skills.json")
result = {
    "scope": "deterministic local acceptance/package review only",
    "catalog_identities": len(catalog["skills"]),
    "profile_identities": len(profile["skills"]),
    "source_definitions": len(profile["sources"]),
    "source_urls": sum(len(source["urls"]) for source in profile["sources"].values()),
    "unique_source_urls": len({url for source in profile["sources"].values() for url in source["urls"]}),
    "exact_ids": set(profile["skills"]) == {row["id"] for row in catalog["skills"]},
    "undefined_references": sorted({source for row in profile["skills"].values() for source in row["source_ids"]} - set(profile["sources"])),
    "skills": [],
    "native_roles": [],
}

for entry in catalog["skills"]:
    source_dir = ROOT / entry["path"]
    members = closure(ROOT, [source_dir / "SKILL.md"])
    mapping = {p: Path("skills") / entry["id"] / (p.relative_to(source_dir) if p.is_relative_to(source_dir) else Path("references/_shared") / p.relative_to(ROOT)) for p in members}
    projected = {value.as_posix() for value in mapping.values()}
    link_errors = []
    for source in members:
        if source.suffix != ".md":
            continue
        for href in LINK.findall(source.read_text(encoding="utf-8")):
            target = reference_path(ROOT, source, href)
            if target is None:
                continue
            relative = os.path.relpath(mapping[target], mapping[source].parent).replace(os.sep, "/")
            resolved = Path(os.path.normpath(mapping[source].parent / relative)).as_posix()
            if resolved not in projected:
                link_errors.append({"source": source.relative_to(ROOT).as_posix(), "href": href})
    result["skills"].append({
        "id": entry["id"],
        "contains_acceptance_profile": ROOT / "core/profiles/acceptance/personal-use.json" in members,
        "simulated_projection_link_errors": link_errors,
    })

for role in ROLES:
    source = ROOT / f"agents/{role}.md"
    members = closure(ROOT, [source])
    sections = [source, *(path for path in members if path != source)]
    instructions = "\n\n".join(LINK.sub(lambda match: match.group(0).split("](", 1)[0] + "]", path.read_text(encoding="utf-8")) for path in sections)
    result["native_roles"].append({
        "role": role,
        "closure": [path.relative_to(ROOT).as_posix() for path in members],
        "contains_acceptance_profile": ROOT / "core/profiles/acceptance/personal-use.json" in members,
        "markdown_link_targets_remaining_after_flattening": LINK.findall(instructions),
    })

duplicate = OUT / "duplicate-profile.fixture.json"
duplicate.write_text((ROOT / "core/profiles/acceptance/personal-use.json").read_text(encoding="utf-8").replace('"schema_version": 1,', '"schema_version": 999,\n  "schema_version": 1,', 1), encoding="utf-8")
result["duplicate_key_acceptance_reader"] = rejected(lambda: validate_profile(_load_json(duplicate), catalog=catalog))
result["duplicate_key_existing_reader"] = rejected(lambda: load_json(duplicate))
boolean_version = deepcopy(profile)
boolean_version["schema_version"] = True
result["boolean_profile_schema_version"] = rejected(lambda: validate_profile(boolean_version, catalog=catalog))

paths = [
    "core/profiles/acceptance/personal-use.json", "core/acceptance.py",
    "core/policies/acceptance-policy.md", "core/workflows/execution.md",
    "skills/core/nckh-cook/SKILL.md", "tests/acceptance/test_profile.py",
    "core/state.py", "core/build.py", "core/schema.py", "docs/personal-use.md",
    "evals/protocols/qualification.json", "core/registry/catalog/skills.json",
]
result["source_sha256"] = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in paths}
(OUT / ("profile-review.json" if LABEL == "initial" else "profile-review-final.json")).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: value for key, value in result.items() if key not in {"source_sha256", "skills", "native_roles"}}, indent=2))
print(f"skill closure/projected links: {len(result['skills'])}; profile present: {sum(row['contains_acceptance_profile'] for row in result['skills'])}; link errors: {sum(len(row['simulated_projection_link_errors']) for row in result['skills'])}")
print(f"native role closures: {len(result['native_roles'])}; profile present: {sum(row['contains_acceptance_profile'] for row in result['native_roles'])}; remaining markdown links: {sum(len(row['markdown_link_targets_remaining_after_flattening']) for row in result['native_roles'])}")
