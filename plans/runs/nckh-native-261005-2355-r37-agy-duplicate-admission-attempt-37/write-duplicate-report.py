"""Reconcile the completed duplicate observations without closing unrelated gates."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {"path": p.relative_to(WORK).as_posix(), "sha256": sha(p)}
record = read(RUN / "verified-duplicate-delivery.json")
assert record["status"] == "verified-agy-five-event-duplicates-and-scoped-config-admission"
name = "delivery-261005-2355-r37-agy-duplicate-admission"
report = WORK / "plans/reports" / (name + ".md")
with report.with_suffix(".json").open("x", encoding="utf8") as stream:
    json.dump(record, stream, ensure_ascii=False, indent=2)
cleanup = read(RUN / "cleanup.json")
text = f"""# AGY CLI r37: five-event project/plugin duplicate và config admission

[Verified bindings](./{name}.json) ghi hai distinct conversations trên CLI1.2.17/Gemini3.8FlashMedium/always-proceed/effort medium requested. Source r37/281 pins/hash `{record['source_lock_hash']}` unchanged. Observer outer5s/inner5s; không fault injection/model retry/global plugin install.

## Project và workspace plugin

| Event | Actual callbacks | Matching same-input pairs | Policy receipts |
|---|---:|---:|---:|
| PreInvocation | 4 | 2 | 1 |
| PreToolUse | 2 | 1 | 1 |
| PostToolUse | 2 | 1 | 1 |
| PostInvocation | 4 | 2 | 1 |
| Stop | 2 | 1 | 1 |

14 genuine callbacks tạo bảy pairs. Mỗi pair có cùng native input SHA256, một source project và một source plugin; actual conversation hash, step index2 và TargetFile bind tool callbacks. Một native Write/DONE, đúng revised bytes/final marker/resultSUCCESS/num_turns1. Five policy files chứng minh idempotent receipt behavior; hai model-invocation cycles vẫn được phân biệt qua input hash, không gọi ordinary lifecycle repetition là controlled duplicate.

PostToolUse policy pending vì không declared artifact QA context; wire không rollback mutation. Callback duplication/receipt suppression không chứng minh scientific QA hoặc human acceptance. Native tool-use ID/backend/effort telemetry attestation absent; model alias and always-proceed are observed, medium bound to actual command.

## Unknown configured event

Second definition có `NckhUnsupportedNativeEvent` và five known event definitions. Native turn completes: seven known callbacks/five policy receipts, one Write/DONE/exact bytes/final marker, zero unknown callback. Không sửa runner input hoặc event sau supported callback. Đây là config-admission observation; không chứng minh host đã phát hoặc dispatch unknown native event, không tuyên bố full unsupported-event qualification.

## Cleanup và state

Two matching project-plugin files removed before second turn; final cleanup removes26 matching config/payload members, preserves{cleanup['historical_members_unchanged']} historical files/protected settings-hooks hashes. Union897 PID/creation FILETIME identities: zero matching/tracked-live, no taskkill. Final native process exits0; no owned daemon/listener left. Controller direct global write/plugin install/source update not performed. Verifier first attempt exit0, inline artifact review/no independent reviewer.

Combined native34–37: **34 user turns / 31 actual native tool requests**. Original partial34/failed search35 oracles and repairs remain bound. Plan **44 of45/P3 active/full native task unchecked**. Remaining host/tool/surface matrices, unknown native event delivery, Claude model/effort/turns and direct app qualification remain explicit. Installed r25 and exact r29 owner VI/EN acceptance retain prior state.
"""
with report.open("x", encoding="utf8") as stream:
    stream.write(text)
targets = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md",
    WORK / "plans/journals/2026-10-05-cursor-native-timeout-controls-and-r37-repair.md"]
preimages = []
for index, target in enumerate(targets):
    original = target.read_text(encoding="utf8")
    preimage = RUN / "document-preimages" / (str(index) + "-" + target.name)
    preimage.parent.mkdir(exist_ok=True)
    preimage.write_bytes(target.read_bytes())
    preimages.append({"target": bind(target), "preimage": bind(preimage)})
    if index == 0:
        original = original.replace("controlled duplicate/unsupported-event and remaining host/tool/surface cells",
            "unsupported-event and remaining host/tool/surface cells; AGY five-event duplicate verified")
        original = original.replace("final union836 identities/zero live", "final union897 identities/zero live")
        original = original.replace("New continuation:32 user turns/29 actual tools", "New continuation:34 user turns/31 actual tools")
        original = original.replace("and [search35 gaps]", "[AGY duplicate37](../reports/" + name + ".md) and [search35 gaps]")
    else:
        original += f"\n\n## AGY current project/plugin duplicate\n\n[Native37](../reports/{name}.md) verifies14 callbacks/seven same-input project-plugin pairs across all five selected events and five idempotent receipts, one actual Write execution/exact bytes. Unknown configured event turn has seven known callbacks and zero unknown callback; native unknown-event delivery unqualified. Two turns/no retries, cleanup28/preserved950/final union897 identities/zero live/no taskkill. Source r37 unchanged; combined34–37 is34 user turns/31 actual tools. Full native task stays unchecked/44 of45/P3 active.\n"
    target.write_text(original, encoding="utf8")
pending = {"source_revision": 37, "source_lock_hash": record["source_lock_hash"], "plan_tasks": "44/45", "full_native_gate": "unchecked",
    "current_verified_AGY_scopes": ["direct write/read/private/plan-only controls29", "replace controls31", "PreToolUse faults30",
        "lifecycle/PostToolUse/Stop matrix34+36", "five-event controlled duplicate37"],
    "pending_or_unqualified": ["AGY current-version shell pending guard control", "AGY search/multi-replace unknown or no-tool routes; failures retained",
        "genuine unsupported native event delivery", "remaining Codex/Cursor event-tool/fault and duplicate cells",
        "Claude model/effort selection and native tool turns", "Codex Desktop/IDE, Cursor IDE, AGY IDE qualification"],
    "human_decisions_retained": ["CLI route dangerous granted", "exact r29 VI and EN samples accepted"],
    "source_update": "not-performed", "global_install": "not-performed", "process_state": "zero owned live at native37 union audit"}
with (RUN / "native-continuation-todo.json").open("x", encoding="utf8") as stream:
    json.dump(pending, stream, ensure_ascii=False, indent=2)
with (RUN / "doc-update.json").open("x", encoding="utf8") as stream:
    json.dump({"status": "reconciled-native37-report-and-pending-scope", "preimages": preimages,
        "documents": [bind(p) for p in targets], "reports": [bind(report), bind(report.with_suffix(".json"))],
        "pending_scope": bind(RUN / "native-continuation-todo.json")}, stream, indent=2)
print(json.dumps({"status": "reconciled-native37-docs", "done_tasks": 44, "total_tasks": 45}))
