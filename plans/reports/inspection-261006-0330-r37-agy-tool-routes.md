# AGY CLI: help và danh mục agent hiện tại

[Bindings](../runs/nckh-native-261006-0330-r37-agy-tool-route-inspection-attempt-46/verified-cli-inspection.json) ghi bốn lệnh chỉ đọc từ AGY CLI **1.2.17** trong project thử đã được cấp quyền: version, help, agent help và agent inventory. Cả bốn đều exit0; không gửi prompt model, yêu cầu tool, bật hook hoặc cài plugin.

## Những gì đã quan sát

| Surface | Kết quả |
|---|---|
| Main help | Có `--agent` cho phiên CLI và hai subcommand `agent`/`agents` |
| Main help stream | Nội dung help ở stderr; stdout rỗng, process exit0 |
| Agent help | `agent [flags]`, mục đích liệt kê agent; chỉ có hai flags help |
| Agent inventory | 16 tên riêng biệt, gồm Explore, fullstack-developer, researcher, planner và tester |
| Agent/tool mapping | Không được cung cấp trong help và inventory đã quan sát |

Danh mục native xác nhận có thể chỉ định tên agent đã đăng ký. Ca này không mở phiên agent nên effective selected agent và callable toolset vẫn chưa được xác lập. Các tên tool trong init frame của search35 từng khác với khả năng dispatch thực tế; danh mục agent không giải quyết được khoảng trống đó.

Giữ các failed oracles search35: private find_by_name có actual request rồi dispatcher trả unknown-tool; ba search outcomes khác không có native tool request. Không đổi chúng thành pass hoặc suy ra private-path enforcement từ danh mục mới. Chưa có causal evidence để lặp lại cùng search prompt.

## Tiến trình và phạm vi

[Audit cuối](../runs/nckh-native-261006-0330-r37-agy-tool-route-inspection-attempt-46/process-final-audit.json) kiểm union2018 PID/creation identities: zero matching/tracked-live, không dừng process. Hash settings và global hooks được bảo vệ giữ nguyên; project vẫn không có hook config. Helper ghi command, PID, thời điểm tạo, descendants và hash stdout/stderr của từng lệnh.

Controller được bổ sung action inventory sau khi đọc help thật; hash bản ban đầu và bản thích ứng đều lưu trong bindings. Source kit r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` giữ nguyên. Kiểm source-lock lần này là identity check, không phải chạy lại toàn bộ integrity hoặc native qualification. Review inline; không có independent reviewer.

AGY/Gemini3.8FlashMedium/dangerous và Cursor/Grok4.7/500k/xhigh/fast=false/dangerous tiếp tục là các tuyến đã được người dùng chọn. Không có lượt model mới trong inspection này. Full native task giữ **unchecked / 44 of45 / P3 active**; các ô tool/fault, Codex cache authority, Claude selection và direct IDE qualification vẫn mở.
