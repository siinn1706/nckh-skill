# Dùng NCKH trong project cá nhân

Chế độ personal-use dành cho người dùng tự dùng skill, đánh giá đầu ra và yêu cầu
sửa tiếp. Tiêu chí mặc định nằm trong
[profile chung](../core/profiles/acceptance/personal-use.json); mỗi skill đọc dòng
đúng identity của mình cùng phạm vi áp dụng của nguồn.

Danh mục nguồn duy nhất là [resource registry](../core/registry/catalog/resources.json).
Các pack dưới đây là snapshot nhỏ cho personal-use, có rights note và lineage
riêng; chúng không phải corpus đại diện hoặc giấy phép phát hành chung.

## Cách dùng

1. Gọi skill phù hợp và mô tả kết quả cần có, tài liệu đầu vào, ngôn ngữ đầu ra.
2. Cung cấp source hoặc chọn resource phù hợp domain/thể loại. Giữ URL, phiên bản,
   quyền, số liệu và bối cảnh của mẫu.
3. Skill tạo đầu ra, ghi việc đã kiểm, lỗi và những điều chưa biết. Khi task đã
   được giao thực thi, các bước thường lệ tiếp tục trong phạm vi đó.
4. Người dùng đọc và dùng đầu ra, rồi chỉ rõ phần cần giữ hoặc sửa. Có thể chấm
   theo thang cá nhân; bộ kit không gán một điểm đạt chung cho mọi domain.
5. Feedback ghi đúng artifact/revision/input. Khi đầu ra hoặc nguồn đổi, kiểm
   lại phần liên quan và giữ attempt trước.

Chọn `nckh-humanwrite --vi` hoặc `--en` cho polish/dịch; chọn
`nckh-paperwrite --vi` hoặc `--en` cho outline/section/argument/reporting/response
từ evidence đã có. `nckh-write` route tương thích theo action. Hai flag cùng lúc
dừng trước sửa; thiếu target rõ ràng thì resolve brief/draft rồi hỏi một câu khi
còn mơ hồ. Ngôn ngữ đầu ra độc lập locale/domain/genre của resource.

## Checklist đọc đầu ra

- Đúng công việc và đúng skill đã yêu cầu.
- Có sản phẩm thực tế mở/đọc/dùng được.
- Claim, quote, số liệu và nguồn không vượt quá bằng chứng.
- Văn phong và thể loại phù hợp mục đích của người dùng.
- Hành động nằm trong quyền đã giao; lỗi và việc chưa xong được ghi rõ.
- Phần người dùng đã đánh giá được phân biệt với kiểm tra tự động.

Reviewer bên ngoài và protected holdout không là điều kiện bàn giao của chế độ
này. Người dùng là người chấm cuối sau khi tự dùng. Chưa có feedback nghĩa là
đánh giá cá nhân còn chờ; không tự ghi một lần chấm đã xảy ra.

## Các pack thật và phạm vi quyền

| Resource | Consumer đã định | Nội dung đọc được và giới hạn quyền |
|---|---|---|
| `R-vi-wikisource-passages` | `nckh-write`, `nckh-taste`, `nckh-humanwrite` | Ba passage con thực tế từ ba tác phẩm Wikisource, mỗi record giữ parent/root locator metadata; không coi root là prose record. Giữ attribution CC BY-SA ở cấp trang; tuyên bố public-domain của tác phẩm cần kiểm jurisdiction riêng. |
| `R-pmc-scientific` | `nckh-write`, `nckh-evidence`, `nckh-method`, `nckh-humanwrite`, `nckh-paperwrite` | Hai projection article-level từ các XML snapshot đã kiểm CC BY 4.0; provenance giữ locator và hash của snapshot. Phạm vi ngữ liệu nghiêng biomedical/health science; không suy ra quyền từ nhãn PMC Open Access chung. |
| `R-worldbank-vietnam-population` | `nckh-visuals`, `nckh-analytics`, `nckh-method` | Một series dân số Việt Nam `SP.POP.TOTL`, 2000–2025, từ API snapshot. Giữ nguyên giá trị và `unit` trống; điều khoản World Bank và hạn chế indicator bên thứ ba vẫn áp dụng. |
| `R-django-sqlmigrate-fixtures` | `nckh-fix`, `nckh-test`, `nckh-code-review` | JSONL gồm hai code fixture Django BSD 3-Clause và task locators cho `django__django-10087`. Không đưa issue text, problem statement, benchmark patch, test patch hoặc dataset-row bytes vào pack; quyền BSD chỉ áp dụng cho hai fixture. |
| `R-uci-bank-marketing` | `nckh-market-research`, `nckh-marketing-plan`, `nckh-campaign`, `nckh-analytics` | Mười dòng thật từ `bank.csv`, với lineage archive chính thức và DOI/CC BY 4.0 trong provenance. `duration` xảy ra sau contact và có thể leak target; dữ liệu không phải campaign copy hoặc causal uplift. |

Artifact đã chuẩn hóa và mọi raw acquisition có hash riêng; lookup trả source
locator, resource ID, lineage, transformation và limitation để phân biệt bytes
được đóng gói với nguồn upstream. Các registry/schema/reader check này chỉ là
source/package evidence.

## Phạm vi của mẫu thật và kiểm tra

Mẫu VI lịch sử chỉ dùng theo thể loại và bối cảnh cụ thể. Bài PMC có quyền riêng
từng bài. World Bank giữ số đo đã lấy và `unit` trống khi nguồn trả trống; task engineering và dữ liệu
marketing giữ giới hạn nguồn. Mẫu đã trích cần original snapshot, locator,
attribution và lineage; một mẫu không đại diện toàn bộ ngôn ngữ hoặc domain.

Reader, hash, tests và build kiểm những thuộc tính cụ thể của source/package.
Model run cần input/output và route observation thật. Selected model label,
model requested trong lệnh và model telemetry là các quan sát khác nhau.

Native evidence vẫn cần host discovery, invocation, output và cleanup thực tế;
personal-use không tự ghi build, cài đặt hoặc native acceptance. Owner evidence
chỉ xuất hiện khi người dùng đọc/dùng artifact rồi ghi feedback gắn với
revision, artifact hash và input hashes. Scientific/domain evidence cần reviewer,
rubric và threshold riêng; không gate nào trong bốn lớp này được tạo bởi hash,
parse, registry validation hay test local.

[Qualification khoa học/stable](qualification.md) và
[release gates](release-checklist.md) vẫn có phạm vi riêng. Personal-use không
cấp human gold, peer review, scientific validation hoặc chứng nhận phát hành.
