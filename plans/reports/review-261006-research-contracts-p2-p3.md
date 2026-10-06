# Independent review — P2/P3 research contracts

Ngày: 2026-10-06, Asia/Saigon. Snapshot: 09:29 +07:00.

**Current outcome:** see **Re-review 2 — final bounded review** below. All seven reproduced baseline findings and the two incomplete repair cases are closed for the inspected revision/cases. Original failed snapshots remain in this report; scientific/native/provider acceptance remains separate and pending.

## Scope, authority và evidence

- Authorization reference: current user `AGENTS.md` public-contract review gate; controller delegation `/root/review_research_contracts`, P2/P3 scope of the accepted P7 review. This record documents the inherited read/review/report scope; it grants no provider, publication, installation or product-repair authority.
- Owned output: this report only. Source, tests, plans and existing receipts were not edited. Local fixture directories created by the existing `temporary_tree()` helper were cleaned by that helper. No background process was started.
- Flags: `--auto`; no `--yagni`. No network, provider, installation, global source-lock/build or package qualification run.
- Review skill: `nckh-review`, including authorization, evidence, preservation, acceptance and handoff policies. Logical review requirement: deep/public-contract inspection. Execution: same reviewer agent, fresh delegated context; effective model/effort/cost/window telemetry unavailable. No claim of model independence, human review or scientific acceptance.
- Read the four source owners, four schemas, three research test modules, P2/P3 phase files, acceptance matrix and named P3 attempt manifests/receipt. Supporting reads: `core/paths.py`, `core/schema.py`. Earlier memory supplied only the schema-subset/evidence-boundary reminder; all findings below use current source and actual local reproduction.

## Verdict of the 09:29 baseline

**P2/P3 deterministic contract gate needs repair before candidate freeze.** The existing 47 focused tests pass, and the current World Bank pilot artifacts reconcile. Seven reproducible contract failures remain. They affect admission/data integrity; they do not establish that the current pilot produced incorrect observations or that a scientific result was accepted.

Severity: P1 = invalid scientific input/readout can receive `contract: pass`; P2 = boundedness or supported numeric/telemetry behavior is incorrect and needs correction before claiming the corresponding gate.

## Findings

### P1 — Raw counts and transform lineage are assigned from claims instead of observed rows

Location: `nckh-kit/core/datasets.py:43`, `:87`, `:95`–`:101`.

`raw` artifacts are hash-checked but never counted. `available` assigns the complete declared `counts.raw` to **every** raw hash. Each transform compares its declared input count to that assignment, and adds its declared output count without inspecting intermediate output membership/count. Global excluded/quarantined totals are not reconciled with observed raw rows or each transform's dispositions.

Reproduction: start with `dataset_fixture(root)`; replace `raw` and the transform input with a hash-bound JSON `[]`, update `sources[0].archive_sha256` to that hash, and keep six normalized/sample-index rows and declared raw/input/output counts of six. Actual result: `contract: pass`, despite zero actual raw rows. This uses valid hashes and closed-schema fields.

Impact: omitted input rows or fabricated retained rows can pass the purported raw-to-normalized lineage check. Multiple raw sources also inherit the same global row count, so a legitimate multi-source transform cannot reconcile their actual combined cardinality reliably.

Owner/action: P3 dataset owner. Bind an explicit source-row projection/index or format-specific bounded row reader; count each actual source/intermediate artifact and reconcile the transform's combined inputs, output membership and dispositions. Preserve source-format flexibility: the real World Bank payload has metadata plus a 26-row data array, so counting only the outer JSON array would also be incorrect. Add empty-raw, multi-source and intermediate-output-count counterexamples.

### P1 — Readout membership and task identity are unrelated to bound dataset/split/run content

Location: `nckh-kit/core/statistics.py:98`–`:118`; positive fixture `nckh-kit/tests/research/test_statistics.py:101`–`:122`.

The readout verifies input/run hashes and a result JSON echo, but never parses/validates the dataset, split or run identity, nor reconciles its observation/independent-unit memberships with those artifacts. Internal membership reconciliation at lines 28–40 only compares fields in the readout itself.

