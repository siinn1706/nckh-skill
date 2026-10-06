# Contract ownership

This experimental kit implements the approved 43-identity design. Instructions are
English; artifacts follow the brief's Vietnamese/English/bilingual locale.
[Version-1 schemas](../core/contracts/brief.schema.json) reject unknown fields/versions.
The stdlib validator implements type, properties, required, additionalProperties,
items, enum, const, minLength, minimum, minItems and pattern, plus descriptive
title/description/$schema. Unknown keywords fail. It is not a complete JSON Schema engine.

Source identity, evidence locators, semantic support, profiles, private task state,
receipts, model resolution and delegation have separate schemas.
[State helpers](../core/state.py) implement progression, revision-bound gates,
interactive feedback and descendant invalidation. HostGrant records supplied live
host authority; it is not a security boundary. Unknown model/cost/window remains unknown.

Personal inputs, holdout labels and raw receipts live outside source/dist.
Python 3.11+ is required for package tools, not instruction-only skills.
No provider calls, runtime installation or paid evaluation occurs in unit tests.

## Selected resources and rights

The [resource registry](../core/registry/catalog/resources.json) is the single
source catalog. Each resource declares consumer, reader, format, exact source
path/full commit/file hash, license/attribution pins, expected artifact and rollback.
The [registry schema](../core/contracts/resource-registry.schema.json) and
[copied-content schema](../core/contracts/resource-provenance.schema.json) are closed.

| Resource | Upstream and commit | Use and source rights review |
|---|---|---|
| R-reporting-lookup | K-Dense scientific-agent-skills, `154988403bb5a18e9d3c0ce4e6d5e2e4b184a298` | Verbatim 15-record registry for matching clinical/health study designs; its official-source URLs are references, not imported reporting checklists. |
| R-publisher-profile | Same K-Dense commit | Verbatim eight-profile publisher snapshot for planning. External pages were not copied; exact journal/year/track/article-type/stage applicability remains unverified. |
| R-ui-lookup | nextlevelbuilder/ui-ux-pro-max-skill, `09170eec67eefd46a7ae85de61b40c194020f997` | Verbatim 119-row UX heuristic table, used by frontend. No fonts, logos, third-party packages or executable upstream code are imported. |
| R-nature-reference | Yuan1z0825/nature-skills, `84880815fb37317b3766bff2c2abba395b8993c3` | Only the manifest-routed English language fragment. Its suggestions are advisory; it is not a VI/EN prose corpus or current universal Nature policy. |
| R-vi-wikisource-passages | Wikisource Vietnamese oldids `179667`, `179899`, `106841`, `19383`, `80653`, `71961` | Normalized JSONL keeps three actual child passages with parent/root locator metadata; no separate root records are exposed as prose. Text remains historical/literary and page-level CC BY-SA attribution does not settle underlying-work public-domain status for every jurisdiction. Consumers: `nckh-write`, `nckh-taste`, `nckh-humanwrite`. |
| R-pmc-scientific | Europe PMC `PMC13623134` and `PMC13623154` fullTextXML snapshots | Normalized JSONL is bounded to two article projections; provenance records the XML snapshot hashes and the rights note preserves each article's CC BY 4.0 statement. Article-level license and biomedical scope apply. Consumers: `nckh-write`, `nckh-evidence`, `nckh-method`, `nckh-humanwrite`, `nckh-paperwrite`. |
| R-worldbank-vietnam-population | World Bank API `VNM/SP.POP.TOTL`, 2000–2025, snapshot `2026-07-13` | One normalized time-series bundle records the raw JSON response lineage. Returned values and blank `unit` fields are preserved; World Bank default CC BY 4.0 terms and possible third-party indicator restrictions remain attached. Consumers: `nckh-visuals`, `nckh-analytics`, `nckh-method`. |
| R-django-sqlmigrate-fixtures | SWE-bench `django__django-10087`, base commit `02cd16a7a04529c726e5bb5a13d5979119f25c7d` | Bounded JSONL with two BSD 3-Clause Django code fixtures and task locators. Issue text, problem statement, benchmark patch, test patch and dataset-row bytes are not packaged; the BSD scope applies only to the two pinned fixtures. Consumers: `nckh-fix`, `nckh-test`, `nckh-code-review`. |
| R-uci-bank-marketing | UCI Bank Marketing DOI `10.24432/C5K306`, official archive lineage and nested `bank.csv` sample | Normalized JSONL contains ten actual rows; its lineage and rights note retain the official CC BY 4.0 route without treating staged archive bytes as owned package content. `duration` is post-contact and can leak the target; this is campaign-response data, not copy or causal uplift evidence. Consumers: `nckh-market-research`, `nckh-marketing-plan`, `nckh-campaign`, `nckh-analytics`. |

