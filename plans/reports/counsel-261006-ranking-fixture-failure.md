# Counsel: P6 ranking regression fixture metric declaration

## TL;DR

The two `KeyError: 'mrr'` errors are caused by the regression fixtures asking
for an undeclared output metric. `protocol_fixture()` declares `hit@k` for RCA
and `ndcg@k` for retrieval, while the two new tests index `result["metrics"]["mrr"]`.
The evaluator is intentionally projection-based: it computes supported task
metrics internally but exports only the metrics declared by the frozen protocol.

Declare `mrr` explicitly in those two regression fixtures. Do not change the
production metric-selection logic or globally change the shared fixture’s
default RCA/retrieval metric mapping.

## Verified cause

- `core/aiops.py:13` supports `mrr` for both `rca` and `retrieval`.
- `core/aiops.py:171-182` computes the full ranking metric set internally,
  including `mrr`, `hit@k`, `recall@k`, and `ndcg@k` as applicable.
- `core/aiops.py:210-219` then constructs `selected` by iterating only over
  `record["metrics"]`; only those declared IDs are emitted in the returned
  `metrics` mapping. This is the intended frozen-protocol contract.
- `tests/research/test_aiops.py:23` maps RCA to `hit@k` and retrieval to
  `ndcg@k`. The existing retrieval no-relevant test depends on `ndcg@k`, so
  changing the shared mapping globally would regress a valid test and alter the
  fixture’s default protocol semantics.
- `tests/research/test_aiops.py:128-136` expects `mrr` in the RCA empty-gold
  regression without declaring it. `tests/research/test_aiops.py:138-153`
  likewise expects `mrr` for both RCA and retrieval in the denominator/coverage
  regression while retaining the default single declared metric.
- The retained run `plans/runs/nckh-upgrade-261006-0850-attempt-01/p6-review-repair-tests-attempt-01.txt`
  reports 59 tests with exactly those two `KeyError: 'mrr'` errors; no
  production assertion or metric calculation failed before the test attempted
  to read the undeclared key.

## Minimal cause-aligned fix

Modify only the two regression fixture setups in
`tests/research/test_aiops.py`:

1. In `test_rca_empty_gold_obeys_explicit_no_relevant_policy`, after creating
   the RCA fixture, set the declared metric ID to `mrr` before calling
   `evaluate_predictions`.
2. In `test_ranking_denominator_policy_preserves_failure_coverage`, set the
   declared metric ID to `mrr` for each RCA/retrieval fixture before changing
   denominator policies and evaluating.

The narrow form is to replace the single fixture metric ID in each local test
record, preserving the existing metric schema fields and denominator policy.
Appending a second metric is also valid only if the assertions and fixture
intent are updated to cover both outputs; replacing the local declared metric
is the smaller change for tests that assert only `mrr`.

Do not change the `METRICS` set, the internal ranking calculation, or the final
selection loop. Do not use `metrics.get("mrr")`, add a default MRR to every
protocol, or weaken the tests to accept a missing key. The tests are supposed
to state which frozen output they require.

## Focused validation

After the test-only fixture edit, run from
`C:/Users/USER/Downloads/test-skill/nckh-kit`:

```text
python -B -m unittest tests.research.test_aiops
```

Expected result: all 59 tests pass with zero failures/errors. The two repaired
tests should now receive an explicit `mrr` output while the existing retrieval
`ndcg@k` coverage test continues to receive `ndcg@k` from its unchanged default
fixture declaration.

Do not retry the unchanged source or report the retained 57-pass/2-error run as
green. No production code, schemas, build, provider, or freeze changes are
needed for this checkpoint.

## Status

Status: DONE

Summary: Both regressions read `mrr` from a result whose frozen fixture declared
only `hit@k` or `ndcg@k`. Explicitly declaring `mrr` in those local regression
fixtures fixes the contract mismatch while preserving production metric
selection.

Concerns/Blockers: The AIOps class remains unverified until the test-only edit
and a clean 59-test run.
