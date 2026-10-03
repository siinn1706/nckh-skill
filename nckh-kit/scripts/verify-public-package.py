"""Verify the public instruction packages without installing or invoking models."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.build import load_json, verify_bundle
from core.schema import ContractError


def main():
    catalog = load_json(ROOT / "core/registry/catalog/skills.json")
    expected = {row["id"] for row in catalog["skills"]}
    if len(expected) != 37:
        raise ContractError("public catalog must contain 37 unique skills")
    summaries = []
    for host in ("claude", "codex", "cursor", "agy"):
        bundle = ROOT.parent / "packages" / host
        manifest = verify_bundle(bundle)
        if manifest["host"] != host or manifest.get("resource_access") != "on":
            raise ContractError("unexpected public package host/resource mode")
        registry_record = next(
            (record for record in manifest["files"]
             if record["source_path"] == "core/registry/catalog/resources.json"), None
        )
        if registry_record is None:
            raise ContractError("enabled public package has no resource registry")
        registry = load_json(bundle / registry_record["path"])
        declared = {(row["resource_id"], consumer)
                    for row in registry["resources"] if row["dependency"] == "required"
                    for consumer in row["consumers"] if consumer in expected}
        actual = {(row["resource_id"], row["consumer"])
                  for row in manifest["resources"]}
        resource_ids = {row["resource_id"] for row in manifest["resources"]}
        if actual != declared or len(resource_ids) != 9:
            raise ContractError("enabled public resource inventory differs from registry")
        if {row["id"] for row in manifest["skills"]} != expected:
            raise ContractError("public package skill inventory differs from catalog")
        if load_json(bundle / "source-lock.json")["revision"] != "26":
            raise ContractError("unexpected public source revision")
        summaries.append({"host": host, "skills": len(expected),
                          "agents": len(manifest["agents"]), "resource_access": "on",
                          "resource_types": len(resource_ids), "resource_bindings": len(actual),
                          "closure_hash": manifest["closure_hash"]})
    print(json.dumps({"status": "pass", "packages": summaries}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ContractError, OSError, ValueError, KeyError) as error:
        print(json.dumps({"status": "fail", "error": str(error)}), file=sys.stderr)
        sys.exit(1)
