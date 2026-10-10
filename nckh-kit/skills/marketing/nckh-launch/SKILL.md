---
name: nckh-launch
description: "Plan product or feature go-to-market readiness (ra mắt sản phẩm, kế hoạch ra mắt, chuẩn bị ra mắt, lên kệ, ra mắt tính năng) and release sequencing with communication and rollback gates. The surrounding promotional campaign belongs to nckh-campaign. Does not deploy or send announcements by default."
metadata:
  version: "0.1.0"
  status: experimental
---

# nckh-launch

## Inputs and owned output

Inputs: Product/feature release scope and revision, audience, readiness evidence, constraints and rollout authority.

Output: Launch checklist that names the product/release revision (`unknown` when not supplied), launch sequence, readiness matrix, dependencies and owners, audience/message/comms plan, unresolved gates and rollback decisions.

## Required contracts

Read [Authorization](../../../core/policies/authorization-policy.md),
[Evidence](../../../core/policies/evidence-policy.md),
[Preservation](../../../core/policies/preservation-policy.md) and
[Acceptance](../../../core/policies/acceptance-policy.md) before work.
Output follows the brief's locale. Same-agent is the default; use
[model/context policy](../../../core/workflows/model-and-context.md) before delegation.
Scientific venue/ranking rules apply only when the task explicitly needs them.

## Workflow and boundaries

Inspect actual product/release readiness, audience and approved claims. Record the release revision the plan applies to; an unknown revision stays `unknown` and is not invented. Define launch stages, channel/audience sequencing, dependencies, owners, support capacity, measurement and stop/rollback conditions.

Go-to-market readiness and release sequencing belong here; the time-bound promotional campaign around the launch belongs to nckh-campaign. Reuse campaign/content assets where applicable. Separate proposed announcement readiness from verified product availability. Unresolved security, rights, integration or acceptance gates remain visible; a marketing plan does not clear them.

Create draft communication and contingency routes without sending messages. Product deployment belongs to its explicitly authorized engineering/ops route; external announcements and spend have their own grants.

Return a concrete launch plan and decisions. Do not fabricate success metrics, deploy a product, notify people or publish automatically.

## References

- [Brief schema](../../../core/contracts/brief.schema.json)
- [Claim schema](../../../core/contracts/claim.schema.json)
- [Provider boundaries](../../../extensions/providers/marketing/contract.json)
