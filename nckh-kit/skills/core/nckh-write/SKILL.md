---
name: nckh-write
description: "Compatibility route used only when nckh-write is called explicitly (soạn văn bản, viết song ngữ, công văn, Việt lẫn Anh). Prefer the owners: nckh-humanwrite for polish or translation, nckh-paperwrite for scientific authoring, nckh-copy for marketing copy, nckh-docs for repository documentation. Preserves locale, facts and legacy bilingual requests."
argument-hint: "<action and prose/evidence brief> [--en|--vi]"
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-write

## Inputs and owned output

Inputs: Draft or evidence/outline, language/genre/audience, glossary, protected regions and requested change.

Output: Usable draft or minimal edit plus factual-delta/terminology record and unresolved evidence gates.

## Required shared contracts

Read [Authorization](../../../core/policies/authorization-policy.md), [Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and [Acceptance](../../../core/policies/acceptance-policy.md) before work.
Read the route-specific references below when their mode applies. Output language
follows the brief; keep same-agent execution unless delegation has a recorded benefit.

## Workflow and boundaries

Normalize the [writer language contract](../../../core/profiles/style/writer-language.md)
before drafting. Route polish/translate to [humanwrite](../nckh-humanwrite/SKILL.md),
including paper paragraphs; route scientific outline/section/argument/reporting/
revision-response to [paperwrite](../nckh-paperwrite/SKILL.md). Decide from the
requested action and supplied evidence, not the word "paper". Keep legacy general
prose drafting here only when called explicitly and no owner applies: new marketing
copy goes to nckh-copy or nckh-content, and documentation for changed repository
behavior, setup, commands or contracts goes to nckh-docs. Carry the original
`--en`/`--vi` flags and normalized target through the handoff. Both flags conflict
with no artifact mutation; ambiguous no-flag locale needs one clarification.

Select VI, EN, bilingual or vi-to-en/en-to-vi from the brief. Read the matching language/genre profile. Preserve the user's chosen thesis, terminology, protected regions and citations; apply a minimal diff for polishing rather than rebuilding the manuscript.

For Vietnamese use concrete wording, coherent rhythm and language-appropriate register. For English scientific prose prioritize fidelity, precision and genre requirements; do not impose IMRaD on all genres. Literary translation keeps ambiguity, edition/translator context and interpretation boundaries instead of mechanically mapping a rubric.

Draft only from supplied claims with allowed certainty and evidence, or clearly marked hypotheses. The writer creates prose, not evidence/citations. Pure style editing on supplied facts needs no new literature search. New factual claims or stronger certainty require an evidence gate.

Compare before/after numbers, units, denominators, population/time, negation, modality, certainty, causal language, terminology, limitations and citations. Explain unresolved deltas; fidelity failure blocks acceptance even if taste improved. Do not rewrite quotations for fluency.

Return a usable artifact in the requested locale, with concise delta notes where necessary. Taste critique is advisory and human/domain fidelity remains a separate gate.

## References

- [Vietnamese style](../../../core/profiles/style/vi.md)
- [English style](../../../core/profiles/style/en.md)
- [Fidelity and glossary](references/fidelity-and-glossary.md)
- [Scoped resource lookup](references/resource-lookup.md)
