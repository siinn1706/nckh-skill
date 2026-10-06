# Cursor workspace route: native duplicate observations

[Verified bindings](../runs/nckh-native-261006-0240-r37-cursor-workspace-duplicates-attempt-44/verified-duplicate-observations.json) record one interactive Cursor CLI2026.09.15-d2fe57e turn using the existing Grok4.7/500k/xhigh/fastfalse selection. Fresh workspaceOpen output and a genuine project/plugin sessionStart pair were verified before the single model prompt. One Write was requested; no model retry or alternative route was submitted.

## Actual callbacks

| Event / tool | Project | Plugin | Same-input pair / receipts |
|---|---:|---:|---|
| sessionStart | 1 | 1 | One pair / one receipt |
| beforeSubmitPrompt | 1 | 0 | Missing plugin / one receipt |
| preToolUse Read | 1 | 1 | One extra pair / manual/tool-route-uncovered |
| preToolUse Write | 1 | 1 | One pair / allow |
| postToolUse Write | 1 | 1 | One pair / pending artifact QA |
| stop | 1 | 0 | Missing plugin / one receipt |

One additional workspaceOpen diagnostic callback returned the owned plugin path. Total11 callbacks,10 forwarded packaged-policy callbacks, four same-input project/plugin pairs and six receipts in per-event instrumented namespaces. The Read callbacks share the Write ID and exact public marker path; an independent model Read request is not established. Read scope remains manual; this is not a general Read enforcement claim.

## Frozen oracle remains failed

The all-five-event duplicate oracle did not pass: beforeSubmitPrompt and stop still have no plugin callback; the extra Read preflight yields six instead of five receipts. The actual Write marker contains CRLF while the frozen requested bytes specify LF. Exact marker-byte comparison stays failed. No expected-byte correction or regrading was applied after the run.

The matching Write pre/post ID, requested path and one changed public marker establish a scoped actual mutation. The final reply marker was observed in a later terminal poll. PostToolUse returned pending/artifact-final-bytes-missing-or-stale after mutation; scientific/artifact QA is unverified. Exit0 does not establish the frozen oracle or four-host parity.

Both handlers and inner runner use5s in this instrumented duplicate control; default enforcement and fault-mode behavior are separate. Native19/21 failures remain intact. Native43 proves workspace loading, while this new route still does not supply the two missing plugin event callbacks. A repeat requires new causal evidence, not a different marker expectation.

Native /exit and monitor ended exit0. Matching cleanup removed32 owned members, preserved867 historical files and retained the failed marker,11 observations and six receipts. Final union1803 PID/creation identities had zero matching/tracked-live/no process stop. Protected global hook/MCP/plugin hashes stayed exact; CLI-owned state hashes are retained without inferring changed fields. Controller global direct writes=false.

Source r37/281 pins/hash629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb unchanged. Full native task stays unchecked/44 of45/P3 active. Native41 cache/metadata authority, Claude model/effort selection, remaining event/tool/fault cells and direct IDE qualification remain open. Review was inline; no independent reviewer.
