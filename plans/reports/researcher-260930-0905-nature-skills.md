# Nghiên cứu `nature-skills` cho bộ skill nghiên cứu–viết–slide Việt/Anh

## Kết luận điều hành và xếp hạng lựa chọn

Khuyến nghị **hạng 1: xây một kit cá nhân mỏng, Việt/Anh rõ ràng, lấy kiến trúc và các cổng QA của `nature-skills` làm mẫu; không fork/copy nguyên bundle**. Đây là phương án phù hợp nhất với mục tiêu plan-only: giữ được grounding, provenance, kiểm tra định lượng, figure/PPTX QA và human review, nhưng không thừa hưởng mặc định tiếng Trung, định tuyến Nature/CNS, xếp hạng tài liệu chưa được kiểm chứng, cron/delivery hằng ngày hay asset bên thứ ba.

| Hạng | Phương án | Đánh giá |
|---|---|---|
| 1 | Kit cá nhân mỏng, `vi`, `en`, `vi-to-en`, có evidence ledger và human gates | **Nên chọn**; chi phí tích hợp vừa phải, rủi ro thấp nhất nếu tách venue/provider |
| 2 | Fork rồi loại bỏ dần phần Nature/Trung Quốc | Dùng được nhưng dễ mang theo coupling, policy assumption và asset/license debt |
| 3 | Dùng nguyên bundle upstream | Không nên; phù hợp demo/khảo sát hơn là workflow Việt/Anh có trách nhiệm |

## Phạm vi, revision và kích thước corpus

- Đối tượng: `https://github.com/Yuan1z0825/nature-skills`, phục vụ kế hoạch cá nhân về đọc/tìm kiếm/viết học thuật, figure và chuyển paper thành slide bằng tiếng Việt và tiếng Anh.
- Revision ghim: `84880815fb37317b3766bff2c2abba395b8993c3` (short SHA `8488081`), commit: <https://github.com/Yuan1z0825/nature-skills/commit/8488081>.
- Thời điểm kiểm tra: `2026-09-30`, múi giờ `Asia/Saigon`.
- Corpus inventory: **20 thư mục skill cấp cao**, trong đó README nhận diện **19 skill có thể trigger** và `nature-shared` là thư mục dùng chung. Đây là kích thước thư mục/skill, không phải cam kết về số dòng hay toàn bộ file đã được audit.
- Phương pháp: đọc source manifest qua Repomix remote `--stdout` và commit patch; không tạo bản clone lưu lâu dài trong workspace (Repomix có thể dùng checkout tạm), không sửa upstream, không chạy provider/cron, không mở phiên PowerPoint để xác nhận visual QA.
- Phạm vi đọc sâu: các module liên quan trực tiếp và reference/script được liệt kê dưới đây; các module không liên quan không được xem là đã audit đầy đủ.

## Source manifest

### Upstream

- `README.md`, `LICENSE`, `THIRD_PARTY_NOTICES.md`.
- `skills/nature-reader/{SKILL.md,manifest.yaml,static/core/principles.md,static/core/workflow.md,static/core/output-contract.md,references/grounding-rules.md,references/equation-handling.md,references/figure-extraction.md,scripts/validate_reader_math.py}`.
- `skills/nature-writing/SKILL.md`, `skills/nature-polishing/SKILL.md`.
- `skills/nature-academic-search/SKILL.md`, `skills/nature-citation/SKILL.md`, `skills/nature-ref-verifier/SKILL.md`.
- `skills/nature-data/SKILL.md`, `skills/nature-statistics/SKILL.md`, `skills/nature-reviewer/SKILL.md`.
- `skills/nature-literature-pipeline/SKILL.md`.
- `skills/nature-paper2ppt/{SKILL.md,references/design-and-layout.md,scripts/audit_pptx_quality.py}`.
- `skills/nature-figure/{SKILL.md,manifest.yaml,static/core/contract.md,references/ai-graphical-abstract-workflow.md,references/asset-adaptation.md,references/demos.md,references/qa-contract.md,scripts/validate_figure.py,scripts/audit_panel_alignment.py,scripts/audit_figure_collisions.py}`.
- `skills/nature-image2ppt/SKILL.md` và `skills/nature-paper-card/SKILL.md` được xem là phụ trợ; `image2ppt` không thay thế pipeline authoring từ research notes.

