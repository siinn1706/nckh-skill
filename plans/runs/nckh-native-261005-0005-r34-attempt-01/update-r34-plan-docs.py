"""Refresh the short plan index and append evidence without closing its native gate."""

import json
import re
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / "plans/261004-0047-nckh-research-data-hooks-writing"
report = json.loads((WORK / "plans/reports/delivery-261005-0005-r34-cursor-agy.json").read_text(encoding="utf8"))
assert report["source_revision"] == 34 and report["plan_progress"]["done"] == 44
paths = [PLAN / "plan.md", PLAN / "phase-03-portable-hooks.md", PLAN / "phase-04-integration-and-personal-acceptance.md"]
before = {path: path.read_text(encoding="utf8") for path in paths}
phase_texts = [path.read_text(encoding="utf8") for path in sorted(PLAN.glob("phase-*.md"))]
assert sum(len(re.findall(r"^- \[[xX]\] ", text, re.M)) for text in phase_texts) == 44
assert sum(len(re.findall(r"^- \[[ xX]\] ", text, re.M)) for text in phase_texts) == 45
assert "- [ ] Record host evidence per surface/version/event" in before[paths[1]]
backup = RUN / "plan-preimages-final"
backup.mkdir(exist_ok=False)
for path in paths:
    (backup / path.name).write_bytes(path.read_bytes())
