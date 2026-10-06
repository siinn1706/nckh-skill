---
title: "NCKH: mẫu thật, tiêu chí chính thức và dùng thử cá nhân"
description: "Thực hiện bốn yêu cầu đã được giao theo research → plan → cook."
status: completed
priority: P1
created: 2026-10-03
tags: [nckh, personal-use]
---

# NCKH: mẫu thật, tiêu chí chính thức và dùng thử cá nhân

## Kết quả cần có

37 skill giữ identity hiện tại, dùng nguồn thật và tiêu chí có nguồn chính thức. Người dùng tự dùng, chấm cuối và yêu cầu sửa. Project duy nhất: test-skill; thực thi đã được giao trong mục tiêu hiện tại.

Đã hoàn tất bàn giao personal-use ngày 03/10/2026: **completed, 26/26 đầu việc** theo các phase. Cả ba đầu ra mới đã nhận và review; source/render/native QA của các artifact World Bank đã đạt trong phạm vi receipts. Owner scoring sau sử dụng vẫn `pending-personal-review`.

[Native goal đã chuyển `complete`](../evaluation/personal-use/personal-use-goal-completion-01.json) sau khi kiểm cấu trúc plan, 26/26 phase checkboxes và 139 liên kết nội bộ ở checkpoint validation. Phạm vi model theo quyết định mới của người dùng; qualification rộng hơn của portable/resource-quality giữ riêng.

## Phases

| Bước | Việc cần hoàn thành | Trạng thái | Phụ thuộc |
|---|---|---|---|
| 1 | [Chốt nguồn và phạm vi](phase-01-start.md) | Đã kiểm | Không |
| 2 | [Lấy mẫu thật và nối vào skill](phase-02-sources.md) | Source, reader và package checks đã xong | 1 |
| 3 | [Tiêu chí mặc định cho 37 skill](phase-03-acceptance.md) | Source và checks đã xong | 1 |
| 4 | [Build, cài project và chạy ứng dụng](phase-04-runtime.md) | Completed: r25 checks/build/cài project, repairs và source/render/native QA trong phạm vi đã kiểm đạt | 2, 3 |

## Success Criteria

- [x] Nguồn thật có bytes, quyền, phiên bản, hash, vị trí trích và consumer thực sự đọc.
- [x] Tiêu chí chung và riêng phủ đúng 37 identity, có nguồn chính thức/phạm vi áp dụng.
- [x] Personal-use cho owner tự chấm cuối; external reviewer/protected holdout không chặn lane này.
- [x] r25 có tests/build/extracted checks và project installation receipts đạt; physical after/backup hashes, doctor, post-preview và ba installed binding integrity checks đã kiểm. Giữ lịch sử r14/r22/r24 và các failed attempts.
- [x] Cursor/Grok 4.7 Extra High, Antigravity/Gemini 3.8 Flash High và current-app/chỉ GPT-6.1 Sol có output/run trong phạm vi đã giao: current-app giữ native trace; hai IDE có đầu ra/receipts và người dùng xác nhận đã thực thi prompt. Các lỗi review và hợp đồng SVG đã được sửa, kiểm lại theo artifact/revision thực. Model theo prompt/user report giữ riêng với effective provider telemetry chưa xác minh.
- [x] Checklist bàn giao tách việc đã làm và phần người dùng tự đánh giá sau khi dùng.

## Bằng chứng và quyết định

[Hợp đồng](../reports/brainstorm-261003-personal-use-contract.md) · [Nguồn](../reports/researcher-261003-real-sources.md) · [Tiêu chí](../reports/researcher-261003-official-acceptance.md) · [Runtime](../reports/scout-261003-project-runtime.md).

Baseline: source bắt đầu r22; project trước cập nhật cài r14. Kết quả cũ chỉ áp dụng subject cũ. Người dùng xác nhận @ChatGPT là ứng dụng đang mở chat này, local project. Selected model và effective model được ghi riêng. Không tự cấp stable/scientific certification hoặc human acceptance.

Checkpoint lịch sử r24: 120/120 tests và package checks đạt, 43 installed items current tại lần kiểm đó. [Bằng chứng runtime](../reports/runtime-261003-candidate-r24-checkpoint.md) · [Checklist](../reports/checklist-261003-hoan-thanh-plans.md) · [Nhật ký r24](../journals/2026-10-03-nckh-r24-personal-use-resources-and-runtime-checkpoint.md). Hai IDE đã hoàn tất năm memo và sáu reader receipts mỗi ứng dụng; các receipts khớp installed source r24. Current app/chỉ GPT-6.1 Sol đã tạo artifact VI thật, exit 0 và đóng owned process group. Selected/requested model được ghi riêng; effective model/effort vẫn unknown/null. Các run này chỉ bao phủ năm consumer identities của năm ca nguồn thật, không kiểm hành vi native của cả 37 skills.

