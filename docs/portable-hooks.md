# Hook trong package r37

Mỗi package cho Claude, Codex, Cursor và Antigravity có thư mục `hooks/`, bao gồm
runner, codec của ứng dụng, template, manual checker và công cụ cấu hình.
Dependency và hash nằm trong manifest cùng source lock revision 37. Bản xuất
plugin giữ cùng closure tại `plugin/references/nckh-hooks/`.

Hook mặc định có trạng thái `packaged-inactive`; `enabled`, `registered` và
`trusted` đều là `false`. Upload lên GitHub không bật hook trong ứng dụng.

## Preview cấu hình

Ví dụ với package Codex, chạy từ repository:

```text
python -I packages/codex/hooks/configure-hooks.py preview --project PROJECT --host codex --package packages/codex --events PreToolUse --context CONTEXT --output PREVIEW.json
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

Shell tools được map trả về `pending/shell-targets-unverifiable`; native pre-tool
codec từ chối pending. Policy không suy ra toàn bộ đường dẫn và side effect của
một shell command từ `path` hoặc `file_path`. Event/tool chưa được hỗ trợ giữ
trạng thái manual/unverified. Có runner trong package chưa chứng minh host đã
đăng ký hook, thực thi deny đúng hoặc hoàn tất qualification. Bản công khai vẫn
là experimental; các gate native, scientific và human acceptance giữ nguyên.
