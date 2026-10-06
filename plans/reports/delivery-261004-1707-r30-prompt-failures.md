# NCKH r30 — Codex native prompt failure paths

Trạng thái: **bảy callbacks thực đã ghi; có native fail-open ở các lỗi đã thử; qualification còn mở, plan 44/45**.

Bổ sung sau [direct prompt admission](delivery-261004-1707-r30-prompt-admission.md). [Structured evidence](delivery-261004-1707-r30-prompt-failures.json) bind source-lock r30 và các receipts thực. Source kit, writers, deterministic tests và archives không đổi; không chạy lại full suite/build.

## Phạm vi và cách thử

Codex CLI **0.154.0**, đúng project thử đã được [native grant](../runs/nckh-native-261004-1707-attempt-01/native-grant.json). Một observer do controller sở hữu được normal UI review/trust/enable riêng. Native host gọi observer bằng event `UserPromptSubmit`; sau callback mới inject lỗi đã khai báo. Observer ghi input hash/size/field names, không lưu full prompt/transcript. Các nhánh delegate chạy unchanged extracted r30 runner; malformed-output, timeout và crash được inject trước khi delegate.

Execution route là installed CLI `app-server --stdio` qua native `thread/start`/`turn/start`; CLI TUI được dùng cho trust/enable/cleanup. Không lấy route này để thay bằng chứng prompt nhập trực tiếp trong TUI, Desktop hoặc IDE.

Provider vẫn chỉ tới refused loopback, không có fake server/response/key. 27 user-config hooks và ba configured MCP servers disabled theo invocation; builtin `cua_repl` vẫn có thể báo ready, không được gọi. Không có successful inference hoặc tool invocation. Cửa sổ quan sát mỗi case 10 giây; sau đó owned app-server đóng.

## Kết quả native thực

| Case đã khai báo | Runner/observer | Phản ứng native | Receipt |
|---|---|---|---|
| Policy deny | Runner `block / bounded-input-exceeded` | Hook `blocked`, turn hoàn tất với `items=[]` | [Policy deny](../runs/nckh-native-261004-1707-attempt-01/projects/codex/failure-probe-policy-deny.json) |
| Advisory | Runner góp context `writing-resource-advice-only` | Hook `completed`, sau đó có provider connection failure | [Advisory](../runs/nckh-native-261004-1707-attempt-01/projects/codex/failure-probe-advisory.json) |
| Malformed runner input | Callback host hợp lệ; observer thay runner input bằng `{`; runner trả `block / hook-input-or-context-invalid` | Hook `blocked`, turn hoàn tất với `items=[]` | [Malformed input](../runs/nckh-native-261004-1707-attempt-01/projects/codex/failure-probe-malformed-input.json) |
| Malformed observer output | Observer in invalid JSON và exit 0 | Hook `failed`, lỗi invalid user-prompt JSON; host vẫn thử tới provider | [Malformed output](../runs/nckh-native-261004-1707-attempt-01/projects/codex/failure-probe-malformed-output.json) |
| Timeout | Observer vào callback rồi sleep 8 giây; definition timeout 2 giây | Hook `failed` với `hook timed out after 2s`; host vẫn thử tới provider | [Timeout](../runs/nckh-native-261004-1707-attempt-01/projects/codex/failure-probe-timeout.json) |
| Crash | Observer ghi intentional exit 17 rồi dừng | Hook `failed`; host báo exit code 1 ở command layer, vẫn thử tới provider | [Crash](../runs/nckh-native-261004-1707-attempt-01/projects/codex/failure-probe-crash.json) |
| Unsupported selected codec event | Native event vẫn là UserPromptSubmit; observer chọn `UnknownNckhEvent` cho runner. Runner exit 3/`{}`, có degraded receipt `block` | Hook `failed`; host báo exit code 1, vẫn thử tới provider | [Unsupported codec](../runs/nckh-native-261004-1707-attempt-01/projects/codex/failure-probe-unsupported-codec.json) |

