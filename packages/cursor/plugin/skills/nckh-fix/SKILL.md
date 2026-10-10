---
name: nckh-fix
description: "Repair an authorized bug (sửa lỗi, sửa bug, khắc phục lỗi, sửa giúp, khắc phục giúp) using a proven cause and focused regression evidence, with a bounded diagnosis first when the cause is unknown. Diagnose-only requests remain nckh-debug. Does not authorize unrelated refactors or weakening tests."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-fix

## Inputs and owned output

Inputs: Bug, expected repaired behavior, diagnosis/reproduction, authorized files and regression oracle.

Output: Cause-aligned patch, regression checks run in this attempt and remaining risks.

## Required contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Run commands under [Command discipline](references/_shared/core/workflows/execution.md#command-discipline) and [Host shell robustness](references/_shared/core/workflows/execution.md#host-shell-robustness),
label claims with the [Attempt ledger](references/_shared/core/workflows/execution.md#attempt-ledger) and keep inputs per
[Input preservation](references/_shared/core/policies/preservation-policy.md#input-preservation).
Output follows the brief's locale. Same-agent is the default. Use
[model/context policy](references/_shared/core/workflows/model-and-context.md) before delegation.

## Workflow and boundaries

Inspect the reproduction and cause before editing. A request that asks for a repair belongs here even when the cause is unknown: perform a bounded cause-first diagnosis, then fix. A request that only asks why, without a repair, belongs to nckh-debug. Choose the smallest fix that restores the expected contract and preserves explicit user decisions, existing patterns and unrelated changes.

When debug transfers control in the same session, read its bounded packet and reuse the proven cause and input receipts. Recheck the live repair grant, allowed product paths and unresolved gates before creating a repair preimage or editing. A packet records existing authority and cannot create it. Reuse a current grant for the same action and scope; an explicit handoff-only/no-edit request, missing authority or unspecified product paths leaves repair pending with no product mutation. Fix owns the authorized patch and focused regression checks; debug owns diagnosis and nckh-cook retains phase and attempt state.

Establish a meaningful regression oracle for the actual failure. Implement real behavior, not fake fixtures or shortcuts that merely satisfy a check. Run the focused check, then broaden only for changed callers/public contracts or a concrete remaining risk.

Repair regressions within scope. Do not delete, skip or weaken a failing test to declare success; record unavailable tools as pending. Do not silently turn a bug fix into a full refactor, dependency upgrade, public-contract redesign or deployment. A fix that changes a schema or stored data passes the nckh-data backup and restore-check gate before the mutation.

Review the patch and hand off files, cause, evidence and limits. Product repair needs current authority; review/diagnosis alone does not grant it. nckh-cook owns phase/attempt progression when this fix belongs to a larger task.

## References

- [Execution/authority modes](references/_shared/core/workflows/execution.md)
- [Review/handoff](references/_shared/core/workflows/review-and-handoff.md)
- [Scoped resource lookup](references/resource-lookup.md)
