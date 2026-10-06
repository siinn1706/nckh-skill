# real-source-worldbank-visual-01

Case `real-source-worldbank-visual-01`. Host cursor. Candidate r25. Runner ghi nhận trong phiên: Grok 4.7. Thư mục này chỉ chứa hiện vật của lượt chạy này.

## Source and data receipt

- Reader: `python -I .agents/skills/nckh-visuals/references/_shared/scripts/search-resource.py --resource-id R-worldbank-vietnam-population --consumer nckh-visuals --domain chart-measurement --locale und --genre indicator-time-series --query worldbank-vnm-SP.POP.TOTL-2000-2025 --json`
- Kết quả reader: status=`matched`, resource_read=true, đúng 1 record. stdout `plans/evaluation/personal-use/native/cursor-grok-r25-visual-01/reader.stdout.json`, sha256=`3afca7f91305ea19c0cf96f1f0eee4c523c6c74bd9d503761155de161faa6d5d`, stderr rỗng, exit 0.
- resource_id=`R-worldbank-vietnam-population`
- source_id=`worldbank-vnm-SP.POP.TOTL-2000-2025`
- API locator=`https://api.worldbank.org/v2/country/VNM/indicator/SP.POP.TOTL?date=2000%3A2025&format=json&per_page=100`
- response_lastupdated=`2026-07-13`
- raw_sha256=`a63e499e9f24ae600bb52ecac8acb07bbb959a812e830cc7cf870fbca2fe5781` (đã đối chiếu byte file `plans/evaluation/personal-use/source-acquisition/raw/worldbank-vnm-population-2000-2025.json`)
- series_sha256=`a29802fa36bc453ce9abbf9789e119bae689462ffd6348e327ee7d7f5e9cb4b2` (đã đối chiếu byte JSONL đóng gói trong skill)
- reader_sha256=`e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb`
- resource_sha256 trong stdout reader=`a29802fa36bc453ce9abbf9789e119bae689462ffd6348e327ee7d7f5e9cb4b2`
- Raw page: total=26, per_page=100, sourceid=2, lastupdated=2026-07-13
- 26 quan sát gốc trong JSON API và 26 dòng projection. Mọi `unit` đều là chuỗi rỗng. Mọi `value` khác null. `decimal` nguồn = 0, `obs_status` / `observation_status` rỗng. Không dùng decimal để làm tròn.
- Country nguồn: Viet Nam. countryiso3code=`VNM`. indicator id=`SP.POP.TOTL`. indicator value=`Population, total`.
- Thứ tự mảng nguồn giảm dần từ 2025 về 2000. Thứ tự hiển thị chỉ sắp năm tăng dần. Không sắp theo giá trị và không nội suy.
- Năm 2000 = 77154011. Năm 2025 = 101598527.
- Trong 25 cặp năm liên tiếp của bản ghi này, giá trị năm sau lớn hơn giá trị năm trước: true. Đây là mô tả dãy đã đọc, không phải nguyên nhân.
- Nhãn quyền trong record: CC BY 4.0 default with World Bank terms. Locator điều khoản: https://data.worldbank.org/summary-terms-of-use. Caveat nguồn: Third-party indicators may have additional restrictions.
- Checker binding: status=`integrity-verified`, binding_sha256=`f6f169101530c03e3ee75874af17ac86e34b451faf2acf6c6a66daf2dfa759a4`, capability=`svg-render`, global_status=`unavailable`, authorization=`not-established-by-checker`, acceptance=`pending-independent-gates`. stdout sha256=`8161dc9c32306c4f0cb7262b67aa1d1c351b964806dbf16ecdfe3582381a1967`, exit 0.

Phép tính cuối chuỗi, tách khỏi tọa độ dấu:

- Chênh lệch tuyệt đối = 101598527 - 77154011 = 24444516. Phép trừ số nguyên, kết quả đúng, không làm tròn.
- Phần trăm = (24444516 / 77154011) * 100. Thương hữu tỷ rút gọn = 2444451600/77154011. Mẫu sau khi bỏ thừa số 2 và 5 còn khác 1: true, nên khai triển thập phân không kết thúc.
- Khai triển Decimal precision 80: 31.682754639936995628133967007885046961459981646320370822976397170070652580848972
- Biểu diễn hữu hạn được yêu cầu, `31.682754639936995%`, trùng `repr` của giá trị IEEE-754 binary64 do CPython tính `(24444516 / 77154011) * 100`. Python: `3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]`.
- Chữ số thập phân ngay sau chuỗi đó trong khai triển đúng là `6`. Cắt cụt đúng 15 chữ số thập phân ra cùng các ký tự đó; làm tròn half-up tại vị trí đó không ra cùng chuỗi. Binary64 cũng không phải thương vô hạn đúng.

