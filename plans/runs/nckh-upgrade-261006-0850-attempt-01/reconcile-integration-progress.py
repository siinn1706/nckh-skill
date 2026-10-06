"""Advance only the independently reviewed integration prerequisites."""
from pathlib import Path

RUN = Path(__file__).resolve().parent
PLAN = RUN.parents[2] / "plans/261005-0036-nckh-devops-aiops-research-upgrade"
path = PLAN / "phase-07-integration-and-qualification.md"
text = path.read_text(encoding="utf-8")
for _ in range(3):
    text = text.replace("- [ ]", "- [x]", 1)
text += "\n## Integration checkpoints\n\n[Pre-freeze and corrective source reviews](../reports/review-261006-research-integration-p7.md) verify exact preserved baseline sets, twelve separate supplemental routes, rights/privacy and helper closures. [Migration inventory](../runs/nckh-upgrade-261006-0850-attempt-01/migration-inventory.json), [protected-byte check](../runs/nckh-upgrade-261006-0850-attempt-01/p7-protected-check-01.json) and [114 lock-independent tests](../runs/nckh-upgrade-261006-0850-attempt-01/p7-domain-tests-attempt-01.txt) record actual evidence. The first r39 pinned78 run failed on two stale counts, a missing fixture catalog and isolated bytecode writes; [preserved failure](../runs/nckh-upgrade-261006-0850-attempt-01/p7-pinned-tests-attempt-01.txt), [counsel](../reports/counsel-261006-pinned-regression-failure.md), [eight focused repairs](../runs/nckh-upgrade-261006-0850-attempt-01/p7-corrective-tests-attempt-01.txt) and [corrective r40 freeze](../runs/nckh-upgrade-261006-0850-attempt-01/p7-approved-freeze.json) retain the chronology. The r40 full/package checks remain active; first-freeze verdicts are not transplanted.\n"
path.write_text(text, encoding="utf-8")
print("P7first3/7closed;35/39total;actualfullandpackagegatesactive")