Reproduction: independently validate the six-member `fixture-task` dataset/split from `dataset_fixture()`/`split_fixture()`. Bind those actual artifacts to `StatisticsTests.readout(root)`, whose task remains `fixture-comparison`, observation IDs remain `w1,w2`, and denominator remains two. Keep the existing fixture's `run.json` body `deterministic fixture artifact; not a real run`. Actual result: `contract: pass` with the unrelated task/memberships and text run body.

Impact: a correctly hashed dataset/split can lend apparent provenance to results from another task/population; a copied result/denominator JSON is sufficient to satisfy the current numeric binding check. This conflicts with P2's actual data/run/results and wrong-unit rejection requirement.

Owner/action: P2 statistics owner, coordinated with the P6 run-contract owner. Validate dataset/split parent and task identities; bind actual analysis-unit membership and recorded outcomes to the chosen analysis cohort. Require a structured run receipt of the owning accepted contract, or retain an explicit pending gate until that receipt exists. A statistical validator need not rerun an estimator or infer scientific validity.

### P1 — Forecast decision time can move after the target without invalidating availability

Location: `nckh-kit/core/datasets.py:151`–`:157`; `nckh-kit/core/contracts/split-manifest.schema.json`, `features` object.

Feature checks compare two caller-supplied times. No bound prediction origin/horizon or target interval constrains `decision_at`; there is also no feature-source binding or exact feature coverage check. The RCA diagnostic-window check is specific to RCA and does not constrain forecasting.

Reproduction: the split fixture's target sample `s5` has interval `[50,51]`. Set its forecasting feature to `available_at=55`, `decision_at=60`, `diagnostic_window_end=60`. Actual result: `contract: pass`. The forecasting decision occurs after the target window, while all currently checked comparisons are satisfied.

Impact: future target-window data can be admitted by moving the declared origin forward. Merely comparing `available_at <= decision_at` does not bind availability to the frozen forecasting task.

Owner/action: P3 split owner with P4 forecast protocol owner. Bind prediction origin and horizon/target membership in the frozen protocol; constrain the forecast origin relative to the actual target interval, and validate each feature's provenance/availability against that origin. Preserve the approved RCA incident-window exception. Add the post-target-origin counterexample; do not infer an arbitrary universal cutoff for other tasks.

### P2 — Counter reset detection incorrectly applies to normalized rates/deltas

Location: `nckh-kit/core/telemetry.py:114`–`:115`, `:129`–`:137`.

Rows are taken from normalized outputs. When `source_type=counter`, every decrease in those output values is classified as a cumulative reset, including when `aggregation=rate` or `delta`.

Reproduction: actual cumulative values `[10,15,17]` at times `[1,2,3]`, normalized per-second rates `[null,5,2]`, explicit source/output/code/config bindings and reconciled counts. No cumulative reset occurs. With `resets=[]`, validation fails with `actual cumulative counter resets differ from declared lineage`. Setting `resets=['s3']` produces `contract: pass`, accepting an invented reset.

Impact: a normal falling rate is rejected, or the user must falsify reset lineage to pass. Normalized rate/delta semantics therefore do not preserve source counter semantics.

Owner/action: P3 telemetry owner. Calculate reset evidence from the bound cumulative source sequence, with a source-to-output map; validate rate/delta outputs under their own semantics. Add decreasing-rate-with-monotonic-source and actual-source-reset cases.

### P2 — Record budget is checked after the complete array is parsed and allocated

Location: `nckh-kit/core/research_io.py:88`–`:100`.

`rows()` calls `bound_json()`, which executes `json.loads()` for the complete array, then checks its row count. Per-file/aggregate byte limits apply first, but the independently trusted record limit does not prevent parsing/allocation.

Reproduction: `ArtifactReader(root, ResearchLimits(records=1)).rows()` on a hash-bound 10,000-element JSON array. A wrapper around the real `json.loads()` observes the fully allocated 10,000-element list before the subsequent `research record budget exceeded` exception. Existing tests only exercise `count()` directly and byte limits; they do not test this order.

