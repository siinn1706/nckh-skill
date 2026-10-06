# Direct skill development evaluation — completed for this project scope

## Final observed result — 2026-10-02, Asia/Saigon

All 37 installed skills received four concrete requests and all 148 cases were reviewed against the frozen checks. Six targeted diagnostic sessions repeated ten requests after recorded execution issues. The original corpus, first attempts and verdict history remain unchanged.

| Review view | Pass | Fail | Pending | Not reviewed |
|---|---:|---:|---:|---:|
| First round | 137 | 4 | 7 | 0 |
| Latest development observations | 147 | 1 | 0 | 0 |

| Group | Skills | Cases | Latest pass | Latest fail |
|---|---:|---:|---:|---:|
| Core | 10 | 40 | 40 | 0 |
| Engineer | 13 | 52 | 52 | 0 |
| Marketing | 13 | 52 | 51 | 1 |
| Xia tooling | 1 | 4 | 4 | 0 |

There are 42 completed native sessions and one retained timeout attempt, with no running sessions. Exit zero means completed execution; only the controller's separate case review supplies the verdict. These latest counts combine different recorded development conditions and are not an estimate of scientific quality, a baseline comparison or a blind routing success rate.

The remaining failure is `nckh-cro:positive`: the audit omits the present `noindex` metadata required by the frozen oracle. The original four failures and seven pending observations remain in history. No package source or installed content was changed to improve the score.

## Authority and scope

The user authorized: **“bạn sẽ trực tiếp ra thử prompt để test, trực tiếp tự test skill luôn, ngân sách vô hạn, phạm vi chỉ trong project này”**.

All task workspaces and raw traces for this evaluation are project-local. The controller authors prompts, invokes the installed skills through an actual Codex CLI, and reviews their observed outputs. This is exposed development evaluation by an agent, not human/domain acceptance or a protected holdout. Unlimited budget is authorization; actual billing remains unknown.

## Frozen inputs

- [Development corpus](../evaluation/direct-skill-tests/development-corpus.json): 37 identities × positive, outcome, negative and failure = 148 concrete requests; SHA256 `bbb6d312df45c4bad75bef5b5e8b5a42202dfcf0122382ee59e51ce84c63de84`.
- Inputs are agent-authored synthetic passages, source cards, local Python defects, CSV events, HTML, readiness records and hypothetical marketing briefs. They are explicitly labeled synthetic and owned for development use.
- Expected outcome checks were written before the full suite dispatched. They stay in the controller corpus and are not included in the performer prompts.
- The original 148 case definitions in `nckh-kit/evals/cases/` and their history remain intact. This version supplies concrete requests where older scenarios lacked necessary input text/data.
- Installed revision 14 is the performer’s subject. Source revision 18 and prior candidate/receipt records remain separate and unchanged.

## Native route and isolation

Observed executable: desktop `codex.exe`, `codex-cli 0.159.2`. Native `exec --json` receives prompts through stdin and inherits the selected `gpt-6.1-sol` / `max` configuration. Early sessions used `--ephemeral`; subsequent sessions retain full project-local rollouts. Persisted native `turn_context` records show `sandbox_policy.type: read-only`, `approval_policy: on-request` and `approvals_reviewer: auto_review`; scoped writes go through that native review route. The earlier workspace-write description was a controller assumption and is superseded by this actual observation. No force, permission bypass, hook trust bypass or global configuration mutation is used. Native context records the model/effort request; effective provider model/effort and billing remain unknown.

Each skill runs directly in one native session, with four separate scenario directories and permission boundaries. This is explicit skill invocation, not a blind routing evaluation. Scenarios share that skill session’s context; they are not independent random samples. The wrapper also states authorization/evidence boundaries, so success cannot isolate the skill’s contribution from the prompt or base agent. Other host/OS/surface and selective-delegation evidence remain untested by this route.

The project-only scope requires a project-local harness rather than the package’s generic runner contract, which requires an outside-project private store and separate human freeze references. The [native suite harness](../evaluation/direct-skill-tests/run-native-suite.py) records the actual grant and agent-only review protocol without fabricating those human references. Raw traces live in a sibling private area outside the task workspace and package source/dist. There is no claim of enforced blind read separation.

Owned child processes use the package’s Windows Job Object lifecycle. PID, command, workspace, timeout and cleanup status are retained per attempt. The selected native configuration was copied only into owned project-local runtime areas. All ten unchanged credential-bearing configuration copies were removed after process reconciliation; global configuration and authentication files were untouched. Raw rollouts, traces and artifacts remain available.

## Invocation pilot

The first local launch failed before model dispatch because the CLI rejects combining explicit `--sandbox` with `--approve-for-me`. That actual failure is retained. Removing the redundant option produced a real native run with observed skill/reference reads and four substantive writing answers.

The successful pilot took 396.75 seconds, returned exit 0, and emitted usage: 161,710 input tokens (132,224 cached input tokens), 6,492 output tokens, including 4,904 reasoning output tokens. Cached usage is a subset of the reported input; it is not an additional token total. Billing is unknown.

