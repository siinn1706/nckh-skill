"""Reconcile the new native denial witness while preserving the partial earlier oracle."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PRIOR = RUN.parent / "nckh-native-261006-0345-r37-cursor-directory-search-attempt-49"
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
REPORT = WORK / "plans/reports/delivery-261006-0400-r37-cursor-directory-denial.md"
JOURNAL = WORK / "plans/journals/2026-10-06-private-search-and-native-app-availability.md"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}


def save_new(path, value):
    with path.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


verified = read(RUN / "verified-directory-denial.json")
assert verified["status"] == "verified-current-Cursor-private-directory-Grep-native-denial"
assert verified["model_turns"] == verified["actual_native_tool_requests"] == 1
assert verified["native49_regraded"] is False
paths = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "native-evidence-history.md", JOURNAL]
contents = {path: path.read_text(encoding="utf8") for path in paths}
before = {str(path): sha(path) for path in paths}
preimages = RUN / "document-preimages"
preimages.mkdir(exist_ok=False)
for path in paths:
    with (preimages / path.name).open("xb") as stream:
        stream.write(path.read_bytes())
index = PLAN / "plan.md"
text = contents[index]
old = '[directory49](../reports/delivery-261006-0345-r37-cursor-directory-search.md)'
new = '[directory49/50](../reports/delivery-261006-0400-r37-cursor-directory-denial.md)'
assert text.count(old) == 1
text = text.replace(old, new)
old = 'directory49 native failure witness and glob/root scope unqualified'
new = 'glob/root and remaining native cells unqualified; original directory49 oracle partial'
assert text.count(old) == 1
text = text.replace(old, new)
old = 'Latest native49:1 turn/2 actual directory Grep preflights/6 callbacks/6 receipts; public post and private deny wire/no post observed, explicit native denial response missing. Cleanup28/preserved899/final union2468 zero live; source r37/protected global hashes unchanged. Full native task remains unchecked.'
new = 'Latest native50:1 turn/1 private-directory Grep/5 callbacks/4 receipts; native permission_denied matches preflight tool ID/session/path/version. Cleanup27/preserved921/final union2592 zero live; source r37/protected global hashes unchanged. Full native task remains unchecked.'
assert text.count(old) == 1
index.write_text(text.replace(old, new), encoding="utf8")
summary = (
    "[Cursor private-directory denial50](../reports/delivery-261006-0400-r37-cursor-directory-denial.md) verifies one "
    "Grok4.7/500k/xhigh/fastfalse turn/one native Grep on CLI2026.09.15-d2fe57e:four policy callbacks/receipts plus "
    "actual postToolUseFailure permission_denied/private-holdout-credential-path, same tool ID/session/path/version as preflight. "
    "No successful post, unchanged exact fixture and final reply; no injection/retry. Native/monitor exit0, cleanup27/preserved921/"
    "final union2592 zero live/protected global hashes unchanged. Added native diagnostic addresses missing witness49 without regrading it; "
    "exact directory qualified, glob/root/direct5s/all-tools remain unqualified. Source r37 unchanged;44/45/P3 active."
)
for path in paths[1:]:
    assert "Cursor private-directory denial50" not in contents[path]
    path.write_text(contents[path].rstrip() + "\n\n## Cursor exact directory native denial\n\n" + summary + "\n", encoding="utf8")
todo = read(PRIOR / "native-continuation-todo.json")
todo["process_state"] = "native50 terminal25793 and monitor61453 exit0; final union2592 zero matching/tracked-live; no process stop"
todo["latest_scoped_evidence"] = bind(RUN / "verified-directory-denial.json")
todo["final_process_audit"] = bind(RUN / "process-final-audit.json")
todo["current_verified_Cursor_scopes"].append("private-directory Grep50 actual native permission_denied with matching preflight identity; normal producer20s bound, bounded diagnostic; original49 partial preserved")
todo["Cursor_directory_Grep"]["native50_verification"] = bind(RUN / "verified-directory-denial.json")
todo["Cursor_directory_Grep"]["native50_report"] = bind(REPORT)
todo["Cursor_directory_Grep"]["native_enforcement"] = "verified exact private directory in native50; original49 remains partial"
todo["next_authorized_native_cell"] = "Inspect retained Cursor search event/fault records before selecting genuinely missing current-r37 directory-Grep fault cells with native diagnostic; preserve source/timing and unknown/glob/root limits. Cache-authority and Claude model/effort decisions remain pending."
todo["current_turn_classification"] = "progress: native48 Stop cases, native49 directory scope observations and native50 actual private-directory denial; current Write scope corrected from25/27"
save_new(RUN / "native-continuation-todo.json", todo)
counts = {}
for path in sorted(PLAN.glob("phase-*.md")):
    items = re.findall(r"^\s*- \[([ xX])\]", path.read_text(encoding="utf8"), re.MULTILINE)
    counts[path.name] = {"done": sum(item.lower() == "x" for item in items), "total": len(items)}
assert [(row["done"], row["total"]) for row in counts.values()] == [(13, 13), (9, 9), (10, 11), (12, 12)]
links = 0
for path in [*sorted(PLAN.glob("*.md")), REPORT, JOURNAL]:
    for reference in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf8")):
        if reference.startswith(("http:", "https:", "#", "mailto:", "codex:")):
            continue
        assert (path.parent / reference.split("#", 1)[0]).resolve().exists(), str(path) + " missing link " + reference
        links += 1
save_new(RUN / "plan-reconciliation.json", {
    "timestamp_utc": datetime.now(timezone.utc).isoformat(), "status": "in-progress", "tasks": "44/45", "phases": counts,
    "source_revision": 37, "source_lock_hash": verified["source_lock_hash"], "full_native_gate": "unchecked",
    "docs": [{"path": path.relative_to(WORK).as_posix(), "before_sha256": before[str(path)], "after_sha256": sha(path),
        "preimage": bind(preimages / path.name)} for path in paths], "report": bind(REPORT), "todo": bind(RUN / "native-continuation-todo.json"),
    "local_links_checked": links, "link_evidence_class": "structural only", "broad_tests_rerun": False, "index_reindex_performed": False,
    "current_goal_turn": "progress", "verifier": bind(Path(__file__)),
})
print(json.dumps({"status": "in-progress", "tasks": "44/45", "local_links": links, "process_union": 2592, "live": 0}))