Impact: the hard record cap cannot bound row-object allocation or parser work. A compact array below the 8 MiB file cap can exceed the intended 100,000-record cap substantially. The reader remains byte-bounded; this finding does not claim an unlimited file read.

Owner/action: shared reader owner. Use bounded incremental row parsing or a safe preflight that counts top-level canonical rows before constructing them. Charge the graph's cumulative record budget before each materialized row. Add an allocation-order test with a deliberately low trusted record cap.

### P2 — Protected-label references are neither verified nor tied to a separate access artifact

Location: `nckh-kit/core/datasets.py:19`–`:25`, `:42`–`:46`; `dataset-manifest.schema.json`, `labels.references`.

`protected-evaluation-only` requires nonempty provenance/references, but the curated validator does not resolve/check those reference hashes or their separation from other data paths. The only feature check is that the caller supplies an empty `feature_fields` list.

Reproduction A: declare `references=[{'path':'nonexistent-protected-labels.json','sha256':'0'*64}]` and nonempty provenance. The reference does not exist; actual result is `contract: pass`. Reproduction B: use the exact normalized artifact as the protected label reference; that alias also passes.

Impact: the artifact can claim an actual protected evaluation label store while its evidence is nonexistent or aliases another dataset artifact. This reproduction does not prove that every normalized target column is a model feature; feature meaning still depends on the owning protocol. It proves that the declared protection/reference boundary is unchecked.

Owner/action: P3 dataset owner. Validate the explicitly authorized label-store identity/access metadata and hashes through an appropriate separate resolver; enforce protocol-required path/artifact separation, or expose the unresolved reference/access gate as pending. Do not read protected label values through a feature reader merely to close this check. Add missing/stale label references and forbidden alias cases.

### P2 — Finite paired inputs can return infinite descriptive metrics

Location: `nckh-kit/core/statistics.py:142`–`:145`.

`finite_number()` validates only the operands. Floating subtraction and summation can overflow; the derived differences and mean are not checked.

Reproduction: `paired_difference_summary({'i1': -1e308}, {'i1': 1e308})` returns both difference and mean as `inf`. Both inputs are finite. A later `allow_nan=False` serialization can then crash instead of preserving a failed calculation.

Owner/action: P2 statistics owner. Validate derived differences and aggregate values, use a numerically appropriate aggregation, and raise a bounded `ContractError` or preserve a failure when the result is not representable. Add finite-input subtraction and accumulation overflow cases.

## Executed checks

From `C:/Users/USER/Downloads/test-skill/nckh-kit`, Python 3.12.10:

```powershell
python -B -m unittest tests.research.test_statistics tests.research.test_datasets tests.research.test_telemetry
```

Actual output: `Ran 47 tests in 0.628s`, `OK`; exit code 0. These tests are deterministic contract fixtures.

Inline local counterexamples above ran through PowerShell stdin into `python -B -`, using the existing `dataset_fixture`, `split_fixture`, `StatisticsTests.readout`, `telemetry_fixture`, `save_fixture` and `temporary_tree` helpers. The completed counterexample run exited 0. An initial setup attempt exited 1 because `StatisticsTests.readout` overwrote the same `dataset.json` path used by another fixture, correctly causing `stale research artifact binding: dataset.json`; the second attempt isolated construction order. That setup failure is retained here and is not a product finding.

Recomputed the current named P3 artifacts with the current validators. The complete recomputed dictionary equals `p3-artifact-checks.json`. Additional direct inspection of the pinned World Bank payload verified:

- Actual source data array: 26 rows; normalized rows: 26; sample index: 26.
- Source archive hash equals the bound raw artifact hash.
- Each normalized sample's year, value and original blank unit match its raw source record.
- Actual partitions contain train 20, validation 3, test 3, with unique complete membership.
- Holdout status remains `prior-access-disclosed`; telemetry remains `not-applicable` with no invented operational modalities.

No external source was refreshed. This verifies the local dated snapshot and derivative integrity, not current World Bank values, publication-time availability, scientific efficacy or native/provider behavior.

## Independent gate matrix

