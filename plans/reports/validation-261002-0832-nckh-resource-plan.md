# Validation record — NCKH resource plan

Ngày: 02/10/2026, Asia/Saigon. [Plan subject](../261002-0832-nckh-skill-resource-quality/plan.md). Trạng thái: **bảy amendments đã được duyệt và áp dụng vào plan; thực thi vẫn pending, không suy readiness từ cấu trúc**.

## Kiểm tra tại lượt review trước duyệt (lịch sử)

Các kết quả trong mục này là snapshot trước amendments, không phải số đếm sau chỉnh sửa. Follow-up hiện tại được ghi riêng bên dưới.

- `ak plan validate plans/261002-0832-nckh-skill-resource-quality --json --no-interactive`: `valid: true`, exit 0.
- `ak plan parse ... --json --no-interactive`: 4 phase files, 29 phase tasks, 0 complete, plan pending. Các acceptance checkboxes ở index không được parser cộng vào 29 phase tasks.
- Resource-map parse: 37 rows, 37 unique IDs, exact set match với `nckh-kit/core/registry/catalog/skills.json`; không thiếu/thêm identity.
- Đọc đủ sáu Markdown của plan. Kiểm tra cuối sau khi thêm red-team/validation: 11 documents (6 plan + 4 report chính + 1 journal), 30 local links, 0 broken; plan index 56 dòng. Ba research/runtime reports còn lại đã được kiểm trong lượt trước. Link checks chỉ chứng minh đường dẫn tồn tại.
- Source package validation cuối: `python evals/run-evals.py --validate-only`, exit 0. Canonical source-lock hash `f52a03676b29fbd5434673a0f831dcae397fe879131beec00f35d3ca9b4d472d`; 184 pins, 37 identities, 148 package cases, 19 families, 224 native cells, qualification pending. Đây là structure check với những giới hạn validator đã nêu trong audit, không phải toàn bộ eval integrity hay quality proof.
- Controller narrow suite trong lượt review: `tests.evidence.test_guards`, `tests.release.test_qualification`, `tests.build.test_closure`: 19 tests pass (32.574s). Runtime reviewer chạy bộ 19 tests có phần giao nhau; không cộng thành 38 tests độc lập.
- AgentKit body lint: 44 Markdown, zero heuristic findings. `quick_validate.py` chưa chạy được vì thiếu PyYAML (exit 1); routing-aware lint chưa verified. Không cài dependency để che limitation.
- Local plan index được reindex bằng `AGENTKIT_HOME` project-local; không đổi cấu hình người dùng. Không có native task-management capability phù hợp; phase files là authority, không claim live task hydration.
- Local journal được tạo và `ak journal validate` trả `ok: true`; AgentWiki publish skipped.
- Orphan check bằng read-only process inspection: không thấy process python/node/codex có command line chứa test-skill. Không có background process mới cần giữ hoặc dừng. Không suy ra mọi tiến trình trên máy đều sạch.

## Integrity không đổi

Các SHA-256 bytes cuối khớp snapshot đầu review:

| File | SHA-256 |
|---|---|
| `.agents/.nckh-install.lock` | `6F16F785061C96AEF94A4599DB7F5FA52D75E208F321AF683D23D94A07A37CCA` |
| `.nckh-state/ownership.json` | `DA9DEDCA9668F657EB7FB053E2AD44ECF34A12F086EAEB52077D14DDAF543ACF` |
| `nckh-kit/core/registry/source-lock/source-lock.json` | `74932B56FD0F58360D2F7CB5FACD85711126F1453D9A8BF26314E336186BC5B2` |

Canonical source-lock hash và raw file hash là hai phép hash khác nhau, không được so như cùng một giá trị. Source-lock verification kiểm tất cả 184 pinned files. Không sửa source, installed skills, corpus/receipt lịch sử; không clone, import dataset, chạy provider/native, triển khai hay publish. Mọi artifact mới của lượt này là review/plan/validation/journal và local index.

## Chất lượng và gate còn mở

- Direct development là bằng chứng thật riêng: first 137/4/7, latest 147/1/0 trên installed revision 14, exposed synthetic cases, controller review. Không human gold, holdout, blind routing, matched baseline hay qualification revision 18.
- Dataset mới không được tự bịa; sources/records của shortlist đã được đọc, pin/hash khi báo cụ thể, nhưng per-file reuse rights, domain selection và VI/EN corpus/reviewer chưa được đóng.
- [Red-team record](red-team-261002-0832-nckh-resource-plan.md): R1/R2/R4/R5/R6/R7/R10 đã được duyệt và áp dụng vào plan; R3/R8/R9 vẫn Reject. Review/plan approval không tạo authority triển khai.
- Sequencing, closed bundle rights/schema, same-base design và route limits đã được mô tả lại; code behavior tương ứng **chưa sửa/chưa chứng minh**. Không che pending implementation bằng `valid: true`.

