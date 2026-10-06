"""Execute known local qualification commands for one frozen candidate."""
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

RUN = Path(__file__).resolve().parent
KIT = RUN.parents[2] / "nckh-kit"
sys.path.insert(0, str(KIT))
from core.build import verify_source_lock
from core.paths import digest_record, digest_file

def now(): return datetime.now(timezone.utc).isoformat()
lock = verify_source_lock(KIT)
approved = json.loads((RUN / "p7-approved-freeze.json").read_text(encoding="utf-8"))
assert digest_record(lock) == approved["source_lock_hash"]
lock_hash = digest_record(lock)
records = []
commands = [
    ("cases-validation", [sys.executable, "-B", "evals/run-evals.py", "--validate-only", "--output", str(RUN / "p7-cases-validation.json")]),
    ("deterministic", [sys.executable, "-B", "evals/run-evals.py", "--run-deterministic", "--output", str(RUN / "p7-deterministic.json")]),
    ("reproducibility-standalone", [sys.executable, "-B", "scripts/build-artifacts.py", "--all", "--check", "--resource-access", "on"]),
    ("reproducibility-plugin", [sys.executable, "-B", "scripts/build-artifacts.py", "--all", "--check", "--plugin", "--resource-access", "on"]),
]
for access in ("on", "off"):
    for plugin in (False, True):
        mode = access + ("-plugin" if plugin else "-standalone") + ("-internal" if access == "off" else "")
        argv = [sys.executable, "-B", "scripts/build-artifacts.py", "--all", "--resource-access", access,
            "--output", str(RUN / "bundles" / mode)]
        if plugin: argv.append("--plugin")
        commands.append(("build-" + mode, argv))
commands.append(("extracted-qualification", [sys.executable, "-B", str(RUN / "qualify-extracted-packages.py")]))

for name, argv in commands:
    assert digest_record(verify_source_lock(KIT)) == lock_hash
    output = RUN / ("p7-" + name + "-attempt-01.txt")
    started = now()
    with output.open("xb") as stream:
        process = subprocess.Popen(argv, cwd=KIT, stdout=stream, stderr=subprocess.STDOUT, shell=False)
        active = {"name": name, "pid": process.pid, "parent_pid": os.getpid(), "argv": argv, "cwd": str(KIT), "started_at": started, "port": None}
        with (RUN / "p7-active-process.json").open("w", encoding="utf-8") as status:
            status.write(json.dumps(active, indent=2) + "\n")
        print(json.dumps({"started": name, "pid": process.pid}), flush=True)
        exit_code = process.wait()
    record = {**active, "ended_at": now(), "exit_status": exit_code, "output": output.name,
        "output_sha256": digest_file(output), "cleanup": "exact owned Popen handle reaped", "source_lock_hash": lock_hash}
    records.append(record)
    with (RUN / ("p7-command-" + name + ".json")).open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(record, indent=2) + "\n")
    with (RUN / "p7-active-process.json").open("w", encoding="utf-8") as stream:
        stream.write(json.dumps({**record, "owned_live": 0}, indent=2) + "\n")
    print(json.dumps({"completed": name, "exit_status": exit_code}), flush=True)
    if exit_code != 0:
        raise SystemExit(exit_code)
    assert digest_record(verify_source_lock(KIT)) == lock_hash
with (RUN / "p7-local-gates.json").open("x", encoding="utf-8") as stream:
    stream.write(json.dumps({"revision": lock["revision"], "pins": len(lock["files"]), "source_lock_hash": lock_hash,
        "commands": records, "status": "pass", "owned_live": 0, "native_qualification": "unverified", "scientific_acceptance": "pending"}, indent=2) + "\n")
