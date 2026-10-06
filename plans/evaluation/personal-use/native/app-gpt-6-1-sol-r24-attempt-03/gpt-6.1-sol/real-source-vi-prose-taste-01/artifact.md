# Memo tiếng Việt: register, nhịp câu và khẩu vị đọc *Thầy trò trong khám/I*

## Source receipt

**Case:** `real-source-vi-prose-taste-01`  
**Revision bàn giao:** attempt 03, ngày 2026-10-03, Asia/Saigon.  
**Skills đã đọc và áp dụng:** `nckh-taste`, `nckh-write`, cùng các policy bắt buộc, profile tiếng Việt, acceptance criteria theo đúng skill ID, resource lookup, resource rights contract và fidelity contract có liên quan.

**Đường dẫn controller được yêu cầu lưu:**

```text
plans/evaluation/personal-use/native/app-gpt-6-1-sol-r24-attempt-03/gpt-6.1-sol/real-source-vi-prose-taste-01/artifact.md
```

Đây là đường dẫn bàn giao theo output contract. Artifact hiện được trả trong final; tôi chưa tạo file hoặc tính hash của artifact được controller lưu.

### Nguồn thực tế đã đọc

| Trường | Giá trị |
|---|---|
| Resource ID | `R-vi-wikisource-passages` |
| Record ID | `vi-wikisource-19383` |
| Source ID | `vi-wikisource-19383` |
| Tên trang con | `Thầy trò trong khám/I` |
| Child oldid | `19383` |
| Parent source ID | `vi-wikisource-106841` |
| Parent oldid | `106841` |
| Vai trò mẫu | `actual-passage`, `actual_passage=true` |
| Genre trong record | `translated-novel` |
| Snapshot được ghi trong receipt | `2026-10-03` |
| Locator exact | `https://vi.wikisource.org/w/index.php?title=Th%E1%BA%A7y_tr%C3%B2_trong_kh%C3%A1m%2FI&oldid=19383` |

**Lệnh reader đã chạy**, từ `C:/Users/USER/Downloads/test-skill`:

```text
python -I .agents/skills/nckh-taste/references/_shared/scripts/search-resource.py --resource-id R-vi-wikisource-passages --consumer nckh-taste --domain language-literary --locale vi --genre prose-verse-samples --query vi-wikisource-19383 --json
```

Reader hoàn tất **exit 0**, trả `status=matched`, `resource_read=true`, đúng một record. Query chỉ dùng source ID. Installed resource có sẵn; **không dùng fallback** hoặc dữ liệu tổng hợp. Record acquisition được đọc bổ sung để kiểm tra ba neo và đối chiếu hash đầu vào, không thay thế passage của installed reader.

### Hash và lineage

| Đối tượng | SHA-256 | Evidence trong lượt này |
|---|---|---|
| Installed resource pack | `36d52fcd6a97ed5d8376ab5c1862c39404359e4843944362c8b396945470492f` | Reader receipt trả `resource_sha256` |
| Record được chọn | `13149ead6bebde7171e5697919acfacfda9b22850023caf6e51971edf7080566` | Reader receipt trả `record_sha256` |
| Installed reader | `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb` | Reader receipt trả `reader_sha256` |
| Acquisition `derived/reader-ready.jsonl` | `16175d1edc8116d07d9e952584f3ef47b3227cf8bd7d599cc30c695bff4f893e` | Tính lại bằng `Get-FileHash`; 221904 byte |
| Raw child API JSON | `f52fbe45efebb62659384352ae8151bf3aa19d048b45418b17cdf39f9c977c1a` | Tính lại bằng `Get-FileHash`; 31106 byte |
| Raw child HTML | `5220e82099a8fa6a0beced7f660c14afdbeba9d79893c5fac6dbf627ccfa7661` | Tính lại bằng `Get-FileHash`; 71196 byte |
| Repair evidence `plans/reports/review-261003-1435-gpt-6-1-sol-r24-output.md` | `c271ccf60192806e12111eb8aa2b13fdd8899eae5ef8b3405df21d07b38c51cc` | Đã đọc và tính lại hash; khớp hash được cấp |

