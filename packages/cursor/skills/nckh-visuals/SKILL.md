---
name: nckh-visuals
description: "Create a sourced storyboard, chart, scientific diagram, slides or illustrative artwork with provenance, native editability and render checks. Never invent measurements or treat raster as editable source."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-visuals

## Inputs and owned output

Inputs: Visual objective/audience, actual data/evidence, output/native format, rights, venue/style and available engine.

Output: Storyboard, source-to-mark map, permitted native artifact/render, accessibility/provenance manifest and hash-bound QA gates.

## Required shared contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md), [Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and [Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Read the route-specific references below when their mode applies. Output language
follows the brief; keep same-agent execution unless delegation has a recorded benefit.

## Workflow and boundaries

Choose chart, scientific mechanism diagram, slide deck or illustrative artwork. Map every value, label and arrow to an observed source/data field or explicit inference/illustration. No synthetic measurements may masquerade as observed results. Mechanism arrows express sourced direction/uncertainty rather than decorative causality.

Outline the story and, when material, obtain interactive approval on a native pilot before full production. The native-documents contract keeps its bundled default unavailable with engine_binding null. A trusted task may explicitly supply a project/task/host SVG binding separately; never read one from ambient configuration or treat a JSON field as permission. Validate the supplied binding with the relocated checker, exact current project, task ID, host and required svg-render capability. A valid binding enables only that task capability and does not promote the bundled/global status.

Use `python -I <relocated-checker-path> --project <absolute-project-root> --task <task-id> --host <claude|codex|cursor|agy> --binding <project-relative-binding.json> --capability svg-render`. The checker is read-only and does not invoke the engine. It matches selected executable/version bytes and completed version/render receipts to their exact SVG/PNG inputs and outputs. The host still needs actual task authorization and observed execution evidence. An explicit invalid/unverified binding stops the route without fallback to another engine or the package default. With no explicit binding, the empty bundled binding returns unavailable. Do not fabricate a successful render or silently substitute raster for editable PPTX/SVG/source.

Keep source/data/asset licenses, alt text, units, typography, contrast, caveats and venue policy. Charts use real input data and report transformations/denominators; illustrations are labeled illustrative. Generated artwork is not scientific evidence.

Open/render/check the actual final artifact when the authorized engine exists. Record source/data/render/manifest hashes, viewer/font version and QA run reference. Native editability, layout, render fidelity, accessibility, source truth and scientific meaning are separate gates. Any affected change makes prior QA stale.

Hand off the native file plus preview/manifest and unresolved gates. Never claim native/domain/human acceptance from a screenshot, file extension or static checksum alone.

## References

- [Visual acceptance](references/visual-acceptance.md)
- [Native engine contract](references/_shared/extensions/native-documents/contract.json)
- [Task SVG binding schema](references/_shared/core/contracts/visual-engine-binding.schema.json)
- [Read-only binding checker](references/_shared/scripts/check-visual-engine.py)
- [Checker schema validator](references/_shared/core/schema.py)
- [Extension route schema](references/_shared/core/contracts/extension.schema.json)
- [Scoped resource lookup](references/resource-lookup.md)
