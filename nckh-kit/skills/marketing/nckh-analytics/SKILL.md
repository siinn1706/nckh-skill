---
name: nckh-analytics
description: "Analyze actual KPI, funnel or campaign data (phân tích số liệu, báo cáo KPI, đọc dashboard, đọc số liệu, số liệu phễu, so sánh chỉ số) with definitions, denominators, time range and quality checks. Correlation alone is not causal lift or attribution; A/B design and causal readout belong to nckh-experiment."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-analytics

## Inputs and owned output

Inputs: Authorized dataset/provenance, KPI definitions, units/time range and analysis question.

Output: Reproducible descriptive analysis, denominators/quality limits and bounded implications.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Read actual data and its provenance/rights. Define events, population/unit, numerator/denominator, aggregation, time range/timezone, exclusions and missingness before computing metrics. Unknown/missing values are not zero.

Check duplicates, instrumentation changes, selection, data completeness and incompatible windows. Preserve transformations and sample counts so the analysis is reproducible. Distinguish a dashboard number, estimate, observed rate and unsupported claim. Label figures as the [Attempt ledger](../../../core/workflows/execution.md#attempt-ledger) requires: a number restated from an earlier report, slide or dashboard without a locator in this attempt's inputs is `unverified` and never stated as fact.

Describe trends/associations with uncertainty and relevant counterevidence. Do not infer causal uplift, channel attribution or randomized effects from correlation. nckh-experiment owns A/B design, randomization and causal readout requirements.

Charts of the analysed data stay here. Banners, ads, thumbnails and other marketing visuals follow [Marketing and brand assets](../../../core/policies/visual-asset-policy.md#marketing-and-brand-assets): brief only, asset gate `pending`.

Return actual findings, data-quality limits and next measurement steps. No invented results, hidden data upload or unauthorized live tracking changes; private datasets stay out of source/dist.

## References

- [Brief schema](../../../core/contracts/brief.schema.json)
- [Claim schema](../../../core/contracts/claim.schema.json)
- [Provider boundaries](../../../extensions/providers/marketing/contract.json)
- [Scoped resource lookup](references/resource-lookup.md)
