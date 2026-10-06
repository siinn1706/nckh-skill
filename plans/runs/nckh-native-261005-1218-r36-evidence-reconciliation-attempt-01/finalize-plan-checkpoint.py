"""Reconcile plan files/index and create the local journal without closing gates."""

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
env = {**os.environ, "AGENTKIT_HOME": str(RUNTIME)}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bind(path):
    return {"path": path.relative_to(WORK).as_posix(), "sha256": digest(path)}


def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def invoke(name, argv, body=None):
    command = [str(AK), *argv]
    result = subprocess.run(command, cwd=WORK, env=env, input=body, text=True, encoding="utf8",
                            capture_output=True, timeout=60)
    stdout, stderr = RUN / f"commands/{name}.stdout", RUN / f"commands/{name}.stderr"
    stdout.parent.mkdir(exist_ok=True)
    with stdout.open("x", encoding="utf8") as stream:
        stream.write(result.stdout)
    with stderr.open("x", encoding="utf8") as stream:
        stream.write(result.stderr)
    record = {"command": command, "cwd": str(WORK), "agentkit_home": str(RUNTIME),
              "exit_code": result.returncode, "stdout": bind(stdout), "stderr": bind(stderr)}
    write_new(RUN / f"commands/{name}.json", record)
    assert result.returncode == 0, (name, result.returncode, result.stderr)
    return json.loads(result.stdout), bind(RUN / f"commands/{name}.json")


def index_snapshot():
    with sqlite3.connect(DATABASE.as_uri() + "?mode=ro", uri=True) as database:
        database.row_factory = sqlite3.Row
        plans = [dict(row) for row in database.execute("SELECT id, plan_dir, state, issue_number, root_comment_id, linked_pr, current_phase FROM plans")]
        phases = [dict(row) for row in database.execute("SELECT plan_id, n, comment_id, rev, notes, evidence, acceptance FROM phases ORDER BY plan_id,n")]
    return {"plans": plans, "phase_bookkeeping": phases}


assert not (RUN / "plan-finalization.json").exists()
backup = json.loads((RUN / "plan-store-preimage.json").read_text(encoding="utf8"))
assert digest(WORK / backup["backup"]["path"]) == backup["backup"]["sha256"]
documents = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md",
             WORK / "plans/reports/delivery-261005-1218-r36-native-reconciliation.md",
             WORK / "plans/reports/delivery-261005-1225-r36-cursor-interactive.md"]
links = []
for document in documents:
    for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", document.read_text(encoding="utf8")):
        if target.startswith(("https://", "http://", "mailto:", "#")):
            continue
        target = target.strip("<>").split("#", 1)[0]
        resolved = (document.parent / target).resolve()
        assert resolved.exists(), (document, target)
        links.append({"document": document.relative_to(WORK).as_posix(), "target": target})
