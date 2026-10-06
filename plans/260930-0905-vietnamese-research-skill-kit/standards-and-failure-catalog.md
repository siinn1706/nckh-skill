# Quy chuẩn có phạm vi, lỗi cần bắt và coverage blueprint

Ngày 30/09/2026, Asia/Saigon. Đây là nội dung thiết kế cho P2/P3/P4/P5, chưa phải
skill đã cài hay benchmark đã chạy. Mục tiêu là chuyển nguồn uy tín thành quyết
định và phép kiểm cụ thể; không gom hướng dẫn các journal thành một “siêu chuẩn”.

## 1. Cách tổng hợp nguồn thành rule có thể dùng

| Lớp | Điều nó quyết định | Khi nạp | Ranh giới |
|---|---|---|---|
| Kit integrity invariant | Không bịa quote/result/source; giữ uncertainty, provenance, quyền và originals | Mọi task có claim/artifact liên quan | Đây là hợp đồng kit được user chọn, không nói một tổ chức áp luật cho mọi ngành |
| Method/reporting guidance | Những mục cần báo cáo cho loại study đã chọn | Có study design tương ứng và revision rõ | Reporting đầy đủ không chứng minh study conduct tốt |
| Venue policy | Format, anonymity, limits, disclosure, AI/figure use | Chỉ một venue/year/track/article-type/stage đích | Không dùng policy của journal khác lấp chỗ trống |
| University/editorial heuristic | Clarity, argument, cohesion, hedging, paraphrase | Đúng genre và vấn đề câu/đoạn đang sửa | Advisory; không cấm tuyệt đối passive voice, cấu trúc hay từ vựng |
| Personal taste | Gu, nhịp, xưng hô, sắc thái, mức rewrite | Có brief và samples được phép | Human preference không sửa sự thật, không phải standard quốc gia |

Quy trình biên soạn: đọc trang gốc → xác định authority/scope/ngoại lệ → diễn
giải ngắn bằng English → gắn lỗi mà rule ngăn → chọn deterministic check,
semantic review hay human gate → thêm một counterexample tránh false positive.
Lưu URL/section/version/as-of và phần chưa đọc được; không biến search snippet
thành policy đã xác minh. Chỉ nạp các rule cards cần cho task theo budget P1.

Rule card tương lai chứa `rule_id`, `rule_type`, `source_url`, `source_section`,
`source_revision`, `retrieved_at`, `applies_to`, `requirement`, `exceptions`,
`check`, `severity`, `review_owner`, `recheck_trigger` và `test_ids`. Một rule
không rõ scope/revision hoặc xung đột profile ở trạng thái pending, không enforce
bằng cách lấy điều kiện chặt nhất hay lỏng nhất tùy ý. Không copy nguyên manuals.

## 2. Nguồn chọn lọc và quyết định lấy/không lấy

Nguồn và giới hạn chi tiết ở [báo cáo nghiên cứu official](../reports/researcher-260930-1706-official-standards-writing.md).
Các URL dưới đây đã được đọc trong lượt nghiên cứu 30/09/2026; Nature có giới
hạn truy cập riêng, không được coi là policy hiện hành đã resolve.