Checkpoint lịch sử ngày 03/10/2026, trước khi nhận ba đầu ra mới lúc 21:13–21:29: neutral shared roots và task current-app đã đóng theo [review VI attempt 03](../reports/review-261003-1448-gpt-6-1-sol-r24-repair-01.md); plan khi đó **in-progress, 25/26**, còn IDE repairs/SVG/QA. [Cursor repair review](../reports/review-261003-1448-cursor-r24-repair-01.md) đóng Django/UCI; [Antigravity repair 01 review](../reports/review-261003-1448-agy-r24-repair-01.md) đóng EN claim/Django/UCI, còn chú giải VI/self-count EN ở thời điểm đó. Các reviews giữ scope artifact, không xác nhận effective telemetry hoặc owner score.

[Checkpoint kỹ thuật r25](../reports/runtime-261003-1623-r25-verification-and-install-handoff.md) ghi 10 technical checks đạt: 136 tests gồm 135 pass/một skip, bốn host build on/off và extracted reads pass. Source r25 đã review/freeze 243 files. Các update trước, gồm [lượt script thủ công thất bại](../reports/runtime-261003-1720-r25-manual-failure-and-lock-diagnosis.md), đã rollback về r24 và được giữ làm lịch sử; không thay ACL. Sau khi người dùng đóng Cursor, [receipt cài r25 thành công](../evaluation/personal-use/install-r25-after-cursor-close-01/receipt.json) ghi update exit 0, transaction committed, install identity giữ nguyên, physical after/backup hashes khớp, doctor 43 current, post-preview 43 unchanged và ba binding integrity checks đạt. [Review cài đặt độc lập](../reports/review-261003-1757-r25-project-install.md) có 14 checks PASS, không có finding chặn cài đặt. Project hiện cài r25; kết quả chỉ xác nhận installation/binding integrity. Wrapper hiển thị lỗi đã sửa bằng actual retained stderr; SVG checker có 12 focused tests đạt, không thay candidate r25 và không thay final-artifact QA.

Closeout ngày 03/10/2026: [cả ba đầu ra mới đã nhận và kiểm](../reports/runtime-261003-2137-three-prompts-and-personal-use-closeout.md). [Antigravity repair 02](../reports/review-261003-2137-agy-repair-02.md) đóng chú giải VI và self-count EN; conclusion giữ nguyên, 161 whitespace-separated tokens. [Source audit hai IDE](../reports/review-261003-2137-ide-worldbank-source-and-receipts.md) và [final native QA review](../reports/review-261003-2137-ide-worldbank-controller-qa.md) đạt trong scope receipts, không có blocker. Hai SVG có 26 source marks; native AGY 29 text frames, Cursor 166, mỗi bản 26 paths/zero raster; actual render và chuỗi edit/save/close/reopen/restore đã kiểm. [Run receipt current-app/chỉ GPT-6.1 Sol](../evaluation/personal-use/native/app-gpt-6-1-sol-r25-visual-attempt-01/gpt-6.1-sol/real-source-worldbank-visual-01/receipt.json) giữ generation-time `completed-unreviewed`; [source review](../reports/review-261003-gpt-sol-r25-worldbank-source-and-memo.md) và [controller QA sau đó](../evaluation/personal-use/native/app-gpt-6-1-sol-r25-visual-attempt-01/gpt-6.1-sol/real-source-worldbank-visual-01/controller-qa.json) ghi verdict thực cho artifact đã gắn hash.

AGY SVG/PNG byte-identical với GPT-6.1 Sol trước đó, không xác lập independent Gemini generation. Reader receipts tái dùng không chứng minh fresh execution. AGY raw memo tự ghi Source truth pass sớm được giữ; [reviewed memo](../evaluation/personal-use/native/agy-gemini-r25-visual-01/controller-qa-01/reviewed-memo.md) và [revision receipt](../evaluation/personal-use/native/agy-gemini-r25-visual-01/controller-qa-01/memo-revision.json) hiệu chỉnh nhãn thời điểm/model provenance, giữ SVG không đổi. Owner review vẫn pending, effective telemetry chưa xác minh; accessibility chỉ gồm structural/contrast checks, chưa thử công nghệ hỗ trợ. [Audit blocked](../reports/blocked-audit-261003-native-r24.md) và các failures là lịch sử; `get_goal` trả active tại checkpoint closeout trước khi controller chốt docs/validation và cập nhật goal. r24, raw outputs và failed attempts được giữ.

[Review current-app QA độc lập](../reports/review-261003-gpt-sol-r25-worldbank-controller-qa.md) đạt integrity/native checks đã giao; [nhật ký r25 trước](../journals/2026-10-03-nckh-r25-installed-and-gpt-sol-world-bank-controller-qa.md) giữ checkpoint installation/current-app QA lúc IDE còn mở. [Nhật ký closeout](../journals/2026-10-03-nckh-three-prompts-reviewed-and-personal-use-handoff.md) lưu bàn giao personal-use hoàn tất. Portable/resource-quality qualification vẫn mở; completion này không cấp scientific/stable/human certification hoặc publishing clearance.

Cursor chỉ được test **Grok 4.7 Extra High**; Antigravity dùng **Gemini 3.8 Flash High**; ứng dụng hiện tại chỉ **GPT-6.1 Sol**. Tám model current-app khác đã bị loại khỏi scope hiện tại theo quyết định người dùng; failures batch cũ giữ làm lịch sử, không còn câu hỏi xin chạy cả batch và không dùng fallback.

<!-- slug: nckh-personal-use-sources-and-standards -->
