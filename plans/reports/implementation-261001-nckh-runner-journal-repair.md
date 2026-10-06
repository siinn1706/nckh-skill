# NCKH runner journal repair — revision 18

Recorded: 2026-10-01, Asia/Saigon. Local environment: Python 3.12.10 / Windows.

## Decision

**Experimental local candidate only. Stable qualification and public distribution remain NO-GO.**
The previous goal turn made progress by implementing the command adapter and verifying revision 17. This turn made progress by reproducing and repairing two incomplete-journal paths. The full approved scope remains 37 skills, four hosts/eight surfaces and all human/native/economic acceptance requirements.

## Verified cause and repair

The retained [fault reproduction](diagnostic-261001-runner-incomplete-journal.json), bound to revision 17, showed two expected failures escaping the adapter's private receipt handler:

1. An owned-process lifecycle wait raising `TimeoutExpired` left the run at `running` and its attempt at `starting`.
2. A case read failing after preview left a `running` private record with no attempts.

Both are explicitly labeled deterministic injected faults. No driver was dispatched in the reproduction; they are not provider/model, native or human observations.

[The adapter](../../nckh-kit/core/agent_runs.py) now handles case loading inside its receipt scope. Lifecycle timeout records `timeout-unknown`, unknown exit status and unverified cleanup; other subprocess failures retain failure. Summaries omit exception command arguments. The caller still must reconcile actual cleanup before another attempt.

[Two regression tests](../../nckh-kit/tests/release/test_agent_runs.py) exercise the failed-read and lifecycle-error paths, including a private argument marker that must not appear in a returned receipt. The existing real subprocess tests continue to verify transport, nonzero exits and timeout descendant cleanup. [Qualification documentation](../../nckh-kit/docs/qualification.md) records the updated contract.

## Actual final checks

| Check | Observed result | Evidence |
|---|---|---|
| Focused command runner | 16/16 pass | Included in the final full-suite output |
| Existing runner and qualification | 4/4 pass | Included in the final full-suite output |
| Full deterministic discovery | 81/81 pass, 345.721 seconds; no skips reported | Local receipt (historical evidence path: `../../nckh-kit/evals/results/runner-cleanup-local-checks.json`; unavailable in the cleaned checkout) |
| Four-host reproducibility, with optional plugins | Two isolated builds per host, matching hashes | Reproducibility (historical evidence path: `../../nckh-kit/evals/results/runner-cleanup-reproducibility.json`; unavailable in the cleaned checkout) |
| Retained new build | Four manifests match their reproducibility/source pin | Build (historical evidence path: `../../nckh-kit/evals/results/runner-cleanup-build.json`; unavailable in the cleaned checkout) |
| Frozen source | Revision 18, 184 files | Embedded immutable pin (historical evidence path: `../../nckh-kit/dist-runner-cleanup/codex/source-lock.json`; unavailable in the cleaned checkout) |
| Checksum ledger | 2,554 files | Checksums (historical evidence path: `../../nckh-kit/dist-runner-cleanup/checksums.sha256`; unavailable in the cleaned checkout) |
| Earlier artifacts and receipts | Revision 14 and 17 contents and bound receipts match their stored hashes | New candidate (historical evidence path: `../../nckh-kit/evals/results/candidate-runner-cleanup.json`; unavailable in the cleaned checkout) |
| Installed state | All 43 tree hashes, ownership bytes and policy hash unchanged | New candidate's installed-state comparison |

Source-lock hash: `f52a03676b29fbd5434673a0f831dcae397fe879131beec00f35d3ca9b4d472d`.
New artifacts are in `dist-runner-cleanup`; `dist` and `dist-runner` remain available for revisions 14 and 17. No installed candidate update, provider evaluation, Git initialization, commit or publication was performed.

## Completion audit against all seven phases

| Phase and explicit acceptance scope | Authoritative evidence available | Completion still unproven |
|---|---|---|
| P1: schemas/state, four workflow skills, profiles and auto/interactive boundaries | Pinned source, contract tests and current full-suite receipt | Actual workflow feedback/resume, native model and delegation behavior |
| P2: six research/writing/visual skills, evidence/VI/EN/venue/literary/native contracts | Source profiles, fault guards and frozen case definitions | Rights-cleared VI/EN samples, human/domain fidelity/taste and actual native scientific visuals |
| P3: 13 Engineer skills and Xia, diagnosis/repair/dirty-file/permission boundaries | Source, guard tests and earlier limited Xia development probe | Full authorized skill outcomes, tool traces and independent scoped acceptance |
| P4: 13 Marketing skills, competitor/design brief, KPI and draft/send/spend boundaries | Source, local guards and frozen case definitions | Real agent outcomes, human/statistical review and permitted connector behavior |
| P5: four adapters, self-contained reproducible artifacts, all eight surfaces | Current four-host build receipts; earlier scoped Codex catalog discovery | Invocation/config precedence, effective model/effort, hooks/tool/egress and cleanup on every advertised cell |
| P6: shared engine, two entrypoints, owned transactions/recovery | Current deterministic tests; actual revision-14 Windows project-copy installation and unchanged repeat | Full OS/runtime/global/symlink and real update/rollback/uninstall scenarios |
| P7: frozen metrics/rights/review/budget/holdout, matched baselines, lineage and release decision | Protocol/rubric proposals, current local receipts and scoped NO-GO decision | Human freeze, protected holdout, cross-run lineage, authorized agent/native/human runs and measured economics |

The eight unchecked Todo entries remain unchecked: one each in P1–P6 and two in P7. The plan stays **in-progress, 28/36 tasks**, with no fully accepted phase. All 148 full per-skill cases, 224 full native cells and ten full installer/OS scenarios remain unqualified; earlier partial discovery/installation observations do not close those matrices.

The owner has no VI/EN corpus or human/domain reviewers. Provider authority/funding, native lab/driver evidence, approved review thresholds and protected holdout remain absent. Cost stays unknown, accepted task count zero, and cost per accepted task undefined. Source hashes and test passes cannot supply these inputs or authority.

This audit does not mark the goal complete. Further qualification depends on the corresponding human inputs and external permissions/environment. Preserve the installed revision 14 and re-inventory it before any proposed update.
