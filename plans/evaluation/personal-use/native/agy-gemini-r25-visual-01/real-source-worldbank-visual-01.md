# real-source-worldbank-visual-01

## 1. Source and data receipt

- **Kỹ năng (Skill)**: `nckh-visuals`, phiên bản `0.1.0`, trạng thái `experimental`.
- **Môi trường & Mô hình (Host & Model)**: `agy` (Antigravity), mô hình duy nhất được sử dụng là **Gemini 3.8 Flash (High)** trong môi trường dự án hiện hữu; không fallback.
- **Đợt đánh giá (Candidate run)**: `r25` (Candidate r25 WorldBank visual case sau khi controller xác nhận r25 đã được cài đặt; kết quả r24 unavailable trước đó vẫn là lịch sử tham chiếu).
- **Mã ca (case_id)**: `real-source-worldbank-visual-01`.
- **Làn đánh giá (lane)**: World Bank measurement and editable visual.
- **Tài nguyên (Resource)**: `R-worldbank-vietnam-population`.
- **Mã bản ghi & Mã nguồn (record_id & source_id)**: `worldbank-vnm-SP.POP.TOTL-2000-2025`.
- **Quốc gia nguồn**: `Viet Nam` (mã ISO3: `VNM`).
- **Chỉ báo (Indicator)**: `Population, total` (mã chỉ báo: `SP.POP.TOTL`).
- **Bộ định vị API (API locator)**: `https://api.worldbank.org/v2/country/VNM/indicator/SP.POP.TOTL?date=2000%3A2025&format=json&per_page=100`
- **Ngày cập nhật phản hồi (response_lastupdated)**: `2026-07-13`; ngày thu thập ghi trong resource: `2026-10-03`.
- **Kết quả đọc từ reader**: Bộ đọc tài nguyên trả `status: matched`, `resource_read: true`: đủ **26 quan sát gốc, 26 giá trị khác null** (`observation_count: 26`, `non_null_value_count: 26`), liên tục cho từng năm từ 2000 đến 2025.
- **Trường đơn vị API để trống (Raw blank unit field)**: Trường `unit` trong dữ liệu gốc là chuỗi rỗng (`unit: ""`) trên cả 26 quan sát. Tuyệt đối không suy diễn, bổ sung đơn vị (như "người" hay bất kỳ đơn vị nào khác).
- **Nguyên tắc bảo toàn**: Chỉ sắp xếp năm tăng dần để phục vụ hiển thị biểu đồ; giữ nguyên mọi giá trị quan sát gốc. Không dùng dữ liệu giả lập, không thực hiện phép nội suy.
- **Đường dẫn thư mục kết quả mới**: `plans/evaluation/personal-use/native/agy-gemini-r25-visual-01/`.

### Lệnh bộ đọc tài nguyên cài đặt thực tế

```powershell
python -I .agents/skills/nckh-visuals/references/_shared/scripts/search-resource.py --resource-id R-worldbank-vietnam-population --consumer nckh-visuals --domain chart-measurement --locale und --genre indicator-time-series --query worldbank-vnm-SP.POP.TOTL-2000-2025 --json
```

Biên nhận reader thực tế được lưu tại: `plans/evaluation/personal-use/native/agy-gemini-r25-visual-01/reader-receipt.json`.

### Bảng mã băm nguồn và bộ đọc

| Đối tượng | SHA-256 |
|---|---|
| Reader cài đặt (`search-resource.py`) theo biên nhận reader | `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb` |
| Record được chọn theo biên nhận reader | `65b7007d7ea17cae6091e2925ec725bf88433573635536386868bfa4c1304800` |
| Resource pack (`worldbank-series.jsonl`) theo biên nhận reader | `a29802fa36bc453ce9abbf9789e119bae689462ffd6348e327ee7d7f5e9cb4b2` |
| Acquisition `raw/worldbank-vnm-population-2000-2025.json` (đọc trực tiếp) | `a63e499e9f24ae600bb52ecac8acb07bbb959a812e830cc7cf870fbca2fe5781` |
| Acquisition `derived/reader-ready.jsonl` (đọc trực tiếp) | `16175d1edc8116d07d9e952584f3ef47b3227cf8bd7d599cc30c695bff4f893e` |
| Acquisition `derived/worldbank-series.jsonl` (đọc trực tiếp) | `a29802fa36bc453ce9abbf9789e119bae689462ffd6348e327ee7d7f5e9cb4b2` |

