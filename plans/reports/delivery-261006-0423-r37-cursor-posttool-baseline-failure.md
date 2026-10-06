# Cursor r37 — PostToolUse Write baseline thất bại

**Trạng thái:** failed native baseline observation đã đối chiếu; sáu ca phụ thuộc chưa chạy. Plan **44/45, P3 active, full native gate unchecked**.

[Frozen brief](../runs/nckh-native-261006-0423-r37-cursor-posttool-controls-attempt-52/frozen-brief.json) chuẩn bị bảy ca Cursor CLI **2026.09.15-d2fe57e / Grok4.7 / 500k / xhigh / fast=false / Run Everything**, mỗi ca một Write vào marker public do controller tạo. [Controller adaptation](../runs/nckh-native-261006-0423-r37-cursor-posttool-controls-attempt-52/controller-adaptation.json) chọn current-r37 Write/PostToolUse tại producer5s vì bằng chứng fault PostToolUse trước thuộc r34/Shell. Nguồn r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` giữ nguyên. Existing selectedModel/native startup display xác nhận lựa chọn; backend parameters không được attested.

## Native observation và frozen oracle

[Verification](../runs/nckh-native-261006-0423-r37-cursor-posttool-controls-attempt-52/verified-baseline-failure-observation.json) đối chiếu **1 lượt / 1 actual Write / 5 callbacks / 5 policy receipts**, gồm SessionStart và prompt/pre/post/Stop. Pre/post cùng native tool ID/session/path/version; Write đã đổi marker trước callback PostToolUse.

| Byte contract | Đuôi bytes |
|---|---|
| Frozen expected marker | CR LF / `0d0a` |
| Actual marker ở PostToolUse, Stop và cuối lượt | CR CR LF / `0d0d0a` |

PostToolUse trả **pending / artifact-final-bytes-missing-or-stale**, wire native là `additional_context` với cùng reason. Exact marker/advisory oracle thất bại. Final reply vẫn quan sát được; đây không phải semantic QA, prevention/rollback hoặc pass của bảy ca.

Lượt này khai báo CRLF từ đầu theo observation Write44. Native input có field `content`, nhưng body của field chưa retained. Origin của ký tự CR bổ sung chưa xác định; bounded vendor JS searches chỉ thấy parser/rendering snippets, không tìm được owner của Write normalization. Không quy lỗi riêng cho model hoặc tool từ output bytes alone. Original LF oracle44 và current CRLF oracle52 đều giữ failure của chính mình; không đổi thành tolerance hoặc regrade.

[Sealed failure](../runs/nckh-native-261006-0423-r37-cursor-posttool-controls-attempt-52/failed-baseline-observation.json) giữ callback/receipt hashes và exact altered bytes. Sáu fault/deny ca tiếp theo chưa được chọn hoặc gửi; không model retry. Read prerequisite nằm ngoài selected `^Write$` matcher. PreToolUse20s, PostToolUse/other handlers5s, inner runner5s; prepared sleeper8s chưa được kích hoạt.

## Temporal capture và lỗi khi root đóng

Root PID9404/exact creation tick `134357093863657883` bind terminal29583. Repaired temporal capture thu252 identities; [monitor error](../runs/nckh-native-261006-0423-r37-cursor-posttool-controls-attempt-52/monitor-failure.json) xuất hiện khi root đóng: “Owned root identity changed or is not observable”. Native terminal thoát0, monitor5099 thoát1. Last snapshot giữ running status; continuous monitor completion unqualified.

[Actual process-state control](../runs/nckh-native-261006-0423-r37-cursor-posttool-controls-attempt-52/verified-process-exit-state-control.json) dùng một Python process do controller tạo, giữ handle sau exit0: creation time vẫn query được, trong khi **GetExitCodeProcess xác nhận terminated**. Điều này chứng minh creation time không đủ để gọi process active. Closing-race là supported inference cho lỗi native52, không thay raw failure thành exit0. Helper mới đọc active/terminated/absent/unobservable để dùng ở lượt tiếp theo; permission failure giữ unobservable.

[Final audit](../runs/nckh-native-261006-0423-r37-cursor-posttool-controls-attempt-52/process-final-audit.json) dùng **612 qualified temporal identities / zero matching hoặc tracked-live**, so PID + creation với CIM precision. Không dùng raw union2968 làm ownership, giữ27 preexisting apps từ correction51. Không process stop.

## Cleanup, review và continuation

[Cleanup](../runs/nckh-native-261006-0423-r37-cursor-posttool-controls-attempt-52/cleanup.json) gỡ33 matching config/payload/fixture members, giữ991 historical project members và protected global config hashes. Cleanup definition chỉ đổi hash của fixture đã match genuine Post/Stop snapshots để gỡ đúng altered owned bytes; frozen byte oracle giữ nguyên. CLI-owned state hash có đổi; fields không được suy ra. Không direct global write hoặc installed r25 replacement.

Failure-observation verifier đạt lần đầu; review inline. Chưa chạy seven-case success verifier vì baseline gate thất bại/sáu ca unstarted; original verifier source giữ nguyên. Terminal chunks có truncation, không full-transcript claim. Broad unchanged r37 checks được tái sử dụng.

Next native needs bounded input-content hash/tail diagnostics trên đúng marker public, contract phân biệt LF trong Write argument và CRLF trên disk, và monitor đọc actual exit state. Không gửi lại prompt52. Codex cache/metadata authority, Claude model/effort và direct IDE/Desktop qualification còn mở; CLI/dangerous grants và exact r29 VI/EN acceptance giữ hiệu lực.