Controller review found that the pilot preserved `18/60`, `12`, August 2026, seconds, the exact protected quotation, the marker `[S1]`, noncausal scope and uncertainty. It rejected unsupported proof of increased accuracy for all students and handed new claim verification to `nckh-evidence`. This is an observed development result, not a human taste or scientific-validity verdict.

## Full suite evidence

The full development suite and recorded diagnostics have finished. Per-skill raw native events, stderr, prompts and receipts are retained in `plans/evaluation/direct-skill-tests/private/round-1/` and `round-2/`. Task outputs are in `plans/evaluation/direct-skill-tests/workspaces/round-1/` and `round-2/`.

The controller inspected actual answers, source changes, calculations and visual artifacts. A zero process exit alone remains `completed-unreviewed`, not a case pass or stable qualification. [Results](../evaluation/direct-skill-tests/results.md), [machine-readable aggregate](../evaluation/direct-skill-tests/results.json) and [hash-bound controller reviews](../evaluation/direct-skill-tests/controller-reviews.json) retain the observed evidence and limits.

## Execution corrections and observed limitations

The user subsequently instructed: **“không giới hạn thời gian cook là 15p nhé, task dài thì sao?”**. The project harness now defaults to no task deadline (`timeout_seconds: null`). Existing lanes were drained using owned, temporary dispatch reservations; their completed outputs were retained. Remaining scenarios ran without automatic time cuts, with progress and owned-process monitoring. The interrupted cook attempt remains `timeout-unknown`; its process group was closed and its partial artifacts remain available for inspection. The subsequent cook session completed after 1,201.094 seconds without a deadline. This change is documented in process policy record (historical evidence path: `../evaluation/direct-skill-tests/private/process-policy-change/policy-change.json`; unavailable in the cleaned checkout).

The persisted native catalog observation (historical evidence path: `../evaluation/direct-skill-tests/private/process-policy-change/native-catalog-observation.json`; unavailable in the cleaned checkout) captures 149 global AK identities and no NCKH identities in the host-supplied catalog of a nested, non-Git evaluation workspace. NCKH's own skill is explicitly loaded from its actual project file. Project-local `CODEX_HOME` therefore does not isolate the native catalog to the project kit. Earlier ephemeral outputs selected `ak-fix`, `ak-security` and `ak-email` where frozen checks expected project NCKH owners. These are recorded as scope/routing failures; the selected AK identities really exist. Earlier sessions have no retained complete catalog snapshot, so the new observation is evidence about the repeated native route, not a reconstruction of every prior session.

Diagnostic follow-ups explicitly constrained owner selection to the observed 37-skill project NCKH catalog. The original requests, expected checks and first-run verdicts stay intact; the changed execution condition is recorded per receipt. Follow-ups also retain complete project-local native rollouts to inspect calculation calls omitted by the compact `--json` event stream. A missing visible calculation call is unresolved provenance, not demonstrated fabrication.

Controller verification separately ran the real, unchanged two-test suite against the repaired `nckh-fix` failure-case output: both tests passed, exit 0, and fixture hashes were preserved. The performer had not run that scenario's tests under the wrapper's explicit local-program restriction. Controller receipt (historical evidence path: `../evaluation/direct-skill-tests/private/controller-checks/nckh-fix-failure/receipt.json`; unavailable in the cleaned checkout) preserves that distinction.

The final aggregate is [results.md](../evaluation/direct-skill-tests/results.md); [controller reviews](../evaluation/direct-skill-tests/controller-reviews.json) bind observed answers, traces and receipts by hash. The CRO positive case has a first-run coverage failure: its usable signup audit omitted the present `noindex` metadata required by the frozen check. That result is retained without silently changing the check or extending the skill's source responsibilities. Installed `nckh-seo` explicitly owns canonical/index controls; installed `nckh-cro` owns signup/conversion friction. This suggests a possible test-scope mismatch, but it does not erase the confirmed omission or establish an instruction-source defect. No source patch or oracle change was made.

## Diagnostic outcomes and retained history

The [original follow-up protocol](../evaluation/direct-skill-tests/followup-protocol.json) was frozen before its five sessions. A sixth session used a separate [Xia owner protocol](../evaluation/direct-skill-tests/followup-xia-owner-protocol.json), frozen after its first observed permission issue and before dispatch. Every diagnostic used the original request/checks, installed revision 14, no deadline and retained rollouts. No automatic retry or best-of-N selection was used.

| Skill / repeated cases | First observation | Later observed result |
|---|---|---|
| Cook / all four | 900-second timeout; no final four-case packet | 1,201.094-second completed packet; real failed reproduction, one-line repair, two passing tests; exact interactive plan/review hashes and downstream stop; debug handoff and failed/pending release gates preserved |
| Experiment / positive and negative | Calculation provenance missing in compact stream; AK email owner selected | Actual PowerShell calculation: 1,093.739 raw, 1,094 per arm, 2,188 total; proper NCKH email handoff, no launch |
| Campaign / negative | AK fix owner selected | Actual NCKH fix metadata read and bounded handoff |
| Marketing-plan / negative | AK security owner selected | Actual NCKH security metadata read and bounded handoff |
| Brand / outcome | Claimed JavaScript contrast calculation not visible | Usable two-option design brief; explicitly no contrast/render/font check performed; proposed QA/rights/human gates remain open |
| Xia / negative | Native auto-review denied other-owner SKILL reads as outside Xia scope; provisional handoff and permission question | Under explicit project catalog, actual fix/debug/cook metadata reads returned zero; correct fix handoff and no repair, delegation or routine permission question |

