---
name: nckh-statistics
description: "Design or validate scientific statistical analysis plans and readouts (phân tích thống kê, kiểm định thống kê, cỡ mẫu nghiên cứu, ý nghĩa thống kê): estimands, independent units, nesting, assumptions, pairing, missingness, uncertainty, multiplicity and stopping. Marketing A/B tests belong to nckh-experiment, KPIs to nckh-analytics, database work to nckh-data and research files to nckh-dataset."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-statistics

## Inputs and owned output

Inputs: Research question/protocol, estimand, actual independent units and nesting,
dataset/split bindings, proposed estimator and actual run/output artifacts when available.

Output: A `statistical-analysis` plan or actual bound readout, assumption/uncertainty
record and limitations. Follow the requested Vietnamese, English or bilingual locale.

## Required shared contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md).

## Workflow and boundaries

Define the estimand, population, independent unit, repeated/cluster/time structure
and comparison before selecting an estimator. Match paired comparisons by actual
independent IDs; expose incomparable units and missing/failed calculations.

Freeze missingness, transformations, multiplicity and stopping before analysis.
Required assumptions need evidence or explicit unresolved limitations; a diagnostic
non-rejection does not certify all assumptions. Choose task-specific uncertainty,
seed and replication policies; record applicability reasons instead of invented values.

A plan may retain pending data/assumptions and contains no observed estimates or
run receipts. A readout binds actual dataset, split, protocol, run and structured
result bytes; values and denominators must match the bound output. Preserve zero,
negative/null results and failed attempts. Do not turn temporal windows, folds or
technical repetitions into independent n or an IID confidence interval.

Keep descriptive, predictive, associational, causal and simulation claims separate.
Identified causal claims require the method owner's design evidence and domain
review. Numerical contract checks do not certify scientific interpretation.

nckh-dataset owns labels/splits, nckh-telemetry owns observation mapping, nckh-aiops
owns task metrics, nckh-method owns design and nckh-cook owns authorized execution.
Database schemas and queries go to nckh-data; marketing A/B tests go to
nckh-experiment. Statistical reporting alone does not establish scientific validity. Computation packages
are optional task bindings. Return an analysis plan when actual data/runs are absent;
do not launch providers, install packages or write a paper from invented results.

## References

- [Inference and reporting](references/inference-and-reporting.md)
- [Statistical record](references/_shared/core/contracts/statistical-analysis.schema.json)
- [Scoped authored resource lookup](references/resource-lookup.md)