Tổng **7 callbacks, 4 policy receipts**, gồm hai normal/advisory receipts và hai degraded input/codec receipts. Không biến `decision=block` của deterministic receipt thành host prevention: unsupported-codec case có block receipt nhưng native hook vẫn failed/continued.

## Quyết định từ bằng chứng

Trong đúng UserPromptSubmit/version/surface này, malformed output, timeout, crash và unsupported selected codec đều **fail-open ở prompt admission**: sau hook failure có error notification từ provider connection attempt. Endpoint refusal giới hạn probe; chưa có model output hoặc tool-side-effect oracle. Đây không phải PreToolUse/tool-level prevention result.

Không kích hoạt route này như enforcement. Giữ candidate inactive/manual cho qualification chưa đủ. Malformed-input case chỉ chứng minh handler phản ứng với input bị inject sau callback; không khẳng định native host đã phát malformed event. Unsupported-codec case không phải host phát unsupported event/tool. Duplicate project/plugin invocation và unsupported native tool vẫn chưa thử ở Codex; những event/surface khác giữ pending/unverified.

## Trust và cleanup

[Definition](../runs/nckh-native-261004-1707-attempt-01/projects/codex/failure-probe-registration.json): `sha256:083884235854b0985c5612fab601f099bf17bbe0d4a422667a3d967abe0aafa3`, observer timeout 2 giây. [Metadata trước review](../runs/nckh-native-261004-1707-attempt-01/projects/codex/failure-probe-metadata-01.json) là modified/disabled. [Normal UI review](../runs/nckh-native-261004-1707-attempt-01/projects/codex/failure-probe-ui-trust.json) chọn riêng project Hook 6, trust rồi enable. [Metadata trước tests](../runs/nckh-native-261004-1707-attempt-01/projects/codex/failure-probe-metadata-02.json) xác minh đúng hash trusted/enabled.

[UI disable](../runs/nckh-native-261004-1707-attempt-01/projects/codex/failure-probe-ui-disable.json) và [metadata](../runs/nckh-native-261004-1707-attempt-01/projects/codex/failure-probe-metadata-03.json) xác nhận hook đã tắt. [Matching cleanup](../runs/nckh-native-261004-1707-attempt-01/projects/codex/failure-probe-cleanup.json) gỡ một config và 26 staged payload members; contexts/control/observer/observations/receipts giữ làm evidence. Unrelated native-hook-state hash không đổi. [Sau cleanup](../runs/nckh-native-261004-1707-attempt-01/projects/codex/failure-probe-metadata-04.json), host không còn project hooks callable.

Native store hiện giữ **ba project-test state keys disabled**. UserPromptSubmit key đã đổi trusted_hash từ direct-runner definition cũ sang observer definition mới qua normal UI; không cộng các historical definitions thành bốn trusted hashes hiện có. PreToolUse/SessionStart keys cũ vẫn disabled. Project trust có thể còn lưu; không chỉnh trực tiếp global trust store.

[Process audit đầu](../runs/nckh-native-261004-1707-attempt-01/process-audit-prompt-failures.json) thấy chính metadata probe đang chạy đồng thời. Probe đó kết thúc exit 0; [audit sau khi nó kết thúc](../runs/nckh-native-261004-1707-attempt-01/process-audit-prompt-failures-final.json) có 0 matching run processes. Không restart probe từ observation timeout hoặc dừng user process.

## Công việc còn lại

Native checkbox của [phase 3](../261004-0047-nckh-research-data-hooks-writing/phase-03-portable-hooks.md) vẫn unchecked. Cần event/version/surface và duplicate/tool prevention evidence còn thiếu; các lượt cần inference thực vẫn chờ host/quota hoặc provider budget. Cursor authentication, AGY eligibility/connectivity, Desktop/IDE evidence giữ các gate riêng. Hai mẫu VI/EN đã accepted; installed r25 và release/scientific/stable state không thay đổi.
