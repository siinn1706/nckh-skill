# Hợp đồng thiết kế bộ skill viết và nghiên cứu Việt–Anh

Ngày: 30/09/2026, Asia/Saigon. Trạng thái: đề xuất để lập kế hoạch, chưa phê duyệt triển khai.

**Cập nhật sau duyệt:** người dùng đã cho phép áp dụng 11 chỉnh sửa vào plan,
thêm hooks/subagents, cost optimization, automatic catalog routing và context cap.
Chi tiết hiện hành nằm ở [plan](../260930-0905-vietnamese-research-skill-kit/plan.md),
[routing/budgets](../260930-0905-vietnamese-research-skill-kit/design-routing-hooks-cost.md)
và [standards/coverage](../260930-0905-vietnamese-research-skill-kit/standards-and-failure-catalog.md).
Các tài liệu này cụ thể hóa design bên dưới; không có approval triển khai.

## Quyết định đề xuất

Xây một lớp skill cá nhân mỏng, theo mô hình **gọi năng lực upstream rồi kiểm tra đầu ra**. Cập nhật theo bổ sung trực tiếp của người dùng: ưu tiên giữ AgentKit là dependency được maintainer cập nhật, không chép prompt của AgentKit thành bản riêng phải tự bảo trì. Bộ gồm hai entrypoint `research-plan`/`research-cook` và khoảng 10 module chuyên môn bên dưới; đây là ranh giới trách nhiệm, không phải 12 engine phải viết lại. Bộ riêng sở hữu brief, bằng chứng, gu Việt, profile venue và cổng nghiệm thu; AgentKit/nature-skills/runtime official là worker được chọn theo khả năng và quyền sử dụng. Chỉ adapt/copy phần thật sự cần và có license rõ. Giữ đầy đủ năm mục tiêu và các chức năng trong blueprint.

Hợp đồng đầu ra, ràng buộc, ngoài phạm vi và nghiệm thu của lượt này nằm ở [báo cáo nguồn cục bộ](research-260930-0905-local-sources-and-evidence.md). Lượt này dừng ở tài liệu. Mọi tên file/module dưới đây là **thiết kế tương lai**, không phải thứ đã tồn tại.

## 1. Phân rã năng lực dự kiến

**Ngôn ngữ do người dùng yêu cầu:** `SKILL.md`, metadata, chỉ dẫn bắt buộc, adapter contracts và tài liệu vận hành của bộ tương lai được viết bằng tiếng Anh. Ví dụ, corpus và câu mẫu tiếng Việt giữ nguyên tiếng Việt; quote và nội dung nguồn không được dịch thay bản gốc. Ngôn ngữ chỉ dẫn không khóa ngôn ngữ đầu ra: brief có `output_language=vi|en|bilingual`, thể loại và style profile riêng. Tài liệu plan hiện tại viết tiếng Việt để người dùng duyệt; không có bằng chứng nào trong lượt này chứng minh instruction tiếng Anh tự nó giảm ảo giác hoặc nâng chất lượng.

| Entrypoint dự kiến | Hợp đồng |
|---|---|
| `research-plan` | Tạo short plan index và phase detail cho nghiên cứu/viết/visuals; khóa outcome, constraints, non-goals, acceptance, evidence needs, venue/source/style profile và tool/data permission. Không tạo bài/slide hoàn chỉnh, chạy thí nghiệm, cài dependency hoặc tự gọi cook. |
| `research-cook` | Đọc kế hoạch được người dùng cho phép thực hiện, khóa revision/hash và inputs, chọn worker theo từng phase, kiểm receipt/evidence/artifact rồi bàn giao. Tiếp tục/resume theo dữ liệu thật, không suy completed từ file hiện diện; thay đổi material scope/profile/input làm mất hiệu lực nghiệm thu liên quan và cần chốt lại. |

