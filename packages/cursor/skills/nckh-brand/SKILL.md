---
name: nckh-brand
description: "Define positioning, brand voice, message hierarchy or an identity/design brief. Does not create final production assets or claim trademark/legal clearance."
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

Keep locale-specific voice; Vietnamese and English do not need literal slogan translation. Avoid unsupported claims, copied competitor assets, invented trademark clearance or a mandatory provider.

Deliver the usable brief/voice examples and consequential decisions. Final logos/media require a selected permitted asset engine and separate rights/native QA. This brand request does not authorize publication, spend or production deployment.

## References

- [Brief schema](references/_shared/core/contracts/brief.schema.json)
- [Claim schema](references/_shared/core/contracts/claim.schema.json)
- [Provider boundaries](references/_shared/extensions/providers/marketing/contract.json)
