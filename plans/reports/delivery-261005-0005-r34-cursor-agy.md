# Delivery r34 và native Cursor/AGY

## Trạng thái

Candidate **r34** đạt local delivery. Plan giữ **in-progress, 44/45**; task native evidence theo event/version/surface vẫn unchecked. Hai mẫu VI/EN của r29 đã được owner chấp nhận. [Structured evidence](./delivery-261005-0005-r34-cursor-agy.json) bind hashes, archived packages, callbacks, tool outcomes, cleanups và historical failures.

Source có **281 pins**, đúng **39 identities / 156 base cases / 19 families / 9 resources**; canonical hash `8ca3304f3c906b0a3421c38fbb32c939ec23839537e9b9c5fc23421da0a21b34`. Public resource access giữ ON; OFF chỉ dùng internal comparison. Installed r25 chưa update; stable/scientific/release chưa qualified.

## Native evidence dẫn tới sửa lỗi

- r31 sửa AGY permission shape: non-blocking dùng `ask`, block/pending dùng `deny`; native permission checks vẫn thuộc host. R32 sửa closure-test expectation tương ứng; [full r32](../runs/nckh-native-261004-2112-r32-attempt-01/deterministic-r32-attempt-01.json) đạt 183 tests và một skip.
- [Native protected-write trước sửa](../runs/nckh-native-261004-2112-r31-attempt-01/projects/agy-model/attempts/protected-file-before-01.reconciliation.json) thực sự tạo marker 19 bytes vì codec bỏ native `TargetFile`. Giữ marker, collector failure và callback evidence; không ghi thành deny.
- r33 kiểm `TargetFile`, `AbsolutePath`, `DirectoryPath`, `SearchDirectory`, `SearchPath`, các alias, target thiếu/sai kiểu; 21 subcase regressions trước sửa và 14 focused tests sau sửa được giữ trong [review](../runs/nckh-native-261004-2112-r32-attempt-01/source-native-path-review.json). Native file/plugin subset đạt ở r33.
- [Full r33](../runs/nckh-native-261004-2112-r33-attempt-01/deterministic-r33-attempt-01.json) thất bại: 186 tests, một concurrent receipt error, một skip. [Windows diagnostic](../runs/nckh-native-261004-2112-r33-attempt-01/receipt-parent-resolution-diagnostic-01.json) ghi child `Path.resolve` giữ extended prefix khi receipt parent xuất hiện đồng thời; root không có prefix. Đây là lỗi normalization/race thực, chưa phải path escape thực.
- r34 tạo contained receipt directory trước child resolution. Containment/no-links/kernel-lock/atomic-write guards giữ nguyên. [Review](../runs/nckh-native-261004-2112-r33-attempt-01/source-receipt-parent-review.json) ghi 15 focused passing tests, gồm 150 fresh directories × 6 concurrent calls và traversal rejection. Review inline; không claimed independent reviewer.

## Local delivery đã chạy

| Gate | Kết quả r34 |
|---|---|
| Full deterministic | 187 tests, 1 Windows symlink skip; successful, 1098.609 giây |
| Reproducibility/build | Bốn variants, 16 bundles; mọi command exit0 |
| Archive/extraction | 16 archives giải nén ngoài source, closure/manifest verified |
| Extracted resource readers | 216 genuine local reads |
| OFF writer behavior | 48 disabled/no-read observations |
| Hook closure | 24 primary/reference projections |
| Installer previews | Tám surfaces, 39 skills + sáu agents, project bytes unchanged |
| Preservation | 509 protected hashes unchanged; installed r25 và bốn legacy bundles giữ nguyên |

[Full suite](../runs/nckh-native-261005-0005-r34-attempt-01/deterministic-r34-attempt-01.json), [archives](../runs/nckh-native-261005-0005-r34-attempt-01/archive-summary.json), [extracted observations](../runs/nckh-native-261005-0005-r34-attempt-01/smoke-summary.json), [previews](../runs/nckh-native-261005-0005-r34-attempt-01/installer-previews.json) và [preservation](../runs/nckh-native-261005-0005-r34-attempt-01/final-preservation.json) cùng bind current r34. Không có overall deadline tùy ý; individual test timeouts giữ nguyên.

## Native r34: AGY

AGY CLI `1.2.16` dùng `gemini-3.8-flash-medium`, effort medium, `--dangerously-skip-permissions` trong project thử riêng theo human grant. [Verified native archive chain](../runs/nckh-native-261005-0005-r34-attempt-01/native-package-chains.json) có cùng bundle closure với final build.

[Ba native file cases](../runs/nckh-native-261005-0005-r34-attempt-01/agy-native-file-summary.json) đạt:

- Allowed `write_to_file`: tool DONE, marker được tạo, hook trả `ask`.
- Protected `write_to_file`: native tool ERROR `private-holdout-credential-path`, target vẫn absent.
- Protected `view_file`: native tool ERROR cùng reason; seeded test marker giữ nguyên hash.

[Project + workspace plugin](../runs/nckh-native-261005-0005-r34-attempt-01/agy-native-workspace-plugin-summary.json) có hai callbacks cùng session/step/tool, một policy receipt, một actual `run_command` DONE và một marker. Plugin nằm trong project thử, không cài global. Đây là các tool/version/surface observations trên; remaining native tools và IDE evidence còn thiếu.

