# Review độc lập: bốn memo Antigravity r24 repair-01

Ngày: 2026-10-03 · Múi giờ: Asia/Saigon · Phạm vi: `C:/Users/USER/Downloads/test-skill`.

## Kết luận theo phạm vi

**Ba case đã đóng lỗi nội dung được giao sửa; VI còn một P2 về cách trình bày chú giải.** EN còn một P3 về phương pháp đếm từ tự báo, nhưng đoạn kết luận đáp ứng 120–180 theo phương pháp tách khoảng trắng được nêu rõ. Review không đặt P3 này thành yêu cầu chạy lại toàn bộ hành vi.

| Case | Identity/receipt | Kết quả repair nội dung | Còn lại |
|---|---|---|---|
| VI prose/taste | PASS | PARTIAL | Giọng kể, chẩn đoán bệnh và metadata đã sửa; chú giải cụ thể ở dòng 38–39, 74 chưa phân biệt nghĩa đã xác minh với diễn giải theo ngữ cảnh. |
| EN scientific fidelity | PASS | PASS cho sửa claim | Không còn suy diễn first authorship thành early-career; 161 token tách khoảng trắng. Nhãn `178 standard words` chưa có phương pháp tái lập, P3. |
| Django static review | PASS | PASS | Đã mô tả đúng comparator defect và phản ví dụ tĩnh; không xác lập lỗi runtime/backend. |
| UCI analytics | PASS | PASS | `balance=-88` được diễn giải đúng là số dư trung bình năm âm; bảng, tần số và giới hạn suy diễn khớp nguồn. |

Đây là review artifact cục bộ bằng `nckh-review`. Không chạy model, provider, UI, resource reader hoặc test suite; không sửa memo, installed skills, raw inputs hay source-lock. User đã tự gửi repair prompts vào native UI; controller không trực tiếp quan sát các lần gửi đó. Các tệp và receipts hiện có là chứng cứ artifact, không thiết lập một lần gọi reader mới, effective model/effort hoặc telemetry thực thi mới.

Owner scoring vẫn chờ đánh giá thực tế. Review không tạo human gold, không chứng nhận khoa học, không quyết định khẩu vị văn học thay owner, và không đặt external reviewer thành điều kiện cho personal-use.

**World Bank không thuộc vòng review này.** Case đó vẫn cần bằng chứng visual r25 mới; report này không thay memo blocker, SVG thật hoặc kiểm tra open/render/editability.

## Binding trước/sau và nguồn đọc

- [Review gốc](review-261003-1423-agy-r24-outputs.md): SHA-256 `0901fb285d9ee5b13e34a99b0220c1eb3eafb3ac8d0cadde10bff8c87a4ffdb0`.
- [Case definitions](../evaluation/personal-use/native/cases/real-source-cases.json): SHA-256 hiện tại `d4b926e855cbf8203d8f434db3fa6a427eb71fbd02a07d274fe5ef485cfeb875`, khớp review gốc.
- Trước: `plans/evaluation/personal-use/native/agy-gemini-r24/`. Sau: `plans/evaluation/personal-use/native/agy-gemini-r24-repair-01/`.
- Đã tính lại hashes của bốn memo gốc và năm receipts gốc: đều khớp review gốc. Các bản gốc được bảo toàn.
- Đã đọc cả năm receipts repair và so toàn bộ đối tượng JSON với receipts gốc: không có field nào đổi giá trị. Byte hashes thay đổi do cách lưu JSON; sự khác biệt này không chứng minh một lần resource read mới.
- Đã so `records[0].content` với đúng record được chọn từ resource JSONL trong installed consumer; cả năm khớp. Hai receipts VI cùng một record.
- Tính lại `record_sha256` từ JSON chuẩn hóa bằng `json.dumps(content, sort_keys=True, ensure_ascii=False, separators=(",", ":"))`, mã hóa UTF-8: cả năm khớp receipt. Hash resource và reader hiện tại cũng khớp receipt/catalog.
- Hash raw inputs đã được xác minh trong review gốc được giữ làm binding đã xác minh; review này không lặp lại việc hash toàn bộ raw. Đã đọc lại phần wikitext VI, các đoạn PMC XML liên quan và `bank-names.txt` trong archive để kiểm nội dung. Không đọc private benchmark issue/task/patch fields.