Ba file acquisition nằm trong `plans/evaluation/personal-use/source-acquisition/`. Theo provenance của record, passage được trích từ rendered `parse.text` của child API response đã pin; normalization chỉ xử lý whitespace và ranh giới đoạn, không sửa chính tả hoặc nội dung. Lượt này không tái dựng extraction từ raw HTML.

Một lệnh trình bày hash ban đầu lỗi vì PowerShell constrained language không cho tạo `PSCustomObject`. Lệnh đọc hash trực tiếp sau đó hoàn tất; đây là lỗi trình bày của kiểm tra phụ, không phải lỗi installed reader.

### Ngoại lệ đọc instruction-authority của host

Đã đọc `C:/Users/USER/.claude/rules/development-rules.md` theo developer instruction bắt buộc. Đây là **ngoại lệ đọc authority của host**, được ghi riêng khỏi case/source reads. Không dùng ngoại lệ đó để mở rộng quyền đọc source, cấu hình, dữ liệu người dùng hoặc kiểm thử ngoài project.

Các thao tác của lượt này là đọc contract, đọc nguồn, chạy resource reader và kiểm tra hash/chuỗi trong project. Không tạo hoặc sửa file, chạy tests, thay cấu hình/provider, gọi model bổ sung, dùng UI, gửi thông điệp ra ngoài, tạo agent con hoặc publishing.

## Anchored observations

### Ba neo nguyên văn

**Neo 1 — mở đầu lời kể:**

```text
Vào khoảng năm 1815, tại cửa biển Mạc-xây nước Pháp
```

**Neo 2 — lời từ chối cầu hôn của Mai-tây-đương:**

```text
Thân tôi đã hứa cho Đàm-đức-tư rồi, không thể nào dời đổi được.
```

**Neo 3 — lời đáp khi Phất-nhĩ-nam đặt giả định Đàm chết:**

```text
-- Chàng chết thì tôi đây cũng nguyện chết theo chàng.
```

Cả ba chuỗi có trong passage do reader trả; kiểm tra chuỗi trên record acquisition cũng trả `True` cho từng neo. Chính tả, tên riêng và dấu câu trong các phần trích được giữ nguyên.

### 1. Register: lời kể giải thích rõ, lời thoại thay đổi theo quan hệ

**Vị trí:** đoạn mở đầu giới thiệu tàu Phan-long, chủ tàu và hai người giữ chức chúa tàu; cảnh Mai-tây-đương từ chối Phất-nhĩ-nam; cảnh Đàm chào người đang ngồi trong nhà.

Ở phần mở đầu, người kể giới thiệu nhân vật bằng vai trò, tuổi và phẩm chất. Cụm `“là người công bình, ngay thật”` cho thấy lời kể đánh giá trực tiếp, thay vì chỉ để độc giả suy từ hành động. Cách gọi `“chúa tàu”` và hệ thống tên có gạch nối cũng là những dấu hiệu cụ thể của register trong passage này.

Ở cảnh cầu hôn, neo 2 đặt một quyết định dứt khoát vào lời nói của Mai-tây-đương. Đến câu `“-- Uả hay! Tôi còn sống một ngày thì cái tình ấy cứ đượm đà một ngày chứ sao?”`, lời thoại có cảm thán và phản vấn, nghe gần lời nói hơn phần giới thiệu nhân vật.

Khi Đàm bước vào, lời chào dùng `“người quý khách”`, còn Mai gọi mình là `“thiếp”`. Những lựa chọn xưng hô ấy tạo sắc thái lễ độ và tình cảm khác với lời chọc ghẹo ở quán rượu.

