"""Append verified native observations while retaining all acceptance gaps."""

import hashlib
import json
import os
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
read = lambda p: json.loads(p.read_text(encoding="utf8"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert read(RUN / "native-duplicate-summary.json")["status"] == "verified-three-native-project-plugin-duplicate-events-two-plugin-cells-unqualified"
previous = WORK / "plans/runs/nckh-native-261005-1842-r37-cursor-private-create-attempt-18"
assert read(previous / "native-private-summary.json")["status"] == "verified-private-create-request-blocked-at-Read-Write-unqualified"
block = (
    "[Private create18](../reports/delivery-261005-1842-r37-cursor-private-create.md) records an absent-target create request "
    "blocked at native **Read**, target absent before/after and final marker/Stop observed. Private Write/denial remains "
    "unqualified. [Project/plugin19](../reports/delivery-261005-1900-r37-cursor-project-plugin-duplicate.md) verifies native "
    "duplicate sessionStart/preToolUse/postToolUse: eight actual callbacks total/five policy receipts. Plugin "
    "beforeSubmitPrompt/stop callbacks were not observed and remain unqualified. Both batches preserve source r37, "
    "protected global configs and historical evidence; cleanup removes26/28 matching members, preserves716/727 historical "
    "members and leaves zero owned processes. Full native task remains unchecked. Fresh AGY inventory still exposes "
    "zero AGY-owned windows; no app input, access/unlock grants retained.\n"
)
documents = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md",
    WORK / "plans/journals/2026-10-05-cursor-native-timeout-controls-and-r37-repair.md"]
snapshots = []
for document in documents:
    before = document.read_bytes()
    target = RUN / "checkpoint-document-preimages" / document.name
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("xb") as stream:
        stream.write(before)
    snapshots.append({"path": str(document), "before_sha256": sha(document),
        "preimage": target.relative_to(WORK).as_posix(), "preimage_sha256": sha(target)})
for document, snapshot in zip(documents, snapshots):
    text = document.read_text(encoding="utf8")
    assert "[Private create18]" not in text and "[Project/plugin19]" not in text
    if document.name == "plan.md":
        anchor = "Config/payload rollback removes only owned matching bytes"
        assert text.count(anchor) == 1
        text = text.replace(anchor, block + "\n" + anchor)
    else:
        text = text.rstrip() + "\n\n## Additional native evidence — r37 Cursor18–19\n\n" + block
    temporary = document.with_suffix(document.suffix + ".native-checkpoint.tmp")
    with temporary.open("x", encoding="utf8") as stream:
        stream.write(text)
    assert sha(document) == snapshot["before_sha256"], "Document changed after preimage; preserve concurrent edits"
    os.replace(temporary, document)
    snapshot["after_sha256"] = sha(document)
record = {"status": "verified-observations-appended-gaps-retained", "documents": snapshots,
    "source_revision": 37, "plan_tasks": "44/45", "full_native_gate": "unchecked",
    "native18": {"path": str(previous / "native-private-summary.json"), "sha256": sha(previous / "native-private-summary.json")},
    "native19": {"path": str(RUN / "native-duplicate-summary.json"), "sha256": sha(RUN / "native-duplicate-summary.json")}}
with (RUN / "checkpoint-document-update.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": record["status"], "documents": len(documents)}))
