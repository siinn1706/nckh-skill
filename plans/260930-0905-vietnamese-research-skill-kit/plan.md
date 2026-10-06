---
title: "Bộ skill nghiên cứu và viết Việt–Anh — hồ sơ đã thay thế"
description: "SUPERSEDED ngày 2026-10-01 bởi kế hoạch NCKH portable; giữ baseline để tra cứu, không triển khai plan này."
status: pending
priority: P1
effort: "12–20 ngày (ước tính cập nhật, không cam kết)"
tags: [research, writing, evidence, vietnamese, scientific-visuals]
blockedBy: []
blocks: []
created: 2026-09-30
---

# Bộ skill nghiên cứu và viết Việt–Anh

> **SUPERSEDED — 01/10/2026 (Asia/Saigon).** Người dùng đã duyệt [kế hoạch NCKH Skill Kit portable](../260930-1910-nckh-portable-skill-kit/plan.md) thay kế hoạch này. Index, năm phase và hai design details trong thư mục này chỉ còn là hồ sơ lịch sử; không cook từ chúng. Các invariant được giữ theo [migration map đã duyệt](../260930-1910-nckh-portable-skill-kit/installer-evaluation-migration.md). Trạng thái `pending` bên dưới ghi việc triển khai cũ chưa diễn ra, không thể hiện authority hiện tại hoặc hoàn thành. Blueprint gốc được giữ nguyên.

## Overview

Đây là kế hoạch **chỉ lập kế hoạch**: chưa tạo package, cài/cập nhật skill, gọi provider hay chứng minh chất lượng. Người dùng chỉ cần `plan -> cook`, tag skill tùy chọn; router tự chọn capability từ catalog thật. Wrapper quanh AgentKit/upstream có hai entrypoint `research-plan`/`research-cook` và 10 module nội bộ; instructions dùng English, output chọn `vi|en|bilingual`.

## Goals and boundaries

- Gu/giọng Việt có corpus được phép và human taste review; evidence/research có provenance, claim–evidence binding, Q1/Q2 theo policy từng task và venue isolation.
- English scientific prose/`vi-to-en` giữ certainty, số, đơn vị, thuật ngữ và claim scope.
- Slides, charts, scientific diagrams và artwork minh bạch về loại, nguồn, quyền, editability.
- Hook/subagent có chọn lọc, quyền host thật; tối ưu cost trên task được nghiệm thu, không giảm chất lượng.
- Skill context: soft `min(20k, 10% W)`, hard `min(40k, 20% W)`; tính cả references/hook/delegate và dùng chung pool, không nhân trần theo số agent.
- Rule cards từ official/university sources có scope, phiên bản, lỗi mục tiêu và phép kiểm; không trộn policy với gợi ý văn phong.
- Không fork/copy collection, giả `ak run-skill`, auto-install/update, upload, trả phí, commit, publish hay submit.

## Dependencies and state

Các báo cáo là record tại 2026-09-30; chưa có behavioral benchmark/nghiệm thu chất lượng từ con người; runtime/catalog, quyền sample, ngân sách eval và venue profile chốt theo use-case.

| Dependency | Trạng thái / điều kiện |
|---|---|
| Hợp đồng và nghiên cứu nguồn | Có; xem [tổng hợp lựa chọn](../reports/synthesis-260930-0905-skill-kit-selection.md), [design proposal](../reports/brainstorm-260930-0905-skill-kit-contract.md), [evidence report](../reports/research-260930-0905-local-sources-and-evidence.md), [nature report](../reports/researcher-260930-0905-nature-skills.md), [ecosystem report](../reports/researcher-260930-0905-skill-ecosystem.md). |
| Blueprint người dùng | Giữ nguyên, chỉ làm yêu cầu: [blueprint](../../vietnamese-writing-research-skills-blueprint.md). |
| Runtime thực tế | Chưa chốt; phải resolve catalog và interface thật, không suy từ tên skill. |
| Quyền/venue/provider | Chờ người dùng cấp theo task; thiếu thì giữ `pending`/`AUTHOR_INPUT_NEEDED`. |

## Phases

| # | Phase | Status | Estimate | Depends on |
|---|---|---|---|---|
| 1 | [Hợp đồng, router, hooks và adapter](./phase-01-start.md) | Pending | 3–5 ngày | Báo cáo nguồn |
| 2 | [Bằng chứng và research](./phase-02-evidence-and-research.md) | Pending | 2–4 ngày | P1 |
| 3 | [Việt ngữ và English writing](./phase-03-vietnamese-and-english-writing.md) | Pending | 2–3 ngày | P1–P2 |
| 4 | [Slides và scientific visuals](./phase-04-slides-and-scientific-visuals.md) | Pending | 2–3 ngày | P1–P2; P3 cho text |
| 5 | [Đánh giá, chi phí và đóng gói](./phase-05-evaluation-and-packaging.md) | Pending | 3–5 ngày | P1–P4 |

