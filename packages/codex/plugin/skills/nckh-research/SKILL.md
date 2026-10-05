---
name: nckh-research
description: "Discover and read sources, perform bounded literature review and synthesize evidence or gaps. Use narrative, scoping or systematic mode; novelty and claim support require evidence."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-research

## Inputs and owned output

Inputs: Research question, review mode, databases/source access, scope/date/locale, venue policy if required.

Output: Search/screening log, source/reader cards, evidence/counterevidence map and bounded synthesis with open gaps.

## Required shared contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md), [Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and [Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Read the route-specific references below when their mode applies. Output language
follows the brief; keep same-agent execution unless delegation has a recorded benefit.

## Workflow and boundaries

Choose narrative, scoping or systematic review from the brief. Narrative work may use a focused search; scoping maps coverage and exclusion rules; systematic work needs a frozen question, protocol, search sources/queries/dates, inclusion/exclusion, deduplication, screening and extraction before synthesis. Do not call an opportunistic search systematic.

Record queries, database/source, as-of, inclusion/exclusion and actual access. Discovery services and ranking hints identify candidates, not verified findings. Read the available source version, keep exact locators and context, and state metadata-only or abstract-only limits.

Create reader cards with question, methods/data/argument, observed results, limits and counterevidence. Literary studies preserve edition, translator, original quotation and historical/contextual scope. Method design belongs to method; claim/quote support is recorded under evidence.

Synthesize only after mapping source -> evidence -> claims. Distinguish agreement, contradiction, insufficient access and hypothesis. A gap is bounded by the observed search; do not invent novelty from absent results. Q1/Q2 filters require system/category/year evidence and are task-specific. Preserve venue isolation.

Stop with sourced synthesis and unresolved checks; do not invent sources/results or collect private/full-text material beyond access/evaluation/redistribution rights.

## References

- [Review modes](references/review-modes.md)
- [Source schema](references/_shared/core/contracts/source.schema.json)
- [Evidence schema](references/_shared/core/contracts/evidence.schema.json)
