---
title: "Resource map — 37 NCKH identities"
status: selected
---

# Resource map — 37 NCKH identities

Thực thi chọn lọc đã ghi đủ 37 disposition. Một registry chứa bốn resources với năm consumer identities; các identity khác giữ Markdown và contracts hiện hữu. `promoted-local` chỉ là trạng thái kỹ thuật sau staged support, không phải human/scientific acceptance hay stable release.

Không tạo dataset tổng hợp mới, không copy repository. Bytes gốc, license và source/hash/as-of được giữ; reader phát per-record provenance. Clinical, publisher, UI và English advice ở namespace riêng, không mix records. VI/EN prose corpus, chart measurements và human gold vẫn thiếu. Những template/glossary/log đề xuất trước đây chưa có input/consumer được chọn thì giữ MD-only.

| # | Identity | Consumer/need | Actual resource/disposition | Acceptance gate |
|---:|---|---|---|---|
| 1 | `nckh-plan` | Plan scope, dependencies, user gates | MD-only; existing references/contracts, no selected data consumer | plan-only không mutate; pending gates giữ nguyên |
| 2 | `nckh-cook` | lifecycle, budget/stop, rollback | MD-only; existing references/contracts, no selected data consumer | permission/timeout/rollback receipt, không provider tự động |
| 3 | `nckh-review` | review packet, evidence classes | MD-only; existing references/contracts, no selected data consumer | hash/scope/status rõ; không biến review thành acceptance |
| 4 | `nckh-handoff` | owner handoff và unresolved Qs | MD-only; existing references/contracts, no selected data consumer | owner/path/rights/next gate đầy đủ |
| 5 | `nckh-research` | review mode, screening, reader card | MD-only; existing references/contracts, no selected data consumer | source/locator/access/as-of/status; no unsupported synthesis |
| 6 | `nckh-evidence` | claim, locator, counterevidence | MD-only; existing references/contracts, no selected data consumer | source hash/locator/support distinct; validator + negative case |
| 7 | `nckh-method` | argument/evidence/method boundary | promoted-local: `R-reporting-lookup` | assumptions/results/limits separated; no invented result |
| 8 | `nckh-write` | VI/EN genre fidelity, factual slots | promoted-local: `R-reporting-lookup`, `R-nature-reference`; VI/EN genre corpus blocked-input | actual sourced/user artifact; numbers/units/negation/causality protected; registries are not prose corpus; human fidelity pending |
| 9 | `nckh-taste` | local prose critique, register | promoted-local: `R-nature-reference`; VI/EN genre corpus blocked-input | style vs evidence separated; no human-gold claim |
| 10 | `nckh-visuals` | honest chart/source-map/visual QA | promoted-local: `R-publisher-profile`; actual chart measurements blocked-input | data/metric/mechanism locators, hashes; editor/accessibility gate separate |
| 11 | `nckh-scout` | scoped repository/resource discovery | MD-only; existing references/contracts, no selected data consumer | path/hash/rights/as-of; no broad unbounded crawl |
| 12 | `nckh-debug` | diagnosis evidence and failure modes | MD-only; existing references/contracts, no selected data consumer | reproduction/expected/actual/limits; no fix without authority |
| 13 | `nckh-fix` | cause-aligned repair and rollback | MD-only; existing references/contracts, no selected data consumer | failed reproduction before fix; tests/rollback recorded |
| 14 | `nckh-test` | test matrix and evidence class | MD-only; existing references/contracts, no selected data consumer | malformed/negative/zero-discovery paths; no weakened test |
| 15 | `nckh-code-review` | diff/risk/public-contract review | MD-only; existing references/contracts, no selected data consumer | findings cite code/test; no plan ID in code artifacts |
| 16 | `nckh-security` | threat model, secret/data boundary | MD-only; existing references/contracts, no selected data consumer | actual stored/exposed data and mitigation; no fake scan pass |
| 17 | `nckh-context` | context selection and privacy | MD-only; existing references/contracts, no selected data consumer | private/public/holdout boundaries preserved |
| 18 | `nckh-docs` | docs impact and source navigation | MD-only; existing references/contracts, no selected data consumer | links/claims rechecked; smallest owning surface |
| 19 | `nckh-frontend` | UI behavior and visual/source handoff | promoted-local: `R-ui-lookup` | UI-only domain fit, actual reader/output, source/asset rights and visual gate explicit |
| 20 | `nckh-backend` | API/data flow/contract implementation | MD-only; existing references/contracts, no selected data consumer | data in/out/error ownership and tests named |
| 21 | `nckh-data` | schema, provenance, dedup/lookup | MD-only; existing references/contracts, no selected data consumer | schema/hash/rights/split; JSONL not human gold |
| 22 | `nckh-devops` | deploy/observability/rollback route | MD-only; existing references/contracts, no selected data consumer | command/owner/rollback evidence, no deployment claim |
| 23 | `nckh-git` | diff/status/commit hygiene | MD-only; existing references/contracts, no selected data consumer | no destructive reset; commit contract preserved |
| 24 | `nckh-xia` | compare/disposition/upstream boundaries | MD-only; existing references/contracts, no selected data consumer | full-SHA/license/byte decision or explicit blocked-rights |
| 25 | `nckh-market-research` | source screening and market evidence | MD-only; existing references/contracts, no selected data consumer | real rows/full source pin or explicit user material; no public=redistributable inference |
| 26 | `nckh-brand` | positioning and taste brief | MD-only; existing references/contracts, no selected data consumer | taste/rights/human review pending; no uplift claim |
| 27 | `nckh-marketing-plan` | goals, channel, budget boundaries | MD-only; existing references/contracts, no selected data consumer | assumptions/measurement/approval explicit; no spend/provider |
| 28 | `nckh-campaign` | campaign brief and execution handoff | MD-only; existing references/contracts, no selected data consumer | audience/claim/asset rights/owner/stop gate |
| 29 | `nckh-launch` | launch readiness and rollback | MD-only; existing references/contracts, no selected data consumer | deployment/rollback evidence distinct from plan |
| 30 | `nckh-content` | content brief and evidence | MD-only; existing references/contracts, no selected data consumer | locale/claim/source/rights preserved |
| 31 | `nckh-copy` | conversion copy/local edits | MD-only; existing references/contracts, no selected data consumer | protected terms/claims and local delta reviewed |
| 32 | `nckh-seo` | canonical/index/crawl/on-page ownership | MD-only; existing references/contracts, no selected data consumer | actual `noindex`/canonical evidence; no ranking guarantee |
| 33 | `nckh-email` | message/recipient/measurement boundary | MD-only; existing references/contracts, no selected data consumer | no send/provider call; consent and claims explicit |
| 34 | `nckh-social` | platform-aware content/handoff | MD-only; existing references/contracts, no selected data consumer | platform/locale/rights/approval explicit; no publish |
| 35 | `nckh-analytics` | metric/denominator/window interpretation | MD-only; existing references/contracts, no selected data consumer | denominator/window/source/hash; no causal uplift inference |
| 36 | `nckh-cro` | conversion friction và owner-authorized canonical/noindex inspection | MD-only; existing references/contracts, no selected data consumer | locate actual directives; live indexing unknown; retain historical fail and intentional directives |
| 37 | `nckh-experiment` | design, metric ledger, stopping | MD-only; existing references/contracts, no selected data consumer | actual calculation/source/assumption receipt; no launch/provider |

