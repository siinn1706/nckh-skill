# Reproducible experiment graph

Freeze the question, independent unit, available-at-origin inputs, splits, fixed
baselines, metrics, oracles, uncertainty/stopping policy and rights before the run.
The [experiment manifest](../../../../core/contracts/experiment-manifest.schema.json)
binds actual protocol, five scientific parents, transitive data/rights, code,
configuration and observed environment. Use contained project paths and exact byte
hashes. Task limits may lower the [controller limits](../../../../core/research_io.py)
and cannot raise them. Amendments retain the previous graph and chronology.

Keep plan and readout separate. A plan has no observed outputs or receipts. A
readout binds its original frozen plan, every attempted terminal receipt and exact
actual output hashes. Changed data/code/configuration invalidates dependent
evidence. Do not transplant historical verdicts to changed inputs.

For retries, freeze distinct output paths with an `attempt_id` on every
`expected_outputs` entry. Each declared attempt has exactly one predictions and
metrics path; other output kinds are optional. A receipt may bind only its own
attempt route. Keep failed partial outputs at their original paths. Legacy
unscoped single-attempt routes remain valid; do not overwrite historical bytes.
Standalone statistical and AIOps readouts require exact path/hash/kind membership
in their terminal receipt outputs. Computed results require a completed receipt.

The [read-only checker](../../../../scripts/check-research-artifacts.py) validates
the graph and recomputes task metrics through their owning contracts:

```text
python -I <checker-path> --project <absolute-authorized-root> --task <id> --manifest <relative-manifest> --output <fresh-relative-check-receipt>
```

It never executes recorded commands, calls providers, installs packages or writes
beyond the fresh explicit check receipt. A successful integrity check does not
authenticate a claimed host observation or confer scientific acceptance.

For a real pilot, retain actual source values, label access, prior access, vintages,
failures and denominators. Calendar ordering in a retrospective snapshot does not
prove historical publication availability. Reconcile arithmetic with a separate
oracle. State dependence and uncertainty limits; a single dependent series may
support descriptive errors without an inferential interval.

Simulation is optional and task-specific. Label it `simulation/not observed
measurements`; bind generator, parameters, seed, replications, warm-up,
conservation checks, uncertainty and model-validity limits. Mechanical fixtures
and simulation never replace an observed pilot or human scientific review.
Simulation parameter bytes belong to the frozen graph and every run input list.
