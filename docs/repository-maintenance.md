# Bảo quản và xuất bản repository

Tài liệu này giúp người dùng và agent phân biệt source cần giữ, tài nguyên tham
khảo, evidence lịch sử và dữ liệu riêng trên máy trước khi dọn workspace.

## Nơi sở hữu nội dung

| Nội dung | Nơi tra cứu |
|---|---|
| Instructions, code và contract của kit | [Chỉ mục kit](../nckh-kit/docs/index.md) |
| Phiên bản source và hash | [Source lock](../nckh-kit/core/registry/source-lock/source-lock.json) |
| Cập nhật global và ownership local | [Deployment utility](../scripts/install-global-kits.py) và `.nckh-state/global-kit-deployment.json` |
| Package đang phân phối | [Packages](../packages/) và [verifier](../scripts/verify-public-package.py) |
| Snapshot upstream để tham khảo | [Reference sources](reference-sources.md) và license/notice trong từng snapshot |
| Resource được kit thực sự sử dụng | [Registry](../nckh-kit/core/registry/catalog/resources.json) |
| Thiết kế ban đầu | [Blueprint](../vietnamese-writing-research-skills-blueprint.md) |
| Kế hoạch, review và evidence theo lần chạy | [Plans](../plans/) |
| Quyền và giới hạn bản công khai | [Public edition](public-edition.md) |

Snapshot tham khảo không đồng nghĩa với dependency đã được chọn, công cụ đã
được cài hoặc chất lượng khoa học đã được chấp nhận. Giấy phép/notice upstream
áp dụng cho phần tương ứng; việc đặt chúng cùng repository không tạo giấy phép
chung cho mã và instructions tự viết.

## Ranh giới dọn dẹp

Giữ source được pin, package phân phối, license/attribution, thiết kế, kế hoạch,
báo cáo và evidence cần để hiểu kết quả lẫn giới hạn. Build thử và bản export
trùng lặp có thể dọn sau khi đối chiếu package và source lock.

Logs thô, transcript, prompt ghi lại từ phiên chạy và biên nhận cài đặt riêng
trên máy không thuộc bản công khai. Khi dọn lịch sử, giữ kết luận cùng trạng thái
pass/fail/blocked/unverified; không biến việc xóa trace thành bằng chứng đã pass.
Evidence đã loại thông tin riêng phải được nhận diện là bản chia sẻ, không dùng
hash của nó thay cho hash artifact gốc.

Giữ state ownership và journal hiện tại để cập nhật hoặc gỡ đúng file. Bản sao
rollback và payload giao dịch cũ chỉ được xóa sau khi kiểm tra bản thay thế và
có quyền xóa riêng; xóa chúng làm mất khả năng rollback về lần cài trước.
Khi đó, phục hồi bằng package đã xác minh và một giao dịch preview/cài mới.
Không thay cấu hình host và không xóa thư mục của attempt đang
chạy. Thư mục bị Windows từ chối truy cập cần được ghi nhận; không đổi ACL để dọn.

Đợt r46 dùng [công cụ dọn theo phạm vi](../plans/261010-1106-r46-publish-and-cleanup/tools/clean-old-copies.ps1)
và [bản ghi triển khai](../plans/reports/deploy-261010-1106-r46-publish-and-cleanup.md).
Công cụ mặc định chỉ chọn package build cũ, kiểm tra đường dẫn trong workspace
và từ chối link/junction. Phạm vi `rollback-payloads` cần quyền xóa bổ sung.
Các bản sao trong `references/_shared` thuộc closure của package đang dùng.

## Đường dẫn xuất bản

Test chỉ dành cho workspace nằm ở plan sở hữu nó, tránh thêm file ngoài inventory
được pin của kit. [Test đọc kit](../plans/261006-1433-nckh-kit-gemini-read-test/plan.md)
giữ bản nháp và lệnh chạy; việc chuyển vị trí không hoàn tất plan test này.

GitHub là nơi chia sẻ source và package; repository này không triển khai một
dịch vụ web. Đích được kiểm tra từ Git remote của checkout, đối chiếu với
`gh repo view` trước khi push. Quyền xuất bản gồm source, resources tham khảo,
kế hoạch và evidence đã rà soát; không gồm credentials hay cấu hình cá nhân.

Sau khi xuất bản, đối chiếu local HEAD với nhánh remote và chạy verifier từ
source/package công khai. Dọn repo không thay các gate trong
[release checklist](../nckh-kit/docs/release-checklist.md).

Nếu lịch sử local chưa push chứa raw evidence hoặc đường dẫn cá nhân, giữ các
commit đó dưới backup ref local. Tạo tree công khai từ remote parent đã xác minh,
chỉ đưa source/package, tài liệu sở hữu và summary đã rà soát vào index riêng.
Chạy [publication audit](../scripts/audit-publication.py) với index này, kiểm tra
cả bytes được stage rồi push bình thường. Giữ nguyên file local khi căn lại HEAD
và index; không force-push hoặc xóa file để che lịch sử riêng.

## Các phiên test được giữ nguyên

Đợt dọn này giữ nguyên các thư mục local
`plans/261006-2210-r41-agy-full-skill-test/`,
`plans/261006-2210-r41-shared-testcases/` và
`plans/261006-2210-r41-cursor-full-skill-test/`, cùng các attempt
`r41-agy-*` và `r41-cursor-*` trong `plans/runs/`. Các agent đang dùng chúng.
Đường dẫn tương thích `github-publication/` được giữ local trong thời gian test.

[Snapshot chia sẻ của ba plan](../plans/evidence/active-test-plans-261006-2300.zip)
được loại đường dẫn cá nhân và logs trước khi xuất bản; các file local của agent
không bị sửa. Snapshot này lưu thiết kế và testcase, không phải bằng chứng test
đã hoàn tất hoặc bản thay thế các pin của attempt đang chạy.

Kế hoạch dọn và kết quả theo lần chạy thuộc
[cleanup plan](../plans/261006-2300-repository-cleanup/plan.md).
