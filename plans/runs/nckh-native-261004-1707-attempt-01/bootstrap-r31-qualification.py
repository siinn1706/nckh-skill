"""Start a fresh evidence attempt without overwriting r30's native failures."""

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

PREVIOUS = Path(__file__).resolve().parent
RUN = PREVIOUS.parent / "nckh-native-261004-2112-r31-attempt-01"
RUN.mkdir(exist_ok=False)
sha = lambda value: hashlib.sha256(value).hexdigest()
checkpoint = json.loads((PREVIOUS / "r31-source-checkpoint.json").read_text(encoding="utf8"))
assert checkpoint["revision"] == 31
adapted = []
for name in ["qualification-run.py", "cursor-agy-native-observer.py", "direct-deterministic-suite.py",
             "archive-delivery.ps1", "cursor-agy-model-dangerous-grant.json", "native-grant.json", "model-medium-grant.json"]:
    source, target = PREVIOUS / name, RUN / name
    shutil.copyfile(source, target)
    adapted.append({"source": str(source), "target": name, "source_sha256": sha(source.read_bytes()),
                    "target_sha256": sha(target.read_bytes()), "adaptation": "exact-copy"})
for source_name, target_name in [("run-delivery-r30.py", "run-delivery-r31.py"),
                                  ("cursor-agy-native-probe.py", "cursor-agy-native-probe.py"),
                                  ("deterministic-without-global-deadline.py", "deterministic-without-global-deadline.py")]:
    source = PREVIOUS / source_name
    text = source.read_text(encoding="utf8")
    if source_name.startswith("run-delivery"):
        text = text.replace('lock["revision"] != "30"', 'lock["revision"] != "31"')
        text = text.replace("nckh-hooks-r30-1707-attempt-01", "nckh-hooks-r31-2112-attempt-01")
        text = text.replace("assert runner == {}", 'assert runner == ({"decision": "ask"} if host == "agy" else {})')
    elif source_name == "cursor-agy-native-probe.py":
        text = text.replace("55a4b60779228f3be3ae42d7691a49dec1df1b4e6f26139a32435aa1914562e1", checkpoint["source_lock_hash"])
    else:
        text = text.replace('"""Preserve r30\'s timed-out attempt and run its unchanged suite to completion."""',
                            '"""Run the reviewed r31 suite without an overall deadline; keep individual test timeouts."""')
        text = text.replace("deterministic-r30-attempt-02", "deterministic-r31-attempt-01")
        text = text.replace('lock["revision"] != "30"', 'lock["revision"] != "31"')
        text = text.replace('"deterministic-r30.json"', repr(str(PREVIOUS / "deterministic-r30-attempt-02.json")))
    target = RUN / target_name
    target.write_text(text, encoding="utf8", newline="\n")
    adapted.append({"source": str(source), "target": target_name, "source_sha256": sha(source.read_bytes()),
                    "target_sha256": sha(target.read_bytes()), "adaptation": "reviewed-revision-and-AGY-wire-contract"})
(RUN / "commands").mkdir()
(RUN / "ownership.json").write_text(json.dumps({
    "schema_version": 1, "created_at": datetime.now(timezone.utc).isoformat(), "owner": "/root",
    "work_context": str(PREVIOUS.parents[2]), "timezone": "Asia/Saigon", "language": "vi",
    "source_revision": 31, "source_lock_hash": checkpoint["source_lock_hash"], "previous_run": str(PREVIOUS),
    "source_checkpoint": str(PREVIOUS / "r31-source-checkpoint.json"),
    "source_review": str(PREVIOUS / "source-agy-native-permission-review.json"),
    "human_grant_reference": str(PREVIOUS / "cursor-agy-model-dangerous-grant.json"),
    "copied_grant_semantics": "same existing human grant; not a new grant or fabricated approval",
    "helpers": adapted, "installed_update": "not-authorized-by-this-attempt",
    "native": "unverified", "scientific_release": "pending"
}, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf8")
print(json.dumps({"run": str(RUN), "source_revision": 31, "helpers": len(adapted)}))
