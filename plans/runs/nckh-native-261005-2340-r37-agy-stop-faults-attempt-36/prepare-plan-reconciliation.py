"""Adapt the established files-first reconciler to the newly verified evidence."""

import ast
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-2310-r37-agy-agent-inventory-attempt-33"
text = (BASE / "reconcile-plan.py").read_text(encoding="utf8")
text = text.replace("read(RUN / 'agent-inventory-summary.json')['status'] == 'recorded-read-only-agent-inventory'",
    "read(RUN / 'verified-stop-delivery.json')['status'] == 'verified-four-native-agy-Stop-fault-observations'")
text = text.replace("'appended-native32-33-evidence'", "'reconciled-native34-36-reports-and-concise-index'")
start = text.index("documents = [")
end = text.index("\nlinks = []", start)
text = text[:start] + """documents = [PLAN / 'plan.md', PLAN / 'native-evidence-history.md', PLAN / 'phase-03-portable-hooks.md',
    PLAN / 'phase-04-integration-and-personal-acceptance.md',
    WORK / 'plans/journals/2026-10-05-cursor-native-timeout-controls-and-r37-repair.md',
    WORK / 'plans/reports/delivery-261005-2320-r37-agy-event-observations.md',
    WORK / 'plans/reports/delivery-261005-2335-r37-agy-search-gaps.md']""" + text[end:]
text = text.replace("verified-r37-native32-33-reconciled-gate-open", "verified-r37-native34-36-reconciled-gate-open")
text = text.replace("bind(RUN / 'agent-inventory-summary.json')", "bind(RUN / 'verified-stop-delivery.json')")
text = text.replace("'read_attempt32':", "'event_observations34':").replace(
    "nckh-native-261005-2255-r37-agy-read-tools-attempt-32/verified-read-attempt.json",
    "nckh-native-261005-2320-r37-agy-event-controls-attempt-34/verified-event-delivery.json")
text = text.replace("nckh-native-261005-2240-r37-agy-tool-controls-attempt-31/plan-reconciliation.json", BASE.name + "/plan-reconciliation.json")
text = text.replace("'verifier': bind(Path(__file__))", "'search35': bind(WORK / 'plans/runs/nckh-native-261005-2335-r37-agy-search-controls-attempt-35/verified-search-delivery.json'), 'verifier': bind(Path(__file__))")
ast.parse(text)
target = RUN / "reconcile-plan.py"
assert not target.exists()
target.write_text(text, encoding="utf8")
