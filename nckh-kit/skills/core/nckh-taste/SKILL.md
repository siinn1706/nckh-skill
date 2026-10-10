---
name: nckh-taste
description: "Critique Vietnamese or English voice, rhythm, specificity and genre fit (nhận xét văn phong, góp ý giọng văn, nhận xét giọng văn, hơi sáo) with located suggestions. Advisory critic only; applying edits belongs to nckh-humanwrite. No AI detection or fabricated human taste score."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-taste

## Inputs and owned output

Inputs: Draft, language/genre/audience, user preferences and rights-cleared reference samples when available.

Output: Language-specific rubric, located issues and prioritized suggestions with preference uncertainty.

## Required shared contracts

Read [Authorization](../../../core/policies/authorization-policy.md), [Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and [Acceptance](../../../core/policies/acceptance-policy.md) before work.
Read the route-specific references below when their mode applies. Output language
follows the brief; keep same-agent execution unless delegation has a recorded benefit.

## Workflow and boundaries

Read the appropriate VI or EN profile and the user brief. Critique specificity, rhythm, coherence, register, cliché, reader effort and genre fit using located examples. Separate a grammatical defect, domain-fidelity issue and subjective preference.

Use licensed or user-cleared examples as references, preserve authorship/provenance and acknowledge absent samples. Do not treat a model scalar as human gold, claim AI detection, apply an absolute banned-word list or translate the Vietnamese rubric mechanically into English.

Suggest concrete local edits without changing facts, certainty, citations or protected regions. Applying the edits belongs to nckh-humanwrite. Do not rewrite the whole document unless separately authorized. When a fresh critic context is useful record that benefit; same model/context critique is not independent human confirmation.

Return prioritized recommendations and uncertainty. Human/native reviewers own personal taste acceptance; no authorized reviewer/sample protocol means that gate remains pending.

## References

- [Vietnamese style](../../../core/profiles/style/vi.md)
- [English style](../../../core/profiles/style/en.md)
- [Human review protocol](references/human-taste.md)
- [Scoped resource lookup](references/resource-lookup.md)