### Bốn memo

| Tên tệp | SHA-256 trước | SHA-256 sau |
|---|---|---|
| [real-source-vi-prose-taste-01.md](../evaluation/personal-use/native/agy-gemini-r24-repair-01/real-source-vi-prose-taste-01.md) | `9f8565552188ce6670905f7577183ff00a05d4c0475c354f0a3f35faac2bbf4b` | `f47672d4c22fab85fc43473d7c14f305282d6aab80f2cf72f78e256a27f3c210` |
| [real-source-en-scientific-fidelity-01.md](../evaluation/personal-use/native/agy-gemini-r24-repair-01/real-source-en-scientific-fidelity-01.md) | `0fe949bf1fa39187ca065bcec0fcc8c054ae47da29bef754900de05a26f28072` | `97a9c44c3124a3d410f86221933981d3afc193a33c0c58e30bfcdbf5861ad090` |
| [real-source-django-code-review-01.md](../evaluation/personal-use/native/agy-gemini-r24-repair-01/real-source-django-code-review-01.md) | `9d75d8dd1c5aa9d7f2641f32ad18dc683e1f2abcd6407e0fcdda7aade39ddce3` | `4bf4e5ef7ad83e20b2cc5cdb5468ddd5e5e564b22f3df77dd8fbd3cdc3bd7bfb` |
| [real-source-uci-analytics-01.md](../evaluation/personal-use/native/agy-gemini-r24-repair-01/real-source-uci-analytics-01.md) | `5eaf7acae7ce9248ac452fd781ccad6d6cb560799cf6e2cf812048b4abf8b06a` | `a0d06bcddd9393fc43b4a46c47e720f75f6780d039586bc801eb2072c1cf8406` |

### Năm reader receipts

Các tệp sau nằm dưới `reader-receipts/` của từng thư mục trước/sau.

| Receipt | SHA-256 trước | SHA-256 sau |
|---|---|---|
| [nckh-taste / VI](../evaluation/personal-use/native/agy-gemini-r24-repair-01/reader-receipts/nckh-taste__R-vi-wikisource-passages__vi-wikisource-19383.json) | `def004febd95f984aa353888d543c9af4609e38e46580273f1b6474119a7e267` | `f4ec28f951205f0c6b272304698dd8959ae0dd95d3c433040bfc611ebb4a9d5d` |
| [nckh-write / VI](../evaluation/personal-use/native/agy-gemini-r24-repair-01/reader-receipts/nckh-write__R-vi-wikisource-passages__vi-wikisource-19383.json) | `40a058ed49cc9f78eb5b24c62a71491cd6dfc7ccca7269b7ed508931af410939` | `176d293cd0c079ca35e0183e09f973f98778625c178c1fbcd12f386245b4ed01` |
| [nckh-write / PMC](../evaluation/personal-use/native/agy-gemini-r24-repair-01/reader-receipts/nckh-write__R-pmc-scientific__pmc-PMC13623154.json) | `90818d10ce0f8eb9a9f4271a20c7434b095b2d38bfe786925239066c4f4ef29d` | `2210df422a3031f4da8ffc564e63295fbb381ec41c6b59a79ee666eed4a89858` |
| [nckh-code-review / Django](../evaluation/personal-use/native/agy-gemini-r24-repair-01/reader-receipts/nckh-code-review__R-django-sqlmigrate-fixtures__django__django-10087.json) | `705d2b978dd7e58539e6dec380dca9d73e534ca4d390d6b4c5dfc2ba419e548a` | `d4e306f2954b999a92930071847b7c481cb31069fbdbed8c8246a3f7f0e3db55` |
| [nckh-analytics / UCI](../evaluation/personal-use/native/agy-gemini-r24-repair-01/reader-receipts/nckh-analytics__R-uci-bank-marketing__uci-bank-marketing-bank-csv-first-10.json) | `b0100b18d4d3ffd96e4458bbea9a5b3a7daaabec88824ac518146f86116ef1e6` | `f9dbcdff5e18f1040c9d16c05aa323d382fcf6d0e9dde4bd811766fe8ae8632a` |

