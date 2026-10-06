"""Refresh corrected document bindings and preserve index-owned lifecycle/bookkeeping."""

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
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}
read = lambda path: json.loads(path.read_text(encoding="utf8"))


def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def snapshot():
    with sqlite3.connect(DATABASE.as_uri() + "?mode=ro", uri=True) as database:
        database.row_factory = sqlite3.Row
        plans = [dict(row) for row in database.execute("SELECT id,plan_dir,state,issue_number,root_comment_id,linked_pr,current_phase FROM plans")]
        phases = [dict(row) for row in database.execute("SELECT plan_id,n,comment_id,rev,notes,evidence,acceptance FROM phases ORDER BY plan_id,n")]
    return {"plans": plans, "phase_bookkeeping": phases}


def invoke(name, args):
    result = subprocess.run([str(AK), *args], cwd=WORK, env=ENV, capture_output=True,
                            text=True, encoding="utf8", timeout=60)
    write_new(RUN / f"commands/{name}.json", {"command": [str(AK), *args], "exit_code": result.returncode,
                                            "stdout": result.stdout, "stderr": result.stderr})
    assert result.returncode == 0, (name, result.stderr)
    return json.loads(result.stdout)


assert not (RUN / "plan-reconciliation.json").exists()
summary = read(RUN / "native-existing-summary.json")
assert summary["status"] == "verified-existing-file-observations-mutation-route-unqualified"
assert read(RUN / "cleanup.json")["status"] == "pass"
assert read(RUN / "final-process-audit.json")["matching_count"] == 0
afterimages = read(RUN / "report-correction-afterimages.json")
for row in afterimages["documents"]:
    assert sha(WORK / row["immutable_snapshot"]["path"]) == row["current_document_at_correction"]["sha256"]
backup_path = RUN / "plan-store-before-reindex.sqlite"
assert not backup_path.exists()
with sqlite3.connect(DATABASE.as_uri() + "?mode=ro", uri=True) as source, sqlite3.connect(backup_path) as backup:
    source.backup(backup)
    assert backup.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
before = snapshot()
write_new(RUN / "plan-store-preimage.json", {"database": str(DATABASE), "backup": bind(backup_path), "integrity_check": "ok"})
write_new(RUN / "index-bookkeeping-before-reindex.json", before)
documents = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md",
             WORK / "plans/reports/delivery-261005-1257-r36-cursor-prompt-stop-faults.md",
             WORK / "plans/reports/delivery-261005-1340-r36-cursor-direct-interactive.md",
             WORK / "plans/reports/delivery-261005-1415-r36-cursor-existing-mutations.md",
             WORK / "plans/journals/2026-10-05-r36-cursor-prompt-stop-faults-and-direct-5s-observations.md"]
links = []
for document in documents:
    for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", document.read_text(encoding="utf8")):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean_target = target.strip("<>").split("#", 1)[0]
        assert (document.parent / clean_target).resolve().exists(), (document, target)
        links.append({"document": document.relative_to(WORK).as_posix(), "target": target})
write_new(RUN / "local-link-checks.json", {"status": "pass", "links_checked": len(links), "links": links})
invoke("plan-validate", ["plan", "validate", str(PLAN), "--json"])
parsed = invoke("plan-parse", ["plan", "parse", str(PLAN), "--json"])["data"]
assert parsed["status"] == "in-progress" and parsed["total_tasks"] == 45 and parsed["done_tasks"] == 44
assert [(row["number"], row["done_tasks"], row["total_tasks"]) for row in parsed["phases"]] == [(1,13,13),(2,9,9),(3,10,11),(4,12,12)]
invoke("reindex-preview", ["plan", "reindex", "--path", str(WORK), "--json"])
invoke("reindex-apply", ["plan", "reindex", "--path", str(WORK), "--apply", "--json"])
after = snapshot()
assert before == after
target = [row for row in after["plans"] if Path(row["plan_dir"]).resolve() == PLAN.resolve()]
assert len(target) == 1 and target[0]["state"] == "active" and target[0]["current_phase"] == 3
write_new(RUN / "index-bookkeeping-after-reindex.json", after)
previous = WORK / "plans/runs/nckh-native-261005-1340-r36-cursor-direct-interactive-attempt-08/plan-finalization.json"
record = {"status": "corrected-documents-and-native09-reconciled-full-native-gate-open", "plan": str(PLAN),
          "done_tasks": 44, "total_tasks": 45, "current_phase": 3, "state": "active", "full_native_gate": "unchecked",
          "SQLite_backup": bind(backup_path), "phase_bookkeeping_preserved": True, "links_checked": len(links),
          "documents": [bind(path) for path in documents], "native_summary": bind(RUN / "native-existing-summary.json"),
          "report_correction": bind(RUN / "report-correction.json"), "corrected_snapshots": bind(RUN / "report-correction-afterimages.json"),
          "previous_finalization": bind(previous), "previous_finalization_scope": "historical; its old document hashes are preserved",
          "verification_scope": "structure-state-integrity; does not qualify native/scientific/stable/release gates",
          "agentwiki_publish": "skipped", "verifier": bind(Path(__file__))}
write_new(RUN / "plan-reconciliation.json", record)
print(json.dumps({"status": record["status"], "done_tasks": 44, "total_tasks": 45, "links_checked": len(links)}))
