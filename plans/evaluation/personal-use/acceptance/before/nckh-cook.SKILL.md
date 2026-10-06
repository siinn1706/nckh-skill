---
name: nckh-cook
description: "Execute an authorized task or accepted plan with validation, repair and review. Use --auto or --interactive; auto preserves permissions and mandatory gates."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-cook

## Inputs and owned output

Inputs: Task or accepted plan, current revision/authorization, execution mode, tools and domain acceptance.

Output: Authorized artifacts, durable phase/attempt state, actual verification receipts, scoped review and factual handoff.

## Required shared contracts

Read Authorization (historical evidence path: `../../../core/policies/authorization-policy.md`; unavailable in the cleaned checkout), Evidence (historical evidence path: `../../../core/policies/evidence-policy.md`; unavailable in the cleaned checkout),
Preservation (historical evidence path: `../../../core/policies/preservation-policy.md`; unavailable in the cleaned checkout) and Acceptance (historical evidence path: `../../../core/policies/acceptance-policy.md`; unavailable in the cleaned checkout) before work.
Read the route-specific references below when their mode applies. Output language
follows the brief; keep same-agent execution unless delegation has a recorded benefit.

## Workflow and boundaries

Read the plan and inspect current artifacts before execution. Resolve authority from the human request and host policy. A prior design approval alone is insufficient, while an explicit cook request covers reversible implementation within scope.

Select exactly one mode. --auto completes authorized phases without routine pauses. --interactive declares substantive review boundaries, gives the exact artifact/hash and checks, then waits for approve/request-changes/reject before downstream material work. Preserve an approved mode; if no mode is specified state the proposed interactive default. Reject conflicting or unsupported flags. There is no stable --no-test.

Inspect, implement, run the narrowest meaningful checks, repair supported regressions and review acceptance. Match verification to the artifact: code checks for code; evidence/fidelity/domain/visual gates for research and prose. Do not impose builds on a pure writing task. Keep the lifecycle here; domain skills own their specialty outputs.

Record state and attempts in the authorized private store. Reconcile outstanding handles before timeout retry. Changed scope/input/profile/closure hashes invalidate dependent gates. Interactive feedback must identify the current revision and artifact. Auto still waits at human-scientific/taste/rights, paid, external and irreversible gates.

Finish with current artifacts, hashes, checks, remaining gates and next actions. Never accept required pending/fail/stale gates or create commit/publish/install authority from the word auto.

## References

- Execution modes (historical evidence path: `../../../core/workflows/execution.md`; unavailable in the cleaned checkout)
- Model/context (historical evidence path: `../../../core/workflows/model-and-context.md`; unavailable in the cleaned checkout)
- Review/handoff (historical evidence path: `../../../core/workflows/review-and-handoff.md`; unavailable in the cleaned checkout)
- State schema (historical evidence path: `../../../core/contracts/task-state.schema.json`; unavailable in the cleaned checkout)
- Receipt schema (historical evidence path: `../../../core/contracts/receipt.schema.json`; unavailable in the cleaned checkout)
