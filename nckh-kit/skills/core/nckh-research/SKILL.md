---
name: nckh-research
description: "Discover and read scientific sources, perform bounded literature review (tổng quan tài liệu, tìm tài liệu, đọc bài báo, tìm bài báo, tìm các nghiên cứu) and synthesize evidence or gaps in narrative, scoping or systematic mode. Market, customer and competitor questions belong to nckh-market-research; task plans to nckh-plan; method design to nckh-method; claim verification to nckh-evidence."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-research

## Inputs and owned output

Inputs: Research question, review mode, databases/source access, scope/date/locale, venue policy if required.

Output: Search/screening log, source/reader cards, evidence/counterevidence map and bounded synthesis with open gaps.

## Required shared contracts

Read [Authorization](../../../core/policies/authorization-policy.md), [Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and [Acceptance](../../../core/policies/acceptance-policy.md) before work.
Read the route-specific references below when their mode applies. Output language
follows the brief; keep same-agent execution unless delegation has a recorded benefit.

## Workflow and boundaries

Choose narrative, scoping or systematic review from the brief. Narrative work may use a focused search; scoping maps coverage and exclusion rules; systematic work needs a frozen question, protocol, search sources/queries/dates, inclusion/exclusion, deduplication, screening and extraction before synthesis. Do not call an opportunistic search systematic.

Record queries, database/source, as-of, inclusion/exclusion and actual access. Discovery services and ranking hints identify candidates, not verified findings. Read the available source version, keep exact locators and context, and state metadata-only or abstract-only limits.

Create reader cards with question, methods/data/argument, observed results, limits and counterevidence. Literary studies preserve edition, translator, original quotation and historical/contextual scope. Method design belongs to nckh-method; claim/quote support is verified by nckh-evidence. Market, customer and competitor questions go to nckh-market-research; a task plan with phase files goes to nckh-plan.

Synthesize only after mapping source -> evidence -> claims. Distinguish agreement, contradiction, insufficient access and hypothesis. A gap is bounded by the observed search; do not invent novelty from absent results. Q1/Q2 filters require system/category/year evidence and are task-specific. Preserve venue isolation.

Stop with sourced synthesis and unresolved checks; do not invent sources/results or collect private/full-text material beyond access/evaluation/redistribution rights.

## References

- [Review modes](references/review-modes.md)
- [Software/AIOps search and appraisal](references/software-research-review.md)
- [Source schema](../../../core/contracts/source.schema.json)
- [Evidence schema](../../../core/contracts/evidence.schema.json)
