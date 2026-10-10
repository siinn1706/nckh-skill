---
name: nckh-plan
description: "Create or validate a task plan saved as files: a plan.md index plus phase files with checks, verified by check-plan.py. Use to lập kế hoạch, chia giai đoạn, lên kế hoạch, kiểm tra kế hoạch, weigh design trade-offs or --validate; planning does not authorize implementation."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-plan

## Inputs and owned output

Inputs: Task/plan, source paths, constraints, non-goals, acceptance, locale and current authority.

Output: Plan files per the [Plan artifact](../../../core/workflows/execution.md#plan-artifact) contract: an outcome contract, a `plan.md` index and phase files with evidence-backed decisions, dependencies, checks and rollback; a validation ledger when requested.

## Required shared contracts

Read [Authorization](../../../core/policies/authorization-policy.md), [Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and [Acceptance](../../../core/policies/acceptance-policy.md) before work.
Read the route-specific references below when their mode applies. Output language
follows the brief; keep same-agent execution unless delegation has a recorded benefit.

## Workflow and boundaries

Capture the outcome, constraints, non-goals and acceptance before writing. Reuse a valid accepted design and inspect current owners, source, tests and permissions. Write the plan as the [Plan artifact](../../../core/workflows/execution.md#plan-artifact) section requires.

Neighbouring routes: source discovery and reading go to nckh-research, research method or protocol design to nckh-method, marketing strategy to nckh-marketing-plan, locating code owners to nckh-scout, and porting from an external repository to nckh-xia. Execution goes to nckh-cook. This skill turns their results into the task plan.

Brainstorm belongs here: compare viable options only where a material trade-off exists, challenge critical flaws with evidence and ask only for the missing decision. Research depth follows risk. Preserve journal/conference/year/track/article-type isolation when applicable; marketing and code tasks do not inherit scientific ranking requirements.

The only stable modifier is --validate. Run [check-plan.py](../../../scripts/check-plan.py) on the plan directory and report its verdict and exit status. Then check by hand what the script cannot: read every phase and relevant source for scope, revision, dependencies, authority, owners, oracles, acceptance and rollback. Each VERIFIED claim cites a file:line or hash read in this attempt; report FAILED/UNVERIFIED claims, located findings, a revision diff and unresolved decisions. Structural validity cannot certify implementation readiness.

Run check-plan.py before the plan handoff and stop there; deliverables named in the request stay phases for nckh-cook. Do not create product implementation or deliverables, install dependencies, change global configuration, call paid benchmarks or silently switch to nckh-cook.

## References

- [Execution modes](../../../core/workflows/execution.md)
- [Model/context](../../../core/workflows/model-and-context.md)
- [Brief schema](../../../core/contracts/brief.schema.json)
