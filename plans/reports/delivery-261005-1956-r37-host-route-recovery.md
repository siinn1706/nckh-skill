# R37 — AGY window recovery và bounded Cursor route inspection

## AGY

Fresh Computer Use app/window inventory cho thấy `Google.Antigravity` và `electron.app.Antigravity` đang chạy nhưng không có owned targetable window. Window có title “Antigravity” vẫn thuộc `OpenAI.Codex_2p2nqsd0c76g0!App`; title không đủ để đổi owner hoặc gửi input.

Thử đúng một supported `launch_app` với app id đã returned `Google.Antigravity`, rồi refresh inventory. Launch trả về thành công nhưng vẫn **zero AGY-owned candidates**. Không capture hoặc nhập vào window do Codex sở hữu. AGY IDE native evidence vẫn pending/unverified; access/unlock grants đã có được giữ, không có permission gate mới.

Process snapshots trước/sau launch khớp cả sáu PID/parent/UTC creation/executable identities. Root44132/creation `2026-10-05T02:09:07.8897790Z` được giữ; **zero new processes**, không dừng process nào.

## Cursor

Read-only installed-source inspection giữ bounded contexts từ đúng `index.js` hash `9f51ecf275d932372bf367914708b0dd21bf9c9e807b5e20e789ec9e247d9f86`. Giữ8/10 occurrences của executeHookForStep, tối đa8 contexts/pattern; không evaluate hoặc sửa vendor code, không trigger native callback. Kết quả chưa xác định được nguyên nhân thiếu plugin prompt/stop callback. Missing regex match không chứng minh method absent.

[Native alias21](./delivery-261005-1930-r37-cursor-plugin-alias-controls.md) vẫn giữ hai duplicate cells unqualified; không rerun model prompt hoặc thay oracle từ các text contexts này. Source kit r37 và plan44/45/full native gate unchecked được giữ.

## Evidence

- [Verified summary](../runs/nckh-native-261005-1956-r37-host-route-recovery-attempt-22/host-recovery-summary.json)
- [Before inventory](../runs/nckh-native-261005-1956-r37-host-route-recovery-attempt-22/agy-inventory-before-launch.json), [launch](../runs/nckh-native-261005-1956-r37-host-route-recovery-attempt-22/agy-launch-recovery.json), [after inventory](../runs/nckh-native-261005-1956-r37-host-route-recovery-attempt-22/agy-inventory-after-launch.json)
- [Before process identities](../runs/nckh-native-261005-1956-r37-host-route-recovery-attempt-22/agy-process-before-launch.json), [after process identities](../runs/nckh-native-261005-1956-r37-host-route-recovery-attempt-22/agy-process-after-launch.json)
- [Bounded source contexts](../runs/nckh-native-261005-1956-r37-host-route-recovery-attempt-22/cursor-native-routing-contexts.json)
