# Final contract review: installer and qualification controller

## Code Review Summary

### Scope

- Reviewed the final controller changes in `nckh-kit/core/install.py`, `nckh-kit/installer/schemas/check-receipt.schema.json`, `nckh-kit/evals/run-evals.py`, `nckh-kit/core/evaluation.py`, `nckh-kit/evals/rubrics/catalog.json`, and `nckh-kit/docs/installation.md`.
- Reviewed the focused fixtures in `nckh-kit/tests/installer/test_transactions.py`, `nckh-kit/tests/installer/test_entrypoints.py`, `nckh-kit/tests/release/test_runner.py`, and `nckh-kit/tests/release/test_qualification.py`.
- Compared the result with `plans/reports/review-261001-installer-followup.md`.
- Review was read-only. No install, uninstall, provider, native-host, or global configuration operation was run from this review. Focused tests were inspected while the controller-side test run was in progress; this report does not claim its final runtime result.
- Only this report is modified.

### Overall Assessment

The controller changes close the earlier evidence concern for the intended update boundary. `validate_candidate_evidence()` now rejects top-level pending qualification and `synthetic-fixture` evidence, validates an absolute hash-bound receipt, reloads and validates that receipt during the locked commit re-plan, and requires the receipt to cover the same artifact revision and affected identities.

The evaluation controller also preserves the qualification boundary. Structural validation returns `qualification: pending`, five proposed rubrics remain proposal-only with `reviewer_approval: pending` and no thresholds, and local failure or timeout output cannot satisfy the pass-only check-receipt schema. `doctor()` is read-only and reports local closure/configuration/provenance observations while keeping native freshness and effective model status explicitly unverified.

Two release-gate concerns remain. Doctor does not revalidate the retained candidate receipt after an update, and the candidate-level `evidence_class` is not checked against the classes and input provenance of its receipts. Neither issue creates an installer write outside the existing transaction boundary, but both can allow stale or overstated evidence to be presented to a later release decision.

## Prior Finding Adjudication

### Previous M1: pending or fixture-only evidence could authorize an update — fixed for the stated promotion boundary

`core/install.py:300-323` now rejects `qualification: "pending"` and top-level `evidence_class: "synthetic-fixture"` before an update plan can be committed. It also requires each check receipt to be an absolute, non-link path whose current SHA-256 equals the declared `receipt_sha256`; the receipt must validate against `check-receipt.schema.json`, have `status: "pass"`, match the candidate closure/source-lock maps, and cover every changed identity.

The focused transaction fixture at `tests/installer/test_transactions.py:181-208` covers the intended distinction:

- pending candidate qualification is rejected;
- top-level synthetic-fixture evidence is rejected;
- a bounded static receipt for “candidate bundle integrity only” can support an experimental local update;
- changing that receipt after preview causes `commit_install()` to reject the transaction before ownership state changes.

The last case is not native, human, scientific, or stable qualification. Its receipt declares `input_class: "synthetic-fixture"` and limitations that exclude native and human acceptance. The current documentation correctly limits accepted static checks to their stated scope and keeps native/human qualification separate.

### Previous L1: recovery had no resume path — resolved as an explicit rollback-only policy

`docs/installation.md:90-96` now states that recovery rolls back interrupted transactions and does not resume staged writes. `recover_outstanding()` follows that policy and requires a fresh preview. This is a deliberate safe policy rather than an undocumented missing operation, so it is not carried forward as a finding.

## Critical Issues

None found in the reviewed controller changes.

## High Priority Findings

None found in the reviewed controller changes.

## Medium Priority Findings

### M1. `doctor()` does not revalidate retained candidate receipts

**Evidence:** `core/install.py:617-619` stores `candidate_evidence` in the ownership record. `core/install.py:702-772` recomputes target manifest provenance and visibility, but never calls `validate_candidate_evidence()` or otherwise reads the stored receipt paths and hashes.

