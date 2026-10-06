# Scientific sources → NCKH: selected adaptation analysis

- Ngày: 05/10/2026, Asia/Saigon. Mode: planning-only; workflow `ak-xia` Recon→Map→Analyze→Challenge; không chạy source scripts/install/copy package.
- Baseline planning: xem writer/visual/hooks của `plans/261004-0047-nckh-research-data-hooks-writing/plan.md` đã cooked theo user steering; không nhập lại. Quan sát riêng: catalog có 39 identities, docs có hai writer/research-purpose visual guard, plan live đang r34/in-progress với native gate mở. Nguồn concurrent có thể đổi.
- `nckh-kit/README.md` và root `README.md` không tồn tại; local authority thực là `nckh-kit/docs/index.md`, `nckh-kit/docs/research-and-writing.md`, registry/catalog và skill paths.
- Evidence bên dưới là đọc file/hash/metadata; không chứng minh scientific quality, package API đúng hiện tại, runtime enforcement hay cải thiện model.

## Source manifest và inventory đầy đủ

| Snapshot local | Metadata | Relevant cho phạm vi | Ngoài phạm vi | Ref/license |
|---|---:|---:|---:|---|
| `resources/scientific-agent-skills-main` | 177 | 66 | 111 | README/plugin khai K-Dense-AI/scientific-agent-skills; plugin 2.72.0; root MIT |
| `resources/nature-skills-main` | 20 | 19 | 1 | README khai Yuan1z0825/nature-skills; root Apache-2.0 |

Inventory toàn bộ 197 metadata, frontmatter description/license, disposition, selected anatomy và SHA-256 ở [source-manifest-261005-0036-scientific.json](source-manifest-261005-0036-scientific.json). “Relevant” nghĩa có khả năng thích nghi vào phạm vi; không phải đề nghị nhập 85 skills. `nature-shared` là support package; `nature-proposal-writer` có metadata name `researchwrite`, không suy identity từ tên folder.

Hai root không có `.git`; branch/ref/commit đều unknown. Không lấy `main` trong tên ZIP làm ref và không dùng commit của resource cũ trong kit để gán snapshot mới. Metadata fingerprint lần lượt `9fc9e9b2b02047c24952f52557b24a9a211408c75399c096a99285bdaa6b2418`, `a686ecafb3351902bd37a422a53abb518f47dd05f5f4133464cccc4c895a7098`; JSON ghi recipe, root anchors và selected-file hashes. README K-Dense khai 177, CITATION.cff vẫn ghi 163: dùng actual file count, không dùng badge/citation abstract làm inventory.

K-Dense relevant gồm 23 research/method/evidence, 21 computational methods, 11 scientific communication và 11 execution/ingestion; JSON phân loại mỗi entry. Biology/clinical/chemistry/physics/geospatial-only và workflow thương mại/cá nhân không fit đều exclude, gồm clinical reporting engines, drug/genomics/lab robots và manufacturing; không bỏ domain safeguards rồi tái dán nhãn AIOps. Nature loại Chinese patent workflow; 19 entries còn lại chỉ tham khảo với giới hạn locale/venue/runtime.

Root MIT của K-Dense không thay license từng skill: metadata có GPL/CC/Unknown/Proprietary/PolyForm ngoài MIT/BSD/Apache. Nature có 3 metadata MIT, 17 unspecified; Apache root và nested notices vẫn phải truy vết trước phân phối. `what-if-oracle` khai CC BY-NC-SA 4.0: no-copy candidate, giữ scenario reasoning generic và không coi narrative là causal estimate. `nature-figure` có third-party notices; không nhập asset tree. README promotional/scientific claims chỉ là source claims, chưa được xác minh ở lượt này.

## Source anatomy và selected transfer

Các đường dẫn trong bảng nằm dưới root tương ứng, đều là static evidence. Bốn owner mới cố định: dataset/statistics/telemetry/aiops; không tạo general ML workflow engine.

