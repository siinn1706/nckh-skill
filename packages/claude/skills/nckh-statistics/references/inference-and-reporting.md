# Scientific analysis and reporting

## Plan before calculation

State the question, estimand, target population/system and observation process.
List independent units and observation-to-unit nesting. An incident with hundreds
of metric windows is one incident for incident-level generalization; a single
country time series does not become many independent countries. Select the design
and dependence model before the estimator.

For each estimator, list required assumptions, relevant diagnostic evidence,
violations, applicability reasons and sensitivity alternatives. Normality concerns
the relevant errors or paired differences when the estimator requires it; avoid
pooled raw-data normality as a universal admission test. Diagnostic p values do not
validate independence, correct measurement or causal identification.

Freeze the comparison family, missingness/exclusion policy, stopping rule and
sample/precision rationale. There is no package-wide alpha, power or sample-size
threshold. Keep prior access and amendments with timezone-aware dates and reasons.

## Comparison and uncertainty

Paired comparisons match the exact independent incident/query/origin IDs. Missing
predictions cannot become zero or disappear from the total denominator. Report
coverage, failure and missing counts with completed counts and the stated aggregation.
Candidate-minus-baseline differences retain zero and negative values.

Choose uncertainty for the sampling and dependence structure: cluster or time
resampling when justified, explicit model-based assumptions when applicable, or a
descriptive readout with no inferential interval. Fold SD, technical replicate SD
and between-seed spread are not automatically confidence intervals. Define the
unit, interval/error-bar meaning and estimator rather than calling every spread CI.

For optional simulation-based power, record generator, parameter distribution,
estimator, seed, replications, failed calculations, Monte Carlo uncertainty and
stopping. Simulation answers its specified model; it does not establish observed
real-system power or efficacy. External numerical libraries require task-level
version/environment binding and authorization before installation/execution.

## Plan/readout records

The closed `statistical-analysis` record distinguishes `plan` and `readout`.
Plans keep result fields null, no run/output references and pending applicability
where warranted. Readouts require actual contained hash bindings and reconciled
observation/independent-unit counts. At least one bound result file must exactly
contain `schema_version`, `task_id`, `result` and `denominators` matching the readout.
The artifact checker is read-only; supplied argv/commands do not grant execution.

Readout status may preserve a failed calculation with actual failure reasons.
Computed uncertainty requires actual interval or standard-error values and assessed
required estimator assumptions. A failure or pending assumption stays visible.
The owner validator reports contract integrity and keeps scientific acceptance pending.

Handoff to paperwrite: estimand, unit/n/nesting, design/assumptions, estimator/effect,
denominators, uncertainty, multiplicity/stopping, data/code/environment/run/output
references, failed/null results and bounded interpretation. Do not assert that an
association, feature attribution or model ranking identifies a cause.

## Source contributions

This is independently authored guidance informed by the reviewed local K-Dense
statistical-analysis assumptions/reporting references and Nature statistics
failure-mode reference. Exact snapshot/hash/rights records belong to the source
ledger; no upstream example numbers, scripts, assets or scientific verdicts are adopted.
