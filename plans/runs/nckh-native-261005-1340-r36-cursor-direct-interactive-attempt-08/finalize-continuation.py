"""Reconcile the local plan index and journal without closing native acceptance."""

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
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": digest(path)}


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


def invoke(name, args, body=None):
    result = subprocess.run([str(AK), *args], cwd=WORK, env=ENV, input=body, capture_output=True,
                            text=True, encoding="utf8", timeout=60)
    write_new(RUN / f"commands/{name}.json", {"command": [str(AK), *args], "exit_code": result.returncode,
                                            "stdout": result.stdout, "stderr": result.stderr})
    assert result.returncode == 0, (name, result.stderr)
    return json.loads(result.stdout)


assert not (RUN / "plan-finalization.json").exists()
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
             WORK / "plans/reports/delivery-261005-1340-r36-cursor-direct-interactive.md"]
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
body = """## Native observations

R36 source remains unchanged. Cursor interactive fault07 records ten submissions, nine observed replies and one native admission rejection. Selected malformed-output/timeout/crash/unsupported-codec prompt faults permit continuation; Stop faults follow model reply. Controller-injection origin and instrumented timing remain explicit.

Direct08 records five turns with packaged runner at template5s and no observer. Fifteen policy receipts retain advisory/preflight/stop phases; no pre-delivery receipt. Bounded neutral-hash reconstruction matches four Read events and one Shell. Three requests labeled Write do not provide mutation evidence; public-write oracle failed and plan-only mutation denial remains unqualified. Shell returns pending and its marker is absent.

Both batches removed only matching owned hooks/payloads, preserved historical/global hashes and have zero final process matches. Their harness exit1 follows identity-verified force-stop after graceful refusal. Collector and identity-check failures are retained without model retries.

## Plan and continuation

Plan remains in-progress44/45, current phase3 active, native task unchecked. SQLite backup/integrity check precede reindex; index-owned linkage and phase bookkeeping remain unchanged. Existing-file mutation controls are the next bounded diagnostic. Claude model/effort and actual AGY work-surface recovery remain pending. Installed r25, exact r29 owner feedback and scientific/stable/release gates retain separate bindings.

AgentWiki publish skipped; local history only.
"""
write_new(RUN / "journal-draft.json", {"body": body})
journal = invoke("journal-create", ["journal", "create", "R36 Cursor prompt stop faults and direct 5s observations", "--summary",
                                  "Cursor native evidence added; genuine mutation and full native gate remain open.",
                                  "--stdin", "--date", "2026-10-05", "--json"], body)
record = {"status": "plan-index-and-local-journal-reconciled-native-gate-open", "plan": str(PLAN),
          "done_tasks": 44, "total_tasks": 45, "current_phase": 3, "state": "active", "full_native_gate": "unchecked",
          "SQLite_backup": bind(backup_path), "phase_bookkeeping_preserved": True, "links_checked": len(links),
          "documents": [bind(path) for path in documents], "journal_result": journal,
          "agentwiki_publish": "skipped", "verifier": bind(Path(__file__))}
write_new(RUN / "plan-finalization.json", record)
print(json.dumps({"status": record["status"], "done_tasks": 44, "total_tasks": 45, "links_checked": len(links)}))