[Event fault matrix r34](../runs/nckh-native-261005-0005-r34-attempt-01/agy-native-event-fault-summary.json) ghi **25** attempts, status `recorded-genuine-callbacks`. Mỗi fault được chèn sau callback thật; không claimed native host tự sinh malformed/unsupported events. Five faults: malformed input/output, timeout, crash, unsupported selected codec. Tệp thực và callbacks bind riêng từng attempt.

| Selected event | Recorded attempts | Attempts tạo marker |
|---|---:|---:|
| PreInvocation | 5 | 5 |
| PreToolUse | 5 | 0 |
| PostToolUse | 5 | 5 |
| PostInvocation | 5 | 5 |
| Stop | 5 | 5 |

[Native tool states và actual callback order](../runs/nckh-native-261005-0005-r34-attempt-01/agy-native-event-timing.json) xác nhận five PreToolUse fault cases có actual tool ERROR và marker absent. Bốn PostToolUse faults (malformed output/timeout/crash/unsupported selected codec) có tool ERROR sau khi marker đã tạo; PostToolUse malformed input và fifteen PreInvocation/PostInvocation/Stop cases có tool DONE với marker được giữ. PreToolUse trước tool, PostToolUse sau tool. PreInvocation/PostInvocation bao quanh từng model invocation; trong các turns này có callbacks cả trước và sau tool. Stop sau final response. Mô tả `effect_timing` ban đầu trong raw summary quá rộng; diagnostic giữ original hash và sửa interpretation, không ghi đè raw receipts. [Initial collector assertion failure](../runs/nckh-native-261005-0005-r34-attempt-01/event-timing-collector-initial-failure.json) giữ việc giả định mọi non-pretool state DONE bị bác bỏ bằng actual stream. Marker tồn tại khi post hook lỗi không tự chứng minh prevention failure. Bảng không gọi mọi absence là policy deny hoặc mọi model exit0 là successful tool execution.

## Native r34: Cursor

Cursor CLI `2026.09.15-d2fe57e` dùng selector `grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]`, `--force --trust --sandbox disabled` trong project thử riêng. Historical native init xác nhận Grok 4.7 500K Extra High; callbacks hiện ghi base model `grok-4.7`. Metadata chưa là backend attestation hoặc billing receipt.

| Case | Callback/receipt | Native tool và tệp |
|---|---|---|
| [Allow](../runs/nckh-native-261005-0005-r34-attempt-01/projects/cursor-model/attempts/allow-01.json) | sessionStart/preToolUse/postToolUse; một pretool/policy receipt | Shell completed, marker được tạo |
| [Project + transient plugin duplicate](../runs/nckh-native-261005-0005-r34-attempt-01/projects/cursor-model/attempts/duplicate-01.json) | Hai same-tool pretool callbacks, runner exit0/JSON hợp lệ, một policy receipt | Native host báo `Hook script timed out after 20000ms`, marker không tạo |

Duplicate timeout lặp lại từ r31 trên current r34. CLI exit0 và final response không chứng minh tool thành công; raw native tool rejection giữ nguyên. Chưa có nguyên nhân đủ evidence để sửa host hoặc gọi duplicate route qualified. `beforeSubmitPrompt`/`stop` chưa có callback trên print route này. Wrapper baseline 20s/fault2s/sleep8s là harness; public template5s chưa có production timing qualification.

## Historical r31 matrix

Các receipts dưới đây giữ đúng source r31; không regrade thành r34 sau runner repair.

| Case | Cursor tạo marker | AGY tạo marker |
|---|---:|---:|
| allow | Có | Có |
| policy-deny | Không | Không |
| malformed-input | Không | Không |
| malformed-output | Không | Không |
| timeout | Không | Không |
| crash | Không | Không |
| unsupported-codec | Không | Không |
| uncovered-tool | Không | Có |
| duplicate | Không | Có |

Fault cases là controller injection sau genuine native callback, selected ở PreToolUse; host không tự phát malformed/unsupported events. Uncovered AGY ghi manual/ask rồi thực thi; uncovered Cursor có native timeout, owned process termination sau 270 giây. R31 AGY duplicate chỉ là hai project groups; project/workspace-plugin duplicate được quan sát ở r33/r34. Historical Claude/Codex evidence giữ trong [r30 checkpoint](./delivery-261004-1707-r30-native-checkpoint.md), [prompt faults](./delivery-261004-1707-r30-prompt-failures.md) và [model/tool observations](./delivery-261004-1707-r30-model-tools.md).

## Cleanup và gates còn mở

Current r34 gỡ **82** matching config/payload/plugin files; cộng r31/r33 là **164**. Hai project hooks đều không callable, protected global config hashes unchanged. [Final process audit](../runs/nckh-native-261005-0005-r34-attempt-01/final-process-audit.json) không có matching task process. Native conversation/trust history, archived packages, callbacks, policy receipts, oracles và failures được giữ.

Task native vẫn unchecked. Claude còn model/tool oracle và các events khác; chưa có configured approved-GPT route quan sát được ở Claude. Codex còn duplicate/other-event/protected-path gaps và bốn observed failure cases fail-open. Cursor còn timeout anomaly và events thiếu; AGY event faults giữ actual status ở trên, remaining native tools/surfaces và production timing còn mở. Codex Desktop/IDE, Cursor IDE, AGY IDE chưa có direct application receipts. Advertised targets giữ nguyên. Owner acceptance chỉ bind hai mẫu r29 đã đọc; quality/scientific/stable/install/release gates không tự đóng bằng các kiểm tra cấu trúc hoặc subset native.
