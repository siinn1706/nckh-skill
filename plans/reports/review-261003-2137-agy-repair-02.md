# Review độc lập: Antigravity repair 02 — VI và EN

Ngày: 2026-10-03 · Múi giờ: Asia/Saigon · Project: `C:/Users/USER/Downloads/test-skill`.

## Kết luận trong phạm vi

**PASS cho hai sửa được giao:** VI đã đóng finding P2 về trạng thái chứng cứ của chú giải; EN đã đóng finding P3 về phương pháp đếm. Không có finding chặn hai delta artifact trong phạm vi review này. Giữ các kết luận nội dung đã đạt ở repair 01 vì source/claims ngoài delta không đổi.

| Cổng | Kết quả | Giới hạn |
|---|---|---|
| VI: `mại bản` và `mắt măng mắt vược` | PASS | Ghi rõ quan sát nguồn và diễn giải tạm theo ngữ cảnh; không nhận là nghĩa từ điển, chẩn đoán hay chức trách lịch sử đã xác minh. |
| VI: attribution từ điển không có nguồn | PASS | Dòng 74 bỏ attribution cũ; cách giải thích thêm phải được ghi là tentative contextual reading. |
| VI: ba anchors và source quotes | PASS | Ba anchors nguyên văn; mọi quote cũ được giữ và 14 fragment trong dấu ngoặc kép khớp nguồn, với `...` là dấu rút gọn đã hiện rõ. |
| EN: bảo toàn conclusion | PASS | Từng ký tự không đổi so với repair 01; SHA-256 paragraph cố định bên dưới. |
| EN: đếm conclusion | PASS | `len(paragraph.split()) = 161`; không còn `178` hoặc `standard words`. |
| Source/reader receipt binding | PASS | Ba selected records, canonical record hashes, resource/reader bytes và catalog bindings khớp installed consumers hiện tại. |
| Fresh native reader/model execution | Không được xác lập bởi các tệp này | Receipts có JSON bằng repair 01 và bytes bằng originals; không có trace mới trong scope được giao. |
| Effective model/effort | unknown/unverified | Prompt yêu cầu Gemini 3.8 Flash High; không có provider telemetry trong các receipts. |
| Owner acceptance | pending-personal-review | Người dùng tự chấm sau sử dụng; review không chấm khẩu vị thay owner. |

Review dùng `nckh-review`, thao tác đọc, hash, đếm và so sánh artifact cục bộ. Không chạy model/provider/UI/resource reader/test suite, tra cứu ngoài, sửa originals, installed files hoặc plans/checklist. World Bank và các case khác có review riêng.

## Brief, input và provenance

Đã đọc prompt repair 02 (historical evidence path: `../evaluation/personal-use/native/agy-gemini-r24-repair-02-prompt.txt`; unavailable in the cleaned checkout), [case manifest](../evaluation/personal-use/native/cases/real-source-cases.json), [review repair 01](review-261003-1448-agy-r24-repair-01.md), cả hai memo trước/sau và ba receipts mới. Bàn giao controller ghi người dùng báo cả ba prompts đã hoàn tất; review này xác nhận các artifacts hiện có, không tự suy một lần UI dispatch hay effective model từ lời báo đó.

| Artifact | SHA-256 |
|---|---|
| Prompt repair 02 | `6da496f7a108bf92fa00d70462a5ea4e591387f32a756bc127bd27aff07929d5` |
| Case manifest | `d4b926e855cbf8203d8f434db3fa6a427eb71fbd02a07d274fe5ef485cfeb875` |
| Review repair 01 | `c3b4929ac3ae950bc6b05439e0fd654438ef3e8caf9ff3eca238d459a03666b7` |
| VI repair 01 | `f47672d4c22fab85fc43473d7c14f305282d6aab80f2cf72f78e256a27f3c210` |
| [VI repair 02](../evaluation/personal-use/native/agy-gemini-r24-repair-02/real-source-vi-prose-taste-01.md) | `26a89daa1ab779cde8fdd1e1c6e839f335b255074137c6a16a5d8a4874b3642c` |
| EN repair 01 | `97a9c44c3124a3d410f86221933981d3afc193a33c0c58e30bfcdbf5861ad090` |
| [EN repair 02](../evaluation/personal-use/native/agy-gemini-r24-repair-02/real-source-en-scientific-fidelity-01.md) | `cd192529ca791abaaa7cf5e7a44fc187fea235cff524013906f959018462a2a8` |

