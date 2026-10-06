# Independent review — experiment graph and offline pilot

Status: **DONE_WITH_CONCERNS**

## Scope and authorization

- Live scope reference: controller `/root` delegation to `/root/review_experiment_graph`, received 2026-10-06, revision 1. Scope is read-only P4/P6 source/artifact review plus focused lock-independent tests and disposable counterexamples. The only retained write is this report.
- Work context: `C:/Users/USER/Downloads/test-skill`; timezone `Asia/Saigon`.
- Reviewed revision: the source hashes recorded below, and frozen experiment manifest SHA-256 `8ad6731d9611f69ea6e13ae15fab33be3fb7550688458075c461e0e5875d4d03`.
- Original RUN files, source, tests, installed skills, source lock and builds were preserved. No pilot rerun, provider, network request, native agent evaluation, global install, source freeze or pinned test occurred.
- Review skill: `nckh-review`; authorization/evidence/preservation/acceptance and reviewer model/context policies read. Requested profile/tier: inherited session, deep scrutiny of public contracts. Resolved/configured/applied host model and effort have no separately verified run receipt here; effective model/effort, model independence, usage/cost and usable context window remain **unknown**. Context independence is a bounded independent source/artifact inspection; scientific/human expertise is not claimed.
- Historical memory was used only to maintain the separation between project-local development evidence, native/model telemetry and scientific/human acceptance. Current findings and numbers were checked against live files.

## Finding summary

| Priority | Finding | Affected scope | Owner / action |
|---|---|---|---|
| P1 | Domain readouts accept outputs absent from their actual run receipts | Standalone statistics and AIOps readouts | Domain owners: bind exact path/hash/kind output provenance to validated terminal run receipts |
| P2 | Ranking ignores the selected completed denominator policy | RCA/retrieval and agent success policy | AIOps owner: implement or reject unsupported denominator choices |
| P2 | No-gold ranking rows become defined zeros despite undefined policy | RCA hit/MRR and retrieval MRR | AIOps owner: apply no-relevant policy consistently |
| P2 | Retrieval permits candidates outside corpus and grades outside frozen scale | Retrieval evaluation | AIOps owner: check actual document membership and frozen relevance grades |
| P2 | Simulation parameter refs are omitted from receipt inputs | Simulation experiment receipts | Experiment owner: include exact simulation parameter bindings in frozen run closure |
| P2 | Fixed shared output paths cannot preserve changed partial output across retry | Multi-attempt experiment graph | Experiment owner: define attempt-specific output ownership or explicit separate amended graphs |
| P3 | Frozen prose asks for MAE per partition, realized machine protocol is test-only | Pilot reporting fidelity | Controller: preserve protocol and record the narrower realized scope/deviation |

The **actual single successful forecasting pilot's arithmetic remains correct**. Findings in other task branches do not invalidate its measured numerical outputs. P1 prevents treating a standalone domain validator pass as proof that the referenced process produced its selected readout outputs.

## Located findings and reproduced evidence

### P1 — Domain outputs do not have to be outputs of a bound run

Locations: [aiops.py](../../nckh-kit/core/aiops.py), lines 243–248 and 255–283; [statistics.py](../../nckh-kit/core/statistics.py), lines 114–126.

The validators read run records, check task/status and a set of parent hashes, then separately read predictions/results or statistical outputs. They never require the selected output references to equal any exact output path/hash/kind in those run receipts. The statistics check proves equality between a result declaration and a selected JSON file; that file can be independent of the receipt.

**Independent counterexample:** copied the actual pilot's bound graph files into an owned disposable tree, retaining its full original receipt and unchanged original outputs. For the AIOps readout, changed one prediction by +123, saved replacement predictions plus recomputed replacement metrics, and pointed the readout to those replacement files. For the statistical readout, changed estimate to 0, saved a matching replacement statistical output, and changed the readout output reference. Neither replacement was an output of the full original run receipt. Both validators returned `contract: pass`, `scientific_acceptance: pending`.

