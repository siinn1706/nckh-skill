---
name: nckh-test
description: "Design or run meaningful tests for touched behavior (chạy test, viết test, kiểm thử) and report actual failures/results. Tracing why a symptom or failing test occurs remains nckh-debug. Unit evidence does not certify live integration or acceptance."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-test

## Inputs and owned output

Inputs: Behavior/contract, source diff, test tools/environment, data rights and permitted side effects.

Output: Test design and actual run receipts with counts, failures and evidence limits.

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

Select the narrowest oracle that can falsify the touched behavior. Read existing test utilities and callers; tests should distinguish correct from incorrect outcomes, not mirror implementation text or create fake success. Reversible trivial edits need proportionate verification.

Execute only permitted tests, each as its own command with its own exit, and keep environment, counts and source/input hashes. Diagnosing why a test fails belongs to nckh-debug. Empty discovery is a failure to verify. Report failures directly; never hide them behind unrelated passing checks.

Broaden for shared/public contract changes or unresolved risk. Browser and provider integration require an available qualified driver, disposable scope and separate permission where needed; a unit fixture is not a live host/provider run.

Preserve failures and pending tools. Under authorized TDD characterize behavior before refactor and rerun it. Return a receipt that labels deterministic, agent, host and human evidence separately, with no fabricated screenshots or copied old pass.

## References

- [Execution/authority modes](../../../core/workflows/execution.md)
- [Review/handoff](../../../core/workflows/review-and-handoff.md)
- [Scoped resource lookup](references/resource-lookup.md)
- [Scientific evaluation protocol](../../core/nckh-aiops/references/benchmark-protocols.md): contract fixtures, actual run oracles and scientific acceptance are distinct.
