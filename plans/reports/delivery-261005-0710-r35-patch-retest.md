# Delivery r35 — native patch-path repair

## Current candidate

Current **r35/281 pins**, canonical source-lock hash `4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255`. [Structured bindings](./delivery-261005-0710-r35-patch-retest.json) bind actual local results, source/package/command/callback hashes, markers, cleanup and process audit. Plan remains **in-progress, 44/45**; the full native event/version/surface task stays unchecked.

## Local checks completed

| Check | Actual result |
|---|---|
| Deterministic | 190 tests successful, 1 Windows symlink skip; 645.312 seconds |
| Inventory | Exact 39 identities / 156 base cases / 19 families / 9 resources |
| Packaging | Four reproducibility variants; 16 builds/archives/extractions |
| Extracted behavior | 216 resource reads; 48 OFF writer no-read observations; 24 hook projections |
| Installer previews | Eight surfaces; each 39 skills + six agents; project bytes unchanged |
| Preservation | 509 protected hashes; installed r25 and four legacy bundles retained |

The [pipeline receipt](../runs/nckh-native-261005-0710-r35-attempt-01/revalidation-summary.json) records six successful stages. Public resource access remains ON; OFF bundles are internal comparisons. Local counts do not provide scientific/human/full-native acceptance.

## Genuine native apply_patch retest

Codex CLI **0.154.0 exec**, GPT-5.6 Luna medium, dangerous native flags within the existing grant. The already trusted r34 file scratch project was reused with a new evidence namespace and verified r35 payload. No new workspace trust key or global hook/config bytes changed. Each PreToolUse callback reported `apply_patch` and an exact command hash matching the requested patch; no fault injection was used.

| Attempt | Policy | Marker created | Completed file-change items |
|---|---|---|---:|
| r35-file-allow-01 | allow | Có | 1 |
| r35-file-policy-deny-01 | block | Không | 0 |
| r35-file-protected-01 | block | Không | 0 |
| r35-file-uncovered-01 | manual | Có | 1 |

The protected private-path attempt returned `private-holdout-credential-path`, with no completed file change and no marker. The following eight genuine attempts exercise update/delete/move and a mixed public/private add patch. Synthetic input files were created by the controller before native calls; actual before/after hashes, tool items and callbacks were retained.

| Native patch operation | Policy | Completed file-change items | Observed files |
|---|---|---:|---|
| update-allow | allow | 1 | Đúng thay đổi |
| update-private | block | 0 | Không đổi |
| delete-allow | allow | 1 | Đúng thay đổi |
| delete-private | block | 0 | Không đổi |
| move-allow | allow | 1 | Đúng thay đổi |
| move-private-source | block | 0 | Không đổi |
| move-private-destination | block | 0 | Không đổi |
| mixed-add-private | block | 0 | Không đổi |

Public update/delete/move performed the requested changes. Private update/delete, moves with a private source or destination, and mixed public/private add were blocked before any requested change. Native command hashes matched each requested patch exactly. These observations cover the tested canonical envelopes; shell targets, other tools and other surfaces retain their pending/manual status. Backend model/billing attestation was not observed.

[Historical r34 failure](./delivery-261005-0658-r34-codex-file-failure.md) retains the private marker and original receipts. R35 reads canonical patch headers; three regressions had 22 failures before repair and 12 focused tests passed afterward. The r34 failure has not been regraded.

## Trust correction and cleanup

[Trust correction](../runs/nckh-native-261005-0052-r34-codex-attempt-01/trust-report-correction.json) distinguishes native-persisted workspace trust from invocation-only hook-definition bypass; original report/helper/document preimages remain. The normal UI trust action was rejected and did not run, while the subsequent native CLI route did persist its own project trust.

[Cleanup helper review](../runs/nckh-native-261005-0658-r34-codex-file-attempt-01/cleanup-helper-review.json) found and repaired a static variable-shadowing defect that could direct a receipt write at the global hooks file. The global file retained its `hooks` structure; no overwrite was observed. The retained trace does not prove this defect caused the earlier CPU stall. Historical reconciliation receipts are unchanged.

[R35 native cleanup](../runs/nckh-native-261005-0710-r35-attempt-01/native-codex-file/cleanup.json) removed 26 matching payload files, retained native evidence, and verified 81 historical project member hashes plus raw global config/hook hashes. [Final process audit](../runs/nckh-native-261005-0710-r35-attempt-01/final-process-audit.json) found zero matching task processes. Review was inline; no independent reviewer is claimed.

[Operation cleanup](../runs/nckh-native-261005-0710-r35-attempt-01/native-codex-patch-ops/cleanup.json) separately removed its 26 matching payload members and verified 152 historical project hashes plus unchanged raw global config/hook hashes. All fixtures, native outcomes and failures remain.

## Remaining requirements

Claude needs an owner-authorized model/effort for model/tool and other event observations. Codex project/plugin duplicate, shell targets and other tools, Cursor CLI prompt/stop/file routes and timeout diagnosis, remaining AGY tools/timing, and direct Desktop/IDE receipts remain pending. Production timing and stable/scientific/install/release acceptance are separate. Owner VI/EN acceptance remains bound to the exact two r29 samples.
