# Cursor r37 — native plugin prompt/stop alias control

## Kết quả

Một interactive turn trên Cursor CLI `2026.09.15-d2fe57e`, đúng model được cấp `grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]`. Project giữ năm native event definitions; minimal plugin qua `--plugin-dir` chỉ có nested `UserPromptSubmit` và `Stop`. [Giả thuyết đóng băng trước khi chạy](../runs/nckh-native-261005-1923-r37-cursor-plugin-routing-inspection-attempt-20/routing-hypothesis.json) dựa trên parser của bản CLI hiện tại và [Cursor third-party hooks reference](https://cursor.com/docs/reference/third-party-hooks). Source/docs evidence không tự chứng minh native callback.

| Event | Project callbacks | Plugin callbacks | Policy receipts | Duplicate result |
|---|---:|---:|---:|---|
| beforeSubmitPrompt / UserPromptSubmit | 1 | 0 | 1 | Unqualified |
| stop / Stop | 1 | 0 | 1 | Unqualified |

Có thêm một project sessionStart callback/receipt; plugin sessionStart không được cấu hình trong control này. Tổng **3 actual callbacks / 3 policy receipts**, cùng native session/version và verified r37 runner. Final reply marker observed; không có selected tool callback, một prompt/submission, không injected fault hoặc model retry. Hai alias vẫn không cung cấp plugin callback trong invocation này; nguyên nhân chưa verified, không suy thành unsupported cho mọi version/surface và không regrade native19.

## Capture và cleanup

Project preToolUse20s/failClosed=true, handlers khác5s; hai plugin handlers5s. Observer forwards genuine bounded payload tới packaged runner unchanged với inner bound5s. Đây là instrumented control; raw terminal bị truncation và không có native tool-return observation.

Cursor thoát bằng Ctrl+D với **exit0**. Controller sau đó thử graceful cleanup không cần thiết; guard từ chối vì root đã absent, exit1 và không gọi taskkill. [Refusal receipt](../runs/nckh-native-261005-1930-r37-cursor-plugin-alias-controls-attempt-21/post-exit-cleanup-refusal.json) được giữ. Final audit có zero matching/zero tracked-live processes; AGY process được giữ cho công việc tiếp theo.

Cleanup gỡ **28 matching owned members**, giữ **750 historical members** và protected global config hashes. CLI-owned state hash thay đổi; changed fields không được suy từ hash. First preparation observation failure, prepared-state recovery và first terminal-wrapper save đều được giữ; wrapper/direct response khớp cùng native chunk, không có prompt/poll retry để thay kết quả.

Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` giữ nguyên; reuse local checks của đúng source. Plan vẫn **44/45, phase3 active**, full native matrix/private Write/remaining surfaces và Claude model/effort còn mở. Exact r29 VI/EN owner acceptance được giữ; installed r25/publication/scientific/stable/release không đổi.

## Evidence

- [Verified bindings](./delivery-261005-1930-r37-cursor-plugin-alias-controls.json)
- [Original collected case](../runs/nckh-native-261005-1930-r37-cursor-plugin-alias-controls-attempt-21/case-alias.json)
- [Native summary](../runs/nckh-native-261005-1930-r37-cursor-plugin-alias-controls-attempt-21/native-alias-summary.json)
- [Frozen brief](../runs/nckh-native-261005-1930-r37-cursor-plugin-alias-controls-attempt-21/frozen-brief.json) và definition hashes (historical evidence path: `../runs/nckh-native-261005-1930-r37-cursor-plugin-alias-controls-attempt-21/definitions/session.json`; unavailable in the cleaned checkout)
- Preparation recovery (historical evidence path: `../runs/nckh-native-261005-1930-r37-cursor-plugin-alias-controls-attempt-21/preparation-terminal-reconciliation.json`; unavailable in the cleaned checkout) và terminal wrapper recovery (historical evidence path: `../runs/nckh-native-261005-1930-r37-cursor-plugin-alias-controls-attempt-21/terminal-wrapper-reconciliation.json`; unavailable in the cleaned checkout)
- [Cleanup](../runs/nckh-native-261005-1930-r37-cursor-plugin-alias-controls-attempt-21/cleanup.json) và [process audit](../runs/nckh-native-261005-1930-r37-cursor-plugin-alias-controls-attempt-21/final-process-audit.json)
