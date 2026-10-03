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
        if manifest["host"] != host or manifest.get("resource_access") != "off":
            raise ContractError("unexpected public package host/resource mode")
        if manifest.get("resources") or any(
            record["rights"] != "owned-local-package" for record in manifest["files"]
        ):
            raise ContractError("public package includes copied resource content")
        if {row["id"] for row in manifest["skills"]} != expected:
            raise ContractError("public package skill inventory differs from catalog")
        if load_json(bundle / "source-lock.json")["revision"] != "25":
            raise ContractError("unexpected public source revision")
        summaries.append({"host": host, "skills": len(expected),
                          "agents": len(manifest["agents"]), "resource_access": "off",
                          "closure_hash": manifest["closure_hash"]})
    print(json.dumps({"status": "pass", "packages": summaries}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ContractError, OSError, ValueError, KeyError) as error:
        print(json.dumps({"status": "fail", "error": str(error)}), file=sys.stderr)
        sys.exit(1)