This is a provenance failure, independent of whether the receipt's host observations are authentic. The experiment validator does check its receipt-selected predictions/metrics, which contains this gap for those outputs when the complete experiment graph is the admission route. It does not establish receipt provenance for an independently submitted statistical readout.

Action: validate the structured terminal receipt contract at the domain admission boundary, require exact input path/hash pairs, and require selected prediction/metric/statistical outputs to be exact appropriately typed outputs of the selected completed run. Add wrong-output/new-output negative cases using a full receipt. Keep host authenticity separate.

### P2 — Frozen denominator policy is ignored for ranking

Locations: [aiops.py](../../nckh-kit/core/aiops.py), lines 149–172 and 194–204; [aiops-evaluation.schema.json](../../nckh-kit/core/contracts/aiops-evaluation.schema.json), `metrics[].denominator_policy`.

The schema permits `all-issued` and `completed-with-coverage` for every task. Ranking always divides by `counts.total`; agent success also always divides by that total. The selected denominator field only changes forecasting behavior.

**Counterexample:** RCA with one completed correct prediction and one failed prediction, metric `hit@k`, and `denominator_policy: completed-with-coverage` returns 0.5, completed1/total2. The requested completed denominator would yield 1.0, with failed coverage separately retained. Alternatively this policy should be rejected for RCA instead of accepted and silently ignored.

The actual pilot completed3/issued3 for each forecasting baseline, so its MAEs are unaffected.

### P2 — No-gold ranking coverage is reported as defined zero

Locations: [aiops.py](../../nckh-kit/core/aiops.py), lines 32–36 and 164–172.

`ranking_metrics` returns hit0 and MRR0 for an empty accepted set. Only recall/nDCG can return None. Consequently `no_relevant: undefined-with-coverage` never reaches undefined handling for RCA hit/MRR or retrieval MRR.

**Counterexample:** one completed RCA row, ranking `["a"]`, accepted `[]`, undefined-with-coverage policy, metrics hit@k and MRR. Result: both 0.0 with coverage defined1/undefined0. This conflates absent valid gold with a measured incorrect answer.

Action: preserve the no-gold state for every applicable ranking metric, or explicitly constrain the supported metric/policy combinations. Test RCA hit/MRR and retrieval MRR, in addition to the existing nDCG-only case.

### P2 — Retrieval corpus membership and frozen grade scale are not enforced

Locations: [aiops.py](../../nckh-kit/core/aiops.py), lines 38–44, 100–108 and 163–165.

Protocol validation checks document IDs and grade bounds, but prediction scoring does not require ranked/accepted IDs to be documents in that corpus and checks relevance only against the global 0–30 range. It does not check the frozen `relevance_scale`.

**Counterexample:** retrieval protocol declares document `d1`, relevance scale `[0,1,2]`; prediction ranks/accepts `a`, relevance `{"a":3}`. It returns nDCG1.0 and defined coverage. Both corpus membership and scale differ from the declared protocol.

Action: resolve canonical actual corpus/qrels membership and validate prediction/gold candidate IDs and relevance grades against it before calculating metrics. No real retrieval or RCA execution was observed in this pilot.

### P2 — Simulation parameter bytes are missing from the receipt input closure

Locations: [experiments.py](../../nckh-kit/core/experiments.py), lines 26–28, 35–40 and 157–164.

Simulation parameters are checked by `reader.binding`, but `manifest_bindings` does not include `simulation.parameters`. Receipt validation therefore accepts a completed run that omits a parameter reference from `inputs`.

**Counterexample:** valid synthetic simulation manifest includes a separate `sim-params.json` ref, seed7, replications2, generator and required validity fields. Manifest validation passes; `ref in manifest_bindings(manifest)` is False; a completed simulation receipt with no parameter input passes.

Action: include parameter references in the frozen binding closure with duplicate/alias handling. This is static contract evidence only; no simulation was run.