| Gate | Review state | Evidence / boundary |
|---|---|---|
| Closed supported schemas, duplicate/nonfinite JSON rejection | pass for exercised cases | Current schema/reader and passing focused tests |
| Per-file and aggregate bytes before parse | pass for exercised cases | Existing positive/negative read tests |
| Record budget before row allocation | fail | 10,000 rows allocated under `records=1` |
| Actual normalized/sample/partition membership, missing versus zero | pass for exercised cases | Focused tests plus direct 26-row pilot check |
| Raw/intermediate counts and transform lineage | fail | Empty raw admitted as six input rows |
| Protected label-store evidence/access separation | fail | Nonexistent reference and artifact alias admitted |
| Forecast availability bound to actual frozen origin | fail | Origin 60 admitted for target `[50,51]` |
| Plan does not invent observed results | pass for exercised cases | Existing statistics plan rejection tests |
| Readout task/unit/run integrity | fail | Unrelated valid dataset/split and text run admitted |
| Telemetry missing/zero, joins/cardinality and unknown modalities | pass for exercised cases | Current telemetry tests |
| Source counter versus normalized rate reset integrity | fail | Falling rate forces invented source reset |
| Finite descriptive output metrics | fail | Finite inputs produce `inf` |
| Current local P3 pilot artifact integrity | pass | Recomputed receipt and direct source-row comparison |
| Scientific/data interpretation and actual protected/blind evaluation | pending | Validators already preserve pending acceptance; pilot discloses prior access |
| Frozen source-lock/build/package/native/provider qualification | pending, intentionally unrun | Controller defers stale r38 pin/build reconciliation to P7 |

## Reviewed source identities

SHA-256 at the reviewed snapshot; workspace-relative paths. Future source changes invalidate findings/check reuse for the affected owner.

| Path | SHA-256 |
|---|---|
| `nckh-kit/core/research_io.py` | `a2fe0ee3656f21a8175d4865778d0897fe28635be7308a2e3457614335641661` |
| `nckh-kit/core/statistics.py` | `f4833eebb1517b2fc18b1adc0ad7719c413e4891ca6904516d3201adb64a30a3` |
| `nckh-kit/core/datasets.py` | `a74892aa212a6264d4410ae8b03039f1af54792a3dec622217b5acb3f715e8d1` |
| `nckh-kit/core/telemetry.py` | `eeccab363fa836b0d28c4d4be62ed7407a21e807ad9129d38cdde0ab9dfe0304` |
| `nckh-kit/core/contracts/statistical-analysis.schema.json` | `f3e5e8f03dfaf518f37c63b503a26fb308edbf790f1e1b3552bbc3fdcf43e229` |
| `nckh-kit/core/contracts/dataset-manifest.schema.json` | `017767836521fce060a68cc594a2afcf11a75b7f706f39aa23438a1c87f15568` |
| `nckh-kit/core/contracts/split-manifest.schema.json` | `a36a2df17ea85252853f1c177592057a53894d7d592a007f49a117d39e908968` |
| `nckh-kit/core/contracts/telemetry-manifest.schema.json` | `6e75e2f15337f8fc5c2b80f1d8f4e8cc1cff9ac4a644da5e858941eea1322dbb` |
| `nckh-kit/tests/research/test_statistics.py` | `51cf5b123ff0382dfa3836a378c1bc786f12942b0ceb19ce798d22fe75ff74cf` |
| `nckh-kit/tests/research/test_datasets.py` | `a884c4a3d7f1cc833bbeb19c041ddde7f54aa1c256ef38f372e2baacfa89b458` |
| `nckh-kit/tests/research/test_telemetry.py` | `fc3760c12c13a313f251262f761c5405a0463fd894f8d50fb2a10127b558da54` |
| `plans/261005-0036-nckh-devops-aiops-research-upgrade/phase-02-research-and-statistics.md` | `4b51efc2394c0008aa40592fa423c14637d91c09aa13d66ca43b15ddd849c333` |
| `plans/261005-0036-nckh-devops-aiops-research-upgrade/phase-03-scientific-datasets-and-telemetry.md` | `d4c9d78b7771cec5e6ea3c921f4d98cd3c69139b8bb8585a38c2c78993943527` |
| `plans/261005-0036-nckh-devops-aiops-research-upgrade/acceptance-matrix.md` | `02047fd6e28481b3216a2db67513382155f2e24c691200a51840ed7b0616efb7` |
| `plans/runs/nckh-upgrade-261006-0850-attempt-01/dataset-manifest.json` | `81972050948371345f8ed1b56a62113d0fd21eaa036629bf2d05a2c7d65bd991` |
| `plans/runs/nckh-upgrade-261006-0850-attempt-01/split-manifest.json` | `efa0132c0cfb7979ea7913e9287a2e26a5753ed1c3024ffc0d0056d70819509b` |
| `plans/runs/nckh-upgrade-261006-0850-attempt-01/telemetry-manifest.json` | `ad10b0ab7aa214492dd6ce976f335934c6f84dec772da45ec78f90293ef9a398` |
| `plans/runs/nckh-upgrade-261006-0850-attempt-01/p3-artifact-checks.json` | `ac826a61c4cfe4bab22234568f7690b084d7060ea06e81c65e8f01d3f240d87d` |

