"""Close the reviewed experiment phase while retaining qualification limits."""
import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261005-0036-nckh-devops-aiops-research-upgrade"

def bind(path):
    return {"path": str(path.relative_to(WORK)).replace("\\", "/"), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

report = WORK / "plans/reports/review-261006-experiment-graph-and-pilot.md"
assert "revision 2" in report.read_text(encoding="utf-8").lower() or "re-review" in report.read_text(encoding="utf-8").lower()
handoff = {"scope": "Actual retrospective dependent country series, no scientific/human/native/provider promotion",
    "review": bind(report), "previous_handoff": bind(RUN / "paperwrite-evidence-handoff.json"),
    "current_evidence": [bind(RUN / name) for name in ("p6-domain-tests-attempt-04.txt", "p6-isolated-graph-check-02.json",
        "experiment-readout.json", "statistical-readout.json", "aiops-readout.json", "partition-supplement-freeze.json",
        "partition-supplement-receipt.json", "partition-supplement-output.json", "partition-supplement-oracle.json")],
    "validator_source": [bind(WORK / "nckh-kit/core" / name) for name in ("aiops.py", "statistics.py", "experiments.py", "research_io.py")],
    "pending": ["owner feedback", "scientific acceptance", "full native qualification", "provider/paid scope", "stable/public release"],
    "cost": "unknown/unmeasured; provider unused", "owned_live": 0}
with (RUN / "paperwrite-evidence-handoff-v2.json").open("x", encoding="utf-8") as stream:
    stream.write(json.dumps(handoff, indent=2) + "\n")
phase = PLAN / "phase-06-reproducible-experiment-workflows.md"
text = phase.read_text(encoding="utf-8")
text = text.replace("status: in-progress", "status: completed", 1).replace("- [ ]", "- [x]")
text += "\n## Actual execution evidence\n\n[Independent review and repaired re-review](../reports/review-261006-experiment-graph-and-pilot.md), [110 domain tests](../runs/nckh-upgrade-261006-0850-attempt-01/p6-domain-tests-attempt-04.txt) and [fresh isolated graph check](../runs/nckh-upgrade-261006-0850-attempt-01/p6-isolated-graph-check-02.json) qualify source behavior and the unchanged actual graph. [Pilot readout](../runs/nckh-upgrade-261006-0850-attempt-01/pilot-readout.md) retains 26 source observations, six test predictions and independent endpoint arithmetic. [Partition supplement](../runs/nckh-upgrade-261006-0850-attempt-01/partition-supplement-receipt.json) adds genuine separate train/validation/test calculations: 52 outcomes, 49 completed and three insufficient-history unknowns; original test values are unchanged. The supplement is a separately hash-bound process observation, not a promoted research-run graph. [Final evidence handoff](../runs/nckh-upgrade-261006-0850-attempt-01/paperwrite-evidence-handoff-v2.json) binds current validator source, actual receipts and pending gates. Original fixture failures and counsel remain preserved. Both owned child handles are reaped; CPU/memory/provider cost remains unknown. Scientific/owner/full-native/provider/stable/public gates stay separate.\n"
phase.write_text(text, encoding="utf-8")
phase = PLAN / "phase-07-integration-and-qualification.md"
text = phase.read_text(encoding="utf-8").replace("status: pending", "status: in-progress", 1)
phase.write_text(text, encoding="utf-8")
path = PLAN / "plan.md"
text = path.read_text(encoding="utf-8")
text = text.replace("| P3–P5 / experiment owner | In progress |", "| P3–P5 / experiment owner | Completed |")
text = text.replace("| P1–P6 / single integration owner | Pending |", "| P1–P6 / single integration owner | In progress |")
path.write_text(text, encoding="utf-8")
print("P1-P6 completed32/39;P7active")