### Selected records và installed resources

| Resource / selected record | Record SHA-256 | Resource SHA-256 |
|---|---|---|
| `R-vi-wikisource-passages` / `vi-wikisource-19383` | `13149ead6bebde7171e5697919acfacfda9b22850023caf6e51971edf7080566` | `36d52fcd6a97ed5d8376ab5c1862c39404359e4843944362c8b396945470492f` |
| `R-pmc-scientific` / `pmc-PMC13623154` | `546888bb164ac36cd719f432ccacb7ed3dba076704b8191c47c88f5efe2f0223` | `b2dadda901d4ca37ea8124aca1f7f282f9adbee4582638bc5f334a4a389eeb45` |
| `R-django-sqlmigrate-fixtures` / `django__django-10087` | `3600a5e446a811f585fe3bc7c044cf7305db5815e2a9ff04ec1168ee52b318a8` | `e81048922d196fd302555f192d289d51d82449b0ae724fc05cb2e2b4bfeb90cf` |
| `R-uci-bank-marketing` / `uci-bank-marketing-bank-csv-first-10` | `d85b74d70eacd63a194a0188527a233d5dd65b77a6a12b4a9c3defba04d6eaf6` | `647a774b9fb4545d6bc652114910df53677fbe993a00c268c16d4f50b03fe123` |

Installed lookup route: `.agents/skills/<consumer>/references/_shared/core/registry/catalog/resources.json` → resource `path`; reader `scripts/search-resource.py`. Cả năm reader bindings khớp SHA-256 `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb`.

Cả năm receipts có `status=matched`, `resource_read=true`, một selected record đúng query/source_id, consumer/domain/locale/genre. Các trường `policy_applicability=unverified`, `evidence_class=resource-read-observation`, `human_acceptance=not-evaluated` được giữ nguyên; chúng không được nâng thành acceptance nội dung.

## Finding còn lại

### P2 — VI: chú giải cụ thể chưa được gắn đúng trạng thái suy diễn

- **Artifact:** VI memo, dòng 38–39 và 74.
- **Claim:** dòng 38 giải nghĩa `mại bản` thành `nhân viên quản trị tài chính/thương vụ trên tàu buôn`; dòng 39 giải nghĩa `mắt măng mắt vược` thành `mắt mờ, nhìn không rõ`. Dòng 74 đề xuất ghi nhận đây là `cách giải nghĩa tham khảo từ từ điển`, nhưng không có từ điển, mục từ, phiên bản hay locator; cùng dòng lại giải nghĩa thành `mắt nhìn không thấu/lơ đãng`.
- **Nguồn đã đọc:** đoạn chỉ gọi Đặng là `người mại bản` và kể việc ganh tị; không mô tả chức trách quản trị tài chính. Đàm nói `Xin tha lỗi cho tôi, tôi vào nhà mà mắt măng mắt vược không thấy người quý khách.` Ngữ cảnh hỗ trợ quan sát rằng Đàm chưa để ý thấy người khách; không xác lập nghĩa từ điển là thị lực mờ. Installed record không chứa mục từ hoặc glossary. Review không kết luận mọi gloss đều sai.
- **Tác động:** trong phần anchored observations, định nghĩa thêm được trình bày như nghĩa đã xác minh. Caveat chung ở dòng 24 không xác định gloss nào chỉ là diễn giải theo ngữ cảnh; dòng 74 còn tạo ấn tượng có nguồn từ điển cho chính các ví dụ đó. Đây là vấn đề trạng thái chứng cứ, không phải phán xét khẩu vị.
- **Sửa tối thiểu:** giữ nguyên mọi literal source quotes. Gắn các gloss thêm vào là `diễn giải tạm theo ngữ cảnh, chưa đối chiếu từ điển`; với `mại bản`, chỉ giữ chức danh mà đoạn nguồn gọi Đặng nếu không có chứng cứ về nhiệm vụ. Với `mắt măng mắt vược`, mô tả Đàm tự nhận chưa để ý thấy người khách trong lời thoại, tránh kết luận về thị lực. Ở đề xuất cước chú, chuyển `từ từ điển` thành việc tra cứu cần làm trong tương lai hoặc cung cấp nguồn tra cứu thật nếu muốn giữ một nghĩa xác định. Không bắt buộc nguồn ngoài cho nhận xét nhịp câu, cảm nhận register hoặc lời diễn giải đã ghi rõ là suy luận.

