# Memo khẩu vị văn xuôi Việt: *Thầy trò trong khám/I*

## Source receipt

| Trường | Giá trị |
|---|---|
| Case | `real-source-vi-prose-taste-01` |
| Bản memo | `r1`, ngày 03/10/2026 |
| Đường dẫn controller lưu | `plans/evaluation/personal-use/native/real-source-vi-prose-taste-01.md` |
| Skill | `nckh-taste` — phê bình khẩu vị; `nckh-write` — trình bày memo và giữ nguyên trích dẫn |
| Resource id | `R-vi-wikisource-passages` |
| Record id / source id | `vi-wikisource-19383` |
| Trang con | `Thầy trò trong khám/I` |
| Child oldid | `19383` |
| Parent source id / parent oldid | `vi-wikisource-106841` / `106841` |
| Loại mẫu trong record | `actual-passage`, `translated-novel`, tiếng Việt |
| Kết quả reader | `status=matched`, `resource_read=true`; trả về một record đúng selector |
| Phạm vi | Một trang con được cộng đồng chép lại; nhận xét giới hạn trong đoạn thực tế đã đọc |

**Locator chính xác:**  
[Thầy trò trong khám/I, oldid 19383](https://vi.wikisource.org/w/index.php?title=Th%E1%BA%A7y_tr%C3%B2_trong_kh%C3%A1m%2FI&oldid=19383)

**Lệnh reader đã chạy**, từ `C:/Users/USER/Downloads/test-skill`:

```powershell
python -I .agents/skills/nckh-taste/references/_shared/scripts/search-resource.py --resource-id R-vi-wikisource-passages --consumer nckh-taste --domain language-literary --locale vi --genre prose-verse-samples --query vi-wikisource-19383 --json
```

**Biên nhận SHA-256:**

| Đối tượng | SHA-256 | Căn cứ |
|---|---|---|
| Resource JSONL đã cài | `36d52fcd6a97ed5d8376ab5c1862c39404359e4843944362c8b396945470492f` | Reader trả về `resource_sha256` và `artifact_sha256` |
| Record được chọn | `13149ead6bebde7171e5697919acfacfda9b22850023caf6e51971edf7080566` | Reader trả về `record_sha256` |
| Reader | `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb` | Reader trả về `reader_sha256` |
| Acquisition `derived/reader-ready.jsonl` | `16175d1edc8116d07d9e952584f3ef47b3227cf8bd7d599cc30c695bff4f893e` | Đã tính trực tiếp; kích thước `221904` byte, khớp pin của brief |
| Child API JSON | `f52fbe45efebb62659384352ae8151bf3aa19d048b45418b17cdf39f9c977c1a` | Lineage của record; `31106` byte |
| Child HTML | `5220e82099a8fa6a0beced7f660c14afdbeba9d79893c5fac6dbf627ccfa7661` | Lineage của record; `71196` byte |

Resource đã cài khả dụng; **không có gap cần dùng fallback**. Đã đọc đúng record trong acquisition `reader-ready.jsonl` để đối chiếu: trường `text` bằng chính xác trường `text` của record trong resource đã cài. Hai hash file JSONL khác nhau thuộc hai gói có phạm vi khác nhau; phép đối chiếu trên xác nhận riêng nội dung passage được chọn. Hash raw JSON và HTML ở bảng trên là metadata lineage đã đọc, chưa được tính lại từ raw files trong lần này.

Ba neo bắt buộc đều xuất hiện chính xác trong passage:

> Vào khoảng năm 1815, tại cửa biển Mạc-xây nước Pháp

> Thân tôi đã hứa cho Đàm-đức-tư rồi, không thể nào dời đổi được.

> -- Chàng chết thì tôi đây cũng nguyện chết theo chàng.

## Anchored observations

### 1. Register: lời kể gần khẩu ngữ, xen cách nói trang trọng

**Quan sát có căn cứ.** Ngay đoạn mở đầu, sau neo “Vào khoảng năm 1815, tại cửa biển Mạc-xây nước Pháp”, người kể giới thiệu tàu, chủ tàu và người điều khiển bằng những cách nói như “Người chủ có tàu kêu là” và “làm vai đàn anh”. Cách giới thiệu ấy đưa nhân vật đến với người đọc qua quan hệ và vai trò dễ hình dung.

Ở những đoạn sau, “anh nầy”, “va”, “chớ” cùng tồn tại với “sở nguyện”, “ái tình”, “thiếp”, “mỗ”. Register thay đổi theo vị trí: lời kể thường trực tiếp, lời cầu hôn có sắc thái trang trọng, còn cuộc bàn mưu trong quán chuyển sang cách gọi gay gắt như “hai đứa nó”, “thằng kia”, “con nọ”.

**Diễn giải giới hạn.** Sự pha trộn này tạo cảm giác một truyện dịch được kể bằng giọng Việt giàu sắc thái giao tiếp. Riêng passage chưa đủ để xác lập niên đại bản dịch, phương ngữ của người dịch hay cách nói của cả một thời kỳ. Năm 1815 ở câu mở đầu là mốc trong câu chuyện.

### 2. Nhịp câu: phần dẫn chuyện dồn thông tin, đối thoại chia thành nhịp ngắn

**Quan sát có căn cứ.** Câu đầu đặt thời gian, địa điểm, tên tàu rồi nối các phẩm chất “vững chãi, đẹp đẽ và chạy mau có tiếng trong thời đó”. Đoạn giới thiệu Đặng-cách-luân tiếp tục gom tuổi tác, tính cách, thái độ của người trong tàu và động cơ ganh tị vào một câu nhiều vế. Nhịp kể vì vậy có xu hướng tích lũy thông tin trước khi chuyển sang hành động.

Đến cuộc cầu hôn, lượt lời tách riêng và dấu `--` làm nhịp đọc đổi rõ. Lời Mai-tây-đương:

> -- Thân tôi đã hứa cho Đàm-đức-tư rồi, không thể nào dời đổi được.

có hai vế: xác nhận lời hứa, rồi khép lại khả năng thay đổi. Cặp hỏi–đáp tiếp theo đẩy tình huống đến mức quyết liệt:

> -- Nếu chẳng may mà chàng va chết đi thì thế nào?  
> -- Chàng chết thì tôi đây cũng nguyện chết theo chàng.

Câu đáp ngắn, lặp “chết” và kết ở “theo chàng”, tạo một điểm nhấn cảm xúc rõ. Đây là lời nhân vật trong tình huống truyện; memo không suy rộng nó thành quan niệm sống của người dịch hoặc độc giả.

### 3. Từ vựng và chính tả lịch sử: có độ lạ đối với người đọc hiện nay

**Quan sát có căn cứ.** Đoạn kể việc trên tàu và trao thư giữ các dạng “bịnh”, “tánh”, “bình nhựt”, “sanh”, “nhơn”, “phong thơ”; đại từ “va” xuất hiện trong cả lời kể và lời thoại. Các tên “Mạc-xây”, “Đàm-đức-tư”, “Nã-phá-luân” được ghi bằng chuỗi âm tiết có gạch nối.

Độ khó không chỉ nằm ở chính tả. “Mại bản”, “thiệt thọ”, “mắt măng mắt vược” có thể khiến độc giả hiện đại phải dừng để đọc theo ngữ cảnh. Trong khi đó, “chúa tàu” được giới thiệu qua quan hệ thay người chủ điều khiển tàu, nên passage tự cung cấp một phần điểm tựa cho việc hiểu vai trò.

**Diễn giải giới hạn.** Những dạng này góp phần tạo sắc thái lịch sử của bản chép đang đọc. Chưa có đối chiếu bản in hoặc ảnh trang để phân loại từng trường hợp thành cách viết của bản dịch, biến thể chính tả hay lỗi sao chép. Vì vậy, memo giữ nguyên cả những chỗ dễ gây nghi vấn như “Uả hay!” và “mững rỡ”.

### 4. Giọng kể: định hướng đánh giá nhân vật, đồng thời dựng cảnh bằng cử chỉ

**Quan sát có căn cứ.** Người kể gọi Mã-lặc-nhi là “công bình, ngay thật”, mô tả Đặng-cách-luân có “tánh hiểm độc và khéo nịnh hót”, và mở đoạn thăm cha bằng “Đàm là người có hiếu”. Những nhận định ấy cho người đọc một hướng đánh giá khá sớm.

Tuy nhiên, cảnh Phất-nhĩ-nam chứng kiến đôi tình nhân còn dùng động tác: “hai hàm răng cắn sít lại”, “ngồi phịch xuống ghế dựa”, rồi chi tiết bàn tay giữ dao. Cảm xúc được thể hiện qua thân thể và hành vi bên cạnh lời nhận xét của người kể.

**Diễn giải giới hạn.** Passage kết hợp kể chuyện có phán xét đạo đức với cảnh ghen tuông và âm mưu giàu kịch tính. Cách phối hợp này phù hợp với nhãn `translated-novel` của record; nó chưa đủ để đánh giá phong cách toàn bộ tác phẩm.

### 5. Đối thoại: quan hệ xưng hô và cấu trúc lặp tạo sức ép

**Quan sát có căn cứ.** Trong cuộc cầu hôn, “em”, “tôi”, “chàng va” phân biệt người đang hỏi, người trả lời và người được nhắc đến. Khi Đàm xuất hiện, lời Mai chuyển sang “thiếp” và “chàng”, làm sắc thái giao tiếp thay đổi ngay trong cùng cảnh.

Ở quán rượu, Đặng-cách-luân dùng hai câu hỏi song song: “sống mà lìa nhau với chết mà xa nhau” và “sống mà ngồi trong ngục với chết mà nằm trong mả”. Các đáp án ngắn dẫn cuộc nói chuyện từng bước đến phương án hãm hại. Đây là cấu trúc thuyết phục của nhân vật trong truyện; memo không xác nhận lập luận ấy là đúng.

Dấu thoại `--`, dấu hỏi, dấu cảm và các lượt lời riêng là bằng chứng trực tiếp cho nhịp đối đáp. Giữ chúng giúp bảo toàn cách passage phân bố lời nhân vật.

## Defect versus subjective preference

| Điểm đọc | Phân loại | Nhận định trong phạm vi mẫu |
|---|---|---|
| “bịnh”, “nhơn”, “va” và tên có gạch nối | Đặc điểm văn bản cần bảo toàn | Khác thói quen đọc hiện nay chưa đủ để gọi là lỗi. |
| Câu dẫn chuyện nhiều vế, nhiều tên | Khẩu vị và công sức đọc | Độc giả muốn vào cảnh nhanh có thể thấy nặng thông tin; độc giả thích giọng kể tuần tự có thể thấy dễ theo dõi. |
| Lời thề chết theo người yêu | Nội dung và mức độ kịch tính | Có thể được cảm nhận là mạnh hoặc cường điệu tùy khẩu vị; không có căn cứ sửa lời nhân vật. |
| Nhận xét đạo đức trực tiếp của người kể | Lựa chọn giọng kể | Có thể hợp với người thích định hướng rõ, hoặc giảm khoảng trống suy đoán đối với người thích tự đánh giá nhân vật. |
| “Uả hay!”, “mững rỡ” | Điểm chưa xác minh | Cần đối chiếu chứng tích văn bản trước khi kết luận là lỗi; không tự sửa. |

**Chưa xác lập lỗi ngữ pháp hoặc lỗi sao chép cần sửa.** Những nhận xét về độ nặng, độ kịch và mức trực tiếp ở trên là đánh giá đọc có căn cứ vị trí, vẫn phụ thuộc khẩu vị.

**Lựa chọn khẩu vị đề nghị để owner cân nhắc:** giữ lớp chữ lịch sử, dấu thoại và nhịp hỏi–đáp; hỗ trợ độc giả hiện đại bằng chú giải ngoài passage. Đây là phương án biên tập đề nghị, chưa phải sở thích đã được owner xác nhận.

## Optional bounded suggestions

1. **Thêm một chú giải ngắn ngoài văn bản tại lần đầu gặp “va”.** Có thể dùng: *“Trong đoạn này, ‘va’ là cách gọi người được nhắc đến; hãy theo tên và hành động ở câu liền trước để xác định nhân vật.”* Chú giải này hỗ trợ theo dõi mà giữ nguyên từ trong passage. Không dùng nó để gán tác giả, niên đại hoặc phương ngữ.

2. **Thêm một dòng định hướng trước đoạn mở bằng “Lúc Lý-khắc-lai chết giữa đường”.** Có thể dùng: *“Đoạn sau chuyển sang bối cảnh chính trị và việc trao thư, làm nền cho âm mưu về cuối trang.”* Dòng này thuộc phần hướng dẫn đọc của người biên tập, cần đặt ngoài và ghi rõ không thuộc nguyên văn. Nó giúp người đọc nhận ra sự chuyển đoạn mà không cắt hoặc viết lại câu kể.

Cả hai đề xuất đều tùy chọn và chưa được áp dụng vào nguồn. Không thay tên, sửa chính tả, đổi `--` hoặc giảm mức quyết liệt của lời thoại.

## Limitations and rights boundary

- **Phạm vi văn bản:** đây là trang con *Thầy trò trong khám/I* ở `child_oldid=19383`, được chép lại trên Wikisource. Không đại diện cho toàn bộ tác phẩm. Brief ghi parent `oldid=106841` có lưu ý thiếu kỳ XIV; memo giữ giới hạn đó, chưa kiểm chứng độc lập trang parent trong lần đọc này.
- **Giới hạn chứng tích:** record ghi nội dung được trích từ `parse.text` của API trang con, loại bỏ markup và thành phần bố cục. Chưa đối chiếu ảnh bản in, ấn bản gốc hoặc thông tin người dịch; không suy đoán các dữ kiện này.
- **Quyền sử dụng:** metadata ghi văn bản trang theo **CC BY-SA 4.0**, với [locator giấy phép Wikimedia](https://foundation.wikimedia.org/wiki/Legal%3AText_of_the_Creative_Commons_Attribution-ShareAlike_4.0_International_License/en). Lý do public domain của tác phẩm nền là một trường riêng và còn phụ thuộc thẩm quyền pháp lý. Metadata đóng gói `permitted-with-notices` không tạo quyền tái phân phối phổ quát.
- **QA đã quan sát:** reader chọn đúng một actual passage; hash và kích thước acquisition JSONL khớp pin; passage đã cài bằng chính xác passage acquisition; cả ba neo bắt buộc hiện diện nguyên văn. Đây là kiểm tra đọc và đối chiếu có giới hạn, không phải chứng nhận chất lượng văn chương.
- **Trạng thái chấp nhận:** `pending-personal-review`. Hai skill vẫn ở trạng thái `experimental`. Chưa có phản hồi owner, human gold, xác nhận của người đọc bản ngữ hoặc chứng nhận khoa học/native.
- **Biên nhận artifact:** toàn bộ memo được giao trong câu trả lời cuối để controller lưu; chưa có file đầu ra hoặc SHA-256 của file đã lưu. Phản hồi owner sau sử dụng cần gắn với revision `r1`, hash artifact thực lưu và các hash đầu vào ở trên.