### Nguồn chính sách/đối chiếu bên ngoài

- [Nature Portfolio editorial policies](https://www.nature.com/nature-portfolio/en/editorial-policies), [AI policy](https://www.nature.com/nature-portfolio/editorial-policies/ai), [formatting guide](https://www.nature.com/nature/for-authors/formatting-guide), [initial submission](https://www.nature.com/nature/for-authors/initial-submission), [final submission](https://www.nature.com/nature/for-authors/final-submission).
- [Nature plagiarism/duplicate publication](https://www.nature.com/nature/editorial-policies/plagiarism), [data availability and data citations](https://www.nature.com/documents/nr-data-availability-statements-data-citations.pdf).
- [Nature Methods: Using AI responsibly in scientific publishing](https://www.nature.com/articles/s41592-026-03020-1) và [Scientific Reports AI risk framework](https://www.nature.com/srep/journal-policies/ai).
- [Independent review snapshot](https://mrkeyoor.com/repos/nature-skills/) và [third-party registry snapshot](https://tessl.io/registry/skills/github/Yuan1z0825/nature-skills/) chỉ là tín hiệu bổ sung, không phải bằng chứng chất lượng hay adoption.
- GitHub releases tại <https://github.com/Yuan1z0825/nature-skills/releases> hiện không cung cấp release artifact; vì vậy revision commit là provenance chính.

## Độ bao phủ và giới hạn bằng chứng

Đã đủ dữ liệu để đánh giá kiến trúc, output contract, các cổng kiểm tra và rủi ro tích hợp của các module liên quan. Chưa đủ dữ liệu để tuyên bố chất lượng khoa học, độ chính xác dịch/viết, độ đúng của ranking hay độ ổn định provider trong production: các script chưa được chạy trên corpus đại diện, chưa có benchmark hành vi Việt/Anh, chưa có kiểm tra người dùng/biên tập viên, và chưa có release artifact hoặc changelog làm cơ sở maturity. Một số claim trong upstream là procedure/design intent; không biến chúng thành kết quả thực nghiệm.

## Ma trận trích xuất cho năm capability yêu cầu

| Capability | Path upstream chính xác | Nên giữ | Cần đổi trong kit cá nhân |
|---|---|---|---|
| 1. Đọc paper, dịch và grounding | `skills/nature-reader/SKILL.md`; `skills/nature-reader/static/core/output-contract.md`; `skills/nature-reader/references/grounding-rules.md`; `skills/nature-reader/scripts/validate_reader_math.py` | Source-format routing; anchor `S001/C001/F001/T001/E001`; source map; block/page grounding; uncertainty và equation fallback | Locale `vi`/`en`; song song nguyên văn–dịch; provenance hash/page; không mặc định tiếng Trung; test chống translation drift |
| 2. Tìm kiếm, citation và reference health | `skills/nature-academic-search/SKILL.md`; `skills/nature-citation/SKILL.md`; `skills/nature-ref-verifier/SKILL.md`; `skills/nature-literature-pipeline/SKILL.md` | Claim-to-source ledger; phân mảnh claim; field-level DOI/metadata verification; cờ conflict/mismatch | Tách source tier và venue; không suy ra chất lượng từ impact/ranking; lưu query, timestamp, raw result, version; xác minh thủ công claim quan trọng |
| 3. Viết và polishing học thuật song ngữ | `skills/nature-writing/SKILL.md`; `skills/nature-polishing/SKILL.md` | Routing theo task/paper/section/venue; placeholder khi thiếu evidence; bảo toàn fact/terminology; tách rewrite khỏi layout | Thêm voice tiếng Việt, `vi-to-en`, terminology ledger, claim-drift diff; cô lập quy tắc từng journal/conference; không coi Nature guidance là policy chung |
| 4. Dữ liệu, thống kê và figure có thể chỉnh sửa | `skills/nature-data/SKILL.md`; `skills/nature-statistics/SKILL.md`; `skills/nature-figure/SKILL.md`; `skills/nature-figure/static/core/contract.md`; `skills/nature-figure/scripts/validate_figure.py`, `skills/nature-figure/scripts/audit_panel_alignment.py`, `skills/nature-figure/scripts/audit_figure_collisions.py` | Data/license gate; phân biệt measured quantity–independent unit–inference; figure contract; alignment tolerance; collision/PDF text audit; provenance bundle | Giữ số liệu bất biến từ nguồn; `AUTHOR_INPUT_NEEDED` cho n/p/test/correction thiếu; editable SVG/PDF/PPTX; human panel QA; tách asset license khỏi code license |
| 5. Chuyển paper thành slide | `skills/nature-paper2ppt/SKILL.md`; `skills/nature-paper2ppt/references/design-and-layout.md`; `skills/nature-paper2ppt/scripts/audit_pptx_quality.py` | Sáu presentation arcs; evidence-first hierarchy; conclusion-style title; text budget; source labels; speaker notes; PPTX audit | Locale/voice Việt/Anh; layout không phụ thuộc Nature; kiểm tra editability, font, contrast và source note; `skills/nature-image2ppt/SKILL.md` chỉ là reconstruction tùy chọn |

## Quyết định adopt / adapt / reject

**Adopt:** source map và stable anchors; claim/evidence ledger; placeholder và `AUTHOR_INPUT_NEEDED`; field-level reference verification; data/statistics gates; figure contract và deterministic QA; editable outputs; paper-type arcs; source labels/speaker notes; provenance bundle gồm input, tool/model/version, thời gian, output và manual correction; human review cuối.

**Adapt:** mọi routing phải nhận `language={vi,en,vi-to-en}`, `task`, `paper_type`, `section`, `venue`; tạo terminology ledger song ngữ; lưu query/raw snapshot/hash; coi quy tắc venue là config riêng; giới hạn provider/MCP bằng capability manifest; để daily pipeline là manual-on-demand; thêm trạng thái `UNVERIFIED`, `AUTHOR_INPUT_NEEDED`, `HUMAN_REVIEW_REQUIRED`.

**Reject hoặc cô lập:** Chinese-only default voice; hard-coded Nature/CNS assumptions; automatic literature score trình bày như scientific quality; daily cron/delivery cho kit tối thiểu; AI-generated scientific image ghi là submission-ready; copy asset `figures4papers` trước khi clearance; mọi số liệu/citation/experimental detail không có provenance.

## Năm nhóm rủi ro cần giữ trong kế hoạch

1. **Thiếu voice Việt và kiểm soát drift:** polishing upstream không hỗ trợ tiếng Việt trực tiếp; dịch `vi-to-en` có thể làm đổi mức độ claim, thuật ngữ, đơn vị hoặc điều kiện. Cần terminology ledger, source-linked diff và human bilingual review.
2. **Venue isolation chưa đủ:** writing/citation/paper2ppt mang giả định Nature/CNS và corpus-derived guidance. Không áp dụng sang journal/conference Việt, IEEE hay grant mà không nạp rule set riêng và ghi rõ version.
3. **Ranking/citation không phải bằng chứng chất lượng:** literature pipeline dùng weighted scoring và tự động deduplicate; score có thể biến thành proxy authority. Citation chỉ được coi là hỗ trợ sau khi claim-level abstract/full-text/publisher check; không dùng title/metadata/impact làm đủ.
4. **Scientific image và asset provenance:** AI graphical abstract phải là draft nếu chưa xác minh policy venue, không được bịa measurement/mechanism/citation và không upload confidential data. `figures4papers` là third-party material, không tự động thuộc Apache-2.0.
5. **Khoảng trống behavioral evaluation:** chưa tìm được benchmark phù hợp cho Vietnamese/English grounding, translation drift, reference conflict, figure editability hay PPTX readability trong các path đã đọc. Đây không phải khẳng định đã khảo sát toàn bộ benchmark công khai. Script pass không chứng minh người đọc hiểu hoặc output nộp được.

## License và xử lý asset

Root repository tại revision ghim ghi **Apache License 2.0**. Nếu tái sử dụng code/file, phải giữ notice, license và attribution phù hợp; phương án ít nợ pháp lý hơn là tái triển khai ý tưởng/contracts thay vì copy nguyên bundle. `skills/nature-figure/assets/figures4papers/` được upstream đánh dấu là third-party material và yêu cầu đọc `THIRD_PARTY_NOTICES.md`; không đưa các asset này vào kit hoặc deck phân phối cho tới khi kiểm tra từng license, attribution, modification/redistribution right. Chưa có release artifact nên mọi build cần lưu commit SHA và manifest nguồn.

## Behavioral tests đề xuất trước khi coi kit sẵn sàng

- **Reader/grounding:** một PDF có text, scanned PDF và HTML; output phải map được `S/C/F/T/E`, page/block, equation và asset; câu không có trong nguồn phải trả `原文未明确说明` tương đương Việt/Anh, không suy đoán.
- **Bilingual:** cùng một claim có hedge/định lượng; so diff `vi`, `en`, `vi-to-en`, bắt drift về modality, số, đơn vị, tên gene/thuật ngữ; human reviewer ký duyệt mẫu khó.
- **Citation/reference:** cố ý tạo DOI–title, author-order và year conflict; report phải flag field conflict, giữ raw sources, không tự chọn “đẹp” hơn.
- **Statistics/data:** prompt thiếu `n`, independent unit, test, correction hoặc exclusion; output phải dừng ở `AUTHOR_INPUT_NEEDED`, không sinh p-value/n hay software version.
- **Venue:** chạy cùng task với Nature, một venue quốc tế khác và một venue Việt; rule set, citation style, wording và availability statement không được lẫn.
- **Figure:** contract sai dimension/data type, panel lệch, text collision và thiếu provenance; validator phải fail đúng lỗi, sau đó human kiểm tra từng panel và editable layer.
- **Slides:** paper type khác nhau; PPTX phải có source labels/notes, text budget, font/contrast, editable shapes và audit report; kiểm tra rendering trên ít nhất hai viewer.
- **Provenance/asset:** output lưu input hash, model/provider/version, prompt, timestamp, candidate/selected output, manual changes và third-party notices; confidential input phải bị chặn khỏi AI route.

## Câu hỏi chưa giải quyết

- Bộ kit sẽ ưu tiên journal/conference nào ở Việt Nam và quốc tế; cần những venue rule set/version nào?
- “Viết tiếng Anh” là dịch từ bản Việt đã khóa, hay cho phép draft trực tiếp bằng tiếng Anh? Ai là human approver cho claim nhạy cảm?
- Có được dùng API/MCP bên ngoài không; dữ liệu nào bị cấm upload và cần offline-only mode không?
- PPTX đích là PowerPoint desktop, Google Slides hay cả hai; có yêu cầu font/template thương hiệu cụ thể không?
- Có chủ trương copy một phần code Apache-2.0 hay chỉ clean-room reimplementation? Ai sẽ cấp phép asset/figure bên thứ ba?
- Cần corpus gold song ngữ và danh sách reference/figure/PPTX để chạy behavioral tests ở mức nào trước khi triển khai?

## Status

**Status:** DONE_WITH_CONCERNS  
**Summary:** `nature-skills` cung cấp kiến trúc và QA pattern rất tái sử dụng cho kit nghiên cứu–viết–slide, nhưng cần một lớp Việt/Anh mới, provenance/evidence ledger, venue isolation và behavioral gates. Khuyến nghị xây kit cá nhân mỏng; không dùng nguyên bundle và không phân phối third-party figure assets khi chưa clearance.  
**Concerns/Blockers:** Chưa có benchmark hành vi Việt/Anh, live provider/cron validation, release artifact hoặc xác nhận license từng asset; các điểm này phải được xử lý trong plan/acceptance gates tiếp theo.
