---
name: nckh-paperwrite
description: "Author outlines, sections, arguments, reporting revisions or reviewer responses for a paper, thesis, proposal or research report from existing evidence. Use for scientific authoring; prose-only polish/translation belongs to nckh-humanwrite."
argument-hint: "<authoring action and evidence brief> [--en|--vi]"
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-paperwrite

## Inputs and owned output

Use the authoring action, research question, existing claims/evidence, audience,
genre, chosen venue/year/track/article type, glossary and protected regions.
Return an outline, section, argument or reviewer response with evidence IDs,
factual-delta record and unresolved gates. Never create evidence or observations.

## Shared contracts and language

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md).
Use the shared [writer language contract](../../../core/profiles/style/writer-language.md).
`--en` chooses English; `--vi` chooses Vietnamese. Both flags return a conflict
before any draft mutation. Without a flag resolve explicit target, brief, then
dominant draft language; if unresolved ask one question. Keep bilingual requests
and explicit flag overrides. Skill arguments do not establish native host syntax.
Read the selected [VI](../../../core/profiles/style/vi.md) or
[EN](../../../core/profiles/style/en.md) style; bilingual uses both.

## Scientific authoring

Read [paperwriting policy](references/paperwriting-policy.md) for this action.
Tie each factual statement to existing evidence or label a hypothesis. Separate
methods, observed results, computed/simulated outputs, interpretation and limits.
Report missing inputs explicitly. Do not invent results, citations or author acts.
Preserve numbers, units, denominators, negation, modality, certainty, population,
time, causality, terminology, citations, limitations, quotes and protected regions.
Compare factual deltas when revising existing sections.

Select structure by genre and the chosen venue profile; do not force IMRaD or
clinical checklists onto unrelated disciplines. Handoff paragraph polish or
translation to `nckh-humanwrite`, carrying locale and flags.
`nckh-taste` remains a critic. Human/domain acceptance is separate.

## Scoped resources

Use [writer lookups](../../../core/profiles/style/writer-resources.md) when applicable.
Paperwrite may read PMC English biomedical fidelity samples, Nature English advice
and reporting lookup only for matching clinical/health study designs. It cannot
read Wikisource literary samples or publisher profiles as scientific style gold.
Keep EN source locale when writing VI. Resource-off cannot block evidence-based
core authoring and must return disabled/no-read. Optional LanguageTool is an
English diagnostic requiring Java 17 and nested LGPL/rights review; no mandatory
service, rule copying or public-server call is part of this skill.