## Editable visual

- File: `plans/evaluation/personal-use/native/cursor-grok-r25-visual-01/real-source-worldbank-visual-01.svg`
- sha256 SVG=`410c47985a1419bace3234a7d177c4e906ad37ae222e1276918c0631139a49e6`
- width=1400, height=1794, viewBox=`0 0 1400 1794`
- Phần tử native: `text`, `line`, `polyline`, `circle`, `rect`, `title`, `desc`. Không có `image` hay `foreignObject`.
- 26 phần tử `circle`, mỗi cái có `data-year` và `data-value` bằng số nguyên gốc. Một `polyline` dùng đúng 26 cặp tọa độ đó, theo năm tăng dần.
- font-family trên mọi `text` hiển thị: `Arial`. Không khai báo họ font thứ hai. font-weight và font-style đều normal, để không gọi mặt Arial Bold/Italic.
- File font quan sát trên host, không chứng minh renderer đã chọn nó: `C:\Windows\Fonts\arial.ttf`, sha256=`b3658eadae55e682b5f69eb64c439c1ecc8f196c0bb8d4756d145d13bc86476a`.

Chưa mở SVG trong trình sửa đồ họa, chưa lưu từ trình đó và chưa mở lại. Cổng sửa được native, open, save/reopen vẫn pending.

## Axes/units/caption/alt text

- Trục giá trị, đúng cụm chữ: Population, total (SP.POP.TOTL; raw unit field blank)
- Trường unit gốc trống. Không gán persons hay đơn vị được cung cấp nào khác.
- Trục năm: nhãn `Năm`, vạch và nhãn chữ cho đủ năm 2000–2025 tại đúng tọa độ năm.
- Biên thang hiển thị: năm 2000..2025; giá trị trục 70000000..110000000. Hai biên giá trị không phải quan sát mới. Vạch y cách 5000000, nhãn là đúng giá trị vạch.
- x = 180 + (year - 2000) * 1160 / 25
- y = 668 - (value - 70000000) * 512 / 40000000
- x, y ghi trên dấu và trong bảng là dạng thập phân kết thúc đúng của hai thương này. Không lượng hóa thêm.
- Baseline nhãn vạch y đặt trên đúng y của vạch. Renderer có căn giữa glyph hay không chưa được chứng nhận.
- Tiêu đề thay thế (`title`): Biểu đồ 26 điểm quan sát chỉ số Population, total (SP.POP.TOTL) của Việt Nam, từ năm 2000 đến năm 2025, theo bản ghi worldbank-vnm-SP.POP.TOTL-2000-2025.
- Mô tả thay thế (`desc`): Thứ tự đọc: tiêu đề và mô tả này; dòng tiêu đề hiển thị; nhãn trục và nhãn thang với đúng giá trị vạch; đường polyline rồi 26 dấu tròn theo năm tăng dần; chú thích nguồn; bảng year, value, x, y. Giá trị năm 2000 là 77154011. Giá trị năm 2025 là 101598527. Mỗi dấu dùng đúng giá trị gốc, không thêm điểm nội suy. Hình mô tả các giá trị đã đọc và không nêu nguyên nhân. Trường unit gốc để trống. response_lastupdated=2026-07-13. Nhà cung cấp có thể hiệu đính số liệu. Chỉ báo của bên thứ ba có thể có hạn chế quyền riêng.
- `xml:lang` của svg là `vi`. Không đặt `role=img`, để thứ tự đọc đi theo thứ tự phần tử chứ không gói thành một tên ảnh duy nhất.
- Chú thích trong SVG gồm source_id, API locator, raw_sha256, response_lastupdated=2026-07-13, unit trống, hai cảnh báo hiệu đính và quyền bên thứ ba, công thức thang, và trạng thái cổng đang chờ.

## Hash and QA receipt

