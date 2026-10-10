---
name: nckh-email
description: "Draft email sequence content (chuỗi email, soạn email, bản tin email) for lifecycle or campaign stages with segmentation, sender identity, consent and suppression. nckh-campaign coordinates multi-channel campaigns. Does not send mail or upload contacts."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-email

## Inputs and owned output

Inputs: Audience/segment evidence, offer/goal, locale, lifecycle stage, recipient jurisdiction and consent/suppression constraints.

Output: Usable email sequence. Each email has subject, header/preheader, body, CTA, a transactional or commercial classification, sender identity and physical address (labelled placeholders when not supplied), an opt-out path, a consent record reference and a suppression path; the sequence adds timing rationale, the legal gate and delivery gates.

## Required contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](references/_shared/core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Define the lifecycle stage, audience/segment assumptions, goal and approved offer. Use supplied evidence to draft subjects, message, CTA and sequence/timing; retain facts and locale-specific tone. When the sequence is part of a multi-channel campaign, nckh-campaign coordinates channels and schedule while nckh-email owns the sequence content.

Classify each email as transactional or commercial from its content. A promotional message is commercial even inside a receipt or onboarding flow; never relabel it transactional to skip consent, labelling or opt-out.

Determine the recipients' jurisdiction before treating consent as sufficient. Apply only the sources that the [acceptance profile](references/_shared/core/profiles/acceptance/personal-use.json) lists for this skill and that cover that jurisdiction, at the article level they record, and recheck any source whose limitations flag a pending successor or unverified article. When no listed source covers the jurisdiction or rule, set the legal gate to `pending`. Do not cite instrument numbers, articles or fine amounts from memory.

Record consent/rights, suppression, unsubscribe and data-quality requirements. Private contacts are not fixture/source/dist content. Segment names or an email connector do not grant permission to upload a list.

Separate draft acceptance from delivery/provider readiness. External send/schedule/contact mutations need a concrete reviewed target/content and explicit grant; credentials alone are insufficient.

Return the requested finished sequence and remaining delivery gates. Do not send tests to real recipients, auto-enroll contacts, fabricate open/conversion rates or claim deliverability without actual evidence.

## References

- [Brief schema](references/_shared/core/contracts/brief.schema.json)
- [Claim schema](references/_shared/core/contracts/claim.schema.json)
- [Provider boundaries](references/_shared/extensions/providers/marketing/contract.json)
