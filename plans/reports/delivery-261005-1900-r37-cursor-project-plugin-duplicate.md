# Cursor r37 — native project/plugin duplicate callbacks

## Kết quả đã kiểm chứng

Một interactive model turn trên Cursor CLI `2026.09.15-d2fe57e`, đúng `grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]`. Một minimal controller test plugin được nạp bằng `--plugin-dir`; manifest/hook layout dựa trên [Cursor plugin reference](https://cursor.com/docs/reference/plugins), flag được xác nhận trong [installed CLI help](../runs/nckh-native-261005-1900-r37-cursor-project-plugin-duplicate-attempt-19/commands/cursor-local-plugin-help.json). Đây là test plugin gọi cùng verified packaged runner với project hook; không phải native acceptance của toàn bộ kit plugin.

| Event | Project callbacks | Plugin callbacks | Policy receipts | Native duplicate result |
|---|---:|---:|---:|---|
| sessionStart | 1 | 1 | 1 | Verified |
| beforeSubmitPrompt | 1 | 0 | 1 | Unqualified |
| preToolUse | 1 | 1 | 1 | Verified |
| postToolUse | 1 | 1 | 1 | Verified |
| stop | 1 | 0 | 1 | Unqualified |

Tổng **8 actual callbacks / 5 policy receipts**. Ba cặp verified khớp native input hash, session hash, tool ID/name, version và runner output; mỗi cặp tạo một receipt duy nhất. Pre/post khớp một native Read ID và exact public synthetic path; fixture bytes giữ nguyên, final marker và project Stop receipt observed. Không inject fault hoặc retry prompt. Hai plugin callbacks còn lại không observed trong invocation này; không suy thành unsupported cho mọi version/surface.

## Timing, closure và cleanup

Outer preToolUse20s/failClosed=true, các event khác5s; observer forwards genuine bounded payload tới staged pinned r37 runner với inner bound5s. Observer có source/hash riêng, không được mô tả là direct packaged handler. Artifact QA remains separate/pending; raw terminal có truncation, native tool-return content không retained.

Cleanup gỡ **28 matching owned members**, gồm project config, 25 staged payload members và hai plugin definition files; **727 historical members** preserved. Final audit có zero matching / zero tracked-live processes. Native exit requests được giữ, graceful stop exit128 rồi force stop đúng PID/UTC creation identity; interactive harness terminal exit1 được giữ sau model completion. AGY retained process không bị dừng.

Protected global configs giữ nguyên; CLI-owned state hash thay đổi không cho biết changed fields. Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` không đổi, current local checks được tái dùng. Full native gate, remaining event/tool/surface coverage, private Write và Claude model/effort remain open. Plan vẫn44/45; exact r29 VI/EN owner acceptance, installed r25 và scientific/stable/release/publication giữ scope hiện có.

## Evidence

- [Verified bindings](./delivery-261005-1900-r37-cursor-project-plugin-duplicate.json)
- [Original collected case](../runs/nckh-native-261005-1900-r37-cursor-project-plugin-duplicate-attempt-19/case-duplicate.json)
- [Verified native summary](../runs/nckh-native-261005-1900-r37-cursor-project-plugin-duplicate-attempt-19/native-duplicate-summary.json)
- Definition hashes (historical evidence path: `../runs/nckh-native-261005-1900-r37-cursor-project-plugin-duplicate-attempt-19/definitions/session.json`; unavailable in the cleaned checkout)
- [Cleanup](../runs/nckh-native-261005-1900-r37-cursor-project-plugin-duplicate-attempt-19/cleanup.json) và [process audit](../runs/nckh-native-261005-1900-r37-cursor-project-plugin-duplicate-attempt-19/final-process-audit.json)
