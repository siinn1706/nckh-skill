"""Bind the independent route inspection and the requested cache authority."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
PRIOR = RUN.parent / "nckh-native-261006-0135-r37-codex-plugin-routing-attempt-41"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}
assert read(RUN / "verified-workspace-route-inspection.json")["status"] == "verified-readonly-source-route-observation-not-native-qualification"
name = "inspection-261006-0200-r37-cursor-workspace-plugin-route"
report = WORK / "plans/reports" / (name + ".md")
scope = WORK / "plans/reports/proposal-261006-0135-r37-codex-plugin-cache-scope.md"
question = {
    "status": "requested-awaiting-direct-user-answer", "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
    "request_tool": "functions.request_user_input_async", "tool_result": {"accepted": True},
    "approval_scope": bind(scope), "proposal": bind(PRIOR / "plugin-proposal.json"),
    "requested_authority": "native creation/removal of exact test plugin cache and native metadata for nckh-native-hook-probe@nckh-native-project-plugins",
    "answer_received": False, "permission_inferred": False, "native_installation": "not-performed",
}
with (RUN / "cache-authority-request.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(question, ensure_ascii=False, indent=2) + "\n")
todo = read(PRIOR / "native-continuation-todo.json")
todo["pending_cache_permission"] = "explicit asynchronous question submitted; direct user answer required; elapsed time is not authorization"
todo["cache_authority_request"] = bind(RUN / "cache-authority-request.json")
todo["Cursor_workspace_route_inspection"] = {
    "verification": bind(RUN / "verified-workspace-route-inspection.json"), "report": bind(report),
    "status": "native trigger/loading unqualified; current vendor normalization/validation/aggregation observed", "model_prompts": 0,
}
todo["latest_plan_tasks"] = "44/45"
with (RUN / "native-continuation-todo.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(todo, ensure_ascii=False, indent=2) + "\n")
paragraph = (
    f"[Cursor workspace route42](../reports/{name}.md) verifies a read-only observation of the same installed vendor hash:workspaceOpen/pluginPaths literals are in shared parser/response code; no native trigger/loading qualification, new CLI process or model prompt. Native19/21 missing prompt/stop plugin callbacks remain unqualified. [Current pending scope](../runs/{RUN.name}/native-continuation-todo.json) records the explicit native41 cache-authority question awaiting a direct answer and the existing unanswered Claude model/effort selection. Full native task remains unchecked/44 of45/P3 active."
)
targets = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md",
    WORK / "plans/journals/2026-10-06-private-search-and-native-app-availability.md"]
preimages = []
for index, path in enumerate(targets):
    content = path.read_text(encoding="utf8")
    assert name not in content
    backup = RUN / "document-preimages" / (str(index) + "-" + path.name)
    backup.parent.mkdir(exist_ok=True)
    with backup.open("xb") as stream:
        stream.write(path.read_bytes())
    preimages.append({"target_preimage": bind(path), "backup": bind(backup)})
    if index == 0:
        needle = "## Remaining acceptance và rollback"
        assert content.count(needle) == 1
        content = content.replace(needle, paragraph + "\n\n" + needle)
    else:
        content += "\n\n## Cursor workspace route inspection\n\n" + paragraph + "\n"
    path.write_text(content, encoding="utf8")
counts = []
for path in sorted(PLAN.glob("phase-*.md")):
    text = path.read_text(encoding="utf8")
    counts.append({"phase": path.name, "done": len(re.findall(r"^\s*- \[[xX]\]", text, re.M)),
        "total": len(re.findall(r"^\s*- \[[ xX]\]", text, re.M))})
assert [(row["done"], row["total"]) for row in counts] == [(13, 13), (9, 9), (10, 11), (12, 12)]
links = []
for path in [*targets, report, scope]:
    for reference in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf8")):
        if reference.startswith(("https://", "http://", "mailto:", "#")):
            continue
        assert (path.parent / reference.strip("<>").split("#", 1)[0]).resolve().exists(), (path, reference)
        links.append({"document": path.relative_to(WORK).as_posix(), "target": reference})
result = {
    "status": "reconciled-native41-proposal-and-native42-inspection-gates-open",
    "done_tasks": 44, "total_tasks": 45, "current_phase": 3, "full_native_gate": "unchecked",
    "counts": counts, "links_checked": len(links), "verification_scope": "documentation links and unchanged task count; no native qualification",
    "documents": [bind(path) for path in targets], "preimages": preimages, "report": bind(report),
    "latest_pending_scope": bind(RUN / "native-continuation-todo.json"), "permission_request": bind(RUN / "cache-authority-request.json"),
    "source_inspection": bind(RUN / "verified-workspace-route-inspection.json"),
    "native41_static_reconciliation": bind(PRIOR / "proposal-reconciliation.json"),
    "owned_native_process_audit": bind(PRIOR / "process-final-audit.json"),
    "owned_native_process_count": 1163, "owned_native_processes_live": 0,
    "additional_native_CLI_processes": 0, "additional_model_prompts": 0,
    "source_update": "not-performed", "installed_update": "not-performed", "verifier": bind(Path(__file__)),
}
with (RUN / "plan-reconciliation.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": result["status"], "plan_tasks": "44/45", "links_checked": len(links)}))