After a successful update, an operator can delete, edit, or replace the receipt referenced by `index["installs"][install_id]["candidate_evidence"]`. `doctor()` will still report `candidate_integrity: "current"` when the bundle manifest provenance is unchanged, because its current check covers `target_specs` and manifest hashes only. It does not report that the evidence receipt is missing, failed, stale, or changed.

The installer correctly rejects a changed receipt when committing a new update. The remaining gap is post-commit observability: the documentation says that a missing, failed, or stale receipt does not clear a gate, while the read-only diagnostic does not expose that stale state.

**Impact:** A later release or review step that relies on the doctor output can see current artifact provenance without seeing that the evidence supporting the last update is no longer available or hash-valid. This can create an incomplete acceptance record even though it does not silently mutate an installed tree.

**Recommended action:** Add a read-only receipt status to the doctor install row, reusing the same validation rules as commit. Report distinct states such as current, missing, changed, invalid, failed, and unavailable. Keep `candidate_integrity` separate from receipt integrity, and never turn a missing or stale receipt into a qualification pass.

### M2. Candidate evidence class is not bound to the receipt evidence class or input class

**Evidence:** `core/install.py:304-323`; `installer/schemas/candidate-evidence.schema.json:6-15`; `installer/schemas/check-receipt.schema.json:5-12`.

The validator rejects the top-level `synthetic-fixture` class and requires `accepted-for-scope`, but it does not compare `evidence["evidence_class"]` with `receipt["evidence_class"]` or enforce compatible `input_class` values. A caller can therefore supply a passing static, synthetic-fixture receipt whose scope says “candidate bundle integrity only” while labeling the enclosing candidate evidence `native` or `agent-behavior` and setting `qualification` to `accepted-for-scope`. The receipt passes the current hash/status/affected-skill checks and the enclosing evidence is stored in the install record.

The current test uses the safe form: top-level `static`, synthetic input, and an explicit limitation that no native or human acceptance exists. That bounded experimental update is valid. The concern is that the controller does not prevent a caller from overstating the same receipt as native or agent-behavior evidence.

**Impact:** A downstream release report could read the enclosing evidence class as native or agent-behavior qualification even though every supporting receipt is static or synthetic. The current catalog and evaluation controller keep the overall qualification pending, but the stored candidate record itself is not claim-consistent.

**Recommended action:** Require the enclosing evidence class to be derivable from the receipt classes, or require an explicit set of typed checks and reject unsupported class escalation. Keep synthetic input receipts limited to structural/guard scopes. A native or agent-behavior claim requires a matching receipt class and the corresponding scope evidence; human, scientific, OS, and effective-model gates must remain separate and pending.

## Verified Controller Safeguards

### Changed-receipt revalidation

`commit_install()` (`core/install.py:545-560`) re-reads the index and invokes `plan_install()` under the transaction locks. That call reaches `validate_candidate_evidence()` again, so the current receipt bytes and declared hash are checked after preview and before staging. The fixture at `test_transactions.py:200-205` changes the receipt after preview and verifies that commit fails without changing ownership state.

### Read-only doctor behavior

`doctor()` (`core/install.py:702-772`) uses `read_index()`, local tree/reference parsing, TOML/frontmatter parsing, bundle refresh, provenance comparison, and visibility checks. It does not call `commit_install()`, `uninstall()`, `atomic_json()`, or a provider/native API. The transaction fixture at `test_transactions.py:50-76` verifies that the state file remains unchanged while doctor reports closure/syntax and candidate drift.

The returned fields preserve the evidence boundary:

- `closure_or_syntax` reports local copied skill closure or native file syntax;
- `configured_fields` reports encoded fields without claiming they are applied or effective;
- `provenance` and `candidate_integrity` describe the local candidate relationship;
- `native_freshness` is explicitly unverified;
- `native_smoke` is `not-run`;
- `native_model_effective` is `unknown`;
- `hook_enforcement` is `unverified`.

The entrypoint fixture also verifies that `doctor --state-dir ...` and uninstall preview work without an irrelevant scope and leave the explicit state directory unchanged.

### Failure and timeout receipts

