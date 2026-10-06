---
name: nckh-evidence
description: "Verify factual claims, quotations, citations and statistics against actual sources. Distinguish source identity/status/ranking from semantic support and human acceptance."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-evidence

## Inputs and owned output

Inputs: Claims/quotes/citations, actual source versions, locators, task scope and current profiles.

Output: Source/evidence/claim ledger with separate identity, access, locator, support, contradiction and allowed-wording verdicts.

## Required shared contracts

Read [Authorization](../../../core/policies/authorization-policy.md), [Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and [Acceptance](../../../core/policies/acceptance-policy.md) before work.
Read the route-specific references below when their mode applies. Output language
follows the brief; keep same-agent execution unless delegation has a recorded benefit.

## Workflow and boundaries

Resolve source identity/version/access/status and rights before reading. A DOI/metadata match validates identity only. Check correction/retraction and freshness at relevant triggers. Ranking requires issuer/system, category, metric year, as-of and evidence; an article entry or public PDF is insufficient.

For each quote/value retain original text, unit/denominator/population/time, exact page/line/section/table/figure locator and surrounding context. OCR text needs actual visual comparison before an exact-quote pass. Missing full text or a locator remains unverified; never invent it. Literary evidence binds edition/translator and original language.

Evaluate whether the observed evidence supports the precise claim scope, certainty and causal language. Record supported/contradicted/insufficient/unverified separately from identity and ranking, along with counterevidence and permissible wording. Unseen methods/results cannot be supported from metadata.

For a supplied draft audit factual deltas without rewriting the entire piece. Invalidate dependent claims when source/profile/version changes. Route method validity and human scientific acceptance to their owners; a semantic model judgment is not domain signoff.

Return a located ledger and bounded corrections. Do not polish unrelated prose or manufacture evidence/citations to fill a gap.

## References

- [Verdicts and locators](references/verdicts-and-locators.md)
- [Source schema](../../../core/contracts/source.schema.json)
- [Evidence schema](../../../core/contracts/evidence.schema.json)
- [Claim schema](../../../core/contracts/claim.schema.json)
- [Scoped resource lookup](references/resource-lookup.md)