**Lựa chọn khẩu vị:** tôi thiên về giữ sự thay đổi register này vì nó giúp phân biệt lời kể, lời tình tự và lời kích động. Đây là ưu tiên đọc cá nhân, chưa phải đánh giá của chủ dự án hoặc bằng chứng về độc giả bản ngữ nói chung.

### 2. Nhịp câu: kể dồn bối cảnh rồi chuyển sang lượt thoại ngắn

**Vị trí:** đoạn bắt đầu `“Lúc Lý-khắc-lai chết giữa đường”`; chuỗi hỏi đáp giữa Phất-nhĩ-nam và Mai-tây-đương.

Đoạn về Nã-phá-luân tạm chậm nhịp hành động để giải thích phe phái, việc bị đày và việc vận động trở về. Câu chứa nhiều tên và quan hệ chính trị khiến độc giả phải giữ nhiều thông tin cùng lúc. Đây là quan sát về lượng thông tin trong đoạn, không phải kết luận rằng thông tin lịch sử ấy đã được xác minh.

Ở cảnh cầu hôn, nhịp đổi rõ qua hai câu hỏi:

```text
-- Nếu chẳng may mà chàng va chết đi thì thế nào?
```

```text
-- Nếu lại chẳng may mà chàng phụ em thì mới tính sao?
```

Cấu trúc giả định lặp lại khiến Phất-nhĩ-nam liên tục đẩy tình huống sang một bất trắc khác. Các lời đáp ngắn và quyết liệt của Mai-tây-đương, trong đó có neo 3, tạo một nhịp đối đáp căng hơn phần kể bối cảnh.

**Lựa chọn khẩu vị:** tôi thấy đoạn thoại dễ theo dõi hơn đoạn chính trị vì mỗi lượt gắn với một người nói và một ý. Với người thích lời kể nhiều giải thích, đoạn bối cảnh vẫn có thể là phần hấp dẫn. Chưa có quan sát về tốc độ đọc hoặc mức hiểu của người dùng thực tế.

### 3. Từ vựng và chính tả lịch sử: dấu hiệu cần giữ, không tự động là lỗi

**Vị trí:** đoạn giới thiệu Đặng-cách-luân; đoạn Đàm được giao chức chúa tàu; đoạn Đàm về thăm cha; lời chào trong nhà Mai-tây-đương.

Các hình thức `“mại bản”`, `“thiệt thọ”`, `“mững rỡ”`, `“va”` và `“mắt măng mắt vược”` xuất hiện ở những vị trí có chức năng khác nhau: giới thiệu vai trò, xác nhận chức vụ, diễn tả niềm vui, quy chiếu nhân vật và lời tự nhận khi chào khách.

Đặc biệt, `“mại bản”` được trích đúng chữ thường như trong nguồn. Memo không đổi capitalization hoặc thay từ bằng một cách gọi hiện đại. Nghĩa nghề nghiệp chính xác của từ này không được xác minh bằng nguồn từ vựng riêng trong lượt đọc.

**Lựa chọn khẩu vị:** giữ các hình thức ấy giúp người đọc tiếp xúc với giọng văn của bản chép. Độc giả hiện đại có thể cần chú giải, nhưng nhu cầu chú giải không đủ để kết luận rằng nguyên văn sai hoặc cần sửa.

### 4. Giọng kể: phán xét trực tiếp đi cùng cử chỉ cụ thể

**Vị trí:** đoạn Đặng-cách-luân ganh chức chúa tàu; cảnh Phất-nhĩ-nam chứng kiến Đàm và Mai gặp nhau.

Lời kể gọi Đặng là người có `“tánh hiểm độc và khéo nịnh hót”`. Nhận định đạo đức được phát biểu trực tiếp ngay khi nhân vật xuất hiện trong xung đột.

Ở cảnh tình cảm, người kể lại dùng động tác cụ thể: `“hai hàm răng cắn sít lại”`, `“ngồi phịch xuống ghế dựa”` và `“một tay thò vào túi áo núm con dao nhỏ”`. Các chi tiết ấy đặt sự căng thẳng vào thân thể và vật đang cầm, giúp cảnh có dấu hiệu quan sát được trong thế giới truyện.

