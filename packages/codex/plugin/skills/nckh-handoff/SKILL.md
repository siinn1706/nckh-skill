---
name: nckh-handoff
description: "Create a factual durable handoff or resume packet with current scope, artifacts, hashes, receipts and open gates. Does not send messages, spawn chats or grant acceptance."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-handoff

## Inputs and owned output

Inputs: Plan/state, actual artifacts/checks, attempts, current authorization and unresolved gates.

Output: A durable packet sufficient for the next authorized actor to resume without relying on chat memory.

## Required shared contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md), [Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and [Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Read the route-specific references below when their mode applies. Output language
follows the brief; keep same-agent execution unless delegation has a recorded benefit.

## Workflow and boundaries

Reopen the task state, current files and linked receipts. Verify current scope, mode, plan/input/profile/closure revisions and output hashes. Distinguish planned, observed and accepted work. File presence is not completion evidence.

Include outcome, constraints/non-goals, authority reference, completed artifacts with exact paths/hashes, checks with commands/results/environment and evidence class, outstanding handles, failed/pending/stale gates, limitations, next action and responsible owner. Keep raw/private transcripts and labels outside public output; use authorized opaque references.

For resume, reconcile unknown/running attempts before retry and invalidate affected acceptance when hashes or scope changed. Preserve originals, previous failures and user feedback. Never silently convert an incomplete handoff into acceptance.

Write the packet only in the requested authorized location. Do not fork, spawn, send a message, change another chat, install, publish or accept on the human's behalf merely because the handoff identifies a next actor.

## References

- [Review/handoff](references/_shared/core/workflows/review-and-handoff.md)
- [State schema](references/_shared/core/contracts/task-state.schema.json)
- [Receipt schema](references/_shared/core/contracts/receipt.schema.json)
