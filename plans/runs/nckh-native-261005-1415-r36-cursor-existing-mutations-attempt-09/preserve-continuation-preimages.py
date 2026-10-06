"""Preserve corrected prose before appending a new native observation checkpoint."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}
correction = json.loads((RUN / "report-correction.json").read_text(encoding="utf8"))
rows = []
for row in correction["documents"]:
    current = WORK / row["corrected"]["path"]
    assert sha(current) == row["corrected"]["sha256"]
    snapshot = RUN / "report-correction-afterimages" / current.name
    snapshot.parent.mkdir(exist_ok=True)
    with snapshot.open("xb") as stream:
        stream.write(current.read_bytes())
    assert sha(snapshot) == row["corrected"]["sha256"]
    rows.append({"current_document_at_correction": row["corrected"], "immutable_snapshot": bind(snapshot)})
plan = WORK / "plans/261004-0047-nckh-research-data-hooks-writing/plan.md"
snapshot = RUN / "continuation-preimages/plan.md"
snapshot.parent.mkdir(exist_ok=True)
with snapshot.open("xb") as stream:
    stream.write(plan.read_bytes())
record = {"status": "preserved-prose-correction-snapshots-before-new-checkpoint", "correction": bind(RUN / "report-correction.json"),
          "documents": rows, "plan_before_native09_checkpoint": {"document": bind(plan), "snapshot": bind(snapshot)},
          "history": "original correction hashes remain verifiable against immutable snapshots after current documents change"}
with (RUN / "report-correction-afterimages.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": record["status"], "documents": len(rows)}))