Đây là lifecycle cho sản phẩm nghiên cứu, không chỉ là đổi tên `ak-plan`/`ak-cook`. `ak-plan` có thể là planning worker khi hợp đồng tương thích. `ak-cook` hiện có description/workflow thiên về code, inspect code/tests và TDD; chỉ gọi nguyên skill cho phần thực sự là triển khai công cụ/code đã được cho phép. Với viết/paper/slide, dùng control pattern phù hợp và domain workers, không tự áp lint/build/Git/commit vào mọi nhiệm vụ. Tác vụ nhỏ có thể dùng brief/plan ngắn trong phiên, nhưng vẫn cần yêu cầu thực hiện rõ ràng; có plan trên đĩa không tự cấp quyền cook. `--auto` nếu hỗ trợ sau này chỉ giảm hỏi lại trong scope đã duyệt, không bỏ kiểm chứng, quyền upload, license hay human review bắt buộc.

| Skill dự kiến | Sở hữu | Không được làm |
|---|---|---|
| `research-brief` | Mục đích, người đọc, ngôn ngữ, mức sửa, nguồn cho phép, venue/profile, quyền dùng công cụ | Không ép một tạp chí mặc định hay hỏi lại lựa chọn đã có |
| `research-discovery` | Search log, sàng lọc, deduplicate/version linking, literature map/review, gap có phạm vi | Không coi kết quả tìm kiếm là đã đọc toàn văn; không tuyên bố chưa ai làm khi chưa đủ search |
| `research-reader` | Đọc nguồn, evidence cards, số liệu/quote/locator, phương pháp và giới hạn | Không tự chấp nhận nguồn hay quyết định truth chỉ vì tác giả viết vậy |
| `evidence-audit` | Fact-check, claim support, citation/quote/metadata audit, retraction/correction checks | Không sửa giọng toàn bài; không cấp nhãn verified chung cho mọi chiều |
| `research-reasoning` | Cấu trúc lập luận, so sánh, phương pháp, giả thuyết; tiêu thụ glossary dùng chung | Không tạo kết quả, công thức hay phân tích thống kê không có cơ sở |
| `vi-writing` | Soạn/sửa/đánh bóng tiếng Việt; minimal-diff hoặc rewrite theo brief | Không tự tìm citation để hợp thức hóa ý đã bịa; không nâng certainty |
| `vi-taste` | Critique độc lập theo thể loại, người đọc, gu cá nhân; cặp trước/sau có giải thích | Không là AI detector; không cấm từ tuyệt đối hoặc sửa dữ kiện bằng cảm giác |
| `en-scientific-writing` | Viết/sửa học thuật tiếng Anh, cấu trúc rhetorical moves, bảo toàn ý khi chuyển ngữ | Không đánh đồng “Native-like” với đúng khoa học; không áp IMRaD cho mọi thể loại |
| `research-visuals` | Slide, biểu đồ dữ liệu, sơ đồ cơ chế, ảnh minh họa; chọn engine theo đầu ra | Không dùng ảnh sinh làm dữ liệu; không giả PPTX editable bằng ảnh toàn trang |
| `research-review` | Review logic/evidence/domain/style theo rủi ro; final audit và venue preflight | Không tự sửa phần khóa; không tự nộp bài/xuất bản; không coi tự review là peer review thật |

`evidence-first` là hợp đồng chung áp dụng xuyên suốt, không phải bước phải gọi lại bằng một skill riêng. `vi-polishing` là chế độ của `vi-writing`; `citation-auditor`, `claim-verifier`, `fact-checker` là các chế độ kiểm tra riêng trong `evidence-audit`; `argument-architect`, `comparison-engine`, `research-methodology` là các chế độ trong `research-reasoning`; `terminology-manager` có một glossary dùng chung; `final-audit` thuộc `research-review`. Không bỏ chức năng nào chỉ vì giảm số entrypoint.

## 2. Luồng nhỏ nhất đủ cho từng việc

