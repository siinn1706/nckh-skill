# Independent P7 integration review — before candidate freeze

Status: DONE

Summary: The current integration preserves the r38 baseline and meets the inspected pre-freeze exact-set, static supplemental-route, resource-rights, helper-closure and documentation contracts. No concrete blocking finding was identified. Candidate pin verification, build/extraction, installer previews and scoped runtime/human/scientific acceptance remain their separate P7 gates.

Reviewed fingerprint time: 2026-10-06T03:31:08.691413+00:00 (Asia/Saigon: 10:31:08).

## Scope and authorization

Review reference: controller delegation `/root/review_owned_provenance`, P7 integration task received 2026-10-06. Scope: read-only pre-freeze review against `plans/261005-0036-nckh-devops-aiops-research-upgrade/phase-07-integration-and-qualification.md`; this report is the only owned output. Existing project-local `--auto` mechanical scope was recorded by the controller; no `--yagni` was passed. The scope record does not grant provider/cloud/native/global installation/publication authority.

Read the assigned evaluation/build/catalog/schema/matrix/test/documentation owners, plus directly required acceptance/resource/closure helpers and preserved r38 metadata. No source edits, dependency installation, candidate freeze, new build or pinned-source/release check was performed. The only executed unit suite was the explicitly lock-independent `tests.release.test_research_matrix`.

Independent task context was used. Requested/resolved/configured/applied model setting: inherited session; effective native model/effort and cost/window telemetry: unknown. Human expertise and model independence are not established by the reviewer role. No nested delegation or external calls occurred.

## Findings

No concrete blocking defect was found in the inspected pre-freeze scope. The evidence and its limits are recorded below; this is not a post-freeze candidate acceptance or semantic routing result.

## Exact catalog and base cases

Preserved baseline artifact:

```text
plans/runs/nckh-upgrade-native-261006-0850-attempt-01/bundle/codex
embedded source revision: 38
```

Compared its 39 skill identities and embedded source pins with current source:

| Check | Observed result |
| --- | --- |
| Current approved identities | Exactly 43; `validate_catalog` passes. |
| Removed r38 identities | None. |
| Added identities | Exactly `nckh-dataset`, `nckh-statistics`, `nckh-telemetry`, `nckh-aiops`. |
| Kit membership | Core 16, Engineer 13, Marketing 13, Tooling 1. |
| Current base case IDs | Exactly 172: positive/negative/outcome/failure for each current identity. |
| Preserved baseline IDs | All 156. |
| Added base IDs | Exactly 16, belonging to the four added owners. |
| Baseline case file drift | None: all 39 baseline manifest byte hashes match the embedded r38 pins. |
| Personal-use profile | Validates and covers exactly 43 identities. |

Each current skill manifest was passed through `validate_case_manifest`; exact global ID membership was compared independently. The top-level `validate_cases` function was read rather than executed because its final `verify_source_lock` call intentionally depends on a current candidate freeze.

The loader separately loads the exact `research-data-aiops/domain-scenarios.json` path, skips that path in the base-manifest loop and rejects a duplicate/misplaced record with its supplemental kind. Its base-case assertion remains the exact 172-ID set. Supplemental scenario IDs never enter the base-case aggregation.

## Supplemental routes and preserved qualification

Direct `validate_research_matrix` result:

```json
{"scenarios": 12, "evidence_class": "static", "observed_behavior": "unverified"}
```

All twelve records use `status=not-run` and `receipt_reference=null`. The schema and owner validator reject attempted receipt/result claims; expected owner tuples are fixed by the approved route map. Near misses cover dataset/database, scientific statistics/KPI/marketing A/B and telemetry/RCA/debug. Their declared route is rejection/handoff/no execution. Same-owner scenarios declare their bounded own-scope route and retain the task-grant requirement.

Executed from `nckh-kit`:

```text
python -B -m unittest tests.release.test_research_matrix
Ran 3 tests in 0.005s
OK
```

This suite checks static declarations and adverse matrix mutations. It invokes no semantic routing engine, native model or provider and records no observed agent behavior.

All four of these current files remain byte-identical to their preserved r38 pins:

