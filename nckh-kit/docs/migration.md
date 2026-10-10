# Migration and preserved contracts

The approved portable plan superseded the earlier wrapper design on 2026-10-01.
This documentation decision is separate from native installation or package
qualification. There was no verified installed predecessor in this workspace.
Fixture update/rollback is a rehearsal, not an observed migration of a real host.

| Earlier capability | Current owner |
|---|---|
| research-plan / research-cook | nckh-plan / nckh-cook |
| Discovery, literature review and reading | nckh-research |
| Source, quote, DOI, claim and citation audit | nckh-evidence |
| Argument, comparative and methodological reasoning | nckh-method |
| VI/EN drafting, polish and translation | nckh-humanwrite (polish/translation) and nckh-paperwrite (scientific authoring); nckh-write remains a compatibility route |
| Personal Vietnamese/English style critique | nckh-taste |
| Slides, real-data charts, mechanisms and illustrative artwork | nckh-visuals |
| Selected upstream technical and marketing concepts | Distinct Engineer/Marketing identities; optional extensions |
| Upstream Xia comparison | nckh-xia; no ak-xia alias or shadow |

The scientific extension adds `nckh-dataset`, `nckh-statistics`,
`nckh-telemetry` and `nckh-aiops` to the preserved 39 identities. Database
migrations remain with `nckh-data`; marketing analytics/experiments retain their
owners. The current exact set is 43 identities/172 base cases, with 24 required
families, a separate [regression suite](../core/contracts/regression-cases.schema.json) that leaves the
base cases unchanged, and the historical runtime/writer matrices preserved. Authored resources
use `owned-reference` with original contribution provenance; copied/retrieved
resources retain their existing strict checks. Historical format 1/2 bundles and
their recorded helper inventories remain readable without rewriting receipts.

## Evidence ledger version 2

The [receipt](../core/contracts/receipt.schema.json), [claim](../core/contracts/claim.schema.json)
and [task-state](../core/contracts/task-state.schema.json) contracts moved from
version 1 to version 2 (see the Evidence ledger section of `contracts.md`). The schemas
accept only version 2 and new task state is written as version 2, so a version-1
record fails current validation. Version-1 receipts, claims and task state in earlier
plans and results are historical evidence: keep their bytes, do not re-validate them
against version 2 and do not rewrite them. New attempts write version-2 records.

## r44 to r45

The r45 hook closure adds the routing hint and the EOL/BOM guard, so its closure
hash differs from r44. The hook configurator refuses to replace an owned payload
with a different closure (`owned payload differs; remove its matching owned version
first`). For a project installed with r44 hooks, first remove the owned hook
configuration with the r44 package's `configure-hooks.py` (`preview --action remove`,
then `remove`), then run `update` with the r45 package, which registers the r45
hooks by default ([update](installation.md#update),
[portable hooks](installation.md#portable-hooks)). Projects installed with
`--hooks off` and global installs have no hooks to remove.

A project install now also checks the home-level roots of `--home` when the
project lies outside that home. If the same skills are installed globally, the
preview stops with `duplicate visibility` (`global`): remove the global copy or pass
`--acknowledge-ancestor-visibility` (see the duplicate-visibility section of
[installation](installation.md)).
Ownership records written before this change carry no home and keep the earlier
scan until their next `update`.

Negative regression cases now carry `dispatch: invoke-skill`. Runners must take
the sent prompt from `dispatch_prompt` or `check-case-oracle.py --print-prompt`
(see the Evaluation cases section of `contracts.md`); earlier runs that sent these
prompts unchanged remain historical receipts. Routing prompts form a separate
suite; the base, regression and required-family counts are unchanged.

The four Vietnamese marketing-law sources (`MKT-VN-*`) in the
[personal-use profile](../core/profiles/acceptance/personal-use.json) now cite
their records on vbpl.vn; their status, applicability and limits are owned by that
profile. The repository script
`plans/evaluation/personal-use/finalize-resource-integration.py` is retired: it
exits 2 before reading or writing, because the resource-lookup sections are now
maintained by hand against the
[resource registry](../core/registry/catalog/resources.json).

## Eleven preserved invariants

| Invariant | Owning contract |
|---|---|
| Human authority and revision-bound resume | authorization policy; HostGrant and task state |
| Timeout reconciliation and rollback | task attempts; owned transaction journal |
| Source/contract drift and dependent invalidation | source lock; state invalidation; receipt hashes |
| Claim verdict, profile conflict and aggregate acceptance | evidence guards; aggregate required gates |
| Factual delta after polish | factual-delta guard; write-to-evidence route |
| Source/policy freshness | source status/as-of; correction/retraction and venue checks |
| Private data and packaging boundary | explicit source areas, containment and rights ledger |
| Source text versus host-enforced tool authority | authorization policy; native permissions and NOT_CALLABLE |
| Visual QA bound to the final file | source/render hashes and separate visual gates |
| Bounded development and honest holdout/human labels | qualification protocol and exposure rules |
| Scope coverage and permitted plan-only outputs | catalog; plan/review/handoff/Xia boundaries |

All scopes remain present. Tests certify only the behavior they observe. Full
semantic support, human taste and editable scientific visuals require separate
evidence. Framework/provider/native-document extension bindings remain unavailable
until the owner chooses a permitted engine and its actual interface is verified.

Updates keep source-lock history and exact candidate provenance. Existing
user-edited skills/configs are kept, merged by the owner, or explicitly replaced
after preview. Re-inventory real installed state before any migration; old names
in a plan cannot establish file ownership. Follow [installation recovery](installation.md)
for owned rollback/uninstall. No credentials are revoked and no failed receipts
or historical plans are erased.

