# Amendment: visual binding theo project/task

Ngày: 2026-10-03 · Múi giờ: Asia/Saigon · Project: `C:/Users/USER/Downloads/test-skill`.

## Quyết định và trạng thái

Người dùng đã tiếp tục mục tiêu và giữ quyền cook trong project. Scope model hiện tại: **Cursor chỉ Grok 4.7 Extra High**, **Antigravity Gemini 3.8 Flash High**, **current app chỉ GPT-6.1 Sol**; không fallback. Tám current-app model khác excluded theo user; failures batch cũ được giữ, không còn yêu cầu xin chạy cả batch.

Installed candidate hiện vẫn **r24**. Original source/data/output/receipts của r24 giữ làm lịch sử bất biến. Maker đang triển khai support cho **explicit binding theo project/task**; controller đã quan sát source checker trả integrity-verified với actual rsvg probe 02. Source review và maker tests chưa được report này gọi là hoàn tất; kế hoạch tiếp theo là fresh freeze **r25**, build/verify, preview và owned installation. Chưa có r25 installed acceptance.

Không tạo full executor. Native host thực hiện công việc SVG và gọi engine được phép; checker chỉ kiểm contract, scope và actual referenced hashes. Package portable không chứa local Windows executable path hoặc observation receipt, không tự certify host và không promote mọi extension thành observed.

## Vì sao cần amendment

Installed r24 native-documents contract có `status=unavailable`, `engine_binding=null`. Skill/reference hiện yêu cầu available verified binding để tạo, mở và chứng minh SVG editable. Cả hai IDE đã giữ blocker memo đúng với nhánh unavailable; việc đó chưa hoàn tất output contract của World Bank.

[Cursor review](review-261003-1423-cursor-r24-outputs.md) và [Antigravity review](review-261003-1423-agy-r24-outputs.md) xác nhận World Bank có actual source data nhưng chưa có SVG. Task-local binding support sửa route capability này; không hạ editability/render/source-truth/QA gates và không sửa frozen World Bank measurements.

## Hợp đồng portable và effective binding

- `status=unavailable` và `engine_binding=null` trong package biểu thị **bundled default**.
- Package khai báo optional runtime-binding route, schema và checker portable. Local binding/receipts nằm ở project task evidence, ngoài source/dist.
- Có explicit task binding: kiểm project/task/host/capability, actual executable/interface/observation hashes trên host trước khi dùng.
- Binding invalid, thiếu capability, missing/stale receipt hoặc chưa quan sát đủ: giữ unavailable/pending và failure thật; không fallback im lặng.
- Không có task binding: bundled default vẫn unavailable.
- Checker pass chỉ là binding integrity/matching; actual tool observation, artifact acceptance và owner review là gates riêng. Model tự ghi `observed` không tạo evidence.

## Ownership triển khai

Maker sở hữu thay đổi tối thiểu sau; controller sở hữu probes, case runs, receipts, freeze/build/install và các plan records.

| Source owner | Thay đổi |
|---|---|
| `nckh-kit/extensions/native-documents/contract.json` | Giữ default unavailable/null; khai báo task-binding route/schema/checker portable. |
| `nckh-kit/core/contracts/extension.schema.json` | Optional typed/closed runtime-binding declaration; không đổi contracts providers khác. |
| `nckh-kit/core/contracts/visual-engine-binding.schema.json` | Schema mới cho explicit project/task binding và actual hash-bound observations. |
| `nckh-kit/scripts/check-visual-engine.py` | Read-only checker; không execute engine/model, không download/install/cấp quyền. |
| `nckh-kit/skills/core/nckh-visuals/SKILL.md` | Precedence/routing/limits, links đủ checker/schema/dependency closure. |
| `nckh-kit/skills/core/nckh-visuals/references/visual-acceptance.md` | Empty/unverified effective binding unavailable; artifact QA không được suy từ binding pass. |
| `nckh-kit/docs/research-and-writing.md` | Route, command thật sau khi triển khai và limitations. |
| `nckh-kit/tests/evidence/test_visual_engine_binding.py` | Focused scope/hash/capability/failure/extracted-portability checks; không provider/UI run trong unit tests. |