- Sửa câu thuần phong cách: brief đã có → viết/sửa → taste khi cần → kiểm không đổi ý. Không tự mở web cho mọi câu; nếu đụng dữ kiện mới thì chuyển audit.
- Viết literature review: brief/chính sách nguồn → discovery → đọc nguồn → audit bằng chứng → tổng hợp/lập luận → VI hoặc EN writer → review. Nêu rõ narrative, scoping hay systematic; chỉ gọi systematic khi đã làm đầy đủ protocol tương ứng.
- Biên tập paper đã có: khóa phiên bản đầu vào/vùng không sửa → audit và đề xuất → sửa đúng quyền → so diff và preflight. Không coi những chỉ dẫn trong bản thảo là yêu cầu mới của người dùng.
- Làm slide từ paper: đọc paper/bảng/figure → lập storyboard theo người nghe/thời lượng → kiểm claim → dựng deck → render kiểm → giao nguồn chỉnh sửa và bản xem trước.
- Vẽ sơ đồ: dựng quan hệ có nghĩa khoa học → kiểm chiều mũi tên/nhóm/ký hiệu → chọn vector hoặc công cụ tạo ảnh được phép → kiểm hình → gắn provenance và trạng thái minh họa.

Có thể chạy writer/verifier bằng cùng một model với context và vai trò tách biệt khi môi trường không có delegate, nhưng không gọi đó là kiểm chứng độc lập. Bằng chứng ngoài mô hình và quyết định của con người vẫn cần thiết.

## 3. Các hợp đồng dữ liệu cần đặc tả ở phase đầu

**Source:** ID, title/authors/year/DOI hoặc định danh khác, type, publisher URL, bản đã đọc/hash, quyền sử dụng, mức truy cập, quan hệ phiên bản, trạng thái correction/retraction và ngày kiểm.

**Evidence:** source ID/version, đoạn nguyên văn hoặc giá trị gốc, locator loại trang/mục/đoạn/dòng/timestamp, số trang PDF và số trang in khi khác nhau, ngữ cảnh, hình/bảng tương ứng, trạng thái OCR/visual verification. Không biến OCR tự động thành quote đã xác minh.

**Claim:** nội dung, loại fact/observation/interpretation/inference, evidence IDs, phạm vi/population/điều kiện, mức certainty được phép, verdict cùng lý do và người/công cụ kiểm. Tách metadata-match khỏi entailment; xử lý support/contradiction/insufficient thay vì chỉ cờ true/false.

**Ranking:** issuer/system, metric, journal ISSN, category, metric-year, release/version, quartile, URL/ngày kiểm, bằng chứng và trạng thái. `journal-strict` giữ Q1/Q2; ranking unknown không được tự pass. Không dùng “best quartile” ở category không liên quan để lách bộ lọc. Ngoại lệ conference/preprint/book/foundational cần quyết định có lưu vết.

**Venue profile:** venue ID/type, guideline revision/year, track/article type, stage, official sources, scope của từng constraint, citation/display format, limits, anonymity và chính sách AI khi đã kiểm chứng. Cấm trộn profile từ nhiều venue vào cùng đầu ra. Conflict explicit giữa venue, mentor/project overlay, dữ kiện và sở thích: báo khác biệt, không tự giải bằng union hoặc điều kiện lỏng nhất.

**Style profile:** người đọc, thể loại, xưng hô, độ trang trọng, nhịp, từ vựng, đặc điểm mong muốn, ví dụ được phép dùng và lý do thích/không thích. Profile không sửa số liệu, thuật ngữ chuyên môn hoặc mức chắc chắn.

## 4. Thiết kế kho và đóng gói

Nguồn của bộ riêng có `skills/`, một `shared/` nhỏ cho hợp đồng, `profiles/` theo venue/style/project và bộ `evals/`. Không chép các kho tham khảo vào thư mục runtime tự khám phá skill. Source lock/attribution nằm ở mặt duy trì của repo, không nạp toàn bộ vào mỗi prompt.

Mặc định đề xuất thử nghiệm project-local trên môi trường Codex đang dùng; khả năng dùng cùng nội dung trên Claude là mục tiêu tương thích, không tuyên bố đã hỗ trợ khi chưa có consumer run. Việc cài user-global hoặc phát hành marketplace phải là bước được người dùng chọn riêng. Không buộc tạo MCP/server/database riêng nếu một file-ledger và công cụ có sẵn đáp ứng.

Mỗi package phải mang đủ references/shared contracts hoặc có dependency được kiểm tra. Không tạo skill có relative link tới máy cá nhân hoặc tới thư mục repo không đi kèm gói. Adapter runtime giữ bên ngoài lõi nội dung. Tên và metadata phải được kiểm tra trong catalog thật có cả skill cạnh tranh; không thêm toàn bộ tên đối thủ vào description để giành routing.

