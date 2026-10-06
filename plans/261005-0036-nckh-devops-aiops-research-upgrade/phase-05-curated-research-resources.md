---
phase: 5
title: "Curated research resources với truthful provenance và typed readers"
status: completed
priority: P1
effort: 2-3 ngày công
dependencies: [phase-02-research-and-statistics, phase-03-scientific-datasets-and-telemetry, phase-04-devops-and-aiops-methods]
---

# P5 — Curated research resources với truthful provenance và typed readers

## Context và outcome

Tạo bốn bounded packs thật sự có named reader/consumer/artifact/verifier theo [adoption map](./source-adoption-map.md). Đây là authored reference metadata/recipes, không measurements/corpus/gold. Reuse JSONL capability; current JSON/CSV lookup branches chỉ support reviewed resource IDs, không suy file extension là reader support.

`KIT = C:/Users/USER/Downloads/test-skill/nckh-kit`; `RUN` là P1 absolute attempt root. Source manifests có byte hashes/fingerprints nhưng ZIP commits unknown; resolve rights/version ở cook cho bytes thực sự sử dụng. No-copy ClaudeKit/proprietary docs vẫn giữ.

## Ownership và files

Resource owner authored packs/typed selectors/tests; controller có queue độc quyền schema package closure, registry, build/provenance/source-lock mappings. Không hai agent ghi registry/build đồng thời.

| Action | Absolute named path | Change |
|---|---|---|
| Create | `KIT/core/profiles/resources/statistical-recipes.jsonl`, `KIT/core/profiles/resources/telemetry-dictionary.jsonl`, `KIT/core/profiles/resources/aiops-benchmark-cards.jsonl`, `KIT/core/profiles/resources/aiops-evaluation-recipes.jsonl` | Four reviewed typed authored reference packs |
| Create | `KIT/core/contracts/owned-resource-provenance.schema.json` | Additive owned multi-source lineage contract |
| Modify by controller | `KIT/core/contracts/resource-registry.schema.json`, `KIT/core/resources.py`, `KIT/core/build.py` | Truthful source-kind/mode/pin dispatch; preserve legacy variants |
| Integrate serial by controller before pack registration/read | `KIT/core/registry/catalog/skills.json`, `KIT/core/contracts/catalog.schema.json`, `KIT/core/profiles/acceptance/personal-use.json`, `KIT/core/acceptance.py`, `KIT/core/evaluation.py`, `KIT/evals/cases/research-data-aiops/nckh-{dataset,statistics,telemetry,aiops}.json` | Exact identity/profile/four-case manifests and owning count/membership assertions for completed P2–P4 owners; preserve baseline IDs/families |
| Modify | `KIT/scripts/search-resource.py`, `KIT/scripts/resource-smoke.py` | Bounded typed JSONL selection and all declared bindings smoke |
| Create | `KIT/tests/resource/test_research_packs.py` | Typed records/selection/rights/lineage/privacy bounds |
| Modify by controller | `KIT/core/registry/catalog/resources.json`, `KIT/docs/contracts.md` | Producer/reader/consumer/domain/locale/genre/expected artifact/rights entries |
| Modify | New four skill `references/resource-lookup.md` under `KIT/skills/core/nckh-{dataset,statistics,telemetry,aiops}/` | Concrete capability invocation/applicability handoff |

## Truthful provenance design

Current registry/provenance supports `copied-upstream|retrieved-snapshot` and `verbatim-upstream|normalized-with-lineage|metadata-only-reference`; `owned-local-package` pins hiện từ chối provenance thêm. Không encode reauthored pack như copied upstream hoặc lấy root MIT che authored/third-party distinction.

Proposed additive variant: registry `source_kind=owned-reference`, `copied_vs_reauthored=reauthored-with-sources`; source-lock pin `rights=owned-reference` với `owned-resource-provenance` typed record. Fields: artifact SHA-256, owned authored version/as-of/authoring disposition/local release rights, record IDs, source contributions `{source_id,locator,version_kind,version_or_snapshot,observed_hash,as_of,license,rights_scope,attribution,transformation,applicability}`. Unknown upstream commit giữ null/unknown reason với verified snapshot hash; copied content vẫn yêu cầu original upstream rules. No forged license cho owned package; local-package-only/public rights lanes giữ riêng.

Registry/schema supported subset dùng explicit fields/enums; owner validators enforce source-kind-specific required/forbidden fields and multi-source exact bindings. `resource-provenance.schema.json` legacy variants và historical format1/2 readers giữ behavior; add new schema/dispatcher thay vì loosen copied checks. `core.resources`, build/source-lock verifier, standalone relocated reader, manifest export và any public verifier phải agree representation; one owner audits all rights/source-kind dispatch consumers.

## Pack contracts và selectors

| Proposed ID / file | Consumer / domain / genre | Task artifact |
|---|---|---|
| `R-statistical-recipes` / `statistical-recipes.jsonl` | statistics, method / `scientific-statistics` / `analysis-recipe` | Applicable assumption/estimator/uncertainty/reporting recipe selection |
| `R-telemetry-dictionary` / `telemetry-dictionary.jsonl` | telemetry / `observability-research` / `telemetry-field-reference` | Signal/unit/time/resource/correlation mapping checklist |
| `R-aiops-benchmark-cards` / `aiops-benchmark-cards.jsonl` | aiops, dataset / `aiops-research` / `benchmark-reference` | Exact benchmark suite/task/modalities/labels/rights/split card |
| `R-aiops-evaluation-recipes` / `aiops-evaluation-recipes.jsonl` | aiops, statistics, method / `aiops-research` / `evaluation-recipe` | Task-specific baseline/metric/tie/failure/leakage protocol selection |