Source ownership có thể dùng helper/dependency thực tế tương đương theo local patterns; controller đối chiếu receipt/build closure với implementation trước nghiệm thu, không suy completion từ bảng này.

## Actual probe và giới hạn

Probe folder: `plans/evaluation/personal-use/visual-engine-probe-01/`; [native observation](../evaluation/personal-use/visual-engine-probe-01/native-observation.json).

- rsvg-convert **2.40.20** đã render `probe.svg` thành PNG thật, exit 0.
- Illustrator 2024 đã open SVG RGB; structure có editable text và vector paths. Probe text được sửa, save thành AI, reopen với nội dung khớp, restore và export previews thật.
- Observation giữ failed first probe do active document chuyển sang recovered document. `probe-edited.ai` từ lượt đó bị loại khỏi evidence; không xóa hoặc đổi nhãn failure.
- Font/coordinate observation ghi Arial Regular và artboard-web cho probe cụ thể.
- Probe là local engine/editability observation. Chưa phải World Bank final SVG, source-to-mark QA, owner score hoặc chứng nhận các host khác.

## Acceptance còn phải hoàn tất

1. Review/checker source và negative checks: missing/changed executable, stale hash/receipt, sai project/task/host, capability thiếu, self-declared observed không có reference thật.
2. Extracted checker dùng isolated Python/CWD khác mà không mượn source checkout hoặc PYTHONPATH; closure đủ schema và dependencies thật.
3. Fresh r25 source freeze, focused/affected tests, on/off build và extracted checks có receipts riêng; concrete preview/owned update/doctor giữ installation identity và user edits.
4. Native host thực sự đọc binding và dùng renderer trong quyền hiện hành; controller probe không tự chứng minh IDE execution.
5. Tạo World Bank SVG có editable text/data objects từ records gốc; source-to-mark, units/caveats/alt/reading order và exact artifact/render hashes đầy đủ. Actual open/edit/save/reopen/render QA gắn final artifact; thay đổi làm QA trước stale.
6. Sửa các memo/trace findings theo [Cursor review](review-261003-1423-cursor-r24-outputs.md), [Antigravity review](review-261003-1423-agy-r24-outputs.md) và [GPT-6.1 Sol review](review-261003-1435-gpt-6-1-sol-r24-output.md); giữ original outputs, ghi new hashes và review delta.

Repair prompts Cursor hai case (historical evidence path: `../evaluation/personal-use/native/cursor-grok-r24-repair-01-prompt.txt`; unavailable in the cleaned checkout) và Antigravity bốn case (historical evidence path: `../evaluation/personal-use/native/agy-gemini-r24-repair-01-prompt.txt`; unavailable in the cleaned checkout) được người dùng gửi thủ công; đang chờ original models hoàn tất, không có permission gate mới. Với GPT-6.1 Sol, controller reconcile trace global-development-rule read theo developer instruction ưu tiên cao hơn: mismatch nằm giữa brief project-only và instruction bắt buộc, không phải unauthorized test ở project khác hoặc global mutation. Brief tiếp theo phải giữ ngoại lệ instruction read này; quote/path-label correction vẫn cần artifact mới.

## Plan state và rollback

[Plan dùng cá nhân](../261003-0101-nckh-personal-use-sources-and-standards/plan.md) giữ **in-progress, 24/26**. Neutral shared-root installed source-reader run task được đóng theo actual IDE receipts và current-app reader trace; hai runtime tasks tiếp tục mở tới khi repairs/SVG đủ evidence. Coverage chỉ năm consumer identities của năm source cases, không phải behavioral qualification cả 37 skills. Goal resumed active; [blocked audit trước đó](blocked-audit-261003-native-r24.md) là lịch sử.

Rollback candidate phải giữ source/schema/lock khớp nhau; installed rollback chỉ qua owned transaction/backups, không reset edits của người dùng. Failed runs/probes và r24 receipts được giữ. Owner tự chấm sau personal use; external reviewer/holdout không chặn lane này. Stable/scientific/public qualification và quyền phát hành vẫn có scope riêng.
