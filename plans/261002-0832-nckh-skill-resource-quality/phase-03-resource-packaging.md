---
title: "Phase 3: Resource packaging"
status: completed
---

# Phase 3: Resource packaging

## Overview

<!-- Historical plan amendments: R1/R7/R10, 2026-10-02; execution authorized 2026-10-02 -->

Nhận staged packet của P2, bổ sung versioned source-lock/build/bundle rights contract và closure support trước khi promote tài nguyên. Sau support/regression, P2 owner đưa đúng content đã duyệt vào candidate source, P1 ghi freeze/history, rồi P3 mới chạy candidate build/extracted smoke. Không copy-all hay tạo orchestration framework. Build/bundle format 2 đã hỗ trợ registry/rights/explicit closure; format 1 local-only vẫn đọc đúng nghĩa lịch sử. Resource-off giữ reader/registry chung, bỏ copied bytes. Candidate và extracted checks có receipt riêng, không kế thừa lịch sử.

## Baseline revision 18 trước thay đổi

- `nckh-kit/core/build.py:39-50` inventory không gồm `.csv/.jsonl/.svg`; `:53-88` freeze/verify lock; `:91-99` chỉ chấp nhận record `owned-local-package` và `copied_third_party_content=false`.
- `nckh-kit/core/build.py:102-138` `closure()` chỉ theo local Markdown links; import/script/data dependency không tự vào closure.
- `nckh-kit/core/build.py:168-241` build materializes selected skill closure và từ chối unpinned/secret files; `:300-330` bundle verify hash/rights/source provenance và actual file set.
- `nckh-kit/core/build.py:264-289` plugin fields không được dùng để claim runtime state. `nckh-kit/docs/installation.md:17-21,84-109` yêu cầu output rỗng, closure/hash/OS distinction và không suy native từ fixture.
- `nckh-kit/installer/schemas/bundle.schema.json:3-6,54` đóng unknown fields, cố định schema version 1 và rights `owned-local-package`. `core/install.py:61-76,124,275-294` có `resolve_targets`, `plan_install`, `refresh_targets` dùng kết quả shared verifier/tree hashes; thêm resource/provenance phải giữ contract cho cả ba consumer.

## Concrete design

- [x] Thêm **một** resource registry/catalog extension, ưu tiên `nckh-kit/core/registry/catalog/resources.json` (hoặc field tương đương trong catalog nếu schema hiện hữu mở rộng được), không tạo 37 manifest. Mỗi record có ID, consumer skill IDs, relative path, format, `requires`, reader/entrypoint, source kind, version/full SHA, rights contract, release state và expected artifact.
- [x] `resources.json` chỉ liệt kê resource đã được P2 chọn; resource không có consumer không vào source inventory. `required` closure và `optional` preview phải phân biệt; private holdout/receipts không được package.
- [x] Sửa `source_members`/freeze/verify/materializer và closed bundle schema theo format version được khai báo để lấy data từ registry bằng allowlist; không blanket-enable CSV/JSONL/SVG. Phân biệt local re-authored với copied-upstream, giữ full-SHA/source path/license/NOTICE/redistribution disposition; thiếu quyền thì `blocked-rights`. Giữ reader tương thích historical local-only records, không relabel bytes hay viết lại lock cũ.
- [x] Sửa `closure`/materializer để theo `requires` explicit và Markdown links, kiểm tra cycle/path escape/duplicate mapping, pin every member và ghi `resource_id → consumer → output` vào manifest. Reuse `contained`, `no_links`, `unique_paths`, `digest_file`, `digest_record`; không tạo framework mới.
- [x] Thêm extracted-package smoke harness: extract vào thư mục tạm ngoài repo, CWD khác repo, `PYTHONPATH` unset; gọi consumer bằng absolute package path hoặc `python -I`. Smoke phải chứng minh reader thực sự đọc resource, không chỉ file tồn tại.
- [x] Giữ `verify_bundle` là verifier chung; thêm regression cho `resolve_targets`, `refresh_targets`, `plan_install` với bundle/tree và rights đúng/sai. Sau support/tests mới promote P2 content và gửi candidate pins để P1 ghi freeze/revision/history; P3 chỉ sở hữu format contract, không ghi lock hay dựng receipt/approval engine riêng cho từng caller.

## Format và rights compatibility

- Version source-lock/build/bundle contract đồng bộ khi thêm provenance/resource fields; giữ closed-schema validation ở từng phiên bản, không nới arbitrary fields để qua test. Legacy v1 local-only được đọc và verify đúng nghĩa gốc; phiên bản mới mô tả copied-upstream đúng nguồn/quyền, không ép thành `owned-local-package`/`copied_third_party_content=false`.
- Freeze routine/format logic trong `core/build.py` thuộc P3; thao tác ghi `core/registry/source-lock/` và archive revision/history thuộc P1. Candidate packet gồm hashes, resource/source IDs, license/NOTICE/redistribution disposition và schema version; pin không tự cấp quyền sử dụng/release.
- Một shared `verify_bundle` phải kiểm source provenance, closure, file hashes/rights và định dạng. Installer consumers tái dùng verifier/tree hashes; không sao chép quyền phê duyệt thành ba engine mới. Test unknown fields/version, rights thiếu/sai, old local-only read và candidate copied-content round trip.

