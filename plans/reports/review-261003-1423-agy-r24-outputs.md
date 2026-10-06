# Review độc lập: năm đầu ra Antigravity r24

Ngày: 2026-10-03 · Múi giờ: Asia/Saigon · Phạm vi: `C:/Users/USER/Downloads/test-skill`.

## Kết luận theo phạm vi

**Chưa đạt toàn bộ hợp đồng năm case.** Có năm memo Markdown và sáu reader receipts khớp tài nguyên đã cài. Bốn memo có lỗi nội dung cần sửa; case World Bank bảo toàn đúng trạng thái capability unavailable nhưng **UNMET** vì chưa có SVG và chứng cứ open/render/editability. Memo blocker không thay thế đầu ra vector bắt buộc.

Đây là review artifact và nguồn cục bộ bằng `nckh-review`. Không chạy model, UI, provider, Django fixtures hay test suite; không chỉnh đầu ra, nguồn, installed skills hoặc cấu hình. Selected model **Gemini 3.8 Flash High** là quan sát do controller cung cấp. Review này không thiết lập effective provider model/effort. Cursor vẫn chỉ được dùng **Grok 4.7 Extra High**. Owner chấm cuối sau khi dùng; không đặt external reviewer/holdout thành điều kiện cho personal-use và không tạo human gold hoặc scientific certification.

| Case | Chứng cứ đọc nguồn | Đánh giá nội dung/hợp đồng | Việc còn lại |
|---|---|---|---|
| VI prose/taste | PASS | FAIL | Sửa mô tả giọng kể và các chú giải vượt chứng cứ. Giữ nguyên ba literal anchors. |
| EN scientific fidelity | PASS | FAIL | Bỏ suy diễn first authorship thành early-career roles; sửa thông tin đếm từ. |
| World Bank visual | PASS | UNMET; memo có lỗi receipt | Sửa nhãn/hash và caveats; cần engine được phép, SVG thật và QA thật. |
| Django static review | PASS | FAIL | Bổ sung finding có căn cứ về assertion rollback; giữ review-only. |
| UCI analytics | PASS | FAIL | Sửa diễn giải `balance=-88`; giữ nguyên dữ liệu và phép đếm. |

## Binding đầu vào và kiểm tra receipt

- Candidate: **r24**; source-lock giữ nguyên `57e9a049e12d33c0f73b34d7eb13ebae07c18cd9f0c08f96ea9e6d22cf9f7fa0` theo ngữ cảnh controller. Review không tạo freeze mới.
- [Case definitions](../evaluation/personal-use/native/cases/real-source-cases.json): SHA-256 `d4b926e855cbf8203d8f434db3fa6a427eb71fbd02a07d274fe5ef485cfeb875`.
- Prompt Antigravity (historical evidence path: `../evaluation/personal-use/native/agy-gemini-r24-prompt.txt`; unavailable in the cleaned checkout): SHA-256 `ae804871b993f5f82d948ef6ccdd6f8cf987549623a15769252726b342d0cf60`.
- Đã đọc metadata, content và provenance của cả sáu receipts. Cả sáu có `status=matched`, `resource_read=true`, query đúng source_id và đúng consumer/domain/locale/genre. Mỗi query chọn đúng một installed record.
- Đã tính hash từ các resource file và reader hiện tại: cả sáu resource hashes khớp receipt và installed catalog; cả sáu reader hashes khớp `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb`. Content trong từng receipt khớp selected installed record khi so đối tượng JSON đầy đủ; hai receipts VI cùng record.
- Đã tính hash raw XML, hai Django fixtures và license, World Bank API JSON, hai UCI archives, VI child JSON/HTML; đều khớp các hash nguồn khai báo. Đây là kiểm tra identity/integrity, không phải chứng nhận nội dung hay execution telemetry.
- Đã đọc raw PMC XML cho các claim/method/limit liên quan; đọc `bank-names.txt` ngay trong nested archive để xác định nghĩa `balance`, `duration`, `pdays`; đọc pinned VI child wikitext cho metadata và đoạn văn. Không đọc private SWE-bench issue/task/patch text.
- Các failures lịch sử, cổng batch retry, các receipt r14/r22/r23 và source-lock không bị thay đổi bởi review này.

