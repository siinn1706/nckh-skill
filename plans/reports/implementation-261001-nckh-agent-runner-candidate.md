# NCKH agent runner — local candidate checkpoint

Recorded: 2026-10-01, Asia/Saigon. Environment: Python 3.12.10 / Windows.

## Decision and authority

**Revision 17 is an experimental local candidate. Stable qualification and public distribution remain NO-GO.**
The approved cook scope covers this source, tests, review and build. The separately approved project installation remains on revision 14; this continuation did not update its skills, roles, ownership or model policy. Provider evaluation and publication remain unauthorized.

The [active plan](../260930-1910-nckh-portable-skill-kit/plan.md) remains in-progress, 28/36 tasks. Human/native acceptance is still required for its unchecked tasks; the local runner implementation closes the specific source gap found in the [earlier audit](audit-261001-1813-native-progress-and-runner-gap.md).

## Implemented scope

- [Evaluation entrypoint](../../nckh-kit/evals/run-evals.py): read-only command recipe preview and explicitly opted-in development execution.
- [Command adapter](../../nckh-kit/core/agent_runs.py): closed recipes, executable/interface/bridge pins, source/case/input binding, six required freeze references and source/case/time budget checks.
- [Owned processes](../../nckh-kit/core/processes.py): suspended Windows child assigned to a Job Object before resuming; POSIX process-group route remains unqualified on this host.
- [Focused tests](../../nckh-kit/tests/release/test_agent_runs.py): real owned local subprocess fixtures and explicitly injected validation faults. These are deterministic tests, not model/provider or human evidence.
- [Qualification documentation](../../nckh-kit/docs/qualification.md): recipe, preview/dispatch, private traces, budget limitations and evidence boundaries.

Dispatch requires live operator opt-in and the exact reviewed preview hash. Six freeze references must exist; their hashes establish integrity, not rights or human approval. Unknown budget fields and unsupported monetary caps stop before dispatch. Only fixed public development cases are supported; protected holdout execution is unavailable.

The chosen native executable or bridge must be independently reviewed. Declaring a surface/version/model does not establish native identity or effectiveness. Exit zero yields `completed-unreviewed` with `unclassified-command-observation`, zero accepted tasks and unknown cost/model. It cannot serve as accepted native, agent or human evidence.

## Actual verification

| Check | Observed result | Evidence |
|---|---|---|
| Focused runner suite | 14/14 pass after runner fixes | Final full-suite receipt also includes every focused test |
| Existing runner/qualification suites | 4/4 pass after entrypoint/docs changes | Final full-suite receipt includes these checks |
| Full deterministic discovery | 79/79 pass, 214.377 seconds; no skips reported | New local checks (historical evidence path: `../../nckh-kit/evals/results/runner-local-checks.json`; unavailable in the cleaned checkout) |
| Four-host reproducibility, including plugins | Two isolated builds per host with matching hashes | New reproducibility (historical evidence path: `../../nckh-kit/evals/results/runner-reproducibility.json`; unavailable in the cleaned checkout) |
| Retained new artifacts | Four manifests match the reproducibility/source pin | New build (historical evidence path: `../../nckh-kit/evals/results/runner-build.json`; unavailable in the cleaned checkout) |
| New source pin | Revision 17, 184 files | [Archived revision-17 source lock](../../nckh-kit/core/registry/source-lock/history/17-35689ebdccd2ef84713a452819f06d7104fa769241a8cee0ab9c19db79f30394.json) |
| New checksums | 2,554 files, including four manifests | New checksum ledger (historical evidence path: `../../nckh-kit/dist-runner/checksums.sha256`; unavailable in the cleaned checkout) |
| Installed-state preservation | All 43 tree hashes, ownership bytes and policy hash match the saved baseline | New candidate record (historical evidence path: `../../nckh-kit/evals/results/candidate-runner.json`; unavailable in the cleaned checkout) |

Source-lock hash: `35689ebdccd2ef84713a452819f06d7104fa769241a8cee0ab9c19db79f30394`.
Checksum-ledger hash: `62ab1f10171bb26fbb7ffd6c37f5d772d8b728bf0b025c292e282335271980e8`.

| Host | Skills | Declared files | Retained manifest | Native qualification |
|---|---|---|---|---|
| Claude | 37 | 639 | manifest (historical evidence path: `../../nckh-kit/dist-runner/claude/manifest.json`; unavailable in the cleaned checkout) | Unverified |
| Codex | 37 | 633 | manifest (historical evidence path: `../../nckh-kit/dist-runner/codex/manifest.json`; unavailable in the cleaned checkout) | Unverified |
| Cursor | 37 | 639 | manifest (historical evidence path: `../../nckh-kit/dist-runner/cursor/manifest.json`; unavailable in the cleaned checkout) | Unverified |
| Antigravity | 37 | 639 | manifest (historical evidence path: `../../nckh-kit/dist-runner/agy/manifest.json`; unavailable in the cleaned checkout) | Unverified |

The original revision-14 candidate (historical evidence path: `../../nckh-kit/evals/results/candidate.json`; unavailable in the cleaned checkout), its 65-test/build receipts and `dist` checksum contents were rechecked and preserved. Its exact [archived source pin](../../nckh-kit/core/registry/source-lock/history/14-2c98d9edad4db63b1b3b8db620d947e6e9e5182ddbfa24ede5a90d27ea6fde03.json) remains available. New artifacts live in `dist-runner`; old evidence is not reused to certify changed source.

## Review and process ownership

Controller review used `ak-code-review`; this is not an independent model or human review. Fixed concrete findings:

1. Command arguments were exposed in preview/summary metadata. Full arguments now remain in the private command record; preview and CLI summaries contain only executable, count and command hash.
2. Extra budget fields could imply an unenforced billing limit, and malformed scope values could bypass structured diagnostics. Closed budget validation now stops these inputs before dispatch.
3. A case cached between reads could differ from the reviewed definitions even after a fresh source check. Definition/input hashes now bind the exact bytes sent to the child.
4. Interrupted or failed attempts could retain a `starting`/`running` status. Such attempts now retain the incomplete outcome and disclose cleanup as unverified when no successful lifecycle result exists.

The timeout fixture retained partial stdout and verified both the owned parent and descendant had stopped. All test/build sessions ended. Post-run process enumeration found no remaining Python process; no dev server or watcher was started. Windows subprocess evidence does not qualify POSIX/macOS/Linux lifecycle behavior or native agent cleanup.

## Remaining acceptance

- 148 frozen skill cases and matched baselines remain unrun; the new subprocess fixtures do not replace them.
- All 224 full native invocation cells remain unqualified. The earlier Codex catalog discovery and actual project-copy repeat remain separate partial observations.
- Ten installer/OS scenarios remain unqualified in the full advertised matrix.
- The owner has no VI/EN corpus or human/domain reviewers. Rights, thresholds, protected holdout and actual scientific visual review remain pending.
- Provider authority, funding scope and acceptable economics remain absent. Accepted task count is zero; cost is unknown and cost per accepted task is undefined.
- Development rounds are bounded per recipe; cross-run lineage, holdout isolation and native driver/model/egress observations still need their frozen protocol and independent review.
- Redistribution and publication require separate evidence and permission.

There is no basis to mark the whole plan or goal complete. The next evaluation depends on the corresponding human inputs, native environment and scoped authority. Re-inventory installed state before any proposed update.
