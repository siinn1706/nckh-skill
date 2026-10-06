"""Publish revision-bound evidence records and keep the plan index concise."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
REPORTS = WORK / "plans/reports"
EVENT = WORK / "plans/runs/nckh-native-261005-2320-r37-agy-event-controls-attempt-34"
SEARCH = WORK / "plans/runs/nckh-native-261005-2335-r37-agy-search-controls-attempt-35"
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {"path": p.relative_to(WORK).as_posix(), "sha256": sha(p)}
event = read(EVENT / "verified-event-delivery.json")
search = read(SEARCH / "verified-search-delivery.json")
stop = read(RUN / "verified-stop-delivery.json")
assert (event["model_turns"], search["model_turns"], stop["model_turns"]) == (24, 4, 4)
aggregate = {"status": "verified-scoped-agy-r37-events-and-search-observations", "source_revision": 37,
    "source_lock_hash": event["source_lock_hash"], "model_turns": 32, "actual_native_tool_requests": 29,
    "events": bind(EVENT / "verified-event-delivery.json"), "search": bind(SEARCH / "verified-search-delivery.json"),
    "stop": bind(RUN / "verified-stop-delivery.json"), "full_native_gate": "unchecked", "plan_tasks": "44/45",
    "source_modified": False, "independent_review": "not-performed; controller inline artifact review"}
event_report = "delivery-261005-2320-r37-agy-event-observations"
search_report = "delivery-261005-2335-r37-agy-search-gaps"
for name, record in ((event_report, aggregate), (search_report, search)):
    path = REPORTS / (name + ".json")
    with path.open("x", encoding="utf8") as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
table = ["| Sự kiện | Ca | Native tool | Bytes revised | Policy |", "|---|---|---|---|---|"]
for row in event["results"] + stop["results"]:
    table.append("| " + " | ".join((row["event"], row["mode"], ", ".join(row["native_terminal_states"]),
        str(row["fixture_exact_revised"]), ", ".join(row["selected_policy_decisions"]))) + " |")
text = f"""# AGY CLI r37: lifecycle, post-tool và Stop observations

[Bindings](./{event_report}.json) ghi 28 ca sự kiện trên CLI **1.2.17 / Gemini 3.8 Flash medium / always-proceed**: 24 lượt của batch34 và bốn lượt mới batch36. Mỗi lượt có đúng một native `write_to_file`, final marker, resultSUCCESS/num_turns1 và native process exit0. Source r37/281 pins/hash `{event['source_lock_hash']}` giữ nguyên. Đây là observer thử với outer5s/inner5s; normal direct packaged controls29 giữ evidence riêng.

## Kết quả thực tế

""" + "\n".join(table) + """

`PreInvocation` và `PostInvocation` trả block trong policy vẫn cho native tool hoàn tất. Wire codec ở hai event là advisory; không có preventive enforcement claim. Chỉ từ tên lifecycle event không suy thứ tự trước/sau từng thao tác tool.

Bốn lỗi `PostToolUse` malformed-output/timeout/crash/unsupported-codec tạo native ERROR **sau khi toàn bộ bytes revised đã ghi**. Policy-deny và malformed-input ở post-tool vẫn native DONE. Lỗi sau thao tác không được regrade thành preventive denial hoặc rollback. Stop faults đều sau final response và bytes đã ghi; không quan sát model resubmission.

196 callbacks observer tổng cộng: PreInvocation56, PreToolUse28, PostToolUse28, PostInvocation56, Stop28. Repetition của lifecycle chưa là controlled project/plugin duplicate. Unknown selected codec vẫn là injection sau callback được hỗ trợ; genuine unsupported native event admission còn riêng.

## Partial collector, repairs và cleanup

Batch34 freeze28 nhưng collector exit1 sau native lượt24 vì descendant wait30s chưa hết. Raw running summary23 và failure giữ nguyên; bốn ca Stop còn lại không chạy trong batch đó. Read-only inspection sau lỗi và union audit xác nhận zero live; không taskkill và không xác định nguyên nhân delay. Batch36 đóng brief riêng cho đúng bốn ca chưa chạy, không resubmit 24 lượt cũ.

Một PostInvocation timeout observer cập nhật sau snapshot: original snapshot/hash và final callback đều bound, late policy không là native permission. Verifier đầu tiên dùng LF replay trong khi observer Windows lưu CRLF. Failing verifier command/preimage/serialization diagnosis được giữ, CRLF repair chỉ sửa kiểm byte; không thay native oracle. Verifier sau repair exit0. Original PostInvocation timing label được sửa trong verified record, raw summary vẫn giữ.

