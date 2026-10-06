"""Retain real local command results for the current source pin; no provider calls."""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "nckh-kit"
OUT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from core.build import verify_source_lock
from core.paths import atomic_json, digest_bytes, digest_record


def run(group):
    lock = verify_source_lock(ROOT)
    source_hash = digest_record(lock)
    artifact_root = ROOT / ("dist-resource-quality-r" + lock["revision"])
    if group == "deterministic":
        commands = [[sys.executable, "evals/run-evals.py", "--validate-only", "--output", str(OUT / ("structure-r" + lock["revision"] + ".json"))],
                    [sys.executable, "evals/run-evals.py", "--run-deterministic", "--output", str(OUT / ("deterministic-r" + lock["revision"] + ".json"))]]
    elif group == "reproducibility":
        commands = [[sys.executable, "scripts/build-artifacts.py", "--all", "--check", "--resource-access", access, *plugin]
                    for access in ["on", "off"] for plugin in [[], ["--plugin"]]]
    elif group == "artifacts":
        commands = [[sys.executable, "scripts/build-artifacts.py", "--all", "--plugin", "--resource-access", access,
                     "--output", str(artifact_root / access)] for access in ["on", "off"]]
    else:
        raise ValueError("unsupported local check group")
    receipt = {"schema_version": 1, "evidence_class": "local-command-observations", "source_revision": lock["revision"],
               "source_lock_hash": source_hash, "group": group, "recorded_at": datetime.now(timezone.utc).isoformat(),
               "environment": {"python": sys.version.split()[0], "platform": sys.platform}, "commands": [], "status": "in-progress",
               "native_qualification": "unverified", "human_acceptance": "not-evaluated", "qualification": "pending"}
    output = OUT / ("verification-" + group + "-r" + lock["revision"] + ".json")
    if output.exists():
        raise ValueError("preserve the existing check receipt; choose a new receipt suffix before rerunning")
    atomic_json(output, receipt)
    environment = dict(os.environ, PYTHONIOENCODING="utf-8")
    for command in commands:
        start = time.monotonic()
        try:
            process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, encoding="utf-8", timeout=900)
            observation = {"command": command, "exit_status": process.returncode, "stdout": process.stdout, "stderr": process.stderr,
                           "output_sha256": digest_bytes((process.stdout + process.stderr).encode("utf-8")),
                           "duration_seconds": round(time.monotonic() - start, 3), "status": "pass" if process.returncode == 0 else "fail"}
        except subprocess.TimeoutExpired as error:
            observation = {"command": command, "exit_status": None, "status": "timeout-unknown",
                           "duration_seconds": round(time.monotonic() - start, 3),
                           "stdout": (error.stdout or b"").decode("utf-8", errors="replace") if isinstance(error.stdout, bytes) else error.stdout,
                           "stderr": (error.stderr or b"").decode("utf-8", errors="replace") if isinstance(error.stderr, bytes) else error.stderr}
        receipt["commands"].append(observation)
        receipt["status"] = observation["status"] if observation["status"] != "pass" else "in-progress"
        atomic_json(output, receipt)
        print(json.dumps({"group": group, "completed_commands": len(receipt["commands"]), "status": observation["status"]}), flush=True)
        if observation["status"] != "pass":
            return 3
        if digest_record(verify_source_lock(ROOT)) != source_hash:
            receipt.update(status="fail", error="source changed during verification")
            atomic_json(output, receipt)
            return 3
    receipt["status"] = "pass"
    if group == "artifacts":
        receipt["artifact_root"] = artifact_root.relative_to(ROOT.parent).as_posix()
    atomic_json(output, receipt)
    print(json.dumps({"group": group, "status": receipt["status"], "receipt": output.relative_to(ROOT.parent).as_posix()}), flush=True)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", choices=["deterministic", "reproducibility", "artifacts"], required=True)
    sys.exit(run(parser.parse_args().group))
