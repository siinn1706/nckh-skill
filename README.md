# nckh-skill

Bộ **37 skill NCKH** cho nghiên cứu, viết, kỹ thuật và marketing, kèm sáu vai trò
agent tùy chọn. Hướng dẫn của skill bằng tiếng Anh; đầu ra theo ngôn ngữ được yêu
cầu trong công việc.

| Nhóm | Số skill |
|---|---:|
| Core | 10 |
| Engineer | 13 |
| Marketing | 13 |
| Xia | 1 |

## Phạm vi bản công khai

Repository này chứa các package **experimental r25**, được xuất ở chế độ
**`resource-access off`**. Bản công khai giữ đủ skill, hợp đồng dùng nguồn, reader
và công cụ cài đặt; người dùng cung cấp tài liệu hoặc dữ liệu đầu vào của mình.
Các mẫu văn bản, bài báo và dữ liệu sao chép đi kèm bản dùng cá nhân được giữ
ngoài bản công khai vì quyền tái phân phối chưa được chốt đầy đủ.

Mỗi package có manifest và source lock để kiểm tra đúng phiên bản và tính toàn
vẹn. Các trường quyền và qualification trong bản ghi gốc được giữ nguyên;
repository này là bản chia sẻ instructions và công cụ, chưa phải bản stable đã
được kiểm định đầy đủ. Xem [phạm vi và quyền](docs/public-edition.md).

## Cấu trúc

- `packages/claude/`: package cho Claude Code.
- `packages/codex/`: package cho Codex CLI, desktop và IDE.
- `packages/cursor/`: package cho Cursor CLI và IDE.
- `packages/agy/`: package cho Antigravity CLI và IDE.
- `nckh-kit/installer/`: công cụ preview, cài, cập nhật, doctor và gỡ theo ownership.
- `nckh-kit/scripts/verify-public-package.py`: kiểm tra package trước khi dùng.

Mỗi package chứa 37 thư mục skill và sáu agent tùy chọn. Các adapter là cấu hình
được đóng gói; việc có package chưa xác nhận mọi phiên bản ứng dụng và hệ điều
hành đã được kiểm tra thực tế.

## Kiểm tra và cài đặt

Đọc instructions trực tiếp không cần Python. Công cụ kiểm tra và cài đặt cần
**Python 3.11 trở lên**, dùng thư viện chuẩn.

Chạy từ thư mục repository:

```text
python nckh-kit/scripts/verify-public-package.py
python nckh-kit/installer/nckh-installer.py list-skills
```

Ví dụ preview cài đủ ba nhóm vào một project dùng Codex desktop:

```text
python nckh-kit/installer/nckh-installer.py install --package packages --runtime codex-desktop --scope project --project PATH_TO_PROJECT --kits core engineer marketing --mode copy --models balanced --dry-run
```

Thay `PATH_TO_PROJECT` bằng đường dẫn project thực. Đọc preview, giải quyết các
xung đột nếu có, rồi chạy lại cùng lựa chọn, thay `--dry-run` bằng `--yes` để cài.

| Ứng dụng | Giá trị `--runtime` |
|---|---|
| Claude Code | `claude-code` |
| Codex desktop | `codex-desktop` |
| Codex CLI | `codex-cli` |
| Codex IDE | `codex-ide` |
| Cursor IDE | `cursor-ide` |
| Cursor CLI | `cursor-cli` |
| Antigravity IDE | `agy-ide` |
| Antigravity CLI | `agy-cli` |

Thêm `--with-agents` nếu muốn cài sáu agent tùy chọn. Model mặc định kế thừa cấu
hình của ứng dụng; profile `balanced` tự nó không xác nhận model hay effort thực
sự được áp dụng. Cài đặt không gọi model hoặc tự bật hooks/plugin.

Sau khi cài, dùng state directory của project để kiểm tra và preview gỡ:

```text
python nckh-kit/installer/nckh-installer.py doctor --state-dir PATH_TO_PROJECT/.nckh-state
python nckh-kit/installer/nckh-installer.py uninstall --state-dir PATH_TO_PROJECT/.nckh-state --install-id INSTALL_ID --dry-run
```

Lấy `INSTALL_ID` từ biên nhận cài đặt. Update có kiểm tra candidate evidence riêng;
`--yes` không bỏ qua ownership, file đã chỉnh sửa hoặc các điều kiện cập nhật.

## Dùng skill

Chọn `nckh-*` phù hợp, nêu đầu ra cần có, cung cấp tài liệu hoặc dữ liệu, ngôn ngữ
và giới hạn công việc. Với bản công khai này, giữ resource access ở chế độ **off**;
khi gọi reader lookup, truyền `--resource-access off`. Reader sẽ ghi nhận tài
nguyên đi kèm bị tắt. Các URL và hash trong registry là thông tin nguồn gốc,
không có nghĩa dữ liệu mẫu đã được phân phối trong repository.

Biểu đồ, sơ đồ và ảnh cần công cụ tạo/render tương ứng của môi trường. Skill
không tự cung cấp dịch vụ tạo ảnh hoặc chứng nhận file chỉnh sửa được.
