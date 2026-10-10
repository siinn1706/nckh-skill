---
name: nckh-copy
description: "Write new conversion copy, landing pages, ads or messages, or change an angle or CTA (viết quảng cáo, viết landing page, viết lại CTA, trang bán hàng, đổi góc tiếp cận), from supported claims and an approved brief. Light polishing or translation of existing text belongs to nckh-humanwrite. No fabricated testimonials, scarcity or results."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-copy

## Inputs and owned output

Inputs: Audience/offer/message evidence, channel, CTA, locale/tone, constraints and protected facts.

Output: Usable copy variants with CTA/tone, a claim ledger and concise revision notes. The claim ledger has one record per objective claim with statement, type, evidence locators, verdict and attempt status as the [claim schema](references/_shared/core/contracts/claim.schema.json) defines; `supported` needs at least one evidence locator, and subjective copy is marked as such.

## Required contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](references/_shared/core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Read the brief and claim evidence before drafting. Select the format and message hierarchy for the audience/channel: headline, problem/value, reasons to believe, objections and CTA only where useful. Preserve offer/pricing/terms explicitly supplied by the user. When a price, offer term or other commercial fact is missing or `unknown`, leave a labelled placeholder such as `[PRICE: unknown]`; never fill in a number.

Write in the requested locale with concrete wording and credible specificity. Distinguish a proposed promise from an observed result. Do not invent testimonials, urgency/scarcity, customer logos, certifications or causal benefits. New factual claims return to the evidence gate. A figure restated from an earlier artifact without a locator in this attempt's inputs is `unverified` under the [Attempt ledger](references/_shared/core/workflows/execution.md#attempt-ledger) and cannot appear as fact.

Provide useful variants only when they clarify a consequential tone/angle choice. Preserve protected regions, numbers, qualifiers and citations during revision.

New copy, a changed angle or a changed CTA belongs here; light polishing or translation of existing text with minimal edits belongs to nckh-humanwrite, and scientific writing to nckh-paperwrite. Content strategy and reusable briefs belong to nckh-content. A conversion diagnosis from nckh-cro arrives as a handoff: copy changes are made here, page or UI edits belong to nckh-frontend. When nckh-frontend (engineer kit) is not installed, return its part as a handoff note with that owner ID instead of editing pages.

Ad images, banners and thumbnails follow [Marketing and brand assets](references/_shared/core/policies/visual-asset-policy.md#marketing-and-brand-assets): brief only, asset gate `pending`.

Return the finished draft as requested. A draft request does not authorize sending, posting, paid placement or changing the product offer.

## References

- [Brief schema](references/_shared/core/contracts/brief.schema.json)
- [Claim schema](references/_shared/core/contracts/claim.schema.json)
- [Provider boundaries](references/_shared/extensions/providers/marketing/contract.json)
