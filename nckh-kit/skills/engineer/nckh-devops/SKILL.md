---
name: nckh-devops
description: "Build, deploy or operate an explicitly authorized route (triển khai lên server, cấu hình CI/CD, dựng môi trường, deploy lên, đưa lên server) with environment, health and rollback evidence. Local builds do not imply deployment or cloud authority. Scientific RCA, anomaly, forecasting and agent evaluations remain nckh-aiops."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-devops

## Inputs and owned output

Inputs: Operational target/owner, environment, artifact revision, allowed operations and rollback route.

Output: Reproducible build or authorized rollout/health/rollback receipt with unresolved gates.

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

Resolve the actual operational route from repository/docs/live read-only evidence. Separate local build, staging, deployment and genuine acceptance. Inspect settings/runtime wiring/assets/security/backups and provider gates before claiming readiness.

Before starting a server/watcher/tunnel check project/port owners; reuse or stop only owned stale processes. Track command, PID, deterministic port and workspace. Clean up processes started for the task; never kill unrelated user/session/OS processes. When an unknown process holds the port, report its PID and owner, ask the user and wait; do not kill it or silently move to another port.

Use reproducible inputs and actual build output; build output never overwrites an input, template or source file. Deployment/cloud/webhook/DNS/credential changes require explicit target authority; a token or auto mode cannot grant it. Preserve sandbox and egress permissions.

For an authorized rollout verify health and rollback with actual observations. Keep private config/receipts out of source/dist. Update the smallest owning operational docs when a route changes. Return a scoped go/no-go and exact open gates, not production approval from a local smoke check.

## References

- [Execution/authority modes](../../../core/workflows/execution.md)
- [Review/handoff](../../../core/workflows/review-and-handoff.md)
- [Research environment](references/research-environment.md)
