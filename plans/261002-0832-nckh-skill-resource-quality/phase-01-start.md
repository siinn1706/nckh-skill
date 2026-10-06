---
title: "Phase 1: Test/provenance freeze"
status: completed
---

# Phase 1: Test/provenance freeze

## Overview

<!-- Historical plan amendments: R1/R5/R7/R10, 2026-10-02; execution authorized 2026-10-02 -->

Khóa sự thật đầu vào trước mọi resource edit: phân biệt package structural lane với direct-development lane, giữ 37 identities và toàn bộ lịch sử, rồi sửa cause-aligned evaluator guards để một resource chỉ được đóng gói/đánh giá khi có consumer, provenance và quyền rõ. P1 đã triển khai evaluator/schema/holdout guards, lưu baseline 18 và evaluator freeze 19, tạo direct linkage riêng. Source candidate có revision mới; không chạy provider/native/human, cài skill hay đổi package `not-run` thành pass.

## Evidence trước thực thi và runtime audit

- `plans/reports/review-261002-0832-nckh-skill-quality.md:20-42,46-74` ghi source revision 18/hash, 184 pins, 37/148/19/224 package lane, direct 137/4/7 rồi 147/1/0, và giới hạn installed revision 14/exposed synthetic.
- Canonical source-lock hash của baseline lịch sử phải giữ nguyên: `f52a03676b29fbd5434673a0f831dcae397fe879131beec00f35d3ca9b4d472d` (64 hex, revision 18); không dùng hash rút gọn hay nhầm file hash. Candidate được phép có revision/hash mới sau authorization và freeze nhất quán; không viết lại snapshot/history cũ.
- `nckh-kit/core/build.py:39-50` chỉ inventory `.md/.json/.yaml/.toml/.py/.ps1/.sh`; `:53-99` freeze/verify source-lock với `owned-local-package` và `copied_third_party_content=false`.
- `nckh-kit/core/evaluation.py:11-73` giữ 37 identities, 148 cases, 19 families, 5 rubrics, 224 runtime cells, rubric/human/installer gates pending; `nckh-kit/core/schema.py:87-89` là owner validator theo contract hiện hữu.
- Runtime report `plans/reports/code-reviewer-261002-0832-nckh-runtime-evals.md` đã xác nhận narrow validation pass nhưng negative oracle mâu thuẫn expected route ở 37/37 manifests, required-family check chỉ đếm 19, protocol shape chưa validate, direct 148 chưa có machine-readable mapping và `development_round` chưa freeze protected holdout. Đây là repair/ regression work của P1, không phải lý do gọi static validation là quality proof.
- `plans/reports/testing-261001-direct-skill-development.md:5-42,104-110` xác nhận corpus direct 148/hash, installed 14 khác source 18, exposed review, no holdout/baseline/human acceptance; không nhập receipt này vào package lane.
- Nature report `plans/reports/researcher-261002-0832-nature-resources.md` và AgentKit report `plans/reports/researcher-261002-0836-agentkit-resources.md` chỉ cung cấp pattern (router/manifest/consumer/eval), không cấp quyền copy; Nature full HEAD/license phải pin lại khi triển khai.
- `nckh-kit/evals/protocols/qualification.json` giới hạn 3 development rounds, 1 protected holdout run và exposure → development. `core/agent_runs.py:154,163-168` chỉ phát development; `docs/qualification.md:116` xác nhận protected execution chưa callable. Sửa helper không tạo thêm runtime route.

## Requirements

- [x] Giữ 37 catalog records (10 Core, 13 Engineer, 13 Marketing, 1 Xia), dependencies và 4 eval IDs/identity; không tạo manifest bắt buộc cho từng skill.
- [x] Ghi freeze record gồm source-lock revision/hash, catalog hash, package case manifest hash, direct corpus hash, subject revision, lane/evidence class, input rights, split và receipt references. Cờ `not-run`, `pending`, `failed`, `completed-unreviewed` giữ nguyên nghĩa.
- [x] Sửa contract/oracle để mọi negative case có acceptance phủ `expected_route=reject-this-skill` (owner/handoff/no task execution), thêm regression cho 37/37 pattern; không sửa oracle hồi tố để che failure.
- [x] Validate 19 required families theo schema/field types/status/rights/provenance/oracle/evaluator/receipt và map catalog/case IDs, không chỉ `len==19`; validate required qualification protocol keys bằng closed-schema subset.
- [x] Ghi machine-readable linkage riêng cho direct evidence: corpus hash, source/install revision, condition, case mapping, review class và receipt hashes; giữ package cases `not-run` và direct evidence là controller-development, không chuyển thành package pass.
- [x] Chặn `development_round(..., exposed_holdout=False)` thành protected holdout nếu thiếu freeze/rights/reviewer/threshold/partition receipt; helper phải trả pending/error, có default-branch regression. Giữ tối đa 3 development rounds, 1 protected holdout run, exposure → development; current runner vẫn development-only. Protected holdout là pending/NOT_CALLABLE cho đến khi có private route, inputs và human grant thật; không xây protected-holdout engine trong plan này.
- [x] Định nghĩa resource record tối thiểu: `resource_id`, consumer skill, path/format, producer/reader, source kind, version/full SHA, license/NOTICE/redistribution state, copied-vs-re-authored state, dependency type, expected artifact và acceptance/rollback.
- [x] `copied_third_party_content=false` và `owned-local-package` không được dùng để relabel import. Mặc định dùng dữ liệu thật từ source/user-supplied/rights-cleared shortlist; bytes upstream chỉ được xem xét sau rights contract pin riêng, nếu thiếu thì `not-packaged`.
- [x] Nối mapping case/input/oracle/subject/receipt nhưng không sửa 148 case definitions cũ nếu chưa có input/oracle review; direct corpus synthetic owned-development vẫn ở private/evaluation lane, không tạo synthetic dataset mới.

