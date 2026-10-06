---
title: "NCKH skill resource quality — thực thi chọn lọc"
description: "Tài nguyên có consumer cho 37 identities; integrity, lịch sử và qualification được ghi riêng."
status: in-progress
priority: P1
effort: "8–14 ngày công; chưa gồm thời gian chờ corpus, reviewer và runtime gates"
branch: "none (workspace không có Git repository)"
tags: [nckh, resources, provenance, evaluation, portability]
created: 2026-10-02
---

# NCKH skill resource quality

## Outcome và boundary

Thực thi theo `/goal ak-codex-goal ak-cook plan.md --auto` ngày 2026-10-02. Giữ đúng **37 identities / 148 package cases / 19 required families / 224 native cells**. Markdown là mặc định; bốn snapshot có reader, provenance và license riêng đã qua staging/promotion. Các identity khác giữ MD-only. Không tạo corpus tổng hợp mới; VI/EN corpus và chart measurements thật còn `blocked-input`.

Source revision 18 và installed revision 14 là baseline lịch sử bất biến. Revision mới không kế thừa verdict cũ. [Initial freeze](../evaluation/resource-quality/initial-freeze.json), [evaluator freeze](../evaluation/resource-quality/evaluator-freeze.json), [direct linkage](../evaluation/resource-quality/direct-linkage.json) và [promotion receipt](../evaluation/resource-quality/promotion-receipt.json) ghi từng lane. Một answer round-1 của `nckh-cook` thiếu, linkage vẫn pending. Rollback phải khớp source + schema + lock.

## Phases và dependency

| # | Phase | Depends on | Trạng thái / chi tiết |
|---|---|---|---|
| 1 | Test/provenance freeze | Không | Evaluator/linkage/guards đã triển khai; [phase 1](./phase-01-start.md) |
| 2 | Chọn, review và stage resources | P1 freeze | 4 resources, 3 nguồn, quyết định đủ 37 identities; [phase 2](./phase-02-domain-resources.md) |
| 3 | Format/rights/closure, promote, build | P2 packet → P3 support → P1 freeze | Hoàn tất kỹ thuật trên revision 22; [phase 3](./phase-03-resource-packaging.md) |
| 4 | Matched comparison và qualification | P1–P3; inputs/human/runtime grants | Checker đã có; behavioral/human run còn pending; [phase 4](./phase-04-behavioral-qualification.md) |

## Ownership và quyết định

- [Resource map](./resource-map.md) ghi đủ 37 identities và disposition; một registry cho bốn resources, không tạo 37 manifest.
- P2 content → P3 support → P1 freeze đã theo đúng thứ tự. Staging, thất bại kỹ thuật và lịch sử được giữ để review.
- Người dùng chọn **mở rộng CRO để kiểm tra canonical/noindex**; [scope amendment](../evaluation/resource-quality/cro-scope-amendment.json) giữ failure lịch sử. Broader crawl/search analysis vẫn theo SEO.
- Package/native/human/provider/OS/release là các gate riêng. Protected holdout vẫn `pending/NOT_CALLABLE`, current runner development-only; không có tổng deadline 15 phút hay route mới cho case quá 900 giây.

## Measurable acceptance

- [x] Resources có consumer, artifact, source/version/hash, rights, read checks và rollback; đủ 37 disposition.
- [x] Không thêm synthetic dataset; bytes gốc và per-record provenance được giữ, không manufacture missing records hay mix namespaces.
- [x] Candidate/extracted smoke và full deterministic suite có receipt khớp revision cuối; private/unpinned/uncleared data bị chặn.
- [ ] Sáu condition được pin đầy đủ khi có subject/run thật; same-base off/on giữ wrapper/model/budget. Preparation không chứng minh resource benefit; revision 14 migration riêng.
- [ ] Actual corpus/rights/reviewer/threshold/host/model/budget và các gate native/human được duyệt, chạy và review. Stable/public còn **NO-GO**.

## Đầu vào còn thiếu

Corpus VI/EN và phép sử dụng; reviewer cho taste/fidelity/domain/visuals; threshold và coverage; host/OS/model; provider/process budget và economics. Upstream baseline cần skill subject thật được pin và route có phép. Không cấp thêm development round hoặc dựng gold từ model.

## Historical plan review

[Skill review](../reports/review-261002-0832-nckh-skill-quality.md), [shortlist](../reports/researcher-261002-0832-source-shortlist.md), [runtime audit](../reports/code-reviewer-261002-0832-nckh-runtime-evals.md) và [red-team review](../reports/red-team-261002-0832-nckh-resource-plan.md) là hồ sơ trước thực thi. Bảy Accept R1/R2/R4/R5/R6/R7/R10 đã được áp dụng ở mức plan; R3/R8/R9 giữ Reject. Hai review độc lập và một self-audit không được gọi là ba review độc lập. [Validation trước thực thi](../reports/validation-261002-0832-nckh-resource-plan.md) chỉ chứng minh integrity của plan cũ.

<!-- slug: nckh-skill-resource-quality -->
