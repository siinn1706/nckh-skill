# R37 Cursor preToolUse: five native Read failure observations

[Verified bindings](./delivery-261005-1755-r37-cursor-preflight-faults.json) bind five prompt submissions, five final reply markers and five distinct native tool-use IDs on Cursor CLI2026.09.15-d2fe57e, Grok4.7/context500k/xhigh/fast=false. Source remains r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb`. These cases use the verified extracted r37 ON package and an explicit preflight fault observer; they do not replace the direct packaged controls15 or the private editing limit16.

## Actual native response

| Declared injection after genuine preToolUse/Read callback | Native selected-path result | Successful selected Read/post receipt |
|---|---|---|
| Malformed runner input | permission_denied / hook-input-or-context-invalid | 0 |
| Malformed hook output | permission_denied / invalid JSON, failClosed | 0 |
| Sleeper24s | permission_denied / timed out after20000ms, failClosed | 0 |
| Observer crash exit17 | permission_denied / exit17, failClosed | 0 |
| Unsupported selected codec event | permission_denied / runner exit3, failClosed | 0 |

Each selected failure has a matching actual callback tool-use ID, version, Read tool and synthetic public path. The preflight outer bound remains20s/failClosed=true; observer inner runner limit5s, other direct packaged handlers5s, diagnostic failure callback10s. The timeout observer completes after24.148938s with an allow receipt; native still rejects the Read at its20000ms limit. Policy output alone does not establish native permission.

Unsupported-codec injection selects an unknown codec event after a genuine supported native callback. It does not establish native unsupported-event/tool admission behavior. Fault origin remains controller-injection-after-genuine-callback for every case. The diagnostic failure collector itself adds no policy or tool action. Public fixture bytes remain unchanged and every final reply marker is observed; raw native tool-return content is not retained and terminal chunks are bounded/truncated.

## Collector and cleanup evidence

The first collector assertion rejected the malformed-input degraded receipt because it lacks context_hash. [Failure receipt/preimage](../runs/nckh-native-261005-1755-r37-cursor-preflight-faults-attempt-17/collector-attempt-01-failure.json) retains the error and the unsuccessful next selection before any second prompt intent. The corrected collector keeps degraded parse receipts without a context-hash claim, binding them through the selected genuine callback/control/runner and actual failure ID. Normal receipts still require exact context hashes. No model prompt is resubmitted.

Matching-byte cleanup removes26 config/payload members and preserves673 historical project members. Native double interrupt and graceful stop exit128 leave the owned root; exact PID/UTC creation checks precede force-stop across five tracked processes. Harness exit1 remains recorded. Final audit has zero matching/zero tracked-live; AGY stays open. Protected global hook/MCP/plugin hashes are unchanged, CLI-owned state hashes differ, controller direct-write=false. Hash changes do not identify changed fields.

## Remaining acceptance

Plan stays in-progress44/45, P3 active, full native task unchecked. These are scoped preToolUse/Read fault observations. Actual private Write remains unqualified, alongside remaining event/tool/version/surface and project/plugin duplicate matrices. Claude model/effort selection and AGY window/capture recovery remain pending. Exact r29 VI/EN samples, installed r25 and scientific/stable/release/publication retain their separate gates; no source or local test/build counts are regraded.
