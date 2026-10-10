# Contract ownership

This experimental kit implements the approved 43-identity design. Instructions are
English; artifacts follow the brief's Vietnamese/English/bilingual locale.
[Contract schemas](../core/contracts/brief.schema.json) pin an exact `schema_version` and reject unknown fields/versions.
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

## Evidence ledger

[Receipt](../core/contracts/receipt.schema.json), [claim](../core/contracts/claim.schema.json)
and [task-state](../core/contracts/task-state.schema.json) contracts are version 2.
A receipt records each command's own result plus its input and output files; a claim
carries an attempt status; a task attempt can bind input/output hashes and the files
it created. Rules that depend on another field's value cannot be expressed in the
schema subset, so they live in the [ledger validator](../core/ledger.py). The agent
rules these records serve are in [execution](../core/workflows/execution.md#attempt-ledger).

- [check-receipt.py](../scripts/check-receipt.py) `inventory` records a workspace
  before an attempt; `verify` checks a version-2 receipt against that inventory and
  the files on disk. It never executes recorded commands.
- [check-plan.py](../scripts/check-plan.py) checks a plan directory: index, phase
  files, required sections, relative links and a receipt for every completed status.

Both print ASCII JSON and exit 0 for VERIFIED, 1 for FAILED and 2 for a usage error.
Version-1 records stay historical; see the Evidence ledger version 2 section of `migration.md`.
A version-1 record fails with one explicit finding, `<kind> schema: schema_version 1
is unsupported for <kind>; regenerate the record as schema_version 2`, rather than a
list of field errors.

A compound command needs one exit status per segment. The splitter
(`command_segments` in the ledger validator) keeps a top-level POSIX heredoc body
inside the segment of the command that opens it, so separators in the body never
create extra segments; an unterminated body runs to the end of the command.

## Routing boundaries

[Route boundaries](../core/registry/catalog/route-boundaries.json), closed by their
[schema](../core/contracts/route-boundaries.schema.json), are the single source for
sibling skills that are easy to confuse: each entry holds the owner rule and the
Vietnamese cues users type. The routing test (`tests/build/test_skill_routing.py`)
requires each SKILL.md to name its siblings by full ID and each description to carry
one of its cues within the length limit. Skill text cites these rules; it does not
redefine them.

The same cues drive the advisory routing hint (`core/route_hint.py`, used by the
hook runner and by the routing eval). Routing prompt files in `evals/cases/routing/`
carry `kind: routing-prompts` under their
[schema](../core/contracts/routing-prompts.schema.json): natural Vietnamese prompts
labelled with the expected skill or `none`, split into tune and held-out sets. The
case validator counts them separately as `routing_prompts`; they are neither base
nor regression cases and do not change those counts. The thresholds and the measured
held-out result are owned by `tests/release/test_routing_prompts.py`. A mechanical
cue match measures hint coverage only, not host routing.

## Evaluation cases

The base case loader in [evaluation](../core/evaluation.py) rejects an outcome prompt
that repeats the positive prompt, and a prompt with Vietnamese diacritics unless its
`input_language` is `vi` or `bilingual`. Required families in `evals/cases/required-families.json`
are exactly 24 under their [schema](../core/contracts/required-families.schema.json);
a family can list regression case IDs in `family_cases`, and the loader checks that
they exist. Every catalog skill belongs to at least one family
(`tests/release/test_family_coverage.py`).

The regression suite in `evals/cases/regression/` is separate from the base cases,
which it leaves unchanged. Each per-skill manifest follows the
[regression schema](../core/contracts/regression-cases.schema.json): hashed fixtures
and mechanical oracle checks, with every case `not-run` and no receipt until an
observed run. A `file-absent` check concerns files created during the attempt, not
files that already existed. [check-case-oracle.py](../scripts/check-case-oracle.py)
scores one case against a finished workspace and a `check-receipt.py inventory`
taken before the attempt; it calls no model and never edits the manifest. A
mechanical pass covers only the listed checks; criteria in its
`reviewer_acceptance` output still need a reviewer.

A case's optional `dispatch` field fixes how its prompt is sent. `natural` (the
default) sends the prompt unchanged, so host routing is part of the attempt.
`invoke-skill` prefixes the host invocation of the case's skill (`/nckh-x`, Codex
`$nckh-x`), because the oracle assumes that skill was called. Every negative
near-miss case must use `invoke-skill`, and its prompt must not already contain an
invocation. `dispatch_prompt` in [evaluation](../core/evaluation.py) is the single
source of the sent prompt; runners read it through
`check-case-oracle.py --case-id ID --print-prompt [--invocation TEMPLATE]`, which
prints the case ID, dispatch mode and exact prompt without scoring.

`file-absent` ignores new files only when they have the exact shapes the kit's own
hooks write in a project install: event receipts, their locks and the cap marker
under `.nckh-state/hooks/events/<host>/`, pre-edit snapshots under
`.nckh-state/hooks/snapshots/<host>/<session>/`, and the atomic-write temporaries
in those directories. `HOOK_RUNTIME_STATE` in [evaluation](../core/evaluation.py)
owns the patterns. Any other file, including a differently named file inside those
directories, still counts. When the finished workspace
holds a link that the before inventory lacks, scoring adds a failing
`links-created` row, whatever the listed checks say.

An `exit-status` check runs the manifest argv, never the agent's own commands, on a
fresh copy of the workspace in a temporary directory outside it, then deletes the
copy, so the scored workspace stays byte-identical. The command gets only `PATH`,
`SYSTEMROOT`, `TEMP` and `TMP` from the operator's environment, plus a scratch
`HOME`/`USERPROFILE`, UTF-8 Python settings and git settings that stop git at the
copy (`GIT_CEILING_DIRECTORIES`), skip system config and turn off fsmonitor and
hooks. A git check on a workspace without its own `.git` is `BLOCKED`, not scored.
This is filesystem isolation only, not a security sandbox: the command still
imports agent-written code and runs as the operator's user with network and
process access, and the copied repository's own git config still applies. Score
untrusted workspaces inside a disposable VM or container.

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
