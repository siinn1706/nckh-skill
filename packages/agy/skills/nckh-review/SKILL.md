---
name: nckh-review
description: "Review a plan, research writing or delivered artifact against scoped acceptance and consolidate evidence-backed findings and a gate matrix (rà soát kế hoạch, đánh giá bản thảo, duyệt kết quả). Not for code diffs or pull requests; review-only requests do not authorize repair."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-review

## Inputs and owned output

Inputs: Current plan, research writing or non-code artifact, plan/brief, checks, evidence, explicit user decisions and domain gates.

Output: Located findings with severity, evidence, owner/action and an independent gate matrix with a scoped recommendation.

## Required shared contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md), [Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and [Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Read the route-specific references below when their mode applies. Output language
follows the brief; keep same-agent execution unless delegation has a recorded benefit.

## Workflow and boundaries

A code diff or pull request belongs to nckh-code-review; this skill reviews plans, research writing and consolidated gate matrices. Read current artifacts and verify receipt hashes with [check-receipt.py](references/_shared/scripts/check-receipt.py) before relying on earlier checks; for a plan also run [check-plan.py](references/_shared/scripts/check-plan.py). Claims follow the [Attempt ledger](references/_shared/core/workflows/execution.md#attempt-ledger). Compare the result to its outcome and acceptance, affected callers/public contracts, evidence/factual fidelity, methodology, rights/privacy, native visual requirements and runtime scope as relevant.

Separate source identity, semantic support, deterministic checks, model critique, human/domain acceptance and publication authority. Reuse valid checks from unchanged source/inputs/environment. Treat stale or missing evidence as pending. Do not duplicate full domain audits when located findings already establish the issue.

A finding needs a concrete failure mode and evidence, not an abstract concern or score. Identify what the code/data actually protects before proposing security changes. Verified decisions stand unless new evidence changes the context. Present trade-offs and wait before reversing an explicit user decision.

Return actionable findings and a gate matrix. A numeric score or human-reviewed event cannot override required pending/fail gates. A model review is not peer review or independent scientific confirmation. Review-only work may write its requested report and cannot make product repairs or accept for a human. For "review then fix", deliver the findings first, then record the route change and hand the repair to nckh-cook, or to nckh-fix for a code defect.

## References

- [Review/handoff](references/_shared/core/workflows/review-and-handoff.md)
- [Claim schema](references/_shared/core/contracts/claim.schema.json)