| Hạng mục | Giá trị |
| --- | --- |
| Binding | `plans/evaluation/personal-use/visual-engine-probe-02/cursor-binding.json` |
| binding_sha256 | `f6f169101530c03e3ee75874af17ac86e34b451faf2acf6c6a66daf2dfa759a4` |
| Engine | `C:\ProgramData\chocolatey\bin\rsvg-convert.exe` |
| executable_sha256 | `79a0ad2d5fb6f8afd0cf93c14d09a1ce73122c6fd54bdd8850965570a83d27c9` |
| Version command | `['C:\\ProgramData\\chocolatey\\bin\\rsvg-convert.exe', '--version']` |
| Version exit | 0 |
| Version stdout | `rsvg-convert version 2.40.20` |
| Version stdout sha256 | `6340d2262159b081b9d97e687ce8871ee76790bcd951db236672ad1d7c970d4e` |
| Version stderr sha256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Render command | `['C:\\ProgramData\\chocolatey\\bin\\rsvg-convert.exe', '-o', 'C:/Users/USER\\Downloads\\test-skill\\plans\\evaluation\\personal-use\\native\\cursor-grok-r25-visual-01\\real-source-worldbank-visual-01.png', 'C:/Users/USER\\Downloads\\test-skill\\plans\\evaluation\\personal-use\\native\\cursor-grok-r25-visual-01\\real-source-worldbank-visual-01.svg']` |
| Render exit | 0 |
| SVG sha256 | `410c47985a1419bace3234a7d177c4e906ad37ae222e1276918c0631139a49e6` |
| PNG sha256 | `507b929c94785a55953d6f25768d63cae720809ac48ebcf79777903e220346ed` |
| PNG IHDR width x height | 1400 x 1794 |
| Render stdout sha256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Render stderr sha256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Lệnh render không thêm cờ ngoài executable, `-o`, đường dẫn PNG và đường dẫn SVG. Exit 0 và chữ ký PNG chỉ cho thấy tiến trình kết thúc và có byte PNG. Kích thước IHDR là quan sát header, không phải cổng bố cục. Probe `visual-engine-probe-02` kiểm tra binding của probe, không chứng nhận SVG này.

Bảng year / value / x / y:

| year | value | x | y |
| --- | --- | --- | --- |
| 2000 | 77154011 | 180 | 576.4286592 |
| 2001 | 77969361 | 226.4 | 565.9921792 |
| 2002 | 78772224 | 272.8 | 555.7155328 |
| 2003 | 79563777 | 319.2 | 545.5836544 |
| 2004 | 80338971 | 365.6 | 535.6611712 |
| 2005 | 81088313 | 412 | 526.0695936 |
| 2006 | 82167897 | 458.4 | 512.2509184 |
| 2007 | 83633375 | 504.8 | 493.4928 |
| 2008 | 85175788 | 551.2 | 473.7499136 |
| 2009 | 86460018 | 597.6 | 457.3117696 |
| 2010 | 87455152 | 644 | 444.5740544 |
| 2011 | 88468314 | 690.4 | 431.6055808 |
| 2012 | 89510356 | 736.8 | 418.2674432 |
| 2013 | 90573104 | 783.2 | 404.6642688 |
| 2014 | 91679578 | 829.6 | 390.5014016 |
| 2015 | 92823254 | 876 | 375.8623488 |
| 2016 | 94000117 | 922.4 | 360.7985024 |
| 2017 | 95176977 | 968.8 | 345.7346944 |
| 2018 | 96237319 | 1015.2 | 332.1623168 |
| 2019 | 97173776 | 1061.6 | 320.1756672 |
| 2020 | 98079191 | 1108 | 308.5863552 |
| 2021 | 98935098 | 1154.4 | 297.6307456 |
| 2022 | 99680655 | 1200.8 | 288.087616 |
| 2023 | 100352192 | 1247.2 | 279.4919424 |
| 2024 | 100987686 | 1293.6 | 271.3576192 |
| 2025 | 101598527 | 1340 | 263.5388544 |

### Trạng thái cổng

| Cổng | Trạng thái |
| --- | --- |
| native editability | pending |
| open | pending |
| save/reopen | pending |
| layout | pending |
| accessibility | pending |
| source truth | pending |
| scientific meaning | pending |
| owner final score | pending-personal-review |

Không có điểm nào ở bảng trên được chuyển thành pass. Chưa có owner score sau khi dùng.

## Limitations

- Bản ghi là ảnh chụp API ngày response_lastupdated=2026-07-13. Nhà cung cấp có thể hiệu đính giá trị sau ngày đó.
- Trường unit gốc trống và được giữ trống.
- Chỉ báo của bên thứ ba có thể có hạn chế quyền riêng, ngoài nhãn CC BY 4.0 default với điều khoản World Bank.
- 31.682754639936995% là biểu diễn hữu hạn đã nêu ở trên, không phải thương đúng.
- Biên trục 70000000 và 110000000 là biên hiển thị.
- Kiểm tra native, mở/lưu/mở lại, bố cục, khả năng tiếp cận, sự thật nguồn và ý nghĩa khoa học còn chờ người kiểm soát trên đúng hash hiện vật cuối.
- global_status của hợp đồng native-documents vẫn là unavailable. Binding chỉ được đối chiếu cho task/host/capability này.
- Không chụp màn hình. Không có điểm owner sau sử dụng.

Sha256 của chính file Markdown này được ghi sau khi file đóng byte, tại `plans/evaluation/personal-use/native/cursor-grok-r25-visual-01/memo.sha256.txt`.
