# Shortlist nguồn thật cho NCKH skills

**Thời điểm nghiên cứu:** 2026-10-03, Asia/Saigon  
**Phạm vi:** tìm nguồn có thật cho mẫu văn VI/EN, fidelity khoa học, số đo biểu đồ và task engineering/marketing.  
**Trạng thái:** nghiên cứu và acquisition plan; chưa tải, nhập, đóng gói hay sửa registry/package.

## Kết quả ngắn

Đây là shortlist theo **độ phù hợp với consumer, provenance và khả năng giữ quyền**, không phải bảng xếp hạng chất lượng toàn cầu. Thứ tự triển khai khuyến nghị:

1. **VI genre:** bốn trang/bản quét Wikisource được pin bằng oldid/file URL. Đây là nguồn thực, đọc được, có thông tin tác phẩm và quyền ở cấp trang; cần giữ cảnh báo public-domain theo jurisdiction và chất lượng transcription/OCR.
2. **EN scientific writing:** PMC Open Access Subset, lọc **từng bài** theo license cho phép; đây là nguồn prose khoa học thật tốt nhất trong shortlist. Dùng SciFact cho claim–evidence fidelity, không dùng nó làm corpus văn phong rộng.
3. **Translation fidelity:** Tatoeba Challenge `v2023-09-26`, chỉ dùng dev/test `eng-vie` sau khi kiểm manifest và license từng câu. Tatoeba tự nói bản dịch không được chuyên gia bảo đảm và nội dung không được fact-check.
4. **Chart measurements:** World Bank Data API là lựa chọn chính vì có indicator, country, year, value và metadata. OWID Grapher là lớp thuận tiện cho CSV/metadata và chart reader, nhưng vẫn phải lưu nguồn gốc/giấy phép dữ liệu upstream.
5. **Reusable engineering tasks:** SWE-bench là nguồn task thật từ issue GitHub, nhưng chỉ nên dùng metadata/private consumption hoặc subset đã kiểm license từng repository. Không được gom mọi task dưới MIT của tooling.
6. **Reusable marketing tasks:** UCI Bank Marketing là lựa chọn đầu tiên cho campaign/analytics; Online Retail là bổ sung cho RFM/segmentation. Cả hai là dữ liệu hành vi/transaction, không phải corpus copy quảng cáo.

Không có nguồn nào trong báo cáo này tự tạo mẫu, nhãn, số đo, bản dịch, human gold hay claim chất lượng. Các nguồn chỉ trở thành local resource sau khi có consumer, schema, rights review, snapshot và hash.

## Mục lục