### 4.1. Gọi AgentKit mà không đóng băng khả năng cập nhật

Một skill là bộ chỉ dẫn, không mặc nhiên là API có hàm gọi. Adapter cần phân biệt: (a) nạp đúng skill đã cài trong lượt hiện tại, (b) giao cho subagent nếu runtime và người dùng cho phép, (c) dùng tool/CLI thực sự tồn tại khi capability đó có interface gọi được. Không bịa `ak run-skill` hay coi đọc `SKILL.md` là đã thực thi. `ak skills --help` hiện chỉ có graph/install/list/remove/search/show. `ak orchestrate --help` bản 2.19.0 nói external process supervision chỉ có trên Darwin; không lấy nó làm đường thực thi Windows mặc định.

Luồng đề xuất: brief đã khóa → resolve catalog thật → kiểm dependency/quyền/đầu ra → gọi một worker với context tối thiểu → nhận artifact và receipt → kiểm độc lập bằng nguồn, diff hoặc render theo tác vụ → accept, trả sửa có giới hạn, hoặc báo pending. Reader/writer không được tự thay venue hay cấp quyền cho tool. Lỗi, timeout hoặc thiếu receipt không được biến thành success; không tự retry thao tác trả phí hay có side effect chưa đối soát. Writer và critic cùng model phải được ghi rõ, không nhận là bằng chứng độc lập.

Receipt tối thiểu: run/task ID, skill ID và resolved path, kit/skill version cùng hash nội dung/dependency closure đã dùng, adapter/runtime/model nếu biết, brief/profile/input hashes, tool/data egress được phép, trạng thái, output paths/hashes, nguồn/locator và giới hạn còn mở. Không ghi khóa/API key hoặc toàn văn bí mật vào log chung. Upstream không có output schema thì adapter chuẩn hóa nhưng không tự điền giá trị thiếu hoặc tự chứng thực bằng chứng.

Hai mức version: **cài đặt đang có** và **bản đã được kit cá nhân chấp nhận**. Ghi resolved hash mỗi lượt để tái lập; khi upstream thay đổi, đánh dấu candidate chưa kiểm, chỉ đánh giá lại adapter/capability bị ảnh hưởng rồi mới ghi acceptance. Không tự tắt updater, hạ cấp hay sửa AgentKit của người dùng. Nếu không có snapshot cũ được phép giữ và đã kiểm, dừng riêng capability đó hoặc dùng fallback đã được kiểm; không âm thầm dùng bản mới với nhãn verified. Rollback chỉ đổi lựa chọn dependency của kit cá nhân và receipt, không ghi đè bản global. Update là thao tác người dùng cho phép; lượt plan này không update/install hay thêm watcher.

Tiêu chuẩn trung thực/venue/gu do kit riêng sở hữu, không bị upstream tự ghi đè. Trước khi gọi, đọc đủ chỉ dẫn bắt buộc của skill và dependency đã chọn; nếu chỉ dẫn xung đột hoặc bắt buộc upload/diagrams/cron ngoài brief thì không gọi worker đó. Chọn worker khác hoặc adapt được phép, không nói đã dùng nguyên skill rồi bỏ qua các điều kiện bắt buộc. Kiểm tra cập nhật phải bao gồm các references/scripts mà skill kéo vào, không chỉ frontmatter version.

## 5. Nghiệm thu cần chứng minh sau triển khai