- `evals/cases/required-families.json`: 19 required family records; owner validation passes.
- `evals/protocols/qualification.json`: historical protocol unchanged.
- `evals/cases/runtime/invocation-matrix.json`: historical 224-cell matrix unchanged.
- `evals/cases/runtime/writer-invocation-matrix.json`: 256 native and 20 supplemental planned writer cells; owner validation returns static/unverified.

The revised qualification tests expect 43/172 and retain pending qualification, unknown cost, undefined cost per accepted task, five rubrics and the historical OS/installer boundaries. They were inspected but not run before freeze. Documentation explicitly distinguishes the current 172 base cases, historical 148 evidence, supplemental twelve research declarations and twenty writer declarations.

## Resource rights and closure

Current `core.resources.registry` validates 13 resource groups and 35 declared consumer bindings:

| Source kind | Groups |
| --- | ---: |
| copied-upstream | 4 |
| retrieved-snapshot | 5 |
| owned-reference | 4 |

Compared the nine r38 resource rows from its actual packaged registry with current rows: all nine remain structurally identical, including source rights/provenance and consumers. The additive four authored groups retain original contribution provenance and local-package-only rights. The authored record/hash/binding corrections are also documented in `review-261006-owned-resource-provenance.md`; none is converted into copied-upstream/public-MIT permission.

Computed the actual ON closure inputs for all 43 current skills, using the current `closure` and `resource_edges` owners. For each closure, inspected local `core.*` Python imports and literal `validate_record` schema dependencies against its member set. Observed:

```text
43 closures checked
missing local imports: none
missing literal schema dependencies: none
evaluation/private members: none
closure size range: 8–50 files
```

The four scientific skill closures include the standalone resource reader and its catalog/schema/owned-provenance/IO helpers. Method, cook and devops closures include the research graph checker and all sixteen entries in its declared helper/schema dependency list. Concrete selected closure sizes:

| Owner | Members | Checker/reader scripts |
| --- | ---: | --- |
| nckh-dataset | 24 | search-resource.py |
| nckh-statistics | 24 | search-resource.py |
| nckh-telemetry | 23 | search-resource.py |
| nckh-aiops | 26 | search-resource.py |
| nckh-method | 50 | check-research-artifacts.py, search-resource.py |
| nckh-cook | 30 | check-research-artifacts.py |
| nckh-devops | 27 | check-research-artifacts.py |

The current authored verifier root is `skills/<consumer>/references/_shared`, matching the materializer projection. Declared helper completeness, source link containment and that mapping are pre-freeze static evidence. They do not replace the planned actual archive/extract/isolated-reader checks from a fresh candidate.

## Documentation and private-data boundary

Read all six assigned owning documents. Every local Markdown link in `docs/{index,qualification,migration,research-and-writing,engineer,contracts}.md` passed the owning `reference_path` containment/existence check. All 43 computed skill closures also traversed their local Markdown references successfully.

The documents keep:

- scientific dataset/statistics/telemetry/AIOps owners distinct from database and marketing owners;
- method design, cook lifecycle and devops environment responsibility distinct;
- authored summaries/metadata separate from pilot measurements and run/readout evidence;
- local deterministic/static evidence separate from native, owner, scientific and publication acceptance;
- task-grant boundaries for providers, faults, processes and infrastructure explicit.

The current source inventory contains 337 members. It contains no `evals/results/` or `/private/` paths. The known pilot-data and snapshot directories remain outside that source inventory and all inspected skill closures.

As a bounded duplicate-byte check, hashed the eight known pilot-data files, four second-attempt snapshots and six third-attempt snapshots, then compared them with current inventoried source bytes. No raw/pilot data file matched source; the sole match was the already-existing public World Bank rights notice (`pilot-data/rights.md` equals `core/profiles/resources/worldbank-rights.md`). This notice is an intentionally retained legacy rights artifact, not pilot observations or labels. The initial failed snapshot directory contains no files. These are identity/closure checks, not a general semantic privacy classifier.

All 46 explicitly protected source files and all 37 protected historical lock files match their pre-work recorded hashes. No historical baseline/source-protection drift was observed.

## Archived public verifier disposition

Located and read:

