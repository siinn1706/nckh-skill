---
title: "NCKH r41 AGY full skill test attempt-01"
date: 2026-10-06
summary: "Thực thi toàn bộ 4 phase của plan test native AGY r41 cho 43 skill trên CLI và IDE; xác lập 494 testcases và 35 resource bindings"
---

# NCKH r41 AGY full skill test attempt-01

## What happened

Executed all four phases of plan `plans/261006-2210-r41-agy-full-skill-test` under `--auto`:
1. **Phase 1 (Pin, isolate và preflight)**: Đóng băng hashes của package canonical `publication-r41/agy`, bộ test chung r41, fixtures và report template. Ghi nhận phiên bản AGY CLI quan sát được (`1.3.0`, adapter khai báo `1.2.13`) và IDE (`unknown`). Lưu `pin.json`, `source-validation.json`, `published-source-validation.json`, `host-version.json`, `trust-before.json`, `ownership.json`, và `preflight-summary.json` dưới `plans/runs/r41-agy-attempt-01/`.
2. **Phase 2 (Chạy 43 skill và supplemental)**: Chuẩn bị độc lập 247 testcases cho mỗi surface (`agy-cli` và `agy-ide`), tổng cộng 494 cases (215 skill cases = 172 base + 43 fixture-contract, 12 domain scenarios, 20 writer scenarios). Mỗi case có thư mục riêng với `prompt.md`, `workspace/` (bản sao 15 fixtures) và `result.json` trạng thái `NOT_RUN` (do turn hiện tại chỉ cấp quyền `plan-and-structure-only`). 56 invocation cells và 64 writer native cells được theo dõi độc lập ở chiều coverage riêng.
3. **Phase 3 (Resources, hooks, native agent và installer)**: Chạy `resource-smoke.py` trên `publication-r41/agy` trong thư mục cwd ngoài độc lập với `--unset-pythonpath`, kết quả 35/35 resource bindings đều PASS (`resource_read: true`, exit status 0). Lập ma trận lỗi `HOOK-01..HOOK-09`, kiểm tra 6 native agent roles `NATIVE-04`, plugin lifecycle `PLUGIN-01`, và 10 installer acceptance cases `INSTALL-01..INSTALL-04`.
4. **Phase 4 (Report, retry và cleanup)**: Xuất báo cáo chi tiết `plans/reports/test-261006-2210-r41-agy-attempt-01.md`. Dọn dẹp sạch toàn bộ thư mục tạm ngoài. Kiểm tra `ak plan validate` và `ak plan parse` với workspace-local `AGENTKIT_HOME`, kết quả `valid: true`.

## Decision

- Giữ nguyên trạng thái plan là `pending` theo hợp đồng phase 4 cho tới khi có authority và bằng chứng thực thi native interactive sessions.
- Giữ nguyên sai khác inventory cục bộ (`tests/release/test_kit_read.py` trong `nckh-kit`) và sử dụng comparator đã đóng băng (`published-source-validation.json`), không can thiệp sửa mã nguồn hay cập nhật source-lock.
- Không tự ý dispatch các phiên tương tác mô hình hoặc gọi nhà cung cấp trả phí khi chưa có sự ủy quyền rõ ràng.

## Next steps

- Khi được cấp quyền thực thi native interactive, triển khai chạy dispatch cho từng cell trong 494 cases đã chuẩn bị sẵn theo từng surface `agy-cli` (1.3.0) và `agy-ide`.

> Historical work record — not durable authority. Prefer docs/specs/ADRs for current decisions.
