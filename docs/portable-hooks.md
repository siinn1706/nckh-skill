# Hook trong package

Mỗi package cho Claude, Codex, Cursor và Antigravity có thư mục `hooks/`, bao gồm
runner, codec của ứng dụng, template, manual checker và công cụ cấu hình.
Dependency và hash nằm trong manifest cùng source lock của package. Bản xuất
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

## Gợi ý routing và cảnh báo EOL/BOM

Hai lời nhắc này giải quyết hai lỗi đo được khi agent không tự nạp skill: chọn
sai hoặc không chọn skill nào, và đổi kiểu xuống dòng (CRLF/LF) hoặc BOM của file
đang sửa. Cả hai **chỉ có hiệu lực khi cài theo project có hooks** (mặc định
`--hooks advisory`). Cài global không đăng ký hook nên không có gợi ý hay cảnh báo.

Cả hai chỉ thêm lời nhắc vào context của agent. Chúng không bao giờ chặn thao
tác, không tự gọi skill, không sửa file và vẫn chạy khi thiếu controller context.
Mọi lỗi trong lúc tạo lời nhắc đều bị bỏ qua và không đổi quyết định của hook.

**Gợi ý routing.** Ở sự kiện prompt, hook so prompt với `vi_cues` trong
[route boundaries](../nckh-kit/core/registry/catalog/route-boundaries.json) rồi
gợi ý tối đa hai skill đã cài trong thư mục skill project của host, kèm quy tắc
phân vai giữa các skill dễ nhầm. Prompt đã gọi skill tường minh (`/nckh-…` hoặc
`$nckh-…`) không nhận gợi ý. Cú pháp gợi ý theo host: `/nckh-<skill>` cho Claude
và Cursor, `$nckh-<skill>` cho Codex.

Độ phủ là số đo cơ học, không phải hành vi của model. Trên tập held-out viết mù
lần thứ ba, 72,2 % prompt tự nhiên (65/90) nhận gợi ý đúng skill và 0 % prompt
không thuộc skill nào (0/10) nhận gợi ý. Nghĩa là khoảng 3/10 prompt tự nhiên
không nhận được gợi ý. Gọi tường minh `/nckh-<skill>` (Codex: `$nckh-<skill>`)
vẫn là đường chắc chắn. Ngưỡng hiện hành do test
`nckh-kit/tests/release/test_routing_prompts.py` sở hữu; bộ prompt nằm trong
`nckh-kit/evals/cases/routing/`.

Giới hạn đã biết: yêu cầu sửa câu chữ như "sửa lỗi chính tả" có
thể nhận gợi ý `nckh-fix`, vì matcher chỉ khớp cue mà không hiểu ý định
([route_hint.py](../nckh-kit/core/route_hint.py)).

**Cảnh báo EOL/BOM.** Trước khi một tool ghi file chạy, hook chụp snapshot
`{sha256, eol, bom, size}` của file đích đã tồn tại vào
`.nckh-state/hooks/snapshots/<host>/<session>/`. Sau khi tool chạy xong, hook so
lại, xoá snapshot và, nếu EOL hoặc BOM đã đổi, nhắc agent khôi phục trừ khi
người dùng yêu cầu đổi. Giới hạn hiện hành nằm trong
`nckh-kit/core/edit_guard.py`: file lớn hơn 16 MiB bị bỏ qua, mỗi session giữ tối
đa 128 snapshot, session cũ hơn 24 giờ bị dọn, lời nhắc nêu tối đa ba file. Chỉ
các tool ghi file mà codec khai trong `WRITE_TOOLS` được kiểm. File mới tạo, file
đi qua link và file do lệnh shell ghi không được kiểm.

| Host | Gợi ý routing | Cảnh báo EOL/BOM |
|---|---|---|
| Claude | `UserPromptSubmit` → `additionalContext` | `PreToolUse` chụp, `PostToolUse` → `additionalContext` |
| Codex | `UserPromptSubmit` → `additionalContext` | `apply_patch`: `PreToolUse` chụp, `PostToolUse` → `additionalContext` |
| Cursor | `beforeSubmitPrompt` không có kênh thêm context: gợi ý chỉ được ghi vào receipt với `delivered: false` | `preToolUse` chụp, `postToolUse` → `additional_context` |
| Antigravity | Không có sự kiện prompt: không gợi ý | `PostToolUse` không có kênh context: chỉ ghi receipt với `delivered: false` |

Bảng trên là hành vi của codec trong package. Việc host thật nhận và hiển thị lời
nhắc vẫn `unverified` cho tới khi có receipt native của đúng surface và phiên bản.

Receipt nằm dưới `.nckh-state/hooks/events/<host>/` và có trường `nudge`: tên
skill được gợi ý hoặc hash của đường dẫn bị đổi. Receipt không ghi nội dung prompt
hay đường dẫn thô. Lời nhắc mà wire của host không mang đi (Cursor
`beforeSubmitPrompt`, lệnh block của `enforce` ở `UserPromptSubmit`, cảnh báo
EOL/BOM trên AGY) được ghi với `delivered: false`. Để tắt cả hai lời nhắc, cài/cập nhật với `--hooks off` hoặc gỡ
hook bằng giao dịch remove ở phần dưới.

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
cần bằng chứng native trước khi kích hoạt. Khi thiếu hoặc hỏng context, `enforce`
chỉ fail-closed ở sự kiện host có thể chặn: `PreToolUse`/`preToolUse` và
`UserPromptSubmit`/`beforeSubmitPrompt`. `SessionStart`, `PostToolUse`, `Stop`,
`PreInvocation` và `PostInvocation` chỉ trả context advisory với exit 0.
Receipt `degraded-no-context` (ở cả advisory lẫn `enforce`) được gộp theo session
và mang tên `no-context-<64hex>.json`. Chỉ file đúng dạng này bị tính vào trần số
file; lần đầu chạm trần, runner ghi marker `cap-reached-no-context.json` và bỏ các
receipt thiếu context sau đó. Receipt đã kiểm (`checked-unreviewed`) và receipt
lỗi (`degraded-failed`, ghi riêng từng lần thử) không bao giờ bị giới hạn
(xem `record_once` trong [runner.py](../nckh-kit/hooks/runner.py)). Policy không suy ra toàn bộ đường dẫn và side effect của
một shell command từ `path` hoặc `file_path`. Event/tool chưa được hỗ trợ giữ
trạng thái manual/unverified. Có runner trong package chưa chứng minh host đã
đăng ký hook, thực thi deny đúng hoặc hoàn tất qualification. Bản công khai vẫn
là experimental; các gate native, scientific và human acceptance giữ nguyên.
