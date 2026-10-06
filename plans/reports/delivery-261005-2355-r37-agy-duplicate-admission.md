# AGY CLI r37: five-event project/plugin duplicate và config admission

[Verified bindings](./delivery-261005-2355-r37-agy-duplicate-admission.json) ghi hai distinct conversations trên CLI1.2.17/Gemini3.8FlashMedium/always-proceed/effort medium requested. Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` unchanged. Observer outer5s/inner5s; không fault injection/model retry/global plugin install.

## Project và workspace plugin

| Event | Actual callbacks | Matching same-input pairs | Policy receipts |
|---|---:|---:|---:|
| PreInvocation | 4 | 2 | 1 |
| PreToolUse | 2 | 1 | 1 |
| PostToolUse | 2 | 1 | 1 |
| PostInvocation | 4 | 2 | 1 |
| Stop | 2 | 1 | 1 |

14 genuine callbacks tạo bảy pairs. Mỗi pair có cùng native input SHA256, một source project và một source plugin; actual conversation hash, step index2 và TargetFile bind tool callbacks. Một native Write/DONE, đúng revised bytes/final marker/resultSUCCESS/num_turns1. Five policy files chứng minh idempotent receipt behavior; hai model-invocation cycles vẫn được phân biệt qua input hash, không gọi ordinary lifecycle repetition là controlled duplicate.

PostToolUse policy pending vì không declared artifact QA context; wire không rollback mutation. Callback duplication/receipt suppression không chứng minh scientific QA hoặc human acceptance. Native tool-use ID/backend/effort telemetry attestation absent; model alias and always-proceed are observed, medium bound to actual command.

## Unknown configured event

Second definition có `NckhUnsupportedNativeEvent` và five known event definitions. Native turn completes: seven known callbacks/five policy receipts, one Write/DONE/exact bytes/final marker, zero unknown callback. Không sửa runner input hoặc event sau supported callback. Đây là config-admission observation; không chứng minh host đã phát hoặc dispatch unknown native event, không tuyên bố full unsupported-event qualification.

## Cleanup và state

Two matching project-plugin files removed before second turn; final cleanup removes26 matching config/payload members, preserves950 historical files/protected settings-hooks hashes. Union897 PID/creation FILETIME identities: zero matching/tracked-live, no taskkill. Final native process exits0; no owned daemon/listener left. Controller direct global write/plugin install/source update not performed. Verifier first attempt exit0, inline artifact review/no independent reviewer.

Combined native34–37: **34 user turns / 31 actual native tool requests**. Original partial34/failed search35 oracles and repairs remain bound. Plan **44 of45/P3 active/full native task unchecked**. Remaining host/tool/surface matrices, unknown native event delivery, Claude model/effort/turns and direct app qualification remain explicit. Installed r25 and exact r29 owner VI/EN acceptance retain prior state.
