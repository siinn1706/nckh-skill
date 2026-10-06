# R36 — Cursor prompt/stop fault observations

Verified bindings (historical evidence path: `./delivery-261005-1257-r36-cursor-prompt-stop-faults.json`; unavailable in the cleaned checkout) và verifier (historical evidence path: `../runs/nckh-native-261005-1257-r36-cursor-prompt-stop-faults-attempt-07/verify-prompt-stop-delivery.py`; unavailable in the cleaned checkout) ghi 10 prompt submissions, chín model replies quan sát được và một admission rejection. Source r36/281 pins/hash `1a471686c5b1e89e6838957161a8ae4c6787d46d227420d8644636062da90d30` không đổi. Surface là Cursor CLI interactive terminal, version `2026.09.15-d2fe57e`; selector được cấp quyền là Grok 4.7, context500k, xhigh, fast=false.

## Actual native response

| Selected fault | `beforeSubmitPrompt` | `stop` |
|---|---|---|
| Malformed input | `continue:false`, native rejection hiển thị; không có model reply/Stop | Model đã trả lời; một Stop callback |
| Malformed output | Model reply và Stop vẫn xuất hiện | Model đã trả lời; một Stop callback |
| Timeout | Observer ngủ24s, vượt native limit20s; model reply vẫn xuất hiện | Model đã trả lời; observer hoàn tất sau24s |
| Crash | Observer exit17; model reply và Stop vẫn xuất hiện | Model đã trả lời; một Stop callback |
| Unsupported selected codec | Runner nhận event do controller chọn; model reply và Stop vẫn xuất hiện | Model đã trả lời; một Stop callback |

19 case callbacks và một startup callback đều có native version/session/project bindings. Mỗi selected fault được đưa vào sau genuine callback; fault origin là `controller-injection-after-genuine-callback`. Đây là negative-path evidence, không phải universal enforcement PASS. Unsupported-codec injection không thay native unsupported-tool evidence. Stop observations xảy ra sau model reply; số callback được ghi không cho thấy một Stop bổ sung trong từng ca.

Native hook limit20s/runner limit5s là cấu hình instrumented của lượt này. Hai elapsed observations là24.139189s và24.142718s. Production template timing có báo cáo riêng. Terminal là bounded harness chunks; các chunk của lượt07 không báo truncation, không tuyên bố full native transcript. Model/effort có command/UI bindings; backend/billing attestation không được quan sát.

## Cleanup và collector reconciliation

Native exit requests và graceful taskkill chưa đóng cây tiến trình. Exact PID/UTC creation identity được kiểm trước force-stop; harness exit1 được giữ. Final audit có zero matching processes và zero live trong chín tracked PIDs. Cleanup gỡ26 matching config/payload members, giữ406 historical project members và protected global config hashes. CLI-owned state file hash changed from `fc4adefc9e8db323ae84ac77049ae1dfb2f08ed1f5a58b6cc5b51ca39206af91` to `e60abf4e20da00911ef6a550c34f814a23d50751b54d48139f7590a4a3331adc`; controller direct-write remains false. Exact state delta is not recoverable from hashes alone.

Lần identity check đầu từ chối trước taskkill vì PowerShell chuyển JSON timestamp sang DateTime, làm string comparison lệch. Diagnostic xác nhận cùng creation identity; exact UTC ticks được dùng trước thao tác đóng. Verifier đầu gặp hai saved submission key variants; collector được sửa để đọc cả hai, giữ nguyên raw submissions và failure receipt. Không gửi lại model prompts.

Full native task remains unchecked; plan44/45. Installed r25, accepted r29 VI/EN samples và scientific/stable/release gates giữ bindings riêng.
