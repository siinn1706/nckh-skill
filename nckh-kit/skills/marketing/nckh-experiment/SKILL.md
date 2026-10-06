---
name: nckh-experiment
description: "Design or read out an A/B experiment with valid units, randomization, metrics, stopping and uncertainty. No live traffic/budget changes without approval."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-experiment

## Inputs and owned output

Inputs: Hypothesis, population/unit, data/metrics, constraints, randomization and stopping information.

Output: Protocol or bounded readout with allocation, primary metric, guardrails, sample/stopping rationale and validity limits.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Freeze the hypothesis, experimental unit, allocation/randomization, population/exclusions, primary metric and denominator, guardrails and analysis before a run. Specify sample/stopping rationale from supplied assumptions or validated calculation; unknown baselines/economics remain unknown.

Check contamination, interference, instrumentation, sample-ratio mismatch, missingness, multiple testing and peeking. Sequential monitoring needs an explicit valid protocol; repeated significance checks cannot justify opportunistic stopping.

For a readout use actual authorized data, show counts/windows/uncertainty and confirm design assumptions. Separate descriptive associations from causal effects; preserve null/negative results and limits. Human/statistical review remains distinct from model self-scoring.

Return the protocol/readout and decisions. Design does not launch a live experiment, change traffic/budget, send messages or upload private data. Do not fabricate significant lift, sample sizes or approval.

## References

- [Brief schema](../../../core/contracts/brief.schema.json)
- [Claim schema](../../../core/contracts/claim.schema.json)
- [Provider boundaries](../../../extensions/providers/marketing/contract.json)
