---
name: nckh-data
description: "Design or verify schemas, queries, migrations and data integrity. Back up before any authorized schema/data mutation and preserve rollback evidence."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-data

## Inputs and owned output

Inputs: Data contract/current schema, actual owners, sample rights, permitted mutations and backup/rollback route.

Output: Schema/query plan or authorized migration with verified backup, integrity checks and rollback record.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default. Use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.

## Workflow and boundaries

Inspect the actual schema/config/callers and data sensitivity before proposing a change. A design/read-only request permits analysis only. For any schema/data mutation, confirm exact target and authority, take a usable backup first and record restoration mapping/hash and permissions.

Plan reversible steps, constraints, indexes, transactions/concurrency and integrity oracles. Preserve public contracts and user data. Test on an authorized isolated fixture before a live migration when risk warrants it; fixtures are not proof a production backup restores.

Execute only approved targets/operations, verify affected rows/constraints and record the real result. Never drop, bulk update or migrate because a database URL exists. No destructive broad reset or copied personal data in source/dist.

On failure stop safely, preserve receipts and restore only owned changes under the approved rollback. Later user edits are conflicts. Return current data integrity and remaining live/restore acceptance gates.

## References

- [Execution/authority modes](../../../core/workflows/execution.md)
- [Review/handoff](../../../core/workflows/review-and-handoff.md)