Use exact full skill IDs in registry. Source locale retained; authored reference locale declared by actual text, output VI/EN independent. No row quota/default fake examples. Record kinds/allowed fields validated explicitly; trusted per-file/aggregate bytes/records/tokens/output caps enforced before read/parse/allocation with bounded streaming/hash; payload không nâng cap. Oversize hoặc clipped response không được ghi complete. Duplicate IDs/nonfinite/ambiguous JSON refused; query tokens select actual records. Existing `TASK_METADATA_KEYS`/JSONL guards need new typed record dispatch, không accept arbitrary fields/execute embedded snippets. Benchmark unknown rights record is metadata-reference, no data/code/import instructions executed.

## Implementation steps

1. Resolve every selected source/path rights/ref/license/NOTICE and current primary docs version; create per-contribution ledger, review authored versus copied text, retain no-copy dispositions.
2. Controller integrate completed P2–P4 owners' exact catalog/profile/four-case manifests and count/membership consumers as one serial prerequisite, rồi additive owned provenance/source-kind validators before pack registration/read. `core/resources.py` rejects consumers absent from current catalog; không hoãn prerequisite này đến P7 hoặc claim P5/P6 end-to-end reads passed while identities missing. Preserve baseline IDs/19 families, legacy copied/retrieved strict checks và unknown-key fail; domain/schema tests remain independent of stale source-lock pins.
3. Author smallest useful records after prerequisite handoff; factual method/benchmark/telemetry statements cite exact source locators+snapshot hashes; public metadata can be owned reauthored card with contribution provenance. No gold/measured benchmark claims.
4. Add reviewed typed selectors to bounded JSONL branch and contexts; reuse existing CLI `--resource-id --consumer --domain --locale --genre --query --json`, no generic format engine. Verify before file read consumer/locale/genre/domain eligibility.
5. Bind each pack to named skills/artifacts and resource closure/attribution; reflect dependencies in registry/docs. Package raw acquisitions/private task inputs never by Markdown closure links.
6. Trước P6, run lock-independent typed/domain checks và actual current-registry reads qua `core.resources`/standalone reader cho declared bindings; verify local ON reads và OFF disabled/no-read with absent resource files. Current local readers không verify global source lock, nên gate này không cần interim freeze. P6 chỉ nhận packs sau actual local behavior pass; source conflict giữ pending/rejected ledger, không invent rows/rights. Existing lock-dependent closure/build regressions và relocated package tests hoãn P7 sau sole candidate freeze.

## Todo

- [x] Resolve selected contribution rights/ref and owned-versus-copied ledger.
- [x] Controller serially integrate exact identity/profile/base-case and source-kind prerequisites before pack registration/read/P6 handoff.
- [x] Add owned provenance variant across schemas/readers/build/pins/manifest verification.
- [x] Author four bounded packs with exact applicability and named consumers.
- [x] Add typed selectors, mismatch/drift/privacy/bounds cases and smoke bindings.
- [x] Handoff registry/closure amendments to single P7 integration owner.

## Verification — future only

Proposed pre-freeze domain/schema subset from `KIT`: `python -B -m unittest tests.resource.test_research_packs.ResearchPackContractTests`; proposed class must not require source-lock validation/build và covers actual local registry reads/ON/OFF no-read. New-consumer reader invocation requires P5 serial catalog/profile/case/source-kind prerequisites first. Existing CLI after actual pack+registry exists: `python -I scripts/search-resource.py --resource-id R-telemetry-dictionary --consumer nckh-telemetry --domain observability-research --locale en --genre telemetry-field-reference --query timestamp --json`; `en` must match actual authored locale; enumerate actual declared bindings. Record local reader/ON/OFF receipts before P6 handoff. Full proposed `tests.resource.test_research_packs` and existing `tests.resource.test_consumers`/`test_real_sources`/`test_writer_consumers`/`test_closure` pinned compatibility gates plus relocated package tests run P7 after candidate freeze. Do not freeze source mid-phase just to bypass stale pins.

Success: new variant accepted only with actual authored/hash/contribution bindings; mislabeled/copied/unresolved permission fails; no unsupported JSON/CSV auto-read; wrong contexts do not read; OFF works with absent resource files and gives disabled/no-read; existing nine resources/legacy bundles remain verifiable. Successful read proves source/package behavior, không scientific usefulness.

## Risk/security/rollback

Rights/source kind mapping là public contract risk: independent reviewer phải inspect all serializer/verifier/relocated-reader branches before freeze. No instruction/code execution from reference records. Restore owned pack/registry/schema/reader mappings together using preimages and new corrective freeze; retain old lock history/failed attempts. Never silently remove public ON contract hoặc rewrite third-party pins as owned.

## Actual execution evidence

Four packs / 14 records / eight exact consumer bindings; original local rights and multi-source snapshot hashes retained in [contribution ledger](../runs/nckh-upgrade-261006-0850-attempt-01/p5-contribution-ledger.json). [Actual local CLI/OFF receipt](../runs/nckh-upgrade-261006-0850-attempt-01/p5-local-reader-receipt.json), 89 domain tests (historical evidence path: `../runs/nckh-upgrade-261006-0850-attempt-01/p5-contract-tests-attempt-03.txt`; unavailable in the cleaned checkout), focused final 19 (historical evidence path: `../runs/nckh-upgrade-261006-0850-attempt-01/p5-contract-tests-attempt-04.txt`; unavailable in the cleaned checkout) and [independent review/re-review](../reports/review-261006-owned-resource-provenance.md) qualify pre-freeze source behavior. The original two Windows temp ACL errors and counsel are retained in [failure counsel](../reports/counsel-261006-resource-temp-failure.md); no source test was weakened. Legacy r38/r33 Codex verification passes after historical helper mapping repair. New packages/relocation remain P7 gates. Source-lock remains unchanged r38.
