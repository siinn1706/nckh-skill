---
title: "Phase 1: identity, routing và selective writing data"
status: completed
---

# Phase 1: identity, routing và selective writing data

## Outcome và data flow

Đóng băng read-only baseline ở đầu phase → brief/action + locale/genre/protected fields → route `nckh-write`/writer mới → policy/reader chọn lọc → artifact prose hoặc paper outline kèm factual-delta/evidence gates → bốn case/identity và receipt trạng thái. Source lock r26 chỉ được đọc; P4 là owner duy nhất của freeze/revision.

## Điều kiện, contract và ranh giới

- [x] Thực hiện đúng quyết định hai writer với `--en`/`--vi`, additive 37→39; không tách bốn identity theo locale, không xóa route cũ. Lệnh `/goal ak-cook --auto` ngày 04/10/2026 đã cấp quyền implementation cục bộ.
- [x] Giữ 148 case IDs và lịch sử cũ; thêm đúng 4 case `positive/negative/outcome/failure` cho mỗi identity mới, tổng đúng 156 base cases. Supplemental locale/visual/hook cases nằm riêng; không regrade receipt lịch sử. Nội dung case hiện tại chỉ đổi theo contract được duyệt, phải ghi revision mới và làm stale receipt cũ.
- [x] `nckh-humanwrite`: polish/nhịp/ngữ pháp/dịch VI↔EN theo brief, minimal diff; paper paragraph polish vẫn bảo toàn claim, quote, số, đơn vị, phủ định, modality, certainty, causal scope, citations, limits và protected regions.
- [x] `nckh-paperwrite`: outline/section/argument/reporting/revision-response từ evidence đã có cho paper/thesis/proposal/report; không tự tạo kết quả, không ép IMRaD/clinical checklist cho mọi ngành.
- [x] `nckh-write` vẫn là compatibility route và chọn theo requested action, không chỉ từ chữ “paper”; `nckh-taste` chỉ critic rhythm/register/specificity/genre, không AI detector hay điểm “human”.
- [x] Hai writer dùng cùng normalization: `--en` → output English, `--vi` → output Vietnamese; hai flag cùng lúc trả lỗi xung đột, chưa tạo/sửa draft. Không flag: dùng target được user nói rõ, rồi brief, rồi ngôn ngữ chính của draft; nếu vẫn thiếu/mixed không rõ thì hỏi một câu. Output locale không thay resource locale. Bilingual request cũ giữ tương thích, không thêm identity hoặc flag mới.

## File ownership (absolute paths)

Existing:

- `C:/Users/USER\Downloads\test-skill\nckh-kit\core\registry\catalog\skills.json:104-136` — two additive entries/dependencies, no deletion of current 37.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\core\build.py:166-190`, `C:/Users/USER\Downloads\test-skill\nckh-kit\core\evaluation.py:14-37,72-124`, `C:/Users/USER\Downloads\test-skill\nckh-kit\core\acceptance.py:75-82`, `C:/Users/USER\Downloads\test-skill\nckh-kit\core\contracts\catalog.schema.json` — [MODIFY] exact 39 membership, duplicate rejection, bốn base case/identity và 19 families. Schema dùng `minItems=39` cùng ID enum đúng baseline ∪ hai writer; build/eval/acceptance kiểm length=39, no duplicates và exact-set equality. `C:/Users/USER\Downloads\test-skill\nckh-kit\core\schema.py` [READ] không hỗ trợ `maxItems`; không thêm keyword không hợp lệ hoặc mở rộng schema engine chỉ để kiểm count.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\core\profiles\acceptance\personal-use.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\acceptance\test_profile.py:21-48,72-86`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\release\test_qualification.py` — [MODIFY] candidate rows/counts/nguồn/closure; schema và tests phải reject missing/replaced/duplicate ID. `C:/Users/USER\Downloads\test-skill\nckh-kit\scripts\compare-matched.py:51-65` [PRESERVE] giữ đúng 37/148 của historical diagnostic, không search-replace các số lịch sử.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\skills\core\nckh-write\SKILL.md:24-41`, `C:/Users/USER\Downloads\test-skill\nckh-kit\skills\core\nckh-taste\SKILL.md:24-39`, `C:/Users/USER\Downloads\test-skill\nckh-kit\core\profiles\style\vi.md:1-13`, `C:/Users/USER\Downloads\test-skill\nckh-kit\core\profiles\style\en.md:1-13` — compatibility, locale rhetoric and separate critic owner.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\scripts\search-resource.py:206-272`, `C:/Users/USER\Downloads\test-skill\nckh-kit\core\registry\catalog\resources.json:1-526`, `C:/Users/USER\Downloads\test-skill\nckh-kit\evals\cases\research-writing-visuals\nckh-write.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\evals\cases\research-writing-visuals\nckh-visuals.json`, and `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\resource\test_consumers.py:13-59`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\resource\test_real_sources.py:98-117` — bounded reader/rights/real-source tests.

