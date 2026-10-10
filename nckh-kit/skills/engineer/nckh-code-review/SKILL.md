---
name: nckh-code-review
description: "Review a current diff or pull request (review mã nguồn, xem lại diff, rà soát pull request, có thể gây lỗi, trước khi merge, pull request số) for concrete bugs, contract and regression risks, always stating the inspected scope. Plans, research writing and gate matrices remain nckh-review; security-sensitive findings go to nckh-security. Review-only returns located findings without repairs."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-code-review

## Inputs and owned output

Inputs: Current diff/source, callers, contract/tests and explicit user decisions.

Output: Inspected scope (revisions or snapshot, files and commands read) plus actionable findings with file/line or observation, severity and repair direction. A review with no finding still reports its inspected scope.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Run commands under [Command discipline](../../../core/workflows/execution.md#command-discipline) and [Host shell robustness](../../../core/workflows/execution.md#host-shell-robustness),
label claims with the [Attempt ledger](../../../core/workflows/execution.md#attempt-ledger) and keep inputs per
[Input preservation](../../../core/policies/preservation-policy.md#input-preservation).
Output follows the brief's locale. Same-agent is the default. Use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.

## Workflow and boundaries

Read the complete affected source and callers for each relevant diff. Without a Git repository or diff, review the supplied snapshot as files, say plainly that no diff or base revision exists, and do not invent one; Git operations themselves belong to nckh-git. Check correctness, public contracts, state/data ownership, error paths and regression evidence. A finding needs a demonstrable failure path or concrete contract violation; avoid unsupported style churn or abstract objections.

Identify actual protected data/assets before handing a security-sensitive finding to nckh-security. Do not reverse a user decision or a source/test-verified invariant because of a generic audit concern; present new evidence and trade-offs when a decision is needed.

Verify locations against the current diff. Distinguish observed failures from unverified risks and missing checks. Same-model fresh-context review offers context separation, not human/domain independence.

Return prioritized findings, sufficient evidence, affected owner and scoped recommendation. Do not repair product files under a review-only request or infer merge/publish authorization. nckh-review aggregates final gates rather than rerunning this domain audit.

## References

- [Execution/authority modes](../../../core/workflows/execution.md)
- [Review/handoff](../../../core/workflows/review-and-handoff.md)
- [Scoped resource lookup](references/resource-lookup.md)
