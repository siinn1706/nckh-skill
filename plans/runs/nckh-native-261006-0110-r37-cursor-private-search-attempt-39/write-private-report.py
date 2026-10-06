"""Record a scoped native result and preserve the remaining acceptance gates."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
PRIOR = WORK / "plans/runs/nckh-native-261006-0010-r37-agy-shell-control-attempt-38"
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {"path": p.relative_to(WORK).as_posix(), "sha256": sha(p)}
record = read(RUN / "verified-private-search-delivery.json")
assert record["status"] == "verified-native-private-Grep-denial"
name = "delivery-261006-0110-r37-cursor-private-search"
report = WORK / "plans/reports" / (name + ".md")
assert not report.exists() and not report.with_suffix(".json").exists()
report.with_suffix(".json").write_bytes((RUN / "verified-private-search-delivery.json").read_bytes())
report.write_text(f"""# Cursor CLI r37: private Grep control

[Verified bindings](./{name}.json) record one actual native `Grep` request on CLI2026.09.15-d2fe57e. Existing selectedModel and terminal display confirm Grok4.7/context500k/xhigh/fastfalse/Run Everything. Legacy callback model strings do not attest effective backend parameters. Source r37/281 pins/hash `{record['source_lock_hash']}` unchanged.

The native preToolUse callback supplies the exact synthetic private `file_path` and a nonempty tool-use ID. The unchanged packaged runner returns permission deny/private-holdout-credential-path; the actual CLI displays `Error: private-holdout-credential-path` and its blocked-tool note. Four genuine callbacks/four policy receipts cover startup, prompt, preflight and stop; no successful search return or postToolUse callback is observed. The fixture has the same exact bytes before/after; the final response marker is observed. One prompt/one turn/no retries/no injected faults.

The context operation map remains empty. Policy checks protected paths before looking up that map, so this control adds private-path denial evidence while the earlier public Grep manual result remains intact. Scope is an exact `file_path`; directory/glob/search-scope extraction and other tools are unqualified. A bounded observer forwards genuine input to the packaged runner: outer preToolUse20s, other handlers5s, inner runner5s. This is not direct producer5s search qualification.

Native /exit and monitor both exit0. Matching-byte cleanup removes27 config/payload/fixture members and preserves846 historical files/protected global configs. Final union1038 PID/creation FILETIME identities has zero matching/tracked-live; no taskkill. CLI-owned state hash changes are recorded without inferring the changed fields.

The user supplied the AGY app mention again. The current Computer Use API disables native computer access and returns apps=[]; its Chrome inventory also reports an unavailable Codex auth token. No AGY UI input was sent. This is a current tool-availability limitation, not evidence that the real application has no window. The existing authorized AGY CLI route is retained; AGY IDE qualification remains unverified.

Full native task remains **unchecked/44 of45/P3 active**. Remaining host/event/tool/fault/duplicate cells, genuine unsupported native-event delivery, Claude model/effort/turns and direct app qualification stay open. Exact r29 VI/EN owner acceptance, installed r25 and release boundaries remain unchanged. Review was inline; no independent reviewer.
""", encoding="utf8")
targets = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md"]
preimages = []
for index, target in enumerate(targets):
    text = target.read_text(encoding="utf8")
    preimage = RUN / "document-preimages" / (str(index) + "-" + target.name)
    preimage.parent.mkdir(exist_ok=True)
    assert not preimage.exists()
    preimage.write_bytes(target.read_bytes())
    preimages.append({"target": bind(target), "preimage": bind(preimage)})
    paragraph = (f"[Cursor private Grep39](../reports/{name}.md) verifies one actual private file_path search blocked before a successful return: four callbacks/four receipts, exact unchanged fixture, native exit0, cleanup27/preserved846/final union1038 identities/zero live. Observed20s/inner5s; public manual Grep remains historical and directory/glob scope is unqualified. AGY app mention retained; current Computer Use native APIs disabled, IDE unverified. Source r37 unchanged and full native task unchecked.")
    if index == 0:
        needle = "## Remaining acceptance và rollback"
        assert text.count(needle) == 1
        text = text.replace(needle, paragraph + "\n\n" + needle)
    else:
        text += "\n\n## Cursor private search and current AGY access\n\n" + paragraph + "\n"
    target.write_text(text, encoding="utf8")
journal = WORK / "plans/journals/2026-10-06-private-search-and-native-app-availability.md"
assert not journal.exists()
journal.write_text(f"""# Private search and native app availability

[Native39 delivery](../reports/{name}.md) binds the result and limits. An empty controller operation map does not bypass the private-path guard when the native payload exposes the exact file_path: protected paths are checked first. Public Grep manual behavior and this private denial are distinct observations.

Use the existing user-selected CLI routes while the active Computer Use capability disables native apps. An empty API app inventory is not an OS-window absence claim. Keep direct IDE qualification open and retain earlier access/unlock/dangerous permissions. Native CLI /exit completed cleanly; final process union1038 has zero live owned identities. Source r37 unchanged; plan44/45/P3 active.
""", encoding="utf8")
todo = read(PRIOR / "native-continuation-todo.json")
todo["current_verified_Cursor_scopes"] = ["private exact-file_path Grep denial39; previous public manual Grep24 retained"]
todo["current_UI_availability"] = "native computer APIs disabled; app mention retained, AGY IDE unverified"
todo["process_state"] = "zero owned live at native39 union1038 audit"
todo["latest_scoped_evidence"] = bind(RUN / "verified-private-search-delivery.json")
todo["Claude_selection"] = "existing asynchronous question pending; no Claude model prompt sent"
(RUN / "native-continuation-todo.json").write_text(json.dumps(todo, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
(RUN / "doc-update.json").write_text(json.dumps({"status": "reconciled-native39-private-search-report-and-pending-scope",
    "preimages": preimages, "documents": [bind(p) for p in targets] + [bind(journal)],
    "reports": [bind(report), bind(report.with_suffix(".json"))], "pending_scope": bind(RUN / "native-continuation-todo.json")}, indent=2) + "\n", encoding="utf8")
print(json.dumps({"status": "reconciled-native39-docs", "done_tasks": 44, "total_tasks": 45}), flush=True)
