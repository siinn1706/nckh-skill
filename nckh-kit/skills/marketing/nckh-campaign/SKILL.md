---
name: nckh-campaign
description: "Coordinate a time-bound multi-channel campaign (chiến dịch đa kênh, lên chiến dịch, điều phối chiến dịch, từng kênh, làm chiến dịch): brief, channel schedule, asset/task plan and measurement contract. Email sequence content belongs to nckh-email. No automatic ads, budget changes or publication."
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

Scope is a time-bound campaign across several channels. A long-running editorial program belongs to nckh-content; drafts and the posting schedule for a single social platform belong to nckh-social; product or feature release readiness belongs to nckh-launch. This skill coordinates channels and schedule; the content of an email sequence belongs to nckh-email.

Reuse approved strategy and positioning. Define audience, message, offer, channel-specific content/asset needs, schedule, owners and readiness/acceptance. Retain actual source claims and rights across reused assets.

Map channels to content formats, accessibility/localization, tracking and KPI denominators/windows. Distinguish proposed dates/targets from observed campaign results. Hand content, copy and brand work to nckh-content, nckh-copy and nckh-brand without creating another execution engine. Banners, ads and social images follow [Marketing and brand assets](../../../core/policies/visual-asset-policy.md#marketing-and-brand-assets): brief only, asset gate `pending`.

For email, SMS, social or targeted-ad channels, record the audience's jurisdiction and carry the legal gate that nckh-email or nckh-social sets from its sourced jurisdiction check. Do not clear that gate here; without their result it stays `pending`.

For interactive work obtain approval on consequential messaging/pilot before material production. nckh-cook owns durable phase/attempt state; nckh-launch owns product-release sequencing.

Return the usable campaign packet and remaining decisions. Do not log into accounts, schedule external posts, run ads, upload contacts, increase budgets or publish because auto mode or credentials exist.

## References

- [Brief schema](../../../core/contracts/brief.schema.json)
- [Claim schema](../../../core/contracts/claim.schema.json)
- [Provider boundaries](../../../extensions/providers/marketing/contract.json)
- [Scoped resource lookup](references/resource-lookup.md)