Các mã băm đọc trực tiếp khớp chính xác với mã ghim của ca đánh giá. Thao tác đối chiếu này chỉ kiểm tra tính toàn vẹn, không thay thế bộ đọc tài nguyên được chỉ định.

### Giá trị đầu/cuối và thay đổi số học

- **Giá trị năm 2000 (first_value_2000)**: `77,154,011`
- **Giá trị năm 2025 (last_value_2025)**: `101,598,527`
- **Thay đổi tuyệt đối (Absolute change)**: `24,444,516`
- **Thay đổi phần trăm (Percentage change)**: `31.682754639936995%`

**Phương pháp và độ chính xác tính toán**:
- Công thức: `(101598527 - 77154011) / 77154011 * 100`, sử dụng giá trị năm 2000 làm mẫu số.
- Phép tính được thực hiện bằng số thực chuẩn IEEE 754 binary64. Chuỗi phần trăm `31.682754639936995%` là một biểu diễn hữu hạn được tính toán (computed finite representation) với 15 chữ số sau dấu phẩy thập phân, không phải là một thương số vô hạn chính xác tuyệt đối. Toàn bộ các giá trị quan sát gốc là số nguyên được bảo toàn, không bị làm tròn.

---

## 2. Editable visual

Tệp đồ họa vector có thể chỉnh sửa được lưu tại:
`plans/evaluation/personal-use/native/agy-gemini-r25-visual-01/real-source-worldbank-visual-01.svg`

Cấu trúc vector chứa:
- Thẻ văn bản bản địa `<text>` với họ phông chữ Arial duy nhất được cài đặt (`font-family="Arial"`).
- Đủ 26 dấu điểm tròn `<circle>` mang các thuộc tính `data-year` và `data-value` phản ánh chính xác 100% dữ liệu quan sát thô.
- Đường đa tuyến `<polyline>` nối chính xác các tọa độ điểm theo năm tăng dần, không có điểm dữ liệu nội suy hay bổ sung.
- Bảng siêu dữ liệu `<metadata id="source-metadata">` chứa đầy đủ source_id, resource_id, API locator, ngày cập nhật, mã băm nguồn thô, công thức tỉ lệ tọa độ và điều khoản bản quyền.