### Hash của năm memo được review

| Artifact trong `native/agy-gemini-r24/` | SHA-256 |
|---|---|
| `real-source-vi-prose-taste-01.md` | `9f8565552188ce6670905f7577183ff00a05d4c0475c354f0a3f35faac2bbf4b` |
| `real-source-en-scientific-fidelity-01.md` | `0fe949bf1fa39187ca065bcec0fcc8c054ae47da29bef754900de05a26f28072` |
| `real-source-worldbank-visual-01.md` | `bdfe1dfbe60713a0cdc5adbf12e65735de674549ffa5844db53f9d2e2760ef93` |
| `real-source-django-code-review-01.md` | `9d75d8dd1c5aa9d7f2641f32ad18dc683e1f2abcd6407e0fcdda7aade39ddce3` |
| `real-source-uci-analytics-01.md` | `5eaf7acae7ce9248ac452fd781ccad6d6cb560799cf6e2cf812048b4abf8b06a` |

### Hash của sáu reader receipts

| Receipt trong `native/agy-gemini-r24/reader-receipts/` | SHA-256 |
|---|---|
| `nckh-taste__R-vi-wikisource-passages__vi-wikisource-19383.json` | `def004febd95f984aa353888d543c9af4609e38e46580273f1b6474119a7e267` |
| `nckh-write__R-vi-wikisource-passages__vi-wikisource-19383.json` | `40a058ed49cc9f78eb5b24c62a71491cd6dfc7ccca7269b7ed508931af410939` |
| `nckh-write__R-pmc-scientific__pmc-PMC13623154.json` | `90818d10ce0f8eb9a9f4271a20c7434b095b2d38bfe786925239066c4f4ef29d` |
| `nckh-visuals__R-worldbank-vietnam-population__worldbank-vnm-SP.POP.TOTL-2000-2025.json` | `3afca7f91305ea19c0cf96f1f0eee4c523c6c74bd9d503761155de161faa6d5d` |
| `nckh-code-review__R-django-sqlmigrate-fixtures__django__django-10087.json` | `705d2b978dd7e58539e6dec380dca9d73e534ca4d390d6b4c5dfc2ba419e548a` |
| `nckh-analytics__R-uci-bank-marketing__uci-bank-marketing-bank-csv-first-10.json` | `b0100b18d4d3ffd96e4458bbea9a5b3a7daaabec88824ac518146f86116ef1e6` |

## Findings cần sửa

Các số dòng dưới đây là số dòng của artifact hiện tại; dòng upstream fixture được ghi riêng. Owner sửa: controller/người thực hiện vòng sửa native tiếp theo. Review này chỉ đề xuất sửa memo, không cấp quyền sửa upstream Django hoặc binding engine.

### P2 — Django: kết luận no-finding bỏ sót assertion không kiểm đúng thứ tự rollback

- **Artifact:** [Django review](../evaluation/personal-use/native/agy-gemini-r24/real-source-django-code-review-01.md), dòng 37–42, 49–53.
- **Nguồn:** fixture `tests/migrations/test_commands.py`, `test_sqlmigrate_backwards`, dòng 497–503; SHA-256 `c69753ae276a6815faf1abdd0f78d6ab4770d65ec8ba1f38698d73e34832c81a`.
- **Lỗi có thể chứng minh từ bytes:** assertion cuối là `index_tx_end > index_op_desc_unique_together`, nhưng thông báo nói transaction end phải sau `DROP TABLE`. Mốc đúng để kiểm ý định đó là `index_drop_table`. Hai assertion cuối chỉ yêu cầu `DROP TABLE` sau mô tả author và transaction end sau mô tả unique_together; chúng không yêu cầu transaction end sau `DROP TABLE`.
- **Phản ví dụ static:** thứ tự `BEGIN → unique_together → tribble → author → COMMIT → DROP TABLE` đáp ứng tất cả quan hệ index đang được assert trong method, dù `COMMIT` đã đứng trước thao tác rollback cuối. Không thực thi test hoặc khẳng định output Django thật đang có thứ tự này.
- **Tác động:** test có thể bỏ lọt regression thứ tự wrapper của SQL rollback; vì vậy kết luận không có actionable finding chưa được bytes ủng hộ.
- **Sửa memo:** thay no-finding bằng finding P2 tại đúng fixture dòng 501–503, ghi tác động và phản ví dụ trên; required upstream edit được mô tả là so `index_tx_end` với `index_drop_table`. Giữ rõ đây là đề nghị trong review, không tạo patch. Không suy diễn thêm lỗi runtime/backend khi chưa đọc implementation/dependency tương ứng.