### P2 — Multi-attempt preservation conflicts with one shared output set

Locations: [experiments.py](../../nckh-kit/core/experiments.py), lines 88–99, 120–125 and 200–208.

A frozen manifest permits exactly one prediction path and one metrics path. Every completed receipt must contain the entire same expected path set. A failed attempt can retain partial outputs, but a later attempt cannot put its changed outputs at distinct paths within the same frozen graph; shared-path replacement makes the previous failed receipt's hash stale.

**Counterexample:** synthetic failed receipt with a retained partial `predictions.json` passes. Replacing that path with a different retry prediction makes the original failure receipt fail with `stale research artifact binding: predictions.json`. A new attempt path is outside the frozen allowed paths. Distinct completed-attempt output sets cannot satisfy the current all-expected-outputs rule.

Action: define output paths per attempt, or require a separate frozen amended graph/readout for a retry and retain a linking attempt ledger across graphs. Document that route and test failed-partial → changed retry, not only failed-with-empty-outputs. The actual pilot has one completed attempt and no runtime failure, so this conflict was not exercised there.

### P3 — Pilot prose and selected partition scope differ

Location: [research-protocol.md](../runs/nckh-upgrade-261006-0850-attempt-01/research-protocol.md), line9; `aiops-evaluation.json`, `evaluation_partition: test`, sample_ids2023–2025; `pilot-code.py`, six-prediction assertion.

The frozen prose says “MAE per partition/baseline”; the machine protocol and observed run compute test MAE only. Train/validation membership exists but no train/validation prediction/MAE outputs exist. The readout accurately labels its values as test MAE.

Action: preserve the frozen original, record test-only realized scope and the wording discrepancy in the readout/deviation record, and make subsequent protocols unambiguous. Adding new calculations to the historical receipt would require a new actual run/amendment; it is unnecessary for accepting the existing test-only arithmetic demonstration.

## Actual pilot reconciliation

RUN: [nckh-upgrade-261006-0850-attempt-01](../runs/nckh-upgrade-261006-0850-attempt-01/).

### Input and graph integrity

- Independently walked exact `{path,sha256}` refs from experiment plan/readout, receipt, statistical/AIOps readouts, oracle, cleanup and paperwrite handoff: **33 unique references, 0 hash mismatches**.
- Re-ran direct validators against current original files: experiment plan pass/not-run; experiment readout pass/completed-unreviewed/attempts1; statistics pass/independent_n1; AIOps pass/units3. Every scientific acceptance result remained pending.
- Actual readout validation used 301,386 aggregate bytes and 1,273 JSON objects/array members under its selected 1 MiB per-file, 8 MiB aggregate, 10,000-record and 1 MiB checker-output caps.
- Independently projected actual `pilot-data/raw.json` API rows into the normalized fields, sorted by year, and compared exact values: **26 matching rows, years2000–2025, blank source unit preserved**.
- Actual partition membership is train20/validation3/test3, chronological and sample-disjoint. The country is the same series across all partitions; entity independence is not asserted.
- Forecast code uses only prior calendar-year rows, with rolling origins. Previously observed test-year values may enter later origins under this fixed rolling procedure. Historical publication/vintage availability is explicitly unverified; this is not a blind or real-time forecast evaluation.

### Independent exact arithmetic

The review computed rational endpoint drift directly from raw-reconciled observations, independently of the production adjacent-change loop and without executing either pilot script.

| Year | Baseline | Exact prediction | Exact absolute error |
|---|---|---:|---:|
| 2023 | naive | 99680655 | 671537 |
| 2023 | drift | 1107750527/11 | 3876415/11 |
| 2024 | naive | 100352192 | 635494 |
| 2024 | drift | 2331298597/23 | 8581819/23 |
| 2025 | naive | 100987686 | 610841 |
| 2025 | drift | 2447538139/24 | 9173491/24 |