## Handoff

Post-snapshot note: controller repairs began after the 09:29 snapshot. A final identity check detected changes to all four reviewed Python owners, the statistical/dataset schemas and the three research test modules. The findings, 47-test outcome and hash table above remain the preserved baseline review; they do not describe the repaired revision. Re-review is pending controller completion signal.

Status: DONE_WITH_CONCERNS

Summary: Independent P2/P3 source/test/artifact review completed; 47 focused tests pass and the current 26-row pilot receipt reproduces. Three P1 and four P2 findings require repair and focused regression checks before the affected public-contract gates can pass.

Concerns/Blockers: raw/intermediate lineage, readout task/unit/run binding, forecast-origin binding, cumulative-versus-rate reset semantics, preallocation record caps, protected-label reference validation and finite derived metrics. No source edits made. Scientific/native/provider acceptance remains pending.

Unresolved questions: none needed for this review; concrete task-specific origin/run/label-store contract details belong to the named owning phases during repair.

## Re-review 1 — repaired snapshot, 09:38 +07:00

Controller completion signal authorized this bounded re-review. Source edits remained controller-owned. Re-read the repaired P2/P3 owners and touched fixture construction; ran only the P2/P3 test modules. Actual result: **53 tests, 1.199s, OK**, exit 0. Controller's separate 67-test AIOps-inclusive result was not independently repeated here.

Original cases now verified:

| Baseline case | Actual repaired behavior |
|---|---|
| Empty raw claims six rows | Rejects `declared raw count differs from actual acquired rows` under explicit canonical layout |
| Readout task differs from dataset/split | Rejects `statistical readout task differs from dataset/split task`; current tests also cover incorrect independent mapping and text run |
| Forecast decision after target | Rejects `forecast origin must precede actual target interval` |
| Protected-label alias | Rejects `protected gold cannot alias feature/data artifacts`; references are now hash-bound |
| Shared reader parses array before record rejection | Rejects before decoding; patched `JSONDecoder.raw_decode` call count is **0** for 10,000 rows under `records=1` |
| Finite paired operands overflow | Rejects `derived paired difference must be a finite number` |
| Falling normalized rate, monotonic cumulative source | Correctly passes; invented reset is rejected using source cumulative values |

Regenerated current P3 receipt exactly reproduces. The World Bank source-layout record is `worldbank-api-v2`, actual raw data-array count is 26, normalized source values and original blank units match, split has 26 members, telemetry remains `not-applicable`. The four original P3 manifest/receipt files were placed by controller in `RUN/p3-before-review/`; original review evidence above remains preserved.

### Remaining P1 — Intermediate transform count is still trusted

Repaired location: `nckh-kit/core/datasets.py:140`–`:147`.

Actual raw cardinality is now checked, but intermediate outputs still receive `available[sha256] = transform.output_rows` without actual row counting. Reproduced with a real six-row raw fixture, two transforms and a hash-bound empty intermediate JSON array: raw → `[]` declared six output rows, then `[]` → original six normalized rows declared six input/output rows. Both transforms satisfy arithmetic; dataset still returns `contract: pass`.

