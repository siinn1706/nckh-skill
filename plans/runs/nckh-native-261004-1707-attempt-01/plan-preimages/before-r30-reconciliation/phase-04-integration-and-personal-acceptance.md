---
title: "Phase 4: closure, source lock và acceptance lanes"
status: in-progress
---

# Phase 4: closure, source lock và acceptance lanes

## Outcome và data flow

P1–P3 artifacts/receipts → exact catalog/profile/eval/resource invariants → source-lock/history và four-host on/off/plugin bundles → read-only doctor/dry-run → user-approved install/trust/native receipts → separate personal-use feedback hoặc stable/scientific gates. Mọi descendant hash đổi phải stale; không biến pass cấu trúc thành acceptance.

## Điều kiện và invariants

- [x] P1 quyết định hai writer có `--en`/`--vi`, exact 39 = baseline 37 ∪ hai writer; không “nới” validator. Candidate đúng 156 base IDs (148 cũ + 8 mới), giữ 19 families; supplemental writer/visual/hook cases tách riêng. Historical 224 matrix/receipts và historical 37/148 comparator giữ nguyên; locale không là identity mới.
- [x] Source r26 (243 pins) và installed candidate r25 (chỉ bốn pin khác: `pmc-rights.md`, `wikisource-rights.md`, `worldbank-rights.md`, `resources.json`) được ghi là hai revisions; không auto-sync. Chỉ một owner được freeze/revision source-lock ở phase này sau approval.
- [x] Build/resource closure kiểm 9 resources, on/off standalone và plugin packaging cho Claude/Codex/Cursor/AGY; unsupported surface/version là pending/unverified, không thu hẹp target để đóng gate và không claim parity.
- [x] Personal-use owner đọc/dùng artifact rồi feedback gắn revision/artifact/input hashes; thiếu feedback là `pending-personal-review`, không cần external reviewer/protected holdout. Stable/scientific lane giữ rights, reviewer, rubric, threshold, economics riêng.

## File ownership (absolute paths)

Existing:

