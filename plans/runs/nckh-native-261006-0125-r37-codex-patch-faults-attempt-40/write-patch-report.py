"""Write revision-bound native observations and update the owning plan surfaces."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
PRIOR = WORK / "plans/runs/nckh-native-261006-0110-r37-cursor-private-search-attempt-39"
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {"path": p.relative_to(WORK).as_posix(), "sha256": sha(p)}
record = read(RUN / "verified-patch-fault-delivery.json")
assert record["status"] == "verified-five-native-codex-patch-fault-observations"
name = "delivery-261006-0125-r37-codex-patch-faults"
report = WORK / "plans/reports" / (name + ".md")
assert not report.exists() and not report.with_suffix(".json").exists()
report.with_suffix(".json").write_bytes((RUN / "verified-patch-fault-delivery.json").read_bytes())
report.write_text(f"""# Codex CLI r37: canonical patch fault observations

[Verified bindings](./{name}.json) bind five native apply_patch requests on Codex CLI0.154.0/exec, GPT-5.6Luna requested/medium. Callbacks report the model; effort/backend attestation is absent. Source r37/281 pins/hash `{record['source_lock_hash']}` unchanged. Each actual command hash matches the exact requested canonical public add-file patch. No alternative tools or model retries.

## Observed behavior

| Selected PreToolUse fault | Packaged/native observer output | Native file outcome |
|---|---|---|
| Malformed input | permissionDecision deny; block/hook-input-or-context-invalid | No file change, no marker, no post callback |
| Malformed output | Declared invalid native JSON | One completed add-file; exact marker |
| Timeout | Sleeper8s with outer5s; sleep snapshot, no selected preflight receipt | One completed add-file; exact marker |
| Crash | Intentional observer exit17 | One completed add-file; exact marker |
| Unsupported selected codec | Runner exit3/empty native JSON; deterministic block receipt | One completed add-file; exact marker |

These observations establish a scoped deny for malformed input and continued mutation for four other fault modes. Retained exec JSON does not expose native hook notification states; actual callback/file-change items and bytes are verified. The unsupported selected codec is injected after a genuine known native PreToolUse callback; genuine unsupported native-event delivery remains unqualified. PostToolUse artifact QA remains a separate pending check.

Five completed turns/final markers/native process exits0;24 callbacks/21 policy receipts. Outer and inner handlers5s, injected sleeper8s, no whole-turn deadline. Inline sessionFlags reuse the existing native-trusted scratch project and hook trust bypass for the invocation. No new project trust keys; raw global config/hooks hashes unchanged. Native plugin-catalog warmup/authentication warnings remain in stderr, without a plugin duplicate qualification claim.

Cleanup removes26 matching staged payload members and preserves451 historical files. Four synthetic marker artifacts and native observations are retained. Native40 audit binds1145 PID/creation FILETIME identities, zero matching/tracked-live/no taskkill. Later read-only CLI help commands are retained separately and require the final supplementary audit. AGY CLI help was read with zero model prompts; it writes its help on stderr and documents the already selected dangerous/print route. Codex plugin help exposes marketplace add/list/remove management; no marketplace addition or plugin installation was performed.

Full native task stays **unchecked/44 of45/P3 active**. Remaining actual event/tool/fault and project/plugin cells, Claude model/effort/native turns, genuine unsupported event and direct application qualification remain open. Exact r29 owner VI/EN samples and installed r25 boundaries retained. Review was inline; no independent reviewer.
""", encoding="utf8")
targets = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md",
    WORK / "plans/journals/2026-10-06-private-search-and-native-app-availability.md"]
preimages = []
paragraph = (f"[Codex patch faults40](../reports/{name}.md) verifies five actual canonical add-file calls on GPT5.6Luna/medium: malformed input has no mutation; malformed output/timeout/crash/unsupported selected codec each permit a completed file change.24 callbacks/21 receipts, native exits0, cleanup26/preserved451/union1145 identities/zero live at native checkpoint. Inline invocation definitions, no new trust key/source change. Remaining native task stays unchecked/44 of45/P3 active.")
for index, target in enumerate(targets):
    text = target.read_text(encoding="utf8")
    preimage = RUN / "document-preimages" / (str(index) + "-" + target.name)
    preimage.parent.mkdir(exist_ok=True)
    assert not preimage.exists()
    preimage.write_bytes(target.read_bytes())
    preimages.append({"target": bind(target), "preimage": bind(preimage)})
    if index == 0:
        needle = "## Remaining acceptance và rollback"
        assert text.count(needle) == 1
        text = text.replace(needle, paragraph + "\n\n" + needle)
    else:
        text += "\n\n## Codex native patch fault continuation\n\n" + paragraph + "\n"
    target.write_text(text, encoding="utf8")
todo = read(PRIOR / "native-continuation-todo.json")
todo["current_verified_Codex_scopes"] = ["canonical add-file PreToolUse faults40; malformed input deny and four continued mutations"]
todo["pending_or_unqualified"][2] = "remaining Codex/Cursor event-tool/fault and project/plugin duplicate cells; scoped Codex patch faults40 recorded"
todo["process_state"] = "native40 union1145 zero live; subsequent read-only help commands await supplementary union audit"
todo["latest_scoped_evidence"] = bind(RUN / "verified-patch-fault-delivery.json")
todo["plugin_route_readonly_scoping"] = {
    "codex_help": bind(RUN / "commands/codex-plugin-help.json"),
    "route": "marketplace management shown in live help; no registration/installation/duplicate experiment prepared",
    "AGY_help": bind(RUN / "commands/agy-cli-help.json"), "model_prompts": 0}
(RUN / "native-continuation-todo.json").write_text(json.dumps(todo, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
(RUN / "doc-update.json").write_text(json.dumps({"status": "reconciled-native40-patch-fault-report-and-pending-scope",
    "preimages": preimages, "documents": [bind(p) for p in targets], "reports": [bind(report), bind(report.with_suffix(".json"))],
    "pending_scope": bind(RUN / "native-continuation-todo.json")}, indent=2) + "\n", encoding="utf8")
print(json.dumps({"status": "reconciled-native40-docs", "done_tasks": 44, "total_tasks": 45}), flush=True)
