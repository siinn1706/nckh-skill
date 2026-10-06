# Phạm vi phép thử Codex project/plugin

**Trạng thái:** đã chuẩn bị, chưa đăng ký hoặc cài plugin, chưa gửi lượt model. Plan vẫn **44/45, P3 active, native gate unchecked**.

## Mục đích và bản đã kiểm tra

Kiểm tra Codex CLI 0.154.0 có thực sự gọi cả hook project và hook plugin cho cùng sự kiện, và policy chỉ ghi một receipt khi hai callback trùng nhau. Đây là phép thử cho một ô bằng chứng còn thiếu của P3.

[Bản chuẩn bị](../runs/nckh-native-261006-0135-r37-codex-plugin-routing-attempt-41/plugin-proposal.json) có 33 tệp, tree hash `6e6e7e3618decdec995524c42a63e8f24235bd6753e7387be77ffdcae4e2f65b`. [Kết quả kiểm tra](../runs/nckh-native-261006-0135-r37-codex-plugin-routing-attempt-41/verified-plugin-proposal.json) xác nhận 26 tệp hook khớp gói r37, 18 tệp Python biên dịch trong bộ nhớ, JSON/TOML và 10 chuỗi lệnh có đối số Windows đúng. Các kiểm tra này chỉ xác nhận bản chuẩn bị.

## Quyền cần thêm

Phần **Remaining acceptance và rollback** trong [plan](../261004-0047-nckh-research-data-hooks-writing/plan.md) giữ quyền cài ngoài workspace thành gate riêng. Quyền native hiện có cho phép project thử dùng một lần; tuyến plugin của Codex còn tạo cache trong hồ sơ người dùng. [Tài liệu chính thức](https://developers.openai.com/plugins/build/plugins) mô tả cache plugin local dưới `~/.codex/plugins/cache/<marketplace>/<plugin>/local/`.

| Thành phần | Phạm vi đề nghị |
|---|---|
| Plugin | `nckh-native-hook-probe@nckh-native-project-plugins` |
| Cache | `C:/Users/USER\.codex\plugins\cache\nckh-native-project-plugins\nckh-native-hook-probe\` — chưa tồn tại ở thời điểm kiểm tra |
| Metadata | Chỉ metadata cài/gỡ do Codex quản lý gắn với identity plugin thử trên; ghi nhận chênh lệch trước/sau |
| Project đã trusted | `C:/Users/USER\Downloads\test-skill\plans\runs\nckh-native-261005-0658-r34-codex-file-attempt-01\project-02` |
| Model | GPT-5.6 Luna, medium; tối đa một lượt và một yêu cầu `apply_patch` |
| Sự kiện | SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop |
| Dọn | Native uninstall đúng identity; gỡ các tệp project còn khớp hash đã ghi; đối chiếu cache, metadata và tiến trình |

Quyền đề nghị bao gồm tạo/gỡ cache thử và metadata native liên quan. Cấu hình bật plugin nằm trong project thử. Hook dùng bypass trust cho invocation theo quyền native đã có; project trust hiện có được tái sử dụng. Controller chỉ ghi tệp trong workspace.

## Điều kiện trước lượt model

1. Đối chiếu lại toàn bộ hash bản chuẩn bị và các đích đang absent; bảo toàn tệp lịch sử của project.
2. Chụp hash và cấu trúc metadata native cần đối chiếu, giữ nội dung nhạy cảm ngoài báo cáo.
3. Dùng tuyến cài native đã cấp quyền. Native `hooks/list` phải báo đúng nguồn **project** và **plugin**, pluginId, currentHash và timeout cho năm sự kiện.
4. Xác minh callback lifecycle thật từ plugin và project. Việc Codex Windows mở rộng `${PLUGIN_ROOT}` hiện còn **unverified**; roundtrip đối số không chứng minh host thực thi chuỗi lệnh này. Thiếu callback thì giữ failure và dừng trước model.
5. Khi các điều kiện trên đạt, chạy đúng một lượt GPT-5.6 Luna/medium với một patch vào marker công khai của project thử.

## Oracle và kết thúc

Mỗi sự kiện phải có cặp project/plugin với cùng input hash và native session/tool identity, một policy receipt idempotent, một patch thực thi và marker có bytes đúng. Thiếu dữ liệu hoặc khác kết quả dự kiến được giữ thành unqualified/failed observation; exit0 không tự tạo kết quả pass.

Help gỡ plugin của CLI đang cài (historical evidence path: `../runs/nckh-native-261006-0135-r37-codex-plugin-routing-attempt-41/commands/plugin-remove-help.stdout.txt`; unavailable in the cleaned checkout) nêu hỗ trợ gỡ plugin và xóa cache local. Sau phép thử phải quan sát kết quả gỡ thực tế; cache hoặc metadata còn lưu được báo rõ. Nếu native cleanup thất bại hoặc phát hiện chỉnh sửa ngoài phạm vi, giữ evidence và giải quyết quyền cho phần đó trước khi ghi trực tiếp ngoài workspace.

Source r37/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` và các mẫu VI/EN đã được chủ sở hữu chấp nhận vẫn là baseline. Phép thử này chỉ bổ sung bằng chứng project/plugin của Codex; các ô native khác và qualification IDE còn mở.
