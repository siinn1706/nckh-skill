"""Adapt the preceding verified reconciler without modifying historical receipts."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PREVIOUS = WORK / "plans/runs/nckh-native-261005-1900-r37-cursor-project-plugin-duplicate-attempt-19"
source = PREVIOUS / "reconcile-plan.py"
text = source.read_text(encoding="utf8")
replacements = [
    ('read(RUN / "native-duplicate-summary.json")["status"] == "verified-three-native-project-plugin-duplicate-events-two-plugin-cells-unqualified"',
     'read(RUN / "native-alias-summary.json")["status"] == "verified-native-alias-control-two-plugin-cells-unqualified"'),
    ('WORK / "plans/reports/delivery-261005-1900-r37-cursor-project-plugin-duplicate.md"]',
     'WORK / "plans/reports/delivery-261005-1900-r37-cursor-project-plugin-duplicate.md",\n    WORK / "plans/reports/delivery-261005-1930-r37-cursor-plugin-alias-controls.md"]'),
    ('previous = WORK / "plans/runs/nckh-native-261005-1755-r37-cursor-preflight-faults-attempt-17/plan-reconciliation.json"',
     'previous = WORK / "plans/runs/nckh-native-261005-1900-r37-cursor-project-plugin-duplicate-attempt-19/plan-reconciliation.json"'),
    ('"scoped_native19": bind(RUN / "native-duplicate-summary.json"),',
     '"scoped_native19": bind(WORK / "plans/runs/nckh-native-261005-1900-r37-cursor-project-plugin-duplicate-attempt-19/native-duplicate-summary.json"),\n    "scoped_native21": bind(RUN / "native-alias-summary.json"),'),
]
for before, after in replacements:
    assert text.count(before) == 1, before
    text = text.replace(before, after)
target = RUN / "reconcile-plan.py"
with target.open("x", encoding="utf8") as stream:
    stream.write(text)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
with (RUN / "reconciler-adaptation.json").open("x", encoding="utf8") as stream:
    json.dump({"status": "adapted-with-existing-state-contract", "source": str(source), "source_sha256": sha(source),
        "target": str(target), "target_sha256": sha(target), "replacement_count": len(replacements),
        "previous_receipts_modified": False, "state_contract": "44/45; phase3 active; bookkeeping and backup preserved"}, stream, indent=2)
    stream.write("\n")
print(json.dumps({"status": "prepared-reconciler", "replacement_count": len(replacements)}))