**Lựa chọn khẩu vị:** tôi thấy những cử chỉ này tạo sức nặng cho cảnh ghen tuông. Người đọc ưa lối kể kín hơn có thể thấy các lời phán xét trực tiếp quá rõ. Cả hai phản ứng đều thuộc khẩu vị; passage không cung cấp thước đo khách quan để phân xử.

### 5. Đối thoại, audience và genre: tình cảm dẫn sang âm mưu

**Vị trí:** cuộc đối đáp ở nhà Mai-tây-đương, cuộc uống rượu và đoạn Đặng viết giấy tố cáo.

Dấu mở lượt thoại `--` tạo ranh giới nhìn thấy được giữa người kể và lời nhân vật. Ở nhà Mai-tây-đương, các giả định về chết và phụ tình thử mức quyết tâm của nàng. Tại quán rượu, Đặng chuyển đối thoại sang khả năng làm hai người lìa nhau, rồi cụ thể hóa bằng giấy tố cáo. Vì vậy, lời thoại vừa bộc lộ thái độ vừa đưa cốt truyện đến hành động.

Record ghi genre là `translated-novel`. Trong passage đã đọc, việc giới thiệu nhân vật, dựng xung đột tình cảm, chuyển cảnh và kết bằng hành động đem giấy đến tòa Cảnh sát phù hợp với một đoạn tự sự tiểu thuyết.

**Audience đề xuất cho memo:** độc giả hiện đại muốn đọc văn xuôi có chính tả lịch sử và chấp nhận một ít chú giải. Đây là audience phục vụ bàn giao hiện tại; không phải kết luận về độc giả mục tiêu của bản dịch hoặc bản in ban đầu.

## Defect versus subjective preference

| Vấn đề | Phân loại | Căn cứ và cách xử lý |
|---|---|---|
| Viết hoa đầu từ khi trích `“mại bản”` | Lỗi fidelity nếu xảy ra trong memo | Nguồn dùng chữ thường; bản bàn giao này giữ đúng chữ thường. |
| Gắn nhãn controller save path cho một đường dẫn khác output contract | Lỗi handoff | Bản này ghi đúng đường dẫn attempt 03 và nói rõ chưa có file/hash do model lưu. |
| Từ và chính tả lịch sử gây khó đọc | Chi phí đọc có thể có; chưa chứng minh là lỗi văn bản | Giữ nguyên trích dẫn; chỉ đề xuất hỗ trợ ngoài passage. |
| Đoạn bối cảnh chính trị có nhiều tên và quan hệ | Quan sát có vị trí; mức dễ chịu là khẩu vị | Không cắt, chia hoặc viết lại nguồn. |
| Người kể đánh giá đạo đức nhân vật trực tiếp | Đặc điểm giọng kể; thích hay không là khẩu vị | Không đổi thành một giọng kể khác. |
| Lời thề tình cảm mạnh, cử chỉ ghen tuông rõ | Đặc điểm cảnh và đối thoại | Không coi mức kịch tính là lỗi ngữ pháp hoặc một chuẩn chất lượng tuyệt đối. |

Memo không xác lập lỗi ngữ pháp cần sửa trong nguyên văn. Muốn kết luận một hình thức là lỗi chép, lỗi in hoặc sai khác bản dịch cần đối chiếu thêm bản chứng; lượt này chưa có đối chiếu ấy.

**Factual-delta record:** không áp dụng rewrite lên passage. Ba neo, tên riêng và những trích dẫn phụ giữ nguyên hình thức đã đọc. Năm 1815 là mốc trong lời kể, không được dùng để suy ra năm sáng tác, dịch hoặc xuất bản. Memo không thêm danh tính tác giả/dịch giả, không xác nhận tính đúng của các chi tiết lịch sử và không nâng nhận xét khẩu vị thành kết luận khoa học.

