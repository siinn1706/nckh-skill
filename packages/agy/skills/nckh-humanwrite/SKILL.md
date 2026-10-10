---
name: nckh-humanwrite
description: "Polish, revise or translate supplied Vietnamese/English prose with minimal edits and factual-delta checks (sửa văn cho mượt, chỉnh câu chữ, dịch sang tiếng Anh, lủng củng, cho hay hơn), including paper paragraphs. Scientific authoring belongs to nckh-paperwrite; new copy or a changed angle or CTA belongs to nckh-copy."
argument-hint: "<draft and requested edit> [--en|--vi]"
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-humanwrite

## Inputs and owned output

Use the supplied draft, requested edit, audience/genre, glossary and protected regions.
Return the edited prose, a minimal edit diff and a factual-delta record. New claims,
missing facts and unresolved fidelity remain evidence gates. For file inputs follow
[Input preservation](references/_shared/core/policies/preservation-policy.md#input-preservation):
keep encoding and line endings, and keep backups inside the workspace.

## Shared contracts and language

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md).
Normalize arguments with the shared [writer language contract](references/_shared/core/profiles/style/writer-language.md).
`--en` selects English and `--vi` Vietnamese. Both flags conflict: return the error
before creating or changing a draft. Without a flag use the user's explicit target,
then the brief, then the draft's dominant language. Ask one question if still
ambiguous. A bilingual request remains supported; an explicit flag overrides its
output target. These are skill arguments, not a claim of host CLI support.
Read only the selected [VI](references/_shared/core/profiles/style/vi.md) or
[EN](references/_shared/core/profiles/style/en.md) style profile; read both for bilingual output.

## Editing

Read and apply [Humanizer adaptation](references/humanizer-adaptation.md) directly
before editing. It is a contextual Markdown policy in this skill's closure.
Locate the problem in the supplied text, check its context and counterexample,
then make the smallest useful edit. The user's voice, genre and protected fields
override an optional stylistic suggestion. Do not apply an English blacklist to VI.

Preserve quotes, numbers, units, denominators, negation, modality, certainty,
population, time, causality, terminology, citations, limitations and protected
regions. Compare declared factual slots before and after; unresolved changes stop
fidelity acceptance. Translation preserves meaningful ambiguity and source context.
Do not invent anecdotes, authorship, sources, results or citations, or offer AI
detection/evasion. Human taste and scientific fidelity require their own review.

Polish and translation stay here even when the draft is from a paper. Handoff
outline/section/argument/reporting/revision-response authoring to
`nckh-paperwrite`, retaining the normalized locale and flags.
Taste critique belongs to `nckh-taste`. Light polish or translation of existing
marketing text stays here; new copy, a changed angle or a changed CTA goes to
`nckh-copy`. `nckh-write` is a compatibility route that hands polish and
translation here.

## Scoped resources

Read [writer lookups](references/_shared/core/profiles/style/writer-resources.md) only when a
reference helps the requested edit. Humanwrite may read Nature English advice,
Wikisource VI literary rhetoric or PMC English biomedical fidelity samples with
the resource's exact locale/domain/genre. Output VI does not relabel an EN source.
Resource-off keeps core editing usable and returns disabled/no-read. LanguageTool
remains an optional English diagnostic with Java 17 and nested LGPL/rights gates;
do not install it, start a service or call a public server for core editing.
