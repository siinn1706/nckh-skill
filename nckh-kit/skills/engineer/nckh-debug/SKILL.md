---
name: nckh-debug
description: "Diagnose a symptom or failing test with reproduction and a traced cause. Diagnose-only requests end before product edits."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-debug

## Inputs and owned output

Inputs: Symptom, expected behavior, reproduction, environment and bounded repository/log access.

Output: Reproduction receipt, traced cause, counter-hypotheses and cause-aligned repair options.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default. Use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.

## Workflow and boundaries

Frame the expected repaired behavior and safety boundary. Inspect the owning source, caller, relevant tests and actual error before proposing a fix. Reproduce narrowly when permitted; record command, environment, output and input hashes.

Trace the failure to a cause that explains the observed symptom. Test a competing hypothesis when needed; a passing unrelated test or plausible story is insufficient. Distinguish deterministic reproduction, runtime evidence and unverified inference. Do not hide a failed check.

For diagnosis-only work return the cause, evidence and focused options without modifying product files. If a repair is requested, hand the proven cause to fix while cook owns execution state. Avoid speculative retries or unrelated refactors, and preserve existing dirty changes.

## References

- [Execution/authority modes](../../../core/workflows/execution.md)
- [Review/handoff](../../../core/workflows/review-and-handoff.md)
- [Scientific task evaluation](../../core/nckh-aiops/references/benchmark-protocols.md): code diagnosis does not establish incident RCA or benchmark efficacy.
