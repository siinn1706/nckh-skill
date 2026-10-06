# Source adoption, ownership và compatibility

## Authority, roots và evidence identity

`WORK = C:/Users/USER/Downloads/test-skill`; `KIT = C:/Users/USER/Downloads/test-skill/nckh-kit`; `SRC = C:/Users/USER/Downloads/test-skill/resources`. Các file paths dưới root viết rõ bên dưới là absolute named paths, không wildcard ownership. Existing sources chỉ đọc; new paths là proposed create khi cook, không implementation hiện có.

[Scientific report](../reports/researcher-261005-0036-scientific-sources.md), [other kits report](../reports/researcher-261005-0036-other-resource-kits.md), [primary refs](../reports/researcher-261005-0036-primary-aiops-sources.md) và [current-kit review](../reports/code-reviewer-261005-0036-current-research-kit.md) là evidence scope. Đã inventory metadata đủ bảy roots; đọc metadata không có nghĩa audit mọi script. No downloaded script execution ở planning.

| Evidence input | Fingerprint/hash đã đọc | Giới hạn |
|---|---|---|
| `WORK/plans/reports/source-manifest-261005-0036-scientific.json` | Raw SHA-256 `e10bfc3d2d682990bb40067aef9a1b9b15b2268d84923452acaf06b4d39ce959` | Final reviewed input, 197 metadata; selected byte hashes bên trong |
| `WORK/plans/reports/source-manifest-261005-0036-other.json` | Raw SHA-256 `a5f5687c44f8c19114a0f61f345b406ee2f0b2d7bde7089f9acbf6453032a3ed` | Final input, 231 metadata/11 selected groups/36 file hashes |
| `SRC/scientific-agent-skills-main` | Metadata fingerprint `9fc9e9b2b02047c24952f52557b24a9a211408c75399c096a99285bdaa6b2418` | 177 entries; root MIT, per-component rights khác nhau |
| `SRC/nature-skills-main` | Metadata fingerprint `a686ecafb3351902bd37a422a53abb518f47dd05f5f4133464cccc4c895a7098` | 20 entries; root Apache-2.0, nested/per-path review required |
| Current observed kit | Raw lock `671512337bf36942ab9b79eaac6fffac335280aaec45f8219301a7d7d87eb25a`, r34/281 pins/0 drift tại 00:41–00:45 +07 | Historical observation, not execution baseline; installed r25 riêng |

Các ZIP roots không có Git metadata; `main/master` folder suffix chỉ hint. Fingerprint/hash không là commit và không gán pinned commit cũ của package cho ZIP mới. Remote RCAEval/AIOpsLab/OpenTelemetry refs đã đọc primary anatomy, chưa có local bytes/commit receipt; P1/P5 resolve true version/license/snapshot hashes khi chọn component.

## Selected scientific transfer — no whole-package import

Mode `--port` là thiết kế selective; `EXISTS` reuse contract, `NEW` owned behavior/record, `CONFLICT` no literal import. Mọi adapted reference là self-authored từ cleared/public sources, ghi contributions; copied substantial bytes phải theo actual license/NOTICE riêng.

