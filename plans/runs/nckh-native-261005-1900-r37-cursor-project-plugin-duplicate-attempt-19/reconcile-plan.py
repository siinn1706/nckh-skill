"""Reconcile current files without closing native or index-owned lifecycle gates."""

import hashlib
import json
import os
import re
import sqlite3
import subprocess
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
RUNTIME = WORK / "plans/.agentkit-runtime"
DATABASE = RUNTIME / "plans/plans.db"
AK = Path(r"C:/Users/USER\bin\ak.exe")
ENV = {**os.environ, "AGENTKIT_HOME": str(RUNTIME)}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {"path": p.relative_to(WORK).as_posix(), "sha256": sha(p)}
read = lambda p: json.loads(p.read_text(encoding="utf8"))


def write_new(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def snapshot():
    with sqlite3.connect(DATABASE.as_uri() + "?mode=ro", uri=True) as database:
        database.row_factory = sqlite3.Row
        plans = [dict(r) for r in database.execute("SELECT id,plan_dir,state,issue_number,root_comment_id,linked_pr,current_phase FROM plans")]
        phases = [dict(r) for r in database.execute("SELECT plan_id,n,comment_id,rev,notes,evidence,acceptance FROM phases ORDER BY plan_id,n")]
    return {"plans": plans, "phase_bookkeeping": phases}


def invoke(name, args):
    result = subprocess.run([str(AK), *args], cwd=WORK, env=ENV, capture_output=True, text=True, encoding="utf8", timeout=60)
    write_new(RUN / f"commands/reconcile-{name}.json", {"command": [str(AK), *args], "exit_code": result.returncode,
        "stdout": result.stdout, "stderr": result.stderr})
    assert result.returncode == 0, (name, result.stderr)
    return json.loads(result.stdout) if "--json" in args else result.stdout


assert not (RUN / "plan-reconciliation.json").exists()
DELIVERY = WORK / "plans/runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-02"
pipeline = read(DELIVERY / "revalidation-summary.json")
assert pipeline["status"] == "completed-local-checks-native-retest-pending"
assert read(RUN / "native-duplicate-summary.json")["status"] == "verified-three-native-project-plugin-duplicate-events-two-plugin-cells-unqualified"
assert read(WORK / "plans/runs/nckh-native-261005-1842-r37-cursor-private-create-attempt-18/native-private-summary.json")["status"] == "verified-private-create-request-blocked-at-Read-Write-unqualified"
delivery = WORK / "plans/reports/delivery-261005-1640-r37-local-native-checkpoint.json"
assert read(delivery)["status"] == "verified-r37-local-and-scoped-packaged-native-checkpoint"
backup = RUN / "plan-store-before-reindex.sqlite"
assert not backup.exists()
with sqlite3.connect(DATABASE.as_uri() + "?mode=ro", uri=True) as source, sqlite3.connect(backup) as target:
    source.backup(target)
    assert target.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
before = snapshot()
write_new(RUN / "index-bookkeeping-before-reindex.json", before)
write_new(RUN / "plan-store-preimage.json", {"database": str(DATABASE), "backup": bind(backup), "integrity_check": "ok"})
documents = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md",
    WORK / "plans/journals/2026-10-05-cursor-native-timeout-controls-and-r37-repair.md",
    WORK / "plans/reports/review-261005-1640-cursor-pretool-timeout.md",
    WORK / "plans/reports/delivery-261005-1523-r36-cursor-direct-sequence.md",
    WORK / "plans/reports/delivery-261005-1550-r36-cursor-direct-failure-observer.md",
    WORK / "plans/reports/delivery-261005-1610-r36-cursor-direct-timeout-control.md",
    WORK / "plans/reports/delivery-261005-1620-r36-cursor-direct-mutation-control.md",
    WORK / "plans/reports/delivery-261005-1700-r37-cursor-packaged-controls.md",
    WORK / "plans/reports/delivery-261005-1640-r37-local-native-checkpoint.md",
    WORK / "plans/reports/delivery-261005-1740-r37-cursor-private-edit.md",
    WORK / "plans/reports/delivery-261005-1755-r37-cursor-preflight-faults.md",
    WORK / "plans/reports/delivery-261005-1842-r37-cursor-private-create.md",
    WORK / "plans/reports/delivery-261005-1900-r37-cursor-project-plugin-duplicate.md"]
links = []
for document in documents:
    for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", document.read_text(encoding="utf8")):
        if target.startswith(("https://", "http://", "mailto:", "#")):
            continue
        assert (document.parent / target.strip("<>").split("#", 1)[0]).resolve().exists(), (document, target)
        links.append({"document": document.relative_to(WORK).as_posix(), "target": target})
write_new(RUN / "local-link-checks.json", {"status": "pass", "links_checked": len(links), "links": links})
invoke("help", ["plan", "--help"])
for verb in ("validate", "parse", "reindex"):
    invoke(verb + "-help", ["plan", verb, "--help"])
invoke("validate", ["plan", "validate", str(PLAN), "--json"])
parsed = invoke("parse", ["plan", "parse", str(PLAN), "--json"])["data"]
assert parsed["status"] == "in-progress" and parsed["total_tasks"] == 45 and parsed["done_tasks"] == 44
assert [(p["number"], p["done_tasks"], p["total_tasks"]) for p in parsed["phases"]] == [(1,13,13),(2,9,9),(3,10,11),(4,12,12)]
invoke("reindex-preview", ["plan", "reindex", "--path", str(WORK), "--json"])
invoke("reindex-apply", ["plan", "reindex", "--path", str(WORK), "--apply", "--json"])
after = snapshot()
assert before == after
target = [p for p in after["plans"] if Path(p["plan_dir"]).resolve() == PLAN.resolve()]
assert len(target) == 1 and target[0]["state"] == "active" and target[0]["current_phase"] == 3
write_new(RUN / "index-bookkeeping-after-reindex.json", after)
previous = WORK / "plans/runs/nckh-native-261005-1755-r37-cursor-preflight-faults-attempt-17/plan-reconciliation.json"
write_new(RUN / "plan-reconciliation.json", {"status": "verified-r37-checkpoint-reconciled-native-gate-open",
    "plan": str(PLAN), "done_tasks": 44, "total_tasks": 45, "current_phase": 3, "state": "active",
    "full_native_gate": "unchecked", "SQLite_backup": bind(backup), "index_bookkeeping_preserved": True,
    "links_checked": len(links), "documents": [bind(p) for p in documents], "delivery": bind(delivery),
    "previous_reconciliation": bind(previous), "previous_hash_scope": "historical documents; receipts unchanged",
    "scoped_native16": bind(WORK / "plans/runs/nckh-native-261005-1740-r37-cursor-private-mutation-attempt-16/native-private-summary.json"),
    "scoped_native17": bind(WORK / "plans/runs/nckh-native-261005-1755-r37-cursor-preflight-faults-attempt-17/native-preflight-summary.json"),
    "scoped_native18": bind(WORK / "plans/runs/nckh-native-261005-1842-r37-cursor-private-create-attempt-18/native-private-summary.json"),
    "scoped_native19": bind(RUN / "native-duplicate-summary.json"),
    "verification_scope": "structure-state-integrity only", "AgentWiki_publish": "skipped", "verifier": bind(Path(__file__))})
print(json.dumps({"status": "reconciled-native-gate-open", "done_tasks": 44, "total_tasks": 45, "links_checked": len(links)}))
