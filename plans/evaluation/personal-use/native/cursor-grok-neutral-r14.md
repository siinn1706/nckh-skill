# Phân tích mô tả SP.POP.TOTL, VNM, 2000–2025

Phiên cùng agent. Không ủy quyền model khác, không fallback. Skill và nguồn đều đọc được.

## Đường dẫn đã đọc

- Skill: `C:/Users/USER\Downloads\test-skill\.agents\skills\nckh-analytics\SKILL.md`
- Hợp đồng bắt buộc:
  - `C:/Users/USER\Downloads\test-skill\.agents\skills\nckh-analytics\references\_shared\core\policies\authorization-policy.md`
  - `C:/Users/USER\Downloads\test-skill\.agents\skills\nckh-analytics\references\_shared\core\policies\evidence-policy.md`
  - `C:/Users/USER\Downloads\test-skill\.agents\skills\nckh-analytics\references\_shared\core\policies\preservation-policy.md`
  - `C:/Users/USER\Downloads\test-skill\.agents\skills\nckh-analytics\references\_shared\core\policies\acceptance-policy.md`
- Chính sách model trước khi không ủy quyền: `C:/Users/USER\Downloads\test-skill\.agents\skills\nckh-analytics\references\_shared\core\workflows\model-and-context.md`
- Schema tham chiếu đã đọc: `references\_shared\core\contracts\brief.schema.json`, `references\_shared\core\contracts\claim.schema.json` (cùng thư mục skill)
- Nguồn tính: `C:/Users/USER\Downloads\test-skill\plans\evaluation\personal-use\source-acquisition\derived\worldbank-series.jsonl`
- Provenance đi kèm: `C:/Users/USER\Downloads\test-skill\plans\evaluation\personal-use\source-acquisition\derived\manifest.json`
- Raw API để đối chiếu trường `unit`: `C:/Users/USER\Downloads\test-skill\plans\evaluation\personal-use\source-acquisition\raw\worldbank-vnm-population-2000-2025.json`

## Định nghĩa trước khi tính

- Sự kiện: một quan sát năm của chỉ số `SP.POP.TOTL`, quốc gia `VNM`.
- Tập: 26 phần tử trong mảng `data` của đúng một dòng JSONL `source_id=worldbank-vnm-SP.POP.TOTL-2000-2025`.
- Tử số đếm non-null: số phần tử có `value` khác null. Null không được đổi thành 0.
- Mẫu số độ đầy đủ: số quan sát trong mảng.
- Mẫu số phần trăm 2000→2025: `value` năm 2000.
- Phép gộp: không gộp thêm. Mỗi năm một quan sát.
- Cửa sổ: `date` từ 2000 đến 2025. Nguồn không có múi giờ.
- Loại trừ: không loại quan sát nào.
- Đơn vị: trường `unit` là chuỗi rỗng ở cả file dẫn xuất và raw API. Không gán đơn vị được cung cấp. Nhãn chỉ số `Population, total` không phải trường `unit`.

## Kết quả quan sát

| Hạng mục | Giá trị |
|---|---|
| Số quan sát | 26 |
| Số non-null | 26 |
| Số null | 0 |
| Năm, thứ tự lưu trong `data` | 2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000 |
| Quan sát đầu theo thứ tự file | 2025 = 101598527 |
| Quan sát cuối theo thứ tự file | 2000 = 77154011 |
| Mốc thời gian đầu | 2000 = 77154011 |
| Mốc thời gian cuối | 2025 = 101598527 |
| Chênh lệch tuyệt đối 2000→2025 | 24444516 |
| Phần trăm 2000→2025 | 31.682754639936995628133967007885046961459981646320% |

Năm liên tục 2000–2025, không thiếu năm, không trùng năm. Cả 26 `value` là số nguyên. `decimal` lưu là 0. `observation_status` / `obs_status` là chuỗi rỗng.

Đây là chênh lệch số học giữa hai mốc trong snapshot. Không phải hiệu ứng nhân quả, attribution hay tăng trưởng được giải thích bởi một nguyên nhân.

## Phép tính tái lập

Đối chiếu hash, khớp `manifest.json`:

- `derived/worldbank-series.jsonl`: 6004 byte, SHA-256 `a29802fa36bc453ce9abbf9789e119bae689462ffd6348e327ee7d7f5e9cb4b2`
- `raw/worldbank-vnm-population-2000-2025.json`: 5217 byte, SHA-256 `a63e499e9f24ae600bb52ecac8acb07bbb959a812e830cc7cf870fbca2fe5781`

```text
101598527 - 77154011 = 24444516
24444516 / 77154011 * 100 = 31.682754639936995628133967007885046961459981646320
```

Python `decimal.Decimal`, precision 50, không làm tròn giá trị nguồn:

```python
from decimal import Decimal, getcontext
getcontext().prec = 50
v2000 = Decimal(77154011)
v2025 = Decimal(101598527)
delta = v2025 - v2000
pct = (delta / v2000) * Decimal(100)
```

Raw API: `total=26`, `lastupdated=2026-07-13`, 26/26 trường `unit` là `""`, 26/26 `obs_status` là `""`. Giá trị 2000 và 2025 trong raw trùng file dẫn xuất.

## Giới hạn chất lượng

- `unit` trống nên mọi câu có đơn vị được cung cấp đều ngoài bằng chứng.
- `observation_status` trống nên không phân loại ước tính, chính thức hay sửa đổi từ trường này.
- Bản ghi là snapshot: `retrieved_at=2026-10-03`, `response_lastupdated=2026-07-13`, query `date=2000:2025`. Không phải giá trị sống sau ngày truy xuất.
- Giới hạn nguồn: giá trị lịch sử có thể bị nhà cung cấp hiệu đính; JSON không phải artifact CSV.
- Chuẩn hóa ghi trong file: `field-preserving JSON projection; no value transformation`.
- Một quốc gia, một chỉ số, một cửa sổ. Không có nhật ký đổi cách đo trong file.
- Giấy phép giữ nguyên: `CC BY 4.0 default with World Bank terms`, locator `https://data.worldbank.org/summary-terms-of-use`, caveat chỉ số bên thứ ba có thể có hạn chế thêm.
- `rights_rationale` giữ nguyên: phản hồi API được giữ với query chính thức và locator điều khoản World Bank; bản ghi là snapshot có ngày, không phải khẳng định giá trị hiện hành.
- Manifest `no_claims`: human gold, scientific validity, model uplift, public release clearance.
- Không có external reviewer và không có holdout prerequisite. Chủ sở hữu rà sau khi giao. Cổng người duyệt đang pending; báo cáo này chưa được accepted-for-scope.

## Mô hình

- Yêu cầu: Grok 4.7 Extra High.
- Đã áp dụng: cùng agent đang chạy. Không chọn, không thử, không fallback sang model khác.
- Định danh phiên đọc được: Grok 4.7.
- Không có native run receipt cho effort. Effort hiệu lực = unknown.
