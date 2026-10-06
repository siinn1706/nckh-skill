"""Observe actual resource reads from a verified extracted package in isolation."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core.build import verify_bundle
from core.paths import atomic_json, contained, digest_bytes, digest_record, no_links
from core.schema import ContractError


CONTEXTS = {
    "R-ui-lookup": ["--domain", "ui", "--genre", "ui-heuristic", "--query", "keyboard navigation"],
    "R-reporting-lookup": ["--domain", "clinical-health", "--genre", "reporting-reference", "--study-design", "randomized_trial"],
    "R-publisher-profile": ["--domain", "publication-planning", "--genre", "publisher-profile", "--venue", "science", "--stage", "revised", "--year", "2026", "--track", "journal", "--article-type", "research"],
    "R-nature-reference": ["--domain", "scientific-writing", "--genre", "writing-advice"],
}


def smoke(bundle, cwd):
    bundle, cwd = no_links(bundle), no_links(cwd)
    repository_root = ROOT.parent if (ROOT.parent / "plans").is_dir() else ROOT
    if (not cwd.is_dir() or cwd.resolve().is_relative_to(repository_root.resolve())
            or cwd.resolve().is_relative_to(bundle.resolve())):
        raise ContractError("smoke CWD must be an existing directory outside the repository")
    manifest = verify_bundle(bundle)
    if manifest["schema_version"] != 2:
        raise ContractError("resource smoke requires a versioned resource bundle")
    observations = []
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)
    environment.pop("NCKH_RESOURCE_TEST_ROOT", None)
    for resource in manifest["resources"]:
        context = CONTEXTS.get(resource["resource_id"])
        if context is None:
            registry_path = next((path for path in resource["requires"]
                                  if path.endswith("core/registry/catalog/resources.json")), None)
            if registry_path is None:
                raise ContractError("selected resource has no pinned registry context")
            catalog = json.loads(contained(bundle, registry_path).read_text(encoding="utf-8"))
            row = next((item for item in catalog["resources"]
                        if item["resource_id"] == resource["resource_id"]), None)
            if row is None or row["format"] != "jsonl" or row["source_kind"] not in {"retrieved-snapshot", "owned-reference"}:
                raise ContractError("selected resource has no reviewed smoke context")
            context = ["--domain", row["domain"], "--genre", row["genre"], "--locale", row["locale"]]
        else:
            context = [*context, "--locale", "en"]
        command = [sys.executable, "-I", str(contained(bundle, resource["reader"])),
                   "--resource-id", resource["resource_id"], "--consumer", resource["consumer"],
                   *context, "--json"]
        process = subprocess.run(command, cwd=cwd, env=environment, capture_output=True,
                                 text=True, encoding="utf-8", timeout=30)
        if process.returncode:
            raise ContractError("extracted resource reader failed: " + process.stderr)
        result = json.loads(process.stdout)
        if not result["resource_read"] or not result["records"] or result["resource_sha256"] != resource["source_sha256"]:
            raise ContractError("extracted consumer did not read the expected pinned resource")
        observations.append({"resource_id": resource["resource_id"], "consumer": resource["consumer"],
                             "resource_sha256": result["resource_sha256"], "reader_sha256": result["reader_sha256"],
                             "record_ids": [r["record_id"] for r in result["records"]], "exit_status": process.returncode,
                             "output_sha256": digest_bytes(process.stdout.encode("utf-8")), "resource_read": True})
    if manifest["resource_access"] == "on" and not observations:
        raise ContractError("zero resource readers discovered in enabled smoke")
    return {"schema_version": 1, "status": "pass", "evidence_class": "extracted-resource-read",
            "bundle_manifest_hash": digest_record(manifest), "source_lock_hash": manifest["source_lock_hash"],
            "closure_hash": manifest["closure_hash"], "resource_access": manifest["resource_access"],
            "outside_repo_cwd": True, "python_isolated": True, "pythonpath_unset": True,
            "observations": observations, "human_acceptance": "not-evaluated", "qualification": "pending"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument("--unset-pythonpath", action="store_true", help="PYTHONPATH is always removed for consumer subprocesses.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = smoke(args.bundle, args.cwd)
    except (ContractError, ValueError, OSError, KeyError, subprocess.TimeoutExpired) as error:
        result = {"schema_version": 1, "status": "timeout-unknown" if isinstance(error, subprocess.TimeoutExpired) else "fail",
                  "evidence_class": "extracted-resource-read", "error": str(error), "qualification": "pending"}
    if args.output:
        atomic_json(args.output, result)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "pass" else 3


if __name__ == "__main__":
    sys.exit(main())
