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

Read [Authorization](references/_shared/core/policies/authorization-policy.md), [Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and [Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Read the route-specific references below when their mode applies. Output language
follows the brief; keep same-agent execution unless delegation has a recorded benefit.

Resolve the exact skill row from the shared [personal-use acceptance profile](references/_shared/core/profiles/acceptance/personal-use.json)
before grading output. It supplies the five common gates, the skill-specific
positive/negative/output/authority criteria and scoped source applicability.
The project owner may give the final personal-use verdict; external reviewer,
holdout and human-gold evidence are not prerequisites for that lane. Missing
owner feedback is `pending-personal-review`.

## Workflow and boundaries

Read the plan and inspect current artifacts before execution. Resolve authority from the human request and host policy. A prior design approval alone is insufficient, while an explicit cook request covers reversible implementation within scope.

Preserve an approved execution mode. Optional --auto completes authorized phases without routine pauses. --interactive declares substantive review boundaries, gives the exact artifact/hash and checks, then waits for approve/request-changes/reject before downstream material work. Without a mode, continue already-authorized implementation, checks and delivery; ask only for a material missing decision or an action outside that authorization. Reject conflicting or unsupported flags. There is no stable --no-test.

Inspect, implement, run the narrowest meaningful checks, repair supported regressions and review acceptance. Match verification to the artifact: code checks for code; evidence/fidelity/domain/visual gates for research and prose. Do not impose builds on a pure writing task. Keep the lifecycle here; domain skills own their specialty outputs.

Record state and attempts in the authorized private store. Reconcile outstanding handles before timeout retry. Changed scope/input/profile/closure hashes invalidate dependent gates. Interactive feedback must identify the current revision and artifact. Required scientific, rights, paid, external and irreversible actions without an actual scope grant still wait. Personal-use artifacts may be delivered ready for use while final owner/taste feedback remains pending.

Finish with current artifacts, hashes, checks, remaining gates and next actions. Never accept required pending/fail/stale gates or create commit/publish/install authority from the word auto.

Bind owner feedback to the current revision, artifact hash and input hashes. A
mismatch fails closed and an absent record stays pending; do not manufacture a
pass from a successful command, a model critique, a synthetic fixture or a
structural profile read. Already-authorized routine phases continue with or
without `--auto`; honor session grants and the selected lane's actual required
boundaries.

## References

- [Execution modes](references/_shared/core/workflows/execution.md)
- [Model/context](references/_shared/core/workflows/model-and-context.md)
- [Review/handoff](references/_shared/core/workflows/review-and-handoff.md)
- [State schema](references/_shared/core/contracts/task-state.schema.json)
- [Receipt schema](references/_shared/core/contracts/receipt.schema.json)