`evals/run-evals.py:31-63` keeps structural or deterministic failures as `status: "fail"`, and records a subprocess timeout as `status: "timeout-unknown"` with no exit status and captured partial output. It returns a nonzero status and does not add a qualification pass. The failure fixture in `tests/release/test_runner.py:20-29` verifies that a failed receipt is retained and has no deterministic or qualification claim.

`check-receipt.schema.json` intentionally accepts only `status: "pass"` and `exit_status: 0`. Therefore a failed or timed-out runner output cannot be used as a candidate check receipt. This preserves an honest distinction between retained diagnostic output and accepted evidence. The runner description and installation/qualification docs also state that local checks do not execute providers, native hosts, or human evaluation.

### Proposed rubrics remain non-human evidence

`core/evaluation.py:44-64` requires exactly the five rubric identities and real rubric files, but rejects any catalog state in which `reviewer_approval` is not `pending` or thresholds are set. The returned result keeps `rubric_approval: "pending"`, `qualification: "pending"`, `cost: "unknown"`, and `cost_per_accepted_task: "undefined"`.

`evals/rubrics/catalog.json` is explicitly `status: "proposal"`, has `reviewer_approval: "pending"`, `thresholds: null`, and states that the criteria have no human approval or labels. `test_qualification.py:6-15` verifies that complete structural case coverage still does not mark quality as passed. The five proposed rubrics cannot become human gold through catalog completeness, deterministic tests, model critique, or an empty review record.

## Native, Human, and OS Gates

All remain pending or unverified:

- `validate_cases()` returns static structural evidence only and rejects stable skill status for this candidate.
- 148 per-skill cases and 224 native invocation cells remain counts of frozen cases, not executed native or human acceptance.
- Native discovery, invocation, effective model, cleanup, permissions, and OS-specific behavior remain unverified.
- VI taste, English fidelity, domain review, scientific visual review, sample rights, reviewer roles, thresholds, and human gold remain pending.
- The five rubric files are proposed criteria, not accepted labels.

## Positive Observations

- The previous pending/synthetic promotion path is now blocked at planning and rechecked at commit.
- Receipt content is hash-bound to the exact candidate closure/source-lock revision, and a changed receipt is caught before mutation.
- Failure and timeout output cannot satisfy the pass-only check-receipt contract.
- Doctor explicitly separates local configuration and closure inspection from native effectiveness and host freshness.
- The qualification controller preserves pending status even when all structural cases and rubric files are present.
- The documentation matches the controller for rollback-only recovery, static-scope limits, missing/stale receipts, and the absence of native/human acceptance.

## Recommended Actions

1. Add receipt-integrity status to `doctor()` so retained candidate evidence cannot appear complete when its receipt is missing, changed, invalid, or failed.
2. Bind candidate-level `evidence_class` to the classes and input provenance of its receipts, and reject native/agent-behavior escalation from static synthetic checks.
3. Keep static fixture updates explicitly experimental and preserve separate native, human, OS, scientific, rights, and effective-model gates.
4. Keep failed and timed-out runner outputs as diagnostics only; do not adapt them into pass receipts or qualification records.

## Metrics

- Type coverage: Not measured; the reviewed controller is Python.
- Test coverage: Not measured in this read-only review; focused tests were inspected while the current focused run was in progress.
- Linting/typecheck issues: Not run.
- Critical findings: 0.
- High findings: 0.
- Medium findings: 2 release/evidence-integrity concerns.

## Unresolved Questions

- Should `doctor()` treat a changed candidate receipt as a separate `candidate_evidence: stale` state while retaining `candidate_integrity: current` for unchanged bundle provenance, or should the two statuses be aggregated for the release gate?
- Should an accepted static receipt with synthetic input be allowed only for experimental local update operations, or should update authorization be separated from any `accepted-for-scope` label until an external release record exists?

