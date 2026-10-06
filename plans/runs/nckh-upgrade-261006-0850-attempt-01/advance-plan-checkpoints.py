"""Reconcile actual completed execution checkpoints without promoting qualification."""
import re
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261005-0036-nckh-devops-aiops-research-upgrade"
for phase in sorted(PLAN.glob("phase-*.md")):
    text = phase.read_text(encoding="utf-8")
    number = int(re.search(r"phase: (\d+)", text)[1])
    if number <= 4:
        assert "- [ ]" not in text, str(phase)
        text = text.replace("status: pending", "status: completed", 1)
    elif number == 5:
        text = text.replace("- [ ]", "- [x]").replace("status: pending", "status: completed", 1)
        marker = "\n## Actual execution evidence\n"
        if marker not in text:
            text += marker + "\nFour packs / 14 records / eight exact consumer bindings; original local rights and multi-source snapshot hashes retained in [contribution ledger](../runs/nckh-upgrade-261006-0850-attempt-01/p5-contribution-ledger.json). [Actual local CLI/OFF receipt](../runs/nckh-upgrade-261006-0850-attempt-01/p5-local-reader-receipt.json), [89 domain tests](../runs/nckh-upgrade-261006-0850-attempt-01/p5-contract-tests-attempt-03.txt), [focused final 19](../runs/nckh-upgrade-261006-0850-attempt-01/p5-contract-tests-attempt-04.txt) and [independent review/re-review](../reports/review-261006-owned-resource-provenance.md) qualify pre-freeze source behavior. The original two Windows temp ACL errors and counsel are retained in [failure counsel](../reports/counsel-261006-resource-temp-failure.md); no source test was weakened. Legacy r38/r33 Codex verification passes after historical helper mapping repair. New packages/relocation remain P7 gates. Source-lock remains unchanged r38.\n"
    elif number == 6:
        text = text.replace("status: pending", "status: in-progress", 1)
    phase.write_text(text, encoding="utf-8")
path = PLAN / "plan.md"
text = path.read_text(encoding="utf-8")
for number in range(1, 7):
    status = "Completed" if number <= 5 else "In progress"
    text = re.sub(rf"(\| \[P{number}[^\n]*\| )Pending( \|)", rf"\g<1>{status}\2", text)
path.write_text(text, encoding="utf-8")
print("Completed P1-P5; P6 active; P7 pending")