write_new(RUN / "local-link-checks.json", {"status": "pass", "links_checked": len(links), "links": links})
validation, validation_binding = invoke("plan-validate", ["plan", "validate", str(PLAN), "--json"])
parsed, parse_binding = invoke("plan-parse", ["plan", "parse", str(PLAN), "--json"])
data = parsed["data"]
assert data["status"] == "in-progress" and data["total_tasks"] == 45 and data["done_tasks"] == 44
assert [(phase["number"], phase["done_tasks"], phase["total_tasks"]) for phase in data["phases"]] == [(1,13,13),(2,9,9),(3,10,11),(4,12,12)]
before = index_snapshot()
write_new(RUN / "index-bookkeeping-before-reindex.json", before)
preview, preview_binding = invoke("reindex-preview", ["plan", "reindex", "--path", str(WORK), "--json"])
applied, apply_binding = invoke("reindex-apply", ["plan", "reindex", "--path", str(WORK), "--apply", "--json"])
after = index_snapshot()
assert before["phase_bookkeeping"] == after["phase_bookkeeping"]
after_by_id = {row["id"]: row for row in after["plans"]}
assert all(after_by_id[row["id"]] == row for row in before["plans"])
target_rows = [row for row in after["plans"] if Path(row["plan_dir"]).resolve() == PLAN.resolve()]
assert len(target_rows) == 1 and target_rows[0]["state"] == "active"
_, current_phase_binding = invoke("current-phase", ["plan", "update", target_rows[0]["id"], "--current-phase", "3", "--json"])
final_index = index_snapshot()
assert final_index["phase_bookkeeping"] == before["phase_bookkeeping"]
final_target = next(row for row in final_index["plans"] if row["id"] == target_rows[0]["id"])
assert final_target["current_phase"] == 3 and final_target["state"] == "active"
write_new(RUN / "index-bookkeeping-after-reindex.json", final_index)
body = """## R36 checkpoint

Mapped shell execution now remains pending when target coverage cannot be verified; no arbitrary shell parsing was introduced. R35 private-shell failure remains historical evidence.

R36 local revalidation passed 192 tests with one Windows symlink skip, 16 archives/extractions, 216 resource reads, 48 OFF/no-read observations, 24 hook projections, eight previews and 509 protected hashes. Installed r25 and four legacy bundles remain unchanged.

Six Codex and two AGY native turns verify scoped shell/file outcomes. Cursor ACP verified exact granted parameters for two turns, but generated zero NCKH policy receipts; enforcement remains unqualified. ACP required owned process cleanup and recorded exit 3221225786.

Cursor interactive attempt 05 retained incomplete prompt input and zero verified turns. Separate prompt-text and Enter writes in attempt 06 produced one genuine Read and five native callbacks, including beforeSubmitPrompt and Stop. Fixture unchanged; artifact QA pending. Instrumented outer20s/runner5s timing and a truncated terminal chunk are explicit limitations.

Completed native batches removed only matching owned hooks/payloads and retained historical hashes. Interactive process trees needed force-stop after graceful refusal with verified PID/creation identity; their harness exit1 is retained. Final batch audits found no matching processes.

## Plan and remaining work

Plan files/index reconciled after a verified SQLite backup; phase revision/notes/evidence/acceptance preserved. Current phase3 remains active, plan44/45 and full native task unchecked. Exact r29 VI/EN samples accepted. AGY IDE work-surface/window-identity recovery, Claude model/effort grant, remaining native failure/tool/surface coverage and Cursor production timing remain pending. Scientific/stable/install/release gates remain separate.

AgentWiki publish skipped; local history only.
"""
write_new(RUN / "journal-draft.json", {"title": "R36 native shell guard và Cursor interactive evidence", "body": body})
journal, journal_binding = invoke("journal-create", ["journal", "create", "R36 native shell guard và Cursor interactive evidence",
    "--summary", "R36 local/native checkpoint verified; full native task remains open.", "--stdin", "--date", "2026-10-05", "--json"], body)
record = {"status": "plan-index-and-local-journal-reconciled-native-gate-open", "plan": str(PLAN.relative_to(WORK)),
          "total_tasks": 45, "done_tasks": 44, "current_phase": 3, "state": "active", "status_in_file": "in-progress",
          "full_native_gate": "unchecked", "SQLite_backup": bind(RUN / "plan-store-preimage.json"),
          "phase_bookkeeping_preserved": True, "document_hashes": [bind(path) for path in documents],
          "local_links": bind(RUN / "local-link-checks.json"), "links_checked": len(links),
          "commands": [validation_binding, parse_binding, preview_binding, apply_binding, current_phase_binding, journal_binding],
          "journal_result": journal, "agentwiki_publish": "skipped", "verifier": bind(Path(__file__))}
write_new(RUN / "plan-finalization.json", record)
print(json.dumps({"status": record["status"], "done_tasks": 44, "total_tasks": 45, "links_checked": len(links), "journal": journal}))
