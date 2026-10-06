"""Record current consumer contracts, protected bytes and package privacy boundary."""
import hashlib
import json
from pathlib import Path
import re
import sys

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
KIT = WORK / "nckh-kit"
sys.path.insert(0, str(KIT))
from core.build import APPROVED_IDENTITIES, LINK, reference_path, source_members, SCRIPT_REQUIREMENTS
from core.resources import registry

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(name, record):
    with (RUN / name).open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(record, indent=2) + "\n")

baseline = json.loads((RUN / "baseline.json").read_text(encoding="utf-8-sig"))
catalog = json.loads((KIT / "core/registry/catalog/skills.json").read_text(encoding="utf-8-sig"))
assert {row["id"] for row in catalog["skills"]} == APPROVED_IDENTITIES
assert APPROVED_IDENTITIES == set(baseline["approved_baseline_identities"]) | {"nckh-dataset", "nckh-statistics", "nckh-telemetry", "nckh-aiops"}
base_cases = {}
for path in (KIT / "evals/cases").glob("*/*.json"):
    record = json.loads(path.read_text(encoding="utf-8-sig"))
    if "skill_id" in record:
        base_cases[record["skill_id"]] = {row["id"] for row in record["cases"]}
assert len(base_cases) == 43 and sum(map(len, base_cases.values())) == 172
assert all(base_cases[identity] == {identity + ":" + kind for kind in ("positive", "negative", "outcome", "failure")} for identity in APPROVED_IDENTITIES)
resources = registry(KIT)
members = source_members(KIT)
assert not any(name.startswith(("plans/", "pilot-data/", "pilot-output/")) for name in members)
surfaces = ["core/build.py", "core/evaluation.py", "core/acceptance.py", "core/resources.py", "core/owned_resources.py",
    "core/research_io.py", "scripts/search-resource.py", "scripts/resource-smoke.py", "scripts/check-research-artifacts.py",
    "tests/release/test_qualification.py", "tests/acceptance/test_profile.py", "installer/schemas/bundle-v2.schema.json",
    "core/contracts/catalog.schema.json", "core/contracts/resource-registry.schema.json"]
inventory = []
pattern = re.compile(r"APPROVED_IDENTITIES|\b(?:43|172|39|156)\b|owned-reference|copied-upstream|retrieved-snapshot|SCRIPT_REQUIREMENTS|receipt_outputs|validate_research_matrix")
for name in surfaces:
    path = KIT / name
    hits = [{"line": number, "text": line.strip()} for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1) if pattern.search(line)]
    inventory.append({"path": name, "sha256": digest(path), "matches": hits})
archived = WORK / "github-publication/nckh-kit/scripts/verify-public-package.py"
save("migration-inventory.json", {"identities": 43, "base_cases": 172, "supplemental_domain_scenarios": 12,
    "resource_groups": len(resources["resources"]), "resource_consumer_bindings": sum(len(row["consumers"]) for row in resources["resources"]),
    "current_consumers": inventory, "script_helper_closures": SCRIPT_REQUIREMENTS,
    "archived_public_verifier": {"path": str(archived), "sha256": digest(archived), "disposition": "Archived r38 publication snapshot; not current candidate authority; unchanged, no publication authorized"},
    "privacy": "Current explicit source inventory excludes run/raw/pilot/private artifact paths; packs contain authored references and existing bounded source projections only"})
protected = json.loads((RUN / "protected-hashes.json").read_text(encoding="utf-8-sig"))
results = []
for group, values in protected.items():
    if not isinstance(values, dict): continue
    for name, expected in values.items():
        path = KIT / name if group == "source" else KIT / "core/registry/source-lock/history" / name if group == "historical_lock_hashes" else Path(name)
        if not path.is_absolute(): path = WORK / name
        assert digest(path) == expected, str(path)
        results.append({"path": str(path), "sha256": expected})
assert digest(WORK / ".nckh-state/ownership.json") == protected["ownership_file_sha256"]
save("p7-protected-check-01.json", {"checked": len(results) + 1, "mismatches": 0, "files": results, "ownership_unchanged": True})
links = []
for name in ["docs/index.md", "docs/research-and-writing.md", "docs/engineer.md", "docs/qualification.md", "docs/migration.md", "docs/contracts.md"]:
    for href in LINK.findall((KIT / name).read_text(encoding="utf-8-sig")):
        target = reference_path(KIT, KIT / name, href)
        if target is not None:
            assert target.is_file(), (name, href)
            links.append({"from": name, "to": target.relative_to(KIT).as_posix()})
save("p7-doc-link-check-01.json", {"links": links, "checked": len(links), "mismatches": 0})
print(json.dumps({"identities": 43, "cases": 172, "resources": len(resources["resources"]), "protected": len(results), "links": len(links)}))
