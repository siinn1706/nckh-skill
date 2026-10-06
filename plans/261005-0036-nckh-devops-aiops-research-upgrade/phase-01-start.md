---
phase: 1
title: "Baseline hậu cook, quyền nguồn và routing freeze"
status: completed
priority: P1
effort: 1-2 ngày công
dependencies: []
---

# P1 — Baseline hậu cook, quyền nguồn và routing freeze

## Context và outcome

Đọc [scope contract](../reports/brainstorm-261005-0036-research-upgrade-contract.md), [review](../reports/code-reviewer-261005-0036-current-research-kit.md), [adoption map](./source-adoption-map.md) và delivery cuối của plan trước. Ngày 06/10/2026 source baseline thực là r38 advisory. User đã chỉ đạo subagent kiểm chứng native nhanh rồi upgrade khi biết plan trước còn 44/45; source edits chờ actual scoped result, không chờ toàn bộ matrix cũ. Full native/stable acceptance giữ pending riêng.

`WORK = C:/Users/USER/Downloads/test-skill`; `KIT = C:/Users/USER/Downloads/test-skill/nckh-kit`. `RUN` là directory attempt thực do controller tạo dưới `WORK/plans/runs/`, tên có timestamp và attempt; ghi absolute root vào receipt, không giả tạo một run đã có.

## Ownership và file surfaces

Controller owns phase, scope grants, shared catalog/build/acceptance integration, schema package closure, docs integration và final freeze. Domain owners chỉ nhận file boundaries ở phases; không sửa shared files cùng lúc.

| Action | Absolute named path | Mục đích |
|---|---|---|
| Read | `KIT/core/registry/source-lock/source-lock.json`, `KIT/core/registry/catalog/{skills,resources}.json` | Exact baseline revision/hash/identities/resources |
| Read | `WORK/.nckh-state/ownership.json`, `WORK/.agents/skills/`, plan trước và final delivery/check receipts | Installed/source/accepted states riêng |
| Read | `KIT/core/{schema,build,evaluation,acceptance,resources}.py`, `KIT/core/contracts/catalog.schema.json` | Exact-set consumers, supported schema keywords |
| Create at cook | `RUN/baseline.json`, `RUN/rights-ledger.json`, `RUN/ownership-map.json`, `RUN/pilot-selection.json` | Actual observed baseline, source/right/route selection |
| Modify at cook | `KIT/docs/research-and-writing.md`, `KIT/docs/engineer.md` | Chỉ handoff boundaries đã khóa; controller phối hợp P2/P4 |

## Requirements và contract freeze

Target set = exact approved baseline union `{nckh-dataset,nckh-statistics,nckh-telemetry,nckh-aiops}`. Nếu final baseline khác 39/156, báo delta và cập nhật exact set/IDs trước implementation; không xóa scope để đạt counts. New skills thuộc `core`, experimental, English instructions/VI-EN artifacts. Preserve old identity paths, base IDs, 19 families và historical qualification protocol.

Schema names đề xuất được khóa: `dataset-manifest`, `split-manifest`, `statistical-analysis`, `telemetry-manifest`, `aiops-evaluation`, `experiment-manifest`, `research-run-receipt`, `owned-resource-provenance`. Closed/schema-versioned; validator của owner kiểm exact sets/counts/variant conditions. Existing `core/schema.py:validate_record(kind)` resolves `core/contracts/<kind>.schema.json` dynamically, không có registration table; chỉ sửa engine nếu cook chứng minh owning requirement riêng. Engine không hỗ trợ `oneOf/anyOf/uniqueItems/maxItems`; giữ subset hiện tại.

## Implementation steps

1. Nhận final cooked handoff, source lock và actual check receipts của plan trước; resolve đang-running/failed attempt trước khi bắt đầu. Record grants và excluded operations từ user/host policy.
2. Băm current pins, inventory exact catalog/cases/families/resources; record installed ownership riêng. Giữ nguồn concurrent của agent trước, không rewrite reports/receipts của họ.
3. Freeze owner map: dataset intake/selection/splits; telemetry signals/time/joins; statistics inference; AIOps task/evaluation; method design; research discovery; cook lifecycle; devops environment/process. Record near-miss routes trong [matrix](./acceptance-matrix.md).
4. Đọc source manifests theo selected components; trước copied material resolve true upstream version/ref và per-file/nested license/NOTICE. Unknown commit ở ZIP giữ unknown. Restricted ClaudeKit/proprietary docs không copy; public-source independent design theo adoption map.
5. Chọn bounded real pilot cho P6: rights-cleared incident telemetry hoặc supplied scientific project; record modalities thực, source/archive hash, time/unit/label scope, allowed local operations/size. Không ingest hoặc run nếu grant không có. Unknown rights giữ metadata-only và gate còn mở.
6. Ghi baseline/protection hashes cho marketing, writers/visual/hooks, installed state và history; handoff cho P2. Controller giữ shared file queue; P1 chưa freeze new source lock vì chưa có implementation.