| Quantity | Exact value | Decimal |
|---|---:|---:|
| Naive MAE | 1917872/3 | 639290.6666666666 |
| Drift MAE | 6726274519/18216 | 369250.9068401405 |
| Drift-minus-naive paired error mean | -4919044265/18216 | -270039.7598265261 |

All six predictions, targets, target times, origins, both MAEs and the signed contrast reconcile within absolute tolerance1e-6. Each baseline has completed3/issued3, failed0, unknown0; statistical denominators are completed3/total3. One country series is the independent unit; three target-year errors are temporally dependent. No p-value, SE, CI, causal identification or generalization was inferred.

### Process, failures and authenticity

- Receipt SHA-256: `bf35052ed80b662083e794ea965afead685b59f3e4a3ce32b5c20730353c1281`.
- Cleanup SHA-256: `9625c48a4361747d4b10640c2e195b1a34278f67d99e1a7756ec486f3fabd34c`.
- Preserved receipt/logs agree on PID31900, parentPID6968, CPython3.12.10 Windows executable, local `-I` argv, exit0, completed-unreviewed, six predictions, 26 observations, three targets and reaped owned child.
- Stdout is hash-bound and states the arithmetic/development semantics; stderr is genuinely the hash of empty bytes. Wall time is recorded as 0.06199999999989814 monotonic seconds. UTC timestamps run from 03:11:27.015701 to03:11:27.084073 and reconcile within the validator tolerance.
- CPU, peak memory and provider cost stay null. Provider unused and no pilot egress is stated. The supervisor uses the exact Popen handle and `communicate`; it does not execute manifest argv.
- Source/schema checking establishes **integrity and internally consistent preserved observations**. This reviewer did not witness that past launch. No independent OS CreationDate is recorded; receipt text discloses this. Hashes and validator passes cannot authenticate invented host observations, nor establish absence of unrelated user processes. Cleanup is scoped to the supervisor-owned child.
- First P6 contract log preserves two failures and two errors from missing transitive fixture bindings; later log preserves 13passing tests. Current focused rerun passed27 tests. Those prior fixture failures remain visible and are not experimental process failures.
- Original acquisition receipt retains five WinError10061 failures; attempt02 retains AIOpsLab LICENSE404. These are acquisition history, separate from the one successful pilot process.
- Source-lock revision38 is intentionally stale until P7. Fresh package/build/isolated projected helper closure and current pinned regressions remain outside this review. The run graph hashes named code files; imported KIT helpers and preparation metadata/selection dependencies need their own closure evidence for relocated reproduction. This does not change the independently verified arithmetic.

## Checks performed and their limits

1. From KIT: `python -B -m unittest tests.research.test_experiments tests.research.test_aiops` → exit0, **27 tests passed**, 1.969s.
2. Native Python deterministic scripts inspected original RUN files and recomputed hashes, direct graph/domain checks, raw projection and exact Fraction arithmetic → exit0; original artifacts unchanged.
3. Disposable fixture/copy counterexamples reproduced every P1/P2 finding above → native script exit0, owned temporary trees cleaned by `temporary_tree`. These are negative contract evidence, not actual scientific runs.
4. Existing experiment test exercises isolated checker via `python -I`, fresh output and refusal to overwrite. Recorded commands remain data. This verifies repository checker behavior; P7 relocated/package closures remain pending.

## Scoped gate matrix

