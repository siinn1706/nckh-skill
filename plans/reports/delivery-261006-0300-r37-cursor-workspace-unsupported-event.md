# Cursor CLI: sự kiện thật chưa được kit codec hỗ trợ

[Bindings đã kiểm tra](../runs/nckh-native-261006-0300-r37-cursor-workspace-unsupported-event-attempt-45/verified-unsupported-event-observations.json) ghi một phiên khởi động Cursor CLI **2026.09.15-d2fe57e**, dùng lựa chọn Grok4.7/500k/xhigh/fast=false hiện có và quyền dangerous đã cấp. Controller không gửi prompt model hoặc yêu cầu tool. [Brief chốt trước khi chạy](../runs/nckh-native-261006-0300-r37-cursor-workspace-unsupported-event-attempt-45/frozen-brief.json) có cửa sổ quan sát khởi động 15 giây, sau đó thoát bằng `/exit`.

## Quan sát native

| Callback | Số lượt | Kết quả |
|---|---:|---|
| workspaceOpen → packaged runner | 1 | Nguyên dữ liệu native, selector workspaceOpen, stdout `{}`, exit3 |
| workspaceOpen → route diagnostic | 1 | Cùng input hash, trả một đường dẫn plugin thuộc project thử |
| sessionStart của project | 1 | Runner exit0 |
| sessionStart của plugin | 1 | Cùng input và session với project, runner exit0 |

`workspaceOpen` là sự kiện host thực sự phát, nhưng nằm ngoài năm sự kiện mà codec Cursor r37 hỗ trợ. Observer chuyển nguyên bytes vào runner bằng `--event workspaceOpen`; `fault_origin=none`, không thay selector sau một callback được hỗ trợ và không tạo native input giả.

Receipt lỗi có `decision=block`, `status=degraded-failed`, reason duy nhất `hook-input-or-context-invalid`; `event_hash` khớp SHA256 của input native. Receipt này không có decoded phase/context/session/task. Giữ đúng reason của runner, không đặt thêm reason cho unsupported event.

Hai callback sessionStart bắt đầu sau khi runner của workspaceOpen đã hoàn tất với exit3. Cursor tiếp tục đến màn hình sẵn sàng; lifecycle pair tạo một receipt idempotent riêng. Tổng cộng bốn callbacks, ba lượt runner và hai receipts. Cả 17 điều kiện của oracle đã chốt đều khớp quan sát.

## Phạm vi của kết quả

Kết quả xác minh phản ứng với **sự kiện host đã biết nhưng kit codec chưa hỗ trợ** và việc phiên khởi động vẫn tiếp tục. Admission/delivery cho tên sự kiện host không biết vẫn chưa được kiểm chứng. Không có model/tool mutation trong ca này, nên không có bằng chứng ngăn ghi tệp hoặc qualification enforcement mặc định. Outer và inner timeout5s là cấu hình phép thử.

Route diagnostic là handler do controller sở hữu để trả `pluginPaths`; nó không phải codec sự kiện của kit. Plugin được nạp qua kết quả workspaceOpen, không qua `--plugin-dir`. Các failed oracles native19/21/44 và các ô prompt/stop/plugin còn thiếu giữ nguyên.

## Kết thúc và trạng thái

Native CLI và monitor đều exit0. [Cleanup](../runs/nckh-native-261006-0300-r37-cursor-workspace-unsupported-event-attempt-45/cleanup.json) gỡ33 tệp owned còn khớp hash, giữ891 tệp lịch sử, bốn observations và hai receipts. [Audit cuối](../runs/nckh-native-261006-0300-r37-cursor-workspace-unsupported-event-attempt-45/process-final-audit.json) kiểm union2008 PID/creation identities, zero matching/tracked-live; không dừng process bằng tín hiệu. Các hash global hook/MCP/plugin được bảo vệ giữ nguyên; CLI-owned state chỉ ghi hash trước/sau, không suy đoán fields đổi. Controller global direct writes=false.

Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` giữ nguyên. Chuẩn bị biên dịch20 tệp Python trong bộ nhớ và kiểm hash payload; các kiểm này chỉ là integrity evidence. Review inline, không có independent reviewer. Full native task vẫn **unchecked / 44 of45 / P3 active**; quyền cache Codex, Claude model/effort, các ô host/tool/fault và IDE còn mở.
