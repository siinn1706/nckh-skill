---
name: nckh-data
description: "Design or verify database schemas, queries, migrations and data integrity (cơ sở dữ liệu, truy vấn SQL, migration dữ liệu, sửa schema, thêm cột, khóa ngoại). Back up and restore-check before any authorized mutation. Research datasets remain nckh-dataset, statistical analysis remains nckh-statistics and APIs remain nckh-backend."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-data

## Inputs and owned output

Inputs: Data contract/current schema, actual owners, sample rights, permitted mutations and backup/rollback route.

Output: Schema/query plan or authorized migration with a restore-checked backup, integrity checks and rollback record.

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

Inspect the actual schema/config/callers and data sensitivity before proposing a change. A design/read-only request permits analysis only. For any schema/data mutation, confirm exact target and authority, then follow this order: back up inside the workspace; restore the backup into an isolated copy and compare row counts and schema with the source; only then mutate. Record the restoration mapping, hashes, counts and permissions. A backup that has not passed the restore check is not verified.

If the user declines a backup before a destructive operation (drop, truncate, bulk delete/update, lossy type change), stop before mutating: state the trade-off and offer a non-destructive alternative such as `ALTER TABLE ... ADD COLUMN`, a new table or a soft delete. Research files with lineage/labels/splits belong to nckh-dataset, scientific analysis to nckh-statistics, and API/service changes to nckh-backend.

Plan reversible steps, constraints, indexes, transactions/concurrency and integrity oracles. Preserve public contracts and user data. Test on an authorized isolated fixture before a live migration when risk warrants it; fixtures are not proof a production backup restores.

Execute only approved targets/operations, verify affected rows/constraints and record the real result. Never drop, bulk update or migrate because a database URL exists. No destructive broad reset or copied personal data in source/dist.

On failure stop safely, preserve receipts and restore only owned changes under the approved rollback. Later user edits are conflicts. Return current data integrity and remaining live/restore acceptance gates.

## References

- [Execution/authority modes](../../../core/workflows/execution.md)
- [Review/handoff](../../../core/workflows/review-and-handoff.md)
