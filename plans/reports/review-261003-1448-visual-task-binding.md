# Source review: visual task binding

Ngày: 2026-10-03 · Asia/Saigon · Project: `C:/Users/USER/Downloads/test-skill`.

## Kết quả

**Không phát hiện implementation finding chặn route trong tám file được giao.** Binding được cung cấp tường minh theo project/task/host, capability giới hạn `svg-render`; bundled default giữ unavailable/null. Helper chỉ kiểm integrity/matching, không execute engine, cấp quyền hoặc tạo native/scientific acceptance.

Correction hẹp cho câu docs cũ về measured chart data đã được maker sửa và reviewer kiểm lại; ghi delta riêng bên dưới. Review không sửa source, lock, installed skills, native artifacts hoặc runtime matrix. Current installed revision vẫn r24; fresh r25 freeze/build/install do controller sở hữu.

## Scope và source snapshot

| Source path dưới nckh-kit/ | SHA-256 đọc khi review |
|---|---|
| extensions/native-documents/contract.json | `3fe3be8522e319e68e1f5210e25d3993b1be25239e2c9d2ddc9c067efb5db9df` |
| core/contracts/extension.schema.json | `1e662a40066e8a75407465bc679af49fc187e824910c66a15631d7d5a84f38fb` |
| core/contracts/visual-engine-binding.schema.json | `6e90158950747dc2ea85777c69addec93a4f9b57d20f6199414e87ae864eea32` |
| scripts/check-visual-engine.py | `605f7434652d5110208291dfde5b782e6a6facbc3eefb16977d1c9595c6fb256` |
| skills/core/nckh-visuals/SKILL.md | `cf4ddad0701a379251eaa8083c871a8bd7bd6aa63d51e1affba52b8285a6e852` |
| skills/core/nckh-visuals/references/visual-acceptance.md | `8534b32f46de72461e7e195257abf7772cca26788c678da884f87e1ae442ce49` |
| docs/research-and-writing.md | `75b9d0064931d6f4cd5c5bf63690b4db00b552ff2366d196eecb557bf0332832` |
| tests/evidence/test_visual_engine_binding.py | `2ee860313fb0de9fd2b882ccac660a5cca898c6c54caac0f42e4ede1d69b406b` |

Đã đọc toàn bộ tám source files, helper's schema dependency hiện có và source closure/install behavior từ lượt scout. Những hashes này là source snapshot trước correction/freeze, không phải candidate r25 hash hoặc installed receipts.

## Verified decisions

1. **Portable defaults và scope.** [Contract](../../nckh-kit/extensions/native-documents/contract.json) giữ `status=unavailable`, `engine_binding=null`; optional route declaration chỉ `project-task`, `svg`, `svg-render`. [Extension schema](../../nckh-kit/core/contracts/extension.schema.json) đóng route fields. Providers khác không bị bắt thêm route.
2. **No ambient fallback.** [Skill](../../nckh-kit/skills/core/nckh-visuals/SKILL.md) yêu cầu explicit trusted task binding; invalid binding dừng, absent binding unavailable. JSON fields không cấp permission. Task pass không promote bundled/global status.
3. **Relocated root/dependencies.** [Checker](../../nckh-kit/scripts/check-visual-engine.py) resolve root từ `__file__`, load sibling `core/schema.py`; installed layout `_shared/scripts` có root `_shared` và sibling core/contracts/extensions. Skill links trực tiếp checker, validator, cả schemas và contract; closure test xác nhận đủ những dependencies này. Không dùng CWD hoặc PYTHONPATH để tìm source checkout.
4. **Closed integrity checks.** [Binding schema](../../nckh-kit/core/contracts/visual-engine-binding.schema.json) đóng record; checker từ chối unknown/duplicate keys, wrong scope/capability, executable hash drift, stale referenced bytes, version/log/exit/cleanup mismatch và render input/output command identity mismatch. Receipt command là argument array, không có helper shell execution.
5. **Project containment.** Observation references là canonical project-relative paths; resolved paths phải nằm trong project. Command SVG/PNG operands cũng được resolve và kiểm containment. `no_links` có symlink/junction checks khi Python hỗ trợ; fallback `Path.is_junction` trên Python cũ không được xem là chứng minh escape. Resolved member bounds vẫn từ chối outside-project references. Chưa có concrete junction escape được chứng minh trong review này.
6. **Evidence limits giữ đúng.** Result là `integrity-verified`, authorization not-established, acceptance pending-independent-gates. SVG root/PNG signature là integrity/type smoke, không decode/render QA hoặc authentic execution proof. Synthetic receipts/PNG test fixtures được ghi rõ là integrity fixtures. [Visual acceptance](../../nckh-kit/skills/core/nckh-visuals/references/visual-acceptance.md) giữ actual host observations và final artifact editability/render/source truth/accessibility/scientific gates riêng.

