---
phase: 3
title: "Scientific dataset lineage/splits và telemetry semantics"
status: completed
priority: P1
effort: 3-4 ngày công
dependencies: [phase-01-start, phase-02-research-and-statistics]
---

# P3 — Scientific dataset lineage/splits và telemetry semantics

## Outcome và boundaries

`nckh-dataset` sở hữu acquisition/curation/quality/labels/splits/release decision của research files; `nckh-telemetry` sở hữu logs/metrics/traces semantics/time/joins. DB/query/migration vẫn `nckh-data`. Telemetry không tự collect production, tạo modality thiếu hoặc quyết ground truth/RCA.

`KIT = C:/Users/USER/Downloads/test-skill/nckh-kit`; `RUN` là P1 frozen attempt root. Đọc [review](../reports/code-reviewer-261005-0036-current-research-kit.md), [adoption](./source-adoption-map.md), primary OpenTelemetry reference và [matrix](./acceptance-matrix.md). OpenTelemetry convention/version/status phải resolve tại cook; không dùng API nhớ từ snapshot này.

## Ownership và files

Dataset-telemetry owner giữ specialty files; shared schema package closure/catalog/docs controller integrate tuần tự. Không sửa `nckh-data` implementation hoặc resource registry ở phase này.

| Action | Absolute named path | Change |
|---|---|---|
| Create | `KIT/skills/core/nckh-dataset/SKILL.md`, `KIT/skills/core/nckh-dataset/references/intake-lineage-and-splits.md` | Intake/quality/split/release route |
| Create | `KIT/skills/core/nckh-telemetry/SKILL.md`, `KIT/skills/core/nckh-telemetry/references/signals-time-and-joins.md` | Observation mapping/normalization/quality route |
| Create | `KIT/core/contracts/dataset-manifest.schema.json`, `KIT/core/contracts/split-manifest.schema.json`, `KIT/core/datasets.py` | Research file/label/transform lineage và immutable membership validators |
| Create | `KIT/core/contracts/telemetry-manifest.schema.json`, `KIT/core/telemetry.py` | Units/time/resource/correlation/join/quality validators |
| Create | `KIT/tests/research/test_datasets.py`, `KIT/tests/research/test_telemetry.py` | Proposed intake/split/join invariants |
| Create at cook | `RUN/dataset-manifest.json`, `RUN/split-manifest.json`, `RUN/telemetry-manifest.json`, `RUN/data-quality.md` | Metadata/task artifacts; actual data under authorized project private root |

## Contract design

`dataset-manifest` v1: project/task/source IDs+version/raw hashes, retrieval/as-of/rights/access, sample schema/unit/entity/incident/time IDs, modality scope, transform code/config/output hashes, row counts/exclusion/missingness/quarantine, label source/annotator/adjudication/access and release limitations. Raw, normalized, redacted và evaluation inputs giữ separate hashes. Tokenization không đủ chứng minh anonymization.

`split-manifest` v1: parent dataset hash, actual purpose/independence axes, canonical actual sample/group/entity/incident membership và time-interval manifests with hashes/counts, temporal cutoffs/windows/embargo khi design cần, preprocessing/feature/threshold fitting policy, label/holdout access, exclusions và overlap audit. Validator đọc actual keys/intervals để kiểm overlap; chỉ có membership hash/count không đủ phát hiện train={i1,i2}, test={i2,i3}. Scientific axes không dùng unchanged kit qualification `document/author/topic/claim-family` protocol. Chronological/group/incident partitions chọn theo estimand; không áp một ratio cố định.

`telemetry-manifest` v1: actual modalities, source schema/semantic-convention versions, timestamp origin/timezone/precision/clock alignment, unit/type/aggregation/monotonicity khi applicable, resource/service/host identity, trace/span/correlation keys, sampling/cardinality/retention, window/join rules, raw-normalized mapping, missingness/duplicate/gap/clock skew records và quality/output hashes. `unknown` giữ reason; thiếu logs/traces không sinh giả. Join cardinality/time tolerance explicit; raw labels không được leak vào features.

## Implementation steps

1. Author thin owners và source→artifact boundaries; acquire only selected authorized sources. Plan-only hoặc unresolved rights chỉ metadata; no live collector/ambient database credentials grant.
2. Implement closed schemas + stdlib invariants; paths canonical/contained, finite values, duplicate IDs/ambiguous JSON rejected. Controller-trusted hard caps per-file/aggregate bytes/records/output phải kiểm trước read/parse/allocation; stream bounded read/hash thay full `read_bytes` cho large artifacts. Payload không được nâng caps; oversize/cross-file aggregate excess từ chối với reason, không clip rồi ghi complete. Validators không chạy source commands hoặc load unlimited corpus.
3. Verify row/field schema, missing values, duplicates, label conflicts, transformation reconciliation; quarantine preserves locators/reasons. Raw/private bytes stay ngoài source/dist; redaction trước sharing.
4. Freeze canonical actual membership trước model tuning; train-only learned preprocessing, validation-only thresholds/model selection và sealed test. Feature availability bind task decision time: forecasting không đọc future covariates; RCA có thể đọc diagnostic incident-window observations theo frozen protocol. Không blanket cấm post-incident data; label/answer leakage vẫn cấm. Validate temporal/incident/group keys/intervals và access separation. Split drift invalidates experiment/results; holdout exposure ghi development/amendment, không rename thành blind.
5. Normalize real pilot modalities bằng explicit map; preserve empty units/unknown timestamps. Validate one-to-one/one-to-many/many-to-many join rules, clock skew/time tolerance, dropped/unmatched rows, cumulative counter resets và aggregation distinction theo source.
6. Add focused positive/near-miss/failure tests; handoff frozen manifests đến AIOps/statistics. Dataset owner owns labels/splits; telemetry handoff quality, không infer root cause.

## Todo

- [x] Create dataset owner/manifests/validators với rights/privacy/lineage.
- [x] Create immutable split contract và temporal/group/incident leakage checks.
- [x] Create telemetry owner/manifest/normalization-quality checks.
- [x] Test missingness, units/time, joins/cardinality, label conflict và invalidation.
- [x] Handoff frozen artifacts và unknown modality/rights gates cho P4/P6.

## Verification — proposed tests, chưa chạy

Từ `KIT`: `python -B -m unittest tests.research.test_datasets tests.research.test_telemetry`, domain/schema checks độc lập source lock. Existing preservation/state suites `tests.contracts.test_state`/`tests.resource.test_real_sources` cần narrowed dependency inspection; pinned source/build checks hoãn P7 sau candidate freeze. No network/provider/dataset downloads trong unit tests; fixtures tagged deterministic; real pilot deferred to P6.

Success: missing ≠ zero; source counts reconcile; unknown units/time không tự đoán; forbidden many-to-many/time/outside-root join fails; actual membership overlap/decision-time leakage/test-fitted transform fails while permitted RCA incident-window observations pass; oversize/aggregate caps reject before unbounded allocation; label access/rights có actual evidence. Empty data không thành quality pass.

## Risk/security/rollback

Telemetry có thể chứa secrets/PII: bound read/rights/redaction/access, không publish examples từ real logs. Normalization có thể mất semantics: keep raw→normalized lineage và quality reason. Restore only owned derivative/config bytes với hashes; retain raw inputs/quarantine/history; no destructive dataset rewrite, credential use hoặc rollback source baseline của agent khác.
