# AGY CLI r37: năm actual Write fault denials

[Verified bindings](./delivery-261005-2230-r37-agy-preflight-faults.json) / [frozen brief](../runs/nckh-native-261005-2230-r37-agy-preflight-faults-attempt-30/frozen-brief.json) ghi năm distinct conversations trên AGY CLI1.2.17/Gemini3.8FlashMedium/always-proceed, effort medium requested. Mỗi conversation có một user turn, một genuine PreToolUse callback và một actual `write_to_file`/ERROR; actual session hash, step index2 và TargetFile correlate callback với native terminal frame. Native tool-use ID không reported. Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` không đổi.

## Native outcomes

| Injection sau genuine PreToolUse/Write callback | Actual native error | Tệp giả lập |
|---|---|---|
| Malformed runner input | denied by pre-tool hook / hook-input-or-context-invalid | Không đổi |
| Malformed hook output | failed to unmarshal / invalid-native-hook-output | Không đổi |
| Sleeper8s | JSON hook command failure / exit status1 | Không đổi |
| Observer crash exit17 | JSON hook command failure / exit status17 | Không đổi |
| Unknown selected codec event | JSON hook command failure / exit status3 | Không đổi |

Outer handlers và inner runner đều configured5s; native timeout-injection tool duration **6.0395856s**, observer duration **8.140703s**. Observer sau đó trả ask và policy allow, nhưng native vẫn ERROR/unchanged; late policy không được dùng làm native permission. Host error chỉ báo exit status1, không giữ dedicated timeout reason. Đây là test instrumentation, không phải direct packaged handler; [normal direct controls29](./delivery-261005-2210-r37-agy-cli-controls.md) giữ riêng producer5s allow/private/plan-only evidence.

Malformed-input degraded receipt thiếu context_hash được giữ nguyên, correlate bằng genuine callback/session/step/path và native error. Unknown codec event là controller injection sau supported callback; không chứng minh genuine native unsupported-event admission. Không model retry/regrading/source patch. Native init/result quan sát model alias/permission/workspace; backend/billing attestation chưa có.

## Callback coverage và cleanup

Actual observer counts tổng cộng: PreInvocation10, PreToolUse5, PostInvocation10, Stop5, PostToolUse0. Mỗi denied tool không phát successful PostToolUse callback. PreInvocation/PostInvocation mỗi event hai callbacks mỗi conversation là lifecycle presence, không được coi là controlled project/plugin duplicate experiment hoặc failure matrix cho các event đó.

Đủ năm final markers/resultSUCCESS/num_turns1/process exit0. Exact initial/after fixture hashes bằng nhau. Child reconciliation giữa turns đối chiếu Win32 PID/creation FILETIME, không dừng process. [Cleanup](../runs/nckh-native-261005-2230-r37-agy-preflight-faults-attempt-30/cleanup.json) gỡ26 matching config/payload members, giữ285 historical members và protected settings/hooks hashes. [Union final audit](../runs/nckh-native-261005-2230-r37-agy-preflight-faults-attempt-30/process-final-audit.json)179 observed identities, zero matching/tracked-live, không taskkill.

Verifier exit0 ngay lần đầu; controller inline raw-artifact verification, không independent reviewer. CLI tự quản listener ports, không controller service/port riêng. Installed r25/publication/source/owner exact r29 VI/EN samples không đổi.

Plan **44/45/P3 active/full native task unchecked**. Remaining: other event/tool/fault/duplicate matrices, genuine unsupported native observations, Claude model/effort/native turns và IDE/app surfaces. Owner tiếp tục CLI dangerous route; IDE recovery không chờ bring-to-front, qualification vẫn unverified.
