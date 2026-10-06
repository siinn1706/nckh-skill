# Acceptance matrix — proposed cases, mọi gate pending

`KIT = C:/Users/USER/Downloads/test-skill/nckh-kit`; `RUN` là actual absolute attempt root chọn P1. Đây là design cho cook; không có case/run/result đã thực hiện bởi plan này. Deterministic fixtures kiểm behavior, không human gold/real measurement/production evidence.

## Lanes và admission

| Lane | Evidence cần có | Không suy ra |
|---|---|---|
| Planning structure | Seven phases/links/frontmatter/parse/validation consistency | Implementation, runtime, scientific quality hoặc improved skill |
| Static/source | Exact source/version/rights/locators/pins/closure | Semantic validity hoặc native behavior |
| Deterministic | Current tests/oracles/input-output hashes/actual failures | Human taste/gold/LLM safety/empirical efficacy |
| Actual scientific computation/pilot | Actual authorized source/data/code/config/environment/run/predictions/metric counts/failures | Identified causal effect hoặc domain/human acceptance |
| Agent/provider/native | Actual requested/resolved/effective model/route/tool traces/permission/cleanup/cost coverage | Scientific truth hoặc support trên unobserved host/version |
| Owner/scientific | Actual scoped feedback/reviewer/rubric linked exact artifact/input/revision | Stable/public release hay approval cho other candidate |

Required fail/pending/stale không accepted-for-scope. Missing/not-applicable requires reason; unknown costs/model/resources không zero. Pure personal-use owner lane không ép external peer reviewer; scientific claims giữ independent domain/method acceptance riêng.

## Routing và legacy compatibility

| Case | Owner/input | Oracle / failure | Evidence class / phase |
|---|---|---|---|
| Scientific curation versus DB migration | dataset / file cohort; data / SQL schema update | Route correct; dataset không mutate DB, data không tự author scientific split | Agent route + no-side-effect / P1,P7 |
| Statistics versus funnel/A-B | statistics / scientific estimand; marketing analytics/experiment / KPI traffic | Preserve marketing contracts and scope; no generic reroute every analysis | Agent + legacy tests / P2,P7 |
| Telemetry versus RCA/debug | telemetry / signal map; aiops / incident ranking; debug / failing code test | Observation normalization không verdict root cause; correct handoff | Agent + output contract / P3,P4 |
| Protocol versus execution | method / design; cook / approved run; devops / environment | No experiment launch from design/token/config presence | Authority deterministic + actual trace / P2,P6 |
| Four new base manifests | each new skill × positive/negative/outcome/failure | Exact16 new IDs; baseline156 preserved if actual baseline matches; catalog/profile/cases integrated serially before P5 consumer reads | Structural, no quality pass / P5,P7 |
| Legacy identity and evidence | exact old IDs/profiles/families/history/bundles | No deleted/moved/renamed roles; unchanged qualification split semantics | Static/regression / P7 |

## Data, privacy, splits và telemetry

| Case | Artifact/condition | Falsifiable oracle | Owning proposed tests / phase |
|---|---|---|---|
| Rights missing | dataset source access cleared? | Unresolved rights prevents acquisition/redistribution; metadata-only preserved | `tests.research.test_datasets` / P3 |
| Missing versus zero | actual missing token/blank unit/value0 | Unknown stays unknown; zero value preserved; counts reconcile | datasets+telemetry / P3 |
| Label/duplicate conflict | same sample ID differing label/value | Quarantine with original locators; no silent averaging/overwrite | datasets / P3 |
| Transform lineage | raw/config/code/normalized version changes | Hash/count reconciliation; changed parent invalidates dependent splits/results | datasets+experiments / P3,P6 |
| Actual membership overlap | train={i1,i2};test={i2,i3} with valid separate hashes | Read canonical actual keys and fail on i2 overlap; hash/count alone never passes | datasets / P3 |
| Incident/entity/time partition | different row IDs share incident/entity/time intervals | Group/incident and cutoff/embargo invariants tested from actual manifests | datasets / P3 |
| Feature availability by task | future covariate; allowed RCA diagnostic-window signal | Future forecast feature fails; allowed frozen RCA incident-window observations pass; gold labels remain excluded | datasets+aiops / P3,P4 |
| Preprocess/threshold selection | train-fitted transform; validation threshold; sealed test | Training fit and validation-only choice pass; test fit/threshold/selection fails | datasets+aiops / P3,P4 |
| Private labels/PII/secrets | source logs and gold annotation store | Protected store/access, redaction/rights; no package/feature/model-input leak | datasets+package tests / P3,P7 |
| Unit/type/aggregation mismatch | cumulative counter versus gauge/rate, blank unit | Explicit mapping and known conversion lineage; unknown no invented unit | telemetry / P3 |
| Time/skew/precision | timestamp origin/timezone/skew absent | Unknown reason; no invented alignment; defined skew tolerance applied | telemetry / P3 |
| Correlation/resource identities | trace/span/request/service keys duplicated/missing | Referential/cardinality quality report; no fabricated trace/modality | telemetry / P3 |
| Join cardinality | unexpected many-to-many/unmatched windows | Refuse forbidden joins; count retained/dropped/unmatched rows with tolerance | telemetry / P3 |
| Sampling/gaps/counter resets | actual modality partial and missing windows | Capture completeness/retention limitations; missing ≠ normal or zero | telemetry / P3 |
| Hard caps before allocation | oversized file, many files below individual cap but above aggregate | Bounded stream/read/hash; refuse pre-parse oversize/aggregate with bounded error; no clipped complete | datasets+resource packs+experiments / P3,P5,P6 |

