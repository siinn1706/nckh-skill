---
title: "Phase 3: Tiêu chí và owner feedback"
status: completed
---

# 3. Tiêu chí và owner feedback

## Requirements

Dựa vào [official packet](../reports/researcher-261003-official-acceptance.json). Mặc định gồm route/identity, behavior, output/facts, authority và receipts/feedback. Giữ applicability, không gán ngưỡng tự đặt cho nguồn hoặc xếp hạng toàn cầu.

## Todo

- [x] Đưa common criteria và 37 rows/source URLs vào shared profile có consumer.
- [x] Nối acceptance policy mà 37 skill đã đọc tới profile; lookup theo skill ID.
- [x] Mặc định personal-use: owner tự dùng/chấm/sửa; reviewer ngoài/holdout không prerequisite. Historical stable/scientific lane nguyên.
- [x] Đồng bộ execution/cook để routine authorized phases tiếp tục.
- [x] Owner feedback bind artifact/revision/input; absent feedback pending-personal-review.
- [x] Test 37 IDs/source refs/applicability/feedback mismatch và package reachability.

Bằng chứng: [implementation](../reports/implementation-261003-personal-acceptance.md), [technical review](../reports/review-261003-personal-acceptance.md). Bản cuối có 7 acceptance tests và 24 focused regression tests pass; simulated closure đúng 37 skill, zero broken remapped links. Freeze/build/install/native observations thuộc phase 4. Owner chưa chấm artifact.

## Files and implementation

Acceptance worker đọc catalog/report JSON, core/policies/acceptance-policy.md, core/workflows/execution.md, skills/core/nckh-cook/SKILL.md, core/state.py, receipt schema và historical qualification protocol. Chỉ sửa policy/workflow/cook, core/profiles/acceptance/ JSON, acceptance helper/reader/tests riêng nếu cần. Không sửa historical protocol/receipts, resource registry/reader/install/source lock. Controller sở hữu docs và freeze.

## Validation, risk and rollback

Profile lookup trả source/scoped checks; không gọi structural pass là quality pass. Generated closure phải chứa profile cho cả 37 skill. Feedback cá nhân không đổi scientific verdict. Rollback policy/profile/workflow cùng revision bindings; giữ protocol lịch sử.
