---
name: nckh-campaign
description: "Create a campaign brief, channel schedule, asset/task plan and measurement contract. No automatic ads, budget changes or publication."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-campaign

## Inputs and owned output

Inputs: Approved goals/message/audience, channels, constraints, asset rights and measurement.

Output: Campaign brief, calendar/assets/owners, acceptance and measurement plan.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Reuse approved strategy and positioning. Define audience, message, offer, channel-specific content/asset needs, schedule, owners and readiness/acceptance. Retain actual source claims and rights across reused assets.

Map channels to content formats, accessibility/localization, tracking and KPI denominators/windows. Distinguish proposed dates/targets from observed campaign results. Resolve content/copy/brand handoffs without creating another execution engine.

For interactive work obtain approval on consequential messaging/pilot before material production. Cook owns durable phase/attempt state; launch owns product-release sequencing.

Return the usable campaign packet and remaining decisions. Do not log into accounts, schedule external posts, run ads, upload contacts, increase budgets or publish because auto mode or credentials exist.

## References

- [Brief schema](../../../core/contracts/brief.schema.json)
- [Claim schema](../../../core/contracts/claim.schema.json)
- [Provider boundaries](../../../extensions/providers/marketing/contract.json)
- [Scoped resource lookup](references/resource-lookup.md)
