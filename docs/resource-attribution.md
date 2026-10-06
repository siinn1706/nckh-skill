# Ghi công tài nguyên đi kèm

Bốn package r41 giữ `resource-access on`, cùng mười ba nhóm tài nguyên đã đăng ký.
Mỗi skill sử dụng tài nguyên có bản sao giấy phép/notice trong references của
chính skill đó. Bảng dưới liên kết đến một bản trong package Codex; các package
Claude, Cursor và Antigravity giữ cùng tài nguyên và notices theo manifest.

| Tài nguyên | Giấy phép | Bản ghi công đi kèm |
|---|---|---|
| Reporting guidelines từ K-Dense | MIT | [License](../packages/codex/skills/nckh-method/references/_shared/core/profiles/resources/k-dense-license.md), [attribution](../packages/codex/skills/nckh-method/references/_shared/core/profiles/resources/k-dense-attribution.md) |
| Publisher profiles từ K-Dense | MIT | [License](../packages/codex/skills/nckh-visuals/references/_shared/core/profiles/resources/k-dense-license.md), [attribution](../packages/codex/skills/nckh-visuals/references/_shared/core/profiles/resources/k-dense-attribution.md) |
| UI heuristics từ UI UX Pro Max | MIT | [License](../packages/codex/skills/nckh-frontend/references/_shared/core/profiles/resources/ui-ux-pro-max-license.md), [attribution](../packages/codex/skills/nckh-frontend/references/_shared/core/profiles/resources/ui-ux-pro-max-attribution.md) |
| English writing advice từ Nature Skills | Apache-2.0 | [License](../packages/codex/skills/nckh-write/references/_shared/core/profiles/resources/nature-skills-license.md), [attribution](../packages/codex/skills/nckh-write/references/_shared/core/profiles/resources/nature-skills-attribution.md) |
| Ba đoạn văn/thơ Wikisource | CC BY-SA 4.0 cho đóng góp trang; quyền tác phẩm nền được ghi riêng | [Nguồn, tác giả/người dịch và rights notice](../packages/codex/skills/nckh-write/references/_shared/core/profiles/resources/wikisource-rights.md) |
| Hai mẫu bài khoa học Europe PMC | CC BY 4.0 ở cấp bài | [Tác giả, DOI/PMCID và rights notice](../packages/codex/skills/nckh-write/references/_shared/core/profiles/resources/pmc-rights.md) |
| Dân số Việt Nam 2000–2025, World Bank | CC BY 4.0 của indicator | [World Bank, nhà cung cấp dữ liệu và rights notice](../packages/codex/skills/nckh-visuals/references/_shared/core/profiles/resources/worldbank-rights.md) |
| Mười dòng UCI Bank Marketing | CC BY 4.0 | [Tác giả, DOI và rights notice](../packages/codex/skills/nckh-market-research/references/_shared/core/profiles/resources/uci-rights.md) |
| Hai code fixture Django | BSD-3-Clause | [Rights record](../packages/codex/skills/nckh-code-review/references/_shared/core/profiles/resources/swe-bench-rights.md), [notice của hai tệp](../packages/codex/skills/nckh-code-review/references/_shared/core/profiles/resources/swe-bench-notice.md) |

## Nguồn kiểm tra cho các snapshot

- Europe PMC: XML của [PMC13623134](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13623134/fullTextXML)
  và [PMC13623154](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13623154/fullTextXML)
  chứa thông báo copyright và giấy phép ở cấp bài. Bản đóng gói giữ title,
  tác giả, DOI/PMCID, nguồn và giới hạn excerpt trong record/notice.
- World Bank: [Population, total — SP.POP.TOTL](https://data.worldbank.org/indicator/SP.POP.TOTL)
  và [dataset terms](https://www.worldbank.org/ext/en/legal/terms-conditions/datasets).
  Notice ghi công World Bank, World Development Indicators và bốn nhóm nhà
  cung cấp dữ liệu; snapshot ngày 03/10/2026 giữ giá trị từ API.
- Wikisource: các URL parent/child theo revision, tên tác giả/người dịch,
  trạng thái tác phẩm nền và thay đổi do chuẩn hóa nằm trong notice đã liên kết.
  Giữ khác biệt năm 1925/1926 của *Tài mạng tương đố*. Phạm vi review bản dịch
  Phan Khôi năm 1928 được ghi rõ trong notice.

Khi sao chép hoặc điều chỉnh tài nguyên, giữ nguồn, ghi công và giấy phép áp
dụng; đóng góp trang theo CC BY-SA giữ điều kiện chia sẻ tương ứng. Các giấy
phép upstream chỉ áp dụng cho phần nội dung được xác định trong record/notice.

Manifest và source lock giữ hash, provenance và các nhãn qualification gốc.
Xem [phạm vi bản công khai](public-edition.md) để phân biệt quyền chia sẻ và
kết quả kiểm tra tính toàn vẹn với qualification còn mở.


## Bốn pack tham khảo tự biên soạn

Statistical recipes, telemetry fields, AIOps benchmark cards và evaluation
recipes có 14 record, với tám binding đến consumer. Registry giữ metadata
nguồn, snapshot hash, phạm vi áp dụng và provenance của từng pack.
Xem [rights record](../nckh-kit/core/profiles/resources/research-packs-rights.md),
[attribution](../nckh-kit/core/profiles/resources/research-packs-attribution.md)
và [resource registry](../nckh-kit/core/registry/catalog/resources.json).
Quyền chia sẻ source/data do chủ sở hữu cấp cho lần xuất bản này được ghi tại
[phạm vi bản công khai](public-edition.md); nhãn quyền lịch sử vẫn được giữ nguyên.
