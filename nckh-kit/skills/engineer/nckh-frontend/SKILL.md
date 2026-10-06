---
name: nckh-frontend
description: "Design, build or audit an authorized UI with UX, accessibility, state and performance evidence. Framework and asset selection follow the task."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-frontend

## Inputs and owned output

Inputs: User flows, visual/UX brief, current stack/components, assets/rights and acceptance.

Output: UX/component/state contract, authorized UI implementation and real visual/accessibility/performance checks.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default. Use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.

## Workflow and boundaries

Research visual handoffs use the shared research-purpose preflight: question/object/role/evidence and source-to-mark mappings are mandatory. Do not generate logos, banners, ads, thumbnails or generic artwork, including a research logo. Actual computation/simulation plots need verified run provenance and a non-observed label. This indirect route is instruction-only/manual/not-callable until its event/engine is qualified; missing or denied preflight stops generation. Drafting/analysis/UI inspection remains with this owner.

Inspect the existing UI, design tokens, component boundaries and state/error flows. Reuse approved UX and the selected stack; do not force a framework or clone trademarked assets. A design-only/audit request stops at its requested artifact.

Define task-relevant loading/empty/error/success states, responsive behavior, keyboard/focus/semantics, contrast and performance expectations. Build with the smallest existing patterns that meet the full brief.

Use optional framework/browser/visual tools only when available and permitted. Open the actual app and capture/render observed states when possible; no fake screenshot or synthetic performance measurement. Static build/type checks do not certify UX or runtime responsiveness.

For broad UI work preserve meaningful interactive design/pilot boundaries. Report current checks and pending human/native review. Do not deploy/publish, increase motion beyond approved thresholds or acquire assets/providers outside scope.

## References

- [Execution/authority modes](../../../core/workflows/execution.md)
- [Review/handoff](../../../core/workflows/review-and-handoff.md)
- [Scoped resource lookup](references/resource-lookup.md)
