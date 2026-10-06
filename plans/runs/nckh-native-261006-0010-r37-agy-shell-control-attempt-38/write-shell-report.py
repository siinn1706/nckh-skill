"""Record the direct shell result and update only the owning evidence surfaces."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
PREVIOUS = WORK / "plans/runs/nckh-native-261005-2355-r37-agy-duplicate-admission-attempt-37"
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {"path": p.relative_to(WORK).as_posix(), "sha256": sha(p)}
record = read(RUN / "verified-shell-delivery.json")
assert record["status"] == "verified-direct-AGY-current-version-shell-pending-denial"
name = "delivery-261006-0010-r37-agy-shell-control"
report = WORK / "plans/reports" / (name + ".md")
with report.with_suffix(".json").open("x", encoding="utf8") as stream:
    json.dump(record, stream, ensure_ascii=False, indent=2)
with report.open("x", encoding="utf8") as stream:
    stream.write(f"""# AGY CLI1.2.17/r37: direct shell pending guard

[Verified bindings](./{name}.json) bind one actual `run_command` request on Gemini3.8FlashMedium/always-proceed/effort medium requested. Direct packaged handlers use producer5s; no observer or injected fault. Source r37/281 pins/hash `{record['source_lock_hash']}` unchanged.

Native CommandLine exactly equals the frozen controller-owned Python marker command. Actual tool ERROR includes `shell-targets-unverifiable`; one preflight receipt has pending/same reason and binds actual conversation/context byte hash. Marker absent before/after, final marker/resultSUCCESS/num_turns1/process exit0. The policy does not parse command payload or infer protected target paths; this qualifies the conservative pending guard, not shell-target extraction or a sandbox.

Cleanup26 matching config/payload members; preserved996 historical files/protected settings-hooks hashes. Union906 PID/creation FILETIME identities: zero matching/tracked-live, no taskkill. Verifier first attempt exit0; inline review/no independent reviewer. Global controller config writes/installed r25 replacement/publication/source changes not performed.

Combined native34–38: **35 user turns / 32 actual tool requests**. Event fault and duplicate observations remain scoped, original failed search/partial collector evidence retained. Full native task **unchecked/44 of45/P3 active**; other host/event/tool/surface, genuine unknown-event delivery, Claude model/effort/turns and app qualification remain explicit.
""")
targets = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md",
    WORK / "plans/journals/2026-10-05-cursor-native-timeout-controls-and-r37-repair.md"]
preimages = []
for index, target in enumerate(targets):
    text = target.read_text(encoding="utf8")
    preimage = RUN / "document-preimages" / (str(index) + "-" + target.name)
    preimage.parent.mkdir(exist_ok=True)
    preimage.write_bytes(target.read_bytes())
    preimages.append({"target": bind(target), "preimage": bind(preimage)})
    if index == 0:
        text = text.replace("34 user turns/31 actual tools", "35 user turns/32 actual tools").replace("union897", "union906")
        text = text.replace("Source unchanged; direct controls", "[Current shell guard38](../reports/" + name + ".md) verifies native pending denial/absent marker at direct5s. Source unchanged; direct controls")
    else:
        text += f"\n\n## AGY current direct shell guard\n\n[Native38](../reports/{name}.md) verifies actual run_command ERROR/shell-targets-unverifiable with pending preflight and absent marker at direct packaged5s on CLI1.2.17. One exact-command user turn/final marker/process exit0, cleanup26/preserved996/final union906 identities/zero live/no taskkill. Source r37 unchanged; combined34–38 is35 user turns/32 actual tools. Full native gate remains unchecked/44 of45/P3 active.\n"
    target.write_text(text, encoding="utf8")
pending = read(PREVIOUS / "native-continuation-todo.json")
pending["current_verified_AGY_scopes"].append("direct current-version shell pending guard38")
pending["pending_or_unqualified"].remove("AGY current-version shell pending guard control")
pending.update(process_state="zero owned live at native38 union audit", latest_scoped_evidence=bind(RUN / "verified-shell-delivery.json"),
    latest_plan_tasks="44/45", Claude_selection="asynchronous question pending; no Claude model prompt sent")
with (RUN / "native-continuation-todo.json").open("x", encoding="utf8") as stream:
    json.dump(pending, stream, ensure_ascii=False, indent=2)
with (RUN / "doc-update.json").open("x", encoding="utf8") as stream:
    json.dump({"status": "reconciled-native38-shell-report-and-pending-scope", "preimages": preimages,
        "documents": [bind(p) for p in targets], "reports": [bind(report), bind(report.with_suffix(".json"))],
        "pending_scope": bind(RUN / "native-continuation-todo.json")}, stream, indent=2)
print(json.dumps({"status": "reconciled-native38-docs", "done_tasks": 44, "total_tasks": 45}))
