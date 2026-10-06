import json
from collections import defaultdict
from pathlib import Path

repo = Path(r"C:/Users/USER\Downloads\test-skill")
source = json.loads((repo / "nckh-kit" / "core" / "registry" / "catalog" / "resources.json").read_text(encoding="utf-8"))
installed = repo / ".agents" / "skills"
expect = defaultdict(list)
for row in source["resources"]:
    for consumer in row["consumers"]:
        expect[consumer].append(row["resource_id"])

print("source_resources", len(source["resources"]))
print("consumers_not_installed")
installed_names = {path.name for path in installed.iterdir() if path.name.startswith("nckh-")}
for consumer in sorted(expect):
    if consumer not in installed_names:
        print(" ", consumer, expect[consumer])

print("--- installed ---")
for skill in sorted(path for path in installed.iterdir() if path.name.startswith("nckh-")):
    catalog = skill / "references" / "_shared" / "core" / "registry" / "catalog" / "resources.json"
    wanted = expect.get(skill.name, [])
    if not catalog.exists():
        print(skill.name, "NO_CATALOG", "expects", wanted or "none")
        continue
    data = json.loads(catalog.read_text(encoding="utf-8"))
    have = [row["resource_id"] for row in data["resources"]]
    missing = [item for item in wanted if item not in have]
    print(skill.name, "catalog", have, "missing_for_consumer", missing)
