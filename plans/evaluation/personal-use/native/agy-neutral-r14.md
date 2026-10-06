# Báo cáo Đánh giá Tích hợp Bản địa (Native Integration Probe) - R14

## 1. Thông tin Bối cảnh & Đường dẫn Đọc Thực tế (Actual Read Paths)

- **Phạm vi dự án**: `C:/Users/USER/Downloads/test-skill`
- **Kỹ năng dự án được phát hiện độc lập**: `nckh-analytics`
- **Đường dẫn `SKILL.md` đã đọc thực tế**:
  `C:/Users/USER/Downloads/test-skill/.agents/skills/nckh-analytics/SKILL.md`
- **Các hợp đồng cục bộ bắt buộc (Required Local Contracts) đã đọc thực tế**:
  1. `C:/Users/USER/Downloads/test-skill/.agents/skills/nckh-analytics/references/_shared/core/policies/authorization-policy.md`
  2. `C:/Users/USER/Downloads/test-skill/.agents/skills/nckh-analytics/references/_shared/core/policies/evidence-policy.md`
  3. `C:/Users/USER/Downloads/test-skill/.agents/skills/nckh-analytics/references/_shared/core/policies/preservation-policy.md`
  4. `C:/Users/USER/Downloads/test-skill/.agents/skills/nckh-analytics/references/_shared/core/policies/acceptance-policy.md`
  5. `C:/Users/USER/Downloads/test-skill/.agents/skills/nckh-analytics/references/_shared/core/workflows/model-and-context.md`
- **Đường dẫn snapshot dữ liệu thực tế đã đọc**:
  `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/source-acquisition/derived/worldbank-series.jsonl`
- **Tính chất bằng chứng**: Bằng chứng phát triển sử dụng cá nhân (personal-use development evidence); đánh giá của chủ sở hữu diễn ra sau khi bàn giao, không yêu cầu người đánh giá ngoài (external reviewer) hay điều kiện tiên quyết về tập giữ lại (holdout prerequisite).
- **Mô hình & Môi trường**: Giữ nguyên Gemini 3.8 Flash (High); không thay đổi mô hình hoặc môi trường.

---

## 2. Nguồn gốc & Xuất xứ Dữ liệu (Provenance)

- **Mã nguồn (Source ID)**: `worldbank-vnm-SP.POP.TOTL-2000-2025`
- **Bộ định vị API (Locator)**: `https://api.worldbank.org/v2/country/VNM/indicator/SP.POP.TOTL?date=2000%3A2025&format=json&per_page=100`
- **Miền & Thể loại (Domain & Genre)**: `chart-measurement` / `indicator-time-series`
- **Người dùng tiêu thụ (Consumers)**: `["nckh-visuals", "nckh-analytics", "nckh-method"]`
- **Ngôn ngữ**: `und`
- **Giấy phép (License)**: CC BY 4.0 mặc định cùng các điều khoản của Ngân hàng Thế giới (World Bank terms: `https://data.worldbank.org/summary-terms-of-use`; lưu ý: các chỉ số của bên thứ ba có thể có các hạn chế bổ sung)
- **Truy xuất (Retrieval)**:
  - Ngày truy xuất (`retrieved_at`): `2026-10-03`
  - Truy vấn phiên bản (`query`): `date=2000:2025`
  - Cập nhật phản hồi lần cuối (`response_lastupdated`): `2026-07-13`
  - Tệp thô gốc (`raw.raw_file`): `raw/worldbank-vnm-population-2000-2025.json`
  - Mã băm SHA-256 (`raw.sha256`): `a63e499e9f24ae600bb52ecac8acb07bbb959a812e830cc7cf870fbca2fe5781`
  - Dung lượng byte (`raw.bytes`): `5217`
- **Chuẩn hóa (Normalization)**: Phép chiếu JSON giữ nguyên trường (`field-preserving JSON projection; no value transformation`).
- **Cơ sở quyền (Rights Rationale)**: Phản hồi API được lưu giữ cùng truy vấn chính thức và bộ định vị điều khoản của World Bank; bản ghi là một bản chụp (snapshot) có mốc ngày, không phải là tuyên bố về các giá trị thời gian thực.
- **Lưu ý về trường đơn vị (Unit Field)**: Trường `unit` trong toàn bộ bản ghi dữ liệu trả về từ API là chuỗi rỗng (`unit: ""`). Tuyệt đối không tự ý suy đoán, thêm thắt hoặc phát minh đơn vị cung cấp ngoài dữ liệu gốc.

