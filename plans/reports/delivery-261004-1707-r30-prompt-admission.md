# NCKH r30 — bổ sung native prompt admission

Trạng thái: **owner VI/EN accepted; technical checks giữ nguyên; Codex UserPromptSubmit có callback thực; plan 44/45**.

Bổ sung cho [checkpoint r30 trước đó](delivery-261004-1707-r30-native-checkpoint.md). [Structured evidence](delivery-261004-1707-r30-prompt-admission.json) bind source-lock và từng receipt thực. Source, writer instructions, tests và archives không đổi trong continuation này; không chạy lại full suite/build.

## Quyền và phạm vi

[Native grant](../runs/nckh-native-261004-1707-attempt-01/native-grant.json) và [owner feedback](../runs/nckh-native-261004-1707-attempt-01/owner-feedback.json) giữ nguyên. Người dùng đã cho phép registration/trust/enable/cleanup trong project thử riêng và chấp nhận đúng hai mẫu VI/EN. Provider scope/budget vẫn cần câu trả lời riêng trước các lượt inference thực.

Probe chỉ dùng project Codex thử đã có quyền. Provider được override theo invocation tới `http://127.0.0.1:9/v1`, không có server/response/key giả. HTTP(S)/ALL proxy cũng trỏ loopback bị từ chối; credentials environment được bỏ khỏi child. Các thiết lập runtime này không ghi vào config người dùng.

## Quan sát thực

| Host/surface/version/event | Kết quả | Bằng chứng |
|---|---|---|
| Claude Code 2.1.272 / CLI / UserPromptSubmit | Hai cases `--max-budget-usd 0` exit 1 tại CLI argument validation, 0 callbacks | [Zero-budget attempt](../runs/nckh-native-261004-1707-attempt-01/native-prompt-admission-zero-budget.json) |
| Codex CLI 0.154.0 / UserPromptSubmit / policy block | Packaged r30 runner được native host gọi; một deterministic receipt `block / bounded-input-exceeded`; `hook/completed` có `status=blocked`; `turn/completed` có `status=completed`, `items=[]` | [Block observation](../runs/nckh-native-261004-1707-attempt-01/projects/codex/prompt-admission-observe-attempt-01.json) |
| Codex CLI 0.154.0 / UserPromptSubmit / advisory | Cùng trusted definition gọi runner; một receipt mới `advisory / writing-resource-advice-only`; hook hoàn tất với context. Sau đó host báo `Connection failed` và `willRetry=true`; chưa có `turn/completed` khi kết thúc cửa sổ quan sát 8 giây rồi đóng owned app-server | [Advisory observation](../runs/nckh-native-261004-1707-attempt-01/projects/codex/prompt-admission-observe-allow-attempt-01.json) |

Kết quả chặn xác nhận prompt admission ở đúng event trên phiên native này. Chưa có tool invocation hoặc tool side-effect prevention oracle. Nhánh advisory không có model success; connection refusal không phải native enforcement PASS. Deterministic policy receipts vẫn giữ `native_enforcement=unverified`; host observations được ghi riêng, không sửa receipt để nâng evidence class.

## Trust, isolation và cleanup

Definition native: `sha256:3e7a2b1e996f1a2d7dc937ad7a1cff0616934538d428eaa204f0e88692be40b2`.

- [Trước review](../runs/nckh-native-261004-1707-attempt-01/projects/codex/prompt-admission-metadata-attempt-02.json): hook mới, enabled, untrusted. [Normal UI](../runs/nckh-native-261004-1707-attempt-01/projects/codex/prompt-admission-ui-trust.json) chọn riêng Hook 6 thuộc project config và trust đúng definition. [Sau review](../runs/nckh-native-261004-1707-attempt-01/projects/codex/prompt-admission-metadata-attempt-03.json): trusted/enabled. Không dùng trust-all.
- Native metadata xác nhận 27 user-config hooks disabled và ba MCP servers trong config disabled theo invocation. Host vẫn phát startup notification `cua_repl=ready`; không gọi công cụ này. Không mô tả isolation là tắt mọi builtin/plugin capability.
- [Normal UI cleanup](../runs/nckh-native-261004-1707-attempt-01/projects/codex/prompt-admission-ui-disable.json) tắt riêng project Hook 6. [Native check](../runs/nckh-native-261004-1707-attempt-01/projects/codex/prompt-admission-metadata-attempt-04.json) xác nhận đúng hash trusted/disabled.
- [Matching cleanup](../runs/nckh-native-261004-1707-attempt-01/projects/codex/prompt-admission-cleanup.json) gỡ một owned config và 26 matching payload members, bảo toàn context/preimage/receipts. Unrelated user-hook state hash không đổi. [Sau cleanup](../runs/nckh-native-261004-1707-attempt-01/projects/codex/prompt-admission-metadata-attempt-05.json) không còn project hooks callable.
- Tổng cộng ba project-test definition hashes còn trusted nhưng disabled trong native store, gồm hai hashes lịch sử và hash mới. Project trust có thể còn lưu. Không sửa trực tiếp global trust store để xóa lịch sử.
- [Process audit](../runs/nckh-native-261004-1707-attempt-01/process-audit-prompt-admission.json) không thấy process có command line thuộc run còn sống; owned process receipts đều kết thúc. Không dừng user processes.

## Lỗi helper và giới hạn

Lượt TUI đầu exit 1 với `invalid transport` tại MCP name bị bọc quotes trong dotted CLI override. Đổi helper sang bare MCP names đã kiểm và whole `hooks.state` TOML value; metadata xác minh isolation trước turn. Metadata attempt 01 trong sandbox exit 1 với `Access is denied`; retry native có quyền đọc/ghi runtime state kết thúc bình thường. Hai lỗi startup này không được tính là hook failure. Không đổi source kit để sửa helper.

Helper cũ chưa gửi `initialized` notification sau `initialize`; probe mới gửi đúng handshake theo [official app-server protocol](https://developers.openai.com/siwc/token-sharing-open-source/codex-app-server). Đây là khác biệt harness được ghi nhận; chưa đủ bằng chứng để quy nguyên nhân các callback vắng mặt ở route lịch sử cho handshake. Cách diễn giải CLI override đối chiếu [official Codex source](https://github.com/openai/codex/blob/main/codex-rs/utils/cli/src/config_override.rs).

## Gate còn mở

[Plan](../261004-0047-nckh-research-data-hooks-writing/plan.md) giữ `in-progress`, 44/45. Full native failure matrix gồm malformed input/output, timeout/crash, unsupported event/tool, duplicate project/plugin và prevention ở PreToolUse vẫn chưa hoàn tất cho các enabled event/surface. Cursor CLI cần authentication; AGY cần eligibility/kết nối thật; Desktop/IDE tracks chưa có live event evidence. Các targets giữ pending/unverified, không đổi thành unsupported hoặc bốn-host parity.

Để chạy tiếp phần cần inference, cần host được phép dùng, account sẵn sàng và scope/budget. Installed r25, public release, scientific/stable qualification và quyền dùng holdout/reviewer vẫn theo gate riêng. Hai mẫu VI/EN đã accepted, không yêu cầu người dùng duyệt lại.
