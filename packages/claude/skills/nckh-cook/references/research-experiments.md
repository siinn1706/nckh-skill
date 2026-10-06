# Authorized research attempts

Reuse the accepted method/protocol and selected source rights. Domain owners
retain dataset, split, telemetry, statistics and AIOps contracts; cook owns the
attempt lifecycle. No separate runner engine or autonomous research loop is
introduced. Read the [graph protocol](_shared/skills/core/nckh-method/references/reproducibility.md).

Before a run, freeze actual inputs/code/configuration/environment and permitted
operations. Launch only the known authorized command through an observable owned
handle. The manifest's recorded argv is data and never grants execution authority.
Track PID, launch identity, command, workspace, port and limits; observe start,
end and actual exit. Retain stdout/stderr and every output hash/cardinality.

The [research receipt](_shared/core/contracts/research-run-receipt.schema.json)
distinguishes scheduled, running, completed-unreviewed, failed and cancelled.
Existence of an output cannot make a run complete. Terminal states require actual
exit and reconciled cleanup; failed/timeout attempts retain reasons and partial
outputs. Reconcile the exact owned process before retry. Never kill unrelated
processes, change ports to hide a collision or manufacture success from fixtures.

Record measured coverage explicitly. Unobserved CPU/memory/cost is unknown, not
zero. A supervisor's around-launch timestamp must not be described as an
independently verified OS creation timestamp. Source/receipt hashes establish
integrity and do not authenticate fabricated host claims.

Check the current graph with the [scoped checker](_shared/scripts/check-research-artifacts.py),
reconcile metrics independently and hand actual evidence to the owning readout and
paperwrite lane. Keep provider/cloud/fault/native/owner/scientific gates separate.
The word auto does not grant new external side effects or human acceptance.