| Nguồn/path chọn | Anatomy và invariant có ích | Local target/giới hạn |
|---|---|---|
| K-Dense `skills/hypothesis-generation/references/{causal_inference_and_claims,preregistration_and_open_science}.md`; assets hypothesis/prediction/evidence templates | Question→claim type→estimand→rivals→falsifier→measurement→dated deviations. Lexical `scripts/lint_causal_claims.py` chỉ kiểm annotation/language | Mở rộng `nckh-method/references/causal-inference.md`, `research-protocol.md`; reuse source/evidence/claim IDs. Không clone seven CLIs hoặc lexical pass thành identification pass |
| `experimental-design/references/{design_types,randomization_and_blocking,factorial_and_doe}.md` | Unit, randomization, blocking, allocation seed, interference/pseudoreplication; scripts phụ thuộc scientific packages | Method owns design; statistics owns computation. Incident/workload/environment là independent units tùy protocol, request/log windows không mặc định independent |
| `statistical-power/references/{effect_sizes,simulation_based_power}.md`; `scripts/simulate_power.py` | Power dựa full generator/estimator; Monte Carlo CI; failures giữ denominator và reasons; search/confirmation tách | Statistics planning recipes; không chọn magic n/power 0.8 mặc định và không gọi simulation assumptions là real-system power |
| `statistical-analysis/references/{assumptions_and_diagnostics,test_selection_guide,reporting_standards}.md`; statsmodels/PyMC refs | Design before estimator; effect/uncertainty; temporal/cluster dependence; non-rejection không verify assumptions; posterior diagnostics riêng | `nckh-statistics` + `references/inference-and-reporting.md`; package adapters optional per approved project, no core install |
| `exploratory-data-analysis/SKILL.md`; `scripts/_tabular.py`, `missingness_leakage_audit.py` | Explicit supported formats, row/field caps, missing token≠zero, group/entity/time split audit; tokenization≠anonymization | `nckh-dataset`; define data/source/split/transformation cards; source code chỉ anatomy, re-author bounded checks nếu cook được duyệt |
| `aeon/references/{forecasting,anomaly_detection,datasets_benchmarking}.md`; `timesfm-forecasting/references/workflows.md` | Chronological/rolling holdout; available-at-forecast covariates; horizon-specific naive/seasonal baseline; thresholds fit validation; anomaly scores≠probabilities; pretraining overlap riêng | AIOps evaluation recipes cho forecasting/anomaly; no pretrained checkpoint/runtime import. Event-level alert cost, temporal dependence và incident boundaries phải do protocol định nghĩa |
| `scikit-learn/references/{model_evaluation,pipelines_and_composition}.md`; `shap/references/theory.md` | Independent/group/time split; train-only preprocess inside CV; fold SD≠CI; SHAP background/output/masker changes interpretation | `nckh-aiops` evaluation/ref + statistics diagnostics; SHAP model attribution không identify root cause, predictive success không chứng minh causal mechanism |
| `networkx` refs; `simpy/references/simulation-methodology.md`; `scripts/replication_runner.py` | Graph source/inferred edges; simulation conceptual model, warm-up, independent replications, RNG streams, conservation, operational validation; CI covers configured Monte Carlo noise | AIOps topology/RCA cards và simulation protocol; labels derived/simulation; model scenario contrast không là observed intervention effect |
| `datalad/references/provenance.md`; `get-available-resources/references/resource_semantics.md` | Input/output/command/environment lineage; effective resources là intersection inventory/affinity/quota/scheduler/runtime; unknown≠unlimited | Method/cook/devops reproducibility refs; không ép Git-annex/container runtime vào standard-library kit; inventory không grant GPU/CPU budget |
| `arbor/references/htr-methodology.md`; `scripts/tree.py` | Hypothesis-bound attempts, failed attempts, compact insights/artifact refs; helper scalar merge gate và repeated holdout feedback không enforce scientific admission | Reuse existing task/receipt model để ghi attempts; không nhập autonomous research tree engine, agent harness hoặc score-based acceptance |
| Nature `nature-statistics/references/{common-failure-modes,statistical-reporting,figure-statistics}.md` | Reporting unit/n, nesting, paired design, uncertainty, corrections; AUTHOR_INPUT_NEEDED khi facts thiếu | Statistics report→paperwrite handoff; general scientific rules thích nghi cho CS, journal-specific rules chỉ đọc khi đúng venue/year/track/type |
| Nature `nature-experiment-log/{SKILL.md,templates/anomaly-log.md}`; `nature-data/references/fair-metadata-checklist.md` | Raw attachments→dated Markdown record→anomaly/condition link; data dictionary, raw/processed separation, access/license/map to figures | Dataset experiment/incident log: run ID, workload/config/source hash, clock/timezone, anomaly/deviation; bỏ lab equipment IDs/Feishu/Obsidian dependency |
| Nature `nature-paper-card/references/evidence-and-provenance.md`; `nature-reviewer/references/forensic-consistency-audit.md` | Paper/External/Analysis/Hypothesis/User labels; locator modes; arithmetic proof separate aggregation ambiguity/provenance gaps; frozen reviews then audit | Research reader-card refs và review checklist; không ép 16 sections/3 reviewers/Nature criteria. Model review không independent scientific confirmation |
| K-Dense `literature-review/references/core_workflow.md`; `paper-lookup` refs; Nature literature pipeline | Search/export/screen/exclude/study-to-report mapping; metadata/abstract/full-text distinct | Extend research SLR refs; IEEE/ACM/software-engineering applicability cần primary sources. Không nhập weighted prestige scoring, daily cron, provider account hoặc external delivery |

