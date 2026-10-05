---
name: nckh-plan
description: "Research options and create or validate a task plan. Use for planning, design trade-offs or --validate; planning does not authorize implementation."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-plan

## Inputs and owned output

Inputs: Task/plan, source paths, constraints, non-goals, acceptance, locale and current authority.

Output: An outcome contract and a short plan index with scoped phases, evidence-backed decisions, dependencies, checks and rollback; validation ledger when requested.

## Required shared contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md), [Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and [Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Read the route-specific references below when their mode applies. Output language
follows the brief; keep same-agent execution unless delegation has a recorded benefit.

## Workflow and boundaries

Capture the outcome, constraints, non-goals and acceptance before writing. Reuse a valid accepted design and inspect current owners, source, tests and permissions. For a small task use a concise plan. For coordinated work keep the index short and put executable detail in phases.

Brainstorm belongs here: compare viable options only where a material trade-off exists, challenge critical flaws with evidence and ask only for the missing decision. Research depth follows risk. Preserve journal/conference/year/track/article-type isolation when applicable; marketing and code tasks do not inherit scientific ranking requirements.

The only stable modifier is --validate. Read every phase and relevant source; check scope, revision, dependencies, authority, owners, oracles, acceptance and rollback. Report VERIFIED/FAILED/UNVERIFIED claims, located findings, a revision diff and unresolved decisions. Formatting validity cannot certify implementation readiness.

Write requested local plan/research/validation state. Stop at the plan handoff. Do not create product implementation, install dependencies, change global configuration, call paid benchmarks or silently switch to cook.

## References

- [Execution modes](references/_shared/core/workflows/execution.md)
- [Model/context](references/_shared/core/workflows/model-and-context.md)
- [Brief schema](references/_shared/core/contracts/brief.schema.json)
