"""Back up the local index and reconcile corrected current delivery records."""

import json
import os
import re
import sqlite3
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
RESULT = RUN / "plan-reconciliation-r35-delivery.json"
BACKUP = RUN / "before-r35-delivery-reindex.sqlite"
AK = r"C:/Users/USER\bin\ak.exe"
os.environ["AGENTKIT_HOME"] = str(WORK / "plans/.agentkit-runtime")
sys.path.insert(0, str(WORK / "nckh-kit"))
sys.dont_write_bytecode = True
from core.build import verify_source_lock
from core.paths import atomic_json, digest_file, digest_record
from core.processes import run_owned_command

if RESULT.exists() or BACKUP.exists():
    raise RuntimeError("Preserve the previous reconciliation/SQLite preimage")
source_hash = digest_record(verify_source_lock(WORK / "nckh-kit"))
assert source_hash == "4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255"
database = WORK / "plans/.agentkit-runtime/plans/plans.db"
with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as source, sqlite3.connect(BACKUP) as target:
    source.backup(target)
report = "plans/reports/delivery-261005-0710-r35-patch-retest"
commands = [
    ("validate", [AK, "plan", "validate", str(PLAN), "--json"]),
    ("parse", [AK, "plan", "parse", str(PLAN), "--json"]),
    ("reindex", [AK, "plan", "reindex", "--apply", "--path", str(WORK), "--json"]),
    ("phase-3", [AK, "plan", "phase", "update", "test-skill/261004-0047", "3", "--evidence", report + ".md; " + report + ".json",
        "--notes", "R35 canonical patch native retest: 12 genuine turns, protected add/update/delete/move/mixed denial, raw global hashes unchanged. Trust reporting and static cleanup helper corrections retained. Full native task stays unchecked.", "--json"]),
    ("phase-4", [AK, "plan", "phase", "update", "test-skill/261004-0047", "4", "--evidence", report + ".md; " + report + ".json",
        "--notes", "R35 local delivery complete: 190 tests/one Windows symlink skip, 16 archives/extractions, 216 reads, 48 OFF observations, 24 projections, eight previews, 509 protected hashes. Owner acceptance remains exact r29 samples; full native/scientific gates separate.", "--json"]),
    ("status", [AK, "plan", "status", str(PLAN), "--json"]),
    ("journal", [AK, "journal", "validate", str(WORK / "plans/journals/2026-10-05-nckh-r34-native-delivery-checkpoint.md"), "--json"]),
]
outcomes = []
for name, argv in commands:
    stem = RUN / "commands" / ("plan-r35-delivery-" + name)
    stdout, stderr, receipt = (Path(str(stem) + suffix) for suffix in (".stdout", ".stderr", ".json"))
    assert not receipt.exists()
    outcome = run_owned_command(argv, WORK, b"", stdout, stderr, timeout=60)
    atomic_json(receipt, {"argv": argv, "cwd": str(WORK), **outcome,
        "stdout_sha256": digest_file(stdout), "stderr_sha256": digest_file(stderr)})
    if outcome["exit_status"] != 0:
        raise RuntimeError("Keep the failed reconciliation command: " + name)
    outcomes.append({"name": name, "exit_status": 0})
status = json.loads((RUN / "commands/plan-r35-delivery-status.stdout").read_text(encoding="utf8"))["data"]
assert (status["done_tasks"], status["total_tasks"], status["phases_done"]) == (44, 45, 3)
assert "- [ ] Record host evidence per surface/version/event" in (PLAN / "phase-03-portable-hooks.md").read_text(encoding="utf8")
documents = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md",
    WORK / (report + ".md"), WORK / "plans/reports/delivery-261005-0052-r34-codex-events.md",
    WORK / "plans/reports/delivery-261005-0658-r34-codex-file-failure.md",
    WORK / "plans/journals/2026-10-05-nckh-r34-native-delivery-checkpoint.md"]
links = []
for document in documents:
    for reference in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf8")):
        if reference.startswith(("https://", "http://", "#")):
            continue
        assert (document.parent / reference.split("#", 1)[0]).exists(), (document, reference)
        links.append({"document": document.relative_to(WORK).as_posix(), "target": reference})
assert digest_record(verify_source_lock(WORK / "nckh-kit")) == source_hash
atomic_json(RESULT, {"status": "pass", "evidence_class": "structure-state-links-only", "progress": status,
    "source_lock_hash": source_hash, "native_checkbox": "unchecked", "commands": outcomes,
    "sqlite_preimage": BACKUP.relative_to(WORK).as_posix(), "sqlite_preimage_sha256": digest_file(BACKUP),
    "local_links_checked": len(links), "links": links,
    "document_hashes": {path.relative_to(WORK).as_posix(): digest_file(path) for path in documents},
    "previous_reconciliation_retained": "plan-reconciliation.json; earlier document hashes remain historical"})
print(json.dumps({"status": "pass", "done": 44, "total": 45, "native_checkbox": "unchecked", "links_checked": len(links)}))