### Toàn văn mã nguồn SVG bản địa

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1100" viewBox="0 0 1400 1100" xml:lang="vi" role="img" aria-labelledby="chart-title chart-desc">
  <title id="chart-title">Dân số Việt Nam: chuỗi giá trị World Bank, 2000–2025</title>
  <desc id="chart-desc">Biểu đồ gồm 26 quan sát hằng năm của chỉ báo Population, total, mã SP.POP.TOTL, cho Viet Nam. Giá trị tăng qua từng năm từ 77,154,011 năm 2000 lên 101,598,527 năm 2025. Trục tung tuyến tính bắt đầu tại 75,000,000 và kết thúc tại 105,000,000, không bắt đầu tại 0. Trường unit của API là chuỗi rỗng; không bổ sung đơn vị. Đường nối chỉ nối các quan sát để đọc xu hướng, không biểu thị phép nội suy hay nguyên nhân. Dữ liệu là snapshot có response lastupdated 2026-07-13. Render, khả năng chỉnh sửa và chấp nhận trực quan cuối cùng đang chờ kiểm tra.</desc>
  <metadata id="source-metadata">
    source_id: worldbank-vnm-SP.POP.TOTL-2000-2025
    resource_id: R-worldbank-vietnam-population
    record_id: worldbank-vnm-SP.POP.TOTL-2000-2025
    indicator: Population, total
    indicator_id: SP.POP.TOTL
    country: Viet Nam
    country_iso3: VNM
    observation_count: 26
    non_null_value_count: 26
    raw_unit_value: ""
    response_lastupdated: 2026-07-13
    retrieved_at: 2026-10-03
    API locator: https://api.worldbank.org/v2/country/VNM/indicator/SP.POP.TOTL?date=2000%3A2025&amp;format=json&amp;per_page=100
    raw_sha256: a63e499e9f24ae600bb52ecac8acb07bbb959a812e830cc7cf870fbca2fe5781
    resource_sha256: a29802fa36bc453ce9abbf9789e119bae689462ffd6348e327ee7d7f5e9cb4b2
    record_sha256: 65b7007d7ea17cae6091e2925ec725bf88433573635536386868bfa4c1304800
    x = 200 + 40 * (year - 2000)
    y = 700 - (value - 75000000) * 510 / 30000000
    coordinate_precision: 6 decimal places
    license: CC BY 4.0 default with World Bank terms
    terms_locator: https://data.worldbank.org/summary-terms-of-use
    rights_caveat: Third-party indicators may have additional restrictions.
    final_render_status: pending
    native_editability_status: pending
    owner_review_status: pending-personal-review
  </metadata>

  <rect id="background" width="1400" height="1100" fill="#ffffff"/>

  <g id="heading" font-family="Arial" fill="#152638">
    <text id="visible-title" x="200" y="58" font-size="32" font-weight="bold">Dân số Việt Nam, 2000–2025</text>
    <text id="subtitle" x="200" y="94" font-size="19">26 quan sát World Bank · snapshot cập nhật 2026-07-13</text>
    <text id="unit-caveat" x="200" y="126" font-size="18">Trường unit của API: "" (trống); không bổ sung đơn vị.</text>
    <text id="y-axis-label" x="200" y="162" font-size="18">Population, total (SP.POP.TOTL; raw unit field blank)</text>
  </g>

  <g id="grid" stroke="#d5dde5" stroke-width="1" fill="none" aria-hidden="true">
    <path d="M200 700H1200 M200 615H1200 M200 530H1200 M200 445H1200 M200 360H1200 M200 275H1200 M200 190H1200"/>
  </g>

  <g id="axes" font-family="Arial" font-size="17" fill="#26394c">
    <path id="axis-lines" d="M200 190V700H1200" fill="none" stroke="#526476" stroke-width="2"/>
    <g id="y-ticks" text-anchor="end">
      <text x="184" y="706" data-value="75000000">75,000,000</text>
      <text x="184" y="621" data-value="80000000">80,000,000</text>
      <text x="184" y="536" data-value="85000000">85,000,000</text>
      <text x="184" y="451" data-value="90000000">90,000,000</text>
      <text x="184" y="366" data-value="95000000">95,000,000</text>
      <text x="184" y="281" data-value="100000000">100,000,000</text>
      <text x="184" y="196" data-value="105000000">105,000,000</text>
    </g>
    <g id="x-ticks" text-anchor="middle">
      <path d="M200 700V708 M400 700V708 M600 700V708 M800 700V708 M1000 700V708 M1200 700V708" stroke="#526476" fill="none"/>
      <text x="200" y="735" data-year="2000">2000</text>
      <text x="400" y="735" data-year="2005">2005</text>
      <text x="600" y="735" data-year="2010">2010</text>
      <text x="800" y="735" data-year="2015">2015</text>
      <text x="1000" y="735" data-year="2020">2020</text>
      <text x="1200" y="735" data-year="2025">2025</text>
      <text id="x-axis-label" x="700" y="774" font-size="19">Năm</text>
    </g>
  </g>

  <g id="observed-series" data-source-id="worldbank-vnm-SP.POP.TOTL-2000-2025">
    <polyline id="observation-connection" fill="none" stroke="#006b82" stroke-width="3"
      stroke-linejoin="round" stroke-linecap="round"
      points="200,663.381813 240,649.520863 280,635.872192 320,622.415791 360,609.237493 400,596.498679 440,578.145751 480,553.232625 520,527.011604 560,505.179694 600,488.262416 640,471.038662 680,453.323948 720,435.257232 760,416.447174 800,397.004682 840,376.998011 880,356.991391 920,338.965577 960,323.045808 1000,307.653753 1040,293.103334 1080,280.428865 1120,269.012736 1160,258.209338 1200,247.825041"/>
    <g id="observation-marks" fill="#006b82" stroke="#ffffff" stroke-width="1.5">
      <circle id="point-2000" data-year="2000" data-value="77154011" cx="200" cy="663.381813" r="5"><title>2000: 77,154,011</title></circle>
      <circle id="point-2001" data-year="2001" data-value="77969361" cx="240" cy="649.520863" r="5"><title>2001: 77,969,361</title></circle>
      <circle id="point-2002" data-year="2002" data-value="78772224" cx="280" cy="635.872192" r="5"><title>2002: 78,772,224</title></circle>
      <circle id="point-2003" data-year="2003" data-value="79563777" cx="320" cy="622.415791" r="5"><title>2003: 79,563,777</title></circle>
      <circle id="point-2004" data-year="2004" data-value="80338971" cx="360" cy="609.237493" r="5"><title>2004: 80,338,971</title></circle>
      <circle id="point-2005" data-year="2005" data-value="81088313" cx="400" cy="596.498679" r="5"><title>2005: 81,088,313</title></circle>
      <circle id="point-2006" data-year="2006" data-value="82167897" cx="440" cy="578.145751" r="5"><title>2006: 82,167,897</title></circle>
      <circle id="point-2007" data-year="2007" data-value="83633375" cx="480" cy="553.232625" r="5"><title>2007: 83,633,375</title></circle>
      <circle id="point-2008" data-year="2008" data-value="85175788" cx="520" cy="527.011604" r="5"><title>2008: 85,175,788</title></circle>
      <circle id="point-2009" data-year="2009" data-value="86460018" cx="560" cy="505.179694" r="5"><title>2009: 86,460,018</title></circle>
      <circle id="point-2010" data-year="2010" data-value="87455152" cx="600" cy="488.262416" r="5"><title>2010: 87,455,152</title></circle>
      <circle id="point-2011" data-year="2011" data-value="88468314" cx="640" cy="471.038662" r="5"><title>2011: 88,468,314</title></circle>
      <circle id="point-2012" data-year="2012" data-value="89510356" cx="680" cy="453.323948" r="5"><title>2012: 89,510,356</title></circle>
      <circle id="point-2013" data-year="2013" data-value="90573104" cx="720" cy="435.257232" r="5"><title>2013: 90,573,104</title></circle>
      <circle id="point-2014" data-year="2014" data-value="91679578" cx="760" cy="416.447174" r="5"><title>2014: 91,679,578</title></circle>
      <circle id="point-2015" data-year="2015" data-value="92823254" cx="800" cy="397.004682" r="5"><title>2015: 92,823,254</title></circle>
      <circle id="point-2016" data-year="2016" data-value="94000117" cx="840" cy="376.998011" r="5"><title>2016: 94,000,117</title></circle>
      <circle id="point-2017" data-year="2017" data-value="95176977" cx="880" cy="356.991391" r="5"><title>2017: 95,176,977</title></circle>
      <circle id="point-2018" data-year="2018" data-value="96237319" cx="920" cy="338.965577" r="5"><title>2018: 96,237,319</title></circle>
      <circle id="point-2019" data-year="2019" data-value="97173776" cx="960" cy="323.045808" r="5"><title>2019: 97,173,776</title></circle>
      <circle id="point-2020" data-year="2020" data-value="98079191" cx="1000" cy="307.653753" r="5"><title>2020: 98,079,191</title></circle>
      <circle id="point-2021" data-year="2021" data-value="98935098" cx="1040" cy="293.103334" r="5"><title>2021: 98,935,098</title></circle>
      <circle id="point-2022" data-year="2022" data-value="99680655" cx="1080" cy="280.428865" r="5"><title>2022: 99,680,655</title></circle>
      <circle id="point-2023" data-year="2023" data-value="100352192" cx="1120" cy="269.012736" r="5"><title>2023: 100,352,192</title></circle>
      <circle id="point-2024" data-year="2024" data-value="100987686" cx="1160" cy="258.209338" r="5"><title>2024: 100,987,686</title></circle>
      <circle id="point-2025" data-year="2025" data-value="101598527" cx="1200" cy="247.825041" r="5"><title>2025: 101,598,527</title></circle>
    </g>
  </g>

  <g id="endpoint-labels" font-family="Arial" font-size="18" font-weight="bold" fill="#152638">
    <text id="label-2000" x="214" y="685">2000: 77,154,011</text>
    <text id="label-2025" x="1188" y="228" text-anchor="end">2025: 101,598,527</text>
  </g>

  <g id="caption" font-family="Arial" font-size="16" fill="#26394c">
    <text x="200" y="820">Trục tung: 75,000,000–105,000,000; không bắt đầu tại 0. Đường nối các quan sát, không nội suy.</text>
    <text x="200" y="848">Nguồn: World Bank · source_id: worldbank-vnm-SP.POP.TOTL-2000-2025</text>
    <text x="200" y="876">API: https://api.worldbank.org/v2/country/VNM/indicator/SP.POP.TOTL</text>
    <text x="200" y="901">?date=2000%3A2025&amp;format=json&amp;per_page=100 · response lastupdated: 2026-07-13</text>
    <text x="200" y="931">Raw SHA-256:</text>
    <text x="200" y="956" font-size="14">a63e499e9f24ae600bb52ecac8acb07bbb959a812e830cc7cf870fbca2fe5781</text>
    <text x="200" y="986">Điều khoản: https://data.worldbank.org/summary-terms-of-use · CC BY 4.0 mặc định.</text>
    <text x="200" y="1013">Chỉ báo bên thứ ba có thể có hạn chế bổ sung; snapshot có thể được nhà cung cấp sửa đổi.</text>
    <text id="qa-status" x="200" y="1045">QA cuối: chờ render, mở/chỉnh sửa/lưu/mở lại, kiểm tra trực quan và phản hồi chủ sở hữu.</text>
  </g>
