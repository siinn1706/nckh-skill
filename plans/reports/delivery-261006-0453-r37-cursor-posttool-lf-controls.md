# Cursor CLI r37: nội dung LF và các quan sát PostToolUse/Write

[Bằng chứng đã xác minh](../runs/nckh-native-261006-0453-r37-cursor-posttool-lf-controls-attempt-53/verified-posttool-observations.json) ghi **7 lượt model / 7 Write thật / 29 callbacks / 27 receipts** trên Cursor CLI **2026.09.15-d2fe57e**, Grok4.7/500k/xhigh/fast=false, Run Everything. Native terminal và monitor đều exit0. Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` giữ nguyên; full native task vẫn **unchecked / 44 of45 / P3 active**.

## Hợp đồng nội dung và byte

[Brief đóng băng](../runs/nckh-native-261006-0453-r37-cursor-posttool-lf-controls-attempt-53/frozen-brief.json) tách **LF trong argument `content`** và **CRLF dự kiến trên đĩa**. Hash, độ dài32 byte và tail16 hex của argument thật khớp cả PreToolUse/PostToolUse cho từng marker. Hash tệp khớp bytes33 trên đĩa và đã hiện diện khi callback sau ghi bắt đầu. Mỗi lượt có một cặp pre/post Write cùng tool ID/session/path/version, một câu trả lời kết thúc đúng và không retry model.

Observer chỉ giữ hash/length/tail của đúng marker ASCII công khai do controller tạo; không lưu body native `content`. Việc đổi LF sang CRLF được quan sát trên tuyến Write này; hàm chuẩn hóa cụ thể bên trong vendor chưa được xác lập.

[Oracle52 thất bại](../runs/nckh-native-261006-0423-r37-cursor-posttool-controls-attempt-52/verified-baseline-failure-observation.json) giữ nguyên: yêu cầu CRLF nhưng nhận CRCRLF, policy pending/stale bytes, monitor exit1. Oracle LF44 cũng giữ nguyên thất bại. Ca53 có hợp đồng argument khác và diagnostics mới; không regrade hai ca cũ.

## Kết quả từng ca

| Ca | Observer sau Write | Policy/wire đã quan sát |
|---|---|---|
| allow | completed/exit0 | advisory; `delivery-bindings-current-review-separate` |
| policy-deny | completed/exit0 | block; `bounded-input-exceeded` trong additional_context |
| malformed-input | completed/exit0 | degraded block; `hook-input-or-context-invalid` |
| malformed-output | intentional invalid JSON | Không có selected policy receipt |
| timeout | completed/exit0 sau 8.263741s | advisory receipt sau mức khai báo5s; effective native deadline unqualified |
| crash | injected `os._exit(17)` sau callback thật | Không có selected policy receipt |
| unsupported-codec | completed/exit3 | degraded block receipt; native wire `{}` |

Năm lỗi là injection do controller sau callback native thật. Codec không hỗ trợ là selector thử; không chứng minh host giao một unknown event. Tệp đã thay đổi trước PostToolUse và còn đúng bytes ở cuối cả7 lượt; enforcement ngăn ghi/rollback/scientific QA vẫn unqualified.

Timeout có độ trễ khai báo8s, callback thực tế8.263741s và receipt. Native timeout message quan sát: **false**; selected terminal retention complete: **true**. Mức timeout5s trong definition không tự chứng minh deadline hiệu lực của host. [Preimage và refinement](../runs/nckh-native-261006-0453-r37-cursor-posttool-lf-controls-attempt-53/observation-scope-refinement.json) giữ đúng phạm vi này; byte/content oracles và điều kiện exit0 không đổi.

## Tiến trình và cleanup

[Ownership](../runs/nckh-native-261006-0453-r37-cursor-posttool-lf-controls-attempt-53/native-process-ownership.json) bind root PID6532/FILETIME134357110215523880 với terminal78758, project thử, owner `/root`, port do native CLI quản lý. Monitor79098 dùng GetExitCodeProcess và exact generation, xử lý root close bằng trạng thái thật. Snapshot cuối ghi root absent, không capture errors; harness xác nhận cả hai handle terminal exit0. Kết quả không regrade monitor failures51/52.

[Audit cuối](../runs/nckh-native-261006-0453-r37-cursor-posttool-lf-controls-attempt-53/process-final-audit.json): union1542 identities từ bộ612 đã qualified và capture mới; zero matching/tracked-live. Raw historical union2968 không dùng làm ownership. Giữ27 ứng dụng preexisting; không taskkill/Stop-Process. Sau native `/exit`, [cleanup](../runs/nckh-native-261006-0453-r37-cursor-posttool-lf-controls-attempt-53/cleanup.json) gỡ33 matching config/payload/fixture members, giữ1010 historical members và protected global config hashes. Native CLI-owned state có thể còn; controller không direct-write global.

## Verification và giới hạn còn lại

Verifier exit0 ở [tool result](../runs/nckh-native-261006-0453-r37-cursor-posttool-lf-controls-attempt-53/verification-tool-result.json) kiểm hashes, actual input diagnostics, pre/post identities, bytes trước hook, final replies, selected receipt outcomes, terminal/monitor exits, historical preservation và audit. Review inline; không có independent reviewer. Một poll baseline bị output truncation được giữ rõ; bytes/callback evidence và final marker có bindings riêng.

Sandbox CIM preflight và dependent prepare từng fail trước model; [failure record](../runs/nckh-native-261006-0453-r37-cursor-posttool-lf-controls-attempt-53/sandbox-preflight-failure.json) giữ cả hai. Read-only inventory đã chạy qua quyền process reconciliation, rồi mới stage và gửi model. Không retry model, đổi source hoặc che lỗi.

[Source check](../runs/nckh-native-261006-0453-r37-cursor-posttool-lf-controls-attempt-53/final-source-check.json) xác minh current source. Reuse checkpoint192 successful tests/one Windows skip và16 archives cho source/input không đổi; không chạy lại broad suite. Installed r25, publication và human acceptance của exact r29 samples giữ scope riêng.

Các ô native còn thiếu, effective timeout deadline, root/glob search, project/plugin và direct IDE qualification vẫn mở. Quyền cache/metadata Codex ngoài workspace và Claude model/effort đã được hỏi lại sau recovery, chưa có câu trả lời; chưa cài plugin hoặc gửi Claude model prompt. AGY/Gemini3.8FlashMedium/dangerous và Cursor/Grok4.7/500k/xhigh/dangerous grants tiếp tục được giữ.
