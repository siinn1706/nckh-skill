---
name: nckh-fix
description: "Repair an authorized bug using a proven cause and focused regression evidence. Does not authorize unrelated refactors or weakening tests."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-fix

## Inputs and owned output

Inputs: Bug, expected repaired behavior, diagnosis/reproduction, authorized files and regression oracle.

Output: Cause-aligned patch, real regression checks and remaining risks.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default. Use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.

## Workflow and boundaries

Inspect the reproduction and cause before editing. If diagnosis is missing, perform a bounded cause-first investigation. Choose the smallest fix that restores the expected contract and preserves explicit user decisions, existing patterns and unrelated changes.

Establish a meaningful regression oracle for the actual failure. Implement real behavior, not fake fixtures or shortcuts that merely satisfy a check. Run the focused check, then broaden only for changed callers/public contracts or a concrete remaining risk.

Repair regressions within scope. Do not delete, skip or weaken a failing test to declare success; record unavailable tools as pending. Do not silently turn a bug fix into a full refactor, dependency upgrade, public-contract redesign or deployment.

Review the patch and hand off files, cause, evidence and limits. Product repair needs current authority; review/diagnosis alone does not grant it. Cook owns phase/attempt progression when this fix belongs to a larger task.

## References

- [Execution/authority modes](../../../core/workflows/execution.md)
- [Review/handoff](../../../core/workflows/review-and-handoff.md)
- [Scoped resource lookup](references/resource-lookup.md)
