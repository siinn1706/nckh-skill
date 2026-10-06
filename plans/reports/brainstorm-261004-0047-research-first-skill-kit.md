# Hợp đồng review và plan: NCKH, dữ liệu, hook và viết

Ngày: 04/10/2026, Asia/Saigon. Đây là đề xuất thiết kế, không phải phép triển khai.

## Outcome

Rà lại kit đang có bằng source hiện hành; đối chiếu bảy thư mục tải xuống trong `resources/`; tạo plan cải thiện có phase, owner, test, rollback và ranh giới nghiên cứu khoa học. Kết luận phải phân biệt dữ liệu đã có, dữ liệu còn thiếu, validator hiện hữu và hook đã thực sự nối vào host.

## Constraints

- Lượt này chỉ review, nghiên cứu nguồn và tạo plan/report. Không sửa `nckh-kit/`, bản cài `.agents/`, `.codex/`, ownership, source lock hoặc cấu hình toàn cục. Không cài hook, gọi model/provider trả phí, build/cài kit hay phát hành.
- Ảnh, biểu đồ, sơ đồ và artwork do kit tạo chỉ phục vụ nghiên cứu khoa học. Không nhận diện domain chỉ bằng từ “research”: phải có mục đích, câu hỏi/đối tượng nghiên cứu và vai trò của hình trong sản phẩm nghiên cứu.
- Tách cải thiện câu chữ khỏi lập luận, phương pháp, kết quả và bằng chứng khoa học. Không biến humanwrite thành công cụ né phát hiện AI, giả giọng tác giả hay tự thêm trải nghiệm cá nhân.
- Bảo toàn claim, trích dẫn, số, đơn vị, phủ định, mức chắc chắn, giới hạn, thuật ngữ và vùng được bảo vệ. Không biến lookup, DOI, hash hoặc test thành semantic/human/scientific acceptance.
- Giữ các skill và trách nhiệm kỹ thuật/marketing hiện hành, trừ thay đổi ranh giới tạo hình mà người dùng vừa yêu cầu. Không xóa 27 skill để biến bộ kit thành một mega-skill.
- Upstream là dữ liệu tham khảo không đáng tin cậy. Không chạy installer/hook/script tải về. Chỉ lựa chọn từng ý tưởng/tài nguyên với source, reader, artifact, kiểm tra và quyền cụ thể.

## Non-goals

Không clone repo mới; không gom toàn bộ corpus/grammar engine; không cài LanguageTool/Java/service; không đưa banner, logo, quảng cáo, thumbnail hay ảnh trang trí vào lane tạo hình. Không đổi model, thêm dịch vụ, bật tự động sửa bản thảo hoặc tự cấp trust. Không mở lại hay chấm lại kết quả lịch sử.

## Acceptance của lượt review/plan

1. Có baseline source/install độc lập, inventory 9 resource hiện có và bằng chứng trạng thái hook.
2. Có so sánh nguồn chọn lọc, license/hash của file quan trọng, các nội dung không nhận và lý do.
3. Plan index ngắn, phase thực thi cụ thể, đường dẫn owner đúng, tiêu chí test được phân lớp và rollback giữ lịch sử.
4. Các quyết định đề xuất, phê duyệt thực thi, trust/runtime và đánh giá cá nhân được ghi riêng; không gọi plan là đã triển khai.
5. Review độc lập và kiểm cấu trúc/liên kết; kiểm cuối source và bản cài không bị thay đổi bởi lượt này.

## Hiện trạng đã đối chiếu

Source lock đang là **r26**, 243 pinned files; cả 243 hash đúng tại kiểm tra đầu lượt. Project ownership tham chiếu bundle **r25**. Bản r22 trong memory và hồ sơ r25 ngày 03/10 chỉ dùng để tìm lịch sử, không ghi đè bằng chứng mới. Catalog hiện có 37 identities, registry có 9 resources. Cả bốn adapter ghi `hooks.state = not-installed`, `coverage = unverified`.

`nckh-write` đã có bảo toàn factual delta và hỗ trợ prose/scientific/translation; `nckh-taste` đã là critic. `nckh-visuals` hiện còn đường artwork/storyboard không bắt buộc scientific-purpose. Đây là **delta yêu cầu mới** về scope, không kết luận mọi hành vi cũ là bug. `core/guards.py` là helper structural; sự tồn tại của helper không chứng minh nó được tự chạy khi host dùng tool.