## File ownership

| Owner | Exact paths | Responsibility |
|---|---|---|
| P3 registry/contract | `nckh-kit/core/registry/catalog/resources.json`; `nckh-kit/core/contracts/`; `nckh-kit/installer/schemas/bundle-v2.schema.json`; existing `bundle.schema.json` | Resource/rights/source-lock and bundle format versioning; closed-schema backward reading for local-only records. Existing shared schema validator was reused. |
| P3 build | `nckh-kit/core/build.py`; `nckh-kit/core/paths.py` only if existing guard needs it | Allowlisted inventory, freeze format logic, explicit closure, materializer/provenance/shared verifier and extracted smoke path; no source-lock write ownership. |
| P3 installer integration | `nckh-kit/core/install.py` only if compatibility requires; `nckh-kit/tests/installer/test_entrypoints.py`; `nckh-kit/tests/installer/test_transactions.py` | Regress `resolve_targets`, `refresh_targets`, `plan_install` through shared verification/tree hashing, not per-caller approval engines. |
| P3 tests | `nckh-kit/tests/build/test_closure.py`; `nckh-kit/tests/contracts/test_state.py`; `nckh-kit/tests/resource/` | Legacy/new-version, copied-rights, cycle/escape/private-exclusion/unlisted-data/tamper/reproducibility/CWD isolation tests. |
| P2 promotion handoff | Reviewed staging → selected future targets listed in P2 | P2 content owner promotes exact reviewed bytes only after P3 support/tests; no concurrent content edits. |
| P1 freeze handoff | `nckh-kit/core/registry/source-lock/` | P1 alone writes freeze/revision/history from compatible candidate source/schema/pins; preserve old immutable locks. |

## Data flow and failure modes

P2 staged decision/rights packet → P3 format/closure support and regression → P2 owner promotes reviewed content → P1 source-lock freeze → host bundle manifest → shared verifier/installer-consumer checks → extracted consumer smoke → receipt. A missing reader, undeclared dependency, unsupported suffix, hash drift, license gap, private path, cycle or CWD/PYTHONPATH leak fails closed. Keep rejected staged bytes/failed receipts for rework; do not freeze false local-only rights to bypass a missing feature. Successful bundle/hash checks remain integrity evidence only.

## Validation

- Existing candidate build syntax, **only after support/promotion/P1 freeze**: from `nckh-kit`, `python scripts/build-artifacts.py --all --check`, `python scripts/build-artifacts.py --all --plugin --check`. Pin the candidate source/schema/lock subject of each run.
- Existing deterministic syntax: `python evals/run-evals.py --run-deterministic --output evals/results/resource-packaging-local.json`.
- Existing focused tests: `python -m unittest tests.build.test_closure tests.contracts.test_state tests.installer.test_entrypoints tests.installer.test_transactions tests.release.test_qualification`; owning tests cover the new contract in the retained full suite. No real skill installation was performed.
- Implemented: `python -I scripts/resource-smoke.py --bundle EXTRACTED --cwd OUTSIDE_REPO --unset-pythonpath --output RECEIPT` and `python -m unittest tests.resource.test_closure tests.resource.test_extracted_smoke`; actual relocated reader runs with isolation and retained read hashes. Failed revision 21 and corrective freeze remain separate records.

## Risk, rollback và measurable success

- High: package succeeds while consumer cannot read data outside repo. Mitigate with `python -I`, empty external CWD, unset `PYTHONPATH`, and a read-observed receipt; stop promotion and retain failed receipt/staged packet/old bundle.
- High: source-lock revision mislabels imported content or schema becomes incompatible. Mitigate versioned rights contract, shared verifier and P1 write handoff. Roll back candidate source + format/schema + lock as a coherent unit, or freeze a verified corrective revision; never restore an old lock alone onto changed source or erase history.
- Medium: optional dependency silently omitted or duplicated across plugin projection. Mitigate explicit `required/optional`, unique mapping, plugin byte equality and reproducibility tests.

Done means legacy local-only records remain readable without rewrite; new copied-content rights/provenance pass the declared closed schema and shared verifier; all three installer consumers retain verified behavior; P1 freezes coherent candidate pins; two empty-destination builds are byte-identical for each selected host; every selected resource is actually read in extracted smoke; unlisted data/private paths/missing rights fail closed. No runtime/plugin/native qualification or release authority is claimed.

## Execution checkpoint

Format 2, shared verifier và installer-consumer regressions đã triển khai. Revision 21 có một off-closure failure do attribution link; snapshot và failure được giữ, sửa reader/registry closure ở revision 22. Full suite, hai lần build cho từng host/mode và extracted smoke đã pass theo receipts. Không cài skill hoặc chứng nhận native/plugin/OS.
