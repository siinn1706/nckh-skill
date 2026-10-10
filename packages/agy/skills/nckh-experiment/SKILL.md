---
name: nckh-experiment
description: "Design or read out a marketing A/B experiment (thử nghiệm A/B, thiết kế A/B test, so sánh hai phiên bản, bản nào thắng, cái nào hiệu quả hơn, chia nhóm ngẫu nhiên) with valid units, randomization, metrics, stopping and uncertainty. Scientific statistical design belongs to nckh-statistics. No live traffic/budget changes without approval."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-experiment

## Inputs and owned output

Inputs: Hypothesis, population/unit, data/metrics, constraints, randomization and stopping information.

Output: Protocol or bounded readout with allocation, primary metric, guardrails, sample/stopping rationale and validity limits.

## Required contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](references/_shared/core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Scope is a marketing or product A/B experiment with an assigned treatment. Descriptive analysis of existing KPI, funnel or campaign data belongs to nckh-analytics. A scientific study needing estimands, independent units or nested designs belongs to nckh-statistics.

Freeze the hypothesis, experimental unit, allocation/randomization, population/exclusions, primary metric and denominator, guardrails and analysis before a run. Specify sample/stopping rationale from supplied assumptions or validated calculation; unknown baselines/economics remain unknown.

Check contamination, interference, instrumentation, sample-ratio mismatch, missingness, multiple testing and peeking. Sequential monitoring needs an explicit valid protocol; repeated significance checks cannot justify opportunistic stopping.

For a readout use actual authorized data, show counts/windows/uncertainty and confirm design assumptions. Separate descriptive associations from causal effects; preserve null/negative results and limits. Human/statistical review remains distinct from model self-scoring.

Return the protocol/readout and decisions. Design does not launch a live experiment, change traffic/budget, send messages or upload private data. Do not fabricate significant lift, sample sizes or approval.

## References

- [Brief schema](references/_shared/core/contracts/brief.schema.json)
- [Claim schema](references/_shared/core/contracts/claim.schema.json)
- [Provider boundaries](references/_shared/extensions/providers/marketing/contract.json)