---

## 3. Các Chỉ số Thống kê Mô tả (Descriptive Statistics)

- **Số lượng quan sát (Observation Count)**: `26` quan sát (từ năm 2000 đến năm 2025).
- **Số lượng giá trị hợp lệ / không null (Non-null Count)**: `26` (tất cả 26 quan sát đều có giá trị nguyên xác định, 0 giá trị null, 0 giá trị bị thiếu).
- **Các năm được ghi nhận (Years)**: 2000 đến 2025 (26 năm liên tục hàng năm: `2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025`).
- **Giá trị đầu và cuối (First and Last Values)**:
  - *Theo thứ tự thời gian (Chronological)*:
    - Giá trị năm đầu (2000): `77154011` (77.154.011)
    - Giá trị năm cuối (2025): `101598527` (101.598.527)
  - *Theo thứ tự trong tệp snapshot JSONL (Descending order)*:
    - Bản ghi đầu tiên (`data[0]`, năm 2025): `101598527` (101.598.527)
    - Bản ghi cuối cùng (`data[25]`, năm 2000): `77154011` (77.154.011)

---

## 4. Phép tính Số học Tái lập (Reproducible Arithmetic)

### 4.1. Thay đổi tuyệt đối (Absolute Change) từ năm 2000 đến năm 2025

$$\Delta = \text{Giá trị}_{2025} - \text{Giá trị}_{2000}$$

$$\Delta = 101.598.527 - 77.154.011 = +24.444.516$$

- **Kết quả thay đổi tuyệt đối**: Tăng `24.444.516`

### 4.2. Thay đổi phần trăm (Percentage Change) từ năm 2000 đến năm 2025

$$\% \Delta = \frac{\Delta}{\text{Giá trị}_{2000}} \times 100\% = \frac{24.444.516}{77.154.011} \times 100\%$$

$$\% \Delta = 31{,}682754639936995\% \approx +31{,}682755\%$$

- **Kết quả thay đổi phần trăm**: Tăng xấp xỉ `+31,682755%` (giá trị chính xác đầy đủ: `31,682754639936995%`)

---

## 5. Giới hạn Chất lượng Dữ liệu & Ranh giới Suy luận (Quality Limits & Boundaries)

1. **Trường đơn vị để trống (Blank Unit Field)**:
   - Toàn bộ 26 bản ghi trong snapshot đều có `unit: ""`. Tuân thủ chính sách bảo toàn (`preservation-policy.md`), không tự gán hoặc phỏng đoán đơn vị đo lường (như "người", "dân số", v.v.) vì API không cung cấp.
2. **Không khẳng định nhân quả (No Causal Claim)**:
   - Dữ liệu ở đây phản ánh xu hướng thời gian mô tả đơn thuần. Tuân thủ ranh giới kỹ năng `nckh-analytics` và chính sách bằng chứng (`evidence-policy.md`), tương quan hoặc sự tăng trưởng qua thời gian không chứng minh mối quan hệ nhân quả. Không được đưa ra bất kỳ kết luận hay giả định nhân quả nào về nguyên nhân dẫn đến sự biến đổi số liệu từ 2000 đến 2025.
3. **Khả năng điều chỉnh của nhà cung cấp (Provider Revisions)**:
   - Dữ liệu lịch sử có thể được nhà cung cấp (Ngân hàng Thế giới / World Bank) điều chỉnh hồi tố trong các bản phát hành sau (`Historical values may be revised by the provider`).
4. **Giới hạn định dạng và thời điểm snapshot**:
   - Dữ liệu là bản chiếu JSON lưu trữ phản hồi truy vấn tại thời điểm truy xuất (`retrieved_at: 2026-10-03`, `response_lastupdated: 2026-07-13`), không phải là một tạo tác bảng CSV độc lập và không thể thay thế cho dữ liệu trực tiếp thời gian thực.
