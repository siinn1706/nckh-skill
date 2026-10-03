---
name: nckh-analytics
description: "Analyze actual KPI, funnel or campaign data with definitions, denominators, time range and quality checks. Correlation alone is not causal lift or attribution."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-analytics

## Inputs and owned output

Inputs: Authorized dataset/provenance, KPI definitions, units/time range and analysis question.

Output: Reproducible descriptive analysis, denominators/quality limits and bounded implications.

## Required contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](references/_shared/core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Read actual data and its provenance/rights. Define events, population/unit, numerator/denominator, aggregation, time range/timezone, exclusions and missingness before computing metrics. Unknown/missing values are not zero.

Check duplicates, instrumentation changes, selection, data completeness and incompatible windows. Preserve transformations and sample counts so the analysis is reproducible. Distinguish a dashboard number, estimate, observed rate and unsupported claim.

Describe trends/associations with uncertainty and relevant counterevidence. Do not infer causal uplift, channel attribution or randomized effects from correlation. Experiment owns causal design/readout requirements.

Return actual findings, data-quality limits and next measurement steps. No invented results, hidden data upload or unauthorized live tracking changes; private datasets stay out of source/dist.

## References

- [Brief schema](references/_shared/core/contracts/brief.schema.json)
- [Claim schema](references/_shared/core/contracts/claim.schema.json)
- [Provider boundaries](references/_shared/extensions/providers/marketing/contract.json)
- [Scoped resource lookup](references/resource-lookup.md)