| Gate | Verdict | Evidence / limit |
|---|---|---|
| Current actual pilot input/output hashes | pass |33refs, zero mismatches; raw projection exact |
| Single actual pilot descriptive arithmetic | pass |6predictions, two MAEs and paired contrast independently reconciled |
| Actual readout unit/coverage labeling | pass |3target years,1series; missing/failed coverage explicit; no uncertainty claim |
| Preserved process receipt/cleanup consistency | pass for integrity |Source/log/receipt agreement; historical host authenticity unverified here |
| P4 public ranking/oracle/denominator contract | fail |Located reproduced counterexamples |
| Standalone domain receipt-output provenance | fail |Full unchanged receipt with replacement outputs passes |
| P6 simulation parameter closure | fail |Parameter omitted from receipt input binding |
| P6 retry with changed retained partial outputs | fail |Shared frozen path conflict |
| Frozen prose versus realized partition scope | concern |Machine test-only scope is clear; prose says per partition |
| Source lock/current package/helper relocation | pending P7 |No freeze, pinned check or new build performed |
| Human/scientific/native/provider acceptance | pending / not exercised |Model/deterministic review does not close these gates |

Recommendation: retain the actual pilot as a valid bounded descriptive arithmetic demonstration with consistent preserved execution evidence. Repair the located public-contract failures and rerun their focused negative cases before treating P4/P6 validators as complete. Preserve original artifacts, historical failures and the current gate boundaries.

## Reviewed source identities

| Path (relative to KIT) | SHA-256 |
|---|---|
| core/experiments.py |23a6ff2ec1861d3e472d9ba9e7381a4a17c3130d8081a9fe08a01f9593997f52 |
| core/aiops.py |0e119a67b1d7d5d331b7478b90b55cff99dc2037e87a6097afa1db075f85bb6f |
| core/research_io.py |824742c52ea0a92432abe6c6669e2fca27adb350da19697f6d5141df209ef96b |
| core/statistics.py |f4cf3cc89bab15e125c5ab86c8baaa55bb396bbd7126369584315d33757b764f |
| core/datasets.py |85f8b6fe3d0074bbcfb329c874235127a0bef081fe4cf7a7121a3552ff9b97aa |
| core/telemetry.py |ff04a2ceb4534f8edc9a151c2d929e88929605e50f472b2f8c5a06c694b6eda3 |
| core/contracts/experiment-manifest.schema.json |71c1fdaa47b1a638c472071dea69ec999a18831efaa9b4ce5b764f168d225a40 |
| core/contracts/research-run-receipt.schema.json |679813ee91a3778ff781fb94851f6bc084be47a4f43061310aa1d95fce9cc58c |
| core/contracts/aiops-evaluation.schema.json |29c76211576029d7d07b98c5f0dafd90e5f1ad7185f71812303623f4ddf371de |
| scripts/check-research-artifacts.py |6c53facf930683dd5addb872f7965308ffe3048879b4a6be6c70208fcddb5023 |
| tests/research/test_experiments.py |3bc02a509906e6f91c765c05180cf33b5dc81e36bd2e1dcef33efb7bb945303b |
| tests/research/test_aiops.py |1237ba5837415b4547f7103f30f32902ca94b4aaa3ed6ddd4d50f68e52bd5526 |

## Unresolved questions / blockers

No user clarification is required for this review. Controller/domain owners must resolve the located provenance, denominator, no-gold, retrieval membership/scale, simulation-closure and retry contracts. P7 closure/release tests and human/scientific acceptance remain separate pending work.

Status: DONE_WITH_CONCERNS  
Summary: Current pilot hashes and exact descriptive arithmetic reconcile; seven located concerns remain in public contracts/reporting scope.  
Concerns/Blockers: P1 receipt-output provenance and the reproduced P2 cases prevent full P4/P6 contract acceptance.

<oai-mem-citation>
<citation_entries>
MEMORY.md:195-198|note=[project-local evidence and scientific acceptance boundaries]
rollout_summaries/2026-10-01T08-00-56-b2U0-nckh_portable_skill_kit_direct_development_evaluation.md:49-52|note=[retain failures and distinguish receipt integrity from qualification]
</citation_entries>
<rollout_ids>
01a0f67b-15f5-7842-898e-4f8b69d873c0
</rollout_ids>
</oai-mem-citation>


---

# Focused re-review — revision 2, 2026-10-06

