# R36 Cursor direct5s native Read failure, attempt 12

## Native failure đã quan sát

[Verified bindings](./delivery-261005-1550-r36-cursor-direct-failure-observer.json) ghi một prompt/một Read request/một model turn trên Cursor CLI `2026.09.15-d2fe57e`, đúng Grok4.7/500k/xhigh/fast=false. Năm packaged handlers giữ direct invocation và timeout5s. Chỉ thêm diagnostic `postToolUseFailure` handler timeout10s; logger không gọi policy, không đọc transcript và chỉ giữ bounded scrubbed error cho đúng synthetic Read path.

Actual `postToolUseFailure` callback có Read/path/version/tool-use ID đúng selected request, `failure_type=permission_denied`, `is_interrupt=false`. Native error chỉ rõ **preToolUse hook timed out after5000ms**, bị chặn do `failClosed`. Bounded neutral-event hash của policy receipt khớp Read/allow. Policy tính allow không chứng minh native cho phép công cụ chạy thành công.

Đây là bằng chứng nguyên nhân timeout cho **selected Read của ca12**. [Direct08](./delivery-261005-1340-r36-cursor-direct-interactive.md), [existing09](./delivery-261005-1415-r36-cursor-existing-mutations.md) và [direct11](./delivery-261005-1523-r36-cursor-direct-sequence.md) thiếu actual failure response tương ứng; không retroactively gán cùng nguyên nhân.

## Observations và giới hạn

Ba case receipts là advisory/preflight/stop, thêm một startup advisory. Model final marker được giữ; zero postToolUse/pre-delivery receipts. Read thất bại; fixture byte-identical trước/sau. Một terminal chunk truncated; raw model frames/tool-return content không được giữ.

[Local timing controls](../runs/nckh-native-261005-1550-r36-cursor-direct-failure-observer-attempt-12/local-runner-timing.json) ghi ba synthetic subprocess executions khoảng0.109–0.125s, zero model turns. Các controls này không đo native scheduling/process overhead hoặc giải thích toàn bộ timeout, không qualify production timing.

## Cleanup và remaining gates

Cleanup gỡ26 matching config/payload members, giữ565 historical members và toàn bộ native failure evidence. Sau native exit requests, graceful stop exit128 và exact-PID/creation force-stop exit0; final audit zero matching/zero tracked-live, harness exit1 giữ nguyên. Protected global config hashes không đổi; CLI-owned state hashes được ghi riêng, controller direct-write=false.

[Fresh AGY window observation](../runs/nckh-native-261005-1550-r36-cursor-direct-failure-observer-attempt-12/agy-window-continuation.json) vẫn có zero AGY-owned windows; cửa sổ mang title Antigravity thuộc app ID Codex. Không app input được gửi; access/unlock đã được user cấp và không cần xin lại. Claude model/effort selection và direct app surfaces/matrix còn pending.

Source r36/281 pins/canonical lock `1a471686c5b1e89e6838957161a8ae4c6787d46d227420d8644636062da90d30` giữ nguyên; timeout20s chỉ là candidate control riêng trước khi sửa source default. Full native gate unchecked, plan44/45. Installed r25, owner samples và scientific/stable/release không đổi.
