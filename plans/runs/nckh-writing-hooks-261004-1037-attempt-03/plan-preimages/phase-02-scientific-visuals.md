---
title: "Phase 2: research-only scientific visuals"
status: pending
---

# Phase 2: research-only scientific visuals

## Outcome và data flow

Brief giữ `domain` hiện có → bounded `visual_purpose` (câu hỏi/đối tượng nghiên cứu/vai trò artifact/evidence IDs) → purpose guard → consumer route → source/data/mark map → native/render checker riêng → QA manifest và unresolved scientific gate. Không dùng engine-integrity receipt để suy ra purpose, ý nghĩa khoa học hay human acceptance.

## Điều kiện và policy

- [x] Nhận chart từ measurement thật có rights/provenance (`R-worldbank-vietnam-population` là ca sẵn có), derived/computational/simulation output từ phép tính hoặc run thật, scientific mechanism có source và nhãn `inference`, hoặc explanatory illustration có nhãn `illustrative/non-evidentiary`. Không xây thêm simulation pipeline.
- [x] Từ chối ad/banner/logo/thumbnail/generic artwork; research logo vẫn là branding. Cấm bịa observation, measurement, output/run receipt hoặc trình bày mô phỏng như quan sát thật; chart phải có source-to-mark mapping.
- [x] Purpose không được suy từ chữ “research” hay `domain` một mình; thiếu question/object/role/evidence trả `pending`/fail-closed. Giữ native editability, render, accessibility, provenance, scientific meaning thành các gate độc lập.
- [x] Mọi route trực tiếp/gián tiếp phải tuân policy research-only; route chưa có capability enforcement chỉ là instruction/manual/not-callable và phải dừng generation khi thiếu preflight. Không hứa hook chặn mọi arbitrary shell/tool path; giữ nguyên 27 skill/owner còn lại.

## File ownership (absolute paths)

Existing:

- `C:/Users/USER\Downloads\test-skill\nckh-kit\skills\core\nckh-visuals\SKILL.md:24-46`, `C:/Users/USER\Downloads\test-skill\nckh-kit\skills\core\nckh-visuals\references\visual-acceptance.md`, `C:/Users/USER\Downloads\test-skill\nckh-kit\docs\research-and-writing.md:28-64` — contract, source-to-mark, real data và independent gates.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\core\contracts\brief.schema.json:1-95`, `C:/Users/USER\Downloads\test-skill\nckh-kit\core\guards.py:1-69`, `C:/Users/USER\Downloads\test-skill\nckh-kit\scripts\check-visual-engine.py`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\evidence\test_guards.py:50-75`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\evidence\test_visual_engine_binding.py` — purpose/structural guard tách engine checker.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\core\registry\catalog\resources.json:332-380` và `C:/Users/USER\Downloads\test-skill\nckh-kit\scripts\search-resource.py:206-235,271-272` — World Bank source/reader; `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\resource\test_real_sources.py:98-117` — real-source/provenance behavior.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\evals\cases\research-writing-visuals\nckh-visuals.json:1-176`, `C:/Users/USER\Downloads\test-skill\nckh-kit\evals\rubrics\scientific-visuals.md` — existing positive/negative/outcome/failure owner.
- Indirect owners remain existing: `C:/Users/USER\Downloads\test-skill\nckh-kit\skills\marketing\nckh-brand\SKILL.md`, `C:/Users/USER\Downloads\test-skill\nckh-kit\skills\marketing\nckh-content\SKILL.md`, `C:/Users/USER\Downloads\test-skill\nckh-kit\skills\marketing\nckh-analytics\SKILL.md`, `C:/Users/USER\Downloads\test-skill\nckh-kit\skills\engineer\nckh-frontend\SKILL.md` (catalog entries at `C:/Users/USER\Downloads\test-skill\nckh-kit\core\registry\catalog\skills.json:298-304,431-437,507-513,602-608`).
- `C:/Users/USER\Downloads\test-skill\nckh-kit\extensions\native-documents\contract.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\extensions\providers\marketing\contract.json` [MODIFY] — document/asset binding instruction boundaries; bundled engines/providers vẫn unavailable, không biến contract JSON thành grant hay tự thêm provider.

New:

- `C:/Users/USER\Downloads\test-skill\nckh-kit\core\guards.py` [MODIFY] — shared purpose helper; `C:/Users/USER\Downloads\test-skill\nckh-kit\core\contracts\brief.schema.json` bounded optional record [MODIFY]. Không thêm service/module giả sandbox và không gộp với `C:/Users/USER\Downloads\test-skill\nckh-kit\scripts\check-visual-engine.py` receipt integrity.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\evidence\test_visual_purpose.py` [NEW] and expanded `C:/Users/USER\Downloads\test-skill\nckh-kit\evals\cases\research-writing-visuals\nckh-visuals.json` [MODIFY] with direct/indirect positive and negative routes.
- Optional owned `C:/Users/USER\Downloads\test-skill\nckh-kit\skills\core\nckh-visuals\references\scientific-visual-qa.md` [NEW] only after exact K-Dense MIT path/hash and attribution are recorded; do not copy broad scientific-visualization skill.

