---
phase: 7
title: "Exact integration, compatibility và scoped qualification"
status: completed
priority: P1
effort: 2-3 ngày công
dependencies: [phase-01-start, phase-02-research-and-statistics, phase-03-scientific-datasets-and-telemetry, phase-04-devops-and-aiops-methods, phase-05-curated-research-resources, phase-06-reproducible-experiment-workflows]
---

# P7 — Exact integration, compatibility và scoped qualification

## Outcome

Một integration owner merge các specialty outputs và shared contracts, freeze revision thật, verify packaging/legacy/reader/previews và deliver experimental candidate. [Matrix](./acceptance-matrix.md) giữ static/deterministic/agent/native/owner/scientific lanes riêng. Planning validation không certify implementation hoặc readiness to cook.

`WORK = C:/Users/USER/Downloads/test-skill`; `KIT = C:/Users/USER/Downloads/test-skill/nckh-kit`; `RUN` kế thừa P1 absolute attempt root. New build outputs phải empty owned directories under `RUN`, không reuse stale `dist` làm proof. `OUTSIDE` là attempt-owned directory trong permitted host temp, chọn và record exact resolved absolute path/ownership lúc cook; root này phải ngoài `WORK`. Archive/extract ở `OUTSIDE`; `OUTSIDE/cwd` là sibling riêng, ngoài mọi extracted bundle. Check source `resource-smoke.py` rejects CWD anywhere under repository root `WORK`, nên `RUN/outside-cwd` không hợp lệ. Receipts/hashes/temp mapping giữ trong `RUN`; cleanup chỉ exact unchanged owned temp paths, không broad delete.

## Exclusive integration ownership và exact paths

| Owner/action | Absolute named surfaces |
|---|---|
| Controller modify exact catalog/schema/profile | `KIT/core/registry/catalog/skills.json`, `KIT/core/contracts/catalog.schema.json`, `KIT/core/profiles/acceptance/personal-use.json`, `KIT/core/acceptance.py` |
| Controller modify validation/build/source-kind dispatch | `KIT/core/build.py`, `KIT/core/evaluation.py`, `KIT/core/resources.py`, `KIT/scripts/search-resource.py`, `KIT/scripts/resource-smoke.py`; read `KIT/core/schema.py` dynamic lookup, modify only demonstrated owning requirement |
| Controller modify resource/schema closure | `KIT/core/registry/catalog/resources.json`, `KIT/core/contracts/resource-registry.schema.json`, `KIT/core/contracts/owned-resource-provenance.schema.json`; integrate new P2–P6 schemas and package closure |
| Controller reconcile four base case files integrated P5 | `KIT/evals/cases/research-data-aiops/nckh-{dataset,statistics,telemetry,aiops}.json` (four exact files) |
| Controller create supplemental matrix/test | `KIT/evals/cases/research-data-aiops/domain-scenarios.json`, `KIT/tests/release/test_research_matrix.py`; distinguish it from four-case skill manifests in loader |
| Controller modify focused compatibility tests | `KIT/tests/acceptance/test_profile.py`, `KIT/tests/release/test_qualification.py`, `KIT/tests/build/test_closure.py`, `KIT/tests/resource/test_closure.py`, `KIT/tests/resource/test_extracted_smoke.py` |
| Controller review existing shared consumers | `KIT/core/contracts/{skill-cases,required-families}.schema.json`, `KIT/evals/cases/required-families.json`, `KIT/core/registry/compatibility/matrix.json`, `KIT/evals/run-evals.py`, `KIT/installer/nckh-installer.py`; modify only demonstrated current consumer requirement |
| Controller update owning docs | `KIT/docs/{index,research-and-writing,engineer,contracts,qualification,migration,personal-use,installation,runtime-support,release-checklist}.md`, `WORK/docs/README.md` navigation only if needed |
| Controller sole freeze | `KIT/core/registry/source-lock/source-lock.json` and history through `KIT/scripts/freeze-source-lock.py`; preserve historical locks/receipts |

All braced paths are explicit finite sets under declared absolute root, not wildcard edit authority. P7 requires completed P5 serial exact catalog/profile/four-case and source-kind prerequisites admitting new resource consumers; P7 reconciles their final bytes and adds supplemental matrix/closure/qualification. Inventory any additional exact-set/source-kind/rights consumer before freeze with narrowed search; record file/line in `RUN/migration-inventory.json`. Domain owners hand off then stop editing overlapping files.