Batch34 cleanup26/preserved391, audit726 identities/zero live. Batch36 cleanup26/preserved874, audit836 identities/zero live. Protected settings/hooks hashes giữ nguyên; controller không direct-write global. Installed r25/publication/owner exact r29 VI/EN acceptance giữ trạng thái trước. Inline verification; không independent reviewer.

Full native task **unchecked / 44 of45 / P3 active**. Remaining includes controlled duplicates, unsupported-event admission, other host/tool/surface cells, Claude selection/turns and app qualification.
"""
with (REPORTS / (event_report + ".md")).open("x", encoding="utf8") as stream:
    stream.write(text)
rows = ["| Ca | Quan sát | Native error | Policy trước tool |", "|---|---|---|---|"]
for row in search["results"]:
    rows.append("| " + " | ".join((row["attempt"], row["observation"], row["native_error"] or "Không có native tool", "0")) + " |")
text = f"""# AGY CLI r37: bốn search gaps giữ nguyên failed oracles

[Verified bindings](./{search_report}.json) ghi bốn user turns trên CLI1.2.17/Gemini3.8FlashMedium/always-proceed, direct packaged5s. Source r37 giữ nguyên. Brief độc lập gồm public/private `find_by_name` và `grep_search`; không rerun hoặc regrade list_dir attempt32.

""" + "\n".join(rows) + """

Private find_by_name có actual native request rồi dispatcher trả unknown-tool. Đây là genuine native unsupported-tool observation; không có preflight/pre-delivery receipt, nên private enforcement unqualified. Ba ca khác có zero native tool frames: model-only no-tool outcome không chứng minh native unsupported admission hoặc NCKH denial. Cả bốn original oracles vẫn failed/unqualified; exact fixture bytes unchanged.

Four distinct conversations, one user turn per conversation, native exit0/num_turns1/resultSUCCESS. Model retries0, không fallback tool/agent hoặc đổi global profile. Init advertised names không chứng minh tool callable. Read-only help/agents inventory chỉ cung cấp flags/names; effective agent/toolset chưa được established.

Cleanup26/preserved851/protected settings-hooks unchanged. Union audit752 PID/creation FILETIME identities, zero matching/tracked-live, không taskkill. Verifier exit0 first attempt; inline verification/no independent reviewer. Source/installed r25/publication không đổi. Full native task **unchecked/44 of45/P3 active**.
"""
with (REPORTS / (search_report + ".md")).open("x", encoding="utf8") as stream:
    stream.write(text)
targets = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md",
    WORK / "plans/journals/2026-10-05-cursor-native-timeout-controls-and-r37-repair.md"]
preimages = []
for index, target in enumerate(targets):
    original = target.read_bytes()
    path = RUN / "document-preimages" / (str(index) + "-" + target.name)
    path.parent.mkdir(exist_ok=True)
    with path.open("xb") as stream:
        stream.write(original)
    preimages.append({"target": bind(target), "preimage": bind(path)})
history = PLAN / "native-evidence-history.md"
assert not history.exists()
history.write_bytes(targets[0].read_bytes())
note = f"""
## AGY r37 event và search continuation

[Events34/36](../reports/{event_report}.md) binds28 real Write event cases/196 callbacks: lifecycle policy block stays advisory, four PostToolUse faults reportERROR after exact mutation, Stop observations occur after final response. Original batch34 exit1/partial summary and descendant wait failure retained; later audit zero/no taskkill. Four not-run Stop cases complete separately in36, no resubmission/regrading. Windows CRLF verifier repair and late PostInvocation observer retained. [Search35](../reports/{search_report}.md) binds one genuine native unknown find_by_name and three model-only no-tool cases; all four frozen search oracles failed, private enforcement unqualified. Total32 user turns/29 actual tool requests. Cleanup matching bytes/protected configs and final union836 identities/zero live verified; source r37 unchanged. Full native task remains unchecked/44 of45/P3 active; owner samples and installed/release gates retained.
"""
for target in targets[1:]:
    with target.open("a", encoding="utf8") as stream:
        stream.write(note)
old = targets[0].read_text(encoding="utf8")
frontmatter = old.split("---", 2)[1]
index = "---" + frontmatter + "---\n\n" + f"""# NCKH research-first writing, visuals và hooks

## Outcome và quyền thực thi