## Independent focused checks

CWD: `C:/Users/USER/Downloads/test-skill/nckh-kit`.

Đã chạy năm test cụ thể bằng `python -B -m unittest ... -v`:

- `test_default_extension_is_unavailable_and_route_is_closed`
- `test_project_task_and_host_mismatches_fail`
- `test_executable_missing_hash_drift_and_relative_path_fail`
- `test_receipt_input_output_hash_and_command_mismatches_fail`
- `test_extracted_checker_works_with_isolated_python_from_other_cwd`

Actual result: **5 tests passed**, exit 0, unittest elapsed **1.501 seconds**. Extracted checker positive/negative chạy qua isolated Python từ CWD khác, PYTHONPATH không dùng được, không tạo bytecode; negative scope trả unavailable/fallback false.

Maker/controller đã báo focused suite 15 pass/1 WinError1314 symlink-fixture skip và affected suite 24 pass. Các counts đó là evidence do maker/controller cung cấp; reviewer không chạy lại toàn suite. Reviewer cũng không gọi engine/model/provider/UI hoặc thực hiện actual package/install. Controller đã có actual rsvg probe/checker observation riêng; review này không biến nó thành World Bank final QA.

## Documentation correction — đã sửa và kiểm lại

**Vị trí:** [research-and-writing.md](../../nckh-kit/docs/research-and-writing.md), cuối đoạn Selected resources, khoảng dòng 56–57.

Câu “None supplies ... measured chart data” được giữ từ docs cũ nhưng phạm vi hiện tại có actual dated World Bank population pack từ r24. [Resource rights contract](../../nckh-kit/docs/contracts.md) đã phân biệt time-series measurement input với visual-acceptance result. Correction tối thiểu: tách bốn original reference snapshots khỏi năm real sample packs; ghi World Bank pack cung cấp dated measurements, còn corpus/human/native/scientific acceptance chưa được dữ liệu đó tạo ra. Không cần lặp resource/source audit hoặc đổi measurements.

Maker đã sửa đúng owning paragraph: tách optional reference snapshots khỏi năm actual-source packs, ghi World Bank có dated published observations/observed chart values cùng snapshot/hash/blank-unit caveat; corpus/human/scientific/final visual gates giữ riêng. Reviewer đã đọc lại đoạn thực và tính SHA-256 khớp **`b91a067fbdd193cd5e23be2604f61b58d16965640adccbf43b30afef01c9f919`**. Đây là final docs delta so với pre-correction snapshot trong bảng; bảy source files còn lại không có delta mới theo controller. Không chạy lại checker suite cho correction docs này. Source review đã sẵn sàng cho controller freeze r25; không có correction source còn chờ trong phạm vi review.

## Remaining acceptance

- Fresh freeze r25, revision-bound build/extracted verification và owned install/doctor thuộc controller; documentation correction đã đóng.
- Native host phải dùng explicit binding và renderer trong authority hiện hành; helper integrity pass không chứng minh native host execution.
- World Bank vẫn cần final editable SVG, source-to-mark, actual open/edit/save/reopen/render, accessibility, final hash-bound QA; probe không đóng case này.
- Cursor chỉ Grok 4.7 Extra High, Antigravity Gemini 3.8 Flash High, current app chỉ GPT-6.1 Sol; no fallback.
- Owner scores sau personal use vẫn pending; không global host/stable/scientific certification.

Status: DONE

Summary: Public portable contracts, scoped integrity route và relocation dependency closure đã được review; năm focused checks độc lập đạt, correction docs đã được kiểm lại. Không có blocking implementation finding hoặc source correction còn chờ.

Concerns/Blockers: Không có blocker trong source review. Actual native final-artifact QA và revision-bound package/install gates vẫn do controller hoàn tất; không được source review này xác nhận.
