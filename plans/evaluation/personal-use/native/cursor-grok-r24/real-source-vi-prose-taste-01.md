# Memo khẩu vị: Thầy trò trong khám/I

Case `real-source-vi-prose-taste-01`. Văn bản gốc dưới đây được giữ nguyên chính tả. Phần đề xuất không thay thế trang nguồn.

## Source receipt

- `source_id`: `vi-wikisource-19383`
- `child_oldid`: 19383
- `child_title`: Thầy trò trong khám/I
- `parent_source_id`: `vi-wikisource-106841`
- `parent_oldid`: 106841
- Locator: `https://vi.wikisource.org/w/index.php?title=Th%E1%BA%A7y_tr%C3%B2_trong_kh%C3%A1m%2FI&oldid=19383`
- Query reader: đúng `vi-wikisource-19383`. Không dùng câu mô tả `record_selector`.
- Reader `nckh-taste`: `C:/Users/USER\Downloads\test-skill\.agents\skills\nckh-taste\references\_shared\scripts\search-resource.py`
- Pack: `R-vi-wikisource-passages`, domain `language-literary`, locale `vi`, genre `prose-verse-samples`
- Receipt: `plans/evaluation/personal-use/native/cursor-grok-r24/reader-receipts/nckh-taste__R-vi-wikisource-passages__vi-wikisource-19383.json`
- Reader `nckh-write` cùng query: `C:/Users/USER\Downloads\test-skill\.agents\skills\nckh-write\references\_shared\scripts\search-resource.py`
- Receipt write: `plans/evaluation/personal-use/native/cursor-grok-r24/reader-receipts/nckh-write__R-vi-wikisource-passages__vi-wikisource-19383.json`
- Cả hai lần đọc: `status=matched`, 1 record, `actual_passage=true`, `sample_role=actual-passage`, `genre=translated-novel`
- `resource_sha256`: `36d52fcd6a97ed5d8376ab5c1862c39404359e4843944362c8b396945470492f`
- `record_sha256`: `13149ead6bebde7171e5697919acfacfda9b22850023caf6e51971edf7080566`
- `reader_sha256`: `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb`
- Raw API JSON: `raw/vi-child-thay-tro-19383.json`, SHA-256 `f52fbe45efebb62659384352ae8151bf3aa19d048b45418b17cdf39f9c977c1a`, 31106 byte
- Raw HTML: `raw/vi-child-thay-tro-19383.html`, SHA-256 `5220e82099a8fa6a0beced7f660c14afdbeba9d79893c5fac6dbf627ccfa7661`, 71196 byte
- Chuẩn hóa trong record: rendered HTML visible-text; chỉ khoảng trắng và ranh giới đoạn; không sửa chính tả
- Giấy phép trang: `CC BY-SA 4.0 (Wikisource page footer)`; locator CC BY-SA 4.0 của Wikimedia Foundation
- Tác phẩm nền: `public-domain rationale stated by the page; jurisdiction must be checked before redistribution`
- `rights_rationale`: trang con công bố giấy phép trang và một lý do public-domain; hai trường này phải tách nhau

Ba neo nguyên văn có trong `text` của record:

- Vào khoảng năm 1815, tại cửa biển Mạc-xây nước Pháp
- Thân tôi đã hứa cho Đàm-đức-tư rồi, không thể nào dời đổi được.
- -- Chàng chết thì tôi đây cũng nguyện chết theo chàng.

## Anchored observations

Đoạn mở là câu kể dài, xếp năm, địa điểm, tên tàu và tính từ liền nhau: “Vào khoảng năm 1815, tại cửa biển Mạc-xây nước Pháp có chiếc tàu buồm tên là Phan-long, vững chãi, đẹp đẽ và chạy mau có tiếng trong thời đó.” Nhịp đoạn trần thuật đi theo chuỗi sự kiện và câu giải thích của người kể, ví dụ câu chua tên Huê-linh-tôn ngay trong đoạn. Đối thoại đổi nhịp: lời thoại ngắn, xen lượt, và được đánh dấu bằng `--` đầu dòng chứ không phải ngoặc kép hiện đại.

Từ vựng và chính tả lịch sử nằm trong chính văn, gồm dạng như “anh nầy”, “bình nhựt”, “tánh”, “sanh lòng”, “nhơn làm”, “mững rỡ”, “nằn nì”. Tên riêng viết có gạch nối: Mạc-xây, Phan-long, Đàm-đức-tư, Nã-phá-luân. Trong cùng trang, tên chủ tàu xuất hiện cả “Mã-lặc-nhi” ở đoạn mở và “Mã-lạc-nhi” ở đoạn sau. Đây là quan sát về hai dạng chữ trong bản ghim, không phải phán quyết dạng nào đúng.

Register của trang là văn tiểu thuyết dịch (`translated-novel`): người kể xưng “anh ta” / “va”, vừa thuật vừa giảng tên và phe phái cho người đọc. Lời Mai-tây-đương ở hai neo thoại giữ giọng quyết định ngắn, đối với câu hỏi của Phất-nhĩ-nam. Đó là bằng chứng vị trí trong trang, không phải chân dung độc giả phổ quát.

## Defect versus subjective preference

Việc trang kết ở heading “Chú thích” mà không có thân chú thích là ranh giới trích xuất: record nói phần navigation, số trang, references, bảng, ảnh, style và parser metadata bị loại. Không dùng chỗ đứt đó để sửa văn.

Hai dạng “Mã-lặc-nhi” và “Mã-lạc-nhi” là khác biệt quan sát được. Memo này không gọi một dạng là lỗi và không sửa dạng kia.

Câu mở dài và dày tính từ có thể làm người đọc hôm nay tốn sức. Đó là khẩu vị về nhịp, không phải lỗi ngữ pháp của bản lịch sử. Chính tả cổ và dấu `--` là bằng chứng register, không phải defect cần chuẩn hóa.

## Optional bounded suggestions

Hai gợi ý nằm ngoài văn bản nguồn. Chúng không thay câu, không hiện đại hóa chính tả, và không khẳng định bản gốc sai.

1. Một bảng tên riêng đặt ngoài đoạn, giữ nguyên gạch nối trong trích dẫn, để người đọc hiện đại đối chiếu tên mà không đụng vào trang.
2. Một dòng hướng dẫn đọc, cũng đặt ngoài đoạn, nói rằng dòng bắt đầu bằng `--` là một lượt thoại. Dấu `--` trong bản ghim giữ nguyên.

## Limitations and rights boundary

Đây là một trang con được chép lại, oldid 19383, không phải toàn bộ *Thầy trò trong khám*. Record tự giới hạn: một trang con đã ghim, không phải tuyên bố đầy đủ tác phẩm. Query `vi-wikisource-19383` không trả record cha; ghi chú về số XIV ở record cha, nếu có trong brief, không được xác nhận bởi lần đọc này.

Giấy phép CC BY-SA của trang Wikisource và lý do public-domain của tác phẩm nền là hai câu hỏi pháp lý tách nhau. Memo không biến lý do public-domain thành quyền phân phối phổ quát.

Khẩu vị ở đây là nhận xét của phiên làm việc. Không có human gold, không có thẩm quyền văn học rộng, không có chứng nhận khoa học. Chủ sở hữu chấm sau khi dùng. Trạng thái phản hồi: `pending-personal-review`.
