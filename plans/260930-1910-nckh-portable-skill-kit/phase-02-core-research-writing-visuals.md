---
title: "Phase 2: Core research, writing and visuals"
status: in-progress
---

# Phase 2: Core research, writing và visuals

<!-- Core source implemented under cook --auto; human/native gates remain pending. -->

## Overview

Priority P1. Sáu Core skills, profiles và deterministic guards đã triển khai theo [cook --auto được duyệt](plan.md); depends on P1 frozen contracts. Effort ban đầu 5–8 ngày. Research/VI–EN/literary/visuals giữ nguyên phạm vi; native/human acceptance vẫn pending.

## Context Links

- [Catalog Core](skill-catalog.md), [evidence architecture](architecture.md), [eval/migration](installer-evaluation-migration.md).
- Old [evidence](../260930-0905-vietnamese-research-skill-kit/phase-02-evidence-and-research.md), [VI/EN](../260930-0905-vietnamese-research-skill-kit/phase-03-vietnamese-and-english-writing.md), [visuals](../260930-0905-vietnamese-research-skill-kit/phase-04-slides-and-scientific-visuals.md), [standards](../260930-0905-vietnamese-research-skill-kit/standards-and-failure-catalog.md): nguồn lịch sử cho migration map, không là plan triển khai hiện hành.

## Key Insights / Architecture

Một evidence layer dùng chung; VI và EN có style/taste profiles riêng. Literature review là mode research, argument/comparison thuộc method. Citation identity khác claim entailment; OCR text khác quote đã visual-check. Visual engine là extension, nckh-visuals sở hữu truthful/native artifact acceptance.

## Requirements

- Research modes narrative/scoping/systematic có search/screening/exclusion/protocol records phù hợp; không gọi mọi search là systematic review.
- Source/version/edition/translator và exact page/line/section locators; giữ original language/quote, access limits, contradiction và uncertainty.
- Ranking theo system/category/metric-year/as-of; venue profile theo journal/conference/year/track/article type, không union rules và không default một venue.
- Write/translate/polish giữ số, đơn vị, phủ định, modality, scope, citations, glossary và protected regions; new factual delta quay về evidence.
- VI taste dựa licensed examples + human holdout; English scientific fidelity/domain review riêng. Tách deterministic guard, model critic và human gold.
- Slides/charts/diagrams/artwork có source-to-mark mapping, rights, provenance/alt/caveats, native editability và QA gắn exact final hash.

## File ownership — Create after P1

| Absolute path / bounded subtree | Files/content owned |
|---|---|
| `C:/Users/USER/Downloads/test-skill/nckh-kit/skills/core/` | Chỉ nckh-research, nckh-evidence, nckh-method, nckh-write, nckh-taste, nckh-visuals, mỗi directory có SKILL.md + relevant references. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/core/profiles/style/` | vi/en language- and genre-specific style, protected-region và glossary rules. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/core/profiles/venue/` | Profile schema/templates và rules ledger; không tự chọn venue/ranking. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/extensions/native-documents/` | Capability contracts cho editable deck/chart/diagram/source, selected-engine dependencies và real acceptance; provider installation không mặc định. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/tests/evidence/` | Identity/locator/status/factual-delta/visual-hash guard tests. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/evals/cases/research-writing-visuals/` | Sáu skills, literary/VI/EN/visual cases và licensed-source references. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/docs/research-and-writing.md` | Task inputs, states, reviewer gates và engine availability. |

P1 owner duyệt core/contracts/catalog schema changes; phase này không sửa parallel shared files. Actual manuscripts, full texts, personal taste corpus và human labels nằm ngoài source/dist. Không delete baseline.

## Implementation Steps

1. Map mọi old-phase deliverable/invariant đến sáu skills, profiles hoặc extension contract; không rút bớt scope để khớp số lượng.
2. Viết deterministic fault cases trước: DOI đúng nhưng claim sai, missing page, OCR ambiguity, unsupported statistic, retraction/freshness, edition mismatch, venue switch, profile drift.
3. Author research/evidence/method bodies + required references; khóa verdict-to-wording và record invalidation.
4. Author write/taste routes VI, EN, bilingual/vi-to-en, minimal-diff và factual-delta checks. Không auto sửa citations/quotes để câu “hay hơn”.
5. Author visual workflow và bind permitted native engines qua extension interface. Empty engine map phải trả unavailable; raster preview không được ghi editable source.
6. Thiết kế human protocol, licensed samples và isolated holdout trước run; thiếu reviewers/rights giữ pending. Native visual engine acceptance cần thực sự mở/render/check output.
7. Run focused guards rồi broaden; review source/claim/prose trace và capability coverage. Handoff kết quả riêng từng skill/mode, không badge toàn Core.

## Todo

- [x] Map old scope và source/rights dependencies.
- [x] Viết sáu Core skills và VI/EN/venue profiles.
- [x] Viết fault cases và deterministic guards.
- [x] Bind visual/native extension contract và ghi capability availability.
- [ ] Thu human/native evidence khi được phép, còn lại ghi pending.

Human inputs được user xác nhận chưa có corpus VI/EN hoặc reviewer ngày 01/10/2026. Native document engines chưa được chọn/qualified; binding hiện unavailable. Probe viết VI là development input tổng hợp với explicit instruction loading, không human gold hoặc native discovery.

## Success Criteria

- Every factual conclusion trace được source/evidence/claim; thiếu full text không phát minh locator.
- Literary route giữ edition/translation/context; Q1/Q2 không suy từ DOI hoặc @article; venue changes invalidate affected checks.
- Factual-delta fail không được taste/polish success ghi đè; supplied facts không đòi search vô ích.
- Sáu skills có positive/negative/outcome/failure eval; blind human/native acceptance chỉ pass với receipt thực và đủ rights.
- Visual source/render/hash khớp bản cuối; typography/native editability/scientific meaning là separate checks.

## Validation commands và evidence scope

Working directory: `C:/Users/USER/Downloads/test-skill/nckh-kit/`.

`python -m unittest discover -s tests/evidence -p "test_*.py"`

Run locator/factual-delta narrow cases trước toàn suite. Tests hiện có source; receipt local (historical evidence path: `../../nckh-kit/evals/results/local-checks.json`; unavailable in the cleaned checkout) ghi kết quả revision thực. Behavior/human/native cases dùng protocol và outputs đã được phép; không tạo gold bằng self-judge.

## Risk / Security / Rollback

Prompt injection từ nguồn không là instruction. Không redistribution full text/corpus chỉ vì đọc được; permissions tách read/eval/package/publication. Profile hoặc artifact đổi thì invalidate downstream, giữ immutable source và receipts. Rollback chỉ candidate skill/profile version; không xóa human feedback hoặc original manuscript.

## Next Steps

P3/P4 reuse frozen evidence/writing contracts; P5 đóng gói closures. Human/visual pending có thể cho authoring tiếp nhưng cấm release skill/mode đó dưới nhãn stable.