tests = report["deterministic"]["tests"]
seconds = report["deterministic"]["seconds"]
faults = report["native_r34_agy_event_faults"]
totals = report["extracted_totals"]
index = f"""---
title: "NCKH research-first writing, visuals và hooks"
description: "R34 local delivery verified; owner VI/EN accepted; native event/surface gate còn mở."
status: in-progress
priority: P1
effort: 4 phases / 5-8 ngày công
branch: unverified-no-git-worktree
tags: [nckh, research, writing, visuals, hooks, provenance]
created: 2026-10-04
---

# NCKH research-first writing, visuals và hooks

## Outcome và quyền thực thi

Thực thi accepted plan: hai writer theo nhiệm vụ, scientific-purpose visual guard và portable deterministic hooks. Candidate hiện **r34**, local delivery verified. `/goal ak-cook plan.md --auto` cấp quyền implementation và local checks. [Native grant](../runs/nckh-native-261004-1707-attempt-01/native-grant.json), [GPT medium grant](../runs/nckh-native-261004-1707-attempt-01/model-medium-grant.json) và [Cursor/AGY dangerous grant](../runs/nckh-native-261005-0005-r34-attempt-01/cursor-agy-model-dangerous-grant.json) đã được sử dụng trong project thử riêng. [Owner feedback](../runs/nckh-native-261004-1707-attempt-01/owner-feedback.json) chấp nhận đúng hai mẫu VI/EN của r29; không có approval đang chờ cho các quyền này.

## Constraints và non-goals

`nckh-humanwrite` và `nckh-paperwrite` mỗi skill dùng `--en`/`--vi`, theo [language decision](../reports/decision-261004-0047-writer-language-options.md). `nckh-write` giữ compatibility theo action; `nckh-taste` là critic. Exact **39 identities / 156 base cases / 19 families / 9 resources**; giữ historical 148 IDs/224 native cells và exact writer sample bindings.

Visuals chỉ cho research với provenance/parameters/uncertainty/labels; không artwork hoặc invented measurements. Humanizer là owned Markdown policy; LanguageTool optional English diagnostic. Hooks bounded, inactive mặc định, không payload shell/network/provider/nested LLM/full-transcript ingestion. Public `resource_access` giữ ON; OFF chỉ internal comparison. Installed r25, publication, stable/scientific/release có gates riêng.

## Phases và dependencies

| Phase | Kết quả/evidence | Phụ thuộc |
|---|---|---|
| [P1 Writers](./phase-01-start.md) | 13/13; hai writer, locale/preservation/router, source consumers và supplemental matrix | Accepted language decision |
| [P2 Scientific visuals](./phase-02-scientific-visuals.md) | 9/9; purpose/origin/mark guards, local calculation và selective QA | P1 |
| [P3 Portable hooks](./phase-03-portable-hooks.md) | 10/11; four codecs/config transactions; native evidence task còn unchecked | P2 + official schema ledger |
| [P4 Integration](./phase-04-integration-and-personal-acceptance.md) | 12/12; current r34 checks/build/extract/smoke/previews; owner samples accepted | P1–P3, single source-freeze owner |

## Current acceptance evidence

[Delivery r34](../reports/delivery-261005-0005-r34-cursor-agy.md) / [structured bindings](../reports/delivery-261005-0005-r34-cursor-agy.json) ghi current source, failures/repairs, packaged native runs và cleanup.

| Check | Current result |
|---|---|
| Source/inventory | r34, 281 pins; canonical hash `{report['source_lock_hash']}` |
| Full deterministic | {tests} tests, một Windows symlink skip; successful, {seconds:.3f} giây |
| Packaging | Bốn reproducibility variants, 16 bundles/archives/extractions verified |
| Extracted behavior | {totals['resource_reads']} resource reads, {totals['writer_disabled_observations']} writer disabled/no-read observations, {totals['hook_projections_exercised']} hook projections |
| Installer previews/preservation | Tám surfaces; {report['preservation']['protected_hashes_checked']} protected hashes unchanged; installed r25 và bốn legacy bundles preserved |
| Current native AGY | Ba file allow/denial cases; project + workspace-plugin duplicate đạt; {len(faults['results'])} event fault attempts, `{faults['status']}` |
| Current native Cursor | Grok 4.7 500K Extra High selector; allow tạo marker; duplicate có hai callbacks/một receipt nhưng native timeout |

## Remaining acceptance và rollback

Plan giữ **in-progress, 44/45**. Native task cần evidence đúng event/version/surface: Claude model/tool và other events; Codex duplicate/other-event/protected-path routes; Cursor missing events và timeout anomaly; remaining AGY tools/surfaces/timing. Codex Desktop/IDE, Cursor IDE, AGY IDE chưa có direct app receipts. CLI/package presence và parser/hash passes không thay bằng chứng ở các giao diện này.

Current test hooks/configs/payload/plugin files đã cleanup; protected global hashes unchanged và final process audit không có matching task process. Native conversation/trust history và tất cả failed receipts giữ nguyên. Rollback/remove chỉ trên owned matching bytes; config conflict phải preserve. Stable/scientific/install/release không được đóng bằng subset native hoặc owner acceptance của hai mẫu.

## History và source adoption

[Starting baseline](../reports/checks-261004-1037-starting-baseline.json), [r29 delivery](../reports/delivery-261004-1037-r29-local-candidate.md), [r30 native checkpoint](../reports/delivery-261004-1707-r30-native-checkpoint.md), [r34 running checkpoint](../reports/checkpoint-261005-0005-r34-running.md) và [source→reader→artifact→test map](./source-adoption-map.md) giữ chronology/provenance. R31/r32/r33 runs bind đúng revision trong current delivery report; không regrade historical evidence. Chi tiết execution và historical failures ở phase files. Final validate/parse/reindex/link checks chỉ xác nhận structure/state/integrity.

<!-- slug: nckh-research-data-hooks-writing -->
"""
paths[0].write_text(index, encoding="utf8", newline="\n")
appendices = {
    paths[1]: f"""

## Current delivery — r34 native observations

[Delivery r34](../reports/delivery-261005-0005-r34-cursor-agy.md) và [bindings](../reports/delivery-261005-0005-r34-cursor-agy.json) supersede running checkpoint bằng completed local checks. Full r34 đạt {tests} tests, một Windows symlink skip. AGY r34 đạt ba native file cases và project/workspace-plugin duplicate; event fault run có {len(faults['results'])} attempts, status `{faults['status']}`. Cursor current allow tạo marker; duplicate có hai same-tool callbacks/một policy receipt nhưng native host vẫn báo timeout, không gọi qualified.

Current matching test files đã cleanup; final process audit zero matching task processes. Grants đã có, không hỏi lại; installed r25 giữ nguyên. Task host evidence per surface/version/event vẫn unchecked: latest report ghi source/version/event bindings và các Claude/Codex/Cursor/direct app gaps. Fault injection là controller-owned sau native callback thật; post-event side-effect timing giữ riêng. Historical r30–r33 receipts không regrade thành r34.
""",
    paths[2]: f"""

## Current delivery — r34 integration verified

[Current delivery r34](../reports/delivery-261005-0005-r34-cursor-agy.md) bind source r34/281 pins, full {tests} tests successful ({seconds:.3f}s, một Windows symlink skip), bốn reproducibility variants/16 builds, 16 archives/extractions, {totals['resource_reads']} resource reads, {totals['writer_disabled_observations']} OFF writer no-read observations và {totals['hook_projections_exercised']} primary/reference hook projections. Tám installer previews giữ project bytes; {report['preservation']['protected_hashes_checked']} protected hashes và installed r25/bốn legacy bundles unchanged.

Source sửa receipt parent race dựa trên actual Windows diagnostic; review inline và focused 150×6 concurrent regression giữ nguyên guard/timeout. R33 full failure và native protected-write-before-repair giữ riêng. Owner VI/EN acceptance bind đúng hai mẫu r29. Current cleanup/process audit completed; full native task vẫn thuộc P3/unchecked, không lấy P4 local pass để thay direct event/surface qualification.
""",
}
for path, appendix in appendices.items():
    if appendix.strip().splitlines()[0] in before[path]:
        raise RuntimeError("Preserve an existing current-delivery appendix")
    path.write_text(before[path].rstrip() + appendix + "\n", encoding="utf8", newline="\n")
assert "- [ ] Record host evidence per surface/version/event" in paths[1].read_text(encoding="utf8")
print(json.dumps({"status": "updated-evidence-native-gate-open", "plan": str(PLAN / "plan.md"), "backup": str(backup)}))
