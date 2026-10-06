"""Reconcile this bounded observation without completing the remaining native task."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
REPORT = WORK / "plans/reports/delivery-261006-0300-r37-cursor-workspace-unsupported-event.md"
JOURNAL = WORK / "plans/journals/2026-10-06-private-search-and-native-app-availability.md"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}

def write_new(path, record):
    with path.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")

verified = read(RUN / "verified-unsupported-event-observations.json")
cleanup = read(RUN / "cleanup.json")
assert verified["status"] == "verified-genuine-kit-unsupported-event-startup-continuation"
assert len(cleanup["removed"]) == 33 and cleanup["preserved_historical_files"] == 891
paths = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", JOURNAL]
before = {str(path): sha(path) for path in paths}
summary = (
    "[Cursor genuine kit-unsupported event45](../reports/delivery-261006-0300-r37-cursor-workspace-unsupported-event.md) "
    "verifies actual workspaceOpen input forwarded unchanged with the actual selector: runner exit3/degraded block, "
    "then native project/plugin sessionStart continues. Zero model/tool requests; four callbacks/two receipts,17 frozen checks matched. "
    "Known host event outside kit codec; unknown-host-event admission and mutation prevention remain unverified. "
    "Native/monitor exit0, cleanup33/preserved891/final union2008 zero live. Source r37 unchanged;44/45/P3 active."
)
for path in paths:
    text = path.read_text(encoding="utf8")
    assert "Cursor genuine kit-unsupported event45" not in text
    if path.name == "plan.md":
        marker = "## Remaining acceptance và rollback"
        assert text.count(marker) == 1
        text = text.replace(marker, summary + "\n\n" + marker)
    else:
        text = text.rstrip() + "\n\n## Cursor genuine kit-unsupported event\n\n" + summary + "\n"
    path.write_text(text, encoding="utf8")
todo = read(RUN.parent / "nckh-native-261006-0240-r37-cursor-workspace-duplicates-attempt-44/native-continuation-todo.json")
todo["pending_or_unqualified"] = [
    "genuine unknown host event admission/delivery; known Cursor workspaceOpen absent from kit codec verified45" if item == "genuine unsupported native event delivery" else item
    for item in todo["pending_or_unqualified"]
]
todo["current_verified_Cursor_scopes"].append("actual workspaceOpen forwarded unchanged to unsupported kit codec45; native startup continues after exit3")
todo["process_state"] = "native45 final union2008 zero matching/tracked-live; owned native and monitor exit0; no process stop"
todo["latest_scoped_evidence"] = bind(RUN / "verified-unsupported-event-observations.json")
todo["final_process_audit"] = bind(RUN / "process-final-audit.json")
todo["Cursor_genuine_kit_unsupported_event"] = {
    "verification": bind(RUN / "verified-unsupported-event-observations.json"), "report": bind(REPORT),
    "status": verified["status"], "fault_origin": "none", "unknown_host_event": "unverified", "model_prompts": 0,
}
todo["pending_cache_permission"] = "exact cache/metadata scope reconfirmed asynchronously after context recovery; direct user answer remains pending"
todo["cache_permission_reconfirmation"] = {
    "mechanism": "request_user_input_async", "tool_result": {"accepted": True}, "user_answer": "not-received",
    "scope": bind(WORK / "plans/reports/proposal-261006-0135-r37-codex-plugin-cache-scope.md"),
    "installation": "not-performed", "elapsed_time_is_authority": False,
}
write_new(RUN / "native-continuation-todo.json", todo)
counts = {}
for path in sorted(PLAN.glob("phase-*.md")):
    items = re.findall(r"^\s*- \[([ xX])\]", path.read_text(encoding="utf8"), re.MULTILINE)
    counts[path.name] = {"done": sum(item.lower() == "x" for item in items), "total": len(items)}
assert [(row["done"], row["total"]) for row in counts.values()] == [(13, 13), (9, 9), (10, 11), (12, 12)]
checked = []
for path in [*sorted(PLAN.glob("*.md")), REPORT, JOURNAL]:
    for reference in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf8")):
        if reference.startswith(("http:", "https:", "#", "mailto:", "codex:")):
            continue
        target = (path.parent / reference.split("#", 1)[0]).resolve()
        assert target.exists(), str(path) + " missing local target " + reference
        checked.append({"document": path.relative_to(WORK).as_posix(), "reference": reference})
write_new(RUN / "plan-reconciliation.json", {
    "timestamp_utc": datetime.now(timezone.utc).isoformat(), "status": "in-progress", "tasks": "44/45",
    "phases": counts, "full_native_gate": "unchecked", "source_revision": 37, "source_lock_hash": verified["source_lock_hash"],
    "docs": [{"path": path.relative_to(WORK).as_posix(), "before_sha256": before[str(path)], "after_sha256": sha(path)} for path in paths],
    "report": bind(REPORT), "todo": bind(RUN / "native-continuation-todo.json"),
    "local_links_checked": len(checked), "link_evidence_class": "structural only", "local_checkpoint_reused": True,
    "broad_tests_rerun": False, "index_reindex_performed": False, "native45_scope": verified["event_scope"],
    "verifier": bind(Path(__file__)),
})
print(json.dumps({"status": "in-progress", "tasks": "44/45", "local_links": len(checked),
    "native45": verified["status"], "process_union": 2008, "live": 0}))
