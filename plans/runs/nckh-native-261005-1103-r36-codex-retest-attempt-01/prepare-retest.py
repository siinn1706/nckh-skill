"""Adapt the retained controller to a fresh, revision-bound evidence namespace."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-0710-r35-attempt-01/native-codex-file"
source = BASE / "codex-native-files.py"
target = RUN / "codex-native-retest.py"
observer = RUN / "codex-file-observer.py"
assert not target.exists() and not observer.exists()
original = source.read_bytes()
text = original.decode("utf8")
changes = {
    'EXPECTED = "4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255"':
        'EXPECTED = "1a471686c5b1e89e6838957161a8ae4c6787d46d227420d8644636062da90d30"',
    'EVIDENCE = PROJECT / ".nckh-native-r35-file"':
        'EVIDENCE = PROJECT / ".nckh-native-r36-codex-retest-01"',
    'DELIVERY = RUN.parent':
        'DELIVERY = WORK / "plans/runs/nckh-native-261005-1050-r36-shell-guard-attempt-02"',
    'context_reference=".nckh-native-r35-file/context-allow.json"':
        'context_reference=".nckh-native-r36-codex-retest-01/context-allow.json"',
    '"source_revision": 35': '"source_revision": 36',
    '"native-codex-file-r35"': '"native-codex-file-r36"',
}
counts = {}
for before, after in changes.items():
    counts[before] = text.count(before)
    assert counts[before] > 0, before
    text = text.replace(before, after)
compile(text, str(target), "exec")
with target.open("x", encoding="utf8") as stream:
    stream.write(text)
observer.write_bytes((BASE / "codex-file-observer.py").read_bytes())
bind = lambda p: {"path": p.relative_to(WORK).as_posix(), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
record = {"status": "prepared-controller-only", "base": bind(source), "adapted": bind(target),
    "observer": bind(observer), "replacement_counts": counts, "native_started": False,
    "source_modified": False, "owner": "/root", "port": None}
with (RUN / "controller-adaptation.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": record["status"], "native_started": False}))