## Follow-up sau phê duyệt — 02/10/2026

- Authority: câu trả lời “duyệt” chỉ cho bảy plan amendments. Đã sửa sáu plan files cùng trạng thái red-team/validation/journal; không sửa skill/source/install/corpus/history, không import dữ liệu, gọi provider hay cook.
- Decision deltas: R1 rights/versioned schema/shared verifier; R2 same-base off/on và baseline mappings; R4 900-second per-case route; R5 development-only/3-round/1-holdout/exposure; R6 bốn resource-to-consumer decisions và VI/EN gap; R7 current plan-only/future source changes/coherent rollback; R10 P2 staging → P3 support/promotion/P1 freeze/build.
- Whole-plan read: đọc lại index, cả 4 phase và resource map sau amendments; 7 decision deltas và 7 nhóm chi tiết cũ đã đối chiếu, 0 mâu thuẫn chưa giải quyết trong phạm vi được duyệt. Search các mẫu approval/phase prohibition/old comparison/old rollback/P2 candidate-build không còn stale hits; historical review quotes được giữ và ghi rõ là trước chỉnh sửa.
- `ak plan validate ... --json --no-interactive`: `valid: true`, exit 0. `ak plan parse ... --json --no-interactive`: 4 phases, 29 phase tasks (9/7/6/7), 0 complete, status pending. Index vẫn 61 dòng; acceptance checkboxes ở index không nằm trong 29 task.
- Resource matrix: 37 numbered rows, 37 unique IDs, exact catalog set match, 0 thiếu/thừa; bảng phụ có 4 candidate decisions. Đây là mapping thiết kế, không phải 4 tài nguyên đã import.
- Local-link check mở rộng: 14 documents (6 plan + 7 reports + 1 journal), 35 local links, 1 local heading anchor, 0 broken. Chỉ kiểm tồn tại path/anchor; không dùng làm xác nhận semantic quality hay quyền upstream.
- Re-ran `python -B evals/run-evals.py --validate-only`: exit 0, static pass, source revision 18 canonical hash vẫn `f52a03676b29fbd5434673a0f831dcae397fe879131beec00f35d3ca9b4d472d`, 184 pinned files; 37 identities/148 cases/19 families/224 native cells giữ nguyên, agent/native not-run và qualification pending. Không chạy lại unit suite, build, consumer, provider hoặc human evaluation trong lượt sửa tài liệu.
- Raw SHA-256 của ba file trong bảng integrity đã kiểm lại sau edits và **khớp snapshot**; direct corpus SHA-256 vẫn `bbb6d312df45c4bad75bef5b5e8b5a42202dfcf0122382ee59e51ce84c63de84`. Không sửa direct corpus/history.
- Project-local reindex `--apply` nhận đúng plan `test-skill/261002-0832`, 4 phases; `.agentkit-state`/`evaluation` được báo không phải plan, journals/reports là reserved directories, không tạo plan giả. Chỉ dùng `AGENTKIT_HOME` workspace-local, không đổi global configuration. Không có native task-management surface phù hợp; 29 checkboxes trong phase files vẫn là authority.
- `ak journal validate 2026-10-02-nckh-resource-review-and-source-backed-plan --json --no-interactive`: `ok: true`, exit 0; existing journal được bổ sung follow-up có ngày, giữ review history. AgentWiki publish skipped.
- Process reconciliation: sandbox CIM read bị từ chối; read-only check được duyệt đã chạy lại, không thấy process node/python/pythonw/uvicorn/pwsh/powershell có command line gắn test-skill. Không có process nền mới được khởi động hoặc dừng; đây không phải chứng nhận toàn bộ máy không còn process.
- Các giới hạn trước đó vẫn giữ: PyYAML quick validator chưa callable và không cài dependency; unit-test results trong mục lịch sử không được coi là test vừa chạy lại. Plan validation và 184-pin integrity không khắc phục những lỗi evaluator đang lên kế hoạch.

## Handoff

Bảy điểm đã được duyệt ở mức tài liệu, không cần xin duyệt lại cùng amendments. Chỉ thực thi sau yêu cầu riêng của người dùng và quyền cho gate tương ứng; không tự chạy cook, import, provider hoặc goal/autoresearch loop. Corpus, reviewers, per-file rights, native/runtime và protected holdout chưa được đóng bởi lượt này.