## Integration rules

Expected approved identities = P1 baseline + four; target 43/172 only if baseline 39/156. Update exact membership/count assertions and error wording together; no arbitrary catalog acceptance. Current baseline cases remain; new sixteen IDs only; supplemental scenarios do not inflate base count. Preserve 19 required family IDs and historical protocol. Update mappings for relevant new owners when applicable without erasing historical family evidence; domain supplemental matrix owns extra scenarios.

Record schemas closed/versioned; unknown fields/variants fail. Existing `validate_record(kind)` resolves contract paths dynamically; không thêm registration table. New record schemas use only supported keywords, owning validators enforce exact membership/variant requirements. Owned provenance mapping must pass all source-lock/manifest/reader paths, including external public-package verifier if one is discovered; no new public publish step.

## Implementation steps

1. Reconcile P1 final baseline against current lock/agent handoff; review P2–P6 artifacts/tests and protected hashes. Resolve any rights/source-kind/ownership finding before packaging.
2. Reconcile exact P5 identity/profile/four-case prerequisites, complete supplemental matrix loader/validator and route docs. Preserve marketing semantics/writer/visual/hooks contracts and historical 148/224/writer256 evidence. Near-miss dataset-versus-DB/statistics-versus-KPI/telemetry-versus-RCA tests required.
3. Complete additive provenance/schema/readers and artifact helper closures; ensure new reader/checker scripts relocate with stdlib imports and schemas. Package no actual pilot data/private labels/provider traces.
4. Run narrow domain/schema tests proven independent of source-lock validation/build; inspect cross-module source-kind/rights, containment, label/holdout leakage, metric/failure denominators and exact-set integrity with independent reviewer. Defer `validate_cases→verify_source_lock`, release/closure/build regressions until candidate freeze; do not misreport stale-pin failures as behavioral regressions or weaken validators.
5. Sole owner freeze reviewed candidate once all source owners are quiescent. Then run pinned release/resource/build/closure regressions, full validate/deterministic and two-build reproducibility. If post-freeze repair changes bytes, keep failed attempt/receipts, owner repair, freeze corrective revision and rerun affected descendants; no test verdict transplant.
6. Build persistent four-host standalone/plugin resource-ON bundles; create recorded `OUTSIDE` temp root outside `WORK`, archive/extract there and verify exact manifests/relocated readers from separate `OUTSIDE/cwd`. Reject containment under repository or any extracted bundle before smoke. OFF exists only internal same-base experiment and must actually return disabled/no-read. Reuse extracted smoke enumerating exact bindings; counts derived from resulting manifests, không hardcode number of files/pins/reads.
7. Installer preview eight existing surfaces with explicit `--package`, disposable projects and source/target pre/post hashes. Preview no activation/install/trust/native invocation. Legacy format1/2 bundles verify unchanged; changed user files/conflicts preserved.
8. Review P6 real pilot actual artifacts và optional agent/native/human receipts only when granted/performed. Produce experimental delivery record with artifact/revision/input hashes, actual failures/unknown cost/pending gates, cleanup and rollback route. Owner feedback after use remains separate from scientific/stable qualification.

## Todo

- [x] Reconcile P5 exact catalog/profile/IDs; complete matrix/routing and preserve legacy roles/history.
- [x] Complete owned provenance and all schema/reader/manifest/helper closures.
- [x] Review migration/privacy/metric failures; pass independent domain/schema checks.
- [x] Freeze candidate after source owners stop edits; run pinned regressions/full deterministic/reproducibility.
- [x] Build/archive/extract ON and internal OFF; verify relocated exact bindings/legacy bundles.
- [x] Run explicit-package installer previews và preservation/cleanup checks.
- [x] Deliver pilot evidence + experimental candidate with actual scoped acceptance/pending gates.

## Verification commands — existing syntax, future execution

From `KIT`; `<RUN/...>` and `<OUTSIDE/...>` substitute recorded actual absolute attempt/temp paths and must exist/be owned as appropriate. Assert resolved `OUTSIDE` and smoke CWD outside `WORK`, with CWD outside extracted bundle, before invocation:

