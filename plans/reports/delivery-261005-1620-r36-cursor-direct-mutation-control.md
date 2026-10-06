# R36 Cursor direct preToolUse20s mutation controls, attempt14

## Kết quả

[Verified bindings](./delivery-261005-1620-r36-cursor-direct-mutation-control.json) ghi hai prompt/hai model turns trên Cursor CLI `2026.09.15-d2fe57e`, exact Grok4.7/500k/xhigh/fast=false. `preToolUse`20s, other packaged handlers5s; gọi trực tiếp packaged runner, không policy observer/fault injection. Diagnostic failure logger10s chỉ giữ bounded metadata cho selected synthetic file, không đọc transcript.

| Control | Policy và native effect |
|---|---|
| Public auto | Neutral hashes khớp Read rồi Write pre/post; Write allow, exact requested bytes được ghi; zero native failure receipt |
| Plan-only | Read allow/post pending; Write preflight block `plan-only-mutation`; actual failure callback Write/version/path/tool-use ID với permission_denied và error `plan-only-mutation`; file byte-identical trước/sau |

Public hash đổi `ad20f34a3554f11c34fdee1d2cf0b0c8484b375c002ed03b2e53fb35910841ef` → `9eeb68c638fe89741028a9ff2e3d1b083a19a0d55e36652629ebb53c29b47450`; deny giữ exact second hash. Hai final markers/Stop được giữ. Artifact QA pending; native policy receipts không giữ tool-use IDs, nên policy/native correlation là neutral-event hashes và actual selected-path failure record.

## Giới hạn và failures được giữ

Một allow raw terminal chunk không lưu được vì code vượt strict64KB auto-review limit. Recording-failure receipt (historical evidence path: `../runs/nckh-native-261005-1620-r36-cursor-direct-mutation-control-attempt-14/terminal-allow-poll-01-recording-failure.json`; unavailable in the cleaned checkout) giữ missing-evidence condition; native policy receipts/fixture hashes được giữ độc lập. Deny raw chunk truncated và đã lưu. Collector hai lần lỗi khi glob chọn receipt không có output và gọi hash helper không tồn tại; preimages/failure records và repaired collector được giữ, zero model retries.

Controls verify selected public Write effect và plan-only preventive Write denial với20s. Private mutation, full timing/failure/event/surface/version matrix vẫn pending. Không chấm5s failures thành PASS; source r36 default vẫn5s trong controls.

## Cleanup

Cleanup gỡ26 matching config/payload members, giữ596 historical members. Native exit requests/graceful128 rồi exact-identity force0; final audit zero matching/zero tracked-live, harness1 giữ nguyên. Protected global configs không đổi; CLI-owned state hashes ghi riêng, controller direct-write=false. Source r36/281 pins không đổi. Plan44/45, P3 unchecked; r29 samples/installed r25/scientific/stable/release không đổi.