```text
github-publication/nckh-kit/scripts/verify-public-package.py
SHA-256: 4a285d9cfe301b5f6b3a1bbb0258ed1ed437059031d357c99e453f39258a02fa
```

Its contract intentionally targets 39 public identities, nine public resource groups, resource ON, r38 and packaged-inactive/advisory hooks. It imports its own archived `core.build` owner. That archived script is not the new 43/13 candidate verifier.

Read-only Git checks establish that the verifier's worktree bytes equal its tracked `HEAD` bytes, and `git status --short` for the entire archive is empty. No archive edit or public action occurred. Disposition: preserve it as the existing r38 public edition's verifier; new candidate validation uses the current owning `nckh-kit` contracts. Future public promotion would require its separately authorized public owner/workflow and release-rights review. This project-local integration review does not expand that scope.

## Gate matrix

| Gate | State for this review |
| --- | --- |
| 43 identities / 172 base IDs and preserved r38 baseline | Pass. |
| Twelve separately loaded static research scenarios | Pass; observed semantic behavior unverified. |
| Legacy qualification/family/runtime/writer preservation | Pass for verified bytes/owner validators. |
| 13 resource groups and distinct rights variants | Pass. |
| Current static helper/schema/Markdown closure | Pass for all 43 skill closures. |
| Known pilot/raw snapshot packaging exclusion | Pass for inspected inventory, closures and exact-byte comparison. |
| Archived public edition preservation | Pass; retained r38 contract, no edits. |
| Live source-lock freshness | Intentionally stale r38; sole candidate freeze pending. |
| Current pinned tests/full validation/reproducibility/build/extraction | Pending P7; not run by this review. |
| Installer preservation/previews and new relocated package checks | Pending P7. |
| Semantic agent/native/human/scientific/public acceptance | Not evaluated; no implied pass. |

Recommendation: no pre-freeze repair is required from this review. The sole controller can proceed with the already-authorized candidate freeze after confirming source owners are quiescent, followed by the planned pinned and actual package checks. Preserve revision-specific failures and rerun affected descendants if those checks require repairs.

## Reviewed fingerprints

Relative to `nckh-kit/`:

```text
core/evaluation.py
  32fabca688c8030edbaec84869418c063dfb0e2913ab6a1213773f0b97dbae6e
core/build.py
  bd8046619803d14060d8e9f87bc95c0d5dad408c4dfbc4203e8d468b4754a168
core/registry/catalog/skills.json
  f1fac41f51eb4d52d0aa720c6ce6e7d325dd76ae0fae88b7fe275ad06760ed3d
core/registry/catalog/resources.json
  f84eed69a8ffcf1789c66e55b6a388081fdce9275e2b1034e82df77e92a5eac2
core/contracts/research-domain-scenarios.schema.json
  d1b84b3b9e90d123ed432c7fed5014fbb668c5615262197d324e848b251e9cba
evals/cases/research-data-aiops/domain-scenarios.json
  7c85bf6da5a4caee4cf9d6c0398c98cd478985885ef85a86346230b197c661ec
tests/release/test_research_matrix.py
  dfcccc6458fdcdaffdc4ab2fe572900b16752c4014163c87efcae58e6b122de1
tests/release/test_qualification.py
  0931e6112f297aa2773765d02ef79131de60ce999e41f4d3096e68d9211c616b
tests/acceptance/test_profile.py
  9c9d31540adbda484004b1eb741c3c3bbaf3103ff81ebb0b0c22fff45bce5bc3
docs/index.md
  2d50a90ddd3f99dc5fc21dae83ae2c59493c998e20fc712af9a1babdc708b988
docs/qualification.md
  6425beedfdc78709184432c21567d8272e4d832bfe47ba049fc7582757afeab9
docs/migration.md
  d40c9847d354bdddfdb9363ea1fddb7fc8fa6f5f972fbcb5872ef294c8795def
docs/research-and-writing.md
  ca608d8844aed15d7e62049cf8c8d94299be11c9b4518ffcc7e19f26c8347ac0
docs/engineer.md
  02873869525e25a8a4508d9e1bb05a62013a54abea1daf79bb93c6d65c0c5a95
docs/contracts.md
  d1615d5d0aaa59a5b59b71b5ade0547d9cab9ac01ad8364324ec00a42fd73b87
core/registry/source-lock/source-lock.json (intentionally stale r38)
  5616070c7027b0e9f25ae897dc60e51c0830a6c0ae62779708936e62c2b9ce47
```

