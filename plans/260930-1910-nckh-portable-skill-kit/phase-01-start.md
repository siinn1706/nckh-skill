---
title: "Phase 1: Contracts, workflow and model policy"
status: in-progress
---

# Phase 1: Contracts, workflow và model policy

<!-- Cook --auto authorized on 2026-10-01; technical implementation and acceptance are tracked separately. -->

## Overview

Priority P1. Source/contracts đã triển khai theo [cook --auto được duyệt](plan.md) ngày 01/10/2026. Effort ban đầu 4–6 ngày. Acceptance về hành vi auto/interactive và native model vẫn pending. Package paths dưới đây hiện có source; không triển khai orchestration server.

## Context Links

- [Architecture](architecture.md), [workflow/model](workflow-and-model-routing.md), [catalog](skill-catalog.md), [runtime](runtime-compatibility.md).
- [Old authorization/evidence contract](../260930-0905-vietnamese-research-skill-kit/phase-01-start.md) và [11 invariant](../reports/red-team-260930-0905-adjudication.md): chỉ tham chiếu lịch sử; [migration map hiện hành](installer-evaluation-migration.md) quyết định phần kế thừa.

## Key Insights / Architecture

Policies không là skills; state không là chat history; role không là model. Core libraries, four workflow skills và per-task private records cùng một contract. NCKH controllers phải dựa host permissions thật, không tự nhận JSON authorization field là quyền thực.

Model policy resolve theo runtime capability và account được user cho phép; requested khác effective. Same-agent mặc định; fresh context, cheaper/stronger model hoặc independent check là lý do cụ thể, không bắt spawn vì phase có nhiều skill.

## Requirements

- Source/evidence/claim/profile/task/receipt schemas có revision/hash, provenance, uncertainty và gate aggregation.
- State phân planned/authorized/running/checking/ready-for-review/accepted với waiting/failed/timeout-unknown; attempt reconciliation trước retry, invalidation khi scope/input/profile đổi.
- Plan-only không product write; auto không routine pauses nhưng không bỏ mandatory human/security/egress gates; interactive có meaningful stop + feedback/resume.
- Five model profiles và fast/worker/deep/inherit, minimum sufficient context, cost-known/unknown; không universal token cap.
- English skill instructions, output locale theo brief; policies hỗ trợ ba domain, không ép scientific ranking lên mọi content.

## File ownership — Create only after authorization

Primary package root: `C:/Users/USER/Downloads/test-skill/nckh-kit/`.

| Absolute path / bounded subtree | Owner work |
|---|---|
| `C:/Users/USER/Downloads/test-skill/nckh-kit/core/policies/` | Evidence, authorization/privacy, preservation và acceptance policies. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/core/contracts/` | Brief, evidence, claim, profile, task-state, receipt, delegation và catalog schemas. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/core/workflows/` | Plan/validate, cook auto/interactive, review, resume/handoff. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/core/profiles/models/` | Logical profiles + fallback requirements; không hard-coded vendor catalog. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/core/registry/catalog/` | Catalog schema và 37 identity/dependency records; single owner. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/core/registry/source-lock/` | Source pin, hashes, license/attribution status. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/agents/` | Sáu optional role templates và context packets. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/skills/core/` | Chỉ `nckh-plan`, `nckh-cook`, `nckh-review`, `nckh-handoff`. Sáu skill khác thuộc P2. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/tests/contracts/` | Workflow/state/model-policy/registry tests; unittest naming convention. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/evals/cases/workflow/` | Four owned skills, permission và model-routing cases. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/docs/contracts.md` | Contract ownership, extensions và honest status semantics. |

Không delete baseline. P2–P4 gửi registry changes về owner này; không sửa đồng thời shared files. P5 sở hữu compatibility mapping/build, P6 transaction manifests. Private task store không nằm trong source/dist.

## Implementation Steps

1. Re-inventory workspace; đọc approval thiết kế ngày 01/10/2026, xác nhận scope/quyền cook riêng và ghi exact version pins. Không hỏi lại kiến trúc đã duyệt nếu không có delta mới; nếu source đã đổi, review delta trước tạo package.
2. Khóa contracts và migration map của 11 invariant; phân source identity, support và human acceptance thành các trường khác nhau.
3. Viết contract/state tests trước workflow text: unauthorized transition, stale artifact, timeout retry, aggregate gates và changing scope.
4. Viết four Core skills + roles/model profiles. Contract-only validation dùng stdlib và schema subset được test rõ; không tự tải dependency để “validate”.
5. Viết cases auto/interactive, simple/deep/same-model/no-benefit delegation, no-tag/conflicting/unsupported-tag/colliding-trigger routing và unknown telemetry; specify oracle và prohibited actions trước run. Khóa model-resolution và expanded receipt fields theo design documents, không requested-as-effective.
6. Làm capability feasibility check sớm bằng docs/help và authorized disposable probes cho Python, skill roots, spawn/model/effort ở bốn host và prerequisites Windows/macOS/Linux khi có lab. Consumer/paid/OS probe chưa được phép thì record pending; chỉ block phần phụ thuộc, không ghi pass.
7. Review contract consumers: 37 catalog identities, six roles, four adapter contracts, installer và eval records. Freeze revision trước mở P2; không dùng 37 như số source đã triển khai.

## Todo

- [x] Xác nhận quyền cook riêng và khóa private/public boundary theo thiết kế đã duyệt.
- [x] Khóa schemas, shared policies, registry và source pin.
- [x] Viết four workflow skills + model/agent templates.
- [x] Viết và chạy deterministic contract suite sau khi source tồn tại.
- [x] Ghi native feasibility evidence/pending và handoff revision cho P2.
- [ ] Thu behavioral/native acceptance cho auto, interactive, feedback/resume và effective model theo protocol.

## Success Criteria

- Four skills có distinct outcomes và complete eval IDs: plan/review/handoff không mutate product, cook chỉ thực thi trong authorized scope; không claim runtime quality từ static checks.
- Auto không routine pauses; interactive có artifact/hash/review scope, downstream stop và feedback invalidation được quan sát trong authorized behavior run.
- Unauthorized/timeout/stale-hash transitions fail; human-reviewed không tự override pending/failed gates.
- Simple task không unnecessary spawn; deep task không xuống fast âm thầm; unknown model/window/cost giữ unknown.

## Validation commands và evidence scope

Working directory: `C:/Users/USER/Downloads/test-skill/nckh-kit/`.

`python -m unittest discover -s tests/contracts -p "test_*.py"`

Narrow first: workflow state; sau đó toàn contracts. Tests đã có source. Receipt local (historical evidence path: `../../nckh-kit/evals/results/local-checks.json`; unavailable in the cleaned checkout) phải khớp source-lock hiện hành; xem status thực trong receipt. Agent/native/human acceptance cần run và receipt riêng.

## Risk / Security / Rollback

Tránh biến policy library thành giant prompt hoặc state engine thành permission system. Chỉ dùng subset schema đã test; unknown field/version fail minh bạch. Source input không cấp quyền. Khi contract sai, revert candidate files do phase sở hữu về snapshot đã ghi; giữ task evidence và original inputs, không rollback toàn workspace.

## Next Steps

P2 dùng frozen contracts. P3/P4 chưa sửa shared registry. P5 nhận feasibility notes, không cần installer global để chứng minh sớm.
