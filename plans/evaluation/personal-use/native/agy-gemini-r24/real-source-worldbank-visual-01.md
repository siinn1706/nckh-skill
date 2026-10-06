# Blocker Memo: real-source-worldbank-visual-01

## 1. Blocker Status & Contract Reference

- **Mã ca đánh giá (case_id)**: `real-source-worldbank-visual-01`
- **Làn đánh giá (lane)**: World Bank measurement and editable visual
- **Kỹ năng quản lý (governing skill)**: `nckh-visuals`
- **Trạng thái hợp đồng đầu ra (Output Contract Status)**: **UNMET (BLOCKED)**
- **Đường dẫn hợp đồng bị chặn thực tế (Exact Contract Path)**:
  `C:/Users/USER/Downloads/test-skill/.agents/skills/nckh-visuals/references/_shared/extensions/native-documents/contract.json`
- **Các điều khoản ràng buộc liên quan (Governing Skill Contracts)**:
  1. `C:/Users/USER/Downloads/test-skill/.agents/skills/nckh-visuals/SKILL.md` (Workflow, dòng 28–29):
     > *"Bind only an available, permitted native-document/provider engine through the extension contract. An empty/unverified engine map returns unavailable; do not fabricate a successful render or silently substitute raster for editable PPTX/SVG/source."*
  2. `C:/Users/USER/Downloads/test-skill/.agents/skills/nckh-visuals/references/visual-acceptance.md` (Dòng 14):
     > *"Empty/unverified engine binding is unavailable. Do not fabricate render output."*

---

## 2. Lý do Kỹ thuật Chi tiết (Exact Reason for Blocker)

1. Tệp hợp đồng mở rộng công cụ dựng tài liệu bản địa (`references/_shared/extensions/native-documents/contract.json`) khai báo rõ ràng:
   ```json
   {
     "schema_version": 1,
     "id": "native-documents",
     "capability": "editable-deck/chart/diagram/artwork",
     "status": "unavailable",
     "engine_binding": null
   }
   ```
2. Thuộc tính `status` đang là `"unavailable"` và `engine_binding` là `null`. Không có bất kỳ công cụ kết xuất/kiểm tra vector (vector rendering/inspection engine) nào được cấu hình hoặc xác minh hợp lệ trong môi trường hiện tại.
3. Hợp đồng kỹ năng `nckh-visuals` nghiêm cấm tuyệt đối việc tự ý giả mạo kết quả kết xuất (fabricate render output), tự gán trạng thái đạt chuẩn kết xuất mà không có bằng chứng từ công cụ mở/xem thực tế, hoặc thay thế tệp vector có thể chỉnh sửa bằng hình ảnh raster/văn bản tĩnh chưa qua kiểm định.
4. Do đó, yêu cầu tạo tệp vector đồ họa độc lập `real-source-worldbank-visual-01.svg` và biên bản kiểm thử QA kết xuất `real-source-worldbank-visual-01.md` **bị chặn hợp lệ** theo đúng hợp đồng. Không được phép bỏ qua hoặc sửa đổi hợp đồng khi công cụ chưa khả dụng.

---

## 3. Bảo toàn Chứng cứ Nguồn & Dữ liệu Tiếp nhận (Preserved Source and Reader Evidence)

Mặc dù việc kết xuất tạo tác vector bị chặn bởi hợp đồng công cụ, toàn bộ dữ liệu nguồn và biên nhận từ bộ đọc độc lập (`search-resource.py`) đã được tiếp nhận và bảo toàn nguyên vẹn:

- **Mã nguồn (source_id)**: `worldbank-vnm-SP.POP.TOTL-2000-2025`
- **Bộ định vị API (API Locator)**: `https://api.worldbank.org/v2/country/VNM/indicator/SP.POP.TOTL?date=2000%3A2025&format=json&per_page=100`
- **Chỉ số (Indicator)**: `SP.POP.TOTL` (`Population, total`)
- **Quốc gia**: `Viet Nam` (`VNM`)
- **Ngày truy xuất (retrieved_at)**: `2026-10-03`
- **Cập nhật phản hồi lần cuối (response_lastupdated)**: `2026-07-13`
- **Tệp JSON thô (raw_file)**: `raw/worldbank-vnm-population-2000-2025.json`
- **Mã băm SHA-256 tệp thô**: `a63e499e9f24ae600bb52ecac8acb07bbb959a812e830cc7cf870fbca2fe5781`
- **Dung lượng tệp thô**: `5217 bytes`
- **Tệp tiếp nhận từ bộ đọc (Reader Receipt)**:
  `plans/evaluation/personal-use/native/agy-gemini-r24/reader-receipts/nckh-visuals__R-worldbank-vietnam-population__worldbank-vnm-SP.POP.TOTL-2000-2025.json`
- **Mã băm bản ghi chiếu (record_sha256)**: `a29802fa36bc453ce9abbf9789e119bae689462ffd6348e327ee7d7f5e9cb4b2`
- **Giấy phép (License)**: `CC BY 4.0` mặc định theo điều khoản World Bank (`https://data.worldbank.org/summary-terms-of-use`).
- **Số lượng quan sát (Observation Count)**: Đúng `26` quan sát hàng năm từ 2000 đến 2025.
- **Số lượng giá trị hợp lệ (Non-null Count)**: `26` (không có giá trị thiếu hay null).
- **Giá trị năm 2000 (first_value_2000)**: `77154011` (77.154.011)
- **Giá trị năm 2025 (last_value_2025)**: `101598527` (101.598.527)
- **Phép tính số học tái lập (Reproducible Arithmetic)**:
  - Thay đổi tuyệt đối:
    $$\Delta = 101.598.527 - 77.154.011 = +24.444.516$$
  - Thay đổi phần trăm:
    $$\% \Delta = \frac{24.444.516}{77.154.011} \times 100\% = 31{,}682754639936995\% \approx +31{,}682755\%$$
- **Trường đơn vị API để trống (Raw Blank Unit Field)**:
  - Trường `unit` trong phản hồi gốc của World Bank hoàn toàn là chuỗi rỗng (`unit: ""`).
  - Tuân thủ chính sách bảo toàn (`preservation-policy.md`), không tự gán đơn vị (như "người" hay bất kỳ đơn vị suy diễn nào). Nhãn trục Y nếu được dựng sẽ phải là: `Population, total (SP.POP.TOTL; raw unit field blank)`.
- **Nội dung văn bản thay thế (Vietnamese Alt Text Candidate - Non-causal)**:
  - *"Biểu đồ chuỗi thời gian ghi nhận chỉ số dân số tổng cộng của Việt Nam (mã chỉ số SP.POP.TOTL, trường đơn vị để trống theo API World Bank) tăng liên tục từ 77.154.011 năm 2000 lên 101.598.527 năm 2025 qua 26 điểm quan sát hàng năm. Dữ liệu thuần túy mô tả số lượng quan sát từ snapshot của Ngân hàng Thế giới, không hàm ý hoặc khẳng định nguyên nhân hay tác động nhân quả nào."*

---

## 4. Kết luận Xử lý Ca (Case Resolution)

Hợp đồng kỹ năng `nckh-visuals` được tuân thủ nghiêm ngặt: không tạo giả mạo tệp `.svg` hay biên nhận QA khi engine chưa được kích hoạt (`status: unavailable`). Ca đánh giá ghi nhận trạng thái **UNMET (BLOCKED)** do ràng buộc công cụ ngoài phạm vi, bảo toàn toàn bộ chứng cứ nguồn và tiếp tục thực hiện đầy đủ các ca đánh giá còn lại.
