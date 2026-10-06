# Cursor r37 — năm fault native trên directory Grep

**Trạng thái:** scoped native observations verified; **original full-run oracle failed** do monitor. Plan **44/45, P3 active, full native gate unchecked**.

[Frozen brief](../runs/nckh-native-261006-0420-r37-cursor-grep-faults-attempt-51/frozen-brief.json) giữ năm lượt Cursor CLI **2026.09.15-d2fe57e / Grok4.7 / 500k / xhigh / fast=false / Run Everything**. Existing selectedModel và native startup display xác nhận lựa chọn; backend/billing parameters không được attested. Mỗi lượt chỉ yêu cầu một Grep trên đúng thư mục public có marker tổng hợp đã khai báo, không retry, không whole-turn deadline. Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` giữ nguyên.

## Quan sát native

[Scoped verification](../runs/nckh-native-261006-0420-r37-cursor-grep-faults-attempt-51/verified-grep-observations-with-monitor-gap.json) xác nhận **5 actual Grep / 21 callbacks / 14 policy receipts**. Mỗi actual postToolUseFailure có **permission_denied**, tool ID/session/path/version khớp PreToolUse, không successful post, fixture nguyên exact bytes và final marker quan sát được.

| Fault sau genuine PreToolUse | Phản hồi native thật | Policy receipt được chọn |
|---|---|---|
| Malformed input | permission_denied / hook-input-or-context-invalid | block |
| Malformed output | permission_denied / invalid JSON | Không có |
| Timeout | permission_denied / timed out after 20000ms | manual đến muộn |
| Crash | permission_denied / exit17 | Không có |
| Unsupported codec selector | permission_denied / exit3 | block |

Outer PreToolUse20s/failClosed=true, sleeper24s, inner runner5s, other handlers5s và bounded failure diagnostic10s. Timeout observer/runner đã terminal trước khi đổi control. Manual/tool-route-uncovered receipt tới sau không đảo native timeout denial. Native failure logger không inject policy hoặc đọc full transcript.

[Controller adaptation](../runs/nckh-native-261006-0420-r37-cursor-grep-faults-attempt-51/controller-adaptation.json) phân biệt Write27 matcher với directory Grep hiện còn uncovered trong operation map. Normal public route/manual được quan sát riêng ở [native49](./delivery-261006-0345-r37-cursor-directory-search.md); private-directory native denial ở [native50](./delivery-261006-0400-r37-cursor-directory-denial.md) giữ scope riêng. Đây là fault injection **sau callback native thật**; unknown-host-event delivery, glob/root traversal, direct5s và all-tools enforcement vẫn unqualified.

## Monitor failure và hiệu chỉnh ownership

Native Cursor terminal52990 thoát0. Monitor90446 thoát1 do **WinError5 khi os.replace tệp ghi nhận**; exact lock holder chưa xác định. [Original verifier failure](../runs/nckh-native-261006-0420-r37-cursor-grep-faults-attempt-51/original-verification-result.json) và [monitor error](../runs/nckh-native-261006-0420-r37-cursor-grep-faults-attempt-51/monitor-exit.json) được giữ nguyên. Original verifier, snapshots và oracle không bị sửa hoặc regrade; continuous monitoring không được gọi thành successful.

Đối chiếu CIM có xét precision phát hiện **27 raw live matches** trong historical union2968. [Ownership correction](../runs/nckh-native-261006-0420-r37-cursor-grep-faults-attempt-51/process-ownership-correction.json) binds từng match với capture có process creation **trước** root thử: Docker/WSL/cloudflared, Discord và Windows UX đã có từ trước. Parent-PID traversal không xét creation đã gán sai ancestry; exact FILETIME comparison với CIM microsecond đã bỏ sót live matches. Các ứng dụng này được giữ nguyên, không process stop.

Current native51 snapshots có **358 temporally valid captured identities**,20 rows bị loại vì ancestry không hợp lệ; corrected scoped owned-live0 và project-command matches0. Historical raw “all tracked zero live” claims còn cần qualification theo correction này. Không biến union timestamp thành số tiến trình thực tế, không dùng correction để sửa các oracle lịch sử.

[Separate verifier adaptation](../runs/nckh-native-261006-0420-r37-cursor-grep-faults-attempt-51/scoped-verifier-adaptation.json) giữ các behavioral assertions; scope mới xác nhận callback/native response/fixture và corrected scoped process exit, đồng thời bắt buộc monitor exit1/original failed verdict. Đây không phải pass của original full-run oracle.

## Cleanup và phần còn lại

[Cleanup](../runs/nckh-native-261006-0420-r37-cursor-grep-faults-attempt-51/cleanup.json) gỡ27 matching config/payload/fixture members, giữ938 historical project members và protected global configs. CLI-owned state hash thay đổi; fields không được suy ra. Controller không direct-write global hoặc thay installed r25.

Scoped verifier đạt lần chạy đầu; review inline, không independent review. Terminal chunks có truncation; bounded native failure metadata được giữ riêng. Broad r37 tests/build không chạy lại và không được gọi thành native proof.

[Controller capture checks](../runs/nckh-native-261006-0420-r37-cursor-grep-faults-attempt-51/verified-process-capture-checks.json) đạt sáu kiểm tra hẹp: reject preexisting subtree, giữ valid temporal chain, reject mismatched root/ambiguous PID generation, quan sát checker PID thật và atomic write roundtrip. Helper mới yêu cầu exact expected root identity; atomic commit chỉ retry tối đa6 lần/0.775s, giữ terminal error. Đây là controller-only evidence, chưa có native host/model dùng helper mới và không chứng minh đã tái hiện hoặc loại bỏ WinError5. Các helper lịch sử giữ nguyên.

Native tiếp theo phải dùng helper đã sửa cùng timestamp-precision/ownership audit. Codex test-plugin cache/metadata authority và Claude model/effort đã hỏi lại sau context recovery, chưa có direct reply. Cursor plugin prompt/stop gaps, remaining event/tool/fault cells, AGY search/multi-replace và IDE/Desktop qualification còn mở. Existing dangerous/CLI grants và exact r29 VI/EN owner acceptance tiếp tục có hiệu lực.
