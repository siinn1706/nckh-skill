# Blocker: real-source-worldbank-visual-01

Output contract: **unmet**. Không có file SVG. Không có tuyên bố render, editability, hay visual acceptance.

## Contract path and reason

Hợp đồng engine đã đọc:

`C:/Users/USER\Downloads\test-skill\.agents\skills\nckh-visuals\references\_shared\extensions\native-documents\contract.json`

- `id`: `native-documents`
- `capability`: `editable-deck/chart/diagram/artwork`
- `status`: `unavailable`
- `engine_binding`: `null`
- `dependencies`: `[]`

Cùng skill, `references/visual-acceptance.md`: empty/unverified engine binding is unavailable; do not fabricate render output.

`nckh-visuals` SKILL.md: an empty/unverified engine map returns unavailable; do not fabricate a successful render or silently substitute raster for editable SVG/source.

Hợp đồng này không được viết lại và không được đi vòng. Vì `engine_binding` null, case này không tạo SVG.

## Source and data receipt

Reader vẫn chạy và trả record.

- `source_id`: `worldbank-vnm-SP.POP.TOTL-2000-2025`
- Locator: `https://api.worldbank.org/v2/country/VNM/indicator/SP.POP.TOTL?date=2000%3A2025&format=json&per_page=100`
- Query: `worldbank-vnm-SP.POP.TOTL-2000-2025`
- Reader: `C:/Users/USER\Downloads\test-skill\.agents\skills\nckh-visuals\references\_shared\scripts\search-resource.py`
- Pack: `R-worldbank-vietnam-population`, domain `chart-measurement`, locale `und`, genre `indicator-time-series`, consumer `nckh-visuals`
- Receipt: `plans/evaluation/personal-use/native/cursor-grok-r24/reader-receipts/nckh-visuals__R-worldbank-vietnam-population__worldbank-vnm-SP.POP.TOTL-2000-2025.json`
- Status: `matched`, `resource_read=true`, 1 record
- Pack `resource_sha256`: `a29802fa36bc453ce9abbf9789e119bae689462ffd6348e327ee7d7f5e9cb4b2`
- `record_sha256`: `65b7007d7ea17cae6091e2925ec725bf88433573635536386868bfa4c1304800`
- `reader_sha256`: `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb`
- Raw API: `raw/worldbank-vnm-population-2000-2025.json`, SHA-256 `a63e499e9f24ae600bb52ecac8acb07bbb959a812e830cc7cf870fbca2fe5781`, 5217 byte
- `response_lastupdated`: `2026-07-13`
- `retrieved_at`: `2026-10-03`
- Indicator label: `Population, total`
- `indicator_id`: `SP.POP.TOTL`
- Country: `Viet Nam` / `VNM`
- Quan sát: 26. Non-null: 26. `unit` trên mọi quan sát: `""`
- Năm có mặt: 2000 đến 2025, mỗi năm một giá trị
- 2000 = 77154011
- 2025 = 101598527
- Chênh tuyệt đối: `101598527 - 77154011 = 24444516`
- Phần trăm chính xác: `24444516 / 77154011 * 100 = 31.682754639936995628133967007885046961459981646320`
- Tiền tố `31.682754639936995` là phần đầu của chuỗi đó, không phải kết quả đã làm tròn
- Giấy phép: `CC BY 4.0 default with World Bank terms`; `https://data.worldbank.org/summary-terms-of-use`; caveat chỉ số bên thứ ba có thể có hạn chế thêm
- `rights_rationale`: snapshot có ngày, không phải khẳng định giá trị hiện hành

Các số trên là evidence của reader. Chúng không phải chart đã render.

## Editable visual

Unmet. Không tạo `real-source-worldbank-visual-01.svg`. Không có source-to-mark map, không có object text/data trong một SVG, không có raster thay thế.

## Axes/units/caption/alt text

Unmet. Không có trục, caption, hay alt text gắn vào một hình. Trường `unit` nguồn để trống; memo này không gán đơn vị được cung cấp và không mô tả nguyên nhân của chuỗi số.

## Hash and QA receipt

Unmet như một QA của hình. Không có artifact SVG nên không có hash render, viewer, font, hay run id của engine.

Hash nguồn và reader nằm ở mục receipt bên trên. Render/inspection của hình: không chạy. Không ghi trạng thái pass.

## Limitations

- Engine native-documents unavailable là lý do hợp đồng đầu ra unmet.
- Snapshot World Bank có thể bị nhà cung cấp hiệu đính.
- `unit` trống là metadata thiếu, được giữ thiếu.
- Chủ sở hữu là người chấm sau khi dùng. Trạng thái: `pending-personal-review`. Không có chứng nhận khoa học hay thị giác.
