---
title: Review NCKH research data hooks writing
date: 2026-10-04
summary: "Review source r26, installed r25 và đề xuất selective data, hai writer, research-only visuals, portable hooks; chưa triển khai."
---

# Review NCKH research data hooks writing

## Đã kiểm chứng

- Source r26 có 37 identities, 9 resources và 243 pinned files khớp hash. Installed candidate r25 có 43 items current; doctor chỉ đọc thành công, không visibility conflict. Bốn pin khác nhau là registry/rights metadata, không phải JSONL payload.
- Bốn adapter ghi hooks not-installed/coverage unverified; structural guards chưa phải event wiring. Tài liệu host đã được đối chiếu, nhưng chưa cấu hình/trust hay chạy hook NCKH.
- Bảy archive trong resources đã được rà có giới hạn. Không có Git metadata của archive; không suy commit cho toàn bộ bản tải từ các selected-file pins. ClaudeKit LICENSE xung đột metadata MIT nên plan không sao chép code/hooks.

## Đề xuất, chưa phê duyệt thực thi

- Thêm nckh-humanwrite và nckh-paperwrite, giữ nckh-write tương thích. Ban đầu 37 → 39 là proposal; sau đó user giao quyền chọn cách tách ngôn ngữ, controller chốt hai writer dùng --en/--vi, không bốn identity. Implementation vẫn pending.
- Tái dùng 9 packs theo đúng consumer và quyền; Humanizer chỉ adaptation có điều kiện, không né AI detector. LanguageTool English diagnostics là tùy chọn, không dependency bắt buộc.
- Tạo hình chỉ phục vụ nghiên cứu, bao gồm kiểm tra lối gọi gián tiếp; chart phải có nguồn, illustration phải ghi không phải evidence.
- Một checker cục bộ và bốn host codecs, mặc định tắt; native trust, cài đặt và acceptance là các gate riêng.

## Hồ sơ và bước tiếp

Plan nằm tại [plan.md](../261004-0047-nckh-research-data-hooks-writing/plan.md); nguồn và baseline nằm trong các report cùng mã 261004-0047. Sau phản biện độc lập, controller ghi adjudication/validation và xin duyệt các điều chỉnh có ảnh hưởng trước khi sửa phase theo review. Không có implementation, build/install, paid/model/native evaluation hay publication trong lượt này.

Ba review tạo 15 finding; gộp còn 12 nhóm, đề xuất Accept 9 và Reject 3. Chín amendment chưa user-approved. Quyết định language options mới đã được đưa vào plan; không coi nó là phê duyệt các review amendments khác. AgentKit parse lại sau language delta sẽ ghi số task mới, không đánh dấu task implementation nào đã xong.

## Sự cố trong lượt

Một lần đọc output doctor khi tiến trình chưa kết thúc làm parse JSON thất bại; đã đối soát tiến trình và chạy lại có theo dõi, hoàn tất exit 0. Một số truy vấn diện rộng chạm thư mục tạm access-denied; đã thu hẹp đường dẫn. Reconcile tiến trình sau compaction không thấy owned worker còn chạy. Không sửa quyền hoặc global config.

AgentWiki publish skipped. Đây là nhật ký lịch sử, không thay thế tài liệu hiện hành hay phê duyệt của người dùng.

## Tiếp tục sau approval A1–A9

User đã trả lời “duyệt 9 điều chỉnh” và “duyệt tất cả điều chỉnh”. Đã áp dụng chín amendment vào cùng plan: sequencing freeze/tests, exact 39/156, hook package/config transaction, persistent build chain, explicit resource consumers, Humanizer Markdown + writer matrix, computed/simulation scope và enforcement limits. Giữ quyết định hai writer có --en/--vi. Đoạn xin duyệt phía trên là lịch sử, không còn gate chờ approval amendment.

Theo `ak-plan`, cập nhật phase tasks/owners/validation/rollback và kiểm toàn plan; theo `ak-journal`, giữ record lịch sử này thay vì coi journal là product authority. Kết quả kiểm sau sửa ở [validation mới](../reports/validation-261004-1002-approved-plan-amendments.md). Không sửa source/install/config, không build/trust/native/model/provider run hay publish; mọi task implementation vẫn pending.

Checkpoint sau sửa: plan validate/parse PASS, 4 phase/45 tasks/0 done; 33 local links và 1 anchor hợp lệ; 243 source pins/lock/ownership không đổi. Local index đã backup hash-verified rồi reindex, journal validate PASS. Review+plan hoàn tất, không chuyển trạng thái phase triển khai sang completed.
