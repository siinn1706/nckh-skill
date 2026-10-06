---
name: nckh-seo
description: "Audit search intent, crawl/content/on-page discoverability and prioritize evidenced fixes. Does not guarantee rankings or activate paid tools by default."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-seo

## Inputs and owned output

Inputs: Site/content scope, audience/search intent, actual data, tools and permitted inspection.

Output: Intent/crawl/on-page findings with evidence, prioritized fixes and measurement limits.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Inspect current content/site behavior and permitted search/crawl inputs. Map audience queries/intent to pages and document actual evidence/as-of. Distinguish observed crawl/index/search data from proposed keyword hypotheses.

Review task-relevant titles/headings, content usefulness, internal links, canonical/index controls, structured data truth, accessibility and performance. Verify the owning implementation before recommending changes.

Prioritize by concrete user/search impact and effort; keep ranking uncertainty and attribution limits. Avoid guaranteed rank/traffic, keyword stuffing, unsupported schema claims or ungranted scraping/account access.

Paid suites/provider connectors are optional qualified extensions. Return findings and authorized local fixes only; no subscription/spend, publishing or exploit behavior follows from an SEO audit.

## References

- [Brief schema](../../../core/contracts/brief.schema.json)
- [Claim schema](../../../core/contracts/claim.schema.json)
- [Provider boundaries](../../../extensions/providers/marketing/contract.json)
