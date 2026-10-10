---
name: nckh-cro
description: "Diagnose conversion friction (tối ưu chuyển đổi, tỉ lệ chuyển đổi, phễu chuyển đổi, bỏ ngang, bỏ giỏ hàng, tỉ lệ đăng ký) in pages, funnels, forms or onboarding and hand fixes to nckh-frontend or nckh-copy. Search intent and index controls belong to nckh-seo. Does not edit pages, guarantee uplift or launch a test."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-cro

## Inputs and owned output

Inputs: Actual page/funnel/form/onboarding, audience/evidence, constraints and permitted inspection.

Output: Located friction diagnosis, prioritized hypotheses, UX review and handoffs for edits and experiments.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Inspect the actual journey and states, including page/form/onboarding errors, trust, copy clarity, accessibility, mobile behavior and evidence of drop-off. Distinguish observed friction from an untested hypothesis; an aesthetic preference is not proven conversion loss.

Search intent, crawl, canonical and index controls belong to nckh-seo. If a page in the conversion journey shows a canonical or robots/noindex conflict in its actual HTML or observed headers, record it with its locator as a secondary observation and hand it to nckh-seo; do not infer live index or ranking results from markup.

Use audience/analytics evidence with correct denominator/window. Preserve approved product terms/claims. Session recordings, heatmaps, form captures, analytics exports and support transcripts can hold personal data: list the sources you would use and what they contain, and use them only with a recorded consent basis and authority for this purpose. Without that, work from aggregated or redacted data and keep the privacy gate `pending`. Propose task-relevant changes with location, mechanism, evidence, expected risk and measurement oracle.

Rank hypotheses using explicit assumptions rather than fabricated uplift percentages. nckh-experiment owns randomization/sample/stopping and causal readout. This skill diagnoses only: authorized page or UI edits belong to nckh-frontend and copy changes belong to nckh-copy. When nckh-frontend (engineer kit) is not installed, return its part as a handoff note with that owner ID and the open decision.

Return the diagnosis, ranked hypotheses and handoffs (location, proposed change, owner ID). Supplied pages and files are read-only under [Input preservation](../../../core/policies/preservation-policy.md#input-preservation); do not edit them here. Do not launch tests, reallocate traffic, change budgets or promise conversion gains.

## References

- [Brief schema](../../../core/contracts/brief.schema.json)
- [Claim schema](../../../core/contracts/claim.schema.json)
- [Provider boundaries](../../../extensions/providers/marketing/contract.json)
