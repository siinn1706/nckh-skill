# Counsel: P6 experiment fixture transitive binding failure

## TL;DR

The validator is correct. The positive fixture omits one real transitive
binding: `evaluation["gold"]["references"][0]` points to `input.json`, but
`experiment_fixture()` only runs its collector over `parents`. Add
`collect(evaluation)` after the final evaluation rewrite and before building
`artifacts`; keep `check_nested` and `manifest_bindings` unchanged.

## Verified cause

- `core/experiments.py:26` defines the frozen manifest bindings as protocol,
  environment, all five parent input references, code, config, and declared
  artifacts. `validate_experiment_manifest()` builds `declared` from those
  bindings and recursively checks every `{path, sha256}` object in the loaded
  scientific parents (`core/experiments.py:108-141`). A parent reference absent
  from the manifest must fail closed.
- `tests/research/test_aiops.py:14-20` creates and binds `input.json` as the
  shared protocol fixture and places that binding in `record["gold"]["references"]`.
  `forecast_readout_fixture()` later rewrites the parent inputs and readout
  fields (`tests/research/test_aiops.py:52-73`) but retains the gold reference.
- `tests/research/test_experiments.py:21-37` loads and rewrites the four
  non-evaluation parents, then saves the final evaluation. At lines 38-46,
  `collect()` is called only with `parents`. Therefore `input.json`, which is
  reachable only through the evaluation parent’s gold reference, is absent from
  `refs` and from the returned `artifacts` list at lines 47-52.
- The retained failure output confirms the same cause at
  `core/experiments.py:135-141`: both positive plan/readout tests fail before
  their intended assertions. The checker test and simulation-label test are
  downstream failures because graph validation runs first. The transitive
  negative test is still the important contract: removing a declared artifact
  must continue to raise.

## Minimal cause-aligned fix

In `tests/research/test_experiments.py`, after the final
`evaluation_ref = save_fixture(root, "evaluation.json", evaluation)` and
before calculating `inputs`, `used`, or the returned manifest:

```python
refs = {}
collect(parents)
collect(evaluation)
```

This adds `input.json` to the manifest’s artifact bindings because it is an
actual hash-bound dependency of the evaluation graph. The existing `used` set
continues to filter direct protocol/code/config and parent/evaluation input
bindings; `input.json` remains in `artifacts` as the required transitive
binding.

Do not weaken `check_nested`, remove `gold.references`, special-case
`input.json`, or broaden `manifest_bindings()` to silently discover files at
validation time. The manifest must explicitly retain every graph binding, and
the negative omission test must remain meaningful.

The collector must run after the final evaluation update. Running it before
the replacement of the analysis input could preserve a stale reference and
hide the actual final graph.

## Focused validation

After the fixture-only edit, run from
`C:/Users/USER/Downloads/test-skill/nckh-kit`:

```text
python -B -m unittest tests.research.test_experiments
```

Expected result: all 13 tests pass with zero failures/errors. This class also
exercises the standalone checker, transitive omission guard, readout receipt,
and simulation-label ordering. Do not rerun the unchanged source or claim P6
verification from the retained `.F..E.E.F....` output.

## Status

Status: DONE

Summary: Positive fixture failure is caused by `collect(parents)` omitting the
final evaluation graph’s `gold.references[0]` binding for `input.json`.
Collecting `evaluation` after its final rewrite repairs the fixture while
preserving the strict transitive validator.

Concerns/Blockers: No production-code defect is indicated. The focused class
remains unverified until the fixture edit and a clean 13-test run.
