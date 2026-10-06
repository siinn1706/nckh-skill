---
title: personal-research-skill-kit-plan
date: 2026-09-30
summary: "Plan-only: approved eleven revisions applied; automatic plan/cook routing, scoped standards, hooks/subagents and shared context/cost budget; no implementation."
---

# personal-research-skill-kit-plan

## Kết quả trong phiên

Đã nghiên cứu blueprint/ZIP, AgentKit engineer và marketing, nature-skills, các nguồn official/community bổ sung và công cụ tìm/kiểm nguồn. Cập nhật [kế hoạch năm phase](../260930-0905-vietnamese-research-skill-kit/plan.md) và [tổng hợp lựa chọn](../reports/synthesis-260930-0905-skill-kit-selection.md). Sau khi người dùng duyệt, áp dụng đủ 11 điều chỉnh đã phân xử; thêm yêu cầu về automatic catalog routing, hooks/subagents, official rule cards và ngân sách. Kiểm tra cấu trúc AgentKit đạt; parser ghi 5 phase, 57 mục thực hiện, 0 mục hoàn tất. 61 đường dẫn CREATE tương lai không trùng và chưa tồn tại; blueprint/ZIP giữ nguyên SHA256. Không tạo package, cài extension/skill, thay cấu hình global, chạy provider trả phí hoặc tạo slide/ảnh.

## Quyết định và giới hạn

Ưu tiên wrapper gọi skill AgentKit rồi đánh giá đầu ra, có compatibility gate khi upstream đổi; skill instructions bằng English, output VI/EN độc lập. Người dùng chỉ cần plan → cook, không bắt tag từng module; router tự đọc live catalog, shortlist và nạp đầy đủ skill phù hợp. Quyền lập kế hoạch tách quyền thực hiện. Tách venue theo từng task và giữ bằng chứng/Q1-Q2/gu cá nhân là các kiểm tra khác nhau.

[Routing/budget detail](../260930-0905-vietnamese-research-skill-kit/design-routing-hooks-cost.md) đặt ngưỡng mềm `min(20k, 10% W)`, trần cứng `min(40k, 20% W)` cho skill context; shared pool gồm controller và worker còn giữ context, không nhân quota theo số agent. Cached/inherited instructions vẫn được tính; thiếu telemetry không được nhận compliant hoặc zero-cost. Hooks phải kiểm theo host/tool path thật; optional reminders không là enforcement. Chi phí tối ưu trên task accepted đủ scope/quality, không đánh đổi evidence/human gates.

[Standards/failure catalog](../260930-0905-vietnamese-research-skill-kit/standards-and-failure-catalog.md) tách policy chính chủ, reporting guidance, university heuristics và personal taste, với 20 failure classes và blueprint coverage. Nature policy chưa resolve được vẫn unverified. Không biến giới hạn thiết kế hay fault fixtures tương lai thành hiệu quả đã đo.

CLI tạo file plan nhưng không cập nhật được global index do quyền truy cập; giữ file trong workspace, không sửa cài đặt. Các API/tool và license chưa kiểm đủ vẫn là gate mở. Quyết định áp dụng 11 findings đã có và không hỏi lại; nghiệm thu runtime, human corpus/review, ngân sách tiền/provider và venue cụ thể vẫn chờ lúc triển khai/task thật. Xem [validation](../reports/validation-260930-0905-plan-integrity.md) cho kết quả sweep cuối; không xem parser pass là bằng chứng hiệu quả skill.

AgentWiki publish skipped; nhật ký chỉ lưu cục bộ.

> Historical work record — not durable authority. Prefer docs/specs/ADRs for current decisions.
