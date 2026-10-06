# R37 Cursor fresh packaged controls, attempt15

## Native outcomes

[Verified bindings](./delivery-261005-1700-r37-cursor-packaged-controls.json) record two prompt submissions/two model turns using a freshly built r37 Cursor bundle with resource-access ON. Source-lock hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb`, staged payload member hashes and config producer/definition are bound. The producer's default preToolUse20s/failClosed=true is used directly; other packaged handlers5s. No packaged-event observer or fault injection.

Cursor CLI `2026.09.15-d2fe57e` TUI displays Grok4.7 500K Extra High/MAX/Run Everything; exact granted selector remains Grok4.7/context500k/reasoning_effortxhigh/fast=false. Backend/billing attestation is not observed.

| Control | Observed outcome |
|---|---|
| Public auto Read→edit | Neutral policy hashes match Read and Write pre/post; Write allow and exact requested bytes observed; zero native failure callbacks |
| Plan-only Read→edit | Read allow/post pending; Write preflight block `plan-only-mutation`; actual selected-path Write failure callback reports permission_denied/plan-only-mutation; file unchanged |

Public fixture hash changes `33280328b2ce86d1557423aed843394f4b7cc4bdc10708dd4e7c93679ceb2a61` → `161bfac78370186c35763f6b595ae411b07d7a9950e0cf70f9ab8cc017df4c59`; deny preserves exact latter hash. Both final markers and Stop observed. Artifact QA remains pending; native policy receipts omit tool-use IDs, so matching is bounded neutral-event hash plus actual selected-path failure ID/version/tool. This fresh observation is r37-bound; r36 failures are unchanged historical evidence.

## Capture và cleanup

Raw allow and deny terminal chunks are truncated; retained tails/final markers, receipt bytes and artifact hashes were verified independently. The initial deny collection preceded final marker/Stop; its running observation is preserved, then terminal continuation is reconciled without a second prompt/model turn. No raw chunks were lost to the64KB save limit in this batch; raw model frames/tool-return contents remain unretained.

Matching-byte cleanup removes26 config/payload members, preserves626 historical project members, and final process audit reports zero matching/zero tracked-live. Native exit requests/graceful128 followed exact-PID/creation force0; harness exit1 retained. Protected global hook/MCP/plugin hashes unchanged; CLI-owned hashes recorded separately and controller direct-write=false. No installed update or publication; controller does not write the trust store. Hash changes do not identify the native-owned fields that changed.

## Remaining acceptance

This verifies selected public Write and plan-only preventive Write denial using the r37 packaged default. Private mutation, unsupported routes, remaining failure/events and Desktop/IDE surfaces still need their own native evidence. Full P3 task remains unchecked and plan44/45. Exact r29 VI/EN owner acceptance, installed r25 and scientific/stable/release gates stay separate.