- `C:/Users/USER\Downloads\test-skill\nckh-kit\core\registry\source-lock\source-lock.json:1376-1380`, `C:/Users/USER\Downloads\test-skill\nckh-kit\core\registry\source-lock\history\` và `C:/Users/USER\Downloads\test-skill\nckh-kit\scripts\freeze-source-lock.py` — single-owner freeze, archive previous lock, no invented commit/SHA.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\core\build.py:166-190,193-336,344-494`, `C:/Users/USER\Downloads\test-skill\nckh-kit\scripts\build-artifacts.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\installer\schemas\bundle-v2.schema.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\build\test_closure.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\resource\test_closure.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\scripts\resource-smoke.py` — integrate P1/P3 exact membership, hook/resource closure, extracted readers và plugin/on-off behavior; schemas v1/history không đổi.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\core\evaluation.py:72-124`, `C:/Users/USER\Downloads\test-skill\nckh-kit\core\acceptance.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\core\contracts\catalog.schema.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\evals\run-evals.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\evals\cases\required-families.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\release\test_qualification.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\acceptance\test_profile.py` — exact 39/156 checks; `validate_cases` bắt buộc gọi P1 `validate_writer_matrix`. `C:/Users/USER\Downloads\test-skill\nckh-kit\evals\cases\runtime\invocation-matrix.json` và `C:/Users/USER\Downloads\test-skill\nckh-kit\scripts\compare-matched.py` [PRESERVE] giữ 224 và historical 37/148, không search-replace.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\core\registry\compatibility\matrix.json:1-90`, `C:/Users/USER\Downloads\test-skill\nckh-kit\adapters\claude\adapter.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\adapters\codex\adapter.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\adapters\cursor\adapter.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\adapters\agy\adapter.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\core\install.py:124-254,554-642,714-791`, `C:/Users/USER\Downloads\test-skill\nckh-kit\docs\installation.md:46-132` — four-host projections, dry-run, ownership, backups/conflicts/rollback and doctor.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\docs\personal-use.md:12-35,47-72`, `C:/Users/USER\Downloads\test-skill\nckh-kit\docs\qualification.md:3-27,149-165`, `C:/Users/USER\Downloads\test-skill\nckh-kit\docs\research-and-writing.md:41-64` — acceptance-lane and non-claim wording.

New:

- `C:/Users/USER\Downloads\test-skill\nckh-kit\evals\cases\runtime\writer-invocation-matrix.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\core\contracts\writer-invocation-matrix.schema.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\release\test_writer_matrix.py` [NEW IN P1, integrate P4] — mandatory exact matrix/schema/oracles; data validator được gọi tự động bởi existing `--validate-only`, không có future flag mồ côi.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\hooks\test_config.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\hooks\test_closure.py` [NEW IN P3, integrate P4] — mandatory config lifecycle và package smoke. `C:/Users/USER\Downloads\test-skill\nckh-kit\docs\installation.md`/`C:/Users/USER\Downloads\test-skill\nckh-kit\docs\qualification.md` [MODIFY] cho user-visible commands/state changes; không thêm một rollback suite trùng owner.
- User project `.nckh-state\ownership.json` and `.agents\`/`.codex\` are [TARGET ONLY AFTER APPROVAL], never edited in this plan turn; preserve shared Codex+AGY `.agents` and user config.

## Tasks

- [x] Re-run read-only source/installed baseline and compare hashes before implementation; attach r26/r25 reconciliation record and preserve prior failed receipts.
- [x] Reconcile toàn bộ P1 candidate consumers: catalog schema, build select, evaluation, acceptance validator/profile và tests phải exact 39/156. Đối chiếu frozen baseline ID set, không chỉ count; giữ 19 families/5 rubrics và historical protocol/comparator/matrix. Đổi content current cases phải ghi new revision/receipt, không regrade historical 148 evidence.
- [x] Hoàn tất integration/schema/docs/test code trước freeze. Một owner P4 chạy `freeze-source-lock.py` sau review source/rights, lưu previous lock rồi mới full validate/build. Nếu kiểm tra fail và phải sửa pinned bytes, giữ failure receipt, invalidate outputs và freeze candidate revision kế tiếp bởi cùng owner; không rewrite history, không ép “chỉ freeze một lần” khi code đã đổi.
- [x] Build each host with resources on/off and plugin flag, extract outside repository, run standalone resource smoke, and verify selected writer/visual reads with exact source/license/lineage hashes. Mark static/deterministic only.
- [x] Nối writer matrix của P1 vào `core/evaluation.py::validate_cases` và summary; bắt buộc schema/exact IDs/route/surface/receipt/no-side-effect oracles. Giữ old 224 matrix/history, output locale khác resource locale và router giữ flags. Generated TOML/frontmatter/hash không được tự đổi `not-run`/`not-callable` thành native PASS.
- [x] Run narrow tests before full deterministic suite; then four-host packaging and installer preview. Only with explicit user grant run approved disposable native discovery/invocation/trust; record requested/resolved/effective settings separately.
- [x] Exercise skill install/update và hook config thành hai transaction riêng: explicit extracted `--package`, skill dry-run; hook preview/apply/remove qua P3 owner chỉ trong isolated tests hoặc grant thật. Test changed-after-preview, edited/shared target, invalid JSON, partial failure và rollback-conflict; không auto-enable/trust hoặc trộn quyền hai installer.
- [x] Collect personal-use owner feedback only after usable artifact; keep external reviewer/holdout/stable/scientific decisions as independent pending gates.

## Checkpoint sequence và output chain

Tất cả lệnh ở đây dành cho implementation được cấp quyền, không chạy ở lượt plan. Cwd source là `C:/Users/USER\Downloads\test-skill\nckh-kit`. Pre-edit baseline có thể dùng full validator với lock r26; sau edit chỉ focused suites của P1–P3. Sau P4 freeze mới chạy full validator, build/closure suites và integrated deterministic evaluation.

1. Trước run, tạo attempt mới không đè dữ liệu: `RUN` là absolute owned directory mới trong `C:/Users/USER\Downloads\test-skill\plans\runs\nckh-writing-hooks-<attempt>`; `OUTSIDE` là fresh temp directory tạo bằng `New-Item`, resolve ra ngoài workspace, gồm `extracted/`, `cwd/`, `project/`. Ghi tất cả expanded absolute paths, source revision/hash và ownership vào run receipt trước build. Các placeholder chỉ mô tả path contract, phải resolve trước khi chạy.
2. Sau freeze: `python -B evals/run-evals.py --validate-only --output RUN/validate.json`; focused new suites gồm `tests.resource.test_writer_consumers`, `tests.release.test_writer_matrix`, `tests.evidence.test_visual_purpose`, `tests.hooks.test_policy`, `tests.hooks.test_runner`, `tests.hooks.test_config`, `tests.hooks.test_closure`, `tests.runtime.test_hook_adapters`; rồi `python -B evals/run-evals.py --run-deterministic --output RUN/deterministic.json`. Không dùng lại `evals/results/local-checks.json`; retry dùng attempt mới, không xóa fail/timeout receipts.
3. Reproducibility: `python -B scripts/build-artifacts.py --all --resource-access on --check` và tương ứng `off`, có/không `--plugin`. Đây là staging dùng một lần, không phải nguồn cho install.
4. Persistent builds: `python -B scripts/build-artifacts.py --all --resource-access on --output RUN/build/on-standalone`; đổi `on`→`off` và thêm `--plugin` cho `RUN/build/on-plugin`, `RUN/build/off-plugin` (đủ 16 host/variant outputs). Mỗi directory ban đầu rỗng; actual host bundle là `RUN/build/<variant>/<host>/manifest.json`, không phải `dist` hoặc check staging.
5. Tạo archive từng host tree bằng `Compress-Archive`, expand bằng `Expand-Archive` vào `OUTSIDE/extracted/<variant>/<host>` rỗng. Kiểm manifest ở ngay extraction root, no-links/containment và `verify_bundle` sau extract. Archive path `RUN/archives/<variant>-<host>.zip`; receipts dưới `RUN/receipts/<variant>-<host>/`, không tái dùng output cũ. Ghi archive hash, bundle closure hash, extraction root và outside CWD trước smoke; không sửa file để làm verification pass.
6. `python -I scripts/resource-smoke.py --bundle OUTSIDE/extracted/<variant>/<host> --cwd OUTSIDE/cwd --unset-pythonpath --output RUN/receipts/<variant>-<host>/resource-smoke.json`; với resource-on phải đọc đúng toàn bộ consumer/resource pairs của P1. Resource-off cần thêm direct packaged-reader tests cho từng writer trả disabled/no-read; zero-observation smoke riêng nó chưa chứng minh không đọc. `tests.hooks.test_closure` gọi runner/manual checker đã extract bằng Python `-I` từ cùng outside CWD, bỏ PYTHONPATH, kiểm dependent imports/template/schema và missing-member/tamper fail. Plugin inactive projection được kiểm riêng, không cần đăng ký để chứng minh package closure.
7. Skill preview full-kit cụ thể: `python -B installer/nckh-installer.py install --package OUTSIDE/extracted/on-standalone/codex --runtime codex-cli --scope project --project OUTSIDE/project --kits core engineer marketing --mode copy --models balanced --dry-run`. Lặp host/surface theo compatibility matrix với đúng extracted host bundle. Preview phải chỉ đúng proposed targets và không viết project; không bỏ `--package`. `doctor --state-dir STATE` chỉ sau tồn tại installed state được cấp quyền, không giả dry-run đã cài.
8. Hook payload/config preview lấy đúng verified extracted package qua P3 CLI; apply/remove/native observation chỉ sau grant tương ứng. State report phân biệt packaged/registered/enabled/trusted/native-verified. Cleanup chỉ owned attempt paths/processes, lưu receipts trước; không tự dọn project/global của người dùng.

Existing CLI syntax đối chiếu `scripts/build-artifacts.py`, `evals/run-evals.py`, `scripts/resource-smoke.py`, `installer/nckh-installer.py`; các test/CLI hook mới có owner P3, matrix được integrate thay vì thêm flag. No test/build/hash may close human, scientific, native or rights gates.

## Risk và rollback

Risk: source/install drift or accidental lock overwrite (L3×I5=15); single owner, lock history and pre/post hash reconciliation. Risk: shared config/visibility collision (L4×I5=20); dry-run, owned blocks, conflict stop, preserved edits and installer transaction journal. Risk: unsupported host falsely promoted (L3×I5=15); per-surface receipts and honest pending state. Risk: owner feedback conflated with stable science (L3×I4=12); separate lane records and rubric/threshold gates.

Rollback after authorized mutation: skill files dùng `core/install.py` transaction/backup; hook payload/config dùng P3 `core/hook_config.py` remove/rollback contract. Cả hai chỉ sửa phần owned còn đúng hashes, giữ later edits và báo `rollback-conflict` khi lệch. Revert owned source/catalog/docs/manifest changes theo revision tương thích và retain history/failed receipts; không xóa old 37/148/224 evidence hoặc overwrite global/shared configs.

## Measurable exit

Exact 39 contract/profile/build/eval checks pass với đúng 156 base cases và supplemental writer matrix được validate; historical 148 IDs/224 cells/receipts nguyên vẹn. Nine-resource + hooks on/off/plugin bundles có scoped extracted receipts, explicit installer package chain, single freeze owner và rollback giữ user edits. Personal-use/native/scientific/rights statuses trung thực, không đòi tất cả đều pass để ghi technical checkpoint. Technical execution r29 đã hoàn tất theo cook grant; native/trust và owner feedback vẫn cần grant/evidence riêng.

<!-- Updated: Validation Session 2 - approved A1 A2 A3 A4 A5 A6 A7 A9; plan-only -->

## Execution checkpoint — r29

Delivery record (historical evidence path: `../reports/delivery-261004-1037-r29-local-candidate.md`; unavailable in the cleaned checkout): 281 pins, 181 deterministic tests (`OK`, một symlink skip), 16 persistent ZIP/extracted bundles, 216 resource reads, 48 writer disabled/no-read observations, 24 hook projections và 8 installer previews (39 skills + 6 agents). Preservation (historical evidence path: `../runs/nckh-writing-hooks-261004-1037-attempt-03/final-preservation.json`; unavailable in the cleaned checkout) giữ 509 protected hashes và installed r25; bốn legacy schema-v1 bundles vẫn verify được. r27/r28 failures và source-lock history được giữ; r29 delta review (historical evidence path: `../reports/review-261004-1037-r29-source.md`; unavailable in the cleaned checkout) riêng với snapshot review trước freeze. Hai owner-feedback checkboxes chưa có evidence nên giữ unchecked. Supplemental writer matrix 256/20 và historical 224 cells vẫn không có native pass được tạo bởi local checks.