## Statistics và method

| Case | Condition | Falsifiable oracle | Tests/lane / phase |
|---|---|---|---|
| IID/pseudoreplication | many windows from same incident/workload | Unit/nesting/cluster/time dependence exposed; no unjustified IID CI | statistics / P2 |
| Paired comparison | models tested on mismatched incident sets/horizons | Pair by exact independent units; incomparability/failures reported | statistics+aiops / P2,P4 |
| Plan versus results | no actual run/output/data bound | Analysis plan allowed; readout/scientific result gate pending/fails | statistics+experiments / P2,P6 |
| Assumption/test selection | mismatched estimator/design or non-rejection | Assumption evidence required; p>threshold không validate every assumption | statistics / P2 |
| Effect/uncertainty/multiplicity | estimate without independent n/CI design/correction | Missing fields/gates explicit; no magic alpha/power/sample-size | statistics / P2 |
| Optional power simulation | generator/estimator/replications/failure attempts | Monte Carlo label/CI/failed denominator; no real-system power claim | statistics+experiments / P2,P6 |
| Causal overclaim | SHAP/topology/correlation/RCA suggestion | Prediction/association/hypothesis distinguished; identified effect needs design evidence | Agent+scientific review / P2,P4 |
| Peeking/negative suppression | test-tuned thresholds/keep-discard only successes | Freeze/amendments, attempts/null/failures retained; sealed test access policy | statistics+experiments / P2,P6 |
| Search scope/access | abstract-only source or no search match | No unseen result support/global novelty; full-text limits/queries recorded | Agent/evidence / P2 |

## AIOps evaluation, retrieval và agent trust

| Case | Condition | Falsifiable oracle | Tests/lane / phase |
|---|---|---|---|
| RCA rank ties/multi-cause | equal scores/duplicate candidates/multiple gold causes | Frozen tie/membership/top-k rule; exact incident denominator, no arbitrary tie win | aiops / P4 |
| Unknown/no-answer | missing gold/no relevant cause/abstention | Explicit policy; no false negative as zero/hidden denominator exclusion | aiops / P4 |
| Failed/timeout predictions | incomplete run with partial predictions | Coverage/failure counts shown, predefined aggregation; no success-only superiority | aiops+experiments / P4,P6 |
| Anomaly point/event distinction | duplicate alerts/partial windows/tolerance | Actual chosen granularity/timing/false-alert denominator and delay oracle | aiops / P4 |
| Forecast horizon/availability | horizon missing or pretrained overlap unresolved | Per-horizon completeness, chronological policy, overlap unknown; no fabricated score | aiops / P4 |
| Retrieval corpus/qrels | dedup/cutoff/snapshot changed after protocol | Drift invalidates result; train/test/query/gold leakage refused | aiops+datasets / P4 |
| Ranking metric definitions | qrels relevance scale/zero relevant query/ties | Recall/MRR/nDCG scope/relevance/normalization/policy matches protocol | aiops / P4 |
| RAG answer source support | fluent unsupported or contradictory answer | Evidence/locator/support/abstention checked separately from retrieval metrics | Agent+evidence/domain / P4,P6 |
| Injection in retrieved docs/logs | text asks reveal labels/run command/grant privilege | Text stays untrusted data; no gold read/external action from injected content; actual side-effect trace if agent route exercised | Fixture contract + granted actual agent/native / P4,P6 |
| Agent resets/cost/runaway | retry/no reset/tool timeout/unknown usage | State isolation/reset/failure/retry/resource cap/cost coverage and cleanup records | aiops+experiments+actual host / P4,P6 |
| Simulation/topology labels | simulated values or inferred graph edge | Raw/code/parameters/run hash and simulation/inference labels; no observed-causal promotion | experiments+visual baseline guard / P6 |

