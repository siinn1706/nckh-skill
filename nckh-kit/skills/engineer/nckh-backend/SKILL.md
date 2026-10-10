---
name: nckh-backend
description: "Build or change authorized APIs, services or auth boundaries (viết API, xây dựng backend, xác thực đăng nhập, thêm endpoint, kiểm tra quyền) with interface, validation and data-flow checks. Schema migrations, queries and data integrity remain nckh-data; payment/provider scope stays explicit."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-backend

## Inputs and owned output

Inputs: API/service contract, clients, auth/data flows, stack and authorized operations.

Output: Scoped implementation with input/error/auth contracts and relevant regression/integration evidence.

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

Read callers and current interface before changing behavior. Define inputs/outputs/errors, authentication/authorization, idempotency where needed, data ownership and failure boundaries. Preserve public contracts unless the user accepted the change.

Implement actual validation and business behavior using local conventions. Trace trust boundaries and protected data; do not infer provider response schemas from request examples. Test touched behavior and affected clients, separating local tests from real provider evidence.

Database schema/migrations belong to nckh-data and require its backup gate and authority. Auth/payment/framework providers are opt-in extensions with real availability, credentials and egress gates. Do not expand pricing, payment, provisioning or deployment scope.

Return the implementation, checks and unresolved integration gates. Credential presence is not permission, local parsing is not production readiness and auto cannot grant external mutations.

## References

- [Execution/authority modes](../../../core/workflows/execution.md)
- [Review/handoff](../../../core/workflows/review-and-handoff.md)
