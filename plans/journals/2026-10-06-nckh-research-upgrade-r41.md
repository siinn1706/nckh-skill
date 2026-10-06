---
title: NCKH research upgrade r41
date: 2026-10-06
summary: "Scientific owners, reproducible artifacts and truthful local qualification"
---

# NCKH research upgrade r41

## Thay đổi

Hoàn tất research upgrade với bốn owner `nckh-dataset`, `nckh-statistics`, `nckh-telemetry`, `nckh-aiops`; bổ sung scientific contracts, bốn authored reference packs và experiment graph/checker dùng stdlib. Candidate r41 có 337 pins, 43 identities, 172 base cases, 13 resource groups và 35 consumer bindings. Giữ lịch sử, writer/visual/hooks và ranh giới engineering/marketing.

## Kiểm chứng và sửa lỗi

Lần r39 pinned regression có hai failures và hai errors: stale counts, fixture thiếu catalog và isolated reader tạo bytecode trong package. Sửa chính xác, không nới validators/post-smoke checks. Lần r40 public deterministic runner chạm giới hạn 900 giây; verbose diagnostic xác nhận assertion Core cũ 12, thực tế 16. Counsel và independent review chấp thuận sửa đúng expected count 16 rồi freeze r41.

Full discovery r41 chạy đủ 311 tests trong 914.791 giây: 310 pass, một Windows symlink fixture skip vì privilege 1314; exit 0, không exclusions và source hashes trước/sau giống nhau. Giữ runner public và receipt timeout cũ; actual pass dùng task-local observable wrapper của cùng full suite.

Hai-build reproducibility trên bốn host cho standalone/plugin, 16 bundles, 420 isolated resource reads, tám relocated checker runs và tám read-only installer previews đều có actual receipts. Independent final review đối chiếu 590 protected hashes, zero mismatch; legacy format 1/2 giữ nguyên. Exact owned external temp được dọn sau snapshot 20.528 files; owned process count cuối là 0.

## Pilot và phạm vi

Actual World Bank Vietnam snapshot có 26 observations, train 20 / validation 3 / test 3. Bổ sung partition reporting tạo 52 outcomes, 49 completed và ba explicit unknown; sáu test predictions gốc giữ nguyên và được đối chiếu bằng Fraction. Chuỗi phụ thuộc hồi cứu, independent_n = 1, source units trống và prior/vintage/availability limits được giữ; scientific acceptance chưa được suy ra từ pilot.

Quick genuine Codex advisory hooks check thực hiện theo chỉ đạo user trước upgrade. Full-native của plan cũ 44/45, semantic agent routing, owner/human/scientific/provider/stable/public và actual install/migration giữ riêng. Candidate chỉ experimental/local-package-only.

## Hồ sơ

- Plan: `plans/261005-0036-nckh-devops-aiops-research-upgrade/plan.md`.
- Delivery: `plans/reports/delivery-261006-research-upgrade-r41.md`.
- Final review: `plans/reports/review-261006-research-final-qualification.md`.
- Receipts: `plans/runs/nckh-upgrade-261006-0850-attempt-01/`.

AgentWiki publish skipped.

> Historical work record — not durable authority. Prefer docs/specs/ADRs for current decisions.
