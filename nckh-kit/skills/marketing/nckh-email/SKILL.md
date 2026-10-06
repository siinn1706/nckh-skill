---
name: nckh-email
description: "Draft an email lifecycle or campaign sequence with segmentation, consent and suppression assumptions. Does not send mail or upload contacts."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-email

## Inputs and owned output

Inputs: Audience/segment evidence, offer/goal, locale, lifecycle stage and consent/suppression constraints.

Output: Usable email sequence with subjects, copy/CTA, timing rationale and delivery gates.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Define the lifecycle stage, audience/segment assumptions, goal and approved offer. Use supplied evidence to draft subjects, message, CTA and sequence/timing; retain facts and locale-specific tone.

Record consent/rights, suppression, unsubscribe and data-quality requirements. Private contacts are not fixture/source/dist content. Segment names or an email connector do not grant permission to upload a list.

Separate draft acceptance from delivery/provider readiness. External send/schedule/contact mutations need a concrete reviewed target/content and explicit grant; credentials alone are insufficient.

Return the requested finished sequence and remaining delivery gates. Do not send tests to real recipients, auto-enroll contacts, fabricate open/conversion rates or claim deliverability without actual evidence.

## References

- [Brief schema](../../../core/contracts/brief.schema.json)
- [Claim schema](../../../core/contracts/claim.schema.json)
- [Provider boundaries](../../../extensions/providers/marketing/contract.json)