Năm input paths duy nhất của hai case đều có hash và byte count khớp manifest: `reader-ready.jsonl`, child Wikisource JSON/HTML, PMC XML và `pmc-scientific.jsonl`. Đây là kiểm tra pinned bytes hiện có, không truy cập website hoặc cập nhật snapshot. Trạng thái `prepared-not-run`/all-model policy trong case manifest là hồ sơ lúc chuẩn bị; prompt repair 02 và quyết định model hiện hành được ghi riêng, không dùng manifest cũ làm xác nhận trạng thái thực thi mới.

## VI: delta và source preservation

VI có 82 dòng trước/sau. Chỉ dòng 11, 38, 39 và 74 đổi:

- Dòng 11 đổi hai reader-receipt paths sang thư mục repair 02; source ID, child/parent oldids, locator, record hash và rights limits giữ nguyên.
- Dòng 38 ghi nguồn chỉ gọi Đặng-cách-luân là `mại bản`, không định nghĩa nhiệm vụ. Cách hiểu thương vụ/tài chính được nhắc trong câu có gắn trực tiếp `tentative contextual reading`, từ chối trình bày đó như nghĩa từ điển hoặc sự thực lịch sử đã xác minh. Không còn định nghĩa chức việc được đặt trong ngoặc như kết luận nguồn.
- Dòng 39 dẫn lời Đàm xin lỗi vì chưa nhận thấy người khách. Câu về mắt mờ/nhìn không rõ được ghi là suy đoán tạm theo ngữ cảnh, không phải nghĩa từ điển hoặc chẩn đoán triệu chứng đã xác minh. Không có claim về bệnh lý mới.
- Dòng 74 dùng ví dụ bám đoạn nguồn cho chú thích phụ trợ, bỏ attribution `tham khảo từ từ điển` cũ và yêu cầu mọi giải thích thêm nêu đúng trạng thái phỏng đoán. Đây là đề xuất ngoài source text; bản gốc không bị hiện đại hóa.

Ba anchors bắt buộc hiện diện nguyên văn trong cả memo mới, memo cũ và installed selected record. Đã so các fragment trong dấu ngoặc kép: 14 fragment ở memo mới đều là chuỗi nguồn; hai fragment thêm tại dòng 38–39 cũng khớp đoạn nguồn sau khi nhận diện dấu `...` ở cuối fragment thứ nhất là rút gọn. Mọi fragment cũ được giữ. Các đoạn quote về phẩm chất chủ tàu, Đặng và Đàm, narrative opening và hai lời thoại anchors không đổi.

Phân biệt evidence/taste/context caveats, tối đa hai đề xuất, giới hạn một trang con và page-license/underlying-work rights boundary được bảo toàn. Kết luận PASS này đóng đúng hai gloss được giao sửa; không phải xác nhận từ điển cho mọi từ cổ hoặc phán quyết khẩu vị văn học.

## EN: conclusion và số đếm

EN chỉ đổi dòng 14 (receipt path) và dòng 36 (count label). Sau khi chuẩn hóa hai phần này, toàn bộ memo trước/sau bằng nhau. Năm ledger rows, numbers, association wording, non-causal/generalization limits, giới hạn projection 9,000 characters và ghi nhận Abstract/Results discrepancy giữ nguyên; không thêm claim nguồn mới.

Lấy paragraph ngay dưới `## 3. Faithful conclusion`, trước count note:

- Conclusion repair 02 bằng repair 01 từng ký tự.
- `len(paragraph.split())` bằng **161** cho cả hai bản.
- Paragraph UTF-8 SHA-256: `acccda8557ed60f09aa6ba34814fbb15d6c5a48236d00094958c8a3d13c66512`.
- Count note mới ghi rõ `161 whitespace-separated tokens` và `Python str.split()`; không còn `178`/`standard words`. Review tái lập phép đếm này, không suy từ count note rằng model đã chạy Python mới.