Action: count each bound intermediate output via its typed layout/canonical reader and reconcile aggregate actual output counts before adding it to the available lineage map. This is the intermediate portion of the first baseline finding, not a new scientific acceptance requirement.

### Remaining P2 — Shared preflight is bypassed by two direct JSON parse sites

Repaired locations: `nckh-kit/core/statistics.py:125`–`:127`; `nckh-kit/core/datasets.py:74`–`:80`.

The shared reader's repaired preflight works, but statistical outputs and raw JSONL rows still call `json.loads` directly.

- Valid `StatisticsTests.readout(root)`, plus an extra bound `outputs` artifact `list(range(10000))`, trusted `records=1000`: **pass**, with only **102 records charged**. The complete extra output array was parsed despite exceeding that cap.
- Dataset fixture with six raw JSONL lines, each containing an array of 2,000 zero values; explicit `raw_layout={format: jsonl, rows: 6}`, trusted `records=1000`: **pass**, with only **18 records charged**, after parsing 12,000 nested array members.

Action: route all untrusted research JSON decoding, including outputs and JSONL elements, through the same lexical record/depth preflight. Preserve line counts separately from the graph's allocation budget. These sites also bypass the reader's depth cap.

### Re-review 1 identities

| Path | SHA-256 |
|---|---|
| `nckh-kit/core/research_io.py` | `57c5c2fa5182423fb4406328182b032467f18146eb22ca7ab4b67b62c56df3a8` |
| `nckh-kit/core/statistics.py` | `43d7ce30abe2e3209892aff900036e4fbccb13a6677b5e28408bb7f97c256ef2` |
| `nckh-kit/core/datasets.py` | `2a66cf2003700ecf5b22dbce0a6378a15f4e356178fb547cd1af00b5bc7945b4` |
| `nckh-kit/core/telemetry.py` | `ff04a2ceb4534f8edc9a151c2d929e88929605e50f472b2f8c5a06c694b6eda3` |
| `nckh-kit/core/contracts/statistical-analysis.schema.json` | `65e910c2c42e65939192dbe6ee521b6af83373035797d71e322670e559c57b6e` |
| `nckh-kit/core/contracts/dataset-manifest.schema.json` | `9cbc29b21a10d97a8c968bdf3ffbddc697c6c0a3e912728438857b8928fde5e3` |
| `nckh-kit/tests/research/test_statistics.py` | `40b1a8935472e9218b90139e88ae5cb82fc5f0b33a4b1a423cfc9b0c39cad22b` |
| `nckh-kit/tests/research/test_datasets.py` | `15567f1b3658504878bebdbf64dd5ac4879be62a5dd3995b2979fb32407fb661` |
| `nckh-kit/tests/research/test_telemetry.py` | `ff471a18d9852d018324761e39bcbf37ce68137e39d5a234f9d9865ce109e306` |
| `plans/runs/nckh-upgrade-261006-0850-attempt-01/dataset-manifest.json` | `b2e76f3ca9557e8fc51f989ab24155cdcb8168159d4fff90b26bd86635aa0faa` |
| `plans/runs/nckh-upgrade-261006-0850-attempt-01/split-manifest.json` | `b9607bc6e0d38c40da0e4fbb70788b7c41d505d4d0c8d89383f59d8f8394cdec` |
| `plans/runs/nckh-upgrade-261006-0850-attempt-01/telemetry-manifest.json` | `ad10b0ab7aa214492dd6ce976f335934c6f84dec772da45ec78f90293ef9a398` |
| `plans/runs/nckh-upgrade-261006-0850-attempt-01/p3-artifact-checks.json` | `ac826a61c4cfe4bab22234568f7690b084d7060ea06e81c65e8f01d3f240d87d` |

Status: DONE_WITH_CONCERNS

Summary: The seven original counterexamples now have targeted repairs; five corresponding gates have no remaining reproduced defect in this bounded re-review. Intermediate lineage and JSON allocation-budget coverage remain incomplete; the actual regenerated 26-row P3 receipt reproduces.