- [Tiêu chí và kiểm tra độc lập](#tiêu-chí-và-kiểm-tra-độc-lập)
- [Shortlist acquisition-ready](#shortlist-acquisition-ready)
  - [Tiếng Việt: prose và genre](#tiếng-việt-prose-và-genre)
  - [Tiếng Anh khoa học và fidelity](#tiếng-anh-khoa-học-và-fidelity)
  - [Đo lường biểu đồ](#đo-lường-biểu-đồ)
  - [Engineering tasks](#engineering-tasks)
  - [Marketing tasks](#marketing-tasks)
- [Trade-off và adoption risk](#trade-off-và-adoption-risk)
- [Trình tự acquisition có giới hạn](#trình-tự-acquisition-có-giới-hạn)
- [Standards và taste phải tách riêng](#standards-và-taste-phải-tách-riêng)
- [NO-GO](#no-go)
- [Câu hỏi chưa giải quyết](#câu-hỏi-chưa-giải-quyết)

## Tiêu chí và kiểm tra độc lập

### Tiêu chí xếp hạng

- **Credibility:** ưu tiên cơ quan/chủ sở hữu nguồn, repository/dataset release và license chính thức; README quảng bá, stars và bản mirror chỉ là locator.
- **Provenance:** mỗi record cần source locator, title/ID, tác giả hoặc upstream, version/oldid/revision, thời điểm tải và SHA-256 của bytes đã giữ.
- **Rights:** quyền của từng record/file thắng quyền của repository bao ngoài. “Public”, “Open Access” hoặc “có trên GitHub” không tự đồng nghĩa với quyền redistribution.
- **Consumer fit:** chỉ chọn nguồn có consumer cụ thể trong NCKH; không ép clinical corpus vào CS, UI heuristic vào scientific truth, hay transaction data vào copywriting.
- **Reproducibility:** ưu tiên route có snapshot bất biến hoặc có thể lưu response/archive; mutable `latest`, `main` và API phải được hash và ghi `as-of`.

### Cross-check độc lập đã dùng

| Claim/lane | Các nguồn độc lập đã đối chiếu | Kết luận được phép |
|---|---|---|
| Wikisource VI | Trang tác phẩm và oldid; [Wikimedia Terms of Use](https://foundation.wikimedia.org/wiki/Terms_of_Use); [CC BY-SA text](https://foundation.wikimedia.org/wiki/Legal%3AText_of_the_Creative_Commons_Attribution-ShareAlike_4.0_International_License/en) | Giữ text/page provenance và attribution; public-domain rationale của tác phẩm là tuyên bố ở trang, phải kiểm jurisdiction khi phát hành. |
| PMC | [OA Subset overview](https://pmc.ncbi.nlm.nih.gov/tools/openftlist/); [NCBI retrieval/API guidance](https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/); [Europe PMC downloads](https://europepmc.org/downloads) | Có route retrieval chính thức; license khác nhau theo bài, chỉ chọn allowlist và dùng API/Cloud/OAI/BioC được nêu. |
| SciFact | [README/release](https://github.com/allenai/scifact); [primary LICENSE](https://raw.githubusercontent.com/allenai/scifact/master/LICENSE.md); [data.tar.gz](https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz); paper [Fact or Fiction](https://arxiv.org/abs/2004.14974) | Claims/annotations và abstracts có các license khác nhau; phải ghi conflict với dataset card trước khi release. |
| Tatoeba | [Challenge release README](https://github.com/Helsinki-NLP/Tatoeba-Challenge/blob/master/README-v2023-09-26.md); [dev/test route](https://object.pouta.csc.fi/Tatoeba-Challenge-devtest/); [Tatoeba Terms](https://tatoeba.org/en/terms_of_use) | Có release/split thật và license mặc định, nhưng license có thể theo từng câu; chất lượng/bản dịch/fact checking không được bảo đảm. |
| Chart data | [World Bank API](https://api.worldbank.org/v2/country/VNM/indicator/SP.POP.TOTL?format=json); [World Bank terms](https://data.worldbank.org/summary-terms-of-use); [OWID metadata](https://ourworldindata.org/grapher/population-density.metadata.json?v=1&csvType=full&useColumnShortNames=false) | World Bank cho số đo có indicator/year/value; OWID cung cấp processed chart layer và original-source citations, không thay thế primary source. |
| UCI marketing | [Bank Marketing page](https://archive.ics.uci.edu/dataset/222/bank); DOI [10.24432/C5K306](https://doi.org/10.24432/C5K306); [Online Retail page](https://archive.ics.uci.edu/dataset/352/online%2Bretail) | UCI page ghi nguồn, file, biến và CC BY 4.0; dùng đúng task context và giữ disclosure/leakage. |
| Engineering | [SWE-bench repository](https://github.com/SWE-bench/SWE-bench); [dataset guide](https://github.com/SWE-bench/SWE-bench/blob/main/docs/guides/datasets.md); [HF dataset](https://huggingface.co/datasets/SWE-bench/SWE-bench) | Task/patch/test là thật nhưng quyền nằm cả ở từng upstream repository; tooling MIT không bao trùm mọi task bytes. |

Đây là cross-check của **source facts và rights route**, không phải ba đánh giá độc lập chứng minh writing quality, scientific truth hay model uplift.

## Shortlist acquisition-ready

### Tiếng Việt: prose và genre

#### 1. `Tài mạng tương đố` — ưu tiên cao nhất cho prose/novel

- **Locator:** [trang](https://vi.wikisource.org/wiki/T%C3%A0i_m%E1%BA%A1ng_t%C6%B0%C6%A1ng_%C4%91%E1%BB%91), pinned [oldid 179667](https://vi.wikisource.org/w/index.php?title=T%C3%A0i_m%E1%BA%A1ng_t%C6%B0%C6%A1ng_%C4%91%E1%BB%91&oldid=179667). Trang cho biết đây là tác phẩm 1926, thể loại tiểu thuyết, có hai quyển.
- **Provenance:** giữ title, author, publication year, oldid, revision timestamp, từng volume/link và raw bytes. Trang hiện được ghi sửa lần cuối 2024-09-29.
- **Rights:** page ghi tác phẩm public domain ở Hoa Kỳ vì phát hành trước 1931 và nêu author mất năm 1947 cho các jurisdiction có life+75/shorter-term rationale. Text của Wikisource được phát hành theo CC BY-SA; page-level license và underlying-work status phải lưu riêng.
- **Consumer:** `nckh-write`, `nckh-taste`; genre/register sample, historical prose, không phải human-gold hiện đại.
- **Acquisition:** lấy page/revision qua oldid hoặc MediaWiki API pinned revision; lưu response, encoding, SHA-256 và attribution. Không tự chuẩn hóa chính tả trong bytes gốc.
- **Limit:** Wikisource là transcription cộng đồng; public-domain statement của trang không thay thế legal review ở nơi phát hành.

#### 2. `Thầy trò trong khám` — translation/register có cảnh báo incompleteness

- **Locator:** [trang](https://vi.wikisource.org/wiki/Th%E1%BA%A7y_tr%C3%B2_trong_kh%C3%A1m), pinned [oldid 106841](https://vi.wikisource.org/w/index.php?title=Th%E1%BA%A7y_tr%C3%B2_trong_kh%C3%A1m&oldid=106841).
- **Provenance:** bản dịch tiếng Việt của Phan Khôi từ *Le Comte de Monte Cristo*; giữ source-work attribution, translator, oldid và volume/issue metadata.
- **Rights:** trang nêu source và translation public domain theo các quy tắc được trang dẫn; kiểm lại jurisdiction và giữ nguyên attribution/license notice của Wikisource.
- **Consumer:** `nckh-write`, `nckh-taste`; translation/register comparison.
- **Limit:** Wikisource cảnh báo bản collected thiếu issue XIV và bản dịch đầy đủ có thể incomplete. Không gọi đây là canonical complete translation, không dùng làm coverage benchmark nếu chưa xác minh.

#### 3. `Truyện Kiều (bản Trương Vĩnh Ký 1911)` — verse và historical orthography

- **Locator:** [trang](https://vi.wikisource.org/wiki/Truy%E1%BB%87n_Ki%E1%BB%81u_%28b%E1%BA%A3n_Tr%C6%B0%C6%A1ng_V%C4%A9nh_K%C3%BD_1911%29), pinned [oldid 80653](https://vi.wikisource.org/w/index.php?title=Truy%E1%BB%87n_Ki%E1%BB%81u_(b%E1%BA%A3n_Tr%C6%B0%C6%A1ng_V%C4%A9nh_K%C3%BD_1911)&oldid=80653).
- **Provenance:** bản 1911 có verse, prose summary, notes và orthography lịch sử; giữ page structure/notes, không trộn với prose Việt hiện đại.
- **Rights:** page tuyên bố bản gốc 1911 và translation public domain theo rationale của page; text Wikisource vẫn cần attribution/CC BY-SA record.
- **Consumer:** `nckh-write`, `nckh-taste`; literary/poetic register and historical spelling.
- **Limit:** đây là nguồn văn học/thi ca; không dùng để kết luận modern Vietnamese naturalness.

#### 4. `Thơ ngụ ngôn (1928)` — scan cần OCR gate

- **Locator:** [file page](https://vi.wikisource.org/wiki/T%E1%BA%ADp_tin:Th%C6%A1_ng%E1%BB%A5_ng%C3%B4n_%281928%29_by_%C4%90%E1%BB%93_Nam_T%E1%BB%AD_%28Nguy%E1%BB%85n_Tr%E1%BB%8Dng_Thu%E1%BA%ADt%29.pdf), [original PDF](https://upload.wikimedia.org/wikipedia/commons/0/07/Th%C6%A1_ng%E1%BB%A5_ng%C3%B4n_%281928%29_by_%C4%90%E1%BB%93_Nam_T%E1%BB%AD_%28Nguy%E1%BB%85n_Tr%E1%BB%8Dng_Thu%E1%BA%ADt%29.pdf).
- **Provenance:** file page nêu Gallica identifier `bpt6k4242640k`, Nguyễn Trọng Thuật (1883–1940), Hà Nội, 1928, 66 trang. Page báo SHA-1 `1bd491fc054b2170bc26a71884aed123c788f2f9`; acquisition phải tự tính SHA-256 của file tải về.
- **Rights:** Commons page đánh dấu public domain ở Việt Nam và Hoa Kỳ theo rationale của page; lưu page license/attribution cùng scan.
- **Consumer:** `nckh-write`, `nckh-taste`; fable/poetry genre.
- **Limit:** scan, OCR và transcription là ba artifacts khác nhau. OCR sai không được âm thầm sửa thành “nguyên bản”.

**VI scope boundary:** chưa có quota genre hiện đại/đương đại do owner chỉ định. Vietnamese Wikipedia dump (`https://dumps.wikimedia.org/viwiki/latest/`) không được chọn làm prose corpus: nó là encyclopedic dump, còn `viwikisource/latest` chưa có route đã kiểm trong lượt này. Oldid-bounded acquisition an toàn và nhỏ hơn.

### Tiếng Anh khoa học và fidelity

#### 5. PMC Open Access Subset — nguồn prose khoa học chính

- **Official route:** [OA Subset overview](https://pmc.ncbi.nlm.nih.gov/tools/openftlist/), [NCBI retrieval/API](https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/), [Europe PMC downloads](https://europepmc.org/downloads), [PMC OAI endpoint](https://pmc.ncbi.nlm.nih.gov/api/oai/v1/mh/).
- **Content fit:** JATS/XML và section thật gồm abstract, methods, results, tables, units, negation, uncertainty và causal language. Phù hợp `nckh-write`, `nckh-evidence`, `nckh-method`, `nckh-visuals`.
- **Rights:** PMC nói OA Subset gồm bài/preprint có Creative Commons hoặc license tương tự, nhưng **không phải mọi bài trong PMC đều được text-mining/reuse** và license khác nhau theo article. Chỉ cho allowlist, ưu tiên CC BY; lưu article-level license statement. Không suy ra quyền từ nhãn “PMC Open Access”.
- **Retrieval:** automated/bulk retrieval chỉ qua PMC Cloud, OAI-PMH, E-Utilities hoặc BioC như trang chính thức nêu; không scrape HTML.
- **Snapshot:** lọc English research article và license trước, giữ PMCID/DOI, article URL, publisher/license statement, JATS/XML bytes, retrieval date, API query và SHA-256. `latest`/search result không đủ làm version.
- **Limit/adoption risk:** hạ tầng NCBI/Europe PMC ổn định, nhưng domain nghiêng biomedical/life sciences và license fragmentation làm packaging phức tạp. Không dùng làm corpus CS tổng quát hay human taste gold.

#### 6. SciFact — claim/evidence fidelity có annotation rõ

- **Locator/download:** [repository](https://github.com/allenai/scifact), [dataset tarball](https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz), [claims with citances](https://scifact.s3-us-west-2.amazonaws.com/release/latest/claims_with_citances.jsonl), [paper](https://arxiv.org/abs/2004.14974).
- **Content fit:** expert-written scientific claims ghép với abstract có evidence, labels và rationales; phù hợp `nckh-evidence`, `nckh-method` và factual-slot checks của `nckh-write`.
- **Rights from primary LICENSE:** `claims_*.jsonl` và evidence annotations là CC BY 4.0; abstracts trong `corpus.jsonl` thuộc S2ORC và ODC-By 1.0; code Apache-2.0. Giữ ba rights classes tách nhau.
- **Conflict:** Hugging Face dataset card được quan sát ghi CC BY-NC 2.0, khác primary `LICENSE.md`. Chưa được phép chọn một bên để phát hành; acquisition phải lưu cả hai statements, xác minh release bytes và xin owner/legal decision.
- **Snapshot:** không dùng mù `release/latest`; resolve release/commit nếu có, lưu tarball và `claims_with_citances.jsonl` hash, row count, schema, source URL.
- **Limit:** labels/rationales là task annotations, không phải human gold cho văn phong, không bảo đảm mọi claim đúng trong mọi domain, và không phải corpus prose rộng.

#### 7. Tatoeba Challenge `v2023-09-26` — smoke test song ngữ, không phải scientific corpus

- **Release:** [README](https://github.com/Helsinki-NLP/Tatoeba-Challenge/blob/master/README-v2023-09-26.md), [dev.tar](https://object.pouta.csc.fi/Tatoeba-Challenge-devtest/dev.tar), [test.tar](https://object.pouta.csc.fi/Tatoeba-Challenge-devtest/test.tar). README release nói có nhiều language pairs, trong đó cần kiểm manifest `eng-vie` tại acquisition.
- **Rights:** release README phân biệt dev/test CC BY 2.0 FR và training CC BY-NC-SA 4.0; [Tatoeba Terms](https://tatoeba.org/en/terms_of_use) nói text mặc định CC BY 2.0 FR nhưng license có thể theo từng sentence/author. Lưu sentence ID, author và license; không gộp thành một license chung nếu chưa kiểm.
- **Consumer:** `nckh-write`, `nckh-evidence`, translation fidelity smoke test: preservation of numbers, names, negation, units and meaning slots.
- **Limit:** Tatoeba nói contributor là volunteer, translations không được professional guarantee, và sentence content/meaning không được fact-check. Không gọi dev/test là human gold, không dùng factual truth benchmark.
- **Snapshot:** giữ release README revision, tar bytes, pair manifest, split, sentence IDs và hash. Chỉ dùng dev/test theo sequence; training chưa được chọn.

### Đo lường biểu đồ

#### 8. World Bank Data API — lựa chọn chính

- **Concrete endpoint:** `https://api.worldbank.org/v2/country/VNM/indicator/SP.POP.TOTL?format=json`.
- **Observed response:** response có `indicator`, `country`, `date`, `value`, `unit`, `obs_status`, `decimal`; snapshot được quan sát ghi `lastupdated: 2026-07-13` và dãy Việt Nam 1976–2025. Đây là quan sát của response tại thời điểm nghiên cứu, không phải cam kết dữ liệu tương lai.
- **Rights:** [summary terms](https://data.worldbank.org/summary-terms-of-use) và [public licenses](https://datacatalog.worldbank.org/public-licenses) nêu default CC BY 4.0 với attribution/dispute terms bổ sung; indicator từ bên thứ ba có thể có điều kiện khác.
- **Consumer:** `nckh-visuals`, `nckh-analytics`, `nckh-method`; có unit/metric/window/source để dựng chart measurement record.
- **Snapshot:** lưu URL/query, response bytes, retrieval date/timezone, `lastupdated`, indicator metadata, country, unit, source page và SHA-256. Gắn `as-of`; không ghi “current” sau snapshot.
- **Limit/adoption risk:** API chính thức và khá ổn định; revisions có thể đổi historical values. JSON route không mặc nhiên thỏa consumer cần CSV; đây là câu hỏi chưa giải quyết.

#### 9. Our World in Data Grapher — chart reader thuận tiện, không phải primary measurement authority

- **Routes:** [chart](https://ourworldindata.org/grapher/life-expectancy), [CSV](https://ourworldindata.org/grapher/population-density.csv?v=1&csvType=full&useColumnShortNames=false), [metadata](https://ourworldata.org/grapher/population-density.metadata.json?v=1&csvType=full&useColumnShortNames=false), [licensing](https://ourworldindata.org/licensing).
- **Provenance:** metadata quan sát được ghi title, unit, timespan, `lastUpdated`, source citations và processing description. Ví dụ population density kết hợp HYDE, Gapminder, UN WPP và FAO; đây là processed/aggregated layer.
- **Rights:** OWID charts/data/code của OWID được CC BY theo licensing page; third-party source data giữ license gốc. Mỗi column/source cần rights record riêng.
- **Consumer:** `nckh-visuals`, `nckh-analytics`; CSV/metadata thuận tiện cho chart QA, citation and source-map.
- **Limit:** không thay World Bank/UN/FAO primary measurement. CSV/metadata mutable; pin query, downloaded bytes, metadata hash và source citation.

### Engineering tasks

#### 10. SWE-bench — real issue-to-patch task

- **Locator:** [repository](https://github.com/SWE-bench/SWE-bench), [dataset guide](https://github.com/SWE-bench/SWE-bench/blob/main/docs/guides/datasets.md), [Hugging Face dataset](https://huggingface.co/datasets/SWE-bench/SWE-bench), [tooling license](https://raw.githubusercontent.com/SWE-bench/SWE-bench/main/LICENSE).
- **Content fit:** issue/problem statement, repository, base commit, patch/test patch, fail-to-pass và pass-to-pass tests. Phù hợp `nckh-scout`, `nckh-debug`, `nckh-fix`, `nckh-test`.
- **Rights:** MIT của SWE-bench áp dụng tooling/repository files được cấp dưới MIT; issue text, repository snapshot, patch và fixture có thể chịu license riêng của từng upstream repo. Không redistribution toàn bộ task dưới MIT nếu chưa kiểm từng repo.
- **Snapshot:** pin HF dataset revision; lưu row count/hash; pin từng `repo` + base commit; giữ issue URL và upstream LICENSE/NOTICE. Ưu tiên metadata hoặc private local consumption khi không cần phát hành bytes.
- **Limit/adoption risk:** benchmark được dùng rộng nhưng `main`, docs và HF viewer hiện có count khác nhau (docs nêu khoảng 2,294; viewer quan sát khoảng 2.5k). Đây là drift/revision issue, không phải lỗi để tự chọn con số. Heterogeneous repos làm legal/acquisition complexity cao.
- **Rejected comparison:** BugsInPy không được khuyến nghị vì official repository issue được tìm thấy không đưa ra license rõ ràng. Không đóng gói cho tới khi rights statement cụ thể được xác minh.

### Marketing tasks

#### 11. UCI Bank Marketing — ưu tiên cho campaign/response analytics

- **Locator:** [UCI page](https://archive.ics.uci.edu/dataset/222/bank), DOI [`10.24432/C5K306`](https://doi.org/10.24432/C5K306), file download `bank.zip`/`bank-additional.zip` từ official page.
- **Content fit:** direct phone marketing campaigns của một Portuguese bank; page ghi variants 41,188 và 45,211 rows, campaign history, contact fields, previous outcomes và target subscription. Phù hợp `nckh-market-research`, `nckh-marketing-plan`, `nckh-campaign`, `nckh-analytics`.
- **Rights:** official UCI page ghi CC BY 4.0. Lưu citation, DOI, page snapshot, download URL, file hashes và variable metadata.
- **Critical limitation:** `duration` được đo sau khi contact xảy ra và có thể leak target. Prospective prediction phải loại biến này hoặc ghi rõ đây là retrospective task. Context chỉ là một Portuguese bank/campaign; không suy ra campaign uplift chung.

#### 12. UCI Online Retail — bổ sung cho RFM/segmentation

- **Locator:** [UCI page](https://archive.ics.uci.edu/dataset/352/online%2Bretail), DOI/page download route từ UCI.
- **Content fit:** real transaction rows với invoice/date, quantity, unit price, customer/country và product identifiers; phù hợp `nckh-market-research`, `nckh-marketing-plan`, `nckh-analytics` cho RFM, cohort và segmentation.
- **Rights:** page UCI ghi CC BY 4.0; giữ DOI/page snapshot/file hash và attribution.
- **Limit:** đây là purchase/transaction data, không phải campaign copy, creative asset hay causal response experiment. Customer identifiers/context cần privacy review trước khi đưa vào bất kỳ release nào.

## Trade-off và adoption risk

| Candidate | Rights clarity | Provenance | Data/genre fit | Acquisition complexity | Maintenance/drift | Architecture fit | Adoption risk |
|---|---|---|---|---|---|---|---|
| Wikisource oldid bundle | Trung bình; page CC BY-SA, underlying PD theo jurisdiction | Cao nếu pin oldid/page/file và hash | Cao cho VI historical prose/verse; thấp cho modern prose | Thấp–vừa; page/API, scan/OCR tách | Revision/transcription drift | Cần reader text/PDF và license ngoài MIT/Apache hiện tại | Cộng đồng và legal interpretation không đồng nhất |
| PMC CC BY article subset | Cao sau per-article allowlist; không đồng nhất toàn PMC | Rất cao: PMCID/DOI/JATS/license | Cao cho EN scientific prose/factual slots; biomedical bias | Vừa–cao; API/Cloud/OAI/BioC, filtering | Articles/metadata và license statements thay đổi | Hợp JATS/XML nhưng cần per-record rights schema | License fragmentation, publisher version mismatch |
| SciFact | Trung bình–cao nhưng có conflict primary LICENSE vs HF card | Cao khi pin release/tar/hash | Cao cho claim/evidence; thấp cho broad style | Thấp–vừa; tarball + schema | `release/latest` mutable; card/release drift | JSONL hợp reader, ODC-By/CC BY support phải xác minh | Benchmark cũ, license conflict chưa đóng |
| Tatoeba dev/test | Trung bình; per-sentence license, volunteer contributions | Cao nếu giữ ID/author/split | Vừa cho bilingual fidelity; thấp cho truth/style gold | Vừa; tar/pair manifest/license scan | Dev/test updates và terms có thể đổi | Hợp split/JSONL sau per-record rights | Quality không chuyên nghiệp, possible rights exceptions |
| World Bank API | Cao theo terms nhưng third-party exceptions | Rất cao: indicator/country/date/value/API | Rất cao cho measured charts | Thấp; request + response hash | Historical revisions/API schema drift | JSON/API support cần reader; CSV unknown | Stable provider nhưng values can revise |
| OWID Grapher | Trung bình–cao; OWID vs original-source rights tách | Cao với metadata/citation | Cao cho chart QA; không primary | Thấp; CSV + metadata | Processed data and metadata update | CSV/JSON easy, but preserve source chain | Aggregation choices and source drift |
| SWE-bench | Thấp–trung bình toàn bộ; per-repo rights bắt buộc | Cao task/base commit | Cao real engineering tasks | Cao; many repos/commits/licenses | Dataset/main/HF counts and tasks drift | Metadata/private consumption best | Rights heterogeneity, runtime cost, benchmark churn |
| UCI Bank Marketing | Cao: official CC BY 4.0 + DOI | Cao: UCI page/files/variables | Cao campaign/analytics, not copy | Thấp; official zip | Dataset stable, context old | CSV fits analytics reader | Leakage/misuse across contexts |
| UCI Online Retail | Cao: official CC BY 4.0 + DOI | Cao: UCI page/file metadata | Cao transaction/RFM, not campaign text | Thấp | Mostly stable; privacy context review | CSV fits analytics reader | Identifier/privacy and external validity |

**Kiến trúc hiện tại:** registry đang quen với copied upstream, full Git commit, `csv/jsonl/json/markdown/svg` và MIT/Apache pins. CC BY-SA, ODC-By, CC BY 2.0 FR, CC BY-NC-SA 4.0, per-article licenses, static HTTPS/API snapshots và per-repository rights là **support gaps cần một thay đổi hẹp sau này**. Trước thay đổi đó, giữ source ngoài package hoặc private staged artifact; không giả vờ rằng một registry entry hiện tại đã đủ quyền.

## Trình tự acquisition có giới hạn

Mỗi bước dừng nếu rights, route, schema hoặc owner gate không đạt. Không có bước nào tạo record mới để bù quota.

1. **VI Wikisource oldids trước.** Lấy bốn locator ở trên; giữ raw page/scan, metadata, oldid/file URL, attribution, page-level license, underlying-work note, hash. Dừng nếu owner chưa chốt genre quota hoặc jurisdiction.
2. **PMC chỉ lấy English CC BY allowlist.** Dùng Cloud/OAI/E-Utilities/BioC; lọc article-level license trước bytes; giữ PMCID/DOI/JATS/hash. Dừng nếu không có schema per-record rights hoặc consumer cần ngoài biomedical scope.
3. **SciFact claims/evidence.** Tải release route, pin revision/hash/schema, lưu primary `LICENSE.md` và HF conflict như unresolved. Không promote cho release công khai trước khi owner chọn rights interpretation.
4. **Tatoeba dev/test only.** Kiểm `eng-vie` manifest, sentence IDs/authors/licenses; lưu dev/test separately. Không dùng training CC BY-NC-SA 4.0 trong shortlist này.
5. **World Bank API, rồi OWID optional.** Lưu JSON response + metadata/hash và `lastupdated`; chỉ thêm OWID CSV/metadata nếu chart reader thật sự cần CSV, đồng thời giữ original-source chain.
6. **UCI Bank Marketing, Online Retail optional.** Dùng official page/DOI download, file hashes, variables and task framing. Với Bank Marketing, tách prospective task khỏi `duration`; với Retail, privacy/context gate trước release.
7. **SWE-bench cuối cùng, metadata/private first.** Pin HF revision và base commits; lập per-repo license ledger; chỉ copy task bytes khi từng rights check đạt. Nếu ledger không đủ, giữ issue/base-commit locator private.

Artifact tối thiểu sau mỗi bước:

```text
source_id, locator, source_kind, version_or_oldid, retrieved_at,
as_of_or_lastupdated, upstream_author, license_statement,
rights_scope, consumer, schema_or_split, sha256, limitations, status
```

Không dùng `ak plan validate`, hash, parse, row count hoặc successful reader như bằng chứng của human review, factual validity, scientific acceptance, native editability hay stable public release.

## Standards và taste phải tách riêng

| Standards có thể kiểm bằng artifact/metadata | Taste cần owner/human review riêng |
|---|---|
| License, attribution, per-record rights | Register, genre naturalness, idiomaticity |
| Provenance, title/author/DOI/PMCID/issue/base commit | Readability, rhythm, voice, stylistic preference |
| Oldid/revision/release/split/API query and `as-of` | “Nghe tự nhiên” trong tiếng Việt hiện đại |
| Raw bytes, SHA-256, schema, row count, source locator | Bản dịch có sắc thái tốt hay không |
| JATS section/claim rationale/negation/unit fields | Mức hợp với taste của owner/reviewer |
| Chart indicator, unit, date window, processing/source chain | Đẹp, dễ đọc, nhấn nhá và accessibility của chart |
| Task base commit, test metadata, target definition | Chất lượng engineering/marketing task trong workflow cụ thể |

Nguồn labels, expert annotations hoặc community sentences chỉ mô tả dữ liệu của nguồn. Chúng không biến thành human gold cho NCKH owner nếu chưa có reviewer, rubric, sample protocol và threshold đã được duyệt.

## NO-GO

- Không sinh synthetic samples, labels, translations, chart values, citations, human scores hoặc measurements để đạt quota.
- Không gọi source labels/annotations là human gold; không gọi Tatoeba là fact-checked; không suy ra factual truth từ prose availability.
- Không suy ra một license chung từ repository visibility, GitHub presence, `Open Access`, `latest`, mirror hoặc file extension.
- Không phát hành mixed-rights PMC records hoặc toàn bộ SWE-bench dưới license của tooling; per-record/per-repository review bắt buộc.
- Không coi public-domain rationale của Wikisource là legal clearance cho mọi jurisdiction; giữ page license và underlying work thành hai records.
- Không dùng SciFact khi chưa ghi conflict giữa primary license và HF card; không dùng UCI data để claim causal uplift hay marketing copy quality.
- Không dùng OWID processed data như primary measurement nếu không giữ original provider/source chain.
- Không khuyến nghị BugsInPy cho packaging khi chưa có license statement rõ.
- Không sửa `resources.json`, source-lock, installed skill, package hoặc schema trong phase nghiên cứu này.

## Câu hỏi chưa giải quyết

1. Owner muốn quota VI chính xác theo genre nào: modern prose, historical prose, verse, translation, fable, hay tỷ lệ cụ thể giữa chúng?
2. NCKH local release có hỗ trợ CC BY-SA, ODC-By, CC BY 2.0 FR, CC BY-NC-SA 4.0 và mixed per-record licenses không?
3. Chart reader chấp nhận JSON/API snapshot hay bắt buộc CSV? Nếu bắt buộc CSV, source-of-truth và transformation phải ghi ở đâu?
4. SWE-bench cần revision và task subset nào, và có chấp nhận private metadata/base-commit locator thay cho redistributable bytes không?
5. SciFact release intended dùng primary repository `LICENSE.md` hay HF dataset card làm rights authority? Cần owner/legal decision trước public release.
6. PMC có domain/venue/years và exact CC BY allowlist nào; có cần giữ full JATS hay chỉ metadata/selected sections?
7. Ai là reviewer người thật, rubric và threshold cho VI/EN taste, fidelity, domain và visual acceptance?

Status: DONE_WITH_CONCERNS
Summary: Đã lập shortlist acquisition-ready gồm VI Wikisource, PMC/SciFact/Tatoeba, World Bank/OWID, SWE-bench và UCI; mỗi nguồn có locator, snapshot strategy, rights boundary, consumer mapping và giới hạn sử dụng.
Concerns/Blockers: Chưa có rights support cho toàn bộ license mới/per-record mixed rights, chưa có owner quota/reviewer/threshold, chưa pin release/subset cuối cho SciFact/SWE-bench, và chưa có bytes/hash acquisition thực tế. Stable/public packaging vẫn NO-GO.