```text
python -B -m unittest tests.research.test_statistics tests.research.test_datasets tests.research.test_telemetry tests.research.test_aiops tests.research.test_experiments tests.resource.test_research_packs.ResearchPackContractTests
python -B scripts/freeze-source-lock.py --write
python -B -m unittest tests.resource.test_research_packs tests.release.test_research_matrix tests.acceptance.test_profile tests.release.test_qualification tests.engineer.test_authority tests.marketing.test_metrics tests.resource.test_consumers tests.resource.test_real_sources tests.resource.test_writer_consumers tests.build.test_closure tests.resource.test_closure tests.resource.test_extracted_smoke
python -B evals/run-evals.py --validate-only --output <RUN/cases-validation.json>
python -B evals/run-evals.py --run-deterministic --output <RUN/deterministic.json>
python -B scripts/build-artifacts.py --all --check --plugin --resource-access on
python -B scripts/build-artifacts.py --all --plugin --resource-access on --output <RUN/bundles/on>
python -B scripts/build-artifacts.py --all --plugin --resource-access off --output <RUN/bundles/off-internal>
python -I scripts/resource-smoke.py --bundle <OUTSIDE/extracted/on/codex> --cwd <OUTSIDE/cwd> --unset-pythonpath --output <RUN/resource-smoke-codex.json>
python -B installer/nckh-installer.py install --package <OUTSIDE/extracted/on/codex> --runtime codex-cli --scope project --project <OUTSIDE/disposable/codex-cli> --kits core engineer marketing --mode copy --models balanced --dry-run
```

First line names **proposed independent domain/schema tests**, not current successful commands; all pinned regression commands follow freeze. Example preview uses existing `balanced` model profile: record that frozen choice or substitute actual verified profile explicitly; dry-run không prompt, nên `--kits`, `--mode`, `--models` đều phải supplied. Re-run ON check for OFF internal via existing `--resource-access off`; loop smoke/previews over four hosts/eight surfaces using live help and resolved projected directory, not fake native receipts. Plugin manifests/closures verified with existing `core.build.verify_bundle` via owning tests. Archive/extract mechanical tooling records actual source/temp/output paths, ownership and hashes in `RUN`; retain receipts before exact owned temp cleanup. `--check` output is not persistent install package.

## Success, risk và rollback

Success = exact target/catalog/cases/rights/readers; actual full deterministic evidence with all failures/skips reported; deterministic fresh packages, no private bytes; ON reads/OFF no-read; legacy and user-byte preservation; real pilot evidence. Không required pending/fail/stale gate thành accepted. No stable/public/scientific/native promotion từ counts/hashes/build/previews.

Rollback restore only unchanged owned upgraded closures/registry/schema/catalog to frozen baseline with preview/preimage checks; retain history/failures/private project inputs. Windows locks: inspect holder/evidence and user-owned clean exit, no process kill/ACL force. Installed r25 stays separate until future explicit installation grant; provider/cloud/native/public actions remain task-scoped, không từ word auto.

## Integration checkpoints

[Pre-freeze and corrective source reviews](../reports/review-261006-research-integration-p7.md) verify exact preserved baseline sets, twelve separate supplemental routes, rights/privacy and helper closures. [Migration inventory](../runs/nckh-upgrade-261006-0850-attempt-01/migration-inventory.json), [protected-byte check](../runs/nckh-upgrade-261006-0850-attempt-01/p7-protected-check-01.json) and 114 lock-independent tests (historical evidence path: `../runs/nckh-upgrade-261006-0850-attempt-01/p7-domain-tests-attempt-01.txt`; unavailable in the cleaned checkout) record actual evidence. The first r39 pinned78 run failed on two stale counts, a missing fixture catalog and isolated bytecode writes; preserved failure (historical evidence path: `../runs/nckh-upgrade-261006-0850-attempt-01/p7-pinned-tests-attempt-01.txt`; unavailable in the cleaned checkout), [counsel](../reports/counsel-261006-pinned-regression-failure.md), eight focused repairs (historical evidence path: `../runs/nckh-upgrade-261006-0850-attempt-01/p7-corrective-tests-attempt-01.txt`; unavailable in the cleaned checkout) and [corrective r40 freeze](../runs/nckh-upgrade-261006-0850-attempt-01/p7-approved-freeze.json) retain the chronology. The r40 full/package checks remain active; first-freeze verdicts are not transplanted.

### Corrective r41 checkpoint