Do ledger/source inputs không đổi và khớp binding đã xác minh, kết quả source-fidelity của review repair 01 vẫn áp dụng. Không chuyển các association thành causality, first authorship thành career stage hoặc source discrepancy thành lời hòa giải mới.

## Ba reader receipts và installed source

| Receipt repair 02 | SHA-256 bytes |
|---|---|
| [nckh-taste / VI](../evaluation/personal-use/native/agy-gemini-r24-repair-02/reader-receipts/nckh-taste__R-vi-wikisource-passages__vi-wikisource-19383.json) | `def004febd95f984aa353888d543c9af4609e38e46580273f1b6474119a7e267` |
| [nckh-write / VI](../evaluation/personal-use/native/agy-gemini-r24-repair-02/reader-receipts/nckh-write__R-vi-wikisource-passages__vi-wikisource-19383.json) | `40a058ed49cc9f78eb5b24c62a71491cd6dfc7ccca7269b7ed508931af410939` |
| [nckh-write / PMC](../evaluation/personal-use/native/agy-gemini-r24-repair-02/reader-receipts/nckh-write__R-pmc-scientific__pmc-PMC13623154.json) | `90818d10ce0f8eb9a9f4271a20c7434b095b2d38bfe786925239066c4f4ef29d` |

Mỗi receipt có `status=matched`, `resource_read=true`, đúng query/record ID và consumer/domain/locale/genre. Consumer nằm trong resource catalog của đúng installed skill. `records[0].content` bằng record lấy trực tiếp từ resource JSONL tương ứng. Canonical hash được tính lại bằng JSON sort keys, UTF-8, `ensure_ascii=False`, separators `(',', ':')` và khớp cả record hash trong receipt/provenance.

| Binding | SHA-256 |
|---|---|
| VI selected record | `13149ead6bebde7171e5697919acfacfda9b22850023caf6e51971edf7080566` |
| Installed VI resource, cả nckh-taste/nckh-write | `36d52fcd6a97ed5d8376ab5c1862c39404359e4843944362c8b396945470492f` |
| PMC selected record | `546888bb164ac36cd719f432ccacb7ed3dba076704b8191c47c88f5efe2f0223` |
| Installed PMC resource, nckh-write | `b2dadda901d4ca37ea8124aca1f7f282f9adbee4582638bc5f334a4a389eeb45` |
| Installed reader, cả hai consumers | `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb` |

Route đọc được xác minh: `.agents/skills/<consumer>/references/_shared/core/registry/catalog/resources.json` → resource `path`; reader `scripts/search-resource.py`. Hai catalogs cùng hash `08280a57da31f62d88666b4dcca5f6b31589d73f0544c5751ba4632f1cd1ad9b`. r25 installation không làm thay đổi các resource/reader bytes của hai consumers so với nguồn đã dùng ở r24.

Ba receipts có đối tượng JSON bằng repair 01; byte formatting khác repair 01 nhưng bytes bằng ba receipts originals ở `agy-gemini-r24/`. Không dùng sự hiện diện, formatting hoặc field `resource_read=true` để kết luận reader được gọi mới ở repair 02. `policy_applicability=unverified`, `evidence_class=resource-read-observation`, `human_acceptance=not-evaluated` giữ đúng giá trị. Selected/requested Gemini 3.8 Flash High và completion do người dùng báo vẫn tách khỏi effective telemetry chưa được cung cấp.

## Việc còn lại và giới hạn

Không yêu cầu repair tiếp cho hai findings đã giao trong scope này. Owner tiếp tục dùng/chấm các artifacts cố định và phản hồi theo hash/revision; owner acceptance vẫn `pending-personal-review`. Review không tạo human gold, scientific/stable certification, fresh effective-model confirmation hoặc quyền publishing. World Bank/native visual QA giữ evidence riêng; report này không đóng toàn bộ plan thay controller.

Đã đối chiếu lại 28 input paths trước/sau khi ghi report: originals, memos/receipts repair, prompt/manifest/prior review, raw/derived inputs và installed catalog/resource/reader bytes giữ nguyên. Chỉ report này được tạo.