| Nguồn | Cô đọng cho kit | Không mang sang mặc định |
|---|---|---|
| [ICMJE: manuscript preparation](https://www.icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html), mục references/reporting | Citation cần đỡ statement; kiểm identity và bản gốc; study design quyết định reporting | Toàn bộ cấu trúc/author rules của medical journals cho văn học hay mọi conference |
| [COPE retraction guideline](https://members.publicationethics.org/sites/default/files/retraction-guidelines-cope.pdf), v2/2019; [Crossref versioning](https://www.crossref.org/documentation/principles-practices/best-practices/versioning/), cập nhật 2025-08-13 | Notice/version lineage và hậu quả tới dependent claims | Gộp correction với retraction; tự phán misconduct hoặc cấm thảo luận bài đã rút |
| [EQUATOR](https://www.equator-network.org/about-us/what-is-a-reporting-guideline/), [PRISMA 2020](https://www.prisma-statement.org/prisma-2020) | Chọn checklist đúng loại nghiên cứu; lưu protocol/screening khi nhận systematic | Dán PRISMA vào narrative review, hay coi checklist là chứng nhận scientific quality |
| [ASA statement](https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf), 2016 | Diễn giải p-value cùng design/effect/uncertainty; không đổi significance thành importance | Cấm p-value hoặc tự sửa mô hình thống kê mà thiếu dữ liệu/chuyên gia |
| [DORA Declaration](https://sfdora.org/read/), General Recommendation | Journal metric không thay đánh giá từng paper; rank và claim support tách biệt | Bỏ yêu cầu Q1/Q2 của user; bộ lọc vẫn giữ theo system/category/metric-year |
| [Harvard Thesis](https://writingcenter.fas.harvard.edu/thesis), [Counterargument](https://writingcenter.fas.harvard.edu/counterargument) | Luận điểm có phạm vi, căn cứ và phản biện; đoạn văn có chức năng | Bắt mọi genre, kể cả fiction, phải có thesis/counterargument cùng khuôn |
| [UNC Passive Voice](https://writingcenter.unc.edu/tips-and-tools/passive-voice/) | Chọn voice theo actor/focus/clarity | Regex cấm passive hoặc thay tất cả câu Methods sang active |
| [Purdue Paraphrasing](https://owl.purdue.edu/owl/research_and_citation/using_research/quoting_paraphrasing_and_summarizing/paraphrasing.html) | Ghi nhận nguồn và kiểm diễn đạt có giữ nghĩa; phân biệt quote/paraphrase | Đổi vài từ thành “original”; suy intent/đạo văn từ similarity score |
| [Manchester cautious](https://www.phrasebank.manchester.ac.uk/using-cautious-language/), [critical](https://www.phrasebank.manchester.ac.uk/being-critical/) | Rhetorical moves/hedging phù hợp evidence; gợi ý cách nêu giới hạn | Chép phrasebank nguyên kho hoặc thêm hedge để che unsupported claim |
| [Tạp chí Khoa học ĐH Mở TP.HCM](https://journalofscience.ou.edu.vn/vi/guidelines/article-types) | Ví dụ tiếng Việt về cấu trúc theo article type và lời khuyến nghị | Coi word count/reference count hay giọng của một venue là luật tiếng Việt |
| [IEEE/QCE26 policy](https://qce.quantum.ieee.org/2026/wp-content/uploads/sites/13/2026/03/QCE26-IEEE-Author-Policies-with-genAI.pdf), 2026 | Mẫu profile có AI-generated content disclosure và phân biệt grammar editing | Áp lên mọi hội nghị; coi disclosure tự nó làm figure đúng khoa học |
| [Nature AI policy](https://www.nature.com/nature-portfolio/editorial-policies/ai) | Target-policy lookup khi venue phù hợp | Trang bị lỗi/redirect trong lượt này: giữ `policy_unverified`, không suy blanket ban hay ngoại lệ từ editorial/snippet |
| [Anthropic reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) | Cho phép không biết, grounding bằng đoạn nguồn, kiểm claim sau draft | Không hứa loại hết hallucination; không bắt chain-of-thought transcript hay best-of-N mặc định |

Nguồn official xác định policy của chính chủ; không tự làm mọi câu trên trang
thành đúng tuyệt đối. Hướng dẫn viết uy tín vẫn cần thử trên genre, tiếng Việt và
gu người dùng. Chưa có nguồn đủ căn cứ cho một quy chuẩn “taste Việt” phổ quát.

## 3. Failure catalog: dùng làm test, không tuyên bố tần suất đã đo

Các lỗi dưới đây được chọn theo rủi ro của workflow và blueprint, không phải bảng
xếp hạng lỗi AI phổ biến có thống kê. `Block` nghĩa là không nhận artifact/claim
cho scope tương ứng; draft còn thiếu vẫn có thể bàn giao với trạng thái rõ.

| ID / failure | Rule và căn cứ | Kiểm/owner | Boundary hoặc negative control |
|---|---|---|---|
| F01 Invented source/DOI | Kit integrity; ICMJE references | Identity lookup + exact source, P2 block | DOI thật vẫn chưa chứng minh entailment |
| F02 Citation đúng tên nhưng không đỡ câu | Claim-bound support; ICMJE | Reader locator + semantic review P2 | Metadata-only chỉ đỡ identity/status |
| F03 Quote/page/edition sai | Exact text/version; blueprint literary mode | Locator/original/edition match, OCR visual check | Ghi rõ paraphrase không bị kiểm như quote nguyên văn |
| F04 Bài đã sửa/rút nhưng cache còn accepted | COPE/Crossref lineage | Notice/status freshness + invalidate dependents | Có thể cite để bàn chính retraction, không dùng như kết quả còn đáng tin |
| F05 Association thành causality | Kit fidelity; ASA/reporting context | Claim type/design/scope diff + domain reviewer | Không cấm causal claim đã có cơ sở thích hợp |
| F06 p-value thành effect/importance | ASA | Giữ effect/CI/model context và phân biệt SD/SE/CI | Không cấm thống kê kiểm định |
| F07 “May/suggests” thành “proves”, bỏ phủ định | P2 wording matrix; Manchester cautious | Semantic + deterministic anchors, P3 | Không ép hedge mọi quan sát trực tiếp |
| F08 Sai đơn vị, mẫu số, số hay nhãn sau dịch | Kit fidelity | Structured quantities/terms diff P3/P4 | Quy đổi có công thức/nguồn/rounding được phép thì giữ provenance |
| F09 Rank thay cho scientific evidence | DORA + user journal-strict policy | Separate ranking and support records P2 | Q1/Q2 vẫn là filter người dùng chọn; không có “Q1 conference” |
| F10 Kết luận gap ngoài corpus/search | Kit evidence scope; Harvard argument | Search log, inclusion/exclusion, bounded gap P2 | “Chưa thấy trong tập đã khảo sát” khác “chưa ai nghiên cứu” |
| F11 Checklist/format của venue khác rò sang task | EQUATOR/PRISMA + selected venue | Profile key/change reset; compliance pending on conflict | Reporting layer có thể đi kèm venue, nhưng không nhập thành luật chung |
| F12 Patchwriting/ý mượn mất attribution | Purdue + selected venue rules | Source comparison and human review P3/P5 | Phrase phổ thông không tự chứng minh đạo văn; không dùng detector verdict |
| F13 Văn chung chung, dịch cứng, lặp hoặc giả chiều sâu | Blueprint taste + Harvard/UNC heuristics | Critic giải thích chỗ sửa và phương án; human taste | Không cấm danh sách từ, passive hay Hán–Việt tuyệt đối |
| F14 Polish thêm fact nhưng tự nhận style-only | Approved factual-delta contract | Compare output claims, gửi phần đổi về P2 | Fiction giữ fiction; không web-check mọi hình ảnh văn chương |
| F15 Literature interpretation giả làm fact/quote | Primary-text-first blueprint | Edition/passage → observation → interpretation P2 | Một cách đọc có căn cứ có thể khác critic, không phải lỗi chỉ vì bất đồng |
| F16 Ảnh sinh giả kết quả hoặc diagram sai topology | Kit visual truth + selected figure policy | Source-to-mark/arrow/data map + domain review P4 | Artwork được ghi rõ vẫn phải qua venue permission; không giả measurement |
| F17 PPTX chỉ là ảnh, hoặc QA của bản cũ | Editable contract + approved exact-version QA | Native object/round-trip/render/hash check P4 | Nếu user chỉ cần raster, không bắt native editable |
| F18 Nguồn độc hại đổi tools/quyền | Kit authority + host permissions | Source isolation and actual enforcement P1/P2 | Delimiter hay lời nhắc không được gọi là sandbox |
| F19 Gộp mọi gate thành verified/human-reviewed | Approved aggregate contract | P5 required-gates check, no silent scope removal | `not-applicable` phải có lý do từ brief |
| F20 Tràn context/chi phí do agent/hook/cache | User budget + runtime docs | Pool accounting/dispatch preflight P1/P5 | Cached tokens vẫn chiếm window; không có telemetry thì không nhận tiết kiệm |

Mỗi failure cần ít nhất một positive case và một counterexample theo boundary
trong eval manifest; đủ coverage chưa có nghĩa đã có human gold. Theo P5, synthetic
guards không thay bài thật có quyền sử dụng hoặc reviewer đủ chuyên môn.

## 4. Blueprint capability → module/mode → output/test

<!-- Updated: approved red-team finding 11; user approval 2026-09-30. -->

| Blueprint capability | Owner/module/mode | Output và acceptance đã phân công |
|---|---|---|
| `vi-writing` | P3 `vi-writing` draft/edit | VI draft + factual/style diff; F07/F08/F13/F14 |
| `vi-taste` | P3 taste critic | Rubric/alternatives + human decision; không self-score gold |
| `vi-polishing` | P3 polish/minimal-diff mode | Protected regions, minimal patch; F14 |
| `evidence-first`, epistemic rules | P1 contracts + P2 shared workflow | Source/evidence/claim separation; F01/F02/F19 |
| `claim-verifier` | P2 `evidence-audit` support mode | Verdict/counterevidence/allowed wording; F02/F05/F07 |
| `citation-auditor` | P2 citation/quote mode | Metadata, locator, quote, status audit; F01/F03/F04 |
| `fact-checker` | P2 factual mode | Official/primary-source fact ledger; unknown remains visible |
| `research-reader` | P2 reader | Exact version/anchors/method/limits/evidence cards |
| `literature-review` | P2 discovery + reasoning review mode | Search/screening log, synthesis matrix; F10/F11 |
| `research-gap` | P2 scoped gap mode | Gap supported within searched corpus; F10 |
| `research-methodology` | P2 reasoning method mode | Question/design/assumptions/limits; no invented methods/results |
| `argument-architect` | P2 argument mode | Claim–evidence–reason–limitation/counterargument outline |
| `comparison-engine` | P2 comparison mode | Common comparison axes, missing data and differences; no false equivalence |
| `terminology-manager` | P3 task-scoped shared glossary | VI/EN definition/variants/owner, consumed by P2/P4; F08 |
| `peer-reviewer` R1–R4 | P5 review with logic/evidence/VI/domain lenses | Prioritized findings; model critic is not actual journal peer review |
| `final-audit` | P5 `research-review` | Gate matrix, scope status, open items; F19 |
| Shared VI style / anti-pattern library | P3 profiles + P2 failure registry | Original bad/why/better pairs, genre scope; F13 |
| Taste corpus / taste score | P3 sample-rights, P5 holdout | Licensed samples, human rubric, exposure/lineage; score diagnostic only |
| Literary studies / literary citations | P2 primary-text mode + P3 writing | Exact edition/translator/line/chapter, four claim types; F03/F15 |
| Blueprint workflow/permissions/roadmap | P1 plan/cook + phase DAG | Small-task fast path, locked scope, ownership and full coverage |
| User additions beyond blueprint | P1 automatic routing/hooks/cost; P3 EN; P4 visuals | Plan→cook without tags, context caps, bilingual fidelity, editable artifact QA |

Không tạo thêm entrypoint chỉ để giữ nguyên mọi tên trong blueprint. Cách gộp
chỉ thay giao diện gọi, không bỏ năng lực. `research-plan` vẫn được ghi research/
validation/journal trong scope, nhưng không tự chạy các bước implementation ở bảng.

## 5. Cách giữ bộ chuẩn nhỏ và còn cập nhật được

P2 owns registry, P3/P4/P5 đọc các card cần thiết. Chọn theo task risk/genre,
không tải toàn bộ catalog vào mỗi request. Một card chỉ giữ điều thực sự làm
thay đổi quyết định và link nguồn gốc; nguồn dài nằm ngoài context, fetch đúng
section khi cần kiểm. Recheck khi đổi venue/year/study type, nhận notice/update,
resume theo freshness policy và trước venue-facing handoff.

Chưa có venue/profile đích hoặc nguồn bị chặn thì giữ generic draft/policy-pending,
không báo compliant. Chưa có personal corpus/human review thì giữ neutral register.
Các quyết định đó được hỏi ở task tương ứng, không buộc user chọn một journal,
ngân sách tiền hay giọng mẫu cho toàn kit trong lượt plan này.