Concerns/Blockers: none within the pre-freeze review scope. The pending P7 execution/acceptance gates above retain their actual pending state. Unresolved questions: none.

## Focused r39 failure repair review — 2026-10-06 10:45 Asia/Saigon

Status: DONE

Summary: The four observed r39 pinned-test failures have cause-aligned repairs in the inspected source. No concrete blocking defect remains in this bounded repair review. Corrective freeze and affected pinned/package reruns are still pending; the original r39 failed gate remains failed.

### Scope and authorization amendment

Live review reference: controller delegation `/root/review_owned_provenance`, focused r39 repair review received 2026-10-06, reaffirmed by the controller's finalization message in this turn. Scope revision: review only the four preserved failures and their repairs before corrective freeze; append only to this report. The previous pre-freeze sections and historical receipts remain preserved. No source edits, pinned checks, new builds, freeze, provider/native/global installation or publication were performed by this repair review. No nested agents were used.

Read the two actual CLI owners, three corrected test owners, original and corrective controller receipts, and the counsel report. The existing extracted-smoke test was inspected to establish that post-read package verification remains in place. AST/order checks, current exact counts and file fingerprints were read-only reviewer checks. The controller's eight-test corrective run was inspected, not independently rerun. Requested/resolved/configured/applied settings remain inherited session; effective native model/effort, cost and usable-window telemetry remain unknown.

### Preserved failure and repair evidence

Original controller receipt: p7-pinned-tests-attempt-01.txt (historical evidence path: `../runs/nckh-upgrade-261006-0850-attempt-01/p7-pinned-tests-attempt-01.txt`; unavailable in the cleaned checkout). It records 78 tests in 225.417 seconds, ending with two failures and two errors. Its failed result is not superseded by this source review.

| Actual r39 failure | Inspected repair | Retained acceptance boundary |
| --- | --- | --- |
| Profile source count expected 35; actual 36. | Exact equality assertion now expects the actual 36 sources. | The exact source-count assertion remains; no range/inequality substitute. |
| Writer resource count expected nine; actual thirteen. | Exact equality assertion now expects the actual thirteen groups. | The exact resource-count assertion remains. |
| Rights-drift fixture lacked `core/registry/catalog/skills.json`, raising `FileNotFoundError` before testing license drift. | Fixture now copies the actual skill catalog beside actual registry/resource inputs. | The license-hash mutation and rejection assertion remain and now exercise the intended dependency-complete fixture. |
| Isolated `python -I` reader imports created unowned `__pycache__` files in an extracted package; subsequent `verify_bundle(extracted)` rejected the extra files. | Both standalone CLIs set `sys.dont_write_bytecode = True` before any local `core.*` imports. | Package verification still rejects extra files; no cleanup, ignored-bytecode exception or verifier weakening was introduced. |

Bytecode assignment order was verified from the actual source AST: resource reader assignment at line 15 precedes local imports at lines 17–19; research checker assignment at line seven precedes local imports at lines 9–12. The change controls imported helper bytecode from within each CLI, including the isolated invocation that ignores caller environment flags.

The added `ExperimentTests.test_isolated_readers_preserve_complete_helper_tree` uses separate temporary package/project/CWD directories, copies both actual scripts and their complete declared `SCRIPT_REQUIREMENTS`, snapshots file names and SHA-256 hashes, then invokes both CLIs with `python -I` without caller `-B`. It requires successful exits, an identical package tree after each invocation, and an empty CWD. The reader exercises OFF mode. The checker validates a synthetic manifest and writes only its explicitly requested `project/check.json`; the test confirms that receipt exists in the separate project directory. This is a deterministic filesystem/invocation regression test, not scientific or native-agent acceptance.

The actual extracted-smoke test continues verifying the package before smoke and again after actual resource reads. Its source and `core/build.py` still match their r39 pins. Therefore the focused fixture protects isolated CLI no-write behavior, and the unchanged actual extracted-smoke gate retains the remaining ON/package verification responsibility.

