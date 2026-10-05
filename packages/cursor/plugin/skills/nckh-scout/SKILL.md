---
name: nckh-scout
description: "Locate verified code owners, symbols, callers and repository flows. Use for repository questions; scouting does not authorize design or edits."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-scout

## Inputs and owned output

Inputs: Question, repository/workspace, exact scope and available local/semantic tools.

Output: Source map with verified paths, symbols/callers and bounded uncertainty.

## Required contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default. Use
[model/context policy](references/_shared/core/workflows/model-and-context.md) before delegation.

## Workflow and boundaries

Read repository instructions and the owning docs before searching. Start with a bounded file inventory and targeted text/symbol queries; widen only to trace an actual caller or dependency. Verify the owner from source and tests, not a filename or search snippet.

Trace entrypoint -> caller -> implementation -> data/output contract and relevant tests. Return exact paths/locations, observed behavior and gaps. Separate a source inference from a runtime observation. Reuse available semantic navigation only when it adds evidence; no full-repository packing or knowledge graph by default.

Answer the scoped codebase question. A source lookup does not require a deep model or another agent when the current context suffices. Do not make architecture decisions, edit code, run downloaded scripts or create an implementation plan unless requested.

## References

- [Execution/authority modes](references/_shared/core/workflows/execution.md)
- [Review/handoff](references/_shared/core/workflows/review-and-handoff.md)