### P2 — VI: mô tả giọng kể trái trực tiếp với đoạn nguồn

- **Artifact:** [VI memo](../evaluation/personal-use/native/agy-gemini-r24/real-source-vi-prose-taste-01.md), dòng 42.
- **Lỗi:** câu nói giọng kể “không trực tiếp bình phẩm đạo đức”. Đoạn nguồn đánh giá chủ tàu là “công bình, ngay thật”, Đặng là “người có tánh hiểm độc và khéo nịnh hót”, và Đàm là “người có hiếu”. Memo tự trích hai trong các lời đánh giá này ngay trong dòng đó.
- **Tác động:** phân tích narrative voice mô tả sai một thuộc tính quan sát được; đây là fidelity defect, không phải bất đồng về khẩu vị.
- **Sửa:** mô tả người kể ngôi thứ ba kết hợp kể sự kiện với nhận xét phẩm chất nhân vật; neo nhận xét vào đúng các cụm nguồn. Không sửa văn bản gốc.

### P2 — VI: lịch sử và chú giải được nâng thành dữ kiện khi nguồn chưa đủ

- **Artifact:** VI memo, dòng 24, 28–29, 37–39, 55–56, 69–71.
- **Chứng cứ giới hạn:** raw pinned child wikitext ghi Alexandre Dumas và dịch giả Phan Khôi, nhưng trường `năm` trống. Installed record chứa văn bản, locator/oldid và `translated-novel`; không cung cấp chứng cứ lịch sử xuất bản Nam Kỳ, toàn bộ quy ước phiên âm theo thời kỳ, bảng tên nguyên tác hoặc từ điển y học/ngôn ngữ.
- **Lỗi cụ thể:** “đau bịnh óc” được giải nghĩa chắc chắn thành “tai biến/đột quỵ não” ở dòng 37 và thành “tai biến mạch máu não” ở dòng 71, dù đoạn chỉ nói nhân vật đau rồi chết; không có chẩn đoán đó. Các phát biểu chắc chắn về nơi/thời kỳ xuất bản và chuẩn mực chính tả/dịch thuật cũng vượt phạm vi chứng cứ vừa đọc. Review không kết luận mọi phát biểu lịch sử đó sai; trạng thái của chúng là chưa đủ chứng cứ trong receipt này.
- **Sửa:** bỏ chẩn đoán bệnh cụ thể; giữ cách gọi lịch sử và ghi nghĩa cần nguồn chú giải nếu muốn giải thích. Bỏ hoặc gắn trạng thái chưa xác minh cho thông tin lịch sử/bảng đối chiếu ngoài record; chỉ giữ metadata có nguồn. Hai đề xuất phụ trợ vẫn có thể giữ nếu nội dung chú giải cụ thể không được trình bày như sự thật đã xác minh. Không hiện đại hóa literal quotes.

### P2 — EN: first authorship bị đổi thành nhóm early-career

- **Artifact:** [EN brief](../evaluation/personal-use/native/agy-gemini-r24/real-source-en-scientific-fidelity-01.md), dòng 34, cụm `indicating parity in early-career leadership roles`.
- **Nguồn:** abstract chỉ báo phân bố giới trong **first authorship positions**. Methods operationalize first/last author positions làm proxy leadership. Phần limitations trong XML nói authorship order là imperfect measure và đề cập việc thiếu dữ liệu age để phân tích tốt hơn.
- **Tác động:** bình đẳng ở vị trí first author bị đổi thành bình đẳng cho một nhóm giai đoạn sự nghiệp không được đo. Caveat tổng quát ở dòng 45 không sửa được claim cụ thể này.
- **Sửa:** dùng `indicating a roughly balanced gender distribution among first authors in this sample`; tiếp tục dùng association wording, proxy caveat và phạm vi 1,375 studies. Không đổi số, aOR, p-value hoặc CI.

