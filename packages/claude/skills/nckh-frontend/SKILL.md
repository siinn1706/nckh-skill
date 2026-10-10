---
name: nckh-frontend
description: "Design, build or audit an authorized UI (giao diện, làm UI, dựng trang web, sửa giao diện, làm trang) with UX, accessibility, state and performance evidence. Conversion diagnosis remains nckh-cro, copywriting remains nckh-copy, logos and brand assets remain nckh-brand and research figures remain nckh-visuals."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-frontend

## Inputs and owned output

Inputs: User flows, visual/UX brief, current stack/components, assets/rights and acceptance.

Output: UX/component/state contract, authorized UI implementation and real visual/accessibility/performance checks.

## Required contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Run commands under [Command discipline](references/_shared/core/workflows/execution.md#command-discipline) and [Host shell robustness](references/_shared/core/workflows/execution.md#host-shell-robustness),
label claims with the [Attempt ledger](references/_shared/core/workflows/execution.md#attempt-ledger) and keep inputs per
[Input preservation](references/_shared/core/policies/preservation-policy.md#input-preservation).
Output follows the brief's locale. Same-agent is the default. Use
[model/context policy](references/_shared/core/workflows/model-and-context.md) before delegation.

## Workflow and boundaries

Research charts and scientific illustrations belong to nckh-visuals under the [Purpose preflight](references/_shared/core/policies/visual-asset-policy.md#purpose-preflight). Logos (including a research logo), banners, ads, thumbnails and generic artwork belong to nckh-brand, which stops at a brief and keeps the final asset `pending` per [Marketing and brand assets](references/_shared/core/policies/visual-asset-policy.md#marketing-and-brand-assets). Embed or generate an image in the UI only when the brief carries a valid `visual_purpose` and `check-visual-engine.py` reports a permitted engine binding; otherwise stop and hand the request to its owner. nckh-cro diagnoses conversion friction only; this skill applies the authorized page/UI edits from its findings, and changed copy comes from nckh-copy.

Inspect the existing UI, design tokens, component boundaries and state/error flows. Reuse approved UX and the selected stack; do not force a framework or clone trademarked assets. A design-only/audit request stops at its requested artifact.

Define task-relevant loading/empty/error/success states, responsive behavior, keyboard/focus/semantics, contrast and performance expectations. Build with the smallest existing patterns that meet the full brief.

Use optional framework/browser/visual tools only when available and permitted. Open the actual app and capture/render observed states when possible; no fake screenshot or synthetic performance measurement. Static build/type checks do not certify UX or runtime responsiveness.

For broad UI work preserve meaningful interactive design/pilot boundaries. Report current checks and pending human/native review. Do not deploy/publish, increase motion beyond approved thresholds or acquire assets/providers outside scope.

## References

- [Execution/authority modes](references/_shared/core/workflows/execution.md)
- [Review/handoff](references/_shared/core/workflows/review-and-handoff.md)
- [Scoped resource lookup](references/resource-lookup.md)
