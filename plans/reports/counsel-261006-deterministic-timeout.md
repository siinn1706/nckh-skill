# Counsel: P7 deterministic-suite timeout reconciliation

## TL;DR

`p7-deterministic.json` is an incomplete timeout receipt, not a pass or a
completed failure report. The runner used `subprocess.run(...,
capture_output=True, timeout=900)` and retained only the partial progress
stream. A read-only discovery inventory maps the single visible `F` to test
112 of 311:

```text
tests.installer.test_transactions.TransactionTests.test_shared_consumers_need_qualification_and_survive_other_uninstall
```

The concrete failure is `tests/installer/test_transactions.py:142`, which
expects 12 ownership items while the current Core package/index contains 16.
The focused diagnostic confirms `AssertionError: 16 != 12`. Repair that single
explicit expectation in the corrective r41 source/test freeze, preserve this
failed attempt, then run all 311 discovered tests through an observable
task-local `Popen` harness with durable progress and no forced 900-second cap.
Keep the public `evals/run-evals.py` default unchanged.

## Verified timeout evidence

- `plans/runs/nckh-upgrade-261006-0850-attempt-01/p7-deterministic.json` has
  `status: "timeout-unknown"`, `deterministic.exit_status: null`, and the
  original full discovery command. It records `structural_validation: pass`,
  but `qualification: pending`, `accepted_task_count: 0`, and no completed
  deterministic test count.
- The retained progress stream contains 110 `.` characters, one `s`, then one
  `F`, followed by 134 additional `.` characters before the 900-second cutoff.
  The `s` is one skipped test; the `F` is the 112th executed/discovered result
  after 111 preceding result markers. No final unittest traceback was emitted
  because the suite was still running when the outer timeout occurred.
- A read-only `unittest` discovery inventory loaded 311 test IDs in the same
  discovery root/pattern (`tests`, top-level `.`, `test_*.py`) and maps ordinal
  112 to the shared-consumer installer test above. Discovery did not execute
  test bodies and was run with `python -B`.
- The parent supervisor has reaped the previously owned runner/test processes
  (PIDs 28736, 29244, and 12312); no background Python process remains. The
  absence of a live PID does not change the timeout receipt into a completed
  result.
- Two temporary roots created around the late resource-closure activity remain
  available for bounded inspection before cleanup:
  `C:/Users/USER/AppData/Local/Temp/nckh-0d27267dd5f74a1f8529ca8158ac4026`
  and
  `C:/Users/USER/AppData/Local/Temp/nckh-89b7bf7947d34d75b2f87b7f871079e2`.
  Current observation is that the first contains only nested staging
  `nckh-806e34310ab94d6ea47461057596fce3`; the second is empty. This is
  consistent with an interrupted owned staging context, but ownership,
  containment, and reparse status should be recorded before any cleanup.

## Runner behavior and limitation

`nckh-kit/evals/run-evals.py:54-79` constructs the full unittest discovery
command, invokes it with `capture_output=True` and `timeout=900`, and on
`TimeoutExpired` writes `timeout-unknown` with `exit_status: null` plus whatever
partial stdout/stderr Python exposed. It does not stream progress, identify the
current test, or retain a final traceback when the process is still active at
the timeout boundary.

The timeout is therefore evidence of an unfinished attempt and a process
budget boundary, not evidence that the visible `F` was the only failure or that
the remaining tests pass. Do not call the suite green from dots, the skip, the
single `F`, or the fact that the parent later reaped the child.

## Cause discovery before repair

Run this single test first, with verbose output and the same `-B` behavior:

```text
python -B -m unittest -v tests.installer.test_transactions.TransactionTests.test_shared_consumers_need_qualification_and_survive_other_uninstall
```

This should expose the actual assertion traceback. The suspected stale check is
line 142:

```python
self.assertEqual(len(read_index(self.state)["items"]), 12)
```

The current candidate observation reports 16 Core-owned items after the shared
install/uninstall sequence. Do not edit `12` until the focused traceback and
the current package/index contents confirm that the item increase is the
intended r39 candidate change. If confirmed, update the explicit expected
contract to the authoritative count in the same source/test freeze; do not
replace it with a tautological `len(...) == len(...)` or remove the invariant.

The test setup builds the Codex and Agy Core packages once in
`tests/installer/test_transactions.py:21-31`, then the target test installs
Codex, qualifies and installs Agy, uninstalls Codex, and checks that the shared
skill remains (`:132-144`). It is expected to be slower than a pure unit test,
so preserve the full traceback and process chronology if it exceeds normal
latency.

## Full-suite retry after concrete diagnosis

