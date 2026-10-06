# R37 Cursor: năm ca lỗi native Write

[Verified bindings](./delivery-261005-2125-r37-cursor-write-faults.json) / [frozen brief](../runs/nckh-native-261005-2125-r37-cursor-Write-faults-attempt-27/frozen-brief.json) ghi năm model turns/prompt submissions trên Cursor CLI2026.09.15-d2fe57e, Grok4.7/context500k/xhigh/fast=false. Source giữ r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb`.

## Kết quả native

| Fault injection sau actual PreToolUse/Write callback | Phản hồi native | Tệp giả lập |
|---|---|---|
| Malformed runner input | permission_denied/hook-input-or-context-invalid | Không đổi |
| Malformed hook output | permission_denied/invalid JSON | Không đổi |
| Sleeper24s | permission_denied/timeout20000ms | Không đổi |
| Observer crash exit17 | permission_denied/exit17 | Không đổi |
| Unknown codec event | permission_denied/runner exit3 | Không đổi |

Mỗi ca giữ một actual Write callback và một native failure có cùng nonempty tool-use ID/session/path/version; tổng năm distinct IDs. Zero successful selected Write post receipts và đủ năm final reply markers. Fault origin luôn `controller-injection-after-genuine-callback`; observer là test harness, không phải direct packaged handler. PreToolUse20s/failClosed=true giữ producer-default bound, inner runner5s, các packaged handlers khác5s, diagnostic failure observer10s. Timeout observer hoàn tất sau24s, nhưng host từ chối ghi ở20000ms; late policy allow không thay phản hồi native.

Tool hooks chọn `^Write$`; authorized Read prerequisites chỉ trên exact public synthetic fixture và nằm ngoài selected matcher. Các kết quả không chứng minh default-all-tools hoặc confidential-Read enforcement. Unknown codec event được inject sau một supported native Write callback; genuine native unsupported event/tool admission vẫn chưa được chứng minh. Malformed parse receipt không có context_hash được giữ nguyên, correlate bằng selected genuine callback/control/runner và native failure ID; không invent context binding.

## Preservation và dọn dẹp

Native Ctrl+D/exit0; [union process audit](../runs/nckh-native-261005-2125-r37-cursor-Write-faults-attempt-27/final-process-audit-attempt-02.json) đối chiếu start/before-stop của native21/24/25/27:53 identities, zero matching/tracked-live, không taskkill. AGY PID44132 không còn được thấy trong snapshot cuối; controller không stop và không suy nguyên nhân. [Cleanup](../runs/nckh-native-261005-2125-r37-cursor-Write-faults-attempt-27/cleanup.json) gỡ26 matching config/payload members, giữ803 historical project members và native evidence; protected global config hashes unchanged. CLI-owned state hash đổi, fields không được suy ra; global-direct-write=false.

Initial launch chunk chỉ có terminal control bytes; [startup binding adaptation](../runs/nckh-native-261005-2125-r37-cursor-Write-faults-attempt-27/startup-display-binding-adaptation.json) trước first selection bind thêm native startup display, không thay prompt/oracle hoặc retry model. Verifier exit0 ngay lần đầu. Raw terminal chunks bounded/truncated và native tool-return content không được giữ.

## Runtime route và gates còn lại

Owner chọn tiếp tục **AGY CLI dangerous/Gemini3.8Flash** và **Cursor CLI dangerous/Grok4.7xhigh**, sau khi [fresh AGY IDE inventory26](./delivery-261005-2120-r37-agy-window-inventory.md) vẫn không trả đúng owned window. Đây là route cho các lượt tiếp theo; IDE vẫn unverified. Các quyền access/model/dangerous đã cấp giữ nguyên.

Plan **44/45/P3 active/full native task unchecked**. [Write25](./delivery-261005-2055-r37-cursor-selected-write.md) bổ sung actual private Write prevention; batch27 bổ sung Write fault controls cùng revision. Còn event/tool/fault matrices khác, plugin prompt/stop duplicate callbacks, genuine unsupported native observations và Claude model/effort/native turns. Exact r29 VI/EN acceptance, installed r25 và publication/scientific/stable/release gates giữ riêng.
