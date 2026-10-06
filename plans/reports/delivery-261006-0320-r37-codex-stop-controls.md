# Codex r37 — native Stop sau canonical patch

**Trạng thái:** verified trong phạm vi bên dưới; plan **44/45, P3 active, full native gate unchecked**.

## Phạm vi và oracle

[Frozen brief](../runs/nckh-native-261006-0320-r37-codex-stop-controls-attempt-48/frozen-brief.json) giữ bảy lượt **Codex CLI 0.154.0 / exec / GPT-5.6 Luna / medium**: mỗi lượt yêu cầu một `apply_patch` add-file, không retry hoặc tool thay thế. Source **r37 / 281 pins**, lock hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` không đổi. Dùng project thử đã trusted và hook definitions riêng invocation theo quyền native hiện có.

[Verification](../runs/nckh-native-261006-0320-r37-codex-stop-controls-attempt-48/verified-stop-observations.json) xác nhận **7 lượt / 7 patches / 35 callbacks / 32 receipts**. Mỗi lượt có đúng một cặp PreToolUse/PostToolUse cùng tool-use ID, turn/session và patch hash; một `file_change` hoàn tất; marker bytes LF đúng. Marker chưa tồn tại ở PreToolUse, đã tồn tại với hash đúng ở PostToolUse và Stop.

Stop thực sự có `last_assistant_message` và `stop_hook_active`. Observer chỉ giữ độ dài và hash của message, không đọc transcript. Cả bảy message dài 23 bytes, hash khớp final `agent_message`; `stop_hook_active=false`. Mỗi lượt có một callback Stop. Chưa có callback Stop lặp để xác nhận hành vi nhắc lại.

## Kết quả chọn tại Stop

| Ca | Policy hoặc observer | Wire / mutation |
|---|---|---|
| allow | advisory / `writing-resource-advice-only` | `{}`; patch đã hoàn tất |
| policy-deny | block / `bounded-input-exceeded` | `{}`; patch đã hoàn tất |
| malformed-input | degraded block / `hook-input-or-context-invalid` | `{}`, runner exit0; patch đã hoàn tất |
| malformed-output | cố ý trả JSON lỗi; không selected receipt | final turn và patch hoàn tất |
| timeout | outer5s, sleeper8s; final snapshot giữ trạng thái sleep, không selected receipt | final turn và patch hoàn tất |
| crash | observer cố ý exit17; không selected receipt | final turn và patch hoàn tất |
| unsupported-codec | degraded block / `hook-input-or-context-invalid` | `{}`, runner exit3; patch đã hoàn tất |

Policy-deny dùng **33 reference records rỗng do controller sở hữu** để thử giới hạn số lượng; không phải nguồn nghiên cứu. Năm faults được controller chèn sau callback native thật. Unsupported selector là phép thử codec sau Stop thật; chưa chứng minh host giao một event không biết. Raw context trước từng lượt được giữ trong `context-preimages/`; normal receipt hash đối chiếu trực tiếp với các bytes đó.

Current Stop codec trả `{}` cho cả advisory và block. Kết quả quan sát chưa chứng minh host enforce block tại Stop, ngăn mutation, rollback hoặc scientific QA. Output `exec --json` giữ completed file/turn items, không công bố hook notification states; không suy diễn native `failed/blocked/timeout` từ receipt hoặc observer status.

## Kết thúc và giới hạn

Controller terminal (historical evidence path: `../runs/nckh-native-261006-0320-r37-codex-stop-controls-attempt-48/controller-terminal.json`; unavailable in the cleaned checkout) và bảy native invocations exit0. [Cleanup](../runs/nckh-native-261006-0320-r37-codex-stop-controls-attempt-48/cleanup.json) gỡ **26** matching payload members, giữ nguyên **655** historical project files và giữ marker/observations/receipts. Protected global config/hooks hashes không đổi; zero new trust keys, không cài plugin hoặc direct-write global.

[Final audit](../runs/nckh-native-261006-0320-r37-codex-stop-controls-attempt-48/process-final-audit.json) đối chiếu **2.310 PID/creation identities**, zero matching/tracked-live; không dừng tiến trình. Terminal handle42269 đã kết thúc, không poll/restart. Verification đạt ở lần chạy đầu; review inline. Các test local r37 và archive evidence được tái sử dụng theo binding chưa đổi, không chạy lại thành native proof.

[PostToolUse47](./delivery-261006-0253-r37-codex-posttool-controls.md) và historical r34 shell/2s Stop observations giữ nguyên revision/tool/timing riêng. Codex project/plugin cache authority và Claude model/effort vẫn chờ câu trả lời trực tiếp; Cursor/AGY gaps, unknown-host-event và IDE/Desktop qualification còn mở. Hai mẫu VI/EN đã chấp nhận vẫn được giữ.