## Todo

- [x] Reconcile final baseline/handoff và exact approved identity/case set.
- [x] Freeze owner routes, schema names và shared edit queue.
- [x] Resolve selected source rights/ref ledger với no-copy decisions.
- [x] Freeze pilot input/rights/operations/size plan và protected hashes.
- [x] Review P1 artifacts; cấp domain owners file boundaries.

## Verification — tương lai, chưa chạy

Từ `KIT`, existing structural command: `python -B evals/run-evals.py --validate-only --output <RUN/baseline-case-validation.json>`. Đây là case/contract check; không chạy provider/native/human. Hash/pin checks dùng owning `core.build.verify_source_lock` trong trusted local check, record before/after lock hash để phát hiện concurrent drift.

Success: baseline pin inventory đúng, final handoff references tồn tại; source rights không bị nâng thành cleared từ root license; pilot selection có explicit pending/pass cho mỗi quyền; no product/install/config writes trước P1 completion. Không gọi parser/hash là cook/scientific acceptance.

## Risk, security và rollback

Baseline drift hoặc chưa có final handoff: dừng source edits, đọc lại exact changed inputs và update state. Rights conflict: no-copy, reauthor từ public primary references. Private source credentials/labels không vào plan/source/dist. P1 rollback chỉ gỡ matching owned planning/run records đã tạo khi có quyền; giữ old attempts/protected bytes. Không rollback agent trước hoặc installed state.

## Handoff

P2 nhận baseline/schema/ownership ledger; P3–P7 dùng cùng frozen decisions. Thay scope/ref/owner sau freeze phải ghi amendment và invalidate dependent work.

## Actual execution checkpoint — 06/10/2026

Actual attempt root: `C:/Users/USER/Downloads/test-skill/plans/runs/nckh-upgrade-261006-0850-attempt-01`. [Baseline](../runs/nckh-upgrade-261006-0850-attempt-01/baseline.json) records r38, 281 verified pins, exact 39 identities/156 base IDs/19 families/9 resources. [Protected hashes](../runs/nckh-upgrade-261006-0850-attempt-01/protected-hashes.json) preserve 506 installed files, ownership, legacy lock history and source-owned marketing/writer/visual/hook boundaries. [Ownership](../runs/nckh-upgrade-261006-0850-attempt-01/ownership-map.json), [rights](../runs/nckh-upgrade-261006-0850-attempt-01/rights-ledger.json) and [pilot selection](../runs/nckh-upgrade-261006-0850-attempt-01/pilot-selection.json) are observed/preparatory records; quick native admission and final pilot route remain pending. Two project-local SQLite indexes were backed up before status mutation; current index is `.agentkit-runtime`, while the older `.agentkit-state` lookup returned plan-not-found and was preserved.

Final P1 handoff uses [admission](../runs/nckh-upgrade-261006-0850-attempt-01/baseline-admission.json), [rights v2](../runs/nckh-upgrade-261006-0850-attempt-01/rights-ledger-v2.json) and [pilot v2](../runs/nckh-upgrade-261006-0850-attempt-01/pilot-selection-v2.json). All 69 selected local source hashes match; archive commits remain unknown and no-copy dispositions stand. The selected permissible offline scientific-project pilot has 26 actual World Bank observations, exact raw/normalized/notice lineage and 20/3/3 chronological membership. Native subagent observed one Codex CLI0.154.0/GPT5.6Luna/medium callback, advisory non-denial and sandbox-blocked mutation; 791 hashes preserved/zero owned-live at cleanup. The old native gate is unchanged. Shared source owners are the sequential controller; P2 receives actual schema/routes/rights/protection and pilot design.