K-Dense components thường gồm SKILL→references→templates/CLIs→tests: JSON ghi anatomy 22 selected skills. Nature routers dùng manifest/static/core/fragments/shared packages, experiment log chỉ Markdown/templates; JSON ghi 8 selected packages. Source CLIs được đọc để xác định inputs/dependencies/outputs, không chạy. Upstream “tested/production-tested” hoặc bundled tests không chứng minh results của kit.

## EXISTS / NEW / CONFLICT map

| Thành phần | Trạng thái | Quyết định integration |
|---|---|---|
| Source/evidence/claim IDs, locators, receipt/task state, authorization/preservation | EXISTS | Reuse shared contracts; add domain contracts khi cần, không thay verdict semantics |
| Method/protocol, research review modes, paperwrite/humanwrite, visuals, hooks | EXISTS | Add scoped refs/owned handoffs; baseline writer/visual/hooks không thuộc upgrade này |
| Scientific dataset profile/split/transformation/provenance | NEW | `skills/core/nckh-dataset/`, `core/contracts/dataset-card.schema.json`, `split-manifest.schema.json`; sở hữu scientific files, không DB migration |
| Statistical analysis plan/readout/calculation receipts | NEW | `skills/core/nckh-statistics/`, `core/contracts/statistical-analysis.schema.json`; separates computational/inferential/human gates |
| Telemetry signal/time/topology/sampling/cardinality map | NEW | `skills/core/nckh-telemetry/`, `core/contracts/telemetry-manifest.schema.json`; roots này không có full OpenTelemetry contract, cần primary pack của controller |
| AIOps benchmark/task/evaluation contract | NEW | `skills/core/nckh-aiops/`, `core/contracts/aiops-evaluation.schema.json`; exact benchmark release/splits/metrics/labels/time budget; no generic training engine |
| `nckh-data` DB owner, marketing `nckh-analytics`/`nckh-experiment` | CONFLICT nếu nhập scientific scope ngầm | Keep owner semantics; add explicit route/handoff to four new owners, preserve existing identity/tests |
| New re-authored reference packs vs resource schema | CONFLICT | `resource-registry.schema.json`/`resource-provenance.schema.json` chỉ copied-upstream/retrieved-snapshot; thêm truthful re-authored provenance variant compatible, không fake copied lineage |
| Reader `scripts/search-resource.py` | EXISTS + NEW dispatch | Existing JSONL reader có bounds/hash/domain/consumer/locale/genre; JSON/CSV branches theo reviewed IDs; thêm exact typed records/selection tests cho pack, không coi extension là reader support |
| Broad providers/models/GT scripts/biology assets/Arbor engine | CONFLICT | Reference/selective re-author; credentials/install/model execution/network/external-write grants riêng |

## Bốn pack: source → reader → artifact → verification

Reader dự kiến là `nckh-kit/scripts/search-resource.py` sau reviewed registry/typed selector; chỉ tạo pack có consumer rõ, không bắt mọi skill có JSONL. Mỗi record giữ source locator/hash/as-of/license, adapted-vs-copied, scope/version/applicability và uncertainty. Source-lock/registry/schema/reader phải đồng bộ; public resource_access ON, OFF chỉ internal comparison.

| Pack đề xuất dưới `core/profiles/resources/` | Source và consumer | Artifact của task | Verification và giới hạn |
|---|---|---|---|
| `statistical-recipes.jsonl` | Selected design/statistical/power + Nature reporting refs; method/statistics | Source-keyed candidate procedure, unit/assumption/estimand requirements | Exact recipe/consumer/domain retrieval; missing unit/dependence→pending; approved real calculations đối chiếu analytic/reference oracle; model/human inference riêng |
| `telemetry-dictionary.jsonl` | Controller primary OpenTelemetry pack + local telemetry contract, không lấy domain vocab từ biology | Clock/signal/unit/aggregation/topology/sampling/cardinality map | Exact version/unit/source; missing/sampled signal≠zero; reconcile trace/log/metric timestamps; không giả OTEL conformance từ static dict |
| `benchmark-cards.jsonl` | Controller primary RCAEval/AIOpsLab pack + source/data/evaluation docs | Benchmark release/access/labels/splits/tasks/metric/resource card | Match exact release/task; official evaluator được kiểm riêng khi approved; hidden labels/test seals; card≠downloaded dataset/real run |
| `evaluation-recipes.jsonl` | Aeon/sklearn/SHAP/SimPy + benchmark primary sources; aiops/statistics | Frozen metric/threshold/window/horizon/ablation/uncertainty plan | Per-incident/time leakage and validation-only tuning; oracle/metric definition/tests; false alarm/delay/top-k denominator; simulation labels; causal assertions need design review |

