---
name: nckh-copy
description: "Write conversion copy, landing pages, ads or messages from supported claims and an approved brief. No fabricated testimonials, scarcity or results."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-copy

## Inputs and owned output

Inputs: Audience/offer/message evidence, channel, CTA, locale/tone, constraints and protected facts.

Output: Usable copy variants with CTA/tone, grounded claims and concise revision notes.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Read the brief and claim evidence before drafting. Select the format and message hierarchy for the audience/channel: headline, problem/value, reasons to believe, objections and CTA only where useful. Preserve offer/pricing/terms explicitly supplied by the user.

Write in the requested locale with concrete wording and credible specificity. Distinguish a proposed promise from an observed result. Do not invent testimonials, urgency/scarcity, customer logos, certifications or causal benefits. New factual claims return to the evidence gate.

Provide useful variants only when they clarify a consequential tone/angle choice. Preserve protected regions, numbers, qualifiers and citations during revision. General/scientific writing remains write's owner.

Return the finished draft as requested. A draft request does not authorize sending, posting, paid placement or changing the product offer.

## References

- [Brief schema](../../../core/contracts/brief.schema.json)
- [Claim schema](../../../core/contracts/claim.schema.json)
- [Provider boundaries](../../../extensions/providers/marketing/contract.json)