| Source under absolute `SRC` root | Disposition / owner / phase | Nội dung nhận và giới hạn |
|---|---|---|
| `scientific-agent-skills-main/skills/hypothesis-generation/references/causal_inference_and_claims.md` hash `0162cd131dd12c6235a3b78c033c685abd80e98d5f40f9fb297b4d8104f85122` | NEW refs / method / P2 | Claim type/estimand/rivals/falsifier; no lexical-lint scientific guarantee |
| `scientific-agent-skills-main/skills/hypothesis-generation/references/preregistration_and_open_science.md` hash `33788e3cd4eeb62e80e9fb952e3bfb532320d373e7b00ed7c0a75b4200ccdbf4` | NEW protocol / method / P2 | Dated freeze/amendments; no seven-CLI import |
| `scientific-agent-skills-main/skills/experimental-design/references/randomization_and_blocking.md` hash `fabcfae913397fb8c3018b959b67ddf8fe47322b40cbf4155d898fa11738e9ae` | NEW recipes / method+statistics / P2/P5 | Units/nesting/allocation/interference; workload/incident units task-specific |
| `scientific-agent-skills-main/skills/statistical-analysis/references/assumptions_and_diagnostics.md` hash `6e1ebc110c092845b93e5c6d28f38c8a990780105ba1865f0bd47c007620b073` | NEW statistics / P2/P5 | Assumptions/diagnostics; no blanket test/threshold/package runtime |
| `scientific-agent-skills-main/skills/statistical-analysis/references/reporting_standards.md` hash `0a30a1bec63231c94c9c285977acaa4218c50a34c8385857d18f62c61ac817b7` | NEW report contract / statistics / P2 | Unit/n/effect/uncertainty; handoff to existing paperwrite |
| `scientific-agent-skills-main/skills/statistical-power/references/simulation_based_power.md` hash `963fd56791e6db1bffb94efda7c9bef9c3195e3dec3e2a9918d17f3536ec150f` | NEW scoped recipe / statistics / P2/P5 | Generator/estimator/Monte Carlo failures; simulation power ≠ observed power |
| `scientific-agent-skills-main/skills/exploratory-data-analysis/scripts/missingness_leakage_audit.py` hash `28458714e80ee31db636c0265ba21e1623ba27816d31e236fdc9b873a5b78ffc` | Anatomy-only, NEW owned validator / dataset / P3 | Bounded intake/missingness/entity/time audits; do not execute/transplant script |
| `scientific-agent-skills-main/skills/{aeon,scikit-learn,timesfm-forecasting,shap}/references/` selected files per manifest | NEW AIOps refs / P4/P5 | Time/group splitting, available-at-time baselines, train-only pipelines, attribution limits; no checkpoint/runtime import |
| `scientific-agent-skills-main/skills/{datalad,get-available-resources,simpy,arbor}/` selected refs/helpers per manifest | EXISTS state + NEW reproducibility refs / P4/P6 | Provenance/effective resources/replications/failures; no Git-annex/agent tree/loop engine |
| `nature-skills-main/skills/nature-statistics/references/common-failure-modes.md` hash `e4db4cbcc5c2c64bbe40e54a0686986e1c540c0e7530fd3ed2902da92968876b` | NEW bounded scientific reporting / statistics / P2/P5 | Pseudoreplication/paired/uncertainty; venue policy only exact applicable profile |
| `nature-skills-main/skills/nature-experiment-log/templates/anomaly-log.md` hash `db2748355c7dda56388a48ab6961a3a97398f7aa17c6d8cef14841e3719cbfda` | NEW owned attempt/deviation refs / P6 | Actual attachments/conditions/run IDs; no lab equipment/Feishu/Obsidian dependency |
| `nature-skills-main/skills/{nature-data,nature-paper-card,nature-reviewer}/` selected metadata/refs per manifest | EXISTS evidence + NEW appraisal/FAIR refs / P2/P3 | Source/Analysis/Hypothesis distinctions/forensic arithmetic; no forced16sections/three reviewers or model scientific signoff |
| K-Dense biology/clinical-only, Nature Chinese patent, `what-if-oracle` CC-BY-NC-SA, figure asset trees | CONFLICT/no adoption | Không dán nhãn DevOps cho incompatible rules hoặc import assets/nested rights |

Braced selected source roots là nhóm đọc đã triage; exact files/hashes retained in machine manifests. Cook không copy directory closure từ nhóm này; chọn từng file/bytes và rights gate riêng.

## Other sources và primary DevOps/AIOps references

