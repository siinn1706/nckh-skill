---
name: nckh-brand
description: "Define positioning, brand voice (định vị thương hiệu, giọng thương hiệu, thiết kế logo, bộ nhận diện), message hierarchy or a logo/identity design brief. Stops at the brief: no final production assets and no trademark/legal clearance claims."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-brand

## Inputs and owned output

Inputs: Audience, offering/evidence, positioning constraints, language and existing identity/preferences.

Output: Positioning/voice/message architecture plus identity or design brief and review decisions.

## Required contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](references/_shared/core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Inspect existing audience/brand decisions and preserve them. Build positioning from supported customer/problem/offering evidence, distinguishing product facts from proposed messaging. Specify audience, promise, reasons to believe, voice/register and message hierarchy.

Design brief belongs here: define purpose, usage contexts, identity principles, palette/type constraints, accessibility, deliverables, asset/rights requirements and concrete review criteria. Creative direction can present bounded alternatives without fabricating customer preference data.

Logos and identity visuals follow [Marketing and brand assets](references/_shared/core/policies/visual-asset-policy.md#marketing-and-brand-assets): this skill stops at the design brief and records the asset gate as `pending` because no permitted render engine is available. Authorized UI design and build belong to nckh-frontend; research charts and scientific illustrations belong to nckh-visuals; platform-specific social drafts that apply the voice belong to nckh-social. When nckh-frontend (engineer kit) is not installed, hand over the brief with that owner ID and stop.

Keep locale-specific voice; Vietnamese and English do not need literal slogan translation. Avoid unsupported claims, copied competitor assets, invented trademark clearance or a mandatory provider.

Deliver the usable brief/voice examples and consequential decisions. A later final asset still needs its own render receipt plus rights and native QA. This brand request does not authorize publication, spend or production deployment.

## References

- [Brief schema](references/_shared/core/contracts/brief.schema.json)
- [Claim schema](references/_shared/core/contracts/claim.schema.json)
- [Provider boundaries](references/_shared/extensions/providers/marketing/contract.json)
