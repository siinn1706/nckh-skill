# Bounded review nguồn viết/nghiên cứu (04-10-2026)

## Kết luận hành động

Không nhập nguyên gói nào. Giữ chín resource hiện có của NCKH; dùng review này làm input cho plan đề xuất `nckh-humanwrite` và `nckh-paperwrite` (phương án 37→39 còn chờ duyệt), với reader/artifact/test do plan đó định nghĩa. Xếp hạng:

1. **EXISTS — `R-reporting-lookup`**: giữ làm tra cứu reporting-guideline theo thiết kế nghiên cứu; không gọi là chứng nhận tuân thủ.
2. **EXISTS — `R-publisher-profile`**: giữ làm snapshot lập kế hoạch theo venue/năm/track/article-type/stage; không suy ra Q1, peer review hay acceptance.
3. **EXISTS — `R-nature-reference`**: giữ đúng bản tiếng Anh đã khóa; dùng như heuristic viết, không phải corpus, grammar gold hay human gold.
4. **NEW candidate — Humanizer**: đưa checklist structural/no-invention vào proposed `nckh-humanwrite` và phần phù hợp của `nckh-paperwrite`; chưa sửa catalog hay copy package, còn reader/artifact/test sẽ do plan định nghĩa.
5. **NEW/deferred — LanguageTool**: chỉ xem xét adapter chẩn đoán tiếng Anh sau khi có runtime Java/provider và quyền phân phối; không phải giải pháp tiếng Việt.

## Phạm vi và độ chắc nguồn

- Đã đọc bounded năm thư mục: `humanizer-main`, `languagetool-master`, `nature-skills-main`, `scientific-agent-skills-main`, `skills-main`; không cài, không chạy script tải về, không gọi provider/network.
- Local checkout không có Git metadata của các gói; version/commit dưới đây là khai báo trong file hoặc source-lock, không phải xác nhận upstream hiện thời.
- `humanizer`: `blader/humanizer`, v3.1.0, MIT; revision upstream chưa biết. `languagetool`: `languagetool-org/languagetool`, `6.9-SNAPSHOT`, LGPL-2.1+ cho core nhưng resource có thể có license khác; revision chưa biết.
- `nature-skills`: package khai báo v1.5.0, Apache-2.0, owner `Yuan1z0825/nature-skills`; hash hiện tại của selected `language/en.md` khớp entry source-lock `6de5e67b...`, có provenance commit `84880815fb37317b3766bff2c2abba395b8993c3`. `scientific-agent-skills`: package khai báo v2.72.0, MIT, owner `K-Dense-AI/scientific-agent-skills`; hash hiện tại của selected reporting/publisher JSON khớp các entry source-lock, có provenance commit `154988403bb5a18e9d3c0ce4e6d5e2e4b184a298`. Đây chỉ xác nhận các file đã chọn, không xác nhận toàn bộ archive tải xuống cùng commit.
- `skills-main` là implementation skills của Anthropic cho Claude. README phân biệt Apache-2.0 với document skills “source-available, not open source” và tự giới hạn ở demonstration/education (`resources/skills-main/README.md:1,20-24`); không có license root thống nhất. `THIRD_PARTY_NOTICES.md` có BSD/GPL/MIT-CMU/OFL (`:7-365`), nên không được coi toàn bộ gói là Apache.
- Registry hiện có **9** resource (`nckh-kit/core/registry/catalog/resources.json:25-504`), không quay lại baseline thiếu dữ liệu cũ. Source-lock có top-level `revision: "26"` tại `nckh-kit/core/registry/source-lock/source-lock.json:1377-1380`; raw file SHA-256 là `11ac90b7e9ec865bda3a346c7ceea1c4ca762a354518a297eb4d88ea5ce1806f`. Archive directories hiện không có Git metadata; phải đối chiếu selected-file hash trước khi gọi archive là cùng upstream commit.

## Mapping EXISTS / NEW / CONFLICT

