# Hook trong package r41

Mỗi package cho Claude, Codex, Cursor và Antigravity có thư mục `hooks/`, bao gồm
runner, codec của ứng dụng, template, manual checker và công cụ cấu hình.
Dependency và hash nằm trong manifest cùng source lock revision 41. Bản xuất
plugin giữ cùng closure tại `plugin/references/nckh-hooks/`.

Khi cài/cập nhật vào project, installer mặc định đăng ký hook ở chế độ
**advisory: nhắc/kiểm tra, không chặn thao tác**. Các lỗi policy, thiếu context
hoặc lỗi đọc dữ liệu vẫn được ghi nhận, nhưng không phát lệnh deny. Quyền thực
thi và trust của ứng dụng được giữ nguyên.

Thêm `--hooks off` để bỏ qua cấu hình hook. Với scope global, dùng `--hooks off`;
hook được quản lý theo từng project. Artifact trên GitHub giữ `packaged-inactive`
và `install_default: advisory`; trạng thái đã đăng ký chỉ được ghi sau khi cài.
Việc gỡ skill và gỡ hook là hai giao dịch ownership riêng. Dùng công cụ cấu hình
hook để preview/remove nếu muốn gỡ hook.

## Preview cấu hình

Ví dụ với package Codex, chạy từ repository:

```text
python -I packages/codex/hooks/configure-hooks.py preview --project PROJECT --host codex --package packages/codex --mode advisory --events PreToolUse PostToolUse --context CONTEXT --output PREVIEW.json
```

`PROJECT` là project đích. `CONTEXT` là đường dẫn JSON tương đối trong project,
do controller chọn, chứa task/operation mappings, grants và các tham chiếu
brief/source cần kiểm tra. `PREVIEW.json` là bản ghi riêng của project; giữ
bản ghi này ngoài repository công khai. Xem các thao tác `apply`, `remove`
và `recover` bằng `configure-hooks.py --help`.

| Ứng dụng | File cấu hình đích |
|---|---|
| Claude | `.claude/settings.local.json` |
| Codex | `.codex/hooks.json` |
| Cursor | `.cursor/hooks.json` |
| Antigravity | `.agents/hooks.json` |

Công cụ cấu hình kiểm tra preimage/hash, giữ entry không thuộc ownership và từ
chối xung đột hoặc thay đổi sau preview. Hook không gọi model/provider/network
và không thực thi command lấy từ event payload.

## Giới hạn kiểm tra

Shell tools được map trả về `pending/shell-targets-unverifiable`; advisory giữ
chẩn đoán này và không chặn lệnh. Chế độ `enforce` riêng vẫn từ chối pending và
cần bằng chứng native trước khi kích hoạt. Policy không suy ra toàn bộ đường dẫn và side effect của
một shell command từ `path` hoặc `file_path`. Event/tool chưa được hỗ trợ giữ
trạng thái manual/unverified. Có runner trong package chưa chứng minh host đã
đăng ký hook, thực thi deny đúng hoặc hoàn tất qualification. Bản công khai vẫn
là experimental; các gate native, scientific và human acceptance giữ nguyên.