After recording the focused result, run the same complete 311-test suite with
an observable task-local process. Use the unchanged command plus `-v`:

```text
python -B -m unittest discover -s tests -t . -p test_*.py -v
```

The wrapper should:

- use `Popen` with line-oriented stdout/stderr capture and durable tee output;
- retain every verbose test result, skip reason, traceback, exit status, and
  test summary as an attempt artifact;
- record command, Python version, working directory, start/end timestamps,
  PID/parent PID, and cleanup/reconciliation observations;
- avoid a new arbitrary 900-second or 15-minute deadline, while monitoring the
  owned process and preserving a timeout attempt if it genuinely stalls;
- run all 311 discovered tests with no module, class, or case exclusions.

This task-local harness is diagnostic evidence and should not silently replace
the public `run-evals.py` contract. If it completes, the eventual P7 receipt
must identify the alternate observable command and retain its full output
hashes. Reconcile the source-lock hash before and after the run as the current
runner does; a clean test exit with source drift is not a valid deterministic
receipt.

## Temporary-root reconciliation

Before removing the two retained roots, perform only bounded checks on those
exact paths: verify they remain below the intended temp parent, contain no
reparse links, belong to the owned attempt, and are empty after any owned
process cleanup. Remove only an owned empty child/root through the normal helper
route. Do not recursively clean the system temp directory, change ACLs, or kill
processes that are not proven to belong to this attempt.

## What remains pending

- The deterministic suite has no completed exit code or complete test summary.
- The visible `F` is confirmed as the stale line-142 count assertion; the
  focused diagnostic is preserved separately and the one-line repair remains
  pending in the corrective source/test freeze.
- The remaining 199 discovered cases were not completed in the retained
  attempt; the current output does not establish their status.
- `p7-deterministic.json` must remain preserved as historical timeout evidence.

No source, schema, build, provider, or public-runner mutation was made by this
counsel. The focused evidence now justifies only the explicit line-142 count
repair and its corrective r41 freeze; broader changes remain out of scope.

## Status

Status: DONE_WITH_CONCERNS

Summary: Reconciled the 900-second timeout, mapped the visible `F` to test
112/311, confirmed the line-142 stale count as `16 != 12`, and specified the
single repair plus an observable complete-suite rerun without an arbitrary
15-minute cap.

Concerns/Blockers: The single repair has not been applied by counsel, and the
full deterministic gate remains pending until all 311 tests receive a durable
final result with unchanged source-lock before/after evidence.

## Checkpoint addendum: focused failure confirmed

The retained focused diagnostic
`plans/runs/nckh-upgrade-261006-0850-attempt-01/p7-core-count-diagnostic-attempt-01.txt`
ran the mapped test for 52.021 seconds and failed at
`tests/installer/test_transactions.py:142` with the exact result:

```text
AssertionError: 16 != 12
```

The current `nckh-kit/core/registry/catalog/skills.json` contains 43 skills,
of which exactly 16 have `kit == "core"`:

```text
nckh-plan, nckh-cook, nckh-review, nckh-handoff, nckh-research, nckh-evidence,
nckh-method, nckh-write, nckh-taste, nckh-visuals, nckh-humanwrite,
nckh-paperwrite, nckh-dataset, nckh-statistics, nckh-telemetry, nckh-aiops
```

This confirms a stale test expectation, not an installer failure. The four
additional Core owners relative to the old 12-item expectation are part of the
current candidate catalog and package; the corrective r41 repair should update
only the explicit expected count at line 142 from `12` to `16`. Keep the
invariant as an exact count and preserve the final empty-index assertion at
line 144.

After that single assertion repair and the corresponding corrective freeze,
run the complete 311-test discovery command through the observable task-local
Popen harness described above, with `-v`, durable output, no case/module
exclusions, and no arbitrary 900-second/15-minute cutoff. Preserve
`p7-deterministic.json` and the focused failed attempt as historical evidence.

Go/no-go: GO for the single cause-aligned expected-count repair; NO-GO for
declaring deterministic acceptance until the complete 311-test run exits with
a durable summary and the source-lock before/after check remains unchanged.

<oai-mem-citation>
<citation_entries>
MEMORY.md:144-144|note=[per-case runner bounds are historical development limits and failed receipts must be retained]
MEMORY.md:189-189|note=[long runs require owned-process monitoring, timeout reconciliation, and no arbitrary 15-minute cap]
MEMORY.md:205-205|note=[long-run diagnostics must retain full output and verify process identity before cleanup]
</citation_entries>
<rollout_ids>
</rollout_ids>
</oai-mem-citation>
