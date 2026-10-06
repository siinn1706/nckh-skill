# Báo cáo Phân tích Mô tả Bị chặn: Mẫu 10 Dòng Đầu UCI Bank Marketing

## 1. Source/data receipt

- **Mã nguồn (source_id)**: `uci-bank-marketing-bank-csv-first-10`
- **Bộ dữ liệu gốc**: Bank Marketing (`bank.csv`)
- **Tác giả & Bản quyền ghi nhận (Attribution)**: S. Moro, P. Rita, P. Cortez
- **Giấy phép (License)**: `CC BY 4.0` (`https://creativecommons.org/licenses/by/4.0/legalcode`)
- **Mã định danh kỹ thuật số (DOI)**: `10.24432/C5K306`
- **Bộ định vị kho lưu trữ chính thức (Locator)**: `https://archive.ics.uci.edu/dataset/222/bank`
- **Tệp nén ngoài gốc (raw outer archive)**: `raw/uci-bank-marketing.zip`
  - Mã băm SHA-256: `e0bf5f5de5b846e2f18e9d90606637267d46dfa260e0f17bb12e605db5efbeb4`
  - Dung lượng: `1,023,843 bytes`
- **Tệp nén lồng chứa dữ liệu (nested archive)**: `raw/uci-bank.zip`
  - Mã băm SHA-256: `99d7e8eb12401ed278b793984423915411ea8df099e1795f9fefe254f513fe5e`
  - Dung lượng: `579,043 bytes`
- **Tệp tiếp nhận qua bộ đọc (reader receipt)**: `plans/evaluation/personal-use/native/agy-gemini-r24-repair-01/reader-receipts/nckh-analytics__R-uci-bank-marketing__uci-bank-marketing-bank-csv-first-10.json`
- **Mã băm bản ghi chiếu (record_sha256)**: `d85b74d70eacd63a194a0188527a233d5dd65b77a6a12b4a9c3defba04d6eaf6`
- **Cấu hình trích xuất mẫu**: 10 dòng đầu tiên của tệp `bank.csv`, phân cách bằng dấu chấm phẩy (delimiter `;`), đầy đủ 17 cột nguyên bản.

---

## 2. Descriptive counts and tables

### 2.1. Cấu trúc và bảng dữ liệu 10 dòng quan sát thực tế

Bộ dữ liệu mẫu gồm đúng **10 dòng quan sát** và **17 cột thuộc tính**, sử dụng dấu phân cách chấm phẩy (`;`). Các giá trị thực tế quan sát được ghi nhận chi tiết:

| Dòng | age | job | marital | education | default | balance | housing | loan | contact | day | month | duration | campaign | pdays | previous | poutcome | y |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 30 | unemployed | married | primary | no | 1787 | no | no | cellular | 19 | oct | 79 | 1 | -1 | 0 | unknown | no |
| 2 | 33 | services | married | secondary | no | 4789 | yes | yes | cellular | 11 | may | 220 | 1 | 339 | 4 | failure | no |
| 3 | 35 | management | single | tertiary | no | 1350 | yes | no | cellular | 16 | apr | 185 | 1 | 330 | 1 | failure | no |
| 4 | 30 | management | married | tertiary | no | 1476 | yes | yes | unknown | 3 | jun | 199 | 4 | -1 | 0 | unknown | no |
| 5 | 59 | blue-collar | married | secondary | no | 0 | yes | no | unknown | 5 | may | 226 | 1 | -1 | 0 | unknown | no |
| 6 | 35 | management | single | tertiary | no | 747 | no | no | cellular | 23 | feb | 141 | 2 | 176 | 3 | failure | no |
| 7 | 36 | self-employed | married | tertiary | no | 307 | yes | no | cellular | 14 | may | 341 | 1 | 330 | 2 | other | no |
| 8 | 39 | technician | married | secondary | no | 147 | yes | no | cellular | 6 | may | 151 | 2 | -1 | 0 | unknown | no |
| 9 | 41 | entrepreneur | married | tertiary | no | 221 | yes | no | unknown | 14 | may | 57 | 2 | -1 | 0 | unknown | no |
| 10 | 43 | services | married | primary | no | -88 | yes | yes | cellular | 17 | apr | 313 | 1 | 147 | 2 | failure | no |

### 2.2. Phân bố biến mục tiêu (Target `y`) trong mẫu quan sát

| Giá trị biến mục tiêu (`y`) | Số lượng quan sát | Tỷ lệ trong mẫu quan sát (N=10) |
|---|:---:|:---:|
| `no` (Không đăng ký tiền gửi kỳ hạn) | 10 | 100,0% |
| `yes` (Có đăng ký tiền gửi kỳ hạn) | 0 | 0,0% |
| **Tổng cộng** | **10** | **100,0%** |

