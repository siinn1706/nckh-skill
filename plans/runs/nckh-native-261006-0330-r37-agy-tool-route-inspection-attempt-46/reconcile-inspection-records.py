"""Record native discovery and its limits while retaining the open acceptance gates."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PRIOR = RUN.parent / "nckh-native-261006-0300-r37-cursor-workspace-unsupported-event-attempt-45"
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
REPORT = WORK / "plans/reports/inspection-261006-0330-r37-agy-tool-routes.md"
JOURNAL = WORK / "plans/journals/2026-10-06-private-search-and-native-app-availability.md"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}

def save_new(path, value):
    with path.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

verified = read(RUN / "verified-cli-inspection.json")
assert verified["status"] == "verified-read-only-native-AGY-help-and-agent-inventory"
assert verified["process_union_identities"] == 2018 and verified["processes_live"] == 0
paths = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", JOURNAL]
before = {str(path): sha(path) for path in paths}
summary = (
    "[AGY tool-route inspection46](../reports/inspection-261006-0330-r37-agy-tool-routes.md) "
    "records four read-only native CLI1.2.17 commands/exit0 and16 registered agents. --agent is exposed; "
    "per-agent callable tool mapping/effective selection remains unqualified. Zero model/tool requests and hook activation; "
    "search35 failures retained. Final union2018 zero live/protected config hashes unchanged. Source r37 unchanged;44/45/P3 active."
)
for path in paths:
    text = path.read_text(encoding="utf8")
    assert "AGY tool-route inspection46" not in text
    if path.name == "plan.md":
        marker = "## Remaining acceptance và rollback"
        assert text.count(marker) == 1
        text = text.replace(marker, summary + "\n\n" + marker)
    else:
        text = text.rstrip() + "\n\n## AGY native tool-route inspection\n\n" + summary + "\n"
    path.write_text(text, encoding="utf8")
todo = read(PRIOR / "native-continuation-todo.json")
todo["process_state"] = "native46 four read-only commands exit0; final union2018 zero matching/tracked-live; no process stop"
todo["latest_scoped_evidence"] = bind(RUN / "verified-cli-inspection.json")
todo["final_process_audit"] = bind(RUN / "process-final-audit.json")
todo["AGY_native_agent_inventory"] = {
    "verification": bind(RUN / "verified-cli-inspection.json"), "report": bind(REPORT),
    "version": "1.2.17", "agent_count": 16, "selector": "--agent",
    "effective_agent": "unqualified; no session started", "callable_toolset": "unqualified", "model_prompts": 0,
}
todo["retry_boundaries"].append("Do not infer callable AGY search/multi-replace tools from advertised init names or the native agent inventory; require new causal evidence before repeating identical prompts")
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
    "full_native_gate": "unchecked", "source_revision": 37, "source_lock_hash": verified["source_lock_hash"],
    "docs": [{"path": path.relative_to(WORK).as_posix(), "before_sha256": before[str(path)], "after_sha256": sha(path)} for path in paths],
    "report": bind(REPORT), "todo": bind(RUN / "native-continuation-todo.json"), "local_links_checked": checked,
    "link_evidence_class": "structural only", "broad_tests_rerun": False, "index_reindex_performed": False,
    "native45_delivery": bind(PRIOR / "verified-unsupported-event-observations.json"), "verifier": bind(Path(__file__)),
})
print(json.dumps({"status": "in-progress", "tasks": "44/45", "local_links": checked, "process_union": 2018, "live": 0}))