## File ownership

| Owner | Exact paths | Responsibility |
|---|---|---|
| P1 evaluator/freeze owner | `nckh-kit/core/evaluation.py`; `nckh-kit/core/contracts/`; `nckh-kit/evals/cases/`; `nckh-kit/evals/cases/required-families.json`; `nckh-kit/evals/protocols/qualification.json`; `nckh-kit/tests/release/test_qualification.py` | Negative oracle, family/protocol schema, holdout guard, case/source linkage and regression tests. |
| P1 source-lock owner | `nckh-kit/core/registry/source-lock/` | Quyền ghi/freeze revision/history, gồm baseline evaluator local-only của P1. Với resource candidate về sau, P3 gửi format contract + pins sau support/tests rồi P1 mới ghi lock; không freeze copied data từ staging P2 bằng nhãn local-only. |
| P1 evidence owner | `plans/evaluation/resource-quality/` | Immutable comparison manifest and receipts; không sửa `plans/evaluation/direct-skill-tests/`. |
| Existing contract owner | `nckh-kit/core/schema.py` | Chỉ review closed-schema delta; unknown keywords/fields vẫn fail. |

## Data flow và steps

1. Đọc catalog/source-lock/case manifests và runtime audit; tính lại hashes bằng existing helpers, ghi lane table và owner handoff.
2. Sau authorization thực thi, sửa validator/oracle contracts trước resource change; viết regression cho reject-route, family mapping, protocol keys, round/exposure limits và protected-holdout default. Không sửa development runner thành holdout runner.
3. Xác định resource candidate từ [resource-map.md](./resource-map.md); mỗi candidate phải có consumer và expected output trước khi có file.
4. Freeze candidate evaluator local-only nhất quán với source; giữ revision 18/history. P2 chỉ stage tài nguyên ngoài pinned source/dist. Sau P3 format/rights/closure support và content handoff, P1 nhận candidate pins để freeze `source → input → resource dependency → output artifact → verification receipt`; raw traces/holdout phải ở private store ngoài source/dist/agent workspace.
5. Gửi rights questions, reviewer/threshold questions và Nature full-SHA/license re-check sang P2/P4; không tự lấp unknown. Đọc lại lịch sử local-only qua contract tương thích do P3 sở hữu, không migrate/relabel lock lịch sử tại chỗ.

## Validation

Working directory: `C:/Users/USER/Downloads/test-skill/nckh-kit/`.

- Existing syntax (read-only structure): `python evals/run-evals.py --validate-only`.
- Existing focused suite: `python -m unittest tests.evidence.test_guards tests.release.test_qualification tests.build.test_closure`.
- Existing runtime-audit focused syntax: `python -m unittest tests.release.test_qualification tests.release.test_agent_runs tests.release.test_runner tests.build.test_closure`.
- Existing full deterministic entrypoint (only after an authorized implementation change): `python evals/run-evals.py --run-deterministic --output evals/results/resource-quality-local.json`.
- Current owner/tests: `python -m unittest tests.release.test_qualification` covers negative case, family/protocol and holdout guards. Resource source/hash/rights checks run through `registry`, `verify_source_lock` and shared bundle verification; direct linkage is an observed project evidence record with missing receipts retained. No additional nonexistent evaluator module or verifier command is claimed.

## Risk, rollback và success

- High: nhầm direct receipt thành source qualification hoặc để malformed oracle pass. Mitigation: lane/subject/hash + strict route/family/protocol guards; rollback candidate evaluator/manifest/source và lock đồng bộ, giữ history/receipts.
- High: nhập upstream mà chỉ đổi nhãn rights. Mitigation: fail closed khi thiếu full SHA/LICENSE/NOTICE/redistribution; không copy và không increment lock.
- Medium: repair validator làm case cũ fail ngoài scope. Mitigation: preserve all original manifests/results, add explicit migration receipt, stop before resource phase if failure is unexplained.
- Medium: resource map biến thành 37 manifest. Mitigation: một mapping trung tâm, identity không có consumer giữ MD-only.

P1 đã có freeze record đầy đủ hash/rights/status, negative/family/protocol/holdout regressions và validator giữ qualification pending; 37 IDs/148 cases/19 families/224 cells còn nguyên. Evidence đã kiểm được nối trong execution checkpoint. Các unknown và historical receipt bị thiếu vẫn pending; không có installation/provider/human run được suy ra từ việc hoàn tất P1.

## Rollback

Không restore/delete workspace. Nếu freeze hoặc validator repair sai, giữ report/failed receipt để audit và dừng phase sau. Owner hoàn nguyên đúng phần candidate source/contracts/tests kèm lock tương thích, hoặc tạo revision sửa lỗi có source/hash khớp; không restore lock revision 18 đơn độc lên source đã đổi, không xóa history. Chỉ tiếp tục khi cặp source + contract + lock được kiểm lại nhất quán.

## Execution checkpoint

Baseline 18/hash/snapshot được giữ. Evaluator freeze 19 khớp 46 members đã kiểm; 37 negative routes, 19 families và protocol được validate, protected helper bị chặn. Direct linkage có 158 review rows/148 IDs và giữ một answer thiếu. Candidate hiện revision 22. [Freeze](../evaluation/resource-quality/evaluator-freeze.json), [linkage](../evaluation/resource-quality/direct-linkage.json).
