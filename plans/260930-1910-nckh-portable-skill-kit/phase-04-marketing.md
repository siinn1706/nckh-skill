---
title: "Phase 4: Marketing"
status: in-progress
---

# Phase 4: Marketing

<!-- Cook --auto authorized on 2026-10-01; publication is outside that authorization. -->

## Overview

Priority P1. 13 Marketing skills đã triển khai theo [cook --auto được duyệt](plan.md); depends on P1–P2, independent of P3 source files. Effort ban đầu 3–5 ngày. Competitor/design-brief có owning skills; provider execution và publication vẫn cần grant riêng.

## Context Links

- [Marketing catalog](skill-catalog.md), [AgentKit disposition](../reports/researcher-260930-1910-agentkit-port-evidence.md).
- [Workflow/model](workflow-and-model-routing.md), [evidence contracts](architecture.md), [eval](installer-evaluation-migration.md).

## Key Insights / Architecture

Core evidence kiểm factual claims; marketing domain sở hữu audience/channel/KPI context. Marketing-plan là strategy artifact, nckh-plan là execution planning. Campaign không sở hữu orchestration engine; email/social drafting không cấp quyền send/post.

## Requirements

- 13 identities: market-research, brand, marketing-plan, campaign, launch, content, copy, seo, email, social, analytics, cro, experiment; prefix nckh-.
- Competitor research thuộc market-research; design brief thuộc brand; không drop functionality để vừa quota.
- Purpose/trigger/output/non-goal/delegation/overlap cho từng skill; selective reference loading, Core brief/permission/evidence reuse.
- Không fabricate size, testimonial, statistic, scarcity, attribution hay causal lift; ranking/KPI/denominator/time-range/data quality phải có nguồn hoặc explicit assumption.
- No automatic ads spend, send/publish, upload contacts, traffic allocation hoặc experiment launch. Consent/rights/providers là separate gates.

## File ownership — Create after P1–P2

| Absolute path / bounded subtree | Files/content owned |
|---|---|
| `C:/Users/USER/Downloads/test-skill/nckh-kit/skills/marketing/` | 13 catalog directories với SKILL.md và scoped references. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/extensions/providers/marketing/` | Selected email/social/SEO/analytics/ad connector contracts, opt-in only. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/tests/marketing/` | KPI/denominator/source/publish-authority contract guards. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/evals/cases/marketing/` | Per-skill positives, near misses, no-publish/spend và evidence faults. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/docs/marketing.md` | Strategy/production/publication boundaries và extension requirements. |

Không sửa Engineer source hoặc shared core registry parallel; registry delta qua P1 owner. Không delete baseline. Private contacts/customer datasets không được đưa vào fixtures/dist.

## Implementation Steps

1. Map 15 candidate capabilities thành 13 owners; record merge examples và near-miss triggers trước authoring.
2. Pin AgentKit inspirations, license/provenance state; challenge provider baggage và repetitive copy workflows.
3. Author skills, allowing direct use while plan/cook remain normal entrypoints. A pure content request must end with usable draft, không tạo campaign ops ngoài scope.
4. Define market/evidence, brand/design brief, campaign/launch, content/copy, analytics/experiment và CRO/experiment handoff records.
5. Write deterministic tests và agent eval cases: unsupported market stat, hidden upload, false testimonial, missing denominator, correlation/causality, invalid randomization/peeking.
6. Run guards, then authorized real agent cases; statistical/human judgment stays reviewer-owned. Không dùng live campaign/account để test draft safety.
7. Review content-language boundaries VI/EN, 13 stable eligibility records và source closure; integrate registry sequentially.

## Todo

- [x] Map capabilities và licenses/provenance.
- [x] Viết 13 Marketing skills và scoped extensions.
- [x] Khóa handoff/output contracts và negative triggers.
- [x] Viết/run guard suite, lưu authorized agent eval evidence.
- [x] Review claims, publication authority và registry integration.

Local guard suite có actual test receipts cho source không đổi. [Direct development evaluation](../reports/testing-261001-direct-skill-development.md) đã chạy/chấm đủ 52 tình huống Marketing trên revision 14 đã cài: latest 51 pass, một fail CRO bỏ sót `noindex` theo oracle đã khóa. Các lỗi chọn AK owner và thiếu calculation provenance ở lượt đầu được giữ; diagnostic thay catalog scope hoặc trả brief không claim phép tính chưa chạy được ghi riêng. Checkbox ghi đã chạy/lưu evidence, không biến fail thành pass hoặc nghiệm thu stable. Draft/send/publish/spend giữ boundary riêng; không có live campaign/account write hoặc measured lift.

## Success Criteria

- Competitor/design brief outcomes vẫn đầy đủ; không thêm mega dispatcher.
- Marketing claims dùng shared evidence-first nhưng không ép Q1/Q2 lên tất cả content.
- Draft/content request không tạo external write/spend; no credential presence-as-permission.
- Analytics nêu actual denominators/time range/uncertainty; experiment design có unit, allocation, primary metric, stopping/guardrail rationale và assumptions.
- 13 skills có eval/outcome/permission cases; measured lift không được báo nếu chưa có actual experiment.

## Validation commands và evidence scope

Working directory: `C:/Users/USER/Downloads/test-skill/nckh-kit/`.

`python -m unittest discover -s tests/marketing -p "test_*.py"`

Narrow first: data/authority contracts, then suite. Receipt local (historical evidence path: `../../nckh-kit/evals/results/local-checks.json`; unavailable in the cleaned checkout) ghi revision và actual output. Agent/human eval còn pending; không suy observed lift từ scenario.

## Risk / Security / Rollback

Privacy/consent không được bỏ vì marketing data đã có trong file. Untrusted market/source text không cấp quyền publish. Keep editing reversible; rollback candidate skill/profile versions, giữ approved brand choices, source records và human feedback. Do not auto delete provider configuration.

## Next Steps

P5 nhận Marketing source closure, registry entries và eval IDs. Optional integrations chưa qualified vẫn unavailable/experimental, không khóa việc dùng instruction-only workflows đã đủ acceptance.
