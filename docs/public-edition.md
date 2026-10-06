# Phạm vi và quyền của bản công khai

Chủ sở hữu đã cho phép đưa bộ skill lên repository public `nckh-skill` ngày
03/10/2026. Bản cập nhật ngày 06/10/2026 được chủ sở hữu cho phép đăng cùng data và hook,
được tạo từ source lock revision 38, dùng chế độ đóng gói
`resource-access on` theo yêu cầu của chủ sở hữu. Các package phân phối luôn bật
tài nguyên; verifier từ chối package bị chuyển sang `off` hoặc thiếu tài nguyên.

## Nội dung được phân phối

- Bốn package tự chứa instructions và references cho 39 skill.
- Chín nhóm tài nguyên cùng reader, giấy phép, ghi công và provenance đi kèm.
- Sáu agent tùy chọn với cấu hình kế thừa model của ứng dụng.
- Manifest, source lock và adapter của từng package.
- Phần công cụ cài đặt và schema cần để giữ preview, ownership, doctor, update
  gates và rollback.
- Script kiểm tra package và hướng dẫn dùng bản công khai.

Mỗi manifest khai báo `resource_access: on`, bật đủ 9 nhóm tài nguyên qua 27
binding giữa tài nguyên và skill sử dụng. Verifier kiểm tra file, hash, giấy
phép, reference closure và binding thực tế. Reader mặc định dùng `on` và trả lại
nguồn/record cụ thể; lỗi đọc hoặc sai hash cần được xử lý tại nguồn lỗi.

Source acquisition thô, bản build thử, cache, dữ liệu cài đặt local, prompt,
model transcript, kết quả đánh giá và các plan của workspace được giữ ngoài
repository. Chỉ các resource đã đăng ký trong gói mới được phân phối.

| Nhóm tài nguyên | Giấy phép/nguồn quyền |
|---|---|
| Reporting và publisher references từ K-Dense | MIT, kèm license và attribution |
| UI heuristics từ UI UX Pro Max | MIT, kèm license và attribution |
| English writing advice từ Nature Skills | Apache-2.0, kèm license và attribution |
| Ba đoạn văn/thơ Wikisource | CC BY-SA 4.0 cho page text; giữ trạng thái tác phẩm gốc và ghi công |
| Hai mẫu bài khoa học Europe PMC | CC BY 4.0 ở cấp bài, kèm PMCID/DOI và nguồn |
| Dân số Việt Nam từ World Bank | CC BY 4.0 của indicator, kèm World Bank và data-provider attribution |
| Mười dòng UCI Bank Marketing | CC BY 4.0, kèm DOI và ghi công tác giả |
| Hai code fixture Django | BSD-3-Clause, kèm notice của đúng hai tệp |

Xem [ghi công bổ sung và nguồn kiểm tra](resource-attribution.md). Các snapshot
là mẫu có phạm vi giới hạn; đọc được một mẫu không xác nhận chất lượng, tính đại
diện hoặc scientific acceptance của toàn bộ domain.

## Giới hạn

Bản công khai chứa package có tài nguyên đi kèm và hỗ trợ dữ liệu đầu vào do
người dùng cung cấp. Nó không chứa toàn bộ development source để rebuild kit.
Các chức năng build/freeze còn nằm trong module verifier nguyên bản không phải
entrypoint được cung cấp cho bản này.

Các nhãn `experimental`, `native_qualification: unverified` và
`release_rights: local-package-only` trong bản ghi máy của r38 được giữ nguyên.
Quyền chia sẻ instructions và công cụ trong repository được chủ sở hữu cấp cho
bản public này; các nhãn lịch sử không cấp giấy phép tái phân phối tài nguyên
upstream. Việc upload không tự hoàn tất stable/scientific/human qualification.

Repository không gán giấy phép MIT hoặc Apache chung cho toàn bộ instructions
và mã tự viết. Thông tin giấy phép upstream trong metadata chỉ áp dụng cho nội
dung tương ứng; người sử dụng cần xác định quyền của dữ liệu tự cung cấp.

## Hook đóng gói

Bốn package có hook runner, codec/template theo ứng dụng, manual checker và công
cụ cấu hình cùng dependency được pin. Installer mặc định kích hoạt hook advisory
cho project khi xác nhận cài/cập nhật. Artifact chưa được cài vẫn ghi trạng thái
chưa đăng ký/kích hoạt, cùng `install_default: advisory`. Plugin projection chưa kích hoạt.
Xem [hướng dẫn hook](portable-hooks.md).
