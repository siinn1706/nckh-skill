# Xuất bản NCKH r46 và dọn bản skill cũ

Ngày: 10/10/2026. Trạng thái: đã xác minh package và bản cài; đang hoàn tất audit
và push GitHub. Bản phát hành giữ nhãn **experimental**.

## Phạm vi và quyền thực hiện

Chủ sở hữu yêu cầu commit bản skill mới nhất lên GitHub và dọn các bản cũ ở
global/local. Candidate debug → fix đã được chấp nhận; sáu file contract giữ đúng
hash của bản review độc lập và không còn finding source cần xử lý.

[Plan](../261010-1106-r46-publish-and-cleanup/plan.md) ghi mục tiêu và acceptance.
[Publication evidence](../261010-1106-r46-publish-and-cleanup/publication-evidence.json)
là summary đã loại thông tin riêng; raw logs, receipts, cấu hình máy và lịch sử
attempt được giữ local.

## Source và package

Source lock revision 46 pin 430 file. Bốn package Claude, Codex, Cursor và
Antigravity khớp source lock và build lặp lại cho cùng closure hash.

Mỗi package có 43 skill, sáu agent tùy chọn, 13 nhóm tài nguyên và 35 binding.
Resource access bật; hooks trong artifact chưa kích hoạt, mặc định cài project ở
chế độ advisory. Giấy phép, attribution và dependency closure được giữ nguyên.

- 52/52 test thuộc ba module regression/runner/agent-runs đã pass.
- Lần test đầu thất bại do thư mục tạm kế thừa skill đã cài ở ancestor; lần chạy
  trong thư mục cô lập pass. Hai receipt được giữ riêng.
- Reproducible build pass cho cả bốn host; public package verifier pass trước và
  sau cleanup (lần sau exit 0, process đã được reap).
- Việc freeze giữ lock r45 trong history. Không sửa skill để vượt guard cài đặt.

## Bản cài được cập nhật

| Phạm vi | Nội dung được kiểm tra | Kết quả |
|---|---|---|
| Global | Năm skill root của bốn host và bốn agent projection | 239 mục khớp hash r46 |
| Project | 43 skill và sáu agent | 49 mục khớp hash r46 |
| Project hooks | 34 thành phần, advisory, đăng ký và bật | Khớp closure r46 |
| Global hooks | Không đăng ký hook global | Off |

Project update thay 43 skill; sáu agent không đổi. Preview đầu phát hiện một
fixture skill r43 trong attempt đã BLOCKED và có observed process exit 0. Sau
khi kiểm tra không còn process tương ứng, 30 file của fixture được lưu trong ZIP
local và đối chiếu từng hash trước khi gỡ định nghĩa cũ khỏi discovery. Verdict
lịch sử được giữ nguyên.

Preview tiếp theo phát hiện payload hook project r41. Công cụ gỡ của đúng bản
r41 kiểm tra ownership và gỡ hook cũ; sau đó preview và update r46 thành công.
Các guard từ chối xung đột không bị sửa hoặc bỏ qua.

## Dọn bản sao cũ

Đã xóa hai root package build cũ: bản dist r14 và package r45 được giữ trước lúc
promote. Tổng cộng 13.505 file, 114.951.678 logical bytes; không có lỗi. Thư mục
test tạm đã rỗng được xóa, thư mục cha được giữ.

Bộ kiểm duyệt tự động từ chối lần dọn kết hợp vì danh sách còn gồm backup
rollback và payload giao dịch. Lệnh bị từ chối chưa chạy. Danh sách này được
tách riêng: 148 root, 16.269 file, 156.554.292 logical bytes, đang chờ quyền xóa
bổ sung từ chủ sở hữu.

Giữ current ownership/journal, source-lock history, các raw failed attempt, ba
plan test r41 cùng attempt được bảo vệ, `github-publication/`, skill không liên
quan và các bản sao `references/_shared` thuộc package closure.

## GitHub và dữ liệu riêng

Đích đã xác minh: `siinn1706/nckh-skill`, nhánh `main`. Remote parent ban đầu:
`fa3c5224d2dfb48d04e4145bb7668f0717587f34`.

Audit của cây local ban đầu tìm thấy 267 đường dẫn raw output và 32 file chứa
đường dẫn máy cá nhân; không có credential thực. Năm commit chưa push được giữ
dưới `refs/backup/r46-unpublished-20261010`, trỏ tới
`76b0429ac3f0fbf851be3e871d9ee53b2a0a284a`.

Tree công khai được tạo trên remote parent đã xác minh, gồm source/package hiện
tại, các helper cần thiết, tài liệu sở hữu và summary của đợt này. Index thường
và file local được giữ trong lúc chuẩn bị. Rà soát 6.761 changed blob ban đầu
không tìm thấy credential, đường dẫn máy riêng, raw-output filename, restricted
prefix hoặc file vượt giới hạn kích thước GitHub. Sau khi thêm summary records,
exact staged tree có 27.367 file, 817.724.785 bytes và publication audit pass với
0 finding. Link check trên 2.165 Markdown file thay đổi đã kiểm 9.964 link và
pass; full tree kế thừa 161 link evidence cũ bị thiếu, không nằm trong file thay
đổi của đợt này.

Commit/push và đối chiếu remote vẫn đang được thực hiện; SHA cuối sẽ bổ sung sau
khi remote được xác minh.

Push dùng đường thông thường. Không rewrite remote history hoặc force-push.
Rollback publication dùng revert/new commit đã review; phục hồi bản cài dùng
package đã xác minh và giao dịch ownership-aware.

## Giới hạn được giữ

Các phép kiểm tra trên xác nhận source/package integrity, reproducibility và
hash của bản cài. Native discovery/trust, precedence, model/effort thực tế,
scientific và human acceptance chưa được xác nhận; stable qualification vẫn
**NO-GO**. Quyết định miễn metadata process lịch sử không tạo ra observation còn
thiếu. Các cell lịch sử trong release checklist giữ nguyên ý nghĩa.