*Lưu ý quan trọng*: Con số 100% `y=no` chỉ là tần số đếm mô tả thuần túy trên 10 dòng đầu tiên được trích xuất kỹ thuật, tuyệt đối không đại diện cho tỷ lệ phản hồi (response rate) của toàn bộ chiến dịch hoặc tổng thể tập dữ liệu Bank Marketing.

### 2.3. Phân bố tháng liên hệ (`month`)

| Tháng (`month`) | Các dòng quan sát xuất hiện | Tần số xuất hiện | Tỷ lệ mẫu |
|---|---|:---:|:---:|
| `may` (Tháng 5) | Dòng 2, 5, 7, 8, 9 | **5** | 50% |
| `apr` (Tháng 4) | Dòng 3, 10 | **2** | 20% |
| `feb` (Tháng 2) | Dòng 6 | **1** | 10% |
| `jun` (Tháng 6) | Dòng 4 | **1** | 10% |
| `oct` (Tháng 10) | Dòng 1 | **1** | 10% |
| **Tổng cộng** | | **10** | **100%** |

### 2.4. Quan sát số dư trung bình năm âm (`balance = -88`)

Dòng 10 có `balance = -88` euro; theo tài liệu `bank-names.txt` trong kho lưu trữ dữ liệu nguồn, thuộc tính số 6 `balance` được định nghĩa rõ là: `balance: average yearly balance, in euros (numeric)` (số dư trung bình năm, tính bằng euro). Giá trị âm được bảo toàn nguyên vẹn từ dữ liệu quan sát; riêng giá trị này không xác định giao dịch hay tình trạng thấu chi cụ thể, vì bộ dữ liệu tĩnh không theo dõi lịch sử giao dịch hay điều khoản thấu chi của tài khoản.

---

## 3. Data-quality and leakage notes

1. **Nguy cơ rò rỉ dữ liệu từ biến thời lượng (`duration` target leakage)**:
   - Cột `duration` ghi nhận thời lượng cuộc gọi tiếp xúc gần nhất tính bằng giây (trong mẫu dao động từ `57` giây ở dòng 9 đến `341` giây ở dòng 7).
   - *Rủi ro kỹ thuật*: Biến này chỉ được đo lường **sau khi** cuộc gọi đã kết thúc. Nếu mục tiêu là xây dựng mô hình dự báo tiền tiếp xúc (prospective targeting / pre-call lead scoring) để chọn khách hàng tiềm năng trước khi gọi, việc đưa biến `duration` vào sẽ gây ra lỗi rò rỉ mục tiêu nghiêm trọng (target leakage), vì thời lượng cuộc gọi chưa hề tồn tại ở thời điểm ra quyết định gọi điện.
2. **Ký hiệu đặc biệt và giá trị thiếu (Sentinel values)**:
   - Biến `pdays` ghi nhận giá trị `-1` ở các dòng 1, 4, 5, 8, 9, tương ứng với trường hợp khách hàng chưa từng được liên hệ trong chiến dịch trước đó (`previous = 0` và `poutcome = unknown`). Giá trị `-1` ở đây là một giá trị lính canh (sentinel value) có ngữ nghĩa kỹ thuật quy ước trong `bank-names.txt`, không phải là số ngày âm thực tế.

---

## 4. Non-causal interpretation limits

Tuân thủ nghiêm ngặt chuẩn mực phân tích của kỹ năng `nckh-analytics` và chính sách bằng chứng (`evidence-policy.md`):

1. **Không suy diễn tỷ lệ phản hồi tổng thể (No population response rate claim)**:
   - Dữ liệu 10 dòng đầu này chỉ là một lát cắt lấy mẫu phục vụ kiểm định kỹ thuật (smoke/sanity test). Tỷ lệ 0 khách hàng chọn `y=yes` không cho phép suy diễn rằng chiến dịch tiếp thị của ngân hàng hoàn toàn thất bại hoặc không có ai đăng ký.
2. **Không khẳng định tác động nhân quả (No causal lift or attribution)**:
   - Các biến số như số dư (`balance`), loại hình công việc (`job`), tình trạng nhà ở (`housing`) hay thời điểm liên hệ (`month`) trong mẫu quan sát không phản ánh quan hệ nhân quả đối với quyết định từ chối (`y=no`) của khách hàng. Mọi tương quan thống kê đơn thuần không cấu thành bằng chứng đòn bẩy nhân quả (causal lift).
3. **Không phải mô hình dự báo (Not a forecast)**:
   - Bản báo cáo này là phân tích mô tả dữ liệu tĩnh (descriptive observation), không đưa ra bất kỳ dự báo hay ước lượng xác suất tương lai nào cho các chiến dịch tiếp thị tiếp theo.