</svg>
```

---

## 3. Axes/units/caption/alt text

### Miền trục và ánh xạ tọa độ

- **Kích thước ảnh SVG**: Rộng `1400 px`, Cao `1100 px` (đáp ứng yêu cầu tối thiểu chiều rộng 1200 và chiều cao 900 nhằm bảo đảm không gian hiển thị rõ ràng, dễ đọc cho phụ đề tiếng Việt và trợ năng).
- **Phông chữ bản địa**: Khai báo và sử dụng một họ phông chữ duy nhất được cài đặt là `Arial` (`font-family="Arial"`).
- **Vùng vẽ biểu đồ (Plot area)**: `x ∈ [200, 1200]`, `y ∈ [190, 700]`.
- **Trục hoành tuyến tính (x-axis)**:
  - Miền giá trị năm: `[2000, 2025]` (25 khoảng năm, độ rộng trục 1000 px, tương ứng chính xác 40 px mỗi năm).
  - Công thức tính: `x = 200 + 40 * (year - 2000)`.
  - Các vạch chia trục x (x-ticks): `2000`, `2005`, `2010`, `2015`, `2020`, `2025`.
- **Trục tung tuyến tính (y-axis)**:
  - Miền giá trị quan sát: `[75000000, 105000000]` (khoảng giá trị 30,000,000, chiều cao trục 510 px).
  - Công thức tính: `y = 700 - (value - 75000000) * 510 / 30000000`.
  - Lưu ý trục y: Trục tung không bắt đầu tại 0 (điểm gốc trục là 75,000,000); lưu ý này được ghi nhận rõ ràng trên biểu đồ và alt text.
  - Nhãn trục Y bắt buộc: **`Population, total (SP.POP.TOTL; raw unit field blank)`** - hoàn toàn không tự chế hay gắn thêm đơn vị.
  - Các vạch chia trục y (y-ticks) và tọa độ tương ứng:
    - `75,000,000`: tọa độ `y = 700`
    - `80,000,000`: tọa độ `y = 621`
    - `85,000,000`: tọa độ `y = 536`
    - `90,000,000`: tọa độ `y = 451`
    - `95,000,000`: tọa độ `y = 366`
    - `100,000,000`: tọa độ `y = 281`
    - `105,000,000`: tọa độ `y = 190`
- **Độ chính xác tọa độ**: Tọa độ hiển thị `cx`, `cy` và `points` được biểu diễn với độ chính xác 6 chữ số thập phân; các thuộc tính `data-year` và `data-value` lưu giữ chính xác số nguyên thô từ dữ liệu nguồn.

### Bảng ánh xạ nguồn sang dấu đồ thị (Source-to-mark map) — Đủ 26 quan sát

| Năm (`data-year`) | Giá trị nguồn (`data-value`) | Hoành độ x (`cx`) | Tung độ y (`cy`) | ID phần tử |
|---|---:|---:|---:|---|
| 2000 | 77154011 | 200.0 | 663.381813 | `point-2000` |
| 2001 | 77969361 | 240.0 | 649.520863 | `point-2001` |
| 2002 | 78772224 | 280.0 | 635.872192 | `point-2002` |
| 2003 | 79563777 | 320.0 | 622.415791 | `point-2003` |
| 2004 | 80338971 | 360.0 | 609.237493 | `point-2004` |
| 2005 | 81088313 | 400.0 | 596.498679 | `point-2005` |
| 2006 | 82167897 | 440.0 | 578.145751 | `point-2006` |
| 2007 | 83633375 | 480.0 | 553.232625 | `point-2007` |
| 2008 | 85175788 | 520.0 | 527.011604 | `point-2008` |
| 2009 | 86460018 | 560.0 | 505.179694 | `point-2009` |
| 2010 | 87455152 | 600.0 | 488.262416 | `point-2010` |
| 2011 | 88468314 | 640.0 | 471.038662 | `point-2011` |
| 2012 | 89510356 | 680.0 | 453.323948 | `point-2012` |
| 2013 | 90573104 | 720.0 | 435.257232 | `point-2013` |
| 2014 | 91679578 | 760.0 | 416.447174 | `point-2014` |
| 2015 | 92823254 | 800.0 | 397.004682 | `point-2015` |
| 2016 | 94000117 | 840.0 | 376.998011 | `point-2016` |
| 2017 | 95176977 | 880.0 | 356.991391 | `point-2017` |
| 2018 | 96237319 | 920.0 | 338.965577 | `point-2018` |
| 2019 | 97173776 | 960.0 | 323.045808 | `point-2019` |
| 2020 | 98079191 | 1000.0 | 307.653753 | `point-2020` |
| 2021 | 98935098 | 1040.0 | 293.103334 | `point-2021` |
| 2022 | 99680655 | 1080.0 | 280.428865 | `point-2022` |
| 2023 | 100352192 | 1120.0 | 269.012736 | `point-2023` |
| 2024 | 100987686 | 1160.0 | 258.209338 | `point-2024` |
| 2025 | 101598527 | 1200.0 | 247.825041 | `point-2025` |

### Văn bản thay thế tiếng Việt (Alt text) và thứ tự đọc (Reading order)

- **Văn bản thay thế tiếng Việt (`<desc id="chart-desc">`)**:
  > *"Biểu đồ gồm 26 quan sát hằng năm của chỉ báo Population, total, mã SP.POP.TOTL, cho Viet Nam. Giá trị tăng qua từng năm từ 77,154,011 năm 2000 lên 101,598,527 năm 2025. Trục tung tuyến tính bắt đầu tại 75,000,000 và kết thúc tại 105,000,000, không bắt đầu tại 0. Trường unit của API là chuỗi rỗng; không bổ sung đơn vị. Đường nối chỉ nối các quan sát để đọc xu hướng, không biểu thị phép nội suy hay nguyên nhân. Dữ liệu là snapshot có response lastupdated 2026-07-13. Render, khả năng chỉnh sửa và chấp nhận trực quan cuối cùng đang chờ kiểm tra."*
- **Phi nhân quả (No causal claims)**: Nội dung mô tả hoàn toàn tập trung vào dữ liệu quan sát khách quan qua từng năm; không đưa ra bất kỳ kết luận hoặc giả thuyết nhân quả nào về nguyên nhân tăng trưởng dân số.
- **Thứ tự đọc trong DOM SVG**:
  1. `<title>` và `<desc>` liên kết qua `aria-labelledby="chart-title chart-desc"` với thuộc tính `xml:lang="vi"` và `role="img"`.
  2. Khối `<metadata>` chứa nguồn gốc và định nghĩa tham số kỹ thuật.
  3. Khối `<g id="heading">`: Tiêu đề chính, phụ đề, lưu ý trường đơn vị trống và nhãn định danh trục Y.
  4. Khối `<g id="grid">` (có `aria-hidden="true"` để trình đọc màn hình bỏ qua các đường kẻ phụ).
  5. Khối `<g id="axes">`: Đường trục, vạch chia và nhãn trục Y/X.
  6. Khối `<g id="observed-series">`: Đường đa tuyến `<polyline>` và 26 dấu điểm tròn `<circle>` theo đúng thứ tự năm tăng dần từ 2000 đến 2025 (kèm thẻ `<title>` cho từng điểm quan sát).
  7. Khối `<g id="endpoint-labels">`: Nhãn nổi bật hai mốc đầu (2000) và cuối (2025).
  8. Khối `<g id="caption">`: Ghi chú trục, thông tin nguồn World Bank, API locator, response_lastupdated, mã băm SHA-256 tệp thô, điều khoản sử dụng và tình trạng cổng QA.

---

## 4. Hash and QA receipt

### Lệnh kiểm tra ràng buộc công cụ (Binding Checker)

Ràng buộc tác vụ `plans/evaluation/personal-use/visual-engine-probe-02/agy-binding.json` được ủy quyền rõ ràng chỉ dành riêng cho dự án `C:/Users/USER/Downloads/test-skill`, tác vụ `real-source-worldbank-visual-01` và máy chủ `agy`.

Lệnh kiểm tra:
```powershell
python -I .agents/skills/nckh-visuals/references/_shared/scripts/check-visual-engine.py --project C:/Users/USER/Downloads/test-skill --task real-source-worldbank-visual-01 --host agy --binding plans/evaluation/personal-use/visual-engine-probe-02/agy-binding.json --capability svg-render
```

Kết quả kiểm tra từ checker (lưu tại `plans/evaluation/personal-use/native/agy-gemini-r25-visual-01/checker-receipt.json`):
```json
{
  "status": "integrity-verified",
  "scope": {
    "project_root": "C:/Users/USER\\Downloads\\test-skill",
    "task_id": "real-source-worldbank-visual-01",
    "host": "agy"
  },
  "capability": "svg-render",
  "binding_sha256": "721048f870b12bdae43c2cf7c856dc35ccadab44369aedea44b58e18ed9db0df",
  "engine": {
    "executable": "C:\\ProgramData\\chocolatey\\bin\\rsvg-convert.exe",
    "sha256": "79a0ad2d5fb6f8afd0cf93c14d09a1ce73122c6fd54bdd8850965570a83d27c9",
    "version": "rsvg-convert version 2.40.20"
  },
  "global_status": "unavailable",
  "authorization": "not-established-by-checker",
  "acceptance": "pending-independent-gates",
  "limitations": [
    "Receipt integrity and matching do not authenticate execution or grant permission.",
    "Final editability, open/render, source truth, accessibility and scientific meaning remain separate gates."
  ]
}
```

Checker xác nhận trạng thái toàn vẹn của ràng buộc (`integrity-verified`).

### Thực thi công cụ kết xuất đã khai báo (rsvg-convert)

Công cụ `rsvg-convert` được chỉ định chính thức trong ràng buộc đã được thực thi trên tệp SVG nguồn để tạo tệp hình ảnh PNG:

- **Lệnh thực thi đầy đủ (Full command)**:
  `C:\ProgramData\chocolatey\bin\rsvg-convert.exe -o plans/evaluation/personal-use/native/agy-gemini-r25-visual-01/real-source-worldbank-visual-01.png plans/evaluation/personal-use/native/agy-gemini-r25-visual-01/real-source-worldbank-visual-01.svg`
- **Phiên bản công cụ (Engine version)**: `rsvg-convert version 2.40.20`
- **Mã băm tệp thực thi (Engine SHA-256)**: `79a0ad2d5fb6f8afd0cf93c14d09a1ce73122c6fd54bdd8850965570a83d27c9`
- **Mã thoát (Exit status)**: `0`
- **Đầu ra tiêu chuẩn / Lỗi tiêu chuẩn (stdout / stderr)**: Rỗng (không có lỗi)
- **Mã băm tệp SVG đầu vào (Input SVG SHA-256)**:
  `a85e1a4aaa336d20e7d3096362dd019041e7d73e44f887f972fa58773cdafb3e`
- **Mã băm tệp PNG kết xuất đầu ra (Output PNG SHA-256)**:
  `ff6b8f76d4d03c7f5dfe63131c72ef43a5d98c64edd18ebba67aeebda0a73be9`
- **Biên nhận kết xuất chi tiết**: Lưu tại `plans/evaluation/personal-use/native/agy-gemini-r25-visual-01/rsvg-render.json`.

### Ngoại lệ thẩm quyền chỉ dẫn của máy chủ (Host Instruction Authority)

- **Đường dẫn quy tắc**: Đã đọc tệp chỉ dẫn máy chủ bắt buộc tại `C:/Users/USER/.claude/rules/development-rules.md`.
- **Ranh giới ghi nhận**: Thao tác đọc này được ghi nhận riêng biệt theo yêu cầu của máy chủ; không thuộc về các nguồn dữ liệu của ca đánh giá và không mở rộng quyền đọc/ghi ngoài phạm vi dự án.

### Trạng thái các cổng QA cuối (Final QA Gates Status)

| Cổng kiểm thử (Gate) | Trạng thái (Status) | Bằng chứng & Ghi chú |
|---|---|---|
| Nhận diện tài nguyên (Resource identity) | `pass` | Bộ đọc tài nguyên khớp chính xác `R-worldbank-vietnam-population` và `worldbank-vnm-SP.POP.TOTL-2000-2025`. |
| Toàn vẹn nguồn đầu vào (Input integrity) | `pass` | Khớp tuyệt đối mã băm 3 tệp lưu trữ thu thập và mã băm từ bộ đọc tài nguyên. |
| Tính chân thực nguồn (Source truth) | `pass` | Đủ 26 quan sát thực tế; 26 điểm tròn và đa tuyến phản ánh đúng 100% dữ liệu gốc không nội suy. |
| Toàn vẹn ràng buộc công cụ (Binding integrity) | `integrity-verified` | Checker xác nhận tính hợp lệ cho dự án `C:/Users/USER/Downloads/test-skill`, task `real-source-worldbank-visual-01`, host `agy`, capability `svg-render`. |
| Thực thi kết xuất SVG -> PNG | `completed-unreviewed` | `rsvg-convert` thoát mã 0, sinh tệp PNG hợp lệ có chữ ký PNG; mã băm đầu vào và đầu ra được ghi nhận đầy đủ. |
| Khả năng chỉnh sửa bản địa (Native editability) | `pending` | Mã SVG có cấu trúc vector thuần túy; việc kiểm chứng mở, chỉnh sửa, lưu và mở lại trên các phần mềm đồ họa vector thực tế (như Illustrator, Inkscape) thuộc thẩm quyền của controller. |
| Bố cục và hiển thị phông chữ (Layout & font) | `pending` | Khai báo phông chữ `Arial`; hiển thị thực tế trên các trình mở cần controller thẩm định. |
| Khả năng trợ năng thực tế (Accessibility) | `pending` | Đã khai báo đầy đủ title, desc, role, lang, aria-labelledby; cần kiểm chứng qua các công cụ đọc màn hình thực tế. |
| Phạm vi quyền sử dụng (Rights scope) | `pass-with-caveat` | Giữ nguyên liên kết điều khoản World Bank, thông báo CC BY 4.0 và lưu ý hạn chế của chỉ báo bên thứ ba. |
| Điểm số đánh giá của chủ sở hữu (Owner final score) | `pending` | Trạng thái `pending-personal-review` sau khi controller và chủ sở hữu hoàn tất kiểm thử thực tế. |
| Chứng nhận khoa học / chuyên gia | `not-established` | Kết quả thực thi công cụ và bộ đọc không tự động cấp chứng nhận khoa học hoặc chứng nhận ổn định toàn cầu. |

---

## 5. Limitations

1. **Dữ liệu snapshot theo thời điểm**: Dữ liệu phản ánh snapshot từ API World Bank tại thời điểm cập nhật phản hồi `2026-07-13`. Nhà cung cấp số liệu có thể cập nhật hoặc điều chỉnh các số liệu lịch sử trong các đợt phát hành tương lai.
2. **Thiếu hụt metadata trường đơn vị gốc**: Trường `unit` trong phản hồi chính thức của API World Bank hoàn toàn để trống. Biểu đồ bảo toàn tính thiếu hụt này một cách trung thực, không tự ý gán thêm bất kỳ đơn vị nào.
3. **Ý nghĩa của đường đa tuyến**: Đường nối giữa các điểm chỉ nhằm mục đích trực quan hóa xu hướng biến thiên qua các mốc quan sát; không đại diện cho giá trị nội suy giữa các năm và không hàm ý bất kỳ mối quan hệ nhân quả nào.
4. **Giới hạn kiểm tra công cụ**: Việc hoàn thành kết xuất qua `rsvg-convert` chỉ xác nhận tệp SVG hợp lệ về mặt cú pháp kết xuất; các tiêu chí về khả năng chỉnh sửa bản địa (open/edit/save/reopen), bố cục mỹ thuật và trợ năng trực quan cuối cùng vẫn đang chờ kiểm chứng thực tế từ controller.
5. **Ranh giới pháp lý và bản quyền**: Tuân thủ điều khoản World Bank tại `https://data.worldbank.org/summary-terms-of-use`. Resource ghi nhận giấy phép mặc định `CC BY 4.0 with World Bank terms` kèm lưu ý: **`Third-party indicators may have additional restrictions.`** Kết quả của ca đánh giá này phục vụ mục đích kiểm thử cá nhân (`personal-use`), không suy diễn quyền tái phân phối thương mại không giới hạn.
