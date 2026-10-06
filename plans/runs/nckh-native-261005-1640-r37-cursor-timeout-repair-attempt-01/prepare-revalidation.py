"""Reuse the unchanged delivery gates with fresh revision-bound output paths."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-1050-r36-shell-guard-attempt-01"
assert not (RUN / "helper-adaptation.json").exists()
rows = []
for name in ("run-delivery-r36.py", "run-revalidation.py", "deterministic-without-global-deadline.py",
             "direct-deterministic-suite.py", "archive-delivery.ps1"):
    original = BASE / name
    destination = RUN / name.replace("r36", "r37")
    source = original.read_text(encoding="utf8")
    source = source.replace("r36", "r37").replace('"36"', '"37"').replace('source_revision": 36', 'source_revision": 37')
    source = source.replace("r37-1050-attempt-01", "r37-1640-attempt-01")
    if destination.suffix == ".py":
        compile(source, str(destination), "exec")
    with destination.open("x", encoding="utf8", newline="\n") as stream:
        stream.write(source)
    rows.append({"original": original.relative_to(WORK).as_posix(), "original_sha256": hashlib.sha256(original.read_bytes()).hexdigest(),
                 "adapted": destination.relative_to(WORK).as_posix(), "adapted_sha256": hashlib.sha256(destination.read_bytes()).hexdigest()})
with (RUN / "helper-adaptation.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps({"status": "adapted-for-r37", "source_revision": 37, "helpers": rows,
        "global_deadline_seconds": None, "individual_timeouts": "unchanged", "native_model_execution": False}, indent=2) + "\n")
print(json.dumps({"status": "adapted-for-r37", "helpers": len(rows)}))