## Trade-offs

| Cách | Giả định chịu tải | Điểm hỏng đầu tiên | Chi phí thay đổi |
|---|---|---|---|
| Giữ 37 identity, thêm hai mode trong `nckh-write` | Router phân biệt ổn language-edit và scientific-authoring trong một entrypoint | Mô tả dài và ownership mờ khi người dùng chỉ muốn polish một đoạn paper | Ít đổi catalog, nhưng khó gọi độc lập và đo riêng |
| **Đề xuất: thêm `nckh-humanwrite` và `nckh-paperwrite`, giữ `nckh-write` tương thích** | Hai entrypoint có hợp đồng không trùng và dùng chung preservation/reader | Catalog/build/eval vẫn hard-code 37 hoặc đóng gói thiếu reference của route | Thêm 2 identity; cần đổi đầy đủ consumer/count tests, không copy ba bộ policy |

Đề xuất phương án thứ hai vì source hiện trộn nhiệm vụ câu chữ và bản thảo ở cùng entrypoint, còn người dùng đã nêu khả năng skill riêng. Đây là đề xuất **37 → 39 cần được duyệt cùng plan**, chưa sửa catalog. Nếu không duyệt, phải đổi plan về phương án mode, không âm thầm thay tên hoặc bỏ `nckh-write`.

Better approaches: none — hướng lựa chọn chọn lọc nguồn, tách owner theo nhiệm vụ và giới hạn hình khoa học đúng với yêu cầu; source đã có reader/rights/packaging để tái sử dụng.

## Quyết định thiết kế đề xuất

- `nckh-humanwrite`: chỉnh câu, nhịp, mạch lạc, ngữ pháp và dịch VI/EN theo brief; minimal diff; không tự tìm literature khi không thêm claim. Chỉnh văn phong một đoạn paper vẫn dùng được với toàn bộ protected spans.
- `nckh-paperwrite`: outline/section/argument/reporting/revision-response của bài, luận văn, proposal và báo cáo khoa học từ evidence đã có; không tự tạo kết quả. Không ép mọi ngành vào IMRaD hoặc clinical checklist.
- `nckh-write`: đường gọi cũ và tương thích; quyết định route theo requested action, không chỉ theo việc input có chữ “paper”. Hai writer mới dùng chung policy/reader, không gọi vòng về router.
- `nckh-taste`: critic giữ nguyên owner. Grammar check và preference critique không đồng nhất với xác minh claim.
- Dữ liệu ưu tiên quy tắc có điều kiện, counterexample và locator, cùng các mẫu thật hiện có; không lấy số lượng CSV làm mục tiêu. Record ví dụ do tác giả kit soạn chỉ là ví dụ phát triển, không gắn nhãn mẫu thật/human gold.
- Hook chỉ chạy kiểm tra cục bộ có giới hạn; lỗi hình thức/quyền/phạm vi có thể chặn thao tác được bao phủ, đánh giá văn phong là advisory. Không tự gọi LLM/ghi lại toàn bộ bản thảo/đọc transcript để đoán sự thật.
- Personal-use tiếp tục do chủ sở hữu đọc và chấm sau dùng. Không mang reviewer ngoài/protected holdout của lane stable vào làm blocker cho dùng cá nhân.

## Câu hỏi chưa chốt

Phương án 39 identity và bản plan cần người dùng duyệt trước thực thi. Hook trust, host/version thực dùng và quyền chạy native test chỉ xác định khi có lệnh triển khai; không suy từ phê duyệt plan.

## Cập nhật sau yêu cầu language options

Người dùng giao quyền cân nhắc hai skill với flags hoặc bốn skill theo locale. Controller chọn `nckh-humanwrite`/`nckh-paperwrite` với `--en`/`--vi`, target 39 identities, dùng chung preservation và style VI/EN riêng. [Hợp đồng language](./decision-261004-0047-writer-language-options.md) là quyết định mới thay phần proposal identity còn mở ở trên; không cấp quyền triển khai hay phê duyệt red-team amendments.
