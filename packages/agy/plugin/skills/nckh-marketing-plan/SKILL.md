---
name: nckh-marketing-plan
description: "Create a marketing strategy (kế hoạch marketing, chiến lược marketing, ngân sách marketing, kế hoạch tiếp thị, chiến lược tiếp thị) with hypotheses, channels, KPI definitions and budget constraints. A task plan with phase files belongs to nckh-plan. Strategy does not authorize spend or own task orchestration."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-marketing-plan

## Inputs and owned output

Inputs: Goals, audience/evidence, time horizon, constraints, budget authority and measurement inputs.

Output: Strategic plan with hypotheses, channel rationale, KPI definitions, budget scenarios and decision gates.

## Required contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](references/_shared/core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Translate business goals into audience/problem hypotheses and measurable outcomes. Read market evidence and approved positioning. Compare channel choices against fit, constraints, operational capacity and available measurement; distinguish assumptions from observed results.

Define KPIs with numerators/denominators, attribution windows, data sources, quality limitations and guardrails. Budget scenarios need supplied prices/budget or explicit estimates with sources; unknown economics stay unknown.

Plan sequencing, responsibilities, experiment hypotheses and review gates. Preserve the user's explicit spending/threshold decisions. Do not claim a forecast is observed lift or fabricate ROI.

Return strategy as a usable artifact. nckh-plan turns an approved strategy into a task plan with phase files, and nckh-cook owns execution state. No ad account write, spend increase, campaign launch or publication follows merely from a strategy request.

## References

- [Brief schema](references/_shared/core/contracts/brief.schema.json)
- [Claim schema](references/_shared/core/contracts/claim.schema.json)
- [Provider boundaries](references/_shared/extensions/providers/marketing/contract.json)
- [Scoped resource lookup](references/resource-lookup.md)