## Challenge matrix và risk

| Decision | Source way | Local choice | Risk nếu sai / resolution |
|---|---|---|---|
| Necessity/overlap | 197 identities, nhiều package engines | 4 bounded owners + existing refs | >2 ngày rework nếu taxonomy/routing overlap; frozen ownership map xử lý |
| Scientific unit | Some examples independent/tabular | Explicit incident/workload/cluster/time design | Pseudoreplication/leakage làm conclusions vô hiệu; protocol + held-out oracle + independent review |
| Causality | Hypothesis/SHAP/simulation/graph helpers | Prediction/association/root-cause hypothesis/identified effect tách | RCA attribution có thể bị gọi false causal proof; require perturbation/identification assumptions and competing causes |
| Data access | Cloud/ELN/provider/Screenpipe/platform integrations | Rights/redaction/local artifacts; optional adapters | Security/private telemetry leakage; exact target/egress/provider grants before run |
| Maintenance/dependencies | Pinned scientific package matrix, Python 3.12+ nhiều nơi | Core stdlib contracts; project-specific optional runtime | >2 ngày host/package mismatch; verify selected official API/version at cook, no bulk install |
| New resource provenance | Existing kit only copied/retrieved source-kind | Compatible additive re-authored lineage | Misattribution/source-lock drift; exact source/adaptation record and rollback as one closure |
| Evaluation independence | Arbor repeated test-gate; prestige-weighted literature ranking | Dev/validation/final sealed test, source-scope evidence | Adaptive holdout contamination and publication bias; retain attempts/selections/null results, final independent gate |

Bốn critical assumptions cần resolve trước cook: ownership/contract fit, rights/egress, runtime matrix và independent final evaluation (mỗi assumption có khả năng security hoặc >2 ngày rework). Risk Medium theo Xia; planning tiếp tục được, no blanket import. Telemetry semantic completeness, benchmark acceptance và causal/statistical scientific validity không được đóng bằng file tests.

## Concrete edits và acceptance dự kiến

- Extend `skills/core/nckh-research/references/review-modes.md` hoặc linked `software-research-review.md`: search/export/query timestamps, inclusion/exclusion, report→study map, software benchmark appraisal; source/framework choice theo domain.
- Extend `skills/core/nckh-method/references/method-and-argument.md` với links tới `causal-inference.md`, `research-protocol.md`, `reproducibility.md`; preserve literary/argument routes và method no-execution boundary.
- Four new skill trees own linked references; `cook` owns approved run execution/attempt receipts; statistics owns calculation contract; devops owns resource/environment/process cleanup; dataset owns integrity/splits; telemetry owns signal meaning; aiops owns benchmark evaluation.
- Update exact catalog/base cases/router docs/source-lock, named pack registry/provenance/reader and owning validation; avoid inventing current counts after four identities until controller freezes target set.
- Acceptance examples: reject request-window IID inference; reject test-fitted preprocess/threshold; flag SHAP→causal RCA; preserve failed Monte Carlo attempts; distinguish missing telemetry from zero; reconcile metric units/clocks; mark benchmark metadata-only; preserve unavailable human/reviewer/runtime gates.
- Verification gates stay separate: metadata/hash/license; schema/reader; actual calculation/run; leakage/metric oracle; model review; independent statistical/domain review; final real-data/benchmark acceptance. No synthetic fixture is human gold or production evidence.
- Rollback: candidate scientific closures/registry/catalog/schema/lock together; retain source manifests, failed attempts and historical receipts; preserve concurrent cooked baseline and installed state. No stable/public/runtime activation in this analysis.

Status: DONE_WITH_CONCERNS
Summary: Đã triage đủ 197 metadata và phân tích selective transfer cho bốn scientific owners cùng method/research/reproducibility refs. Artifact ở report + JSON, không implementation.
Concerns/Blockers: Snapshot thiếu Git identity; individual/nested rights và official package APIs cần verify khi chọn bytes/runtime; nguồn concurrent thay đổi; scientific/native/human acceptance chưa được thực hiện.

