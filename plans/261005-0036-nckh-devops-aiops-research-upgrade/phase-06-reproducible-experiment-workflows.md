---
phase: 6
title: "Reproducible experiment artifacts và bounded real pilot"
status: completed
priority: P1
effort: 2-3 ngày công
dependencies: [phase-03-scientific-datasets-and-telemetry, phase-04-devops-and-aiops-methods, phase-05-curated-research-resources]
---

# P6 — Reproducible experiment artifacts và bounded real pilot

## Outcome và context

Bind question/protocol → dataset/split → telemetry → code/config/environment → predictions/metrics → evidence/readout bằng actual artifacts/receipts. Method owns design; cook owns lifecycle/attempts; devops owns environment/process/cleanup; four specialty owners keep output contracts. Không thêm research orchestrator, runner framework hoặc autoresearch tree.

`KIT = C:/Users/USER/Downloads/test-skill/nckh-kit`; `RUN` là P1 actual absolute attempt root. Actual pilot data/project root được P1 chọn với grant, không giả định quyền trên repo CS221 khác. Đọc [adoption](./source-adoption-map.md), [matrix](./acceptance-matrix.md), P2–P5 contracts và task accepted protocol.

## Ownership và files

Experiment owner tạo bounded read-only artifact validators/checker và refs; controller serialize edits với P2 method/P4 devops/P7 state/docs owners. Không thay `core/state.py` lifecycle trừ proven contract gap được controller review.

| Action | Absolute named path | Change |
|---|---|---|
| Create | `KIT/core/contracts/experiment-manifest.schema.json`, `KIT/core/contracts/research-run-receipt.schema.json`, `KIT/core/experiments.py` | Closed plan/run artifact graph + drift/failure validator, no execution engine |
| Create | `KIT/scripts/check-research-artifacts.py` | Proposed read-only checker of task artifact graph |
| Create | `KIT/tests/research/test_experiments.py` | Proposed graph/receipt/timeout/failure/simulation/invalidation cases |
| Create | `KIT/skills/core/nckh-method/references/reproducibility.md`, `KIT/skills/core/nckh-cook/references/research-experiments.md` | Actual run/handoff/attempt methodology |
| Modify serialized | `KIT/skills/core/nckh-method/SKILL.md`, `KIT/skills/core/nckh-cook/SKILL.md`, `KIT/skills/engineer/nckh-devops/references/research-environment.md` | Link workflow boundaries/quality gates |
| Create at cook | `RUN/experiment-manifest.json`, `RUN/receipts/`, `RUN/pilot-readout.md`, `RUN/cleanup.json` | Actual freeze/attempt/failure/readout/cleanup artifacts |

## Required artifacts

`experiment-manifest` v1: project/task/protocol IDs+hashes, dataset/split/telemetry/analysis/evaluation refs, source/code/config/environment/workload/model/package versions, selected baselines/ablations, metrics/oracles, resource/egress/provider limits, seed/repeats/uncertainty applicability, expected artifact paths, grants/cleanup route và freeze time/amendment log. External/library versions verified official API tại cook; no support guarantee từ source metadata.

`research-run-receipt` v1: unique attempt/run ID, manifest/input hashes, actual argv/cwd/environment observation, start/end/timezone/exit/status, process identity/PID/cleanup, stdout/stderr refs+hashes, outputs/predictions/metrics hashes/counts, measured resource/cost coverage hoặc unknown, failure/timeout/cancel/deviation reasons. Distinguish scheduled/running/completed-unreviewed/failed/cancelled và reconciliation; no completed flag từ output existence alone. Source/run receipt identity bảo vệ integrity, không authenticate fabricated host observations.

Reuse general receipt evidence classes và task attempts; new research-run record stores domain execution facts, references generic receipt/host observation when needed. Simulation output label `simulation/not observed measurements`, actual code/parameters/RNG/replications/warm-up/conservation/uncertainty và model validity limits; simulation CI không chứng minh real-system effect.

## Implementation steps

