"""Reconcile plan state without promoting running checks or native qualification."""

import json
import os
import re
import sqlite3
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
sys.path.insert(0, str(WORK / "nckh-kit"))
sys.dont_write_bytecode = True
os.environ["AGENTKIT_HOME"] = str(WORK / "plans/.agentkit-runtime")
from core.paths import atomic_json, digest_file
from core.processes import run_owned_command

result_path = RUN / "plan-reconciliation.json"
if result_path.exists():
    raise RuntimeError("Preserve the reconciliation")
database = WORK / "plans/.agentkit-runtime/plans/plans.db"
backup = RUN / "before-plan-reindex.sqlite"
if backup.exists():
    raise RuntimeError("Preserve the SQLite backup")
with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as source, sqlite3.connect(backup) as target:
    source.backup(target)
ak = r"C:/Users/USER\bin\ak.exe"
commands = [
    ("validate", [ak, "plan", "validate", str(PLAN), "--json"]),
    ("parse", [ak, "plan", "parse", str(PLAN), "--json"]),
    ("status", [ak, "plan", "status", str(PLAN), "--json"]),
    ("reindex", [ak, "plan", "reindex", "--apply", "--path", str(WORK), "--json"]),
    ("phase-3", [ak, "plan", "phase", "update", "test-skill/261004-0047", "3", "--evidence",
        "plans/reports/delivery-261005-0052-r34-codex-events.md; plans/reports/delivery-261005-0128-r34-cursor-events.md; plans/reports/delivery-261005-0658-r34-codex-file-failure.md",
        "--notes", "R34 genuine events recorded; actual apply_patch private-path bypass preserved. R35 bounded reader repair/focused checks, full revalidation running. Full native task remains unchecked.", "--json"]),
    ("phase-4", [ak, "plan", "phase", "update", "test-skill/261004-0047", "4", "--evidence",
        "plans/reports/delivery-261005-0005-r34-cursor-agy.md; plans/runs/nckh-native-261005-0710-r35-attempt-01/source-checkpoint.json; plans/runs/nckh-native-261005-0710-r35-attempt-01/revalidation-summary.json",
        "--notes", "R34 retained completed delivery; R35 current source has 12 focused passing tests, full delivery stages running. No current native/scientific promotion or installed update.", "--json"]),
    ("journal", [ak, "journal", "validate", str(WORK / "plans/journals/2026-10-05-nckh-r34-native-delivery-checkpoint.md"), "--json"]),
]
outcomes = []
for name, argv in commands:
    stem = RUN / "commands" / ("plan-" + name)
    stdout, stderr, receipt = (Path(str(stem) + suffix) for suffix in (".stdout", ".stderr", ".json"))
    result = run_owned_command(argv, WORK, b"", stdout, stderr, timeout=60)
    atomic_json(receipt, {"argv": argv, "cwd": str(WORK), **result, "stdout_sha256": digest_file(stdout), "stderr_sha256": digest_file(stderr)})
    if result["exit_status"] != 0:
        raise RuntimeError("Retain plan command failure: " + name)
    outcomes.append({"name": name, "exit_status": 0})
status = json.loads((RUN / "commands/plan-status.stdout").read_text(encoding="utf8"))["data"]
assert (status["done_tasks"], status["total_tasks"], status["phases_done"]) == (44, 45, 3)
assert "- [ ] Record host evidence per surface/version/event" in (PLAN / "phase-03-portable-hooks.md").read_text(encoding="utf8")
documents = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md",
    WORK / "plans/reports/delivery-261005-0052-r34-codex-events.md", WORK / "plans/reports/delivery-261005-0128-r34-cursor-events.md",
    WORK / "plans/reports/delivery-261005-0658-r34-codex-file-failure.md"]
links = []
for document in documents:
    for reference in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf8")):
        if reference.startswith(("https://", "http://", "#")):
            continue
        if not (document.parent / reference.split("#", 1)[0]).exists():
            raise RuntimeError("Broken artifact link: " + str(document) + " -> " + reference)
        links.append({"document": document.relative_to(WORK).as_posix(), "target": reference})
atomic_json(result_path, {"status": "pass", "evidence_class": "structure-state-links-only", "progress": status,
    "native_checkbox": "unchecked", "commands": outcomes, "sqlite_preimage": backup.relative_to(WORK).as_posix(),
    "sqlite_preimage_sha256": digest_file(backup), "local_links_checked": len(links), "links": links,
    "document_hashes": {path.relative_to(WORK).as_posix(): digest_file(path) for path in documents},
    "full_r35_delivery": "running, not certified by reconciliation"})
print(json.dumps({"status": "pass", "done": 44, "total": 45, "links": len(links), "native_checkbox": "unchecked"}))