Concerns/Blockers: one remaining P1 for intermediate output cardinality, one remaining P2 covering statistical-output and JSONL preflight bypass. Findings were sent to controller with exact cases. Scientific/native/provider acceptance remains pending. No source edits.

## Re-review 2 — final bounded review, 09:41 +07:00

Controller signaled the second correction and froze P2/P3 ownership for this review. The following checks use the final source identities below; no source edits were made by this reviewer.

### Actual checks

Same focused command as the baseline:

```powershell
python -B -m unittest tests.research.test_statistics tests.research.test_datasets tests.research.test_telemetry
```

Actual result: **56 tests in 1.157s, OK**, exit 0. The controller's AIOps-inclusive 70-test run is separate evidence and was not repeated in this bounded P2/P3 review.

The inline independent counterexample run also exited 0, with assertions on rejection/pass outcomes. Results:

| Case | Actual final behavior |
|---|---|
| Empty raw declared as six rows | Rejects actual raw-count mismatch |
| Empty intermediate declared as six rows | Rejects `actual intermediate/output row count differs from transformation lineage` |
| Statistical extra output array of 10,000 members under `records=1000` | Rejects record budget during shared preflight |
| Six JSONL lines × 2,000 nested members under `records=1000` | Rejects record budget during shared preflight |
| Canonical array of 10,000 members under `records=1` | Rejects before row decoder; patched decoder call count is **0** |
| 65 nested containers | Rejects trusted depth limit before JSON decoder; patched decoder call count is **0** |
| JSON numeric exponent `1e999` | Rejects nonfinite JSON number |
| Forecast origin after target interval | Rejects origin/target mismatch |
| Protected-label reference aliases normalized artifact | Rejects artifact alias |
| Protected-label reference absent on disk | Rejects with `FileNotFoundError`; no false contract pass |
| Readout task differs from actual dataset/split | Rejects task mismatch |
| Readout independent mapping differs from dataset | Rejects actual mapping mismatch |
| Structured terminal run omits actual dataset/split hashes | Rejects input binding mismatch |
| Finite operands produce an unrepresentable difference | Rejects derived nonfinite difference |
| Falling normalized rate from monotonic cumulative source | Passes supported normalization case |
| Invented cumulative reset for that source | Rejects reset lineage mismatch |

Source review confirms:

- `core/research_io.py:126`–`:134` owns JSON lexical preflight and finite float decoding; `bound_json()` uses it, canonical rows preflight before `raw_decode`.
- `core/datasets.py:49`–`:83` reads typed actual raw counts; JSONL uses shared `parse()` at line 77. Each transform output is parsed as a canonical row array and its actual cardinality checked at lines 140–141 before lineage registration.
- `core/statistics.py:103`–`:119` validates dataset/split task, parent binding, actual observation/independent mapping and structured terminal run input hashes. Outputs use `bound_json()` at line 123.
- Protected references are now hash-bound and forbidden to alias data artifacts. Forecast decisions precede actual target intervals. Source counter values supply reset evidence; derived paired arithmetic is checked for finiteness.

### Current actual P3 artifacts and preservation

Recomputed the full current `dataset/split/telemetry` result and asserted exact equality with `p3-artifact-checks.json`. The current 26-row World Bank source data array and normalized artifact still preserve each value and original blank unit. The split contains 26 members, and telemetry remains `not-applicable`. This is the local retrospective development snapshot; no current-source or publication-vintage claim was introduced.

The original four files under `RUN/p3-before-review/` were hashed directly. Their hashes exactly match the baseline dataset, split, telemetry and artifact-check entries above. Historical failures and the original artifact identities remain intact.

### Final independent gate recommendation

| Gate from the baseline | Final scoped review state |
|---|---|
| Raw/intermediate actual counts and lineage admission | pass for reviewed canonical/typed layouts and counterexamples |
| Dataset/sample/partition membership; missing versus zero | pass for existing tests and actual 26-row snapshot |
| Protected-reference existence/hash and declared artifact separation | pass for reviewed rejection cases |
| Forecast origin bound to target; approved RCA diagnostic window | pass for reviewed cases |
| Plan/readout separation and readout task/parent/mapping/run-input identity | pass for reviewed cases |
| Source counter versus normalized rate reset semantics | pass for reviewed cases |
| Byte/aggregate/record/depth allocation boundaries | pass for reviewed JSON/JSONL/canonical cases |
| Derived metric finiteness | pass for reviewed overflow cases |
| Scientific inference, actual execution provenance and blind evaluation | pending; P6/domain/owner evidence remains required |
| Native/provider, frozen source-lock/build/package/stable qualification | pending and outside this review |