**Latest status: DONE.** The seven original findings above are preserved as historical evidence. They are closed for the repaired source and the observed supplemental arithmetic scope described here. This does not close P7 package/source-lock/relocation or human/scientific/native/provider gates.

## Authorization and reviewed revision

Live scope reference: controller `/root` follow-up delegation to `/root/review_experiment_graph`, 2026-10-06, revision 2: independently verify repairs and supplement, append this report only, use disposable owned probes if required, preserve original RUN/source files. No pilot/supplement execution or source edits were performed by this reviewer.

The controller's proposed resolution of the partition wording gap was a separately frozen and observed local stdlib calculation. The review checked the resulting additional artifacts, rather than treating the proposal or a prose amendment as execution evidence. Original manifest, original process receipt and original three output hashes remain exactly those recorded in revision 1.

Model/context evidence boundaries remain unchanged: inherited reviewer session; no separately verified effective model/effort receipt or scientific/human acceptance.

## Closure of original findings

| Original finding | Re-review verdict | Independent current evidence |
|---|---|---|
| P1 domain receipt-output substitution | closed | Repeated replacement-output probes against disposable copies of actual full receipt; statistical estimate0 rejected as absent actual run output, substituted AIOps predictions/metrics rejected as absent completed run outputs |
| P2 completed denominator policy | closed | RCA hit@k, retrieval nDCG and agent success each yield1.0 with one completed success and one failed row under completed-with-coverage; all-issued coverage remains explicit |
| P2 no-gold defined zeros | closed | RCA hit@k and MRR are both None, coverage defined0/undefined1 under undefined-with-coverage; regression tests also preserve explicit zero policy |
| P2 retrieval corpus/grade scale | closed | Ranked/accepted outside corpus and in-corpus relevance grade3 outside frozen[0,1,2] both rejected |
| P2 simulation parameter receipt closure | closed | Parameter ref is now in manifest bindings; removing it from the receipt inputs rejects with “every exact frozen” |
| P2 changed partial output retry | closed | Nonempty one-row partial prediction retained at first attempt path; changed complete two-row second attempt plus recomputed metrics accepted as preserved-failures; first hash unchanged; cross-attempt output alias rejected |
| P3 MAE per partition reporting | closed by separate observed supplement | All six train/validation/test baseline MAEs independently reconciled, original partitions unchanged, three insufficient-history outcomes explicit, original six test prediction values exactly unchanged |

### Repair behavior and compatibility

- [research_io.py](../../nckh-kit/core/research_io.py) now exposes `receipt_outputs`, which checks task, terminal status, exact input path/hash pairs and canonical unique output path/hash/kind/count records. AIOps admits selected predictions and metrics only from completed receipts; computed statistical outputs also require completed receipt output membership. Preserved failed statistical readouts retain their failure route. This closes the original output-substitution failure; the helper's documented scope does not authenticate host observations.
- [aiops.py](../../nckh-kit/core/aiops.py) now applies selected ranking/agent denominators, preserves empty-gold None values for applicable ranking metrics, and rejects retrieval candidates/grades outside the frozen document/scale declarations.
- [experiments.py](../../nckh-kit/core/experiments.py) includes simulation parameters in the frozen input closure and supports optional exact `attempt_id` routes. The schema rejects unknown fields; semantic checks refuse mixed scoped/shared routes, missing per-attempt predictions/metrics, routes above the attempt limit and receipts using another attempt's outputs.
- The [reproducibility reference](../../nckh-kit/skills/core/nckh-method/references/reproducibility.md) documents distinct attempt outputs, terminal output provenance, simulation input closure and the integrity-versus-authenticity boundary.
- The original legacy unscoped single-attempt manifest still validates unchanged. The independent retry probe used a **nonempty partial artifact** and **different subsequent prediction content**, extending the checked-in empty-array partial fixture to directly exercise the historical failure mode.

## Current checks