New:

- `C:/Users/USER\Downloads\test-skill\nckh-kit\skills\core\nckh-humanwrite\SKILL.md` and `C:/Users/USER\Downloads\test-skill\nckh-kit\skills\core\nckh-humanwrite\references\humanizer-adaptation.md` [NEW]; `C:/Users/USER\Downloads\test-skill\nckh-kit\skills\core\nckh-paperwrite\SKILL.md` and `C:/Users/USER\Downloads\test-skill\nckh-kit\skills\core\nckh-paperwrite\references\paperwriting-policy.md` [NEW]. Humanizer bắt buộc là owned Markdown policy, entrypoint humanwrite phải link và đọc trực tiếp; không JSONL/generic-reader tùy chọn. Hai entrypoints khai báo các lệnh reader theo matrix trong source map.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\evals\cases\research-writing-visuals\nckh-humanwrite.json` and `C:/Users/USER\Downloads\test-skill\nckh-kit\evals\cases\research-writing-visuals\nckh-paperwrite.json` [NEW], plus exact 39-row profile/catalog references [MODIFY].
- `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\resource\test_writer_consumers.py` [NEW, mandatory] — reader/rights/locale, Humanizer link và direct policy consumption; `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\acceptance\test_profile.py` vẫn là profile owner.
- `C:/Users/USER\Downloads\test-skill\nckh-kit\core\contracts\writer-invocation-matrix.schema.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\evals\cases\runtime\writer-invocation-matrix.json`, `C:/Users/USER\Downloads\test-skill\nckh-kit\tests\release\test_writer_matrix.py` [NEW, mandatory]. P1 thêm pure `validate_writer_matrix` vào `core/evaluation.py`; P4 nối vào `validate_cases` và tổng hợp receipt. Không tạo flag CLI mới.

## Tasks

- [x] Record starting source-lock hash/revision, exact 37 catalog IDs, resources=9, exact 148 case IDs và historical 224 matrix hash; preserve old receipts. Capture approved baseline set before sửa; target phải đúng baseline ∪ `{nckh-humanwrite,nckh-paperwrite}`, không chấp nhận thay một skill cũ bằng ID khác.
- [x] Adapt Humanizer concepts into the linked Markdown policy: source/path/hash/license, issue, context, counterexample, protected fields và rationale. Output bắt buộc edit diff + factual-delta record; test rule áp dụng/không áp dụng, giữ số/citation/negation. Ví dụ tự soạn chỉ là test fixture, không corpus/human gold; không dùng 16/16 detector claim hay bịa upstream commit.
- [x] Áp dụng [resource→writer mapping](./source-adoption-map.md#writer-consumer-mapping-đã-duyệt): humanwrite thêm Nature/Wikisource/PMC; paperwrite thêm PMC/Nature/reporting đúng clinical-health applicability. Giữ consumer cũ; không cấp Wikisource cho paperwrite hoặc publisher cho writer. Reader luôn dùng locale/domain/genre/rights của resource, độc lập output VI/EN.
- [x] Define VI rhetoric from the original contextual `vi.md`/owned samples; do not translate an English blacklist. Prohibit AI-detection/evasion and fabricated personal anecdotes.
- [x] Chuẩn hóa skill arguments ở entrypoint hai writer và compatibility router; flag là giao diện của skill, không giả định host/CLI tự hỗ trợ. Nạp có chọn lọc style `en.md`/`vi.md`; giữ shared evidence/fidelity policy và paper-domain riêng, không nhân bản SKILL theo ngôn ngữ.
- [x] Keep LanguageTool deferred: English diagnostic only, Java 17/provider and nested LGPL/resource rights explicit, no mandatory engine/service/public server/copy rule. Absence cannot block core writer contract.
- [x] Add positive/negative/outcome/failure oracles for each writer, including polish-vs-authoring routing, no invented claim/citation, protected-delta failure, wrong-owner handoff and no side effect. Supplemental locale cases bắt buộc: cả hai writer × VI/EN, cả hai flag/conflicting args, no-flag resolution, source→target khác ngôn ngữ, English source lookup khi output VI, bilingual compatibility và router giữ nguyên locale; không nhân đôi base case IDs.

## Writer matrix contract

Supplemental matrix dùng schema đóng, không có top-level `skill_id` để không bị hiểu là base manifest. `native_cases` có exact ID set từ hai writer × 8 surfaces hiện có × 4 invocation routes (`ui-slash`, `native-menu`, `headless-prompt`, `implicit`) × 2 output locales × 2 entrypoints (direct writer, `nckh-write` router): **256 planned cells**, không phải runtime PASS. IDs nối surface/writer/entrypoint/invocation/locale; validator reject thiếu/thừa/trùng, không chỉ đếm. Tám surfaces: claude-code, codex-cli, codex-desktop, codex-ide, cursor-cli, cursor-ide, agy-cli, agy-ide; route chưa hỗ trợ giữ not-callable, không bịa UI syntax.

`scenario_cases` riêng có đúng hai writer × 10 scenarios = **20 supplemental IDs**, không nhân toàn bộ scenarios qua mọi host. Scenarios: `output-en`, `output-vi`, `conflicting-flags`, `no-flag-explicit-target`, `no-flag-brief`, `no-flag-draft`, `no-flag-ambiguous`, `cross-language-fidelity`, `english-resource-vi-output`, `bilingual-compatibility`. Test structural chỉ kiểm contract; observed behavior cần run/receipt riêng khi được cấp quyền. Cả hai tập không được cộng vào 156 base cases hoặc 224 historical cells.

Mỗi cell ghi host/surface, observed version hoặc `unverified`, action/expected owner, args/input-output locale, resource locale, expected route, protected fields, no-side-effect oracle, status và receipt reference/hash. Conflict/ambiguous phải không đổi artifact; bilingual kiểm cả không flag và explicit flag override. Unsupported route vẫn hiện `not-callable` với reason; còn lại `not-run`, receipt null đến khi chạy thật. Receipt thật phải bind input/artifact/source/config/host/version, tool/egress observations và cleanup; tài liệu/hash không được tự đổi thành native pass. Action cases phải bao phủ polish so với scientific authoring. Schema/tests có positive, wrong-owner, protected-delta, false-receipt và missing-cell cases.

## Validation gates và freeze sequencing

Trước mọi sửa source, được dùng `python -B evals/run-evals.py --validate-only` làm baseline. Sau sửa P1–P3, hoãn lệnh đó, full suite và build đến freeze P4; không bypass `verify_source_lock`.

Focused commands (implementation only, cwd `C:/Users/USER\Downloads\test-skill\nckh-kit`): `python -B -m unittest tests.acceptance.test_profile -v`; `python -B -m unittest tests.resource.test_consumers tests.resource.test_real_sources -v`. Đã trace: profile dùng `load_profile`→`validate_profile` và link `closure`, reader dùng resource registry/hash; chúng không gọi global source-lock verifier, nhưng profile suite chỉ chạy sau khi catalog/schema/acceptance/profile cùng chuyển sang exact 39. New mandatory commands: `python -B -m unittest tests.resource.test_writer_consumers tests.release.test_writer_matrix -v`; matrix tests gọi pure validator, không `validate_cases`. Các test đã có trong candidate và được chạy ở lượt cook; native/human gates vẫn riêng. Đóng gói/Humanizer closure integration và native language behavior nằm ở P4, không suy language quality từ static pass.

## Risk và rollback

Risk: consumer count drifts or locale splits duplicate policy (L3×I5=15); mitigate exact-membership tests, shared preservation and action+locale compatibility route. Rights/VI coverage overclaimed (L2×I5=10); mitigate bounded source records, rights fields and pending human/domain gate. Roll back only owned new catalog/profile/case/skill files when hashes still match; retain old 37/148 files, receipts and failed attempts. Do not rewrite source lock or installed r25.

## Measurable exit

Implementation cục bộ đã có exact 39 identities/profile rows, 156 base IDs (giữ 148 ID cũ), supplemental matrix schema/validator cùng Humanizer link/consumer tests. Focused P1 suite (historical evidence path: `../reports/tests-261004-1037-phase-01.log`; unavailable in the cleaned checkout) đạt 32 tests; [four-case writer forward test](../reports/reviewer-261004-1037-writer-forward-test.md) ghi actual prose/outline/conflict/clarification và giới hạn local agent evidence. [Static r29](../runs/nckh-writing-hooks-261004-1037-attempt-03/validate.json) validate 256 planned native cells/20 scenarios; observed behavior của matrix vẫn unverified. Packaged closure, native/human/scientific gates giữ owner P4. Language contract: [decision record](../reports/decision-261004-0047-writer-language-options.md).

<!-- Updated: Validation Session 2 - approved A1 A2 A6 A7; plan-only -->
