"""Reconcile scoped evidence and keep the plan overview short without removing history."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PRIOR = RUN.parent / "nckh-native-261006-0330-r37-agy-tool-route-inspection-attempt-46"
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
REPORT = WORK / "plans/reports/delivery-261006-0253-r37-codex-posttool-controls.md"
JOURNAL = WORK / "plans/journals/2026-10-06-private-search-and-native-app-availability.md"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}

def save_new(path, value):
    with path.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

verified = read(RUN / "verified-posttool-observations.json")
assert verified["status"] == "verified-current-Codex-posttool-patch-controls-and-fault-observations"
assert verified["model_turns"] == verified["actual_native_patches"] == 7
paths = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "native-evidence-history.md", JOURNAL]
before = {str(path): sha(path) for path in paths}
contents = {path: path.read_text(encoding="utf8") for path in paths}
preimages = RUN / "document-preimages"
preimages.mkdir(exist_ok=False)
for path in paths:
    target = preimages / path.name
    with target.open("xb") as stream:
        stream.write(path.read_bytes())
summary = (
    "[Codex current-patch PostToolUse47](../reports/delivery-261006-0253-r37-codex-posttool-controls.md) "
    "verifies seven GPT5.6Luna/medium turns/seven actual canonical add-file patches on CLI0.154.0:35 callbacks/32 receipts, "
    "exact bytes already present at each selected post callback. Normal binding advisory, bounded policy block and five injected faults "
    "all retain completed mutations; preventive rollback/scientific QA unqualified. Native/controller exit0, cleanup26/preserved538/"
    "final union2164 zero live, global hashes unchanged/no new trust key. Source r37 unchanged;44/45/P3 active."
)
index = PLAN / "plan.md"
text = contents[index]
start = text.index("## Current CLI route and native evidence")
end = text.index("## Remaining acceptance và rollback", start)
retained = text[start:end].rstrip()
history = PLAN / "native-evidence-history.md"
history_text = contents[history]
assert "## Native continuation retained at native47" not in history_text
retained = retained.replace("## Current CLI route and native evidence", "### Retained CLI observations before native47", 1)
history.write_text(history_text.rstrip() + "\n\n## Native continuation retained at native47\n\n"
    + "The following scope records were moved from the plan overview without changing their outcomes or source bindings. "
    + "Current acceptance remains in plan.md and the phase records.\n\n" + retained + "\n\n### Current patch post-tool observations\n\n" + summary + "\n", encoding="utf8")
compact = '''## Current CLI route and native evidence

AGY CLI1.2.17/Gemini3.8FlashMedium and Cursor CLI/Grok4.7/500k/xhigh/fast=false dangerous use the existing grants. Codex uses GPT5.6Luna/medium. Exact scopes, revisions, failures, cleanup and timing remain in [native history](./native-evidence-history.md) and [P3](./phase-03-portable-hooks.md).

| Host | Current scoped evidence | Remaining limits |
|---|---|---|
| AGY | [Direct controls29](../reports/delivery-261005-2210-r37-agy-cli-controls.md), [event faults34/36](../reports/delivery-261005-2320-r37-agy-event-observations.md), [duplicates37](../reports/delivery-261005-2355-r37-agy-duplicate-admission.md), [shell38](../reports/delivery-261006-0010-r37-agy-shell-control.md) | [Search35](../reports/delivery-261005-2335-r37-agy-search-gaps.md) failed/unqualified; [inventory46](../reports/inspection-261006-0330-r37-agy-tool-routes.md) does not establish callable tools |
| Cursor | [Private Grep39](../reports/delivery-261006-0110-r37-cursor-private-search.md), [workspace43](../reports/delivery-261006-0215-r37-cursor-workspace-startup.md), [kit-unsupported event45](../reports/delivery-261006-0300-r37-cursor-workspace-unsupported-event.md) | [Duplicate44](../reports/delivery-261006-0240-r37-cursor-workspace-duplicates.md) frozen oracle failed; plugin prompt/stop absent; directory/glob/private Write still unqualified |
| Codex | [Patch faults40](../reports/delivery-261006-0125-r37-codex-patch-faults.md), [PostToolUse47](../reports/delivery-261006-0253-r37-codex-posttool-controls.md) | Current-patch Stop cells and [plugin cache scope41](../reports/proposal-261006-0135-r37-codex-plugin-cache-scope.md) remain open |

Latest native47:7 turns/7 patches/35 callbacks/32 receipts; marker already written at each post callback. Cleanup26/preserved538/final union2164 zero live; source r37 and protected global hashes unchanged. Full native task remains unchecked.

'''
index.write_text(text[:start] + compact + text[end:], encoding="utf8")
for path in (PLAN / "phase-03-portable-hooks.md", JOURNAL):
    text = contents[path]
    assert "Codex current-patch PostToolUse47" not in text
    path.write_text(text.rstrip() + "\n\n## Codex current-patch post-tool observations\n\n" + summary + "\n", encoding="utf8")
todo = read(PRIOR / "native-continuation-todo.json")
todo["process_state"] = "native47 controller and seven native invocations exit0; final union2164 zero matching/tracked-live; no process stop"
todo["latest_scoped_evidence"] = bind(RUN / "verified-posttool-observations.json")
todo["final_process_audit"] = bind(RUN / "process-final-audit.json")
todo["current_verified_Codex_scopes"].append("current r37 canonical patch PostToolUse47: normal binding, bounded policy block and five injected faults; exact mutation before selected callback")
todo["Codex_current_patch_posttool"] = {"verification": bind(RUN / "verified-posttool-observations.json"), "report": bind(REPORT),
    "turns": 7, "patches": 7, "callbacks": 35, "receipts": 32, "prevention_or_rollback": "unqualified", "scientific_QA": "unverified"}
todo["next_authorized_native_cell"] = "Codex current r37 canonical-patch Stop event allow/policy-block/fault cells, using existing workspace trust and GPT5.6Luna/medium grant; preserve r34 shell timing observations"
todo["prior_turn_classification"] = "progress from genuine native45 workspace continuation; native46 refreshes inventory already observed33 and does not establish a changed tool route"
todo["AGY_native_agent_inventory"]["historical_inventory"] = "native33 already observed16 agent names; native46 refresh only, no callable-tool or selected-agent claim"
save_new(RUN / "native-continuation-todo.json", todo)
counts = {}
for path in sorted(PLAN.glob("phase-*.md")):
    items = re.findall(r"^\s*- \[([ xX])\]", path.read_text(encoding="utf8"), re.MULTILINE)
    counts[path.name] = {"done": sum(item.lower() == "x" for item in items), "total": len(items)}
assert [(row["done"], row["total"]) for row in counts.values()] == [(13, 13), (9, 9), (10, 11), (12, 12)]
checked = 0
for path in [*sorted(PLAN.glob("*.md")), REPORT, JOURNAL]:
    for reference in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf8")):
        if reference.startswith(("http:", "https:", "#", "mailto:", "codex:")):
            continue
        target = (path.parent / reference.split("#", 1)[0]).resolve()
        assert target.exists(), str(path) + " missing local target " + reference
        checked += 1
save_new(RUN / "plan-reconciliation.json", {
    "timestamp_utc": datetime.now(timezone.utc).isoformat(), "status": "in-progress", "tasks": "44/45", "phases": counts,
    "source_revision": 37, "source_lock_hash": verified["source_lock_hash"], "full_native_gate": "unchecked",
    "docs": [{"path": path.relative_to(WORK).as_posix(), "before_sha256": before[str(path)], "after_sha256": sha(path),
        "preimage": bind(preimages / path.name)} for path in paths],
    "overview_reorganization": "native scope paragraphs moved intact to history; all acceptance/state/counts preserved",
    "report": bind(REPORT), "todo": bind(RUN / "native-continuation-todo.json"), "local_links_checked": checked,
    "link_evidence_class": "structural only", "broad_tests_rerun": False, "index_reindex_performed": False,
    "prior_goal_turn": "progress", "current_goal_turn": "progress; seven actual current native post-tool cases", "verifier": bind(Path(__file__)),
})
print(json.dumps({"status": "in-progress", "tasks": "44/45", "local_links": checked, "process_union": 2164, "live": 0}))
