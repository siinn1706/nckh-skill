# Analytics mẫu 10 dòng bank.csv

Case `real-source-uci-analytics-01`. Mô tả mẫu đã đọc. Không phải response rate toàn tập, không phải causal lift, không phải forecast.

## Source/data receipt

- `source_id`: `uci-bank-marketing-bank-csv-first-10`
- Locator: `https://archive.ics.uci.edu/dataset/222/bank`
- DOI: `10.24432/C5K306`
- Query reader: `uci-bank-marketing-bank-csv-first-10`
- Reader: `C:/Users/USER\Downloads\test-skill\.agents\skills\nckh-analytics\references\_shared\scripts\search-resource.py`
- Pack: `R-uci-bank-marketing`, domain `marketing-analytics`, locale `und`, genre `campaign-response-tabular`, consumer `nckh-analytics`
- Receipt: `plans/evaluation/personal-use/native/cursor-grok-r24/reader-receipts/nckh-analytics__R-uci-bank-marketing__uci-bank-marketing-bank-csv-first-10.json`
- Status: `matched`, 1 record
- Pack `resource_sha256`: `647a774b9fb4545d6bc652114910df53677fbe993a00c268c16d4f50b03fe123`
- `record_sha256`: `d85b74d70eacd63a194a0188527a233d5dd65b77a6a12b4a9c3defba04d6eaf6`
- `reader_sha256`: `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb`
- Archive ngoài: `raw/uci-bank-marketing.zip`, SHA-256 `e0bf5f5de5b846e2f18e9d90606637267d46dfa260e0f17bb12e605db5efbeb4`, 1023843 byte
- Archive lồng: `raw/uci-bank.zip`, SHA-256 `99d7e8eb12401ed278b793984423915411ea8df099e1795f9fefe254f513fe5e`, 579043 byte
- File: `bank.csv`. Delimiter ghi trong record: `;`
- Chính sách mẫu: 10 dòng dữ liệu đầu; header và giá trị được giữ
- Tác giả trong provenance: S. Moro, P. Rita, P. Cortez
- Giấy phép: `CC BY 4.0`; `https://creativecommons.org/licenses/by/4.0/legalcode`; trang chính thức trùng locator ở trên
- `rights_rationale`: trang UCI ghi CC BY 4.0 và DOI `10.24432/C5K306`; hai archive được giữ để truy lineage
- Chuẩn hóa: giải nén zip và parse CSV; không biến đổi feature hay value
- `retrieved_at`: `2026-10-03`

Định nghĩa trước khi đếm:

- Sự kiện: một dòng trong 10 dòng đầu của `bank.csv`.
- Tập: đúng 10 dòng này. Không phải toàn bộ tập UCI.
- Đơn vị: một dòng. Mười bảy cột nguồn được giữ tên như record.
- Tử số: số dòng có giá trị category đang đếm.
- Mẫu số của mọi tỷ lệ trong memo này: 10 dòng. Không có mẫu số population.
- Cửa sổ thời gian và múi giờ: không có trong record.
- Thiếu: không thấy null ở các cột đã liệt kê. `pdays=-1` là chuỗi sentinel được giữ, không đổi thành 0 hay null.
- Loại trừ: không loại dòng.

Hợp đồng provider marketing tại `nckh-analytics/references/_shared/extensions/providers/marketing/contract.json` có `status=unavailable` và `engine_binding=null`. Memo này không gọi provider. Số liệu chỉ đến từ pack local.

## Descriptive counts and tables

10 dòng, 17 cột: age, job, marital, education, default, balance, housing, loan, contact, day, month, duration, campaign, pdays, previous, poutcome, y.

`y`: `no` trên cả 10 dòng. Trong mẫu này `y=yes` xuất hiện 0 lần. 10/10 và 0/10 là đếm của mẫu 10 dòng, không phải response rate của dataset.

`month`: may=5, apr=2, feb=1, jun=1, oct=1.

`balance` âm: dòng 10 có `balance=-88`. Các balance còn lại, theo thứ tự dòng: 1787, 4789, 1350, 1476, 0, 747, 307, 147, 221.

| # | age | job | marital | balance | month | duration | campaign | pdays | poutcome | y |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 30 | unemployed | married | 1787 | oct | 79 | 1 | -1 | unknown | no |
| 2 | 33 | services | married | 4789 | may | 220 | 1 | 339 | failure | no |
| 3 | 35 | management | single | 1350 | apr | 185 | 1 | 330 | failure | no |
| 4 | 30 | management | married | 1476 | jun | 199 | 4 | -1 | unknown | no |
| 5 | 59 | blue-collar | married | 0 | may | 226 | 1 | -1 | unknown | no |
| 6 | 35 | management | single | 747 | feb | 141 | 2 | 176 | failure | no |
| 7 | 36 | self-employed | married | 307 | may | 341 | 1 | 330 | other | no |
| 8 | 39 | technician | married | 147 | may | 151 | 2 | -1 | unknown | no |
| 9 | 41 | entrepreneur | married | 221 | may | 57 | 2 | -1 | unknown | no |
| 10 | 43 | services | married | -88 | apr | 313 | 1 | 147 | failure | no |

`job` quan sát được: unemployed, services, management, management, blue-collar, management, self-employed, technician, entrepreneur, services. Đây là liệt kê dòng, không phải phân khúc khách hàng.

## Data-quality and leakage notes

Mẫu là 10 dòng đầu theo `sample_policy`, không phải mẫu ngẫu nhiên và không có tuyên bố đại diện. Record giới hạn: mẫu bounded, không tự nó đại diện.

`duration` là độ dài cuộc gọi sau khi tiếp xúc đã xảy ra. Trước khi cuộc gọi kết thúc, giá trị này chưa có. Dùng `duration` để dự báo `y` cho một lượt gọi chưa diễn ra sẽ đưa thông tin sau tiếp xúc vào đầu vào. Đó là rủi ro leakage của bài toán dự báo, không phải một hệ số lift.

`pdays=-1` và `poutcome=unknown` được giữ như chuỗi nguồn. `balance=-88` và `balance=0` là hai giá trị khác nhau.

Không có nhật ký đổi instrumentation trong record. Provider sống không được đọc, nên freshness ngoài snapshot `2026-10-03` là unknown.

## Non-causal interpretation limits

Mọi số trên là đếm mô tả trong 10 dòng. Chúng không đo hiệu quả chiến dịch, không quy nguyên nhân cho tháng, nghề, hay số dư, và không dự báo dòng tiếp theo. `y=no` trên 10/10 không được đọc thành “chiến dịch không có phản hồi”.

Bước đo tiếp, nếu chủ sở hữu muốn một tỷ lệ population, cần mẫu số của toàn bộ `bank.csv` và định nghĩa sự kiện trước khi gọi. Bước đó không nằm trong pack này.

Chủ sở hữu chấm sau khi dùng. Trạng thái: `pending-personal-review`. Không có chứng nhận nhân quả hay khoa học.
