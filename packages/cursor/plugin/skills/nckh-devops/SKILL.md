---
name: nckh-devops
description: "Build, deploy or operate an explicitly authorized route with environment, health and rollback evidence. Local builds do not imply deployment or cloud authority."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-devops

## Inputs and owned output

Inputs: Operational target/owner, environment, artifact revision, allowed operations and rollback route.

Output: Reproducible build or authorized rollout/health/rollback receipt with unresolved gates.

## Required contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default. Use
[model/context policy](references/_shared/core/workflows/model-and-context.md) before delegation.

## Workflow and boundaries

Resolve the actual operational route from repository/docs/live read-only evidence. Separate local build, staging, deployment and genuine acceptance. Inspect settings/runtime wiring/assets/security/backups and provider gates before claiming readiness.

Before starting a server/watcher/tunnel check project/port owners; reuse or stop only owned stale processes. Track command, PID, deterministic port and workspace. Clean up processes started for the task; never kill unrelated user/session/OS processes.

Use reproducible inputs and actual build output. Deployment/cloud/webhook/DNS/credential changes require explicit target authority; a token or auto mode cannot grant it. Preserve sandbox and egress permissions.

For an authorized rollout verify health and rollback with actual observations. Keep private config/receipts out of source/dist. Update the smallest owning operational docs when a route changes. Return a scoped go/no-go and exact open gates, not production approval from a local smoke check.

## References

- [Execution/authority modes](references/_shared/core/workflows/execution.md)
- [Review/handoff](references/_shared/core/workflows/review-and-handoff.md)
- [Research environment](references/research-environment.md)