Chi tiết xuyên phase: [routing/hooks/subagents/context/cost](./design-routing-hooks-cost.md) và [official standards, lỗi, blueprint coverage](./standards-and-failure-catalog.md).

## High-level acceptance

- [ ] Mọi execution artifact và receipt truy được về brief, profile, input hash,
  worker/version/hash và nguồn/locator; thiếu receipt không được pass.
- [ ] Plan/cook có quyền riêng; plan-only chỉ ghi hồ sơ lập kế hoạch đúng scope,
  cook không chạy từ plan chưa được cho phép; user không cần gọi từng module.
- [ ] Fault tests không cho phép bịa quote/DOI/page/stat/result, nâng certainty,
  pass Q1/Q2 khi thiếu hệ/category/year, hoặc trộn venue.
- [ ] VI/EN/bilingual giữ số, đơn vị, phủ định, modality và terminology; gu
  cá nhân chỉ được kết luận từ human gold/holdout, không từ self-score.
- [ ] Chart/diagram/artwork phân biệt đúng; PPTX/SVG/native source editable ở
  mức đã hứa, có source/caveat/alt/provenance và render QA.
- [ ] Update candidate chỉ được accepted sau compatibility evaluation; không
  sửa installation global. Chưa có kết quả đánh giá thì trạng thái vẫn pending.
- [ ] Host-tested hooks/subagents và token accounting giữ shared context/cost caps;
  unknown không thành zero và budget không bỏ evidence/human/quality gates.

## Human decisions still pending

- [ ] Chọn runtime/package scope: project-local trước, hay thêm consumer khác;
  xác định host interface được phép gọi và chính sách offline/network.
- [ ] Xác nhận quyền dùng sample văn phong, bản thảo, figure/asset và quyền phân phối; thiếu quyền chỉ dùng synthetic fixtures cho deterministic guards, không thay human VI-taste/evidence/EN gold và không đóng gate chất lượng.
- [ ] Chốt runner, human reviewers/domain reviewers và ngân sách eval/provider;
  không tự dùng credential sẵn có làm đồng ý.
- [ ] Khi có task, chọn `journal|conference|generic`, year/track/article type,
  ranking system/category/metric-year, ngoại lệ nguồn; không chọn một venue mặc định.

## Red Team Review

Người dùng đã duyệt và 11 điều chỉnh đã áp dụng vào các phase; xem [phân xử và mapping](../reports/red-team-260930-0905-adjudication.md). Ba đề xuất loại được giữ nguyên. Bổ sung mới của user về routing/hooks/cost/context đã được tích hợp; chưa có quyền triển khai.

### Whole-Plan Consistency Sweep

Đối chiếu cả năm phase, hai design details và hồ sơ review theo [validation log](../reports/validation-260930-0905-plan-integrity.md). Trạng thái pending là công việc triển khai tương lai, không phải dấu hoàn thành bộ skill.

## Validation Log

[Cấu trúc, liên kết và phạm vi ghi đã kiểm tra](../reports/validation-260930-0905-plan-integrity.md); không phải behavioral evaluation hay user approval.

### Session 2026-09-30 — NCKH portable objective

Đã [thẩm định lại theo objective mở rộng](../reports/validation-260930-1910-nckh-plan-review.md): plan này hợp lệ về cấu trúc nhưng chưa bao phủ Core/Engineer/Marketing, bốn runtime, model profiles và installer mới. [Proposal bảy phase để duyệt](../260930-1910-nckh-portable-skill-kit/plan.md) được giữ riêng; chưa có câu trả lời duyệt kiến trúc mới và chưa có quyền cook. Năm phase, hai design details và blueprint gốc không bị sửa; approval cũ không tự áp dụng cho kiến trúc độc lập mới.

### Session 2026-10-01 — Đã duyệt thay kế hoạch

Người dùng trả lời “tôi duyệt, thay đổi plan đi” cho câu hỏi duyệt hướng NCKH độc lập với AgentKit, namespace/catalog và installer chung. [Kế hoạch NCKH portable](../260930-1910-nckh-portable-skill-kit/plan.md) trở thành authority hiện tại; ghi nhận chưa có approval trong session 30/09 ở trên là lịch sử đã được thay thế. Năm phase và hai design details cũ được giữ nguyên để truy nguyên, không tiếp tục nhận task triển khai. Phê duyệt chỉ thay kế hoạch, chưa cấp quyền cook, cài đặt, paid eval hoặc publication. Xem [approval record, mục 8](../reports/validation-260930-1910-nckh-plan-review.md).

