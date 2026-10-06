"""Record partial directory evidence and correct stale current Write scope from retained bindings."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PRIOR = RUN.parent / "nckh-native-261006-0320-r37-codex-stop-controls-attempt-48"
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
REPORT = WORK / "plans/reports/delivery-261006-0345-r37-cursor-directory-search.md"
JOURNAL = WORK / "plans/journals/2026-10-06-private-search-and-native-app-availability.md"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}


def save_new(path, value):
    with path.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


verified = read(RUN / "verified-directory-observations.json")
assert verified["status"] == "verified-current-Cursor-directory-Grep-scopes-and-policy-observations"
write_path = WORK / "plans/reports/delivery-261005-2055-r37-cursor-selected-write.json"
write = read(write_path)
assert write["status"] == "verified-scoped-public-Write-and-private-Write-prevention"
case_path = WORK / write["case"]["path"]
assert sha(case_path) == write["case"]["sha256"]
case = read(case_path)
assert case["private_bytes_unchanged"] and case["private_successful_post_count"] == 0
assert case["selected_native_Write_denial_count"] == case["private_preflight_block_count"] == 1
assert case["public_requested_bytes_observed"]
faults_path = WORK / "plans/reports/delivery-261005-2125-r37-cursor-write-faults.json"
faults = read(faults_path)
assert faults["status"] == "verified-five-native-selected-Write-preflight-fault-observations" and faults["model_turns"] == 5
assert write["source_lock_hash"] == faults["source_lock_hash"] == verified["source_lock_hash"]
paths = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "native-evidence-history.md", JOURNAL]
contents = {path: path.read_text(encoding="utf8") for path in paths}
before = {str(path): sha(path) for path in paths}
preimages = RUN / "document-preimages"
preimages.mkdir(exist_ok=False)
for path in paths:
    with (preimages / path.name).open("xb") as stream:
        stream.write(path.read_bytes())
save_new(RUN / "current-scope-correction.json", {
    "reason": "current overview inherited private Write unqualified despite later native25/27 verification",
    "source_lock_hash": verified["source_lock_hash"], "private_Write": "native25 verified actual denial and unchanged bytes",
    "Write_faults": "native27 five verified faults", "source_bindings": [bind(write_path), bind(case_path), bind(faults_path)],
    "historical_reports_modified": False, "model_rerun": False, "original_oracles_regraded": False,
})
index = PLAN / "plan.md"
text = contents[index]
old = '| Cursor | [Private Grep39](../reports/delivery-261006-0110-r37-cursor-private-search.md), [workspace43](../reports/delivery-261006-0215-r37-cursor-workspace-startup.md), [kit-unsupported event45](../reports/delivery-261006-0300-r37-cursor-workspace-unsupported-event.md) | [Duplicate44](../reports/delivery-261006-0240-r37-cursor-workspace-duplicates.md) frozen oracle failed; plugin prompt/stop absent; directory/glob/private Write still unqualified |'
new = '| Cursor | [Write25](../reports/delivery-261005-2055-r37-cursor-selected-write.md), [Write faults27](../reports/delivery-261005-2125-r37-cursor-write-faults.md), [private Grep39](../reports/delivery-261006-0110-r37-cursor-private-search.md), [directory49](../reports/delivery-261006-0345-r37-cursor-directory-search.md), [workspace43](../reports/delivery-261006-0215-r37-cursor-workspace-startup.md), [kit-unsupported45](../reports/delivery-261006-0300-r37-cursor-workspace-unsupported-event.md) | [Duplicate44](../reports/delivery-261006-0240-r37-cursor-workspace-duplicates.md) frozen oracle failed; plugin prompt/stop absent; directory49 native failure witness and glob/root scope unqualified |'
assert text.count(old) == 1
text = text.replace(old, new)
old = 'Latest native48:7 turns/7 patches/35 callbacks/32 receipts; exact marker and final-message hash observed at Stop, one callback each. Cleanup26/preserved655/final union2310 zero live; source r37 and protected global hashes unchanged. Full native task remains unchecked.'
new = 'Latest native49:1 turn/2 actual directory Grep preflights/6 callbacks/6 receipts; public post and private deny wire/no post observed, explicit native denial response missing. Cleanup28/preserved899/final union2468 zero live; source r37/protected global hashes unchanged. Full native task remains unchecked.'
assert text.count(old) == 1
index.write_text(text.replace(old, new), encoding="utf8")
summary = (
    "[Cursor directory Grep49](../reports/delivery-261006-0345-r37-cursor-directory-search.md) verifies one Grok4.7/500k/xhigh/fastfalse "
    "turn on CLI2026.09.15-d2fe57e:two actual file_path directory scopes, public pre/post/manual and private deny wire/no post, "
    "six callbacks/six receipts. Native explicit failure witness missing, oracle partial; glob/root/enforcement remains unqualified. "
    "No retry/injection; unchanged fixtures, native/monitor exit0, cleanup28/preserved899/final union2468 zero live. "
    "Current private Write scope corrected from verified25/27; historical reports/oracles unchanged. Source r37 unchanged;44/45/P3 active."
)
for path in paths[1:]:
    assert "Cursor directory Grep49" not in contents[path]
    path.write_text(contents[path].rstrip() + "\n\n## Cursor directory scopes và current-scope correction\n\n" + summary + "\n", encoding="utf8")
todo = read(PRIOR / "native-continuation-todo.json")
todo["process_state"] = "native49 terminal78710 and monitor40483 exit0; final union2468 zero matching/tracked-live; no process stop"
todo["latest_scoped_evidence"] = bind(RUN / "verified-directory-observations.json")
todo["final_process_audit"] = bind(RUN / "process-final-audit.json")
todo["current_verified_Cursor_scopes"].extend([
    "private Write25 and five Write faults27 already verified r37; prior current-summary gap corrected from unchanged evidence",
    "directory Grep49: actual public/private file_path directories; public post/manual, private deny wire/no post; native explicit failure response missing",
])
todo["Cursor_directory_Grep"] = {"verification": bind(RUN / "verified-directory-observations.json"), "report": bind(REPORT),
    "native_enforcement": "unqualified; explicit native failure response missing", "oracle": "partial", "glob_root_scope": "unqualified"}
todo["next_authorized_native_cell"] = "One private-directory Grep with bounded native postToolUseFailure diagnostic from verified25; this evidence-gathering change addresses missing actual native failure witness49. Preserve oracle49 and no identical retry without this causal change."
todo["current_turn_classification"] = "progress: seven native Stop48 cases and actual Cursor directory scopes49; historical Write25/27 scope corrected"
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
    "scope_correction": bind(RUN / "current-scope-correction.json"), "local_links_checked": links, "link_evidence_class": "structural only",
    "broad_tests_rerun": False, "index_reindex_performed": False, "current_goal_turn": "progress", "verifier": bind(Path(__file__)),
})
print(json.dumps({"status": "in-progress", "tasks": "44/45", "local_links": links, "process_union": 2468, "live": 0}))