| Nguồn | Chủ sở hữu/quyền | Fit và artifact | Trạng thái / xung đột |
|---|---|---|---|
| Nature `static/fragments/language/en.md` | `Yuan1z0825/nature-skills`, Apache-2.0; source-lock pin áp dụng cho file đã chọn, không tự động cho toàn archive | Reader `nckh-kit/scripts/search-resource.py`; một record Markdown bounded cho `nckh-write`/`nckh-taste`; test consumer/real-source/closure | **EXISTS** qua `R-nature-reference`; English-only, không human gold. Heuristic 10–30 từ/SVO không áp đặt cho VI hay mọi genre. |
| K-Dense `scientific-writing/assets/reporting_guidelines.json` | `K-Dense-AI`, MIT; source-lock pin áp dụng cho file JSON đã chọn, không tự động cho toàn archive; 15 record, as-of 2026-10-01 | Reader hiện có; artifact là lựa chọn guideline theo study-design/protocol/AI flags; test `tests/resource/test_consumers.py:25-30` và real-source | **EXISTS** qua `R-reporting-lookup`; paper/planning evidence, không phải kết quả nghiên cứu hay certification. |
| K-Dense `scientific-visualization/assets/publisher_profiles.json` | `K-Dense-AI`, MIT; source-lock pin áp dụng cho file JSON đã chọn, không tự động cho toàn archive; 8 profile, as-of 2026-10-01 | Reader hiện có; artifact là snapshot applicability theo venue/year/track/article-type/stage; test `test_consumers.py:31-45` và real-source | **EXISTS** qua `R-publisher-profile`; snapshot stale/applicability warning bắt buộc; không suy Q1/acceptance. |
| Humanizer `SKILL.md` | `blader/humanizer`, MIT, v3.1.0 | Candidate cho proposed `nckh-humanwrite`/`nckh-paperwrite`: adaptation checklist edit-diff/factual-delta; plan sẽ định nghĩa reader/artifact/test | **NEW candidate**, chưa copy package/sửa catalog. Claim 16/16 blind test không là human gold; detector evasion bị loại; không có coverage VI được chứng minh. |
| LanguageTool core/API | `languagetool-org`, LGPL-2.1+ core; nested rules license riêng | Chỉ có thể làm adapter English diagnostics với Java 17/Maven hoặc HTTP; artifact phải là diagnostics có rule/source/version; hiện chưa có reader/test | **NEW/deferred**. Cây module không có `vi`; không bật provider/public server; không đóng gói rule trước khi review từng license. |

## Nguồn nên loại khỏi scope nhập

- `scientific-agent-skills` broad `scientific-writing`/`scientific-visualization`: giữ các nguyên tắc evidence IDs, no fabrication, raw→transform→presentation, uncertainty/provenance làm design reference; không copy cả skill (clinical/authorship/Python/policy và figure workflow đã trùng `nckh-write`/`nckh-method`/`nckh-visuals`).
- Nature workflow/figure fragments: chỉ source-design; `R-nature-reference` đã đủ bounded English fragment. Không tạo thêm resource figure nếu chưa có data thật, provenance, native export, rights, reader và test.
- `skills-main`: **CONFLICT/defer** vì generic Claude examples, document skills source-available và notices phụ thuộc; không có mapping trực tiếp cho viết nghiên cứu VI/EN. Promotional text, installation/provider instructions và claims trong README không phải evidence.

## Tách human evidence khỏi paper evidence

- `nckh-write` vẫn giữ VI/EN/bilingual routing, minimal-diff, no invented facts/citations và factual-delta checks (numbers, units, denominator, population/time, modality, certainty, causality, terminology, limitations, citations).
- `nckh-taste` chỉ dùng critique về rhythm/specificity/register/cliché/reader effort/genre. Không thêm AI-detector, scalar “human taste”, universal banned-word list; native/human acceptance phải là gate độc lập.
- Static hash, catalog/reader validation, guideline coverage và publisher lookup chỉ chứng minh identity/contract/snapshot. Chúng không chứng minh runtime quality, paper validity, peer review, Q1, human preference, scientific truth hay release readiness.
- Grammar limitation: Nature fragment và Humanizer chưa chứng minh VI; LanguageTool snapshot không có module `vi`; K-Dense JSON là planning metadata, không grammar corpus. Không dùng bất kỳ nguồn nào làm gold labels cho tiếng Việt.

## Source → reader → artifact → test

- Nature: `static/fragments/language/en.md` → `search-resource.py` (`resource_read`, `resource_sha256`, provenance, `human_acceptance=not-evaluated`) → bounded English advice → `test_consumers.py:53-59`, `test_real_sources.py:98-139`, `test_closure.py:98-115`.
- K-Dense reporting: `assets/reporting_guidelines.json` → same reader with design/protocol/AI gate → source-keyed guideline selection → `test_consumers.py:25-30` + rights/provenance guards.
- K-Dense publisher: `assets/publisher_profiles.json` → same reader with venue/year/track/article-type/stage gate → applicability snapshot + stale warning → `test_consumers.py:31-45` + real-source guards.
- Humanizer (plan candidate): selected concepts, not copied file → plan-owned reader/owned-local checklist for proposed `nckh-humanwrite`/`nckh-paperwrite` → edit diff + factual delta report → contract/test to be specified in the accepted plan; no source read/copy or catalog edit in this review.
- LanguageTool (future only): local English module/API → explicit Java/HTTP adapter → rule diagnostics with version/license provenance → integration/runtime/license tests required; no default enablement.

## Hash SHA-256 của local snapshot

Các hash dưới đây chỉ identity evidence, không là proof nội dung đúng hay upstream-current.

