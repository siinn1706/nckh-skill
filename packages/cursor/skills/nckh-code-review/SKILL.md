---
name: nckh-code-review
description: "Review a current diff or pull request for concrete bugs, contract and regression risks. Review-only returns located findings without repairs."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-code-review

## Inputs and owned output

Inputs: Current diff/source, callers, contract/tests and explicit user decisions.

Output: Actionable findings with verified file/line or observation, severity and repair direction.

## Required contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default. Use
[model/context policy](references/_shared/core/workflows/model-and-context.md) before delegation.

## Workflow and boundaries

Read the complete affected source and callers for each relevant diff. Check correctness, public contracts, state/data ownership, error paths and regression evidence. A finding needs a demonstrable failure path or concrete contract violation; avoid unsupported style churn or abstract objections.

Identify actual protected data/assets before escalating a security concern. Do not reverse a user decision or a source/test-verified invariant because of a generic audit concern; present new evidence and trade-offs when a decision is needed.

Verify locations against the current diff. Distinguish observed failures from unverified risks and missing checks. Same-model fresh-context review offers context separation, not human/domain independence.

Return prioritized findings, sufficient evidence, affected owner and scoped recommendation. Do not repair product files under a review-only request or infer merge/publish authorization. The Core review aggregates final gates rather than rerunning this domain audit.

## References

- [Execution/authority modes](references/_shared/core/workflows/execution.md)
- [Review/handoff](references/_shared/core/workflows/review-and-handoff.md)
- [Scoped resource lookup](references/resource-lookup.md)