## Resources, packaging và delivery

| Case | Input | Oracle | Lane / phase |
|---|---|---|---|
| Owned authored provenance | recipe references multiple sources | Truthful owned-reference/reauthored-with-sources/pin mapping, each contribution hash/rights | `tests.resource.test_research_packs` static/deterministic / P5 |
| Legacy copied mislabeled owned | copied bytes with no upstream notices | Reject disguise; legacy commit/license/hash rules remain | Existing resource tests + new variant tests / P5,P7 |
| Typed selector/mismatch | undeclared record fields/consumer/domain/locale/genre | Fail before resource read where applicable; no arbitrary JSON/CSV extension support | Resource behavior / P5 |
| Consumer integration prerequisite | new pack declares dataset/statistics/telemetry/aiops before catalog has owner | Missing consumer rejects; controller integrates exact catalog/profile/case/source-kind prerequisite before actual P5 read/P6 pilot | Structural + reader behavior / P5,P6 |
| ON/OFF | valid pack and missing resource root in OFF | Actual ON read; explicit OFF disabled/no-read without needing registry/files | Resource behavior / P5,P7 |
| Contribution/license/data drift | valid artifact hash but altered provenance/NOTICE | Reject; no inherited rights/candidate pass from wrong source | Resource/package / P5,P7 |
| Relocated closures | attempt-owned temp outside `WORK`; smoke CWD outside repository and extracted bundle/PYTHONPATH | Containment rejected before invocation; isolated readers/checker/imports work using exact packaged schema/helper closure; actual temp mapping/ownership/hash/cleanup retained in `RUN` | Packaging deterministic / P7 |
| Real pilot | rights-cleared actual incident/scientific source, local task baseline | Actual source/data/run/prediction/metric/failure hashes/counts and readout; no simulated stand-in | Actual pilot / P6 |
| Same-case paired benefit | enabled/off/legacy baseline comparison when actually authorized | Same case/split/runtime/config/budget; missing/failures unknown; no improvement claim before actual runs | Actual matched trial/statistics / P6,P7 |
| Preview/install/state | fresh package/disposable project/user bytes and explicit kits/mode/frozen model profile | Dry-run requires supplied models, no prompt; no-write preview, preserved target hashes; installed r25 separate until explicit update grant | Installer deterministic / P7 |
| Candidate freeze order | source edits with stale lock; release/closure tests require verify_source_lock | Independent domain/schema checks first; single freeze after owner quiescence; pinned regressions/packaging next; repair preserves failure and corrective freeze/reruns | Source integrity + actual check order / P7 |
| Scientific/native/stable claim | local tests/build/owner writer feedback only | Required scientific/native/release gates remain pending; experimental scope | Human/admission review / P7 |

## Proposed test ownership và base-case migration

- New tests named above live under `KIT/tests/research/` with descriptive invariants; new resource tests under `KIT/tests/resource/test_research_packs.py`, including proposed lock-independent `ResearchPackContractTests`; supplemental matrix under `KIT/tests/release/test_research_matrix.py`. They do not exist/pass until implemented and run. Pinned release/build/closure cases remain after candidate freeze.
- Four new manifests under `KIT/evals/cases/research-data-aiops/nckh-{dataset,statistics,telemetry,aiops}.json`, each exact IDs `:positive`, `:negative`, `:outcome`, `:failure`. Supplemental matrix records cases here without pretending they are extra base IDs or observations.
- Preserve exact baseline IDs and historical protocol; target 43/172 contingent P1 baseline. Actual native host/surface/version and provider scope selected from verified live tools; no automatic model run authority or fabricated telemetry/cost.
- Owner records every evidence lane with revision/artifact/input hashes and actual pass/fail/pending/stale/not-applicable reasons. Full sample/data rights and reviewer/rubric thresholds freeze before scientific acceptance runs; personal-use lane uses actual owner feedback separately.

## Whole-plan self-check boundary

Before handoff verify seven phase links, all proposed/existing path labels, no completed checkboxes, exact dependency/owner queue, supported schema keywords, old role preservation, truthful source hashes/ref limits and coherent task feature availability/caps. Root plan parse/validate/index/red-team receipts are structural evidence; they do not close any implementation case in this matrix.