### P3 — EN: nhãn đếm `standard words` chưa có quy tắc tái lập

- **Artifact:** EN memo, dòng 36: `161 whitespace-delimited tokens / 178 standard words; strictly verified`.
- **Kiểm tra:** lấy đúng đoạn một paragraph ở dòng 34, dùng `len(paragraph.split())` trong Python: **161**. Phương pháp tách khoảng trắng phù hợp mô tả đầu tiên của memo và nằm trong 120–180. Đối chiếu thêm `len(re.findall(r"\w+", paragraph))` cho 182 word runs, minh họa rằng phương pháp khác xử lý số/thành phần toán khác nhau; không dùng số 182 để kết luận đoạn vi phạm contract.
- **Vấn đề:** memo không định nghĩa `standard words`, nên không tái lập được số 178 hoặc khẳng định `strictly verified` cho phép đếm thứ hai.
- **Sửa tối thiểu:** giữ `161 whitespace-delimited tokens, counted by splitting on whitespace; within 120–180 under this method`, hoặc ghi quy tắc thực dùng cho số thứ hai. Đây là sửa thông tin tự báo; không yêu cầu retry cả case chỉ vì P3 này.

## Các sửa đã đóng

### VI prose/taste

- Dòng 42–45 đã thay claim người kể không bình phẩm đạo đức bằng nhận xét đúng rằng người kể trực tiếp định danh phẩm chất nhân vật. Ba trích đoạn về chủ tàu `công bình, ngay thật`, Đặng `người có tánh hiểm độc và khéo nịnh hót`, Đàm `có hiếu` khớp literal source; dấu `...` của câu Đặng được nhận diện là trích rút gọn.
- Ba literal anchors bắt buộc ở dòng 16–18 hiện diện nguyên văn trong cả memo và selected source; không hiện đại hóa chính tả.
- Dòng 24 ghi đúng Alexandre Dumas/Phan Khôi và trường `năm` trống trong pinned wikitext. Dòng 37 bỏ chẩn đoán đột quỵ/tai biến; dòng 72 ghi bảng đối chiếu tên là tham khảo ngoài record cần kiểm chứng. Rights boundary và giới hạn một trang con giữ ở dòng 80–82.
- Nhận xét register/nhịp câu và khả năng độc giả thấy tên lạ là phân tích văn học hoặc preference được phép. Câu về phong cách thời kỳ ở dòng 29 được đọc cùng caveat chưa xác minh bối cảnh ngoài văn bản ở dòng 24; không coi đây là chứng cứ lịch sử đã xác minh và không tạo thêm cổng owner taste. P2 ở trên giới hạn vào gloss cụ thể còn mang dạng định nghĩa.

### EN scientific fidelity

