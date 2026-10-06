"""Observe the complete frozen local suite, then its packaging descendants."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

RUN = Path(__file__).resolve().parent
KIT = RUN.parents[2] / "nckh-kit"
sys.path.insert(0, str(KIT))
from core.build import verify_source_lock
from core.evaluation import validate_cases
from core.paths import atomic_json, digest_record, digest_file

def now():
    return datetime.now(timezone.utc).isoformat()

def save(name, value):
    with (RUN / name).open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2) + "\n")

lock = verify_source_lock(KIT)
approved = json.loads((RUN / "p7-approved-freeze-attempt-03.json").read_text(encoding="utf-8"))
lock_hash = digest_record(lock)
assert lock_hash == approved["source_lock_hash"]
inventory_path = RUN / "p7-test-inventory.json"
inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
records = []
commands = [
    ("cases-validation", [sys.executable, "-B", "evals/run-evals.py", "--validate-only", "--output", str(RUN / "p7-cases-validation-attempt-02.json")]),
    ("deterministic", [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-p", "test_*.py", "-v"]),
    ("reproducibility-standalone", [sys.executable, "-B", "scripts/build-artifacts.py", "--all", "--check", "--resource-access", "on"]),
    ("reproducibility-plugin", [sys.executable, "-B", "scripts/build-artifacts.py", "--all", "--check", "--plugin", "--resource-access", "on"]),
]
for access in ("on", "off"):
    for plugin in (False, True):
        mode = access + ("-plugin" if plugin else "-standalone") + ("-internal" if access == "off" else "")
        argv = [sys.executable, "-B", "scripts/build-artifacts.py", "--all", "--resource-access", access,
                "--output", str(RUN / "bundles" / mode)]
        if plugin:
            argv.append("--plugin")
        commands.append(("build-" + mode, argv))
commands.append(("extracted-qualification", [sys.executable, "-B", str(RUN / "qualify-extracted-packages.py")]))

for name, argv in commands:
    assert digest_record(verify_source_lock(KIT)) == lock_hash
    output = RUN / ("p7-" + name + "-attempt-02.txt")
    started = now()
    with output.open("xb") as stream:
        process = subprocess.Popen(argv, cwd=KIT, stdout=stream, stderr=subprocess.STDOUT, shell=False)
        active = {"name": name, "pid": process.pid, "parent_pid": os.getpid(), "argv": argv, "cwd": str(KIT),
                  "started_at": started, "port": None, "timeout_seconds": None, "output": output.name}
        atomic_json(RUN / "p7-active-process.json", active)
        print(json.dumps({"started": name, "pid": process.pid}), flush=True)
        while process.poll() is None:
            time.sleep(20)
            content = output.read_text(encoding="utf-8", errors="replace")
            print(json.dumps({"active": name, "pid": process.pid, "output_bytes": output.stat().st_size,
                              "last_line": content.splitlines()[-1] if content.splitlines() else ""}), flush=True)
        exit_code = process.wait()
    post_hash = digest_record(verify_source_lock(KIT))
    record = {**active, "ended_at": now(), "exit_status": exit_code, "output_sha256": digest_file(output),
              "cleanup": "exact owned Popen handle reaped", "owned_live": 0,
              "source_lock_hash": lock_hash, "post_source_lock_hash": post_hash}
    records.append(record)
    save("p7-command-" + name + "-attempt-02.json", record)
    atomic_json(RUN / "p7-active-process.json", record)
    print(json.dumps({"completed": name, "exit_status": exit_code}), flush=True)
    if name == "deterministic":
        content = output.read_text(encoding="utf-8", errors="strict")
        count = re.search(r"^Ran (\d+) tests? in ([0-9.]+)s$", content, re.MULTILINE)
        matches = list(re.finditer(r"^([^\s]+) \((tests\.[^)]+)\) \.\.\. (.*)$", content, re.MULTILINE))
        cases = [{"id": match.group(2), "result": match.group(3)} for match in matches]
        observed_ids = [row["id"] for row in cases]
        complete = bool(count and int(count.group(1)) == len(inventory) and observed_ids == inventory)
        passed = sum(row["result"] == "ok" for row in cases)
        skipped = [row for row in cases if row["result"].startswith("skipped ")]
        summary = validate_cases(KIT)
        status = "pass" if exit_code == 0 and complete and post_hash == lock_hash else "fail"
        summary.update(status=status, evidence_class="deterministic-local", source_lock_hash=lock_hash,
                       recorded_at=now(), environment={"python": sys.version.split()[0], "platform": sys.platform},
                       deterministic={"status": status, "tests": int(count.group(1)) if count else 0,
                                      "passed": passed, "skipped": len(skipped), "skip_cases": skipped,
                                      "cases": cases, "complete_inventory_match": complete,
                                      "duration_seconds": float(count.group(2)) if count else None,
                                      "exit_status": exit_code, "command": argv, "output": output.name,
                                      "output_sha256": digest_file(output), "inventory_sha256": digest_file(inventory_path),
                                      "process": record, "no_exclusions": True,
                                      "entrypoint": "task-local observable wrapper of the same complete unittest discovery suite; public runner timeout retained separately"})
        save("p7-deterministic-attempt-02.json", summary)
        if status != "pass":
            raise SystemExit(exit_code or 3)
    if exit_code != 0 or post_hash != lock_hash:
        raise SystemExit(exit_code or 3)

save("p7-local-gates.json", {"revision": lock["revision"], "pins": len(lock["files"]), "source_lock_hash": lock_hash,
                           "commands": records, "status": "pass", "owned_live": 0,
                           "native_qualification": "unverified", "scientific_acceptance": "pending"})
