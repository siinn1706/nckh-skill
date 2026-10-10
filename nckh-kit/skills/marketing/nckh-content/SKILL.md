---
name: nckh-content
description: "Design a long-running content strategy (chiến lược nội dung, kế hoạch biên tập, lịch nội dung dài hạn, nội dung blog, lịch biên tập, trụ cột nội dung), editorial program, calendar and reusable briefs. Conversion assets belong to nckh-copy, time-bound campaigns to nckh-campaign, single-platform posts to nckh-social. Does not write every asset or publish."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-content

## Inputs and owned output

Inputs: Audience/intent, approved positioning/evidence, channels, locale and editorial constraints.

Output: Pillars, editorial calendar, content briefs and reuse/provenance map.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Map audience intent and decision stages to content pillars using supplied/customer/search evidence. Distinguish researched needs from hypotheses. Define each brief's purpose, audience, message, supporting sources, format, channel, owner and acceptance. Label figures as the [Attempt ledger](../../../core/workflows/execution.md#attempt-ledger) requires: a number carried over from an earlier artifact or user restatement without a locator in this attempt's inputs is `unverified` and never stated as fact.

Plan a realistic editorial calendar with capacities and dependencies. Retain provenance, rights, attribution and factual scope in reused content. Adapt locale/register to the channel; do not mechanically translate every artifact.

nckh-content owns the long-running editorial program. Writing an individual conversion asset belongs to nckh-copy; a time-bound multi-channel campaign belongs to nckh-campaign; drafts and the posting schedule for a single social platform belong to nckh-social. General prose goes to nckh-humanwrite and scientific prose to nckh-paperwrite. A small content request should yield its requested usable draft/brief rather than expanding into campaign operations.

Thumbnails, banners and other visuals follow [Marketing and brand assets](../../../core/policies/visual-asset-policy.md#marketing-and-brand-assets): brief only, asset gate `pending`.

Return the editorial program/briefs and decisions. No automatic scheduling, contact upload, account access or publication, and no invented production/results data.

## References

- [Brief schema](../../../core/contracts/brief.schema.json)
- [Claim schema](../../../core/contracts/claim.schema.json)
- [Provider boundaries](../../../extensions/providers/marketing/contract.json)
