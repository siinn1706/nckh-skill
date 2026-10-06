---
title: NCKH resource review and source-backed plan
date: 2026-10-02
summary: "Review and approved plan-only amendments: source-backed resource decisions, same-base evaluation, four pending phases; no import or implementation."
---

# NCKH resource review and source-backed plan

## Đã thực hiện

- Review bộ NCKH độc lập 37 identities và đối chiếu AgentKit, Nature Skills, K-Dense, UI UX Pro Max cùng chuẩn Agent Skills/Anthropic eval schemas.
- Phân biệt 184 source pins (75 MD, 71 JSON, 36 Python, 1 PowerShell, 1 shell) với lớp skill Markdown và các dữ liệu chẩn đoán ngoài package.
- Xác minh hai evaluation lanes riêng: package cases còn not-run; direct development trên installed revision 14 có latest 147 pass/1 fail. Không gán điểm development cho source revision 18, human gold hay tác động riêng của skill.
- Xác nhận 37 negative oracles mâu thuẫn expected route, required-family validation chỉ đếm, và giới hạn resource/rights packaging. Bản review: [review](../reports/review-261002-0832-nckh-skill-quality.md).
- Viết [plan bốn phase](../261002-0832-nckh-skill-resource-quality/plan.md) và resource map đủ 37 identities; mọi bước triển khai vẫn pending.

## Quyết định và giới hạn

- Dataset không tự bịa. Shortlist nguồn thật có full commit/file hash, consumer và giới hạn chuyên môn nằm ở [source shortlist](../reports/researcher-261002-0832-source-shortlist.md). Root license/popularity/bytes thật không được coi là human/scientific validation.
- Giữ historical synthetic development records, tách khỏi reusable dataset và holdout/gold. Chưa có corpus VI/EN phù hợp được human review.
- Không thực hiện implementation, import dataset, installation, provider/native run hay publish. Không tạo goal/autoresearch loop cho bài toán exploratory còn quyết định nguồn và acceptance.
- Kiểm tra cấu trúc plan và package pass; narrow suite của controller 19 tests pass. AgentKit quick validator bị thiếu PyYAML; không cài dependency. Source-lock/installed-lock/ownership hashes giữ nguyên.
- Tại thời điểm review trước duyệt: 10 nhóm sau gộp, 7 proposed Accept và 3 Reject. Hai reviewer độc lập và một author self-audit do runtime không cho tạo reviewer thứ ba; không claim ba review độc lập. Khi đó chưa áp dụng proposed changes. Follow-up sau duyệt ghi riêng bên dưới; kiểm tra cú pháp không đồng nghĩa ready to cook. Bản phản biện/validation cuối được liên kết từ plan index.

## Follow-up sau phê duyệt — 02/10/2026

- Người dùng “duyệt” bảy sửa đổi đã thu hẹp ở mức plan. Đã áp dụng R1/R2/R4/R5/R6/R7/R10 vào sáu file, giữ R3/R8/R9 Reject và mọi task triển khai pending; không cần hỏi lại cùng approval.
- Làm rõ P1 quyền ghi freeze/history và P3 format/rights/bundle schema/shared verifier; P2 chỉ chọn/review/stage ngoài pinned source/dist trước khi P3 support và candidate build. Rollback phải đồng bộ source/schema/lock, không restore lock đơn độc hay xóa history.
- Bổ sung bốn candidate-to-consumer decisions từ shortlist đã đọc; clinical lookup chỉ cho study design phù hợp, publisher profile không phải chart data, UI CSV chỉ cho UI, Nature reference không phải corpus. VI/EN vẫn missing/blocked-input; không sinh dữ liệu thay thế.
- Resource effect phải đo off/on cùng base code/instruction policy, giữ same-agent/selective-delegation và hash riêng từng closure/config. Revision 14 migration không chứng minh tác dụng resource; upstream baseline cần subject thật có phép.
- Current runner development-only, tối đa 3 development rounds; 1 protected run và exposure → development giữ nguyên protocol. Timeout 1–900 giây/ca không phải tổng deadline 15 phút. Ca dài hơn cần route/tests/grant; holdout NOT_CALLABLE/pending, không xây engine mới.
- Sau chỉnh sửa đã đọc lại sáu file; validate/parse pass 4 phases/29 pending tasks/0 complete, original matrix exact 37-ID match, bảng phụ 4 candidate decisions. Check 14 documents/35 local links/1 anchor không broken; static source check giữ 184 pins/hash revision 18 và qualification pending. Chi tiết cùng kiểm tra index/journal/integrity ở [validation follow-up](../reports/validation-261002-0832-nckh-resource-plan.md). Không chạy lại unit suite/build/provider; không gọi test lịch sử là test mới.

## Tiếp theo

Amendments ở mức plan đã được duyệt/áp dụng; implementation vẫn cần yêu cầu thực thi riêng cho phạm vi cụ thể. Giữ corpus, reviewer, rights, native/runtime, protected holdout và chất lượng thật ở trạng thái chưa đạt khi thiếu evidence. AgentWiki publish skipped.

> Historical work record — not durable authority. Prefer docs/specs/ADRs for current decisions.