1. Independent current rerun from KIT:

   `python -B -m unittest tests.research.test_experiments tests.research.test_aiops tests.research.test_statistics`

   Exit0, **59 tests passed**, 3.140s. This is a focused rerun by this reviewer; the retained controller log p6-domain-tests-attempt-04.txt (historical evidence path: `../runs/nckh-upgrade-261006-0850-attempt-01/p6-domain-tests-attempt-04.txt`; unavailable in the cleaned checkout) separately records110passing tests in6.605s.

2. Independent disposable negative probes all produced their required rejection; completed-denominator and preserved-retry probes produced their required values/states. Script exit0. Temporary trees were removed by their owning contexts; original RUN bytes were not modified.

3. Direct validation of current original `experiment-readout.json`, `aiops-readout.json` and `statistical-readout.json` passed. Experiment remains attempts1/completed-unreviewed, AIOps units3 and statistics independent_n1. Scientific acceptance remains pending.

4. Retained [p6-isolated-graph-check-02.json](../runs/nckh-upgrade-261006-0850-attempt-01/p6-isolated-graph-check-02.json) reports pass for the unchanged experiment graph, read_only true and commands_executed false. The reviewer did not execute its recorded argv or regenerate that receipt.

5. Independent exact reference walk across original readouts/handoff/cleanup and added supplement freeze/receipt/oracle verified **38 unique references, zero mismatches**. Original checks remain bounded local integrity evidence.

## Supplemental calculation — actual artifacts and independent reconciliation

Artifacts: [code](../runs/nckh-upgrade-261006-0850-attempt-01/partition-supplement.py), [freeze](../runs/nckh-upgrade-261006-0850-attempt-01/partition-supplement-freeze.json), [process observation](../runs/nckh-upgrade-261006-0850-attempt-01/partition-supplement-receipt.json), [output](../runs/nckh-upgrade-261006-0850-attempt-01/partition-supplement-output.json), [oracle](../runs/nckh-upgrade-261006-0850-attempt-01/partition-supplement-oracle.json).

The new freeze explicitly states that it adds missing train/validation partition reporting and preserves the original graph/test receipt. Its input refs bind the actual code, unchanged protocol, normalized observations, original split manifest and environment. The separately preserved process observation records PID23416, parentPID1616, local isolated CPython argv, exit0, completed-unreviewed and the exact owned handle reaped. Freeze/start/end chronology agrees. Both actual stdout/stderr files are empty and hash to their empty-byte digests. CPU, memory and provider cost remain unknown/null.

The supplemental record explicitly says it is **not a research-run-receipt graph promotion**. It does not replace the original graph, make additional original-run predictions, erase the previous scope discrepancy or silently redefine the protocol. The source and preserved observation support a separate local descriptive calculation. This reviewer did not witness its past process launch; host authenticity limitations from revision 1 remain.

### Prediction coverage and membership

Independently checked the exact Cartesian membership of26 actual sample IDs ×2 baselines: **52 unique rows**, **49 completed**, **3 unknown**. Every row's target/year agrees with the unchanged observed dataset and its partition agrees with the actual split membership file.

Unknown rows are exactly:

- `VNM:2000 / naive`: no preceding observation.
- `VNM:2000 / drift`: fewer than two preceding observations.
- `VNM:2001 / drift`: fewer than two preceding observations.

Each unknown has a reason and null prediction/absolute_error. No numeric zero or completed forecast is imputed. Every completed prediction and absolute error was independently recomputed using exact Fraction endpoint drift, absolute tolerance1e-6. The six original test prediction and target values match **exactly**, beyond the stated tolerance.

### Per-partition descriptive MAEs

| Partition | Baseline | Issued | Completed | Unknown | Exact MAE | Decimal |
|---|---|---:|---:|---:|---:|---:|
| train | naive |20 |19 |1 |20019765/19 |1053671.8421052631 |
| train | drift |20 |18 |2 |18021114848/125307 |143815.70740660938 |
| validation | naive |3 |3 |0 |2506879/3 |835626.3333333334 |
| validation | drift |3 |3 |0 |251468338/1197 |210082.1537176274 |
| test | naive |3 |3 |0 |1917872/3 |639290.6666666666 |
| test | drift |3 |3 |0 |6726274519/18216 |369250.9068401405 |

