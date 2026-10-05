---
name: nckh-write
description: "Compatibility route for Vietnamese/English drafting, polishing or translation. Route by requested action to humanwrite or paperwrite while preserving locale, facts and legacy bilingual requests."
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

Read [Authorization](references/_shared/core/policies/authorization-policy.md), [Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and [Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Read the route-specific references below when their mode applies. Output language
follows the brief; keep same-agent execution unless delegation has a recorded benefit.

## Workflow and boundaries

Normalize the [writer language contract](references/_shared/core/profiles/style/writer-language.md)
before drafting. Route polish/translate to [humanwrite](references/_shared/skills/core/nckh-humanwrite/SKILL.md),
including paper paragraphs; route scientific outline/section/argument/reporting/
revision-response to [paperwrite](references/_shared/skills/core/nckh-paperwrite/SKILL.md). Decide from the
requested action and supplied evidence, not the word "paper". Keep legacy general
prose drafting here when neither specialized action applies. Carry the original
`--en`/`--vi` flags and normalized target through the handoff. Both flags conflict
with no artifact mutation; ambiguous no-flag locale needs one clarification.

Select VI, EN, bilingual or vi-to-en/en-to-vi from the brief. Read the matching language/genre profile. Preserve the user's chosen thesis, terminology, protected regions and citations; apply a minimal diff for polishing rather than rebuilding the manuscript.

For Vietnamese use concrete wording, coherent rhythm and language-appropriate register. For English scientific prose prioritize fidelity, precision and genre requirements; do not impose IMRaD on all genres. Literary translation keeps ambiguity, edition/translator context and interpretation boundaries instead of mechanically mapping a rubric.

Draft only from supplied claims with allowed certainty and evidence, or clearly marked hypotheses. The writer creates prose, not evidence/citations. Pure style editing on supplied facts needs no new literature search. New factual claims or stronger certainty require an evidence gate.

Compare before/after numbers, units, denominators, population/time, negation, modality, certainty, causal language, terminology, limitations and citations. Explain unresolved deltas; fidelity failure blocks acceptance even if taste improved. Do not rewrite quotations for fluency.

Return a usable artifact in the requested locale, with concise delta notes where necessary. Taste critique is advisory and human/domain fidelity remains a separate gate.

## References

- [Vietnamese style](references/_shared/core/profiles/style/vi.md)
- [English style](references/_shared/core/profiles/style/en.md)
- [Fidelity and glossary](references/fidelity-and-glossary.md)
- [Scoped resource lookup](references/resource-lookup.md)
