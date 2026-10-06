# Nghiên cứu hệ sinh thái skill bổ sung cho bộ viết/nghiên cứu cá nhân

Ngày đối chiếu: 30/09/2026, múi giờ Asia/Saigon. Đây là báo cáo nghiên cứu để lập kế hoạch; không cài skill, không tạo skill, không gọi provider, không chỉnh runtime và không triển khai sản phẩm.

## Kết luận điều hành

Khuyến nghị xếp bộ tương lai thành các module nhỏ quanh một hợp đồng bằng chứng do dự án tự sở hữu. Chọn lọc ý tưởng từ K-Dense cho claim/evidence và citation audit, từ Orchestra cho slide khoa học chỉnh sửa được, và từ `trussary/vietnamese-language-skill` cho register/locale lint. Giữ kiến trúc hình học và nguồn-truth của OpenAI làm reference, còn văn phong tiếng Việt cá nhân, hồ sơ venue, schema bằng chứng và lớp kiểm tra sơ đồ phải là original work.

Không nên fork hoặc cài nguyên một collection. Các nguồn có mục tiêu khác nhau, dependency/provider khác nhau, license không đồng nhất và nhiều nội dung venue-specific. Bộ mặc định nên là: AgentKit/nature-skills làm orchestration theo các báo cáo nội bộ; nguồn dưới đây chỉ cung cấp adapter, hợp đồng hoặc reference đã được khóa phạm vi.

## Phạm vi và phương pháp

- Đã kiểm tra các source file được chỉ ra dưới đây trên repository chính chủ; ngày kiểm là ngày báo cáo. Không dùng GitHub stars, tên tác giả hay số fork làm bằng chứng chất lượng.
- Không tái nghiên cứu AgentKit hoặc nature-skills; giữ chúng ở vai trò baseline theo công việc của các agent khác.
- Với branch `main` khi không lấy được commit SHA qua giao diện, ghi rõ snapshot/ngày thay vì bịa SHA. Trước khi triển khai phải chốt commit, hash file và license ledger.
- Phân loại hành động: **chọn lọc** (ý tưởng/cấu phần được phép); **ủy quyền** (worker tùy chọn, có receipt và dependency); **reference-only** (đọc để thiết kế, không copy vào runtime); **original** (tự viết và tự chịu trách nhiệm).

## Xếp hạng và ma trận trade-off

Điểm “fit” là độ phù hợp với năm mục tiêu: giọng Việt cá nhân, bằng chứng/citation, English scientific writing, slide editable và diagram trung thực. “Cao” không có nghĩa nguồn đã chứng minh hiệu quả trên dự án này.

