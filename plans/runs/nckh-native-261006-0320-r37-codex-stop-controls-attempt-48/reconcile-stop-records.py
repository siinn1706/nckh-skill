"""Append scoped Stop evidence while preserving acceptance and historical failures."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PRIOR = RUN.parent / "nckh-native-261006-0253-r37-codex-posttool-controls-attempt-47"
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
REPORT = WORK / "plans/reports/delivery-261006-0320-r37-codex-stop-controls.md"
JOURNAL = WORK / "plans/journals/2026-10-06-private-search-and-native-app-availability.md"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}


def save_new(path, value):
    with path.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


verified = read(RUN / "verified-stop-observations.json")
assert verified["status"] == "verified-current-Codex-stop-patch-controls-and-fault-observations"
assert verified["model_turns"] == verified["actual_native_patches"] == 7
assert all(row["native_message_matches_final_frame"] for row in verified["results"])
paths = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "native-evidence-history.md", JOURNAL]
contents = {path: path.read_text(encoding="utf8") for path in paths}
before = {str(path): sha(path) for path in paths}
preimages = RUN / "document-preimages"
preimages.mkdir(exist_ok=False)
for path in paths:
    with (preimages / path.name).open("xb") as stream:
        stream.write(path.read_bytes())
summary = (
    "[Codex current-patch Stop48](../reports/delivery-261006-0320-r37-codex-stop-controls.md) "
    "verifies seven GPT5.6Luna/medium turns/seven canonical add-file patches on CLI0.154.0:35 callbacks/32 receipts, "
    "marker already present at every selected Stop entry. Native message hashes match final23-byte replies and stop_hook_active=false; "
    "one Stop each, repeated-reminder behavior unqualified. Advisory/bounded block/malformed-input produce empty Stop wire; "
    "five injected faults retain their outcomes. Enforcement/rollback/scientific QA unqualified. Native/controller exit0, "
    "cleanup26/preserved655/final union2310 zero live; protected global hashes unchanged/no new trust key. Source r37 unchanged;44/45/P3 active."
)
index = PLAN / "plan.md"
text = contents[index]
old = '| Codex | [Patch faults40](../reports/delivery-261006-0125-r37-codex-patch-faults.md), [PostToolUse47](../reports/delivery-261006-0253-r37-codex-posttool-controls.md) | Current-patch Stop cells and [plugin cache scope41](../reports/proposal-261006-0135-r37-codex-plugin-cache-scope.md) remain open |'
new = '| Codex | [Patch faults40](../reports/delivery-261006-0125-r37-codex-patch-faults.md), [PostToolUse47](../reports/delivery-261006-0253-r37-codex-posttool-controls.md), [Stop48](../reports/delivery-261006-0320-r37-codex-stop-controls.md) | Stop emits empty wire; repeat behavior unqualified; [plugin cache scope41](../reports/proposal-261006-0135-r37-codex-plugin-cache-scope.md) remains open |'
assert text.count(old) == 1
text = text.replace(old, new)
old = 'Latest native47:7 turns/7 patches/35 callbacks/32 receipts; marker already written at each post callback. Cleanup26/preserved538/final union2164 zero live; source r37 and protected global hashes unchanged. Full native task remains unchecked.'
new = 'Latest native48:7 turns/7 patches/35 callbacks/32 receipts; exact marker and final-message hash observed at Stop, one callback each. Cleanup26/preserved655/final union2310 zero live; source r37 and protected global hashes unchanged. Full native task remains unchecked.'
assert text.count(old) == 1
index.write_text(text.replace(old, new), encoding="utf8")
for path in paths[1:]:
    assert "Codex current-patch Stop48" not in contents[path]
    path.write_text(contents[path].rstrip() + "\n\n## Codex current-patch Stop observations\n\n" + summary + "\n", encoding="utf8")
todo = read(PRIOR / "native-continuation-todo.json")
todo["process_state"] = "native48 controller and seven native invocations exit0; final union2310 zero matching/tracked-live; no process stop"
todo["latest_scoped_evidence"] = bind(RUN / "verified-stop-observations.json")
todo["final_process_audit"] = bind(RUN / "process-final-audit.json")
todo["current_verified_Codex_scopes"].append("current r37 canonical patch Stop48: advisory, bounded block and five injected faults; exact mutation before Stop; one callback/native final message hash per turn")
todo["Codex_current_patch_Stop"] = {"verification": bind(RUN / "verified-stop-observations.json"), "report": bind(REPORT),
    "turns": 7, "patches": 7, "callbacks": 35, "receipts": 32, "wire_scope": "empty JSON for selected advisory/block",
    "repeat_behavior": "unqualified; one callback each", "prevention_or_rollback": "unqualified", "scientific_QA": "unverified"}
todo["next_authorized_native_cell"] = "Inspect retained Cursor exact-file controls and frozen oracles before choosing a remaining current-r37 private Write or directory/glob search cell; existing Grok4.7/500k/xhigh/fastfalse dangerous grant retained. No identical failed retry without causal evidence."
todo["prior_turn_classification"] = "progress: seven genuine current native PostToolUse47 cases"
todo["current_turn_classification"] = "progress: seven genuine current native Stop48 cases"
todo["cache_permission_reconfirmation"] = {
    "mechanism": "request_user_input_async", "tool_result": {"accepted": True}, "user_answer": "not-received",
    "scope": bind(WORK / "plans/reports/proposal-261006-0135-r37-codex-plugin-cache-scope.md"),
    "installation": "not-performed", "elapsed_time_is_authority": False,
    "reason": "context recovery; existing pending outside-workspace cache/metadata gate",
}
todo["Claude_selection"] = "model/effort clarification reconfirmed asynchronously after context recovery, no direct answer; no Claude model prompt sent"
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
        target = (path.parent / reference.split("#", 1)[0]).resolve()
        assert target.exists(), str(path) + " missing target " + reference
        links += 1
save_new(RUN / "plan-reconciliation.json", {
    "timestamp_utc": datetime.now(timezone.utc).isoformat(), "status": "in-progress", "tasks": "44/45", "phases": counts,
    "source_revision": 37, "source_lock_hash": verified["source_lock_hash"], "full_native_gate": "unchecked",
    "docs": [{"path": path.relative_to(WORK).as_posix(), "before_sha256": before[str(path)], "after_sha256": sha(path),
        "preimage": bind(preimages / path.name)} for path in paths], "report": bind(REPORT),
    "todo": bind(RUN / "native-continuation-todo.json"), "local_links_checked": links,
    "link_evidence_class": "structural only", "broad_tests_rerun": False, "index_reindex_performed": False,
    "current_goal_turn": "progress; seven actual current native Stop cases", "verifier": bind(Path(__file__)),
})
print(json.dumps({"status": "in-progress", "tasks": "44/45", "local_links": links, "process_union": 2310, "live": 0}))