### P2 — UCI: average yearly balance bị diễn giải thành thấu chi thực tế

- **Artifact:** [UCI memo](../evaluation/personal-use/native/agy-gemini-r24/real-source-uci-analytics-01.md), dòng 65.
- **Nguồn:** nested `uci-bank.zip` → `bank-names.txt`, Attribute information số 6: `balance: average yearly balance, in euros (numeric)`. Dòng 10 thật có `balance=-88`; dữ liệu không có biến transaction/overdraft event hoặc thời điểm số dư hiện tại.
- **Lỗi:** “phản ánh số dư thấu chi thực tế ... trong hệ thống ngân hàng” biến một giá trị số dư trung bình năm âm thành sự kiện thấu chi thực tế đã xác minh. Unit euro đúng theo dictionary; giá trị `-88` đúng.
- **Tác động:** memo trộn quan sát số học với diễn giải sản phẩm ngân hàng không có chứng cứ.
- **Sửa:** viết `Dòng 10 có balance=-88 euro; theo bank-names.txt, balance là số dư trung bình năm. Giá trị âm được giữ nguyên; riêng giá trị này không xác định giao dịch hay tình trạng thấu chi cụ thể.`

### P2 — World Bank: nhầm resource hash thành record hash

- **Artifact:** [World Bank memo](../evaluation/personal-use/native/agy-gemini-r24/real-source-worldbank-visual-01.md), dòng 52.
- **Lỗi:** trường được đặt tên `record_sha256` chứa `a29802fa36bc453ce9abbf9789e119bae689462ffd6348e327ee7d7f5e9cb4b2`. Đây là `resource_sha256` của toàn file installed `worldbank-series.jsonl`. Receipt thực ghi `records[0].record_sha256=65b7007d7ea17cae6091e2925ec725bf88433573635536386868bfa4c1304800`.
- **Tác động:** consumer không thể xác nhận đúng record theo trường hash đã ghi; nguồn dữ liệu và phép đếm vẫn đúng.
- **Sửa:** giữ `a298…` dưới nhãn `resource_sha256` hoặc `derived_artifact_sha256`, và ghi `65b7…` dưới nhãn `record_sha256`. Raw hash `a63e…` giữ nguyên. Trong cùng receipt, bổ sung caveat nguồn đang thiếu: snapshot có thể bị provider sửa và third-party indicators có thể có hạn chế thêm theo World Bank terms. Những caveats này là yêu cầu rights/limitations của case, không thay đổi trạng thái engine unavailable.

### P3 — EN: số đếm từ tự báo không khớp đoạn kết luận

- **Artifact:** EN brief, dòng 36 ghi 146 words. Đoạn dòng 34 có **160 token tách bằng khoảng trắng**, gồm token toán; vẫn trong yêu cầu 120–180 theo phép đếm này. Không dùng một cách token hóa khác để kết luận đoạn chắc chắn vượt ngưỡng khi contract chưa quy định cách đếm.
- **Sửa:** bỏ số 146 chưa tái lập hoặc ghi đúng số cùng quy ước; nội dung sửa phải được đếm lại sau thay đổi. Đây là lỗi receipt nhỏ, không phải lỗi số liệu nghiên cứu.

## Ma trận observable checks từng case

PASS dưới đây chỉ áp dụng check được nêu. FAIL/UNMET ở một required gate giữ case chưa accepted-for-scope.

### 1. VI prose/taste

