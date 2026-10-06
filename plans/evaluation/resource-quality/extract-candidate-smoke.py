"""Archive/extract actual candidates and observe isolated on/off reader behavior."""

import importlib.util
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[3]
ROOT = PROJECT / "nckh-kit"
OUT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from core.build import verify_bundle, verify_source_lock
from core.paths import atomic_json, digest_bytes, digest_file, digest_record, temporary_tree

spec = importlib.util.spec_from_file_location("resource_smoke", ROOT / "scripts/resource-smoke.py")
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)


def run():
    lock = verify_source_lock(ROOT)
    source_hash = digest_record(lock)
    revision = lock["revision"]
    artifacts = ROOT / ("dist-resource-quality-r" + revision)
    output = OUT / ("extracted-smoke-r" + revision + ".json")
    if output.exists():
        raise ValueError("preserve existing extracted-smoke receipt")
    environment = dict(os.environ, PYTHONIOENCODING="utf-8")
    environment.pop("PYTHONPATH", None)
    environment.pop("NCKH_RESOURCE_TEST_ROOT", None)
    receipt = {"schema_version": 1, "status": "in-progress", "evidence_class": "extracted-on-off-reader-observations",
               "source_revision": revision, "source_lock_hash": source_hash, "bundles": [],
               "accepted_task_count": 0, "human_acceptance": "not-evaluated", "qualification": "pending"}
    atomic_json(output, receipt)
    try:
        for host in ["claude", "codex", "cursor", "agy"]:
            enabled = verify_bundle(artifacts / "on" / host)
            for access in ["on", "off"]:
                bundle = artifacts / access / host
                manifest = verify_bundle(bundle)
                if manifest["source_lock_hash"] != source_hash:
                    raise ValueError("artifact subject changed")
                archive = OUT / "archives" / ("r" + revision + "-" + access + "-" + host + ".zip")
                archive.parent.mkdir(parents=True, exist_ok=True)
                if archive.exists():
                    raise ValueError("preserve existing archive")
                with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as packet:
                    for path in sorted(bundle.rglob("*")):
                        if path.is_file():
                            packet.write(path, path.relative_to(bundle).as_posix())
                with temporary_tree() as extracted, temporary_tree() as outside:
                    with zipfile.ZipFile(archive) as packet:
                        packet.extractall(extracted)
                    observed = smoke.smoke(extracted, outside)
                    disabled_observations = []
                    if access == "off":
                        for resource in enabled["resources"]:
                            command = [sys.executable, "-I", str(extracted / resource["reader"]),
                                       "--resource-id", resource["resource_id"], "--consumer", resource["consumer"],
                                       "--resource-access", "off", *smoke.CONTEXTS[resource["resource_id"]], "--json"]
                            process = subprocess.run(command, cwd=outside, env=environment, capture_output=True, text=True,
                                                     encoding="utf-8", timeout=30)
                            result = json.loads(process.stdout) if process.returncode == 0 else None
                            if not result or result["status"] != "resource-disabled" or result["resource_read"] or result["records"]:
                                raise ValueError("relocated off reader did not stay disabled: " + process.stderr)
                            disabled_observations.append({"resource_id": resource["resource_id"], "consumer": resource["consumer"],
                                                          "resource_read": False, "exit_status": process.returncode,
                                                          "reader_sha256": digest_file(extracted / resource["reader"]),
                                                          "output_sha256": digest_bytes(process.stdout.encode("utf-8"))})
                    receipt["bundles"].append({"host": host, "access": access, "archive_reference": {
                        "path": archive.relative_to(PROJECT).as_posix(), "sha256": digest_file(archive)},
                        "smoke": observed, "disabled_reader_observations": disabled_observations})
                atomic_json(output, receipt)
                print(json.dumps({"host": host, "access": access, "status": "pass"}), flush=True)
        if digest_record(verify_source_lock(ROOT)) != source_hash:
            raise ValueError("source changed during extracted smoke")
        receipt["status"] = "pass"
    except Exception as error:
        receipt.update(status="timeout-unknown" if isinstance(error, subprocess.TimeoutExpired) else "fail", error=str(error))
        atomic_json(output, receipt)
        raise
    atomic_json(output, receipt)
    print(json.dumps({"status": receipt["status"], "bundles": len(receipt["bundles"]), "qualification": "pending"}), flush=True)


if __name__ == "__main__":
    run()
