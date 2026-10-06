# R36 — Cursor interactive Read và năm native callbacks

[Verifier](../runs/nckh-native-261005-1225-r36-cursor-interactive-attempt-06/verify-interactive-delivery.py) exit 0; [structured bindings](./delivery-261005-1225-r36-cursor-interactive.json). Source r36/281 pins/hash `1a471686c5b1e89e6838957161a8ae4c6787d46d227420d8644636062da90d30` không đổi.

## Genuine turn và observed callbacks

Một prompt text write, rồi một separate Enter write, đã được native terminal nhận và hoàn tất một genuine turn trên Cursor CLI 2026.09.15-d2fe57e. Terminal hiển thị `Grok 4.7 500K Extra High · MAX` và `Run Everything`. Callback metadata báo `grok-4.7-xhigh` ở session/prompt/stop và `grok-4.7` ở tool stages; backend parameter attestation/billing không được quan sát.

| Native event | Actual observation |
|---|---|
| `sessionStart` | Genuine callback, policy advisory |
| `beforeSubmitPrompt` | Genuine callback sau separate Enter, policy advisory |
| `preToolUse` | Một `Read` đúng synthetic fixture; preflight allow |
| `postToolUse` | Cùng native tool-use ID/path; pre-delivery pending `artifact-final-bytes-missing-or-stale` |
| `stop` | Genuine callback sau tool; advisory, không thêm model turn |

Cả năm callbacks có cùng native session hash, actual version, runner exit 0, không fault injection. Fixture giữ exact preimage hash. Final `ORACLE_ATTEMPT_FINISHED` xuất hiện ở terminal render. Observer giữ metadata/hashes, không giữ exact tool-return content; không dùng ca này để claim exact Read return bytes.

Definition là instrumented native test: outer timeout 20s, packaged runner timeout 5s. Ca này xác minh callback route ở interactive terminal; production template timing, prompt/stop failure matrix và full native qualification vẫn pending. Một terminal chunk bị harness truncate do nhiều redraw frames; report giữ rõ giới hạn capture, không gọi nó là full raw terminal stream. [Attempt 05](../runs/nckh-native-261005-1141-r36-cursor-interactive-attempt-05/native-interactive-summary.json) vẫn là incomplete input evidence.

## Cleanup và retained state

Native Ctrl+C requests và graceful process stop chưa đóng cây tiến trình. Controller đối chiếu PID/creation identity trước force-stop đúng owned tree; harness recorded exit 1, không phải clean native exit 0. Final process audit zero matches, gồm chín recorded PIDs. Cleanup gỡ 26 matching config/payload members và giữ 386 historical project members. Protected global hashes unchanged; global CLI before/after hashes được giữ trong cleanup receipt. Không sửa source/global config trực tiếp, không gọi công cụ Illustrator dù native CLI khởi tạo MCP server đã cấu hình.

Plan remains in-progress 44/45, P3 native task unchecked; accepted r29 VI/EN samples và installed r25 giữ trạng thái riêng.