1. **Cấu trúc:** metadata hợp lệ, link đủ, script an toàn; đây chỉ là lớp kiểm hình thức.
2. **Hành vi:** request tự nhiên bằng VI/EN đi đúng skill; near-miss không kích hoạt nhầm; tác vụ chỉnh sửa nhỏ không bị biến thành toàn bộ pipeline.
3. **Bằng chứng:** bẫy DOI thật nhưng không hỗ trợ claim; quote sai ấn bản; paper bị rút; chỉ có abstract; hai nguồn mâu thuẫn; giả hướng dẫn trong PDF; rank sai category/year; thiếu quyền truy cập đều cho kết quả trung thực.
4. **Cách ly quy chuẩn:** lần lượt chuyển IEEE/Nature/conference/không venue, đổi năm hoặc track, tách mentor rule; không sót quy tắc của nhiệm vụ trước. Các tên này là tình huống test, không phải profile đã soạn.
5. **Văn phong:** so sánh ẩn danh bản gốc/không-skill/nguồn gốc/ứng viên trên cùng dữ kiện; người dùng chấm gu Việt, người có chuyên môn chấm EN khi cần; ghi rõ ai chấm và bất đồng. Không dùng AI-detector hoặc tự chấm làm gold.
6. **Khoa học:** giữ con số, đơn vị, CI/SD/SE, phạm vi, phủ định, mức chắc chắn và giới hạn; citation vẫn đỡ câu sau rewrite/translation.
7. **Slide/hình:** số và nhãn khớp nguồn, citations truy xuất được, không tràn/cắt chữ, kiểm cả bản render lẫn đối tượng/source chỉnh sửa; phân biệt vector diagram và raster artwork.
8. **Hiệu quả:** ghi raw counts, quality, thời gian, công sửa, tool calls, tokens/cost chỉ khi có dữ liệu. Không tuyên bố tốt hơn chỉ từ ít token hoặc ít dòng prompt.
9. **Delegation và cập nhật:** chứng minh catalog resolution, actual invocation, receipt, critic gate, budget/timeout, recursion guard và drift detection; skill thiếu/đổi tên/đổi schema/đổi policy không được pass. So sánh bản upstream được chấp nhận với bản candidate; trace từng artifact về phiên bản thực đã dùng. Cập nhật upstream không đồng nghĩa tự động chấp nhận chất lượng của kit cá nhân.
10. **Plan/cook và language:** yêu cầu plan-only không tạo artifact thực thi; cook không chạy từ một plan chưa được cho phép; resume/đổi profile/đổi input/đổi dependency nhận đúng trạng thái. Chỉ dẫn English phải route được request tự nhiên bằng VI và EN, xuất đúng ngôn ngữ được chọn, không dịch sai quote/thuật ngữ và không biến prose task thành code workflow.

Thiết kế autoresearch: baseline và guard đóng băng trước; mỗi vòng đổi một thành phần; giới hạn mặc định đề xuất ba vòng development; giữ hoặc bỏ bằng evidence; holdout khóa riêng theo tài liệu/tác giả/chủ đề, không để rewrite agent thấy đáp án. Nếu đã xem holdout để sửa thì test đó thành development, phải có holdout mới. Mức này là đề xuất vận hành, không phải kết quả đo.

## 6. Trade-off và điểm thay đổi quyết định

Phương án bộ riêng gọn dựa trên giả định lấy được ví dụ giọng Việt có quyền dùng và có người đánh giá. Nếu chưa có, chỉ được gọi bản đầu là phong cách Việt trung tính đang thử nghiệm, không nhận là đã học “gu” cá nhân. Nếu license một nguồn không cho phép sao chép, giữ ý tưởng/điểm tích hợp được phép và viết mới; nếu thiếu công cụ render/đọc nguồn, báo hạn chế chứ không hạ tiêu chuẩn nghiệm thu.

Router thuần chỉ chọn tên skill thì chưa đủ kiểm soát chồng lấn. Phương án ưu tiên sau bổ sung của người dùng là **wrapper có hợp đồng, kiểm chứng và quản lý tương thích**, không phải router thuần và không phải fork nguyên kho. Tốn công adapter/eval ban đầu, bù lại tiếp tục nhận cải tiến upstream mà giữ được tiêu chuẩn cá nhân. Khi không thể gọi một worker an toàn/đúng định dạng, mới viết phần thiếu hoặc adapt có chọn lọc; không dùng “nhẹ” làm lý do bỏ chức năng đã yêu cầu.

## Câu hỏi còn mở

Kế hoạch có thể hoàn tất mà chưa cần chọn một journal cụ thể. Trước khi triển khai cần người dùng xác nhận runtime ưu tiên, phạm vi dùng riêng/phát hành, và bộ mẫu văn phong. Trước behavioral eval trả phí cần chốt runner/ngân sách; không tự lấy credential sẵn có làm đồng ý.
