# Follow-up review: installer/build

## Code Review Summary

### Scope

- Reviewed the revised installer/build implementation against `plans/260930-1910-nckh-portable-skill-kit/installer-evaluation-migration.md` and the previous report `plans/reports/review-261001-1501-installer.md`.
- Reviewed `nckh-kit/core/install.py`, `nckh-kit/core/build.py`, `nckh-kit/core/paths.py`, `nckh-kit/core/native.py`, `nckh-kit/core/models.py`, `nckh-kit/installer/nckh-installer.py`, the three installer schemas, and the focused build/installer/runtime tests.
- Review mode was read-only. No real install, uninstall, native-host mutation, provider call, global configuration change, or process termination was performed.
- Lines of code and coverage percentages were not independently measured. The review uses function-level source anchors and the existing fixture tests.
- Updated plans: none. The requested scope allowed only this follow-up report.

### Overall Assessment

The revised implementation closes all nine findings from the previous review in the current source. The most important boundary changes are present: manifest identities are constrained, the commit boundary revalidates destination paths, uninstall replans under lock, locks use kernel ownership, rollback validates backups before destructive work, update authorization is explicit, volume checks use device identity, and build output is materialized transactionally.

The remaining concern is qualification semantics. The installer can perform an explicitly requested experimental local update using synthetic or pending evidence, while the plan requires stable claims to remain gated on accepted affected evaluation and on native/human review. That behavior is acceptable for the current experimental kit only when the resulting state remains visibly pending/unverified. It must not be treated as stable qualification or runtime evidence.

No critical security, data-loss, or outage finding remains in the reviewed control flow. Native, human, and OS acceptance remain unverified.

## Previous Findings Rechecked

1. **Manifest skill-ID traversal — fixed.** `core/paths.py:51` constrains skill identities. Bundle verification validates the manifest identity/file grouping, and `plan_install()` resolves selected skill content through the verified bundle and `skill_id()` rather than concatenating unchecked metadata. The regression fixture is `test_manifest_skill_traversal_and_tree_metadata_rejected`.

2. **Forged commit destination outside the target root — fixed.** `owned_entry_path()` and `validate_plan_paths()` (`core/install.py:256` and `:311`) require each transaction destination to resolve to the exact adapter-derived root and expected skill or native-agent filename. `commit_install()` validates the plan before staging or mutation. The regression fixture is `test_commit_rejects_forged_outside_target_before_writing`.

3. **Stale uninstall ownership snapshot — fixed.** Real uninstall acquires the state/physical locks, reloads `ownership.json`, recomputes actions, and verifies that roots did not change before journaling. The regression fixture is `test_uninstall_reloads_owners_after_acquiring_lock`.

4. **Crash-stale lock — fixed.** `exclusive_lock()` (`core/install.py:379`) uses kernel advisory locking, records protocol/PID/nonce state, and releases the kernel lock in `finally`. A crashed process therefore does not leave an ownership file that permanently blocks the next operation. The regression fixture is `test_kernel_lock_released_by_crashed_process`.

5. **Rollback removing a target before validating its backup — fixed.** `rollback()` (`core/install.py:470`) validates the backup location and backup hash while preparing changes, before removing the current target. Missing or changed backups become recovery conflicts and preserve the current tree. The regression fixture is `test_missing_backup_preserves_current_tree_and_restores_index`.

6. **Rollback leaving the ownership index inconsistent on conflict — fixed.** Recovery restores `index_before` even when target conflicts remain, records the conflict in the journal, and exposes the recovery state through `doctor()`.

7. **Install silently promoting an update candidate — fixed in the basic flow.** `plan_install()` has explicit `install`, `update`, and `config-models` operations. An install converts changed owned content into a conflict; an update requires an existing owned install and candidate evidence for changed entries. Provenance includes package, source-lock, adapter, closure, and manifest hashes. `commit_install()` revalidates the full reviewed plan under lock before staging. The synthetic update fixture exercises the authorization boundary.

8. **Cross-device replacement — fixed.** `preflight_volumes()` (`core/install.py:340`) compares resolved device identity for state and target paths and is used for both install and uninstall before mutation. The regression fixture is `test_cross_device_preflight_is_read_only_for_install_and_uninstall`.

9. **Partial build output — fixed.** `build_host()` (`core/build.py:158`) materializes into a temporary sibling tree, verifies the bundle and source lock, then replaces the destination with `os.replace()`. Failed builds clean their staging tree and preserve the prior destination. The regression fixture is `test_failed_build_cleans_staging_and_preserves_destination`.

The revised source also has two useful follow-up safeguards: it rechecks the source lock after materialization, and `verify_bundle()` validates the embedded source lock plus each artifact record's pinned source hash and rights. `target_lock()` now takes a shared visibility lock before per-root locks, which closes the cross-surface duplicate-discovery race identified during the follow-up. The CLI permits `doctor` and `uninstall` to use an explicit `--state-dir` without an irrelevant `--scope`.

## Critical Issues

None found in this static follow-up review.

## High Priority Findings

None found in the reviewed source after the nine fixes above.

## Medium Priority Findings

### M1. Synthetic or pending candidate evidence can authorize an experimental update