Status: DONE_WITH_CONCERNS
Summary: Final controller review confirms pending and top-level fixture-only update evidence is rejected, changed receipts are revalidated before commit, doctor remains read-only and honest about native state, failure/timeout receipts cannot pass the receipt schema, and the five proposed rubrics remain pending rather than human gold. Two medium concerns remain: doctor does not revalidate retained receipts after commit, and candidate evidence class can be overstated relative to its supporting receipts.
Concerns/Blockers: Native, human, OS, scientific, rights, and effective-model acceptance remain pending or unverified; no stable qualification or production claim is supported by this review.

---

## Addendum — 2026-10-01: focused controller delta recheck

This addendum preserves the historical findings above and rechecks only the two Medium concerns against the current controller changes, the changed transaction assertions, and `docs/installation.md`.

### M1 adjudication: retained candidate receipt integrity — fixed

`doctor()` now checks `install["candidate_evidence"]` before reporting candidate provenance. It reuses `validate_candidate_evidence()` in read-only mode and returns a separate `candidate_receipts` record with:

- `status: "current"` when the receipt path, receipt hash, schema, pass status, artifact hashes, typed class, affected identities, and stated scope all still match;
- `status: "invalid-or-stale"` with `qualification: "unverified"` when the receipt is missing, changed, invalid, or otherwise fails the same checks;
- `status: "not-provided"` with `qualification: "unverified"` when no candidate evidence was supplied.

`candidate_integrity` remains a separate manifest/provenance result, so a current bundle can be distinguished from stale receipt evidence. The changed transaction assertions at `tests/installer/test_transactions.py:212-221` verify both states: the receipt is reported current after commit, then deleting it makes the receipt status invalid-or-stale while leaving the ownership file unchanged. `commit_install()` also preserves prior candidate evidence during `config-models` when that operation does not provide a replacement (`core/install.py` retained-evidence branch before the install record write), so model-only changes do not erase the evidence trail for the underlying package update.

The earlier M1 finding is closed. Doctor remains read-only and does not convert receipt integrity into native, human, or release qualification.

### M2 adjudication: candidate evidence class laundering — fixed

`validate_candidate_evidence()` now collects the typed receipt classes and rejects an enclosing candidate whose declared `evidence_class` does not occur in those receipts. It also requires every receipt to cover the complete declared `affected_skills` set, in addition to the existing exact closure/source-lock, hash, schema, status, and path checks.

This closes the previous case where a static synthetic receipt could be wrapped in a misleading `native` or `agent-behavior` candidate label. The current documentation states the same invariant: the declared class needs a matching typed receipt, and static evidence cannot be labeled native or agent behavior.

Synthetic input provenance remains explicit rather than being rejected indiscriminately. A structural or guard observation may legitimately use `input_class: "synthetic-fixture"`, and a genuine native control test may also use synthetic inputs. The receipt records its input class and stated scope, while the controller continues to keep native, human, OS, real-corpus, and effective-model acceptance as separate gates. Synthetic input therefore does not become real-corpus or human evidence merely because its typed class matches the enclosing candidate class.

The earlier M2 finding is closed. No new controller finding was identified in this focused delta.

### Focused acceptance status

- `doctor()` still returns `status: "read-only"`, local closure/configuration/provenance observations, separate candidate receipt state, and explicit native freshness/effective-model unknowns.
- Pending qualification and top-level fixture-only evidence remain rejected for changed updates.
- Changed receipt content is revalidated at commit and is now also visible to doctor after commit.
- Failure/timeout receipt semantics remain unchanged: failed or timed-out outputs are diagnostics and cannot satisfy the pass-only receipt schema.
- All five proposed rubrics, human gold, native host behavior, OS acceptance, rights review, and effective model acceptance remain pending or unverified.

Status: DONE_WITH_CONCERNS
Summary: The focused delta recheck closes both historical Medium concerns. Doctor now revalidates and reports retained receipt integrity separately from candidate provenance, while candidate evidence must have a matching typed receipt class and complete affected-scope coverage; synthetic input remains explicitly scoped and does not become human or real-corpus evidence.
Concerns/Blockers: Native, human, OS, scientific, rights, and effective-model acceptance remain pending or unverified. The focused test run was not independently executed in this review.
