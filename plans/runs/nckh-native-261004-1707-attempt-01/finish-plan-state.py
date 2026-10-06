"""Reconcile the canonical plan files and the rebuildable local index."""

import os
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
ROOT = WORK / "nckh-kit"
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
os.environ["AGENTKIT_HOME"] = str(WORK / "plans/.agentkit-runtime")

from core.build import load_json
from core.paths import atomic_json, digest_file
from core.processes import run_owned_command

AK = r"C:/Users/USER\bin\ak.exe"
plan_id = "test-skill/261004-0047"
commands = [
    ("plan-check-p4-final", [AK, "plan", "check", str(PLAN / "phase-04-integration-and-personal-acceptance.md"), "--json"]),
    ("plan-r30-validate", [AK, "plan", "validate", str(PLAN), "--json"]),
    ("plan-r30-parse", [AK, "plan", "parse", str(PLAN), "--json"]),
    ("plan-r30-status", [AK, "plan", "status", str(PLAN), "--json"]),
    ("plan-r30-reindex", [AK, "plan", "reindex", "--apply", "--path", str(WORK), "--json"]),
    ("plan-r30-current", [AK, "plan", "update", plan_id, "--status", "in-progress", "--current-phase", "3", "--json"]),
    ("plan-r30-native-evidence", [AK, "plan", "phase", "update", plan_id, "3", "--evidence",
        "plans/reports/delivery-261004-1707-r30-native-checkpoint.md", "--notes",
        "Claude SessionStart observed; full preventive event/surface matrix pending; test configs/payload removed.", "--json"]),
    ("plan-r30-owner-evidence", [AK, "plan", "phase", "update", plan_id, "4", "--evidence",
        "plans/runs/nckh-native-261004-1707-attempt-01/owner-feedback.json", "--notes",
        "Exact r29 VI/EN samples accepted by owner; r30 writer bytes unchanged; 182 deterministic tests and 16 archives verified.", "--json"]),
]
outcomes = []
for name, argv in commands:
    stdout, stderr, receipt = (RUN / "commands" / (name + suffix) for suffix in (".stdout", ".stderr", ".json"))
    if receipt.exists():
        raise RuntimeError("Preserve previous plan command")
    result = run_owned_command(argv, WORK, b"", stdout, stderr, timeout=45)
    atomic_json(receipt, {"argv": argv, "cwd": str(WORK), **result,
                         "stdout_sha256": digest_file(stdout), "stderr_sha256": digest_file(stderr)})
    if result["exit_status"] != 0:
        raise RuntimeError(f"Plan reconciliation failed: {name}; inspect retained receipt")
    outcomes.append({"name": name, "exit_status": 0})
    print(name + ": exit 0", flush=True)
status = load_json(RUN / "commands/plan-r30-status.stdout")["data"]
if (status["done_tasks"], status["total_tasks"], status["phases_done"]) != (44, 45, 3):
    raise RuntimeError("Plan checkbox state differs from the acceptance report")
atomic_json(RUN / "plan-reconciliation.json", {"status": "pass", "plan_id": plan_id, "progress": status,
            "commands": outcomes, "evidence_class": "structure-state-only", "native_checkbox": "unchecked"})