## Tasks

- [x] Specify schema fields and bounded enum for chart/mechanism/illustration plus `purpose_question`, `research_object`, `artifact_role`, `evidence_ids`, `source_access`, `inference_labels`, `non_evidentiary_label`; thêm `data_origin` phân biệt observed/derived/computational/simulation. Reject grant fields; với computed/simulation yêu cầu model/code/version/parameters/source/transform/output hashes, run locator và uncertainty hoặc lý do not-applicable.
- [x] Add source-to-mark validator cases: mọi value/label/arrow map tới observed field, verified calculation/run output hoặc explicit inference/illustration. Giữ denominator/unit (kể cả World Bank blank-unit), transforms, rights và artifact/render hashes; calculated/simulated output phải ghi rõ “không phải số đo quan sát”, không mất provenance khi vẽ.
- [x] Adapt chọn lọc K-Dense MIT table/QA sau khi ghi exact path/hash/attribution. World Bank là observed fixture; thêm một phép tính thật có output/hash và labeled simulation fixture chỉ khi có run thật được phép. Fixture contract không chứng minh nghiên cứu thực/human gold; thiếu run là pending, không bịa dataset để đóng test.
- [x] Add direct/indirect negative cases cho thiếu purpose, invented measurements, fake simulation receipt, thiếu uncertainty/label, branding/logo/banner, generic art; positive observed/derived/computed/simulation/mechanism/illustration có provenance. Giữ bốn base IDs của visuals; scenario phụ nằm trong `test_visual_purpose.py`, không thêm base case thứ năm.
- [x] Keep checker output honest: structural/purpose pass cannot certify scientific meaning, source truth, native editability, accessibility or reviewer approval. Existing native binding remains explicit project/task/host authorization.

## Entrypoints, preflight và coverage

| Entry/binding hiện có | Loại kiểm soát cần ghi đúng | Negative/side-effect oracle |
|---|---|---|
| `nckh-visuals/SKILL.md` → task SVG binding của `extensions/native-documents/contract.json` | Instruction gate trước host gọi engine; default unavailable. `scripts/check-visual-engine.py` chỉ đọc receipt, không phải generator hay preventive gate | Thiếu purpose/binding/grant: workflow không gọi render; không dùng receipt hậu kiểm để tuyên bố đã chặn |
| brand/content → `extensions/providers/marketing/contract.json` | Indirect asset handoff; unavailable provider không được tự bật | Logo/banner/thumbnail hoặc đổi tên thành “research”: reject generation, không xóa quyền soạn brief |
| analytics → chart; frontend → image/chart asset | Indirect instruction/manual route; UI inspection/screenshot bằng chứng không tự thành request sáng tác generic artwork | Dữ liệu marketing/UI heuristic không thay purpose/evidence; side-effect trace phải cho thấy không gọi generator khi bị từ chối |
| Tool/engine call được host chọn khi có binding/grant | Chỉ native event/version đã qualify mới được ghi host-enforced; hosted tools/shell escape không mặc nhiên có coverage | Deny, malformed, timeout, crash, unsupported: kiểm trước side effect từng event/version ở P3/P4 |