| Component/source | Choice | Target/dependency/limit |
|---|---|---|
| ClaudeKit E1 logs/investigation/performance, E2 Kubernetes/environment, E3 security/review/test/scenario | CONFLICT literal; independent public-source design | P3/P4 telemetry/DevOps/trust references; proprietary root conflicts MIT metadata/README; no secret decode/apply/delete/self-heal |
| ClaudeKit E4 loop/autoresearch | No adoption | Retain full trials/null/failures/heldout protocol; no single metric keep/discard research engine |
| ClaudeKit Marketing M1 analytics/A-B | No scientific transfer | Marketing roles stay; GA4/CAC/CVR/attribution không là AIOps telemetry/gold |
| Humanizer H1 `SKILL.md` hash `0612f1dfb1672b0ea9b97e139bf1f06cabe98d8b27424fe8ff01e1fb4cc99cad` | EXISTS baseline, no duplicate tasks | Humanwrite/taste post-cook; scientific hedging/facts protected |
| LanguageTool L1 LGPL + nested licenses | EXISTS optional diagnostic, no new integration | No Java/server/rules/dictionaries/core dependency; no VI module claim |
| Anthropic A1 `skills/skill-creator/scripts/aggregate_benchmark.py` hash `123ef128ea5ccc01a4b1ac212ef5567f21e9c13d3d240609780beeb3200c49aa` | Behavioral adaptation, no helper import | P6 paired same-case attempt/readout; missing/empty stats stay unknown, not zero |
| Anthropic A2 webapp-testing / `with_server.py` hash `b0dcf4918935b795f4eda9821579b9902119235ff4447f687a30286e7d0925fd` | Intent-only; reject helper transplant | Optional permitted dashboard evidence; shell/any-listener/undrained-pipe/child-cleanup flaws incompatible |
| Anthropic A3 MCP bounded collector | Optional task route, no default build | Only when actual source case needs it and exact primary API/version/permission verified; readOnlyHint not enforcement |
| Anthropic A4 docs quartet + unresolved doc-coauthoring | No literal copy/derive/import | Existing writer/document lanes; no prompt/code/assets import or new office dependency |
| [RCAEval](https://github.com/phamquiluan/RCAEval) | Metadata benchmark cards; individual data/code rights gate | AIOps/dataset; pin suite/system/modalities/labels/ref/splits. Root MIT excludes unresolved CausalRCA/RUN licenses |
| [AIOpsLab](https://github.com/microsoft/AIOpsLab) | Method anatomy reference | P4/P6 observation/action/reset/workload/fault/cleanup; actual cluster/fault execution separate grant |
| [OpenTelemetry](https://opentelemetry.io/docs/concepts/semantic-conventions/) | Bounded dictionary from reviewed official definitions | P3/P5 timestamp/units/resources/log/metric/trace keys; version/status/access/rights verified at cook |

## Source → producer → reader → artifact → verification

| Candidate pack | Producer + contributions | Named consumers / reader | Required task artifact/verifier |
|---|---|---|---|
| Statistical recipes | Owner-authored scoped recipes, selected K-Dense/Nature/official statistics refs | statistics+method / existing `KIT/scripts/search-resource.py` plus proposed typed dispatch | Applicable analysis plan; unit/assumption/uncertainty/stopping cases |
| Telemetry dictionary | Owner-authored primary OTel semantic snapshot/mapping notes | telemetry / same bounded reader | Telemetry manifest; unit/time/key/sampling/join/missingness cases |
| Benchmark cards | Owner-authored source-keyed RCAEval/AIOpsLab metadata | aiops+dataset / same bounded reader | Exact suite/data/labels/split/rights selection; no implied data access |
| Evaluation recipes | Owner-authored task metric/baseline/failure/leakage templates | aiops+statistics+method / same bounded reader | Evaluation protocol/readout; ranking/ties/temporal/injection/failure cases |

Pack record quantity/domain locale must follow useful reviewed content, no mandatory row quota. Raw scientific data/predictions/gold/runtime receipts stay private project-side. Local source ZIP fingerprint proves input identity only; new authored variant truthfully retains multiple source contributions and owned artifact hash without pretending upstream commit/copy.

## Concrete proposed contract ownership

| Owner | Proposed schema/module | Owned validator scope |
|---|---|---|
| Statistics P2 | `KIT/core/contracts/statistical-analysis.schema.json`, `KIT/core/statistics.py` | Plan/readout binding, independent unit, assumptions/uncertainty/failure denominators |
| Dataset P3 | `KIT/core/contracts/dataset-manifest.schema.json`, `KIT/core/contracts/split-manifest.schema.json`, `KIT/core/datasets.py` | Intake/rights/lineage/actual membership+interval overlap/decision-time access |
| Telemetry P3 | `KIT/core/contracts/telemetry-manifest.schema.json`, `KIT/core/telemetry.py` | Actual modalities/time/unit/key/join/quality |
| AIOps P4 | `KIT/core/contracts/aiops-evaluation.schema.json`, `KIT/core/aiops.py` | Task applicability/baselines/metrics/ties/gold isolation |
| Experiment P6 | `KIT/core/contracts/experiment-manifest.schema.json`, `KIT/core/contracts/research-run-receipt.schema.json`, `KIT/core/experiments.py`, `KIT/scripts/check-research-artifacts.py` | Read-only artifact graph/invalidation/actual receipt/cleanup; no runner orchestration |
| Controller + resource P5/P7 | `KIT/core/contracts/owned-resource-provenance.schema.json` plus existing registry/resources/build/reader dispatch | Additive owned-reference/reauthored-with-sources/owned-reference pin, contribution rights/hashes and legacy compatibility |

Source/evidence/claim/brief/receipt/task state/acceptance, bounded paths, existing resource selectors and process ownership are reused. Supported schema keyword subset unchanged; exact membership/count/variant constraints belong to owner validators. Current kit qualification protocol document/author/topic/claim-family untouched; scientific dataset/incident split has its own actual membership record.

## Sequencing, dependencies, risk và rollback

- P1 freeze routing/rights/baseline; P2 scientific design/analysis; P3 actual data/telemetry; P4 AIOps/environment; P5 controller serial exact identity/profile/base-case/source-kind prerequisites before reference pack registration/read; P6 actual run/pilot; P7 final reconciliation/freeze/qualification. Default sequential; independent source reads/reference drafts can parallelize, source mutations require file ownership.
- P2 method files hand off trước P6 links. P4 devops files hand off trước P6 modifications. P5 reader/resource patches hand off trước P7. Controller alone integrates schema package closure/catalog/profile/build/acceptance/evaluation/docs; existing dynamic schema lookup giữ nguyên trừ demonstrated requirement. Sole freeze owner P7. No mid-phase freeze race or repeated global count replacement.
- P7 exact migration surfaces exhaustively named in its file table and narrowed consumer inventory: catalog/build/acceptance/profile/evaluation/cases/families/tests/source-kind serializers/readers/public verifier if present/docs/closures. Preserve historical IDs/locks/qualification and installed state.
- Pre-freeze checks are domain/schema subsets independent of source lock. Sole candidate freeze follows complete handoffs/source-owner quiescence; pinned release/resource/build/closure regressions, `validate_cases→verify_source_lock`, full deterministic and packaging follow freeze. Any repair preserves failed attempt and uses corrective revision + affected descendant reruns.
- Risks: source rights contradictions; false causal/scientific claims; label/corpus/incident leakage; unbounded allocation/stream parsing; missing/failure as zero; runtime/budget/cleanup. [Acceptance matrix](./acceptance-matrix.md) owns concrete falsifiers.
- Controller-trusted caps checked before read/parse/allocation; streaming hashes and cumulative byte/record/output budgets; artifacts cannot raise caps. Oversize/cross-file cap breach refuses with bounded reason, no clipping-as-complete. Private labels/PII/source credentials never package.
- Rollback: preserve preimages and restore only unchanged owned upgraded artifact closures; registry/schema/reader/catalog/provenance mappings travel together with corrective source revision. Keep all original/failed/historical receipts, raw inputs and concurrently cooked baseline; no forced Windows lock unlock, global reinstall, cluster deletion or arbitrary process kill.

## Execution gates và evidence limitations

Actual source rights/version/native/API/runtime/pilot/grants resolve at cook, before relevant action. Core no-provider/no-cloud/no-install default; actual external operations only exact task authority. ON is public package contract; OFF internal comparison. Build/reader tests qualify mechanics, agent runs qualify observed route, owner use qualifies scoped feedback, scientific review needs actual protocol/data/reviewer. No lane can substitute for another.