| Check trong case | Kết quả | Chứng cứ/giới hạn |
|---|---|---|
| source_id, child/parent oldid, exact locator | PASS | Dòng 5–10 khớp record. |
| Ba required literal content anchors | PASS | Dòng 16–18 giữ nguyên mọi chữ/dấu câu; gồm opening và dialogue. |
| Register, rhythm, vocabulary, audience/genre có vị trí/căn cứ | FAIL | Có phân tích từng phần, nhưng dòng 42 trái nguồn; một số gloss/history vượt evidence như findings. |
| Gợi ý bounded và tách khỏi preserved text | PASS về cấu trúc; FAIL về nội dung chú giải | Chỉ hai đề xuất phụ trợ, không thay văn bản gốc; các chú giải cụ thể cần sửa theo finding. |
| Không claim human gold, universal literary authority, completeness, scientific validity | PASS | Dòng 77–79 giữ sample/rights/authority limits; owner taste vẫn pending. |

### 2. EN scientific fidelity

| Check trong case | Kết quả | Chứng cứ/giới hạn |
|---|---|---|
| source_id, PMCID, DOI, XML hash, article CC BY 4.0 | PASS | Dòng 5–16 khớp record/XML. |
| Mọi số trong five-row ledger traceable và giữ nghĩa | PASS trong phạm vi abstract | 1,375; 1,332; 1,334; 675; 657; 50.7%; 49.3%; 486; 848; 36.4%; 63.6%; χ²=98.23; p<0.001; t=−3.63; −27.14%; CI −32.50% đến −21.77%; aOR/CI 0.93/0.90–0.97, 1.03/1.01–1.05, 1.05/1.02–1.07 đều có trong abstract. Threshold ≥60% có nguồn. |
| Association/aOR/p-value/CI không thành causality | PASS | Dòng 27–28, 34, 50–51 giữ association và giới hạn causal mechanisms. |
| Bounded 9,000-character excerpt khác full XML | PASS | Dòng 16, 42–43 tách rõ; raw XML hash đã kiểm lại. |
| Không unsupported population/generalization/scientific verdict | FAIL | Dòng 34 thêm early-career population/role chưa đo; phần khác không claim scientific acceptance. |
| Task: five-row ledger và conclusion 120–180 words | PASS với phép đếm đã nêu | Đúng năm rows; kết luận 160 whitespace tokens. Dòng 36 self-report 146 cần sửa. |

**Sai khác tồn tại ngay trong nguồn:** abstract báo `t=−3.63` và risk difference −27.14%; Results trong full XML báo `t=−3.77` cùng mean difference −1 (95% CI −1 đến −0.1) cho đoạn mô tả last-author team size. Ledger hiện giữ số abstract đúng; không tự sửa chúng thành số Results hoặc kết luận article không có conflict. Khi sửa memo nên chỉ rõ các số này được neo vào abstract và ghi unresolved source discrepancy. Review này không phân xử scientific validity của bài.

### 3. World Bank visual

| Check trong case | Kết quả | Chứng cứ/giới hạn |
|---|---|---|
| 26 observations, 26 non-null, 2000–2025 | PASS | Đã đọc đủ 26 records; memo dòng 54–55 đúng. |
| First/last values và raw blank unit | PASS | 77,154,011; 101,598,527; unit `""` trong tất cả observations. |
| Source-to-mark map, axes/caption/alt/reading order | UNMET | Chỉ có proposed y-axis/alt text; không có marks, mapping hoặc reading-order artifact. |
| SVG editable/source-native có text/data objects | UNMET | Không có SVG; contract unavailable/null được giữ đúng. |
| Không claim render/inspection pass khi chưa có QA thật | PASS về honesty; QA UNMET | Memo ghi blocker/UNMET, không có render-pass receipt. |

Các giá trị tăng ở mọi bước năm liền kề trong snapshot; proposed alt text “tăng liên tục” có căn cứ mô tả, không gán nguyên nhân. Absolute change 24,444,516 và percentage change 31.682754639936995% khớp hai endpoints và case; nguồn không bị round. Raw hash/metadata đúng, record hash cần sửa theo finding. Rights caveat third-party/provider-revision đang thiếu. Hợp đồng native hiện không chứng minh rằng mọi engine khả dĩ trên máy đều vắng; nó chứng minh binding được chọn trong installed contract chưa khả dụng.

### 4. Django static review

