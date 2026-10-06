# Tài liệu workspace NCKH

Trang này dành cho người dùng và agent cần tìm đúng tài liệu, nguồn contract và
bằng chứng của bộ skill NCKH. Tài liệu chuyên môn của package nằm trong
[chỉ mục NCKH](../nckh-kit/docs/index.md).

## Bắt đầu theo mục đích

| Mục đích | Tài liệu sở hữu |
|---|---|
| Giữ, xuất bản và dọn nội dung workspace | [Repository maintenance](repository-maintenance.md) |
| Dùng skill và phản hồi đầu ra | [Personal use](../nckh-kit/docs/personal-use.md) |
| Nghiên cứu, viết, dịch và hình khoa học | [Research and writing](../nckh-kit/docs/research-and-writing.md) |
| Làm việc với phần mềm | [Engineer](../nckh-kit/docs/engineer.md) |
| Nghiên cứu và soạn nội dung marketing | [Marketing](../nckh-kit/docs/marketing.md) |
| Tìm ranh giới contract, nguồn và quyền sử dụng | [Contracts](../nckh-kit/docs/contracts.md) |
| Đóng gói, cài đặt, phục hồi và cấu hình hooks | [Installation](../nckh-kit/docs/installation.md) |
| Phân biệt projection với hành vi host đã quan sát | [Runtime support](../nckh-kit/docs/runtime-support.md) |
| Đánh giá đầu ra và phạm vi qualification | [Qualification](../nckh-kit/docs/qualification.md) |
| Chuyển phiên bản và bảo toàn nội dung đã sửa | [Migration](../nckh-kit/docs/migration.md) |
| Xem điều kiện phát hành | [Release gates](../nckh-kit/docs/release-checklist.md) |

## Quyết định thiết kế

Bộ kit tách tìm nguồn, kiểm chứng, phương pháp, viết và phê bình để mỗi công việc
có trách nhiệm và bằng chứng riêng. [Blueprint ban đầu](../vietnamese-writing-research-skills-blueprint.md)
giữ lý do thiết kế; khi cần biết contract đang có, đọc tài liệu package và owner
bên dưới.

Polish/dịch và xây dựng lập luận từ evidence là hai nhiệm vụ riêng. Quyết định
phân vai, ngôn ngữ và giới hạn hình khoa học thuộc
[research-and-writing](../nckh-kit/docs/research-and-writing.md).
Quyền của resource thuộc [contracts](../nckh-kit/docs/contracts.md), còn feedback
cá nhân thuộc [personal-use](../nckh-kit/docs/personal-use.md).

## Nguồn sở hữu contract

Các liên kết này dùng để tra cứu trực tiếp, tránh duy trì thêm danh sách identity,
resource, revision hoặc bản sao cấu hình trong tài liệu workspace.

| Cần tra cứu | Owner |
|---|---|
| Identity, vị trí skill và dependency | [Skill catalog](../nckh-kit/core/registry/catalog/skills.json) |
| Resource, consumer và provenance | [Resource registry](../nckh-kit/core/registry/catalog/resources.json) |
| Revision và bytes được pin | [Source lock](../nckh-kit/core/registry/source-lock/source-lock.json) |
| Schema dữ liệu | [Contracts](../nckh-kit/core/contracts/) |
| Profile và policy dùng chung | [Core profiles](../nckh-kit/core/profiles/), [core policies](../nckh-kit/core/policies/) |
| Projection theo host | [Adapters](../nckh-kit/adapters/) |
| Đóng gói | [Build entrypoint](../nckh-kit/scripts/build-artifacts.py) |
| Giao dịch cài đặt | [Installer entrypoint](../nckh-kit/installer/nckh-installer.py) |
| Đọc resource | [Resource reader](../nckh-kit/scripts/search-resource.py) |
| Policy và giao dịch hooks | [Hook policy](../nckh-kit/core/hook_policy.py), [configuration entrypoint](../nckh-kit/scripts/configure-hooks.py) |
| Protocol và kết quả kiểm chứng | [Evaluation protocols](../nckh-kit/evals/protocols/), [evaluation entrypoint](../nckh-kit/evals/run-evals.py) |

## Kế hoạch và bằng chứng theo lần chạy

Lịch sử cập nhật trên máy được tóm tắt tại
[NCKH r41 cho các agent](../plans/reports/install-261006-2154-nckh-r41-all-agents.md).
State ownership hiện tại được giữ local; biên nhận cài đặt riêng và logs cũ không
thuộc bản công khai.

[Plans](../plans/) giữ mục tiêu, quyền thực thi, tiến độ và các gate của từng công
việc. [Reports](../plans/reports/) giữ review và checkpoint;
[runs](../plans/runs/) giữ hồ sơ từng attempt. Đọc plan liên quan rồi theo các
liên kết evidence của chính plan đó.

Đối chiếu revision, input và artifact hashes trước khi dùng một kết quả cũ cho
candidate đang đọc. Kiểm tra cấu trúc hoặc tính toàn vẹn không tự xác nhận hành vi
native, chất lượng viết hay tính đúng đắn khoa học. Phạm vi đánh giá và điều kiện
chấp nhận được sở hữu bởi [qualification](../nckh-kit/docs/qualification.md) và
[release gates](../nckh-kit/docs/release-checklist.md).

Trang này chỉ sở hữu đường dẫn tài liệu của workspace. Khi cập nhật, sửa nội dung
ở tài liệu hoặc executable owner tương ứng; chỉ thay liên kết ở đây nếu route đổi.