Corrective controller receipt: p7-corrective-tests-attempt-01.txt (historical evidence path: `../runs/nckh-upgrade-261006-0850-attempt-01/p7-corrective-tests-attempt-01.txt`; unavailable in the cleaned checkout), inspected directly: eight tests in 0.739 seconds, `OK`. The counsel report is [counsel-261006-pinned-regression-failure.md](counsel-261006-pinned-regression-failure.md). No claim of an independent corrective execution is made here.

### Current fingerprints and gate disposition

Refreshed at 2026-10-06T03:45:04.447574+00:00 / Asia/Saigon 10:45:04; all match the earlier focused-review snapshot at 03:43:25.960760+00:00. Relative paths below are rooted at `nckh-kit/`:

```text
scripts/search-resource.py
  8f7ba3cc69dc93b92aa32e8f7fb5a14e6dcf9bd7728abea2f1b2706b6a9a43c2
scripts/check-research-artifacts.py
  c99ac88a8d4ffd0c84c569b8c42e1cf0f98d526dd0216ccbacfa867cc99aff75
tests/acceptance/test_profile.py
  5bd44239efbf0d7363ec27bdfb55af8ad1fc29c853512bc6fccc3dde32eeb858
tests/resource/test_writer_consumers.py
  43b8b75dc36a27856f67443dd152867644809d5bfbbb289dda3f9fc5840ae6b3
tests/research/test_experiments.py
  d20de0de807eeeeb5f43101e2eb57c79b8d64effde7aafc5d246d5d0d2757f6e
core/build.py (matches r39 pin)
  bd8046619803d14060d8e9f87bc95c0d5dad408c4dfbc4203e8d468b4754a168
tests/resource/test_extracted_smoke.py (matches r39 pin)
  0f6ce41fb3949d6173a8c121238e3b8098ad83b6ec2101693c2f035451eef755
core/profiles/acceptance/personal-use.json (matches r39 pin)
  f791962e41e21d913c3131cb45e3c6ed1747824b91e2a0355bd5797f66171793
core/registry/catalog/resources.json (matches r39 pin)
  f84eed69a8ffcf1789c66e55b6a388081fdce9275e2b1034e82df77e92a5eac2
core/registry/source-lock/source-lock.json (revision 39)
  89fd3077a1069a345d71168cf97410aa3c30a45dcf9373be9d43ba1787a20996
```

Receipt hashes, relative to the workspace:

```text
plans/runs/nckh-upgrade-261006-0850-attempt-01/p7-pinned-tests-attempt-01.txt
  2d6fa00875903bee325bb1a68d1b8f0963168d2fad01ed1760bb851e5803c174
plans/runs/nckh-upgrade-261006-0850-attempt-01/p7-corrective-tests-attempt-01.txt
  1b81be039f7a988c4c3ea2563ff1b590c02f526eb762fb86361794954e71d417
plans/reports/counsel-261006-pinned-regression-failure.md
  5f0b8ed6e9987c9f1a4fe2b2d0d4dbeacbaa33fb7c2e907a00d99ebfec2827be
```

The live lock remains r39. The five repaired source/test files intentionally differ from its pins; these repairs have not yet received the corrective freeze. This source verdict permits the sole controller to proceed with the authorized corrective freeze, then run the affected pinned and actual package checks. Their descendants remain pending until actual receipts exist. Semantic/native/human/scientific/public acceptance remains outside this review.

Concerns/Blockers: none within the focused repair review. Corrective freeze, affected pinned reruns and actual package/extraction checks are pending execution gates, not accepted results. Unresolved questions: none.

### Controller status amendment after corrective freeze - 2026-10-06 10:46 Asia/Saigon

The controller subsequently reported corrective freeze r40/337 with source owners quiescent, a passing static validate-only run, and full deterministic supervisor session `82427` active. The controller also reported eight focused and 114 domain tests passing. This amendment records those as controller-reported execution status; the reviewer did not independently run those suites or inspect the 114-test receipt.