| Hạng | Nguồn / file thực đã đọc | Fit và điểm mạnh | Chi phí, rủi ro, provenance | Quyết định |
|---|---|---|---|---|
| 1 | [K-Dense `scientific-writing/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md), README, CONTRIBUTING, SECURITY | Cao cho evidence-bound English writing: cấm bịa citation/data/method/result; claim phải trỏ evidence ID; giữ uncertainty, denominator, unit, limitation; có manifest/audit offline. MIT, version 2.1 trong frontmatter. | Collection lớn, cập nhật nhanh, không có SHA ổn định trong lần kiểm; không nên nhập venue corpus hoặc prompt nguyên bộ. | **Chọn lọc** claim/evidence registry và audit contract; giữ human verifier. |
| 2 | [K-Dense `citation-management/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/citation-management/SKILL.md) | Cao cho metadata enrichment, duplicate/DOI/reference validation và multi-database search. MIT, version 2.1. | Python 3.9+, `requests`, network OpenAlex/Crossref/PubMed/arXiv/DataCite; Google Scholar là supplement scraped; không được mặc định có key hay coi metadata đúng tuyệt đối. | **Ủy quyền/chọn lọc**; worker trả receipt, người kiểm mở nguồn gốc. |
| 3 | [Orchestra `presenting-conference-talks/SKILL.md`](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/main/20-ml-paper-writing/presenting-conference-talks/SKILL.md) | Cao cho conference deck editable: `python-pptx`, Beamer PDF, speaker notes, talk script, slide count, figure readability và citation workflow. File ghi version 1.0/MIT. | Thiên về ML/systems conference; Python dependency; không phải quy chuẩn universal. Root MIT nhưng thư viện tham chiếu có license riêng. | **Chọn lọc**, kết hợp native validation của runtime hiện tại. |
| 4 | [OpenAI reports/slide automation](https://github.com/openai/plugins/blob/main/plugins/build-web-data-visualization/skills/reports-pdfs-and-slide-automation/SKILL.md) và [PowerPoint/Google Slides reference](https://github.com/openai/plugins/blob/main/plugins/build-web-data-visualization/skills/reports-pdfs-and-slide-automation/references/powerpoint-and-google-slides.md) | Cao cho kiến trúc asset bền vững: source/caveat/alt metadata, owner và regeneration path; `pptxgenjs`; geometry Google Slides rõ ràng. | Plugin/runtime có thể drift; license của đúng path chưa được thiết lập trong lần kiểm; không copy mặc định. | **Reference-only**, dùng để định nghĩa interface và provenance. |
| 5 | [OpenAI UML/software-architecture visualization](https://github.com/openai/plugins/blob/main/plugins/build-web-data-visualization/skills/uml-and-software-architecture-visualization/SKILL.md) | Cao cho diagram có truth contract: xác định modeling job/audience; formal UML hay UML-like; source IDs, labels, inferred-vs-source truth, semantic validation, accessibility, export và visual regression. | Tập trung diagram phần mềm; không tự giải quyết khoa học tự nhiên hoặc correctness của dữ liệu thí nghiệm; license path chưa xác định. | **Reference-only** cho model/validation; sơ đồ khoa học vẫn original. |
| 6 | [Trussary `vietnamese-tech-writing/SKILL.md`](https://github.com/trussary/vietnamese-language-skill/blob/main/skills/vietnamese-tech-writing/SKILL.md), [register matrix](https://github.com/trussary/vietnamese-language-skill/blob/main/shared/references/register-matrix.md), [locale formatting](https://github.com/trussary/vietnamese-language-skill/blob/main/shared/references/locale-formatting.md), [validator](https://github.com/trussary/vietnamese-language-skill/blob/main/shared/scripts/validate_copy.py) | Cao cho technical Vietnamese: code-switching, register, NFC/diacritics, ICU `other`-only, vi-VN numbers/dates, doctype-gated lint. Skill file ghi MIT, version 1.0.0; root repo MIT. | Repository nhỏ (9 commits, 0 issue tại lần kiểm), bus factor/adoption thấp; register generic không thể đại diện gu riêng; legal/compliance rows cần người chuyên môn. | **Chọn lọc** validator concepts và locale references; **original** personal taste corpus. |
| 7 | Runtime [OpenAI presentations skill](https://github.com/openai/skills) và các file local `presentations/SKILL.md`, `style_guidelines.md`, `references/native_evidence.md`, `references/finalization.md` | Cao cho artifact native, bảng/chart/diagram editable, render-inspect QA và source notes; là baseline đang có của môi trường. | Không phải collection external cần nhập; package local không lộ license file ở root lần kiểm; phụ thuộc runtime. | **Giữ nguyên qua runtime**, không copy/redistribute. |
| 8 | [Anthropic `anthropics/skills`](https://github.com/anthropics/skills), `skills/pptx/SKILL.md`, `docx/SKILL.md`, `pdf/SKILL.md`, marketplace | Kỹ thuật OOXML/render/validation có giá trị tham khảo. | README nói nhiều skill Apache-2.0 nhưng từng Office skill ghi `license: Proprietary`, `LICENSE.txt` là điều khoản đầy đủ; issues [#67](https://github.com/anthropics/skills/issues/67) và [#675](https://github.com/anthropics/skills/issues/675) cho thấy rủi ro discoverability/marketplace. | **Reference-only; không copy hoặc phát hành lại** Office skill content. |
| 9 | [Anthropic `claude-plugins-official` plugin-dev](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/plugin-dev/skills) | Tốt cho progressive disclosure, manifest, plugin structure và maintenance. | Không phải lớp viết/citation/diagram; host-specific và license từng path chưa chốt. | **Reference-only** packaging; không đưa vào core. |
| 10 | [`blader/humanizer/SKILL.md`](https://github.com/blader/humanizer/blob/main/SKILL.md), [LICENSE](https://github.com/blader/humanizer/blob/main/LICENSE) | Có checklist chống prose rập khuôn, giữ names/numbers/dates/citations và yêu cầu hỏi khi thiếu dữ kiện; MIT; SHA gần nhất quan sát được `9862685` (06/09/2026). | English-centric; tác giả nói rõ không nhằm bypass detector và output vẫn có thể bị flag; không phải detector, không phải evidence validator. | **Reference-only** anti-slop heuristic sau evidence/claim audit và human review. |

## Bằng chứng từ các file thật và giới hạn diễn giải

`scientific-writing` là ứng viên mạnh nhất vì nó ràng buộc câu với evidence thay vì chấm “văn hay”; điều này phù hợp với yêu cầu không bịa và giữ uncertainty. `citation-management` bổ sung metadata/retraction/duplicate checks nhưng chỉ xác minh danh tính và trạng thái tra cứu, không chứng minh paper hỗ trợ câu đang viết.

Trussary không phải “personal taste model”. `vietnamese-tech-writing/SKILL.md` yêu cầu giữ các term như `deploy`, `commit`, `merge`, dùng register impersonal cho RFC/postmortem/runbook và chạy validator sau khi viết. `register-matrix.md` coi một register là nhất quán trong toàn văn; `locale-formatting.md` đặt dấu phẩy thập phân, dấu chấm phân tách nghìn và VND không có minor unit. Đây là quy tắc locale/register có thể kiểm tra, không thay thế corpus bài đã được người dùng duyệt.

`literature-review` của K-Dense (MIT, version 1.8) có search/screening/reproducibility hữu ích nhưng dùng `OPENROUTER_API_KEY` cho bước LLM và bắt buộc diagram AI trong review; chỉ lấy search log/screening contract, bỏ mandatory diagram và venue mixing. `scientific-schematics` (MIT, version 1.7) tạo raster PNG qua provider và review bằng model; chưa thấy vector/editable source hoặc DPI control trong phần đã đọc, nên không dùng làm scientific diagram truth. `scientific-slides` (MIT, version 1.8) mặc định render mỗi slide thành image/PDF; đường mặc định đó không đáp ứng editable PPTX. Kiểm tra bổ sung của controller xác nhận file cũng có nhánh Alternative: PowerPoint Workflow, tách text khỏi visual và giao cho PPTX skill. Nhánh này là ứng viên có điều kiện, không phải bằng chứng hình/chart còn chỉnh sửa nội bộ hay đã chạy thành công. Vì vậy không loại toàn bộ skill chỉ từ đầu ra mặc định; ưu tiên engine khớp hợp đồng editability và quyền dùng công cụ của nhiệm vụ.

## Comparator phương pháp, không phải skill

- [Stanford OVAL STORM](https://github.com/stanford-oval/storm) và bài [NAACL 2024](https://aclanthology.org/2024.naacl-long.347/) tách pre-writing thành perspective discovery, simulated question asking, curation và writing. Bài báo báo cáo tăng 25 điểm phần trăm về tổ chức và 10 điểm về breadth so với baseline, đồng thời nêu source-bias transfer và over-association. Repo ghi MIT và yêu cầu Python 3.11/LLM/retriever tùy cấu hình. Dùng làm reference cho `discover/outline`, không biến web research tự động thành bằng chứng khoa học đã kiểm.
- [FutureHouse PaperQA2](https://github.com/Future-House/paper-qa) và [bài 2024](https://arxiv.org/abs/2409.13740) là scientific PDF/text RAG, không phải Agent Skill. README hiện ghi version 5/Python 3.11+, `pqa` CLI, page-level evidence, metadata/retraction check; Apache-2.0. Nó cần LLM key hoặc local server; corpora lớn có thể cần Crossref/Semantic Scholar keys. FAQ thừa nhận hệ nội bộ dùng tools/licenses không chia sẻ và kết quả có thể khác, nên chỉ dùng như worker tùy chọn với PDF/manifest riêng và log đầy đủ.

## Guardrail viết khoa học và venue

[ICMJE Recommendations](https://www.icmje.org/recommendations/) cập nhật tháng 01/2026; trang [Preparing a Manuscript](https://www.icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html) yêu cầu cấu trúc theo loại nghiên cứu, reporting guideline tương ứng, reference tới nguồn gốc, kiểm citation bằng nguồn thư mục/original source, không dùng tài liệu AI-generated làm nguồn chính, và giữ figure rõ/self-explanatory. ICMJE cũng nói rõ đây là khuyến nghị chủ yếu cho journal thành viên và phải dùng cùng hướng dẫn từng journal.

[EQUATOR writing toolkit](https://www.equator-network.org/toolkits/writing-research/) cung cấp wizard/library để chọn CONSORT, STROBE, PRISMA, STARD, CARE, ARRIVE… theo study type. Đây là discovery/reference layer; không đưa toàn bộ checklist y khoa vào mọi bài khoa học.

[Nature For Authors](https://www.nature.com/nature/for-authors) và [Nature formatting guide](https://www.nature.com/nature/for-authors/formatting-guide) chỉ được nạp khi người dùng chọn Nature/article type cụ thể. Trang Nature bị redirect trong lần fetch này; không chốt rule hiện hành từ snippet hoặc editorial cũ. Không suy “Nature style” thành English scientific default.

## Kiến trúc kế hoạch được khuyến nghị

Giữ pipeline 10 module của bản thiết kế hiện tại, chỉ gắn nguồn bổ sung như sau:

1. `brief/router`: original; nhận ngôn ngữ, audience, artifact, venue, mức bằng chứng.
2. `discover/reader`: AgentKit/nature baseline; STORM/PaperQA2 chỉ là worker tùy chọn, luôn lưu query/date/source manifest.
3. `evidence-audit`: original schema, lấy claim/evidence patterns từ K-Dense; citation worker có thể ủy quyền cho `citation-management`.
4. `reasoning`: original; tách quan sát, trích nguồn, diễn giải, suy luận và phản biện.
5. `vi-writing`: chọn lọc trussary register/locale lint; term bank và quyết định xưng hô do người dùng sở hữu.
6. `vi-taste`: original, học từ corpus tiếng Việt đã duyệt; không dùng humanizer hoặc generic Vietnamese skill làm giọng tác giả.
7. `en-scientific-writing`: chọn lọc K-Dense; nạp ICMJE/EQUATOR/Nature dưới `venue_id` riêng.
8. `visuals`: slide chọn Orchestra + native runtime; diagram chọn model contract của OpenAI, nhưng source truth và dữ liệu khoa học là original.
9. `review`: original gates: human claim review, native-speaker review, venue check, license/provenance check, render/visual regression.
10. `handoff`: chỉ báo trạng thái thật (`draft`, `evidence-pending`, `human-reviewed`, `ready-for-selected-venue`), không gọi “publish-ready” khi chưa có gate.

## Plan-only: phase, đầu ra và nghiệm thu

| Phase | Đầu ra kế hoạch | Gate nghiệm thu trước khi sang phase sau |
|---|---|---|
| P0 — source lock | Ledger nguồn, URL/path, owner, license, snapshot date/SHA, dependency/provider, được phép dùng hay chỉ reference. | Không có file/skill nào được copy khi license chưa rõ; branch `main` phải pin trước implementation. |
| P1 — evidence contract | Schema source/claim/evidence/locator/version/access/retraction/uncertainty; manifest và receipt format. | Mỗi claim mẫu có locator thật; abstract-only không bị gắn full-text; metadata match không được gọi là semantic support. |
| P2 — Vietnamese layer | Register matrix, locale lint, term bank, corpus taste, quy trình native-speaker review. | Linter bắt NFC/diacritics/number/date/ICU/register; holdout do người dùng chấm; warning không tự biến thành fact. |
| P3 — English scientific layer | Claim-to-evidence writing, uncertainty/limitations, citation audit, venue profile schema. | Không bịa citation/method/result; ICMJE/EQUATOR chỉ áp theo study type; Nature/IEEE không trộn vào generic profile. |
| P4 — editable slides | Native PPTX/slide object contract, speaker notes, source/caveat/alt metadata, render-inspect loop. | Text/table/chart/diagram còn chỉnh sửa được; slide image không được nhận là PPTX editable; figure có provenance và readable reduction. |
| P5 — truthful diagrams | Entity/relationship contract, source IDs, units/uncertainty, inferred-vs-observed flags, SVG/native export. | Semantic/topology checks pass; không dùng raster AI làm evidence; số liệu hình khớp source manifest; người domain review. |
| P6 — evaluation/release | Holdout VN/EN, citation perturbation, missing-source tests, venue-isolation tests, visual regression, cost/privacy matrix. | Có baseline không-skill và reviewer rubric; chưa có human review hoặc external resource/license approval thì trạng thái vẫn pending. |

## Tác động license, adoption và vận hành

- MIT của K-Dense/Orchestra/trussary cho phép dùng theo điều kiện license, nhưng phải giữ notice/attribution và kiểm license dependency; root MIT không tự áp cho mọi file tham chiếu.
- OpenAI plugin path chưa thiết lập license cụ thể trong lần kiểm; giữ ở reference-only. Anthropic Office modules ghi proprietary; không đưa vào bundle.
- K-Dense/Orchestra/trussary đều có nguy cơ drift khác nhau: collection lớn và provider-heavy, collection chuyên venue, hoặc repository nhỏ/bus factor thấp. Cần pin snapshot, smoke test nguồn, và kế hoạch thay thế module.
- Mọi network/API/provider phải là opt-in theo phase; lưu receipt đã redact, chi phí và nguồn; không mặc định gửi bản thảo hay corpus cá nhân ra ngoài.

## Hạn chế và câu hỏi còn mở

- Một số GitHub page/raw path và Nature page bị giới hạn/redirect trong lần fetch; các claim về source hiện dựa trên file/page đã đọc được, không khẳng định toàn bộ repository.
- Không có benchmark độc lập trên corpus tiếng Việt cá nhân, English paper của người dùng, slide PPTX thật hoặc scientific diagrams thật; numeric quality claim của skill không phải acceptance evidence.
- Chưa chốt journal/conference, article type, quartile system, license của corpus văn phong, và reviewer/domain expert. Trước P1/P3/P5 cần người dùng chọn các trường này.
- Cần xác nhận có chấp nhận Python/network/provider tùy chọn hay muốn offline-first; quyết định này thay đổi PaperQA2/citation worker nhưng không thay đổi core evidence contract.
