---
name: nckh-content
description: "Design a content strategy, editorial program, calendar and reusable briefs. Content planning does not automatically write every asset or publish."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-content

## Inputs and owned output

Inputs: Audience/intent, approved positioning/evidence, channels, locale and editorial constraints.

Output: Pillars, editorial calendar, content briefs and reuse/provenance map.

## Required contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](references/_shared/core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Research visual handoffs use the shared research-purpose preflight: question/object/role/evidence and source-to-mark mappings are mandatory. Do not generate logos, banners, ads, thumbnails or generic artwork, including a research logo. Actual computation/simulation plots need verified run provenance and a non-observed label. This indirect route is instruction-only/manual/not-callable until its event/engine is qualified; missing or denied preflight stops generation. Drafting/analysis/UI inspection remains with this owner.

Map audience intent and decision stages to content pillars using supplied/customer/search evidence. Distinguish researched needs from hypotheses. Define each brief's purpose, audience, message, supporting sources, format, channel, owner and acceptance.

Plan a realistic editorial calendar with capacities and dependencies. Retain provenance, rights, attribution and factual scope in reused content. Adapt locale/register to the channel; do not mechanically translate every artifact.

Conversion copy belongs to copy; general/scientific prose belongs to write. A small content request should yield its requested usable draft/brief rather than expanding into campaign operations.

Return the editorial program/briefs and decisions. No automatic scheduling, contact upload, account access or publication, and no invented production/results data.

## References

- [Brief schema](references/_shared/core/contracts/brief.schema.json)
- [Claim schema](references/_shared/core/contracts/claim.schema.json)
- [Provider boundaries](references/_shared/extensions/providers/marketing/contract.json)
