"""Back up the local index, reconcile evidence, and preserve a local journal."""

import importlib.util
import json
import os
import re
import sqlite3
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
AK = r"C:/Users/USER\bin\ak.exe"
env = os.environ.copy()
env["AGENTKIT_HOME"] = str(WORK / "plans/.agentkit-runtime")
spec = importlib.util.spec_from_file_location("native_plan_commands", WORK / "plans/runs/nckh-native-261004-1707-attempt-01/qualification-run.py")
commands = importlib.util.module_from_spec(spec)
spec.loader.exec_module(commands)
commands.RUN = RUN
RESULT = RUN / "plan-reconciliation.json"
BACKUP = RUN / "before-native-continuation-reindex.sqlite"
assert not RESULT.exists() and not BACKUP.exists()
database = WORK / "plans/.agentkit-runtime/plans/plans.db"
with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as source, sqlite3.connect(BACKUP) as target:
    source.backup(target)


def invoke(name, argv, body=b""):
    outcome, stdout, stderr = commands.run_command("native-plan-" + name, argv, cwd=WORK, timeout=60, env=env, stdin=body)
    assert outcome["exit_code"] == 0, (name, stderr.decode("utf8"))
    return json.loads(stdout.decode("utf8"))


invoke("validate", [AK, "plan", "validate", str(PLAN), "--json"])
invoke("parse", [AK, "plan", "parse", str(PLAN), "--json"])
invoke("reindex", [AK, "plan", "reindex", "--apply", "--path", str(WORK), "--json"])
indexed = invoke("show", [AK, "plan", "show", "test-skill/261004-0047", "--json"])
phase_rows = indexed["data"]["phases"]
reports = ["plans/reports/delivery-261005-0746-r35-cursor-files.md",
    "plans/reports/delivery-261005-0746-r35-cursor-files.json",
    "plans/reports/delivery-261005-0838-r35-agy-tools.md",
    "plans/reports/delivery-261005-0838-r35-agy-tools.json"]
for number in (3, 4):
    phase = phase_rows[number - 1]
    previous_evidence = phase.get("evidence") or ""
    previous_notes = phase.get("notes") or ""
    evidence = previous_evidence + ("; " if previous_evidence else "") + "; ".join(reports)
    notes = previous_notes + "\nR35 continuation: Cursor19 turns with retained template5s/native timeout failures; AGY9 turns with replace allow/private denial and direct template5s write allow/plan-only denial. Three AGY unknown-tool and two no-tool turns remain unverified. Source unchanged; full native checkbox stays unchecked."
    invoke("phase-" + str(number), [AK, "plan", "phase", "update", "test-skill/261004-0047", str(number),
        "--evidence", evidence, "--notes", notes, "--json"])
body = """## Kết quả

Current r35 giữ nguyên source-lock và local delivery. Cursor bổ sung 19 native turns với Read/Write stage bindings, direct Write faults và project/plugin duplicate. Direct packaged template5s bị native timeout dù có allow receipt; nguyên nhân chưa xác định.

AGY CLI1.2.16 có 9 new turns: replace public/private và direct template5s write allow/plan-only deny đạt expected native outcome. Three native unknown-tool errors và two model turns không gọi tool được giữ đúng unverified prevention. Four AGY batches cleanup104 matching members; final audits zero matching. Protected global hashes giữ nguyên. Reconciliation ban đầu bị auto-review từ chối trước thực thi; tạo mới qua CreateNew sau existence checks đã completed.

## Trạng thái và bước tiếp theo

Plan in-progress44/45; native checkbox unchecked. Giữ exact owner acceptance của hai r29 VI/EN samples, installed r25 và scientific/stable/release gates riêng. Tiếp tục điều tra Cursor timeout và các native routes/surfaces còn thiếu; Claude cần model/effort grant. AgentWiki publish skipped.
"""
journal = invoke("journal-create", [AK, "journal", "create", "NCKH r35 Cursor and AGY native continuation",
    "--summary", "Bound19 Cursor and9 AGY turns; source unchanged and full native gate open", "--stdin", "--date", "2026-10-05", "--json"], body.encode("utf8"))
journal_path = WORK / "plans/journals/2026-10-05-nckh-r35-cursor-and-agy-native-continuation.md"
assert journal_path.is_file(), journal
invoke("journal-validate", [AK, "journal", "validate", str(journal_path), "--json"])
status = invoke("status", [AK, "plan", "status", str(PLAN), "--json"])["data"]
assert (status["done_tasks"], status["total_tasks"], status["phases_done"]) == (44, 45, 3)
assert "- [ ] Record host evidence per surface/version/event" in (PLAN / "phase-03-portable-hooks.md").read_text(encoding="utf8")
documents = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md",
    *(WORK / report for report in reports if report.endswith(".md")), journal_path]
links = []
for document in documents:
    for reference in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf8")):
        if reference.startswith(("http://", "https://", "#")):
            continue
        assert (document.parent / reference.split("#", 1)[0]).exists(), (document, reference)
        links.append({"document": document.relative_to(WORK).as_posix(), "target": reference})
record = {"status": "pass", "evidence_class": "structure-state-links-only", "progress": status,
    "sqlite_preimage": str(BACKUP.relative_to(WORK)), "sqlite_preimage_sha256": commands.sha(BACKUP.read_bytes()),
    "local_links_checked": len(links), "links": links, "native_checkbox": "unchecked",
    "journal": str(journal_path.relative_to(WORK)), "journal_sha256": commands.sha(journal_path.read_bytes()),
    "AgentWiki_publish": "skipped", "documents": {str(path.relative_to(WORK)): commands.sha(path.read_bytes()) for path in documents}}
with RESULT.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": "pass", "done": 44, "total": 45, "links_checked": len(links), "journal": str(journal_path)}))
