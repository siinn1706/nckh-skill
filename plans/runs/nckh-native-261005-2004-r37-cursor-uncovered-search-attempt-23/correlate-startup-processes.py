"""Compare startup process identities against retained owned native captures."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
bind = lambda p: {"path": p.relative_to(WORK).as_posix(), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
candidates = read(RUN / "final-process-audit.json")["illustrator_startup_processes"]
captures = sorted((WORK / "plans/runs").glob("nckh-native-*/process-tree-*.json"))
retained, skipped = [], []
for capture in captures:
    data = read(capture)
    rows = data.get("processes", []) if isinstance(data, dict) else data if isinstance(data, list) else []
    owner_path = capture.parent / "native-process-ownership.json"
    owner = read(owner_path) if owner_path.is_file() else {}
    if not isinstance(owner, dict) or owner.get("owner") != "/root":
        skipped.append({"capture": bind(capture), "reason": "no-root-controller-ownership-record"})
        continue
    for row in rows:
        if not isinstance(row, dict):
            continue
        pid = row.get("ProcessId", row.get("pid"))
        created = row.get("creation_utc")
        if isinstance(pid, int) and isinstance(created, str):
            retained.append({"pid": pid, "creation_utc": created, "capture": bind(capture), "owner": bind(owner_path)})
matches, unknown = [], []
for candidate in candidates:
    evidence = [row for row in retained if row["pid"] == candidate["pid"] and row["creation_utc"] == candidate["creation_utc"]]
    if evidence:
        matches.append({"process": candidate, "evidence": evidence})
    else:
        unknown.append(candidate)
record = {"status": "startup-ownership-correlation-observation", "capture_files_read": len(captures),
    "strict_PID_and_UTC_string_matches": matches, "unattributed_candidates": unknown, "skipped_captures": skipped,
    "process_stop_performed": False, "scope_limit": "Only exact recorded identities with root-controller ownership can be considered for cleanup"}
with (RUN / "startup-process-ownership-correlation.json").open("x", encoding="utf8") as stream:
    json.dump(record, stream, indent=2)
    stream.write("\n")
print(json.dumps({"capture_files": len(captures), "owned_matches": [{"process": row["process"], "capture_paths": sorted({e["capture"]["path"] for e in row["evidence"]})} for row in matches], "unattributed": unknown}))
