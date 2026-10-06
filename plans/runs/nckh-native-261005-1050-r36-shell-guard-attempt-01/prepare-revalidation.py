"""Adapt retained delivery helpers to the reviewed shell guard revision."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-0710-r35-attempt-01"
files = ("run-delivery-r35.py", "run-revalidation.py", "deterministic-without-global-deadline.py",
    "direct-deterministic-suite.py", "archive-delivery.ps1")
rows = []
for name in files:
    original = BASE / name
    destination = RUN / name.replace("r35", "r36")
    assert not destination.exists()
    source = original.read_text(encoding="utf8")
    source = source.replace("r35", "r36").replace('"35"', '"36"').replace('source_revision": 35', 'source_revision": 36')
    source = source.replace("r36-0710-attempt-01", "r36-1050-attempt-01")
    source = source.replace("native_r36_retest", "native_r36_retest")
    source = source.replace('previous_attempt\": \'C:/Users/USER\\\\Downloads\\\\test-skill\\\\plans\\\\runs\\\\nckh-native-261005-0005-r34-attempt-01\\\\deterministic-r34-attempt-01.json\'',
        'previous_attempt\": \'C:/Users/USER\\\\Downloads\\\\test-skill\\\\plans\\\\runs\\\\nckh-native-261005-0710-r35-attempt-01\\\\deterministic-r35-attempt-01.json\'')
    if destination.suffix == ".py":
        compile(source, str(destination), "exec")
    with destination.open("x", encoding="utf8", newline="\n") as stream:
        stream.write(source)
    rows.append({"source": str(original), "source_sha256": hashlib.sha256(original.read_bytes()).hexdigest(),
        "destination": str(destination), "destination_sha256": hashlib.sha256(destination.read_bytes()).hexdigest()})
with (RUN / "helper-adaptation.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps({"status": "adapted", "base_run": str(BASE), "source_revision": 36,
        "helpers": rows, "global_deadline_seconds": None, "test_timeouts": "unchanged",
        "native_model_execution": "not-performed-by-this-helper"}, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
print(json.dumps({"status": "adapted", "helpers": len(rows)}))
