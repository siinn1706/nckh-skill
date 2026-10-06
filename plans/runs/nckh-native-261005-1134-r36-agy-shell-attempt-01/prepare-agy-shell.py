"""Adapt the retained native harness without changing the frozen kit source."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-0838-r35-agy-tools-attempt-01"
source = BASE / "agy-tool-probes.py"
target = RUN / "agy-shell-runtime.py"
assert not target.exists()
text = source.read_text(encoding="utf8")
replacements = {
    'EXPECTED = "4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255"':
        'EXPECTED = "1a471686c5b1e89e6838957161a8ae4c6787d46d227420d8644636062da90d30"',
    'EVIDENCE = PROJECT / ".nckh-native-r35-agy-tools"': 'EVIDENCE = PROJECT / ".nckh-native-r36-agy-shell-01"',
    'DELIVERY = WORK / "plans/runs/nckh-native-261005-0710-r35-attempt-01"':
        'DELIVERY = WORK / "plans/runs/nckh-native-261005-1050-r36-shell-guard-attempt-02"',
    '"source_revision": 35': '"source_revision": 36',
    '"native-agy-tools-r35"': '"native-agy-shell-r36"',
    '"nckh-native-r35-tools"': '"nckh-native-r36-shell"',
    '"grep_search": "read"}': '"grep_search": "read", "run_command": "write", "Bash": "write", "Shell": "write", "PowerShell": "write", "exec_command": "write", "shell_command": "write"}',
    'Do not use a terminal, inspect another file, ': 'Do not inspect another file, ',
}
counts = {}
for before, after in replacements.items():
    counts[before] = text.count(before)
    assert counts[before] > 0, before
    text = text.replace(before, after)
compile(text, str(target), "exec")
with target.open("x", encoding="utf8") as stream:
    stream.write(text)
with (RUN / "agy-tool-observer.py").open("xb") as stream:
    stream.write((BASE / "agy-tool-observer.py").read_bytes())
grant = WORK / "plans/runs/nckh-native-261005-0005-r34-attempt-01/cursor-agy-model-dangerous-grant.json"
with (RUN / "cursor-agy-model-dangerous-grant.json").open("xb") as stream:
    stream.write(grant.read_bytes())
bind = lambda p: {"path": p.relative_to(WORK).as_posix(), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
with (RUN / "controller-adaptation.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps({"status": "prepared-controller-only", "source_modified": False,
        "base": bind(source), "adapted": bind(target), "replacement_counts": counts},
        ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": "prepared-controller-only"}))
