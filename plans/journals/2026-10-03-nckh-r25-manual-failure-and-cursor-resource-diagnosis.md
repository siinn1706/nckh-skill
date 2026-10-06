---
title: NCKH r25 manual failure and Cursor resource diagnosis
date: 2026-10-03
summary: Manual update rolled back; Cursor resource use observed; checker repairs verified; installation pending.
---

# NCKH r25 manual failure and Cursor resource diagnosis

## Kết quả

Lượt người dùng chạy complete-r25-install.ps1 có preview một replace/42 unchanged/zero conflicts nhưng update vẫn WinError 5, exit 4. Transaction e0b28729028a4ff19848292e73f10feb rolled-back, ownership bằng journal index_before, target hash r24 nguyên, stage r25 đúng và backup chưa tạo. Controller doctor có 43 current.

## Chẩn đoán và sửa

Restart Manager qua read-only diagnostic với escalation xác nhận Cursor PID31492 đang dùng 21 regular files của nckh-visuals; Start/Register/GetList/End đều exit0. Đây là resource-holder evidence, chưa chứng minh duy nhất nguyên nhân rename failure. Người dùng được yêu cầu lưu/thoát Cursor trước reobserve/retry, không thay ACL hoặc tự dừng app.

Wrapper install-candidate.py đã sửa lỗi multi-JSON stderr bằng actual retained logs. SVG checker sửa chia-zero/malformed-points/affine-coordinate false-pass; delegate báo 12 focused tests pass, source/test hashes được controller đối chiếu. Independent reviewer turn lỗi provider503, không claim source-review complete. Controller dọn đúng15 thư mục rỗng failed-temp fixtures sau exact path/time/no-reparse/empty checks; không thay ACL.

## Còn lại

r25 vẫn chưa cài; Antigravity repair02 và World Bank SVG/QA chưa có. Plan25/26, goal active. Model scope giữ nguyên. Bằng chứng: plans/reports/runtime-261003-1720-r25-manual-failure-and-lock-diagnosis.md. Không lặp full suite/build đã đạt.

AgentWiki publish skipped.

> Historical work record — not durable authority. Prefer docs/specs/ADRs for current decisions.
