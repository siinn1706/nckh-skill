# Phạm vi và quyền của bản công khai

Chủ sở hữu đã cho phép đưa bộ skill lên repository public `nckh-skill` ngày
03/10/2026. Bản này được tạo từ source lock revision 25, dùng chế độ đóng gói
`resource-access off` có sẵn.

## Nội dung được phân phối

- Bốn package tự chứa instructions và references cho 37 skill.
- Sáu agent tùy chọn với cấu hình kế thừa model của ứng dụng.
- Manifest, source lock và adapter của từng package.
- Phần công cụ cài đặt và schema cần để giữ preview, ownership, doctor, update
  gates và rollback.
- Script kiểm tra package và hướng dẫn dùng bản công khai.

Mỗi manifest khai báo `resource_access: off`, không có resource được bật và không
đóng gói file mang phân loại `copied-upstream`. Registry và source lock vẫn giữ
thông tin nguồn, giấy phép và hash của dữ liệu gốc để bảo toàn provenance.

Các mẫu sao chép, source acquisition, bản build thử, cache, dữ liệu cài đặt local,
prompt, model transcript, kết quả đánh giá và các plan của workspace được giữ
ngoài repository.

## Giới hạn

Bản công khai là package dùng instructions và dữ liệu đầu vào do người dùng cung
cấp. Nó không chứa toàn bộ development source hoặc dữ liệu cần để rebuild bản
resource-on đã dùng trong project cá nhân. Các chức năng build/freeze còn nằm
trong module verifier nguyên bản không phải entrypoint được cung cấp cho bản này.

Các nhãn `experimental`, `native_qualification: unverified` và
`release_rights: local-package-only` trong bản ghi máy của r25 được giữ nguyên.
Quyền chia sẻ instructions và công cụ trong repository được chủ sở hữu cấp cho
bản public này; các nhãn lịch sử không cấp giấy phép tái phân phối tài nguyên
upstream. Việc upload không tự hoàn tất stable/scientific/human qualification.

Repository không gán giấy phép MIT hoặc Apache chung cho toàn bộ instructions
và mã tự viết. Thông tin giấy phép upstream trong metadata chỉ áp dụng cho nội
dung tương ứng; người sử dụng cần xác định quyền của dữ liệu tự cung cấp.