Read-only fingerprint refresh at 2026-10-06T03:46:37.717028+00:00 confirms all five repaired source/test files retain the exact hashes recorded above. The live lock now records revision 40 and 337 file entries; SHA-256 `5642b6fe59af263c7817b89639cb959a842b5fdf908b397799003e3d42c58ded`. The focused source verdict therefore remains bound to the same repaired bytes after the controller's freeze. No source-lock verification or build was performed by this reviewer.

Current disposition: corrective freeze is complete per the controller and the observed r40 lock. The preceding pending-freeze statement records the earlier state. Failed r39 remains a preserved failed historical attempt; r40 is the corrective candidate, whose affected full deterministic and actual package/extraction results remain pending at this review's close. Status: DONE for the focused repair review; no concrete review blocker.

## Focused Core-count repair review before r41 - 2026-10-06 11:11 Asia/Saigon

Status: DONE

Scope/authorization revision: controller delegation `/root/review_owned_provenance`, bounded pre-r41 review received 2026-10-06. Project-local `--auto` was supplied; no `--yagni`. Read only the assigned test lines 132-144, actual skill catalog, preserved focused diagnostic and counsel's latest checkpoint addendum. This report is the only owned writable output. No source edit, test, build, freeze or nested delegation occurred; other owners' edits and every previous report byte are preserved. Model settings remain inherited; effective native model/effort and cost/window telemetry remain unknown.

The actual catalog contains 43 skills and exactly these 16 unique Core identities:

```text
nckh-plan, nckh-cook, nckh-review, nckh-handoff, nckh-research,
nckh-evidence, nckh-method, nckh-write, nckh-taste, nckh-visuals,
nckh-humanwrite, nckh-paperwrite, nckh-dataset, nckh-statistics,
nckh-telemetry, nckh-aiops
```

The preserved focused diagnostic (historical evidence path: `../runs/nckh-upgrade-261006-0850-attempt-01/p7-core-count-diagnostic-attempt-01.txt`; unavailable in the cleaned checkout) ran one test in 52.021 seconds and failed at line 142 with `AssertionError: 16 != 12`. The inspected current line 142 uses exact equality with 16. The replacement matches every Core identity in the actual catalog and the observed surviving index count; it is a cause-aligned correction of the stale expectation.

The shared-consumer contract remains intact in the inspected method: lines 135-136 require an unqualified second installation to raise `ContractError`; lines 137-138 explicitly qualify both `codex-cli` and `agy-cli`; lines 140-141 uninstall the first installation and verify the surviving `nckh-plan/SKILL.md`; line 143 uninstalls the second; line 144 still requires the index to equal `{}` exactly. The count assertion was not relaxed to an inequality or subset check.

The [counsel checkpoint addendum](counsel-261006-deterministic-timeout.md) agrees with the directly inspected cause and bounded repair. Its full-suite execution recommendation remains controller-owned. This review has not rerun the corrected test and does not establish deterministic or installer acceptance.

Fingerprints captured at 2026-10-06T04:11:35.158590+00:00 / Asia/Saigon 11:11:35, relative to the workspace:

```text
nckh-kit/tests/installer/test_transactions.py
  9a3aceb658074797814f1e2e56c1fded86b050dc27c46af795efdd4598d26d02
nckh-kit/core/registry/catalog/skills.json
  f1fac41f51eb4d52d0aa720c6ce6e7d325dd76ae0fae88b7fe275ad06760ed3d
plans/runs/nckh-upgrade-261006-0850-attempt-01/p7-core-count-diagnostic-attempt-01.txt
  0f9e6eb1b9f50fdc58006dc9771aab8f12feedfec7e3ce0fa56c4c7984abd221
plans/reports/counsel-261006-deterministic-timeout.md
  d22acbbc3fd07faae8f202d3251fdcab881643f9216332d74e440a17ff6ba824
```

Verdict: no concrete blocking finding in this single repair. The already-authorized corrective r41 freeze can proceed under the sole controller. Preserve the focused failure and earlier timeout attempt; actual complete-suite and package results retain their pending state until their execution receipts exist.

Concerns/Blockers: none within this bounded source review. Corrective freeze and affected execution gates remain pending at review close.