Every numerator, completed denominator, issued count and unknown count reconciles. Policy is explicitly completed-with-coverage. The two train MAEs use different warm-up memberships (19 versus18 completed years); they are individual descriptive baseline summaries, **not a paired contrast on identical year sets**. The original paired three-test-year contrast remains unchanged.

The independent unit remains one temporally dependent country series with blank source units and disclosed prior access. No confidence interval, causal/generalization/blind-efficacy or human/scientific signoff is added.

## Re-review source hashes

| KIT-relative path | SHA-256 |
|---|---|
| core/aiops.py |2f14103a61d0b3930fbdc617e7ebf495ba60b675a7f3d3e2f4316c9ad33d225b |
| core/statistics.py |8269caefaf55dce59558e93de380285796d6cfd85f669f0dd6a02f2f7930c2c5 |
| core/research_io.py |650e3130bac9e910b92ccde552c31b2a304c1887bc0b4b79fd4a75a68dcaebb4 |
| core/experiments.py |fe533623a0084d59d587f644b32133a83a8d60a8bf338b059c5812062643fdc1 |
| core/contracts/experiment-manifest.schema.json |e1ef757720c458a28d4b60f3798cb6b4f000cf8f67c530937012e105d35fd540 |
| tests/research/test_aiops.py |21a5df63c4dd67cceb310bc65c6b37f587971142f1c3bca5fd0c28b40361e90a |
| tests/research/test_statistics.py |edfeecaecf624ae1237e88ad9f8a9b181456707504d6abcdf6971016137075c8 |
| tests/research/test_experiments.py |c1f5bb267288bd2dff45eb6cfd2d6dbde617afd36499f2861863eee6ee59a10f |
| skills/core/nckh-method/references/reproducibility.md |2f6928c4f5ba8670cdc93664b392a7b5e4fa146c5c009e76e6fc09ad53a02a09 |

## Added evidence hashes

| RUN-relative artifact | SHA-256 |
|---|---|
| partition-supplement.py |49e39f1ab1c53312d8e8c68c9d9a91d429f532c483d60e978cdd104cef7c2839 |
| partition-supplement-freeze.json |55ac3edbcac99f971c6d27a863425f6967d285981ed143fbe1c9a3b3de38f8a0 |
| partition-supplement-receipt.json |778eab2ea1eb10fd78cb23523409a3da7f47fc6176a029006c3039147d83fffe |
| partition-supplement-output.json |b351f446aab07bc9f6b44410bff02113dc09bc3ea5c77e2873c5ed573911f1f7 |
| partition-supplement-oracle.json |a6c0555ae893c84b7de54ce15f140821951a1af4d30972e0355abc1872256e2b |
| p6-domain-tests-attempt-04.txt |5729a24752b0be327e8e4837291641584b172b1fa3413a4efde9efc74275cbfa |
| p6-isolated-graph-check-02.json |817e3b4ec4bd087316e8d3f517732144a24d762b7d65b9fe0261fc6cdbb56bbf |

## Residual scope and final disposition

No reproduced residual remains in the seven repaired findings at these source hashes. Legacy original graph compatibility is verified; retry behavior is verified by synthetic contract evidence, not a new real failed scientific run. Relocated/source-locked package closure, stable/public release and human/scientific/native/provider acceptance remain outside this focused re-review and retain their own pending states. No unresolved user question is required here.

Status: DONE  
Summary: The seven historical findings are closed by independently verified source repairs or a separately observed, hash-bound partition supplement; original pilot artifacts and failure history remain preserved.  
Concerns/Blockers: None within this focused re-review scope; independent host authenticity and P7/human/scientific gates are not promoted by these checks.