At the pinned commits, the applicable root licenses are
[K-Dense MIT](https://github.com/K-Dense-AI/scientific-agent-skills/blob/154988403bb5a18e9d3c0ce4e6d5e2e4b184a298/LICENSE.md),
[UI UX Pro Max MIT](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/09170eec67eefd46a7ae85de61b40c194020f997/LICENSE), and
[Nature Skills Apache-2.0](https://github.com/Yuan1z0825/nature-skills/blob/84880815fb37317b3766bff2c2abba395b8993c3/LICENSE).
The full pinned repository trees and selected files were reviewed on 2026-10-02.
No license/NOTICE override applies in the selected file ancestry. The retained
licenses and NCKH attribution notices travel with every consumer closure.
Unrelated subtree licenses remain outside this selection. External facts, current
publisher policies and UX effectiveness still require their own verification.

Local code/instructions keep `owned-local-package`. Exact upstream data and license
bytes use `copied-upstream` with full provenance; they cannot be relabeled as owned.
Source-lock and bundle format 2 carry these records, while historical local-only
format 1 remains readable unchanged. Local candidate permission is separate from
native/human qualification and public release acceptance.

Data formats enter inventory only through an explicit resource/rights record.
Private evaluation inputs and raw traces never enter a skill closure. The five
real personal-use packs above are bounded snapshots, not general corpora: the
Wikisource pack has three actual child passages with parent/root metadata, the PMC
pack has two article projections from licensed snapshots, World Bank has one dated series,
SWE-bench is a bounded code-fixture reference, and UCI has ten actual tabular rows. Lookup returns per-record
source/version/hash/as-of/license/locator and keeps the packaged artifact hash
separate from every raw upstream hash. A successful lookup is source/package
evidence only; it does not establish native-host behavior, owner taste, human
gold, scientific validity, causal uplift or public redistribution clearance.

## Authored research reference packs

Four original typed JSONL packs contain 14 bounded records: statistical recipes (3), telemetry field references (3), AIOps benchmark cards (3), and evaluation recipes (5). The registry owns eight exact consumer bindings. No raw acquisition, pilot data, private labels, predictions or measured results enter these packs.

[Owned contribution provenance](../core/contracts/owned-resource-provenance.schema.json) records original-summary disposition, actual artifact hash, exact record/source membership, source snapshot hashes, unknown-commit reasons and original [local rights](../core/profiles/resources/research-packs-rights.md)/[attribution](../core/profiles/resources/research-packs-attribution.md). `owned-reference`/`reauthored-with-sources` pins remain local-package-only; upstream license metadata does not relicense the authored work. Copied and retrieved legacy variants retain their own strict dispatch.

The [bounded reader](../scripts/search-resource.py) validates current catalog identity and exact context before resource reads. Query, input/aggregate/record/depth and actual serialized-output caps are controller-owned; duplicate/nonfinite/private/unknown fields fail. OFF works with absent registry/data files. Package verification preserves historical hook closures and requires complete new helper closures when their pins exist. Local reads establish source behavior; relocated package acceptance follows source freeze and independent review.
