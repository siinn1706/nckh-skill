"""Prove consumer reads vs catalog rows whose bytes are not in the skill bundle."""

import json
import subprocess
import sys
from pathlib import Path

repo = Path(r"C:/Users/USER\Downloads\test-skill")
kit = repo / "nckh-kit"
reader = kit / "scripts" / "search-resource.py"
catalog = json.loads((kit / "core" / "registry" / "catalog" / "resources.json").read_text(encoding="utf-8"))

def run(script, row, consumer):
    command = [sys.executable, "-I", str(script), "--resource-id", row["resource_id"], "--consumer", consumer,
               "--domain", row["domain"], "--locale", row["locale"], "--genre", row["genre"], "--query", "a", "--json"]
    if row["resource_id"] == "R-reporting-lookup":
        command.extend(["--study-design", "randomized_trial"])
    elif row["resource_id"] == "R-publisher-profile":
        command.extend(["--venue", "science", "--stage", "revised", "--year", "2026", "--track", "journal", "--article-type", "research"])
    elif row["resource_id"] == "R-ui-lookup":
        command.extend(["--query", "keyboard navigation"])
    process = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=60)
    detail = (process.stderr or process.stdout or "").strip().replace("\n", " ")
    return process.returncode, detail[:400]

print("SOURCE")
for row in catalog["resources"]:
    code, detail = run(reader, row, row["consumers"][0])
    print(f"{row['resource_id']} consumer={row['consumers'][0]} exit={code} {detail[:220]}")

print("INSTALLED ANALYTICS UNBUNDLED REPORTING")
analytics = repo / ".agents" / "skills" / "nckh-analytics" / "references" / "_shared" / "scripts" / "search-resource.py"
reporting = next(row for row in catalog["resources"] if row["resource_id"] == "R-reporting-lookup")
uci = next(row for row in catalog["resources"] if row["resource_id"] == "R-uci-bank-marketing")
# installed catalog may not include owned resources; use its own catalog rows
local = json.loads((analytics.parents[1] / "core" / "registry" / "catalog" / "resources.json").read_text(encoding="utf-8"))
local_reporting = next(row for row in local["resources"] if row["resource_id"] == "R-reporting-lookup")
local_uci = next(row for row in local["resources"] if row["resource_id"] == "R-uci-bank-marketing")
print("reporting", run(analytics, local_reporting, "nckh-method"))
print("uci", run(analytics, local_uci, "nckh-analytics"))

print("INSTALLED METHOD OWNED RESOURCE ABSENT FROM ITS CATALOG")
method = repo / ".agents" / "skills" / "nckh-method" / "references" / "_shared" / "scripts" / "search-resource.py"
stats = next(row for row in catalog["resources"] if row["resource_id"] == "R-statistical-recipes")
print("stats-via-installed-method", run(method, stats, "nckh-method"))
print("stats-via-source", run(reader, stats, "nckh-statistics"))