## Optional bounded suggestions

Hai đề xuất sau chỉ dành cho phần hỗ trợ đọc bên ngoài passage; chưa được áp dụng vào văn bản nguồn.

1. **Thêm một lời dẫn ngắn trước đoạn trích.** Nội dung đề xuất: “Đoạn trích giữ nguyên chính tả và cách ghi tên của bản chép; một số hình thức có thể khác cách dùng hiện nay.” Lời dẫn giúp người đọc hiểu quy ước trình bày, không thay bất kỳ chữ nào trong passage.

2. **Thêm một chú giải nhận diện nhân vật trước khi đọc.** Chỉ ghi quan hệ hiện diện trong đoạn: Đàm-đức-tư được giao chức chúa tàu và sắp cưới Mai-tây-đương; Đặng-cách-luân ganh việc thăng chức; Phất-nhĩ-nam muốn cưới Mai-tây-đương. Giữ cách ghi tên của nguồn và đặt chú giải ngoài phần trích. Mục đích là giảm việc phải nhớ nhiều tên, không bổ sung tiểu sử hoặc sửa nội dung truyện.

Ưu tiên cá nhân của tôi là lời dẫn trước, chú giải nhân vật sau nếu chủ dự án thấy cần. Chưa có dữ liệu cho thấy hai đề xuất làm tăng mức hiểu hoặc mức hài lòng.

## Limitations and rights boundary

- **Phạm vi văn bản:** đây là một trang con đã pin, `Thầy trò trong khám/I`, không phải toàn bộ tác phẩm. Dữ kiện parent thiếu kỳ XIV đến từ brief và repair evidence; lượt này không đọc riêng parent để xác minh lại.
- **Phạm vi bản chứng:** đây là văn bản chép lại trên Wikisource, qua phép trích visible text được mô tả trong provenance. Không có đối chiếu trực tiếp bản in, bản thảo hoặc ảnh trang trong lượt này.
- **Quyền ở cấp trang:** record ghi `CC BY-SA 4.0 (Wikisource page footer)`. Metadata đó được giữ như thông tin quyền của snapshot.
- **Quyền của tác phẩm nền:** record ghi rationale public domain do trang nêu, đồng thời yêu cầu xem xét jurisdiction trước khi redistribution. Quyền cấp trang và tình trạng tác phẩm nền là hai câu hỏi riêng. Memo không xác nhận quyền tái phân phối phổ quát; nhãn rights của resource registry không mở rộng giới hạn này.
- **Đánh giá:** nhận xét về register, nhịp và giọng kể là phân tích của model trên passage đã đọc. Không phải human gold, chứng nhận native, kết luận khoa học, thẩm định toàn bộ tác phẩm hoặc bằng chứng rằng skill cải thiện chất lượng văn chương.
- **Model và runtime:** model được người dùng cho phép là `gpt-6.1-sol`. Lượt này không gọi model khác hoặc thực hiện fallback. Các lệnh đọc không cung cấp telemetry về effective model/effort của phiên; memo không tự xác nhận các trường đó.
- **Acceptance cá nhân:** trạng thái khẩu vị là `pending-personal-review`. Chủ dự án review sau khi sử dụng; feedback cần bind đúng revision, input hashes và hash artifact sau khi controller lưu. Không có yêu cầu external reviewer hoặc human-gold corpus cho lane personal-use này.
- **Bàn giao và lịch sử:** repair evidence đã được áp dụng vào cách trích `mại bản`, đường dẫn controller và việc ghi riêng host-authority read. Không sửa hoặc ghi đè attempt trước. Artifact hash và receipt sau lưu thuộc bước controller, chưa được quan sát tại thời điểm final này.

**Còn chưa xác nhận:** phản hồi khẩu vị của chủ dự án, hash artifact sau controller lưu và effective-model telemetry.