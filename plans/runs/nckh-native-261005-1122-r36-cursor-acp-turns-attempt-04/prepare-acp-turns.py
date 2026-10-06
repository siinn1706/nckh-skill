"""Prepare an owned runtime controller from the retained extracted-payload harness."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-0818-r35-cursor-template-timing-attempt-01"
source = BASE / "cursor-file-probes.py"
target = RUN / "cursor-acp-runtime.py"
assert not target.exists()
text = source.read_text(encoding="utf8")
replacements = {
    'EXPECTED = "4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255"':
        'EXPECTED = "1a471686c5b1e89e6838957161a8ae4c6787d46d227420d8644636062da90d30"',
    'EVIDENCE = PROJECT / ".nckh-native-r35-cursor-template-timing"':
        'EVIDENCE = PROJECT / ".nckh-native-r36-cursor-acp-04"',
    'DELIVERY = WORK / "plans/runs/nckh-native-261005-0710-r35-attempt-01"':
        'DELIVERY = WORK / "plans/runs/nckh-native-261005-1050-r36-shell-guard-attempt-02"',
    'context_reference=".nckh-native-r35-cursor-template-timing/context-allow.json"':
        'context_reference=".nckh-native-r36-cursor-acp-04/context-allow.json"',
    '"source_revision": 35': '"source_revision": 36',
    '"native-cursor-file-r35"': '"native-cursor-file-r36"',
}
counts = {}
for old, new in replacements.items():
    counts[old] = text.count(old)
    assert counts[old] > 0, old
    text = text.replace(old, new)
compile(text, str(target), "exec")
with target.open("x", encoding="utf8") as stream:
    stream.write(text)
for name in ("cursor-file-observer.py", "cursor-agy-model-dangerous-grant.json"):
    with (RUN / name).open("xb") as stream:
        stream.write((BASE / name).read_bytes())
bind = lambda p: {"path": p.relative_to(WORK).as_posix(), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
record = {"status": "prepared-controller-no-native-turn", "source_modified": False,
    "base_controller": bind(source), "adapted_controller": bind(target), "replacement_counts": counts,
    "owner": "/root", "port": None}
with (RUN / "controller-adaptation.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": record["status"]}))
