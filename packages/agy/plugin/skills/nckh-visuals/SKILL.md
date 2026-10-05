---
name: nckh-visuals
description: "Create research charts, scientific mechanisms or explanatory illustrations from actual sources/calculations/runs, with source-to-mark maps and separate native/scientific gates. Reject branding, ads, banners, logos and generic art."
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

Require a bounded `visual_purpose` in the [brief](references/_shared/core/contracts/brief.schema.json): research question, object, artifact role, evidence IDs/access, origin and mark mapping. A word such as "research" or the brief's domain alone is insufficient. Reject ads, banners, logos (including research logos), thumbnails, branding and generic artwork; the drafting owners may still write their non-visual briefs.

Use chart, scientific mechanism or research illustration. Observed charts require actual dated data; derived/computational/simulation plots require an actual calculation/run with model/code/version/parameters/source/transform/output hashes, run locator and uncertainty or a justified not-applicable reason. Label computed/simulated values `not observed measurements`. Do not build a simulation pipeline to fill absent evidence. Mechanisms retain sourced direction and explicitly labeled inference; illustrations carry `illustrative/non-evidentiary`. Map every value, label and arrow to actual source bytes, verified run output or explicit inference/illustration. Preserve units/denominators, including a source's blank-unit caveat.

Run the shared read-only purpose preflight before a controlled generator writes or calls a provider. Missing/invalid/pending/denied checks stop generation. The same policy applies to brand/content, analytics charts and frontend assets. Current generating bindings are instruction-only/manual/not-callable; a manual checker or post-render receipt does not prove native prevention or arbitrary shell/tool coverage. See [scientific QA](references/scientific-visual-qa.md).

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