## Selected resources và consumers

| Resource | Consumer | Content/limit | Source rights |
|---|---|---|---|
| `R-reporting-lookup` | `nckh-method`, `nckh-write` | 15 clinical/health reporting entries; unmatched CS/domain returns no applicable record | K-Dense pinned MIT; unchanged source bytes |
| `R-publisher-profile` | `nckh-visuals` | 8 publisher snapshots; exact venue/year/track/article-type applicability unknown; Science historical and ACS legacy warnings retained | K-Dense pinned MIT; profile is planning reference |
| `R-ui-lookup` | `nckh-frontend` | 119 unchanged UX rows; bounded query; examples are untrusted data and never executed | UI UX Pro Max pinned MIT; UI-only |
| `R-nature-reference` | `nckh-write`, `nckh-taste` | Only manifest-routed `static/fragments/language/en.md`; optional English advice, no corpus/policy claim | Nature Skills pinned Apache-2.0 with retained license/attribution |

[Registry](../../nckh-kit/core/registry/catalog/resources.json) owns exact source paths, full commits/file hashes, license/NOTICE paths, requires, reader, expected artifacts and rollback. [Source inspection](../evaluation/resource-quality/staging/source-inspection.json) retains full tree and selected-file license evidence; [staged packet](../evaluation/resource-quality/staged-packet.json) and [promotion receipt](../evaluation/resource-quality/promotion-receipt.json) preserve the ordered P2 → P3 → P1 handoff. The earlier [shortlist](../reports/researcher-261002-0832-source-shortlist.md) remains historical research rather than a global ranking.

## Consumer và verification

`scripts/search-resource.py` is the reviewed NCKH stdlib reader, distinct from upstream readers. It checks rights/hash, consumer, domain/locale/genre and publisher context, returns source locators/read hashes and preserves unknown semantic applicability. Resource-off uses the same reader/registry with no copied bytes and returns disabled before any resource read. Shared verifier and extracted smoke inspect the candidate closure with external CWD, isolated Python and unset PYTHONPATH.

CRO canonical/noindex inspection follows the explicit owner decision in [scope amendment](../evaluation/resource-quality/cro-scope-amendment.json). Broader SEO remains separate; no historical verdict was changed. The amended task is a separate not-run record outside the unchanged 148 package identities/case IDs.

P4 preparation preserves no-skill, permitted upstream and two same-base off/on pairs for same-agent/selective delegation, with separate revision 14 migration history. A lookup, valid manifest, imported rows or successful extracted read establishes no causal benefit, human taste, scientific validity, native binding or stable release. Real samples/rights/reviewers/thresholds/host/model/budget remain required.
