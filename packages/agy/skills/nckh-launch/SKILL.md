---
name: nckh-launch
description: "Plan product or feature go-to-market readiness and sequence with communication and rollback gates. Does not deploy or send announcements by default."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-launch

## Inputs and owned output

Inputs: Product/feature release scope, audience, readiness evidence, constraints and rollout authority.

Output: Launch sequence, readiness matrix, audience/message/comms plan and rollback decisions.

## Required contracts

Read [Authorization](references/_shared/core/policies/authorization-policy.md),
[Evidence](references/_shared/core/policies/evidence-policy.md),
[Preservation](references/_shared/core/policies/preservation-policy.md) and
[Acceptance](references/_shared/core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](references/_shared/core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Inspect actual product/release readiness, audience and approved claims. Define launch stages, channel/audience sequencing, dependencies, owners, support capacity, measurement and stop/rollback conditions.

Reuse campaign/content assets where applicable. Separate proposed announcement readiness from verified product availability. Unresolved security, rights, integration or acceptance gates remain visible; a marketing plan does not clear them.

Create draft communication and contingency routes without sending messages. Product deployment belongs to its explicitly authorized engineering/ops route; external announcements and spend have their own grants.

Return a concrete launch plan and decisions. Do not fabricate success metrics, deploy a product, notify people or publish automatically.

## References

- [Brief schema](references/_shared/core/contracts/brief.schema.json)
- [Claim schema](references/_shared/core/contracts/claim.schema.json)
- [Provider boundaries](references/_shared/extensions/providers/marketing/contract.json)
