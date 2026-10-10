---
name: nckh-seo
description: "Audit search intent, crawl, canonical/index controls and on-page discoverability (tối ưu SEO, thứ hạng tìm kiếm, kiểm tra noindex, rớt hạng, lập chỉ mục, lên top Google) and prioritize evidenced fixes. Form or funnel friction belongs to nckh-cro. Does not guarantee rankings or activate paid tools by default."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-seo

## Inputs and owned output

Inputs: Site/content scope, audience/search intent, actual data, tools and permitted inspection.

Output: Intent/crawl/on-page findings with evidence, prioritized fixes and measurement limits.

## Required contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](references/_shared/core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Search intent, crawl, canonical and index controls belong here; conversion friction in forms, funnels or onboarding belongs to nckh-cro.

Inspect current content/site behavior and permitted search/crawl inputs. Map audience queries/intent to pages and document actual evidence/as-of. Distinguish observed crawl/index/search data from proposed keyword hypotheses.

Review task-relevant titles/headings, content usefulness, internal links, canonical/index controls, structured data truth, accessibility and performance. Verify the owning implementation before recommending changes. When citing search-engine guidance, give its source URL and as-of or access date; vendor guidance is vendor-specific.

Prioritize by concrete user/search impact and effort; keep ranking uncertainty and attribution limits. Avoid guaranteed rank/traffic, keyword stuffing, unsupported schema claims or ungranted scraping/account access.

Paid suites/provider connectors are optional qualified extensions. Return findings and prioritized fixes. An authorized local fix is written to a new copy with hashes before and after, never over the supplied file, as [Input preservation](references/_shared/core/policies/preservation-policy.md#input-preservation) requires. No subscription/spend, publishing or exploit behavior follows from an SEO audit.

## References

- [Brief schema](references/_shared/core/contracts/brief.schema.json)
- [Claim schema](references/_shared/core/contracts/claim.schema.json)
- [Provider boundaries](references/_shared/extensions/providers/marketing/contract.json)