**Evidence:** `core/install.py:241-242, 299-307`; `installer/schemas/candidate-evidence.schema.json`; `tests/installer/test_transactions.py:139-169`.

`validate_candidate_evidence()` validates the schema, matches closure/source-lock hashes, and checks that changed skills are listed in `affected_skills`. The schema intentionally permits `evidence_class: "synthetic-fixture"`, `qualification: "pending"`, and arbitrary nonempty check receipts. The existing test then commits an update using exactly that kind of evidence, with a receipt that explicitly says it is not native qualification.

This is valid for a deliberately scoped experimental local update: the fixture proves the installer guard and the state must continue to say that qualification is pending. It is not evidence of a real corpus evaluation, human gold, native behavior, or stable release. The current installer records `qualification` inside the supplied candidate evidence but does not itself reject a pending or synthetic record when an update is committed.

**Impact:** A caller or downstream release process could mistake successful `commit_install()` plus a passing fixture check for accepted stable qualification. That would violate the plan's distinction between synthetic guard fixtures and human/native/runtime evidence.

**Recommended action:** Keep the experimental update path, but make the promotion boundary explicit. A pending or synthetic receipt may update an experimental local candidate only; stable/native/human claims require an `accepted-for-scope` record with the appropriate evidence class and an external review/qualification record. The release/reporting path must refuse to convert the installer result into a stable claim merely because the transaction committed.

**Severity:** Medium release-gate concern; it is not a data-loss or arbitrary-write finding in the current explicitly selected experimental flow.

## Low Priority / Contract Completeness

### L1. Crash recovery is rollback-only

**Evidence:** `core/install.py:438-444`.

`recover_outstanding()` rolls back any non-final journal and requires the caller to re-preview. There is no resume operation for a valid staged transaction. This is safe and preferable to blindly replaying a stale plan, but the plan text describes crash re-runs as supporting `resume/rollback`.

If rollback is the chosen policy for this kit, document that recovery intentionally discards the interrupted transaction and requires a fresh preview. If resume is a required operation, add it as a separately authorized action with the same journal/hash checks. This is an operational completeness issue, not a current destructive-path defect.

## Acceptance and Trust Boundaries

- Build and bundle hashes now establish artifact self-consistency and source-lock integrity. The local threat model does not require a signed author identity, so the absence of package signatures is not reported as a security defect.
- Hash integrity does not establish trusted origin by itself. Origin trust still needs an external/user review record before a package is treated as accepted for release.
- `native_qualification` remains unverified, model effectiveness remains unknown, and transaction results report `native_smoke: not-run`. The fixture-based native model test is evidence of transaction behavior only; it is not native-host evidence.
- Plugin projection remains separate from copied, registered, enabled, trusted, session-only, and tested states. The build/installer flow does not auto-trust or claim those runtime states.
- No live Windows/macOS/Linux permission, symlink, native-agent, IDE discovery, human review, or provider evaluation was performed in this follow-up.

## Positive Observations

- The commit boundary no longer trusts a previously generated plan: targets, roots, sources, provenance, ownership hash, and the complete reviewed plan are revalidated under lock.
- Recovery protects later user edits and restores ownership state on rollback conflicts instead of overwriting an edited target.
- Shared ownership and visible-surface checks distinguish neutral content from host-specific native-agent configuration and block unqualified duplicate definitions.
- The build now carries its embedded source lock and checks each record's source pin, rights, and artifact hash before exposing a candidate.
- The CLI keeps read-only `doctor`, preview-only operation, explicit confirmation, and no-auto-trust behavior visible in the operation contract.

## Recommended Actions

1. Keep `synthetic-fixture` and `pending` evidence explicitly experimental and prevent any release/reporting path from translating it into stable, native, human, or runtime qualification.
2. Record the external/user origin-review reference alongside accepted release evidence; do not infer origin trust from hashes alone.
3. Decide whether rollback-only recovery is the accepted policy. If yes, document it in the transaction contract; otherwise design a separately authorized resume operation.
4. Before stable release, run the pending native, human, and OS acceptance gates with real receipts and preserve incomplete gates as pending.

## Metrics

- Type coverage: Not measured; the reviewed implementation is Python rather than TypeScript.
- Test coverage: Not measured. Focused fixture tests were inspected; this review did not execute real installation or native acceptance.
- Linting/typecheck issues: Not measured in this read-only follow-up.
- Critical findings: 0.
- High findings: 0.
- Medium findings: 1 release-gate concern.
- Low/contract completeness findings: 1.

## Unresolved Questions

- Is rollback-only recovery an intentional product decision under the `resume/rollback` wording, or is a resumable staged transaction required before P6 is considered complete?
- Which release/qualification component owns the final `accepted-for-scope` and external origin-review gate for an experimental local update?

Status: DONE_WITH_CONCERNS
Summary: Follow-up review confirms that all nine previous installer/build findings are addressed, and the added source-lock, provenance, visibility-lock, and explicit-state-dir safeguards are present. One medium release-gate concern remains: synthetic or pending evidence can commit an experimental update and must never be promoted to stable/native/human qualification; crash recovery is currently rollback-only.
Concerns/Blockers: Native, human, and OS acceptance remain pending. This report does not claim runtime, provider, signed-origin, or stable-release evidence.
