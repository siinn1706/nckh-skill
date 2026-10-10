---
name: nckh-social
description: "Create drafts and a posting schedule for one social platform (bài đăng Facebook, lịch đăng bài, mạng xã hội, bình luận tiêu cực) or moderation guidance. Multi-channel campaigns belong to nckh-campaign, editorial programs to nckh-content, brand voice to nckh-brand. No automatic posting, DMs or fabricated organic evidence."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-social

## Inputs and owned output

Inputs: Platform/audience, approved facts/voice, locale, audience jurisdiction, schedule constraints and moderation policy.

Output: Usable posts/calendar or moderation guidance with provenance, disclosure, legal gate and publication gates.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Scope is drafts and the posting schedule for a single platform. A time-bound multi-channel campaign belongs to nckh-campaign; a long-running editorial program belongs to nckh-content; positioning and brand voice come from nckh-brand and are applied here, not redefined.

Select the actual platform and audience from the brief. Any statement about platform limits or policy (length, format, ad rules, targeting of minors) needs a primary source URL and access date; without both, leave the statement out. Adapt voice, length, format, accessibility and CTA to that surface, preserving supported claims and asset rights.

Paid, sponsored, gifted, affiliate or KOL/KOC content carries a visible disclosure in the post itself; never hide a material connection or present it as organic. Determine the audience's jurisdiction, then apply only the sources the [acceptance profile](../../../core/profiles/acceptance/personal-use.json) lists for this skill that cover it, and recheck any source whose limitations flag an unverified article. When no listed source covers the jurisdiction or rule, set the legal gate to `pending`; do not cite instrument numbers, articles or fine amounts from memory.

For calendars define purpose, owner, content/asset needs and measurement hypotheses. Social images and thumbnails follow [Marketing and brand assets](../../../core/policies/visual-asset-policy.md#marketing-and-brand-assets): brief only, asset gate `pending`. For moderation define response/escalation boundaries without impersonating people or sending messages.

Draft in the requested language; quoted engagement/customer reactions require real authorized evidence. Proposed content is not observed organic performance.

Return usable drafts and review/publication decisions. Do not post, schedule externally, follow, direct-message or activate a provider merely because a connector is available. Keep private account/customer information out of public artifacts.

## References

- [Brief schema](../../../core/contracts/brief.schema.json)
- [Claim schema](../../../core/contracts/claim.schema.json)
- [Provider boundaries](../../../extensions/providers/marketing/contract.json)
