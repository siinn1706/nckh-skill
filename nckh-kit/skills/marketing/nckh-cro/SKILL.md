---
name: nckh-cro
description: "Diagnose conversion friction and page discoverability, including canonical/noindex checks, in pages, funnels, forms or onboarding. Does not guarantee uplift or launch a test."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-cro

## Inputs and owned output

Inputs: Actual page/funnel/form/onboarding, audience/evidence, constraints and permitted inspection.

Output: Located friction diagnosis, prioritized hypotheses, UX review and experiment handoff.

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

When a supplied or permitted page is part of the conversion journey, inspect its canonical URL and robots/noindex directives in the actual HTML or observed response headers. Locate conflicting, absent or unobserved directives and explain their possible effect on discoverability before conversion. Do not infer a live index/ranking result from markup. Preserve intentional indexing decisions; broader crawl/search analysis belongs to SEO, and implementation still requires the task's authority.

Use audience/analytics evidence with correct denominator/window. Preserve approved product terms/claims and privacy/consent requirements. Propose task-relevant changes with location, mechanism, evidence, expected risk and measurement oracle.

Rank hypotheses using explicit assumptions rather than fabricated uplift percentages. Experiment owns randomization/sample/stopping and causal readout; frontend/copy own authorized production changes.

Return the requested diagnosis/hypotheses or scoped local implementation under authority. Do not launch tests, reallocate traffic, change budgets or promise conversion gains.

## References

- [Brief schema](../../../core/contracts/brief.schema.json)
- [Claim schema](../../../core/contracts/claim.schema.json)
- [Provider boundaries](../../../extensions/providers/marketing/contract.json)