The r40 public deterministic entrypoint exceeded its built-in900-second limit: [actual timeout-unknown](../runs/nckh-upgrade-261006-0850-attempt-01/p7-deterministic.json), with no complete suite verdict. Verbose focused diagnostic (historical evidence path: `../runs/nckh-upgrade-261006-0850-attempt-01/p7-core-count-diagnostic-attempt-01.txt`; unavailable in the cleaned checkout) confirmed Core ownership16≠12; [counsel](../reports/counsel-261006-deterministic-timeout.md) and independent source review approved the exact expected-count repair to16 while preserving qualification, user-byte preservation and final empty-index checks. [r41 freeze](../runs/nckh-upgrade-261006-0850-attempt-01/p7-approved-freeze-attempt-03.json) records337 pins and canonical hash `114e57918889a52474b514c09443a2afd1999e2dd11990a099d5b8069a9267d5`. Fresh validate-only exited0. Full311-case verbose discovery is active through the task-local observable wrapper, with no exclusions or arbitrary900-second cutoff; public runner and timeout history remain unchanged. Package descendants remain pending until actual receipts exist.

Both exact owned staging roots retained from the timeout were checked for containment/reparse paths, snapshotted320 actual files, then removed; [pre-cleanup receipt](../runs/nckh-upgrade-261006-0850-attempt-01/p7-timeout-temp-before-cleanup.json) and [cleanup receipt](../runs/nckh-upgrade-261006-0850-attempt-01/p7-timeout-temp-cleanup.json) preserve evidence. Process observation before cleanup found no live Python process.

[Full r41 deterministic receipt](../runs/nckh-upgrade-261006-0850-attempt-01/p7-deterministic-attempt-02.json) records311 tests in914.791seconds:310pass,1skip, exit0, exact discovery inventory matched and unchanged source-lock pre/post hashes. The single skip is the real symlink fixture denied by Windows privilege1314. The alternate observable command is recorded explicitly; the original public900-second timeout remains retained separately. Fresh reproducibility and package/extraction/previews remain active until their receipts exist.

Two-build reproducibility completed for four hosts in both standalone ON (historical evidence path: `../runs/nckh-upgrade-261006-0850-attempt-01/p7-reproducibility-standalone-attempt-02.txt`; unavailable in the cleaned checkout) and plugin ON (historical evidence path: `../runs/nckh-upgrade-261006-0850-attempt-01/p7-reproducibility-plugin-attempt-02.txt`; unavailable in the cleaned checkout), exit0 with unchanged r41 source hashes. The first remaining task is therefore complete; persistent16-bundle build, external extraction/reader/preview and final review/delivery remain active.

[All local gates](../runs/nckh-upgrade-261006-0850-attempt-01/p7-local-gates.json) completed with nine actual commands, all exit0 and matching r41 source hashes. [External qualification](../runs/nckh-upgrade-261006-0850-attempt-01/p7-extracted-qualification.json) records16 verified bundles,420 actual isolated resource reads,eight relocated research checker runs,eight read-only installer previews with identical pre/post source/target hashes, and three unchanged legacy bundles in formats1/2. All eight internal OFF bundles have no resource payload and actually returned disabled/no-read. [External temp cleanup](../runs/nckh-upgrade-261006-0850-attempt-01/p7-temp-cleanup.json) records20,528 snapshotted owned files before exact unchanged-root removal. Supervisor and child handles exited; pre-final process observation found no live Python process. Only final evidence assembly/review/delivery remains.

### Delivery closure

[Experimental candidate](../runs/nckh-upgrade-261006-0850-attempt-01/experimental-candidate.json) và [delivery r41](../reports/delivery-261006-research-upgrade-r41.md) đã được tổng hợp từ actual receipts. Final reviewer xác nhận toàn bộ receipt/hash checks hoàn tất và không có blocker; [qualification review](../reports/review-261006-research-final-qualification.md) giữ static finding đã sửa cùng final verdict/fingerprints. [Final preservation](../runs/nckh-upgrade-261006-0850-attempt-01/p7-final-preservation.json) đối chiếu trực tiếp590 protected hashes, zero mismatch. [Final process reconciliation](../runs/nckh-upgrade-261006-0850-attempt-01/p7-final-process-reconciliation.json) ghi supervisor/final reconciler exit0, tất cả tracked PIDs vắng mặt, owned_live0 và không dừng process không thuộc task. P7 hoàn tất trong phạm vi experimental/local-package-only; scientific/human/owner/full-native/semantic/provider/stable/public và actual install vẫn độc lập. Lịch sử failure/timeout/unknown được giữ, không transplant verdict.
