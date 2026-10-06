"""Reconcile plan projections while preserving the open native acceptance gate."""

import argparse
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
ROOT = WORK / "nckh-kit"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
os.environ["AGENTKIT_HOME"] = str(WORK / "plans/.agentkit-runtime")

from core.paths import atomic_json, digest_file
from core.processes import run_owned_command

AK = r"C:/Users/USER\bin\ak.exe"
parser = argparse.ArgumentParser()
parser.add_argument("--checkpoint", choices=("admission", "failures", "model-tools"), default="admission")
checkpoint = parser.parse_args().checkpoint
label = "prompt-" + checkpoint
receipt_path = RUN / f"plan-reconciliation-{label}.json"
if receipt_path.exists():
    raise RuntimeError("Preserve the earlier reconciliation")
database = WORK / "plans/.agentkit-runtime/plans/plans.db"
backup = RUN / f"plan-preimages/before-{label}-index.sqlite"
backup.parent.mkdir(exist_ok=True)
if backup.exists():
    raise RuntimeError("Preserve the existing SQLite preimage")
with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as source, sqlite3.connect(backup) as target:
    source.backup(target)
commands = [
    ("help-reindex", [AK, "plan", "reindex", "--help"]),
    ("help-phase-evidence", [AK, "plan", "phase", "update", "--help"]),
    ("help-validate", [AK, "plan", "validate", "--help"]),
    ("help-parse", [AK, "plan", "parse", "--help"]),
    ("help-status", [AK, "plan", "status", "--help"]),
    ("validate", [AK, "plan", "validate", str(PLAN), "--json"]),
    ("parse", [AK, "plan", "parse", str(PLAN), "--json"]),
    ("status", [AK, "plan", "status", str(PLAN), "--json"]),
    ("reindex", [AK, "plan", "reindex", "--apply", "--path", str(WORK), "--json"]),
    ("phase-evidence", [AK, "plan", "phase", "update", "test-skill/261004-0047", "3", "--evidence",
        "plans/reports/delivery-261004-1707-r30-native-checkpoint.md; plans/reports/delivery-261004-1707-r30-prompt-admission.md"
        + ("; plans/reports/delivery-261004-1707-r30-prompt-failures.md" if checkpoint in {"failures", "model-tools"} else "")
        + ("; plans/reports/delivery-261004-1707-r30-model-tools.md" if checkpoint == "model-tools" else ""),
        "--notes", ("Eight completed gpt-5.6-luna/medium turns and genuine Codex PreToolUse callbacks: allow creates oracle, policy deny prevents shell/marker; four failure cases fail-open. Cleanup passed, four disabled test keys in two projects. Full event/tool/duplicate/surface gate stays open; Cursor login and other-host model routes still needed."
                    if checkpoint == "model-tools" else "Codex UserPromptSubmit: seven native callbacks, malformed output/timeout/crash/unsupported selected codec fail-open; inactive/manual; full event/tool/duplicate/surface qualification pending; test config/payload removed and three native test keys disabled."
                    if checkpoint == "failures" else "Claude SessionStart and Codex UserPromptSubmit block/advisory observed; full native failure/tool/surface matrix pending; test config and payload removed; three test hashes remain trusted but disabled."), "--json"]),
]
outcomes = []
for name, argv in commands:
    stem = RUN / "commands" / ("plan-" + label + "-" + name)
    stdout, stderr, receipt = (Path(str(stem) + suffix) for suffix in (".stdout", ".stderr", ".json"))
    if receipt.exists():
        raise RuntimeError("Preserve the existing command receipt")
    result = run_owned_command(argv, WORK, b"", stdout, stderr, timeout=45)
    atomic_json(receipt, {"argv": argv, "cwd": str(WORK), **result,
                         "stdout_sha256": digest_file(stdout), "stderr_sha256": digest_file(stderr)})
    if result["exit_status"] != 0:
        raise RuntimeError("Plan command failed; inspect retained receipt: " + name)
    outcomes.append({"name": name, "exit_status": 0})
status = json.loads((RUN / f"commands/plan-{label}-status.stdout").read_text(encoding="utf8"))["data"]
if (status["done_tasks"], status["total_tasks"], status["phases_done"]) != (44, 45, 3):
    raise RuntimeError("Native acceptance gate or progress changed")
if "- [ ] Record host evidence per surface/version/event" not in (PLAN / "phase-03-portable-hooks.md").read_text(encoding="utf8"):
    raise RuntimeError("Native checkbox was closed without full evidence")
documents = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md",
             WORK / "plans/reports/delivery-261004-1707-r30-prompt-admission.md",
             WORK / "plans/journals/2026-10-04-nckh-r30-native-checkpoint.md"]
if checkpoint in {"failures", "model-tools"}:
    documents.append(WORK / "plans/reports/delivery-261004-1707-r30-prompt-failures.md")
if checkpoint == "model-tools":
    documents += [WORK / "plans/reports/delivery-261004-1707-r30-model-tools.md",
                  PLAN / "phase-04-integration-and-personal-acceptance.md"]
links = []
for document in documents:
    for match in re.finditer(r"\]\(([^)]+)\)", document.read_text(encoding="utf8")):
        reference = match.group(1)
        if reference.startswith(("https://", "http://", "#")):
            continue
        resolved = document.parent / reference.split("#", 1)[0]
        if not resolved.exists():
            raise RuntimeError("Broken link: " + str(document) + " -> " + reference)
        links.append({"document": str(document.relative_to(WORK)), "target": reference})
atomic_json(receipt_path, {"status": "pass", "evidence_class": "structure-state-links-only", "progress": status,
    "native_checkbox": "unchecked", "commands": outcomes, "sqlite_preimage": str(backup.relative_to(WORK)),
    "sqlite_preimage_sha256": digest_file(backup), "local_links_checked": len(links), "links": links,
    "document_hashes": {str(path.relative_to(WORK)): digest_file(path) for path in documents}})
print(json.dumps({"status": "pass", "done": status["done_tasks"], "total": status["total_tasks"],
                  "native_checkbox": "unchecked", "links_checked": len(links), "sqlite_backup": "created"}))