Hiện kit không có owned generating script cho các route trên; không bịa tên wrapper đã chạy. Bất kỳ controlled generator entrypoint nào được thêm khi triển khai phải gọi shared synchronous preflight ngay trước render/write/provider side effect và kiểm deny/error không sinh file/egress; nếu chưa có thì giữ manual/not-callable, dừng generation. `hook-preflight.py` chỉ là checker, tự chạy nó không chứng minh mọi host call sau đó được khóa. Inventory bindings/tool IDs ghi từ runtime thật sau grant, không đoán từ tên skill.

## Validation gates

Focused lock-independent commands (implementation only, cwd `C:/Users/USER\Downloads\test-skill\nckh-kit`): `python -B -m unittest tests.evidence.test_guards tests.evidence.test_visual_engine_binding -v`; `python -B -m unittest tests.resource.test_real_sources -v`. Đã trace các suite này dùng guard/schema/closure hoặc registry hash, không gọi `verify_source_lock` toàn source. New mandatory check: `python -B -m unittest tests.evidence.test_visual_purpose -v`, bao gồm direct/indirect fixtures; không tạo flag `--visual-purpose-matrix`. Full eval/build chỉ sau freeze P4. Payload/structural tests không đóng native generation/no-side-effect, QA, scientific hay human gates.

## Risk và rollback

Risk: indirect route bypasses purpose guard (L4×I5=20); mitigate one shared guard contract plus route-level negative cases and manual entrypoint fallback. Risk: structural guard is mistaken for engine/scientific proof (L3×I5=15); separate schemas, receipts and rubric statuses. Risk: source/rights drift (L2×I5=10); exact hash/lineage and stale invalidation. Roll back only new schema/helper/cases/QA references whose hashes match; retain old visual cases, receipts and failed evidence, and do not delete existing domain skills.

## Measurable exit

Mọi route được liệt kê có purpose contract và coverage class đúng (`instruction-only`, `controlled-preflight`, `native-verified`, `manual/not-callable`). Positive scientific plots có dữ liệu/run thật, mark mapping và label đúng nguồn gốc; fake observations/receipts bị từ chối. Chỉ route có kiểm trước side effect và bằng chứng thực mới được gọi enforced; unsupported route dừng tại workflow. Engine, scientific, native và human gates vẫn tách biệt.

## Execution checkpoint — r29

Initial fixture failure (historical evidence path: `../reports/tests-261004-1037-phase-02.log`; unavailable in the cleaned checkout) và focused repair (historical evidence path: `../reports/tests-261004-1037-phase-02-repair.log`; unavailable in the cleaned checkout) được giữ riêng. Current visual-purpose suite có 7 tests, gồm World Bank list locator `/0/data/0/value`, blank unit và phép tính thực đọc transform JSON. Full deterministic r29 (historical evidence path: `../runs/nckh-writing-hooks-261004-1037-attempt-03/deterministic.json`; unavailable in the cleaned checkout) đã chạy 181 tests, `OK (skipped=1)`; symlink fixture chưa chạy được vì quyền Windows. Đây là purpose/integrity/local calculation evidence. Checker không xác thực một source/run receipt bịa nhưng tự nhất quán, không certify scientific truth và không chứng minh arbitrary host generation đã bị chặn. Native engine/editability/render/accessibility/human-scientific gates giữ nguyên trạng thái riêng.

<!-- Updated: Validation Session 2 - approved A1 A8 A9; plan-only -->