The first brand calculation remains historically unresolved. The later pass relies on its new bounded brief and absence of a calculation claim; it does not reconstruct or certify that earlier calculation. The early ephemeral catalog snapshots are similarly unavailable.

## Concrete inspected outcomes

- Backend repaired actual input validation/ownership behavior and ran 14 meaningful tests; code, tests and receipts were inspected.
- Fix and cook retained failed reproductions before successful repairs. Existing tests and user-owned fixture bytes were preserved. Cook's interactive scenario created review artifacts and remained `waiting-human`, without creating the proposed CLI or claiming approval. Its discovered hash-list metadata error was repaired with prior records retained.
- Data created actual SQLite backup/migration/restore artifacts, rejected duplicate ownership keys, and was independently inspected through read-only database connections. The session completed after 1,107.141 seconds.
- Writing returned usable VI polishing and EN translation with `18/60`, `12`, August 2026, seconds, the exact quotation and `[S1]`; unsupported accuracy/causality/generalization claims were rejected. This is controller fidelity review, not human taste acceptance.
- Visuals produced an actual vector/text SVG (historical evidence path: `../evaluation/direct-skill-tests/workspaces/round-1/nckh-visuals/request-1/completion-rate.svg`; unavailable in the cleaned checkout), preview (historical evidence path: `../evaluation/direct-skill-tests/workspaces/round-1/nckh-visuals/request-1/completion-rate-preview.png`; unavailable in the cleaned checkout) and source map. Controller inspection verified three input-derived 20%/25%/25% points, a zero-denominator gap, eight QA hashes and nine mechanism-source locators. The actual preview was viewed; no target editor round trip, assistive-technology or domain/human acceptance was claimed. Controller artifact receipt (historical evidence path: `../evaluation/direct-skill-tests/private/controller-checks/nckh-visuals-artifacts/receipt.json`; unavailable in the cleaned checkout) retains that distinction. The native session took 1,021.625 seconds.
- Xia inspected actual source/license hashes, identified the whitespace-collapse mismatch, kept compare report-only and port plan-only, and rejected unknown alias/global overwrite authority. No upstream program was executed.
- Test preserved real failures and zero-test discovery. Review, readiness and release cases retained failed/pending gates and missing tools. These finite observations do not establish universal safety or untested integration compatibility.

## Trace integrity, process cleanup and source preservation

[Observation audit](../evaluation/direct-skill-tests/observation-audit.json) contains 43 attempts: 42 pass its file/read/section invariants; the earlier cook timeout lacks a final packet and remains separately inspectable. This audit is not semantic grading.

All 43 owned native job groups closed. Process reconciliation checked 51 recorded native/controller PIDs. Two numbers had been reused by later Chrome/PowerShell processes; process names and creation times identified them as unrelated, and both were left untouched. Reconciled process record (historical evidence path: `../evaluation/direct-skill-tests/private/process-reconciliation-after-pid-reuse.json`; unavailable in the cleaned checkout) and credential-copy cleanup (historical evidence path: `../evaluation/direct-skill-tests/private/credential-copy-cleanup.json`; unavailable in the cleaned checkout) retain the observed state. No dev server, watcher, Git repository, commit or publication was created.

Final integrity observation (historical evidence path: `../evaluation/direct-skill-tests/private/integrity-after-evaluation.json`; unavailable in the cleaned checkout) verifies source revision 18, all 184 pins and source-lock hash `f52a03676b29fbd5434673a0f831dcae397fe879131beec00f35d3ca9b4d472d`. All 43 installed item hashes, ownership bytes and install-specific model policy match the retained baseline. Doctor finds 43 current items and no closure/TOML findings. The installed revision 14 remains the tested subject; revision 18 was not installed or promoted. Existing 81-test and four-host reproducibility receipts are reused only for that unchanged source; they were not rerun as a substitute for behavior.

## Usage and qualification decision

The 42 completed suite/diagnostic sessions report 8,659,517 input tokens, including 7,157,248 cached tokens; 468,163 output tokens, including 274,724 reasoning tokens. Cache and reasoning are subsets, not additional totals. These counts exclude the separate pilot. Monetary billing and effective provider model/effort remain unknown; requested configuration is `gpt-6.1-sol` / `max`.

The authorized direct development test scope is complete. Package qualification remains **experimental / stable-public NO-GO**: one frozen coverage failure, no protected holdout or matched no-skill/upstream baseline, no human/domain review, no full four-host/native/OS matrix or six-role effective-model evidence. Auto/interactive development observations do not establish full feedback/resume acceptance. The native goal API remains blocked and has no exposed resume operation; execution continued under the user's newer grant. The plan remains in-progress, with execution coverage recorded separately from acceptance.