Execute accepted plan: task-specific humanwrite/paperwrite, scientific-purpose visual guard and portable deterministic hooks. `/goal ak-cook --auto` authorizes implementation/local checks; [native grant](../runs/nckh-native-261004-1707-attempt-01/native-grant.json), [GPT medium grant](../runs/nckh-native-261004-1707-attempt-01/model-medium-grant.json), [Cursor/AGY dangerous grant](../runs/nckh-native-261005-0005-r34-attempt-01/cursor-agy-model-dangerous-grant.json) and [CLI route decision](../runs/nckh-native-261005-2210-r37-agy-cli-controls-attempt-29/cli-route-user-decision.json) remain effective. [Owner feedback](../runs/nckh-native-261004-1707-attempt-01/owner-feedback.json) accepts exact r29 VI/EN samples.

## Constraints và non-goals

Separate `nckh-humanwrite` and `nckh-paperwrite`, each with `--en`/`--vi`; `nckh-write` compatibility router and `nckh-taste` critic. [Accepted language decision](../reports/decision-261004-0047-writer-language-options.md). Exact39 identities/156 base cases/19 families/9 resources; preserve historical148 IDs/224 native cells. Public resource-access ON, OFF only internal comparisons.

Visuals require research purpose, provenance, parameters, uncertainty and origin labels; no artwork/invented measurements. Humanizer is a small owned policy; LanguageTool optional English diagnostic. Hooks bounded/inactive by default, no payload shell/network/provider/nested LLM/full-transcript ingestion. Installed r25, publication, scientific/stable/release and global direct writes have separate gates.

## Phases và dependencies

| Phase | Status | Dependency |
|---|---|---|
| [P1 Writers](./phase-01-start.md) | 13/13 | Accepted language decision |
| [P2 Scientific visuals](./phase-02-scientific-visuals.md) | 9/9 | P1 |
| [P3 Portable hooks](./phase-03-portable-hooks.md) | 10/11, native gate unchecked | P2 + schema ledger |
| [P4 Integration](./phase-04-integration-and-personal-acceptance.md) | 12/12 retained | P1–P3 + freeze owner |

## Current candidate — r37

281 pins/hash `{event['source_lock_hash']}`. [Verified local checkpoint](../reports/delivery-261005-1640-r37-local-native-checkpoint.md) records192 tests successful/one Windows skip,16 archives/extractions,216 resource reads,48 internal OFF/no-read,24 hook projections,eight previews,509 protected hashes/four legacy bundles. Reuse unchanged source/input/environment evidence; these checks establish local integrity/portability.

## Current CLI route and native evidence

AGY CLI1.2.17/Gemini3.8FlashMedium and Cursor CLI/Grok4.7/500k/xhigh/fastfalse dangerous. [AGY direct controls29](../reports/delivery-261005-2210-r37-agy-cli-controls.md), [Write faults30](../reports/delivery-261005-2230-r37-agy-preflight-faults.md), [events34/36](../reports/{event_report}.md) and [search35 gaps](../reports/{search_report}.md) retain exact scoped outcomes and failures. New continuation:32 user turns/29 actual tools; all configs/payloads matching cleanup, final union836 identities/zero live. Source unchanged; direct controls, injected faults and model-only outcomes remain distinct.

## Remaining acceptance và rollback

**In-progress / 44 of45 / P3 active.** Pending: controlled duplicate/unsupported-event and remaining host/tool/surface cells, Claude model/effort/native turns, direct app qualification. CLI route selection closes IDE recovery requests; IDE qualification remains unverified. Unknown tools/fail-open events retain manual/not-callable limits; no four-host parity claim.

Remove only owned matching config/payload bytes; preserve user edits/conflicts, historical failures and revision bindings. Activation, new trust/global config writes, installed replacement and publication require their own authority.

## History và verification

[Earlier native evidence index](./native-evidence-history.md), phase records and revision-bound reports retain all observations. [Source adoption](./source-adoption-map.md). Validate/parse/reindex/link checks establish structure/state/integrity only.

<!-- slug: nckh-research-data-hooks-writing -->
"""
targets[0].write_text(index, encoding="utf8")
with (RUN / "doc-update.json").open("x", encoding="utf8") as stream:
    json.dump({"status": "reconciled-native34-36-reports-and-concise-index", "preimages": preimages,
        "previous_index_exact_snapshot": bind(history), "reports": [bind(REPORTS / (name + suffix)) for name in
        (event_report, search_report) for suffix in (".md", ".json")], "documents": [bind(p) for p in targets]}, stream, indent=2)
print(json.dumps({"status": "reports-written", "model_turns": 32, "native_tools": 29, "full_native_gate": "unchecked"}))
