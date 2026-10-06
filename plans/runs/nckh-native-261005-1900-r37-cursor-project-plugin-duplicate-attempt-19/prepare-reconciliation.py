"""Adapt the previous reconciler; keep its files and SQLite evidence intact."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-1755-r37-cursor-preflight-faults-attempt-17"
original = BASE / "reconcile-plan.py"
source = original.read_text(encoding="utf8")
replacements = [
    ('assert read(RUN / "native-preflight-summary.json")["status"] == "verified-five-native-preToolUse-Read-fault-observations"',
     'assert read(RUN / "native-duplicate-summary.json")["status"] == "verified-three-native-project-plugin-duplicate-events-two-plugin-cells-unqualified"\nassert read(WORK / "plans/runs/nckh-native-261005-1842-r37-cursor-private-create-attempt-18/native-private-summary.json")["status"] == "verified-private-create-request-blocked-at-Read-Write-unqualified"'),
    ('    WORK / "plans/reports/delivery-261005-1755-r37-cursor-preflight-faults.md"]',
     '    WORK / "plans/reports/delivery-261005-1755-r37-cursor-preflight-faults.md",\n    WORK / "plans/reports/delivery-261005-1842-r37-cursor-private-create.md",\n    WORK / "plans/reports/delivery-261005-1900-r37-cursor-project-plugin-duplicate.md"]'),
    ('previous = DELIVERY / "plan-reconciliation.json"',
     'previous = WORK / "plans/runs/nckh-native-261005-1755-r37-cursor-preflight-faults-attempt-17/plan-reconciliation.json"'),
    ('    "scoped_native17": bind(RUN / "native-preflight-summary.json"),',
     '    "scoped_native17": bind(WORK / "plans/runs/nckh-native-261005-1755-r37-cursor-preflight-faults-attempt-17/native-preflight-summary.json"),\n    "scoped_native18": bind(WORK / "plans/runs/nckh-native-261005-1842-r37-cursor-private-create-attempt-18/native-private-summary.json"),\n    "scoped_native19": bind(RUN / "native-duplicate-summary.json"),')
]
for before, after in replacements:
    assert source.count(before) == 1, before
    source = source.replace(before, after)
target = RUN / "reconcile-plan.py"
compile(source, str(target), "exec")
with target.open("x", encoding="utf8") as stream:
    stream.write(source)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
with (RUN / "reconciler-adaptation.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps({"original": str(original), "original_sha256": sha(original),
        "current": str(target), "current_sha256": sha(target), "replacements": len(replacements),
        "previous_unchanged": True, "native18_private_Write": "unqualified", "native19_plugin_prompt_stop": "unqualified"}, indent=2) + "\n")
(RUN / "commands").mkdir(exist_ok=True)
print("Reconciler prepared; no index changes yet")