| Check trong case | Kết quả | Chứng cứ/giới hạn |
|---|---|---|
| Finding, nếu có, phải có fixture/line/impact/why/edit | UNMET cho finding bị bỏ sót | Memo không ghi finding về assertion dòng 501–503; review độc lập chỉ ra phản ví dụ và required edit. |
| No-finding vẫn ghi implementation và ba methods | PASS về inspected-scope receipt | Dòng 15–31 liệt kê Command/handle, forwards/backwards/non-atomic; không đủ để xác nhận kết luận no-finding. |
| Commit, fixture hashes, BSD scope | PASS | Receipt khớp raw hashes và pinned commit; BSD chỉ áp dụng upstream fixtures. |
| Không private issue/task/patch text | PASS trong artifact và packaged receipt | Có tên các private fields để mô tả exclusion; không có body/patch nội dung. Không kiểm lịch sử UI/model bên ngoài artifacts. |
| Review-only, không code change/publish/security guarantee | PASS trong đầu ra được review | Output chỉ memo; không có patch hoặc guarantee. |

Implementation `output_transaction=migration.atomic` và các named tests đúng như memo mô tả. Không dựa vào tên benchmark/ticket để suy ra lỗi backend hoặc ticket intent. Finding xác lập ở đây chỉ là điều kiện assertion sai mốc trong chính test bytes; chưa chạy Django.

### 5. UCI analytics

| Check trong case | Kết quả | Chứng cứ/giới hạn |
|---|---|---|
| 10 rows, 17 columns, delimiter `;`, DOI/locator | PASS | Dòng 9–10, 19, 27–40 khớp receipt; toàn bộ 170 cell values khớp selected installed record. |
| y=no=10, y=yes=0, không population response rate | PASS | Dòng 46–50 và 83–84 đúng và bounded. |
| month counts và balance −88 traceable | PASS về dữ liệu; FAIL về diễn giải balance | may=5/apr=2/feb=1/jun=1/oct=1 và dòng10 balance−88 đúng; phát biểu thấu chi ở dòng65 sai phạm vi. |
| Descriptive khác causal/inferential, có duration leakage | PASS về các giới hạn chính; FAIL riêng balance inference | Dòng 71–75, 83–88 có duration post-contact, pdays sentinel và no-lift/no-forecast. Finding balance vẫn cần sửa. |
| Raw archives và derived record hashes | PASS | Outer/nested archive hashes và record_sha256 đúng; attribution/license/DOI có trong receipt. |

Các phép đếm tái lập từ các rows đã đọc: target no=10/yes=0; month may=5/apr=2/feb=1/jun=1/oct=1; duration min=57/max=341; pdays−1 ở rows1/4/5/8/9 cùng previous0; negative balance ở row10. Không có suy luận về response rate toàn bộ dataset, causal lift hoặc forecast được chấp nhận từ các con số này.

## Repair và giới hạn acceptance

1. Sửa bốn memo theo findings, giữ raw source/reader receipts và input hashes; tạo hash mới cho outputs đã sửa. Không sửa fixture Django trong scope review này.
2. Sửa receipt World Bank và bổ sung nguồn caveats; giữ visual **UNMET**. Chỉ hoàn tất sau khi có engine thực sự được phép và bằng chứng SVG/source-to-mark/open/render/editability/accessibility/hash-bound QA. Không đổi `unavailable` thành available từ static review.
3. Review lại đúng các claim đã sửa và bindings của output mới. Các pass unchanged vẫn có scope rõ; không cần lặp full build/source/resource audit để sửa memo.
4. Sau usable delivery, owner đánh giá khẩu vị, fidelity và usefulness trên artifact/hash tương ứng. Native execution receipt, effective telemetry, owner review và scientific/domain acceptance giữ cổng riêng.

Status: DONE_WITH_CONCERNS

Summary: Đã review đủ năm memo và sáu receipts, kiểm identity/hashes với installed resources và nguồn liên quan. Bốn memo cần sửa factual fidelity; World Bank còn UNMET, blocker memo không đáp ứng SVG contract.

Concerns/Blockers: Engine visual unavailable/null; chưa có native visual QA. Selected model không thay thế effective telemetry; owner-final review vẫn pending-user-use. Review không thay controller quyết định goal status hoặc cấp quyền batch retry.
