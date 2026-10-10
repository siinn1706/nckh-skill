---
name: nckh-context
description: "Create a minimum-sufficient context/evidence loading or retirement packet (nạp ngữ cảnh, giảm ngữ cảnh, tóm tắt ngữ cảnh, trong ngữ cảnh, rút gọn ngữ cảnh, bỏ khỏi ngữ cảnh). Reports measured or unknown usage without universal windows or deleting history. Durable resume packets for a later session remain nckh-handoff."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-context

## Inputs and owned output

Inputs: Task, current context/evidence ownership, usable-window/usage telemetry if exposed.

Output: Selective load/retire plan and bounded packet preserving required instructions and verification reserve.

## Required contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Run commands under [Command discipline](references/_shared/core/workflows/execution.md#command-discipline) and [Host shell robustness](references/_shared/core/workflows/execution.md#host-shell-robustness),
label claims with the [Attempt ledger](references/_shared/core/workflows/execution.md#attempt-ledger) and keep inputs per
[Input preservation](references/_shared/core/policies/preservation-policy.md#input-preservation).
Output follows the brief's locale. Same-agent is the default. Use
[model/context policy](references/_shared/core/workflows/model-and-context.md) before delegation.

## Workflow and boundaries

Identify the active outcome, decisions, open gates and the evidence needed for the next step. Load metadata first, then current phase/owner source and complete required instructions. Use exact paths/hashes rather than dumping a catalog, transcript or repository.

Separate active evidence from historical records while preserving retrieval links and original/failed attempts. Retiring context does not erase past cost or authorize deletion. nckh-handoff owns the durable packet format.

Record usable model window, loaded usage and output/reasoning/verification reserve only when actually measurable. Unknown values stay unknown. Cached tokens still occupy context; windows across agents cannot be added. Do not apply a universal 40k cap.

If the task cannot fit, partition bounded independent evidence or hand off with traceable decisions; do not cut mandatory verification/scope to claim compliance. Delegate only with an actual isolation/parallel/review benefit and available permissions.

## References

- [Execution/authority modes](references/_shared/core/workflows/execution.md)
- [Review/handoff](references/_shared/core/workflows/review-and-handoff.md)
