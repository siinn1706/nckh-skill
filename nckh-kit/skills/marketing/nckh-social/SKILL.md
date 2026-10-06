---
name: nckh-social
description: "Create platform-specific social drafts, strategy, calendar or moderation guidance. No automatic posting, following, direct messages or fabricated organic evidence."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-social

## Inputs and owned output

Inputs: Platform/audience, approved facts/voice, locale, schedule constraints and moderation policy.

Output: Usable posts/calendar or moderation guidance with provenance and publication gates.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Select the actual platform and audience from the brief; verify drift-prone constraints when required. Adapt voice, length, format, accessibility and CTA to that surface, preserving supported claims and asset rights.

For calendars define purpose, owner, content/asset needs and measurement hypotheses. For moderation define response/escalation boundaries without impersonating people or sending messages.

Draft in the requested language; quoted engagement/customer reactions require real authorized evidence. Proposed content is not observed organic performance.

Return usable drafts and review/publication decisions. Do not post, schedule externally, follow, direct-message or activate a provider merely because a connector is available. Keep private account/customer information out of public artifacts.

## References

- [Brief schema](../../../core/contracts/brief.schema.json)
- [Claim schema](../../../core/contracts/claim.schema.json)
- [Provider boundaries](../../../extensions/providers/marketing/contract.json)
