"""Preserve r31's failed suite and create fresh r32 delivery receipts."""

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

PREVIOUS = Path(__file__).resolve().parent
RUN = PREVIOUS.parent / "nckh-native-261004-2112-r32-attempt-01"
RUN.mkdir(exist_ok=False)
checkpoint = json.loads((PREVIOUS / "r32-source-checkpoint.json").read_text(encoding="utf8"))
assert checkpoint["revision"] == 32
rows = []
for name in ["direct-deterministic-suite.py", "archive-delivery.ps1", "qualification-run.py"]:
    shutil.copyfile(PREVIOUS / name, RUN / name)
for original, target in [("run-delivery-r31.py", "run-delivery-r32.py"),
                          ("deterministic-without-global-deadline.py", "deterministic-without-global-deadline.py")]:
    text = (PREVIOUS / original).read_text(encoding="utf8")
    text = text.replace('lock["revision"] != "31"', 'lock["revision"] != "32"')
    text = text.replace("nckh-hooks-r31-2112-attempt-01", "nckh-hooks-r32-2112-attempt-01")
    text = text.replace("deterministic-r31-attempt-01", "deterministic-r32-attempt-01")
    if original.startswith("deterministic"):
        text = text.replace("reviewed r31 suite", "reviewed r32 suite")
        text = text.replace(str(PREVIOUS.parent / "nckh-native-261004-1707-attempt-01" / "deterministic-r30-attempt-02.json"),
                            str(PREVIOUS / "deterministic-r31-attempt-01.json"))
    (RUN / target).write_text(text, encoding="utf8", newline="\n")
for path in RUN.iterdir():
    if path.is_file():
        rows.append({"path": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
(RUN / "commands").mkdir()
(RUN / "ownership.json").write_text(json.dumps({
    "created_at": datetime.now(timezone.utc).isoformat(), "owner": "/root",
    "work_context": str(PREVIOUS.parents[2]), "timezone": "Asia/Saigon", "language": "vi",
    "source_revision": 32, "source_lock_hash": checkpoint["source_lock_hash"],
    "previous_run": str(PREVIOUS), "source_checkpoint": str(PREVIOUS / "r32-source-checkpoint.json"),
    "source_review": str(PREVIOUS / "source-closure-contract-review.json"),
    "previous_failed_suite": str(PREVIOUS / "deterministic-r31-attempt-01.json"),
    "native_runtime_equivalence": str(PREVIOUS / "r31-native-runtime-r32-source-equivalence.json"),
    "helpers": rows, "installed_update": "not-performed", "native": "separate-recorded-r31-runtime"
}, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf8")
print(json.dumps({"run": str(RUN), "source_revision": 32}))
