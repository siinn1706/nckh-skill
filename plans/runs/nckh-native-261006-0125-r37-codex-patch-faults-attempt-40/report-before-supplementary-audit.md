# Codex CLI r37: canonical patch fault observations

Verified bindings (historical evidence path: `./delivery-261006-0125-r37-codex-patch-faults.json`; unavailable in the cleaned checkout) bind five native apply_patch requests on Codex CLI0.154.0/exec, GPT-5.6Luna requested/medium. Callbacks report the model; effort/backend attestation is absent. Source r37/281 pins/hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb` unchanged. Each actual command hash matches the exact requested canonical public add-file patch. No alternative tools or model retries.

## Observed behavior

| Selected PreToolUse fault | Packaged/native observer output | Native file outcome |
|---|---|---|
| Malformed input | permissionDecision deny; block/hook-input-or-context-invalid | No file change, no marker, no post callback |
| Malformed output | Declared invalid native JSON | One completed add-file; exact marker |
| Timeout | Sleeper8s with outer5s; sleep snapshot, no selected preflight receipt | One completed add-file; exact marker |
| Crash | Intentional observer exit17 | One completed add-file; exact marker |
| Unsupported selected codec | Runner exit3/empty native JSON; deterministic block receipt | One completed add-file; exact marker |

These observations establish a scoped deny for malformed input and continued mutation for four other fault modes. Retained exec JSON does not expose native hook notification states; actual callback/file-change items and bytes are verified. The unsupported selected codec is injected after a genuine known native PreToolUse callback; genuine unsupported native-event delivery remains unqualified. PostToolUse artifact QA remains a separate pending check.

Five completed turns/final markers/native process exits0;24 callbacks/21 policy receipts. Outer and inner handlers5s, injected sleeper8s, no whole-turn deadline. Inline sessionFlags reuse the existing native-trusted scratch project and hook trust bypass for the invocation. No new project trust keys; raw global config/hooks hashes unchanged. Native plugin-catalog warmup/authentication warnings remain in stderr, without a plugin duplicate qualification claim.

Cleanup removes26 matching staged payload members and preserves451 historical files. Four synthetic marker artifacts and native observations are retained. Native40 audit binds1145 PID/creation FILETIME identities, zero matching/tracked-live/no taskkill. Later read-only CLI help commands are retained separately and require the final supplementary audit. AGY CLI help was read with zero model prompts; it writes its help on stderr and documents the already selected dangerous/print route. Codex plugin help exposes marketplace add/list/remove management; no marketplace addition or plugin installation was performed.

Full native task stays **unchecked/44 of45/P3 active**. Remaining actual event/tool/fault and project/plugin cells, Claude model/effort/native turns, genuine unsupported event and direct application qualification remain open. Exact r29 owner VI/EN samples and installed r25 boundaries retained. Review was inline; no independent reviewer.
