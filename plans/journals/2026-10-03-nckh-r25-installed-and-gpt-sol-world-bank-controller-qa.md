---
title: NCKH r25 installed and GPT Sol World Bank controller QA
date: 2026-10-03
summary: "Project installation verified; source, render and editable native artifact checked; IDE follow-up remains open."
---

# NCKH r25 installed and GPT Sol World Bank controller QA

## Kết quả

Project r25 đã cài thành công sau khi người dùng đóng Cursor. Installer transaction 7f2ef90a08ad4fd6b3d44b79a739f5ba committed; doctor43 current, post-preview43 unchanged và ba binding integrity checks đạt. Review độc lập14 checks PASS. Các failure/rollback trước được giữ.

World Bank chạy bằng duy nhất GPT-6.1 Sol: exit0 sau286.531 giây, owned-process-group-closed. Raw answer và receipt được giữ. Review nguồn độc lập xác minh26 giá trị/circle/polyline/table, arithmetic, hashes và actual reader trace. Controller extract nguyên SVG, render bằng bound rsvg2.40.20 và mở trong Illustrator28.0.0.

Native QA:29 khung chữ,26 data paths, không raster; sửa chữ và một điểm rồi lưu/đóng/mở lại, thay đổi giữ nguyên. Khôi phục rồi lưu/đóng/mở lại, chữ khớp SVG và điểm lệch tối đa0.0000229375 SVG units. Cả hai render đã nhìn; không thấy cắt/chồng chữ hoặc thiếu dấu. Contrast6.0989–15.3707. SVG title/desc/lang/ARIA/order có kiểm; chưa chạy assistive technology user testing. Native AI metadata preservation và exact rsvg font resolution không được xác lập.

## Bằng chứng

- Runtime report: ../reports/runtime-261003-1757-r25-installed-and-visual-followup.md
- Source review: ../reports/review-261003-gpt-sol-r25-worldbank-source-and-memo.md
- Controller QA: ../evaluation/personal-use/native/app-gpt-6-1-sol-r25-visual-attempt-01/gpt-6.1-sol/real-source-worldbank-visual-01/controller-qa.json
- Native evidence: ../evaluation/personal-use/native/app-gpt-6-1-sol-r25-visual-attempt-01/gpt-6.1-sol/real-source-worldbank-visual-01/illustrator-tool-evidence.json

## Quyết định và phần còn lại

Plan personal-use vẫn in-progress25/26. Người dùng tự gửi prompt; chưa có Antigravity repair02 và hai IDE WorldBank outputs. Cursor chỉ Grok4.7 Extra High, AGY Gemini3.8 Flash High, current-app chỉ GPT-6.1 Sol, không fallback. Effective model/effort telemetry null; owner feedback pending-personal-review. Goal tool vẫn blocked và không có resume API; không ghi goal active/complete. Không publish hoặc cấp stable/scientific/human certification.

> Historical work record — not durable authority. Prefer docs/specs/ADRs for current decisions.
