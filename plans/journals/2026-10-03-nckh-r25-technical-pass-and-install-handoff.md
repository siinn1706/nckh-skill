---
title: NCKH r25 technical pass and install handoff
date: 2026-10-03
summary: r25 checks pass; protected update rolled back; manual installation and final visual QA pending.
---

# NCKH r25 technical pass and install handoff

## Kết quả

Candidate r25 đã đạt 10 commands: full suite 136 tests với 135 pass, một Windows symlink skip, zero failures/errors; build on/off và extracted reads trên bốn host đều đạt. Source lock adc6422394da5a833e1059d922b27c5658eb6699b2ab950568a557d48d71968c giữ 243 pins. Attempt timeout/TEMP cũ được giữ; attempt mới không có deadline tổng và mọi owned process đã cleanup.

## Cài đặt và nguyên nhân dừng

Preview đúng một nckh-visuals replacement, 42 unchanged, zero conflicts. Scoped escalation được chấp nhận nhưng Windows từ chối rename target vào backup bằng WinError 5. Journal rolled-back/no conflicts; physical r24 hash và ownership trước attempt khớp; doctor 43 current. Parent .agents/skills có Deny ACL entries quan sát được. Không thay ACL, cài đè hoặc dừng AGY/PowerShell của người dùng.

## Bàn giao

Người dùng xác nhận IDE hoàn tất vòng sửa 01; Antigravity do người dùng chạy trong PowerShell dangerous. Cursor Django/UCI và current-app VI/GPT-6.1 Sol đã review đạt; Antigravity repair 02 và World Bank SVG/QA còn chờ. Scope current-app chỉ GPT-6.1 Sol; Cursor chỉ Grok 4.7 Extra High; Antigravity Gemini 3.8 Flash High.

Script plans/evaluation/personal-use/complete-r25-install.ps1 đã parser-check và independent review, chưa chạy. Người dùng chạy script từ PowerShell của mình để thực hiện fresh guarded preview/update/doctor/post-preview/installed binding checks. Sau success receipts mới dispatch World Bank prompts. Controller không gửi UI input. Plan giữ in-progress 25/26; owner tự chấm sau personal use, stable/scientific/release scope riêng.

## Bằng chứng

- plans/reports/runtime-261003-1623-r25-verification-and-install-handoff.md
- plans/evaluation/personal-use/candidate-r25-attempt-02/summary.json
- plans/evaluation/personal-use/install-r25-commit-01/stdout.json
- plans/evaluation/personal-use/install-r25-rollback-doctor-01/stdout.json
- plans/evaluation/personal-use/install-r25-denial-observation-01.json

AgentWiki publish skipped.

> Historical work record — not durable authority. Prefer docs/specs/ADRs for current decisions.
