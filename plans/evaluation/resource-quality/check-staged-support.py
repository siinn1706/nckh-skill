"""Check selected consumers and packaging support before source promotion."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "nckh-kit"
EVIDENCE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from core.build import freeze_sources, source_members
from core.paths import atomic_json, digest_bytes, digest_record, temporary_tree

payload = EVIDENCE / "staging/payload"
environment = dict(os.environ)
environment.pop("PYTHONPATH", None)
requests = [
    ["--resource-id", "R-ui-lookup", "--consumer", "nckh-frontend", "--domain", "ui", "--genre", "ui-heuristic", "--query", "keyboard navigation"],
    ["--resource-id", "R-reporting-lookup", "--consumer", "nckh-method", "--domain", "clinical-health", "--genre", "reporting-reference", "--study-design", "randomized_trial"],
    ["--resource-id", "R-publisher-profile", "--consumer", "nckh-visuals", "--domain", "publication-planning", "--genre", "publisher-profile", "--venue", "science", "--stage", "revised", "--year", "2026", "--track", "journal", "--article-type", "research"],
    ["--resource-id", "R-nature-reference", "--consumer", "nckh-write", "--domain", "scientific-writing", "--genre", "writing-advice"],
]
import json
observations = []
with temporary_tree() as outside:
    for arguments in requests:
        command = [sys.executable, "-I", str(payload / "scripts/search-resource.py"), *arguments, "--json"]
        process = subprocess.run(command, cwd=outside, env=environment, capture_output=True, text=True, encoding="utf-8", timeout=30)
        if process.returncode:
            raise ValueError(process.stderr)
        result = json.loads(process.stdout)
        if not result["resource_read"] or not result["records"]:
            raise ValueError("selected source-level consumer did not read an applicable record")
        atomic_json(EVIDENCE / "staging/reads" / (result["resource_id"] + ".json"), result)
        observations.append({"resource_id": result["resource_id"], "resource_sha256": result["resource_sha256"],
                             "reader_sha256": result["reader_sha256"], "records": [r["record_id"] for r in result["records"]],
                             "output_sha256": digest_bytes(process.stdout.encode("utf-8")), "exit_status": process.returncode,
                             "outside_repo_cwd": True, "python_isolated": True, "pythonpath_unset": True})
atomic_json(EVIDENCE / "staging/consumer-receipt.json", {"schema_version": 1, "evidence_class": "source-level-resource-read",
            "status": "pass", "observations": observations, "human_acceptance": "not-evaluated"})
with temporary_tree() as source:
    for relative in source_members(ROOT) + ["core/registry/source-lock/source-lock.json"]:
        target = source / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    shutil.copytree(payload, source, dirs_exist_ok=True)
    lock = freeze_sources(source)
    environment["NCKH_RESOURCE_TEST_ROOT"] = str(source)
    modules = sys.argv[1:] or ["tests.resource.test_consumers", "tests.resource.test_closure"]
    process = subprocess.run([sys.executable, "-m", "unittest", *modules],
                             cwd=ROOT, env=environment, capture_output=True, text=True, timeout=300)
    receipt = {"schema_version": 1, "evidence_class": "staged-contract-regression", "status": "pass" if process.returncode == 0 else "fail",
               "temporary_source_lock_hash": digest_record(lock), "exit_status": process.returncode,
               "output": process.stdout + process.stderr, "promoted": False, "real_installed_skills_changed": False}
    atomic_json(EVIDENCE / "staging" / ("support-tests-" + digest_record(receipt)[:12] + ".json"), receipt)
    print(receipt["output"])
    sys.exit(process.returncode)