No remaining reproduced P1/P2 defect in the reviewed P2/P3 repair scope. Recommendation: continue controller integration and later freeze/qualification. This recommendation does not infer estimator correctness, scientific efficacy, protected-store operating-system enforcement, actual provider execution or stable eligibility from these local checks.

### Final source and artifact identities

| Path | SHA-256 |
|---|---|
| `nckh-kit/core/research_io.py` | `43ab446703f010509abdfc721d1e0d6057498de3361248002de3ce40614b91c7` |
| `nckh-kit/core/statistics.py` | `f4cf3cc89bab15e125c5ab86c8baaa55bb396bbd7126369584315d33757b764f` |
| `nckh-kit/core/datasets.py` | `85f8b6fe3d0074bbcfb329c874235127a0bef081fe4cf7a7121a3552ff9b97aa` |
| `nckh-kit/core/telemetry.py` | `ff04a2ceb4534f8edc9a151c2d929e88929605e50f472b2f8c5a06c694b6eda3` |
| `nckh-kit/core/contracts/statistical-analysis.schema.json` | `65e910c2c42e65939192dbe6ee521b6af83373035797d71e322670e559c57b6e` |
| `nckh-kit/core/contracts/dataset-manifest.schema.json` | `9cbc29b21a10d97a8c968bdf3ffbddc697c6c0a3e912728438857b8928fde5e3` |
| `nckh-kit/core/contracts/split-manifest.schema.json` | `a36a2df17ea85252853f1c177592057a53894d7d592a007f49a117d39e908968` |
| `nckh-kit/core/contracts/telemetry-manifest.schema.json` | `6e75e2f15337f8fc5c2b80f1d8f4e8cc1cff9ac4a644da5e858941eea1322dbb` |
| `nckh-kit/tests/research/test_statistics.py` | `a98017bb16be63e9b2f7cb25b251adb9bab08f9cad6e665e5c94cbddc9e45017` |
| `nckh-kit/tests/research/test_datasets.py` | `340d0bb3d85f486288fc4d90f5be483c807cc94e8486d723e92efcadbd35deeb` |
| `nckh-kit/tests/research/test_telemetry.py` | `ff471a18d9852d018324761e39bcbf37ce68137e39d5a234f9d9865ce109e306` |
| `plans/runs/nckh-upgrade-261006-0850-attempt-01/dataset-manifest.json` | `b2e76f3ca9557e8fc51f989ab24155cdcb8168159d4fff90b26bd86635aa0faa` |
| `plans/runs/nckh-upgrade-261006-0850-attempt-01/split-manifest.json` | `b9607bc6e0d38c40da0e4fbb70788b7c41d505d4d0c8d89383f59d8f8394cdec` |
| `plans/runs/nckh-upgrade-261006-0850-attempt-01/telemetry-manifest.json` | `ad10b0ab7aa214492dd6ce976f335934c6f84dec772da45ec78f90293ef9a398` |
| `plans/runs/nckh-upgrade-261006-0850-attempt-01/p3-artifact-checks.json` | `ac826a61c4cfe4bab22234568f7690b084d7060ea06e81c65e8f01d3f240d87d` |

Status: DONE

Summary: Final bounded P2/P3 re-review completed; 56 focused tests and independent counterexamples pass their intended oracles, and regenerated P3 artifacts reproduce. All seven baseline findings and both incomplete repair cases are closed for these exact identities/cases.

Concerns/Blockers: none remaining in this bounded review scope. Scientific/native/provider acceptance and later freeze/package gates remain pending in their owning phases. No source edits; no active test/fixture process or outstanding attempt remains.

Unresolved questions: none for this review scope.