- Dòng 34 dùng `a roughly balanced gender distribution among first authors in this sample`; dòng 25 và 44–45 từ chối đổi authorship thành career stage/age/institutional role. Lỗi early-career đã đóng.
- Ledger có năm hàng; các số 1,375; 1,332; 1,334; 675/657 và 50.7%/49.3%; 486/848 và 36.4%/63.6%; χ² 98.23; p < 0.001; t −3.63; RD −27.14% với CI −32.50% đến −21.77%; aOR 0.93 (0.90–0.97), 1.03 (1.01–1.05), 1.05 (1.02–1.07) khớp Abstract trong selected source. Conclusion giữ association wording và không khẳng định cơ chế nhân quả.
- Ghi chú ở dòng 27, 50–51 nhận diện đúng khác biệt nội bộ nguồn: Abstract t −3.63/RD −27.14%, còn Results full XML t −3.77/mean difference −1 (95% CI −1, −0.1). Không đổi Abstract numbers hoặc tự tạo lời hòa giải.
- Phạm vi 9,000-character projection, algorithmic binary gender inference ≥60%, giới hạn mẫu và non-causal limit còn được giữ. Review không nâng article-level license thành peer-review/scientific-validity evidence.

### Django static review

- Memo dòng 41–85 ghi đúng fixture `tests/migrations/test_commands.py`, upstream dòng 501–503: assertion so `index_tx_end` với `index_op_desc_unique_together`, trong khi ý định thông báo là sau `DROP TABLE`; required recommendation là dùng `index_drop_table`.
- Phản ví dụ `BEGIN → unique_together → tribble → author → COMMIT → DROP TABLE` đáp ứng sáu quan hệ index hiện có, dù COMMIT đứng trước DROP TABLE. Memo gọi đúng đây là static counterexample và giữ review-only, không khẳng định Django/backend thật đã tạo thứ tự đó.
- `code_fixtures` được đọc đúng ở dạng plural. Nội dung hai fixture có UTF-8 bytes/hashes khớp khai báo: implementation 2,742 bytes / `6ca06cab795d7b1f1247c1a1327ac0ec54bc9295c68e3cbc95ac7f10be817371`; tests 67,864 bytes / `c69753ae276a6815faf1abdd0f78d6ab4770d65ec8ba1f38698d73e34832c81a`.
- Memo giữ BSD-3-Clause scope ở pinned commit và loại private benchmark fields khỏi review. Đề nghị comparator không phải patch đã thực hiện.

### UCI analytics

- Dòng 65 đã trích đúng `balance: average yearly balance, in euros (numeric)` trong nested `bank-names.txt`. Giá trị −88 euro ở dòng 10 không bị đổi thành giao dịch/tình trạng thấu chi thực tế.
- Header gồm đúng 17 cột; đã so toàn bộ **170 ô** của 10 dòng trong bảng memo với selected record, tất cả khớp. Delimiter `;` đúng.
- Target: no=10, yes=0. Month: may=5, apr=2, feb=1, jun=1, oct=1, đúng các dòng tương ứng. Duration min=57 ở dòng 9; max=341 ở dòng 7.
- pdays=−1 ở dòng 1/4/5/8/9, mỗi dòng previous=0 và poutcome=unknown; sentinel definition khớp `bank-names.txt`.
- Đã giữ cảnh báo duration sau liên hệ và leakage cho dự báo trước cuộc gọi; không suy diễn population response rate, causal lift hoặc forecast. Đây là mô tả mười dòng đầu, không phải representative dataset evaluation.

## Giới hạn và bước còn lại

1. Vòng tiếp theo chỉ cần sửa P2 chú giải VI theo trạng thái chứng cứ và chỉnh P3 self-count EN; giữ nguyên ba anchors, số liệu, bảng/counts, receipts và các bản gốc.
2. Report này binding đúng repair-01 hashes nêu trên. Nếu artifact đổi, kết luận cần review lại phần đổi và hash mới; không ghi đè đánh giá lịch sử.
3. World Bank tiếp tục ở luồng r25 riêng, chờ vector artifact và QA thật. Các sửa claim của bốn memo không hoàn thành cổng visual đó.
4. Acceptance personal-use và owner scoring thuộc controller/owner. Kết quả review chỉ đóng các lỗi artifact có căn cứ vừa nêu; không bao phủ tất cả model hoặc release ổn định.
