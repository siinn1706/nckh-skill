---
name: nckh-market-research
description: "Research market, customer or competitor questions (nghiên cứu thị trường, phân tích đối thủ, khảo sát khách hàng, đối thủ chính, app đối thủ) with sourced comparisons and explicit unknowns. Scientific literature reviews belong to nckh-research. No invented market size, customer quotes or private-data scraping."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-market-research

## Inputs and owned output

Inputs: Question, audience/market/geography/time, source access, rights and desired comparison.

Output: Sourced market/customer map, competitor axes, unknowns and evidence-backed implications.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Market, customer and competitor questions belong here; a review of scientific literature belongs to nckh-research.

Define geography, customer segment, time range and decision before searching. Read actual accessible sources and preserve source/version/as-of, methods and limits. Distinguish customer observations, vendor claims, analyst estimates and hypotheses.

Competitor analysis belongs here: choose relevant comparison axes, verify product/pricing claims against current primary sources and record unknown cells. Do not fill missing market size, adoption, customer quotations or performance with plausible numbers.

Use the shared evidence method for factual claims; marketing does not require Q1/Q2 or paper structure unless the brief says so. Separate public access, dataset consent/evaluation and redistribution rights. No private scraping or contact uploads.

Return the bounded map and implications with counterevidence and provenance. nckh-marketing-plan owns channel/budget decisions; this research does not launch a campaign, spend or publish.

## References

- [Brief schema](../../../core/contracts/brief.schema.json)
- [Claim schema](../../../core/contracts/claim.schema.json)
- [Provider boundaries](../../../extensions/providers/marketing/contract.json)
- [Scoped resource lookup](references/resource-lookup.md)
