# NCKH candidate — implementation checkpoint

Recorded: 2026-10-01T10:58:39.701029+00:00. Local scope: Python 3.12.10 / Windows.

## Decision

**Experimental local candidate prepared. Stable qualification and public distribution: NO-GO.**
The plan remains in progress. Native installation, paid/provider execution, human qualification and publication require their own inputs/grants.

## Delivered source

- 37 English instruction skills: 10 Core, 13 Engineer, 13 Marketing, one Xia tooling.
- Shared policies/workflows, 11 core schemas, revision/hash state and receipt guards, five model policies and six optional roles.
- Four adapters / eight surface tracks; optional native-agent and plugin projections from the same frozen source.
- Offline builder and shared installer engine with PowerShell/POSIX entrypoints, preview, owned update/configuration, doctor, rollback and uninstall.
- 148 per-skill cases, 19 required fault families, 224 native invocation cells, 10 installer/OS acceptance scenarios and five proposed review rubrics.
- Framework/provider/native-document bindings stay unavailable until a selected interface is qualified.

## Actual verification

| Check | Observed result | Receipt |
|---|---|---|
| Full deterministic discovery | 65/65 pass; no skipped tests in output | Local checks (historical evidence path: `../../nckh-kit/evals/results/local-checks.json`; unavailable in the cleaned checkout) |
| All-host reproducibility, including plugins | Two isolated builds per host; matching manifests/hashes | Reproducibility (historical evidence path: `../../nckh-kit/evals/results/reproducibility.json`; unavailable in the cleaned checkout) |
| Final generated artifacts | Match the reproducibility closure hashes | Build (historical evidence path: `../../nckh-kit/evals/results/build.json`; unavailable in the cleaned checkout) |
| Source pin | 181 files, revision 14 | [Archived source lock](../../nckh-kit/core/registry/source-lock/history/14-2c98d9edad4db63b1b3b8db620d947e6e9e5182ddbfa24ede5a90d27ea6fde03.json) |
| Artifact checksums | 2554 files, including four manifests | Checksums (historical evidence path: `../../nckh-kit/dist/checksums.sha256`; unavailable in the cleaned checkout) |

Source-lock hash: `2c98d9edad4db63b1b3b8db620d947e6e9e5182ddbfa24ede5a90d27ea6fde03`.
Checksum ledger hash: `8a8fc39fa8d1b8064fc41a16c0a55068273e266d19b04acc5197b2e7fee72f6a`.
These checks establish the observed local behavior and integrity; they do not establish native discovery, scientific validity or human taste.

## Artifacts

| Host | Skills | Declared files | Artifact | Native acceptance |
|---|---|---|---|---|
| claude | 37 | 639 | [manifest](../../nckh-kit/dist/claude/manifest.json) | Unverified |
| codex | 37 | 633 | [manifest](../../nckh-kit/dist/codex/manifest.json) | Unverified |
| cursor | 37 | 639 | [manifest](../../nckh-kit/dist/cursor/manifest.json) | Unverified |
| agy | 37 | 639 | [manifest](../../nckh-kit/dist/agy/manifest.json) | Unverified |

Machine candidate record (historical evidence path: `../../nckh-kit/evals/results/candidate.json`; unavailable in the cleaned checkout) owns exact hashes, receipt bindings and open gates. Each artifact includes six optional native role files; exporting plugin files did not register, enable or trust them.

## Installer and review

Independent [initial review](review-261001-1501-installer.md), [follow-up](review-261001-installer-followup.md) and [final review/addendum](review-261001-final-contracts.md) are retained.
All nine initial findings and both final medium findings were fixed. The final addendum reports no new controller finding; remaining concerns are unqualified external gates. Controller tests then passed on the current source.

The engine revalidates paths, source/candidate/ownership and typed hash-bound receipts before commit. Locks serialize shared visibility; rollback validates backups and preserves later edits. Doctor reports artifact and receipt integrity separately and keeps native effectiveness unknown. Interrupted installation uses rollback followed by fresh preview.

## Concrete installation preview

Codex preview (historical evidence path: `../../nckh-kit/evals/results/codex-preview.json`; unavailable in the cleaned checkout): project scope, copy, Core/Engineer/Marketing, balanced policy with inheritance where native mapping is unavailable, optional native agents.

- Entries: 43; conflicts: 0.
- Targets: `.agents/skills` and `.codex/agents` under `C:/Users/USER/Downloads/test-skill`.
- Model effectiveness: unknown. Parent/session configuration is outside this transaction.
- This was dry-run only; no native installation was committed.
- Preview SHA-256: `5cb31ed0ed261572d2b62ca81aadc666098bcec4009645f6036bab6d89cb43de`.

## Evidence still pending

- All 148 frozen per-skill cases and 224 native invocation cells remain not-run. The two earlier [VI writing](forward-test-261001-1501-write.md) and [Xia](forward-test-261001-1501-xia.md) probes were explicit-loaded development observations only.
- Writing-probe input is controller-supplied synthetic text; its figures are not scientific observations. No evidence establishes human corpus provenance or user authorship for that fixture.
- Human corpus rights, competent reviewers, approved rubric/thresholds and protected holdout are absent. The owner confirmed this on 2026-10-01.
- Windows fixture/PowerShell evidence does not qualify actual Windows host consumption, POSIX/macOS/Linux or symlinks.
- Native scientific visuals, effective models, permission/hook enforcement, matched baselines and cost remain unverified/unknown.
- Accepted task count is zero; cost per accepted task is undefined. No measured quality gain is claimed.
- Origin/redistribution review and exact publication authority remain pending. No Git repository was initialized and no commit/publication was performed.

## Next gate

At this initial checkpoint, the approved plan permitted local implementation/build/test and project installation awaited a separate grant. Keep human/native/OS/rights gates open until corresponding observed receipts exist; do not reduce the approved 37-skill/four-host scope.

## Follow-up — approved project installation, 2026-10-01

The owner subsequently answered “Cho phép cài vào project này” for the concrete Codex preview. The [installation record](installation-261001-1813-codex-project-candidate.md) retains the unchanged reviewed preview, installed receipt, doctor and post-install preview. All 43 entries are current; the 37 skill closures and six native TOML files pass local inspection, with zero visibility conflict. Native discovery/invocation and effective models remain unverified; the initial candidate qualification decision is unchanged.

The saved journal validates with an absolute path or filename stem (exit 0, `ok: true`). A relative path reproduces exit 1 without diagnostics; no journal content defect was found.
