"""Verify the same pinned source after native cleanup and seal its current identity."""
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
spec = importlib.util.spec_from_file_location("posttool_source_owner", RUN / "cursor-posttool-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
lock = probe.verify_source_lock(WORK / "nckh-kit")
assert len(lock["files"]) == 281
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path":path.relative_to(WORK).as_posix(),"sha256":sha(path)}
record = {"status":"verified-unchanged-r37-canonical-source-lock", "timestamp_utc":datetime.now(timezone.utc).isoformat(),
    "source_revision":37, "source_lock_hash":probe.EXPECTED, "verified_pins":len(lock["files"]),
    "guard_source":bind(RUN / "cursor-posttool-runtime.py"), "source_lock":bind(WORK / "nckh-kit/core/registry/source-lock/source-lock.json"),
    "broad_tests_rerun":False, "source_kit_modified":False}
with (RUN / "final-source-check.json").open("x", encoding="utf8", newline="\n") as stream:
    stream.write(json.dumps(record,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"status":record["status"],"pins":record["verified_pins"]}))
