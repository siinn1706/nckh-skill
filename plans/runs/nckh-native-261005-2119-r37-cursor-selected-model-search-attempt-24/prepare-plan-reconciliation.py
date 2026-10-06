"""Reconcile latest native progress while preserving all open acceptance gates."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-1930-r37-cursor-plugin-alias-controls-attempt-21"
source = BASE / "reconcile-plan.py"
text = source.read_text(encoding="utf8")
replacements = [
    ('read(RUN / "native-alias-summary.json")["status"] == "verified-native-alias-control-two-plugin-cells-unqualified"',
     'read(RUN / "native-uncovered-summary.json")["status"] == "verified-native-Grep-uncovered-route-manual-host-completion"'),
    ('WORK / "plans/reports/delivery-261005-1930-r37-cursor-plugin-alias-controls.md"]',
     'WORK / "plans/reports/delivery-261005-1930-r37-cursor-plugin-alias-controls.md",\n    WORK / "plans/reports/delivery-261005-1956-r37-host-route-recovery.md",\n    WORK / "plans/reports/delivery-261005-2004-r37-cursor-search-admission-failure.md",\n    WORK / "plans/reports/delivery-261005-2119-r37-cursor-selected-model-search.md"]'),
    ('previous = WORK / "plans/runs/nckh-native-261005-1900-r37-cursor-project-plugin-duplicate-attempt-19/plan-reconciliation.json"',
     'previous = WORK / "plans/runs/nckh-native-261005-1930-r37-cursor-plugin-alias-controls-attempt-21/plan-reconciliation.json"'),
    ('"scoped_native21": bind(RUN / "native-alias-summary.json"),',
     '"scoped_native21": bind(WORK / "plans/runs/nckh-native-261005-1930-r37-cursor-plugin-alias-controls-attempt-21/native-alias-summary.json"),\n    "scoped_host22": bind(WORK / "plans/runs/nckh-native-261005-1956-r37-host-route-recovery-attempt-22/host-recovery-summary.json"),\n    "scoped_admission23": bind(WORK / "plans/runs/nckh-native-261005-2004-r37-cursor-uncovered-search-attempt-23/native-admission-summary.json"),\n    "scoped_native24": bind(RUN / "native-uncovered-summary.json"),\n    "all_observed_processes": bind(RUN / "all-observed-process-audit.json"),'),
]
for before, after in replacements:
    assert text.count(before) == 1, before
    text = text.replace(before, after)
target = RUN / "reconcile-plan.py"
with target.open("x", encoding="utf8") as stream:
    stream.write(text)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
with (RUN / "reconciler-adaptation.json").open("x", encoding="utf8") as stream:
    json.dump({"status":"adapted-existing-state-contract", "source":str(source), "source_sha256":sha(source),
        "target":str(target), "target_sha256":sha(target), "replacement_count":len(replacements),
        "previous_receipts_modified":False, "state_contract":"44/45; phase3 active; SQLite backup and index bookkeeping preserved"},stream,indent=2)
    stream.write("\n")
print(json.dumps({"status":"prepared-reconciler", "replacement_count":len(replacements)}))
