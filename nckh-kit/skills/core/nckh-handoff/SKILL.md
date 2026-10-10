---
name: nckh-handoff
description: "Create a factual durable handoff or resume packet (bàn giao, tiếp tục phiên sau, mai làm tiếp) with current scope, artifacts, hashes, receipts and open gates. Does not send messages, spawn chats or grant acceptance."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-handoff

## Inputs and owned output

Inputs: Plan/state, actual artifacts/checks, attempts, current authorization and unresolved gates.

Output: A [handoff packet](../../../core/workflows/review-and-handoff.md#handoff-packet) sufficient for the next authorized actor to resume without relying on chat memory, or an inline packet labelled `not-durable` when no location is available.

## Required shared contracts

Read [Authorization](../../../core/policies/authorization-policy.md), [Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and [Acceptance](../../../core/policies/acceptance-policy.md) before work.
Read the route-specific references below when their mode applies. Output language
follows the brief; keep same-agent execution unless delegation has a recorded benefit.

## Workflow and boundaries

Loading or trimming context for the current session belongs to nckh-context; this skill writes the packet for a later or different session. Reopen the task state, current files and linked receipts. Verify current scope, mode, plan/input/profile/closure revisions and output hashes with [check-receipt.py](../../../scripts/check-receipt.py). Distinguish planned, observed and accepted work. File presence is not completion evidence; an artifact without a current receipt is `existing-before-attempt` per the [Attempt ledger](../../../core/workflows/execution.md#attempt-ledger).

Fill every required packet section, plus constraints/non-goals, environment and evidence class of each check, outstanding handles and limitations. Keep raw/private transcripts and labels outside public output; use authorized opaque references.

For resume, reconcile unknown/running attempts before retry and invalidate affected acceptance when hashes or scope changed. Preserve originals, previous failures and user feedback. Never silently convert an incomplete handoff into acceptance.

Write the packet only in the location the packet section allows. Do not fork, spawn, send a message, change another chat, install, publish or accept on the human's behalf merely because the handoff identifies a next actor.

## References

- [Review/handoff](../../../core/workflows/review-and-handoff.md)
- [State schema](../../../core/contracts/task-state.schema.json)
- [Receipt schema](../../../core/contracts/receipt.schema.json)