- Humanizer: `README.md` `a07a054f230dca1e3d25e32ba6c808905b743cc6fa56bf8b6868cee0b12a0432`; `SKILL.md` `0612f1dfb1672b0ea9b97e139bf1f06cabe98d8b27424fe8ff01e1fb4cc99cad`; `LICENSE` `4ac4810254ab36d45419141aeb8e69bf50652cfafe5b2dab947d06d44e5cbf96`.
- LanguageTool: `README.md` `999c7c74959a7bef9b355b09f23146c144988eae5cfb6a23acc5e5674d5f4d7b`; `pom.xml` `c48e5d13fd465b280a27bf22ced4fc1c336aff2c26cd0dbdd1073c5c5815ff37`; `COPYING.txt` `95a62130965bddc821631fcec03abe97246f9130f11a8be6f47579f8bc016fc8`; `RemoteLanguageTool.java` `ec05f6dbab13290b3d23c7f831af98ebbbb5a105ca6d09966b5fb6c28e647c93`.
- Nature: `README.md` `d9f8022437e0728f5d066269aa9e3b590ed55dacb46eafe42e58ba3bee3231f4`; `LICENSE` `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`; `manifest.yaml` `91004af376547a51b033e7e7aeab9fd81eb1fa727995afb9e8823a844e32925a`; `SKILL.md` `ce7c4d20329b96b03b0f0c0bb744411b1b4deaa7a7b69b90757705a83c195b12`.
- Nature selected fragments: `language/en.md` `6de5e67bf7c90361237f998c10f98d6d2c61e9c067ce3c686cab6a3cdf919caf`; `core/workflow.md` `e02426a89e729d6f725d83a4ad41f8393a3aa0fcd968c7a0402a0e2b6b6293fd`; `core/stance.md` `ebe691909f4aef282e0d976565fb08ec2b41e62b72f464629c9781d732c53326`.
- K-Dense: `README.md` `2d4a9f2268c6ed70fc0d0d769921963da6b82966bd71c4b0225e35b0779b2447`; `LICENSE.md` `09b02a3c9df3053c55531d503357a9c7cde275970e6c3ceaa1ddf5f0e90b40c1`; `pyproject.toml` `f1389a7dcea847fab4bbd59d4d4b15a717e9eb7fbd28af46115cb1ad8d9fb876`; `scientific-writing/SKILL.md` `511a2096bebecd8cf0f8212b9d262d37154ae1ba566eb385d93ac968682edbd1`.
- K-Dense data/visual refs: `reporting_guidelines.json` `215f8c55bd40bda0569f2e81556030ff575319e25276b1e1ae70e2cc7475ddcd`; `publisher_profiles.json` `1e1b1b5a4e0e3dfc57877f2abf1e96888fe6b65617234b078f193b8f76e0ebe9`; `scientific-visualization/SKILL.md` `8cbde7cdc10d959cf72cfd08335cc8ce996247eee6ebdb900eb64a4cb0ff34a3`; `references/publication_guidelines.md` `5f70c6b22dbb5e0fae18b0f1197b8794896bf7afc059874bcf7afbd5aa86bbe5`.
- Skills-main: `README.md` `2fb9c4cc026366ea6e21c60cb23c908a4d27c62071819cc06beffaac102d0694`; `THIRD_PARTY_NOTICES.md` `a8ff7a84dee9dfb42ab448de281784387ceafdf63881b7c070ee2de7f6ed865c` (không có root `LICENSE`).
- NCKH current: `nckh-write/SKILL.md` `c549bea6981aece7f87f5d14288c51136b0b370a27411a0d8d2114ea6ef25ca8`; `nckh-taste/SKILL.md` `1c17d6441e661e4653e3effd7a6db64090e0cf6e0b5d36b77344837007058181`; `nckh-research/SKILL.md` `360584948b4119704fe987fe895b3efef8ef8f401614f66e2b7af787a9f944fd`; `nckh-method/SKILL.md` `f1edb47a7e5750d901699828fd0000fab6b9dc7aed44336f8427d4c7ba20124a`; `nckh-visuals/SKILL.md` `cf4ddad0701a379251eaa8083c871a8bd7bd6aa63d51e1affba52b8285a6e852`.
- NCKH registry/runtime: `core/registry/catalog/resources.json` `dbb6c347dc411efc84a7e4b880a955d825e6d464d23407947a052c6038844da5`; `scripts/search-resource.py` `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb`; `core/registry/source-lock/source-lock.json` `11ac90b7e9ec865bda3a346c7ceea1c4ca762a354518a297eb4d88ea5ce1806f`.

## Câu hỏi còn mở / gate

- Phương án 37→39 (`nckh-humanwrite`/`nckh-paperwrite`) vẫn chờ duyệt; owned-local Humanizer adaptation và test chỉ thực hiện sau approval, nhưng candidate không bị loại khỏi plan.
- Nếu cần LanguageTool, phải chốt local Java boundary, module/rule license inventory, English-only scope và runtime acceptance; chưa có quyền bật HTTP/public server.
- Đây không phải ý kiến pháp lý; license/notice chỉ là inventory kỹ thuật, cần review quyền phân phối/derivative/third-party trước release.

Status: DONE_WITH_CONCERNS
Summary: Đã chốt ranked selective reuse, phân biệt human/paper evidence và loại bỏ promotional/AI-evasion scope; chưa có runtime/semantic/human acceptance.
Concerns/Blockers: Revision upstream của ba package local chưa biết; LanguageTool chưa có VI/runtime; mọi adaptation mới cần owner, reader, artifact, test và rights gate.
