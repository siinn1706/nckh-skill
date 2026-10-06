"""Record the reviewed inactive proposal and retain the pending native acceptance."""

import hashlib
import json
import re
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}
record = read(RUN / "verified-plugin-proposal.json")
proposal = read(RUN / "plugin-proposal.json")
audit = read(RUN / "process-final-audit.json")
assert record["status"] == "verified-inactive-proposal-static-preparation-only"
assert audit["matching_count"] == audit["tracked_live_count"] == 0
assert not proposal["executed"] and proposal["provider_prompts"] == 0
name = "proposal-261006-0135-r37-codex-plugin-cache-scope"
report = WORK / "plans/reports" / (name + ".md")
assert report.exists()
paragraph = (
    f"[Codex project/plugin proposal41](../reports/{name}.md) is verified inactive:33 proposal files,26 unchanged r37 payload files,18 Python files compiled in memory,10 Windows argv roundtrips; zero hook/model executions and no installation. Native help/schema confirms project/plugin source metadata and keyed plugin uninstall with local-cache removal. Cache authority outside workspace remains a separate plan gate; Windows PLUGIN_ROOT delivery requires a genuine callback before any model turn. Final process union{len(audit['tracked'])} identities/zero live/no process stop. Full native task stays unchecked/44 of45/P3 active."
)
targets = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md",
    WORK / "plans/journals/2026-10-06-private-search-and-native-app-availability.md"]
preimages = []
for index, path in enumerate(targets):
    content = path.read_text(encoding="utf8")
    assert name not in content
    preimage = RUN / "document-preimages" / (str(index) + "-" + path.name)
    preimage.parent.mkdir(exist_ok=True)
    with preimage.open("xb") as stream:
        stream.write(path.read_bytes())
    preimages.append({"target_preimage": bind(path), "backup": bind(preimage)})
    if index == 0:
        needle = "## Remaining acceptance và rollback"
        assert content.count(needle) == 1
        content = content.replace(needle, paragraph + "\n\n" + needle)
    else:
        content += "\n\n## Codex project/plugin route preparation\n\n" + paragraph + "\n"
    path.write_text(content, encoding="utf8")
todo = read(RUN.parent / "nckh-native-261006-0125-r37-codex-patch-faults-attempt-40/native-continuation-todo.json")
todo["plugin_route_readonly_scoping"] = {
    "status": "verified-inactive-awaiting-test-cache-authority",
    "proposal": bind(RUN / "plugin-proposal.json"), "verification": bind(RUN / "verified-plugin-proposal.json"),
    "approval_scope": bind(report), "native_installation": "not-performed", "model_prompts": 0,
    "next_prerequisites": "user authority for exact native cache/metadata; real hooks/list and lifecycle pair before one model turn",
    "Windows_PLUGIN_ROOT": "native delivery unverified",
}
todo["process_state"] = f"native41 read-only final union{len(audit['tracked'])} zero matching/tracked-live; no owned native sessions active"
todo["final_process_audit"] = bind(RUN / "process-final-audit.json")
todo["pending_cache_permission"] = "not-yet-requested; concrete scope prepared; do not install before direct user authorization"
todo["Claude_selection"] = "existing asynchronous model/effort clarification remains unanswered; no Claude model prompt sent"
target = RUN / "native-continuation-todo.json"
with target.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(todo, ensure_ascii=False, indent=2) + "\n")
links = []
for path in [*targets, report]:
    for reference in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf8")):
        if reference.startswith(("https://", "http://", "mailto:", "#")):
            continue
        assert (path.parent / reference.strip("<>").split("#", 1)[0]).resolve().exists(), (path, reference)
        links.append({"document": path.relative_to(WORK).as_posix(), "target": reference})
result = {
    "status": "reconciled-inactive-native41-proposal-gate-open",
    "source_revision": 37, "source_lock_hash": proposal["source_lock_hash"], "source_update": "not-performed",
    "done_tasks": 44, "total_tasks": 45, "current_phase": 3, "full_native_gate": "unchecked",
    "documents": [bind(path) for path in targets], "preimages": preimages, "approval_scope": bind(report),
    "pending_scope": bind(target), "proposal": bind(RUN / "plugin-proposal.json"),
    "verification": bind(RUN / "verified-plugin-proposal.json"), "process_audit": bind(RUN / "process-final-audit.json"),
    "links_checked": len(links), "verification_scope": "static preparation and documentation links only; no new native qualification",
    "previous_reconciliation": bind(RUN.parent / "nckh-native-261006-0125-r37-codex-patch-faults-attempt-40/plan-reconciliation.json"),
    "verifier": bind(Path(__file__)),
}
with (RUN / "proposal-reconciliation.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": result["status"], "links_checked": len(links), "plan_tasks": "44/45"}))