1. Add linked reproducibility/run protocol refs và closed validators; require each input/output hash resolve to contained authorized project path. Hash/read streams follow controller-trusted per-file/aggregate/record/output hard caps checked before allocation; oversize rejects with bounded reason and cannot become clipped success. Separate plan/readout/run stages; stale code/data/split/metric/config invalidates downstream outputs.
2. Implement proposed checker `--project <absolute-root> --task <id> --manifest <project-relative-file> --output <project-relative-receipt>`; read-only beyond explicitly output receipt, no subprocess/provider/network/install. Run instructions remain with existing cook/devops; untrusted manifest argv is recorded data, never executed by validator.
3. Select at least one bounded rights-cleared real pilot from P1. Use actual available modalities/source labels and local baseline; freeze task/metrics before execution, record source/data/calculation provenance. Benchmark remote ingest/provider/cluster/fault side effects require specific grant; if absent choose permissible offline input route or preserve blocked gate, không invent substitute corpus.
4. Execute only accepted local operations via authorized cook. Resource/runtime dependencies task-level optional; actual inputs/code/config/environment and clean process lifecycle recorded. Preserve failures/timeouts, reconcile handles/PID identity before retry, no arbitrary time limit or changed ports hiding collisions.
5. Compute readout using actual prediction/sample counts with independent oracle; statistics checks unit/assumptions/uncertainty, AIOps checks task metric/tie/failure policy, dataset checks split/gold isolation, telemetry checks missingness/joins. Add simulation-only mini-case only if task needs simulation; not a substitute for real pilot.
6. Handoff evidence ledger/readout to paperwrite and owner. Factual/style review does not create human scientific acceptance; actual owner feedback binds revision/artifact/input hashes. Agent/provider/LLM/RAG trials only when actual granted runtime/budget exists, otherwise pending/not-callable in matrix.

## Todo

- [x] Implement manifest/run receipt graph validators và scoped checker.
- [x] Integrate method/cook/devops references without new lifecycle engine.
- [x] Freeze real pilot source/rights/protocol/metric/runtime grants.
- [x] Run bounded actual pilot và preserve success/failure/reconciliation receipts.
- [x] Review data/telemetry/statistical/AIOps readout, cleanup và evidence handoff.
- [x] Record owner/scientific/native/provider pending states truthfully.

## Verification — future/proposed only

From `KIT`: `python -B -m unittest tests.research.test_experiments`; actual proposed checker after implementation: `python -I scripts/check-research-artifacts.py --project <absolute-pilot-root> --task <task-id> --manifest <relative-experiment-manifest.json> --output <relative-check-receipt.json>`. Isolated checker must include local schema/helper closure; output flag không grants extra paths/side effects.

Success: no fake or historical receipts reused for changed inputs; hashes/row/prediction denominators reconcile; aborted/timeout/failed attempts remain visible; cleanup closes owned handles; real pilot actual readout exists and scope limits explicit. Mechanical fixture or simulation không chứng minh empirical benchmark superiority hoặc scientific acceptance.

## Risk/security/rollback

Missing source/rights/runtime grant giữ pilot pending; controller resolve concrete gate before dependent actions. Resource exhaustion/provider cost có bounded authorized budget; unknown remains unknown. Stop only owned processes, restore owned derivative outputs/preimages with current hash checks, preserve input/raw data/private labels and every failed attempt. Không delete dataset/cluster or modify installed source as rollback.

## Actual execution evidence

[Independent review and repaired re-review](../reports/review-261006-experiment-graph-and-pilot.md), 110 domain tests (historical evidence path: `../runs/nckh-upgrade-261006-0850-attempt-01/p6-domain-tests-attempt-04.txt`; unavailable in the cleaned checkout) and [fresh isolated graph check](../runs/nckh-upgrade-261006-0850-attempt-01/p6-isolated-graph-check-02.json) qualify source behavior and the unchanged actual graph. [Pilot readout](../runs/nckh-upgrade-261006-0850-attempt-01/pilot-readout.md) retains 26 source observations, six test predictions and independent endpoint arithmetic. [Partition supplement](../runs/nckh-upgrade-261006-0850-attempt-01/partition-supplement-receipt.json) adds genuine separate train/validation/test calculations: 52 outcomes, 49 completed and three insufficient-history unknowns; original test values are unchanged. The supplement is a separately hash-bound process observation, not a promoted research-run graph. [Final evidence handoff](../runs/nckh-upgrade-261006-0850-attempt-01/paperwrite-evidence-handoff-v2.json) binds current validator source, actual receipts and pending gates. Original fixture failures and counsel remain preserved. Both owned child handles are reaped; CPU/memory/provider cost remains unknown. Scientific/owner/full-native/provider/stable/public gates stay separate.
