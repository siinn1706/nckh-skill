"""Back up the local index, reconcile files, and retain honest native acceptance state."""

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

AK = r"C:/Users/USER\bin\ak.exe"
result_path = RUN / "plan-reconciliation.json"
if result_path.exists():
    raise RuntimeError("Preserve the existing reconciliation")
database = WORK / "plans/.agentkit-runtime/plans/plans.db"
backup = RUN / "plan-preimages-final/before-r34-index.sqlite"
if backup.exists():
    raise RuntimeError("Preserve the SQLite preimage")
with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as source, sqlite3.connect(backup) as target:
    source.backup(target)
commands = [
    ("help", [AK, "plan", "--help"]),
    ("help-resolve", [AK, "plan", "resolve", "--help"]),
    ("help-validate", [AK, "plan", "validate", "--help"]),
    ("help-parse", [AK, "plan", "parse", "--help"]),
    ("help-status", [AK, "plan", "status", "--help"]),
    ("help-reindex", [AK, "plan", "reindex", "--help"]),
    ("help-phase-update", [AK, "plan", "phase", "update", "--help"]),
    ("resolve", [AK, "plan", "resolve", "--json"]),
    ("validate", [AK, "plan", "validate", str(PLAN), "--json"]),
    ("parse", [AK, "plan", "parse", str(PLAN), "--json"]),
    ("status", [AK, "plan", "status", str(PLAN), "--json"]),
    ("reindex", [AK, "plan", "reindex", "--apply", "--path", str(WORK), "--json"]),
    ("phase-3-evidence", [AK, "plan", "phase", "update", "test-skill/261004-0047", "3", "--evidence",
        "plans/reports/delivery-261005-0005-r34-cursor-agy.md; plans/reports/delivery-261004-1707-r30-model-tools.md",
        "--notes", "R34 native AGY file/duplicate and event-fault observations; Cursor allow/duplicate timeout. Current test files cleaned. Full per-event/version/surface native task stays unchecked.", "--json"]),
    ("phase-4-evidence", [AK, "plan", "phase", "update", "test-skill/261004-0047", "4", "--evidence",
        "plans/reports/delivery-261005-0005-r34-cursor-agy.md; plans/reports/delivery-261005-0005-r34-cursor-agy.json",
        "--notes", "Current r34 full deterministic/build/archive/extract/smoke/previews/preservation completed; 187 tests with one Windows symlink skip. Owner acceptance remains exact r29 samples. Native gate separate.", "--json"]),
]
outcomes = []
for name, argv in commands:
    stem = RUN / "commands" / ("plan-r34-" + name)
    stdout, stderr, receipt = (Path(str(stem) + suffix) for suffix in (".stdout", ".stderr", ".json"))
    if receipt.exists():
        raise RuntimeError("Preserve the existing command receipt: " + name)
    outcome = run_owned_command(argv, WORK, b"", stdout, stderr, timeout=60)
    atomic_json(receipt, {"argv": argv, "cwd": str(WORK), **outcome, "stdout_sha256": digest_file(stdout), "stderr_sha256": digest_file(stderr)})
    if outcome["exit_status"] != 0:
        raise RuntimeError("Plan command failed; inspect retained evidence: " + name)
    outcomes.append({"name": name, "exit_status": 0})
status = json.loads((RUN / "commands/plan-r34-status.stdout").read_text(encoding="utf8"))["data"]
assert (status["done_tasks"], status["total_tasks"], status["phases_done"]) == (44, 45, 3)
assert "- [ ] Record host evidence per surface/version/event" in (PLAN / "phase-03-portable-hooks.md").read_text(encoding="utf8")
documents = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md",
             WORK / "plans/reports/delivery-261005-0005-r34-cursor-agy.md"]
links = []
for document in documents:
    for match in re.finditer(r"\]\(([^)]+)\)", document.read_text(encoding="utf8")):
        reference = match.group(1)
        if reference.startswith(("https://", "http://", "#")):
            continue
        if not (document.parent / reference.split("#", 1)[0]).exists():
            raise RuntimeError("Broken link: " + str(document) + " -> " + reference)
        links.append({"document": str(document.relative_to(WORK)), "target": reference})
atomic_json(result_path, {"status": "pass", "evidence_class": "structure-state-links-only", "progress": status,
    "native_checkbox": "unchecked", "commands": outcomes, "sqlite_preimage": str(backup.relative_to(WORK)),
    "sqlite_preimage_sha256": digest_file(backup), "local_links_checked": len(links), "links": links,
    "document_hashes": {str(path.relative_to(WORK)): digest_file(path) for path in documents}})
print(json.dumps({"status": "pass", "done": 44, "total": 45, "native_checkbox": "unchecked", "links_checked": len(links)}))
