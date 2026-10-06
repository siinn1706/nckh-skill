# Shortlist nguồn tài nguyên thật — không tự sinh dataset

As-of: 02/10/2026, Asia/Saigon. Phạm vi: nghiên cứu và lập plan; chỉ đọc upstream trong bộ nhớ, chưa nhập data, cài dependency hay chạy script upstream.

## Ràng buộc trực tiếp từ người dùng

Dataset không được tự bịa. Chọn tối đa ba nguồn skill mạnh, lấy phần đã tồn tại và phù hợp; có thể phối hợp có kiểm soát. Không tự sinh hàng, manuscript, citation, số liệu, nhãn gold hay đoạn mẫu để đạt quota. Giữ lịch sử 148 synthetic development cases với đúng nhãn diagnostic; không chuyển chúng thành dataset nguồn hoặc human gold.

Đây là **thứ tự ưu tiên khảo sát theo độ phù hợp**, không phải bảng xếp hạng chất lượng top 1–3 toàn cầu. GitHub stars chỉ là tín hiệu phổ biến; không thay thế đánh giá nội dung, tính đúng, provenance, consumer hoặc quyền tái sử dụng. Đã đối chiếu AgentKit đang cài; không đếm một bản tích hợp/biến thể của cùng upstream thành nguồn corroboration độc lập.

## Ba nguồn chọn lọc

Metadata sau lấy bằng GitHub API trong lượt này; mutable main đã được quy về full commit.

| Ưu tiên | Nguồn | Commit đã xác minh | Popularity snapshot / root license | Vai trò được đề xuất |
|---|---|---|---|---|
| 1 | [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | `154988403bb5a18e9d3c0ce4e6d5e2e4b184a298` | 47,299 stars; MIT, đã đọc LICENSE.md đúng commit | Scientific writing/evidence/visuals: registry và template có reader; chọn đúng study design và domain. Không nhập cả bộ. |
| 2 | [Nature Skills](https://github.com/Yuan1z0825/nature-skills) | `84880815fb37317b3766bff2c2abba395b8993c3` | 45,502 stars; Apache-2.0 tại commit này | Phương pháp viết, định tuyến reference và QA hình. Không biến hướng dẫn Nature thành quy định chung hay gán ví dụ minh họa là dữ liệu quan sát. |
| 3 | [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `09170eec67eefd46a7ae85de61b40c194020f997` | 132,353 stars; MIT, đã đọc LICENSE đúng commit | CSV lookup có nội dung cho frontend/UX và handoff Marketing phù hợp; không dùng làm scientific truth hoặc corpus tiếng Việt. |

AgentKit vẫn là đối tượng so sánh chính về consumer/runtime trong [report riêng](researcher-261002-0836-agentkit-resources.md). Anthropic skill-creator và Agent Skills specification là chuẩn tham khảo cách đóng gói/evaluate, không được tính là nguồn dataset thứ tư.

## Tài nguyên đã mở nội dung, không suy từ đuôi file

| Resource tại commit đã pin | Nội dung quan sát | Consumer upstream đã đọc | Giới hạn dùng trong NCKH |
|---|---|---|---|
| [K-Dense reporting_guidelines.json](https://github.com/K-Dense-AI/scientific-agent-skills/blob/154988403bb5a18e9d3c0ce4e6d5e2e4b184a298/skills/scientific-writing/assets/reporting_guidelines.json) | 15 records; mỗi record có official URL và source IDs; phân biệt study design, protocol, primary/extension | [select_reporting_guidelines.py](https://github.com/K-Dense-AI/scientific-agent-skills/blob/154988403bb5a18e9d3c0ce4e6d5e2e4b184a298/skills/scientific-writing/scripts/select_reporting_guidelines.py#L21) nạp registry; disclaimer không chứng nhận quality/compliance | Registry hướng dẫn, không phải dataset thực nghiệm. Phần lớn là health/clinical; chỉ chọn khi task thật khớp, không ép CONSORT/TRIPOD vào mọi nghiên cứu CS. Kiểm nguồn chính thức trước áp dụng. |
| [K-Dense publisher_profiles.json](https://github.com/K-Dense-AI/scientific-agent-skills/blob/154988403bb5a18e9d3c0ce4e6d5e2e4b184a298/skills/scientific-visualization/assets/publisher_profiles.json) | 8 profiles có sources, phase, scope, currency; Science là historical-live-access-blocked, ACS là legacy-2006-guidance | [export_plan.py](https://github.com/K-Dense-AI/scientific-agent-skills/blob/154988403bb5a18e9d3c0ce4e6d5e2e4b184a298/skills/scientific-visualization/scripts/export_plan.py#L16) đọc JSON; dòng 173–177 cảnh báo source currency | Snapshot hỗ trợ lập kế hoạch, không chứng nhận submission. Giữ venue/year/track/article-type/stage riêng; unknown hoặc stale không được promote. |
| [UI UX Pro Max ux-guidelines.csv](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/09170eec67eefd46a7ae85de61b40c194020f997/src/ui-ux-pro-max/data/ux-guidelines.csv) | 119 data rows; 10 cột: No, Category, Issue, Platform, Description, Do, Don't, Code Example Good/Bad, Severity | [core.py](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/09170eec67eefd46a7ae85de61b40c194020f997/src/ui-ux-pro-max/scripts/core.py#L45) khai báo cột tìm kiếm/đầu ra; dòng 363–382 đọc snapshot bằng DictReader | Knowledge/heuristic lookup, không phải empirical or human gold. Chọn đúng UI consumer, rà accessibility và ví dụ theo context; không mặc nhiên chấp nhận mọi severity/rule upstream. |
| [Nature writing manifest](https://github.com/Yuan1z0825/nature-skills/blob/84880815fb37317b3766bff2c2abba395b8993c3/skills/nature-writing/manifest.yaml) và references được nó định tuyến | Trong subtree writing/shared, structured resources quan sát là YAML manifests/agent metadata; không thấy CSV/JSON/JSONL corpus | SKILL.md nạp core rồi reference theo task, section, language, paper type, journal | Nguồn phương pháp bằng Markdown vẫn có giá trị. Không chuyển prose thành hàng data rồi gọi là dataset thực; ví dụ tác giả tạo phải giữ nhãn minh họa. |
| [K-Dense claim_evidence_template.csv](https://github.com/K-Dense-AI/scientific-agent-skills/blob/154988403bb5a18e9d3c0ce4e6d5e2e4b184a298/skills/scientific-writing/assets/claim_evidence_template.csv) | Header và một dòng placeholder TODO | Evidence workflow/template input | Chỉ là biểu mẫu, không có evidence dataset sẵn. Không tự điền bằng số liệu/citation do model nghĩ ra. |

Các file trên **tồn tại thật ở upstream**, nhưng điều đó không chứng minh từng nội dung là sự thật khoa học, do người viết, đã được human review hay phi-synthetic. Nhãn nguồn phải phản ánh điều đã biết; không tự suy ra gold từ tên repo, stars hoặc README marketing.

## Hash bytes đã đọc

SHA-256 tính trực tiếp từ bytes giải mã GitHub contents API, không phải Git blob ID:

| Resource | SHA-256 |
|---|---|
| K-Dense reporting_guidelines.json | `215f8c55bd40bda0569f2e81556030ff575319e25276b1e1ae70e2cc7475ddcd` |
| K-Dense publisher_profiles.json | `1e1b1b5a4e0e3dfc57877f2abf1e96888fe6b65617234b078f193b8f76e0ebe9` |
| UI UX Pro Max ux-guidelines.csv | `ff81ec613f70ba9fc3fcce52dbe4ae35d44b2079dbe6dc066d2d6e38c28facd5` |

Không chạy reader upstream của ba resource này; chỉ đọc code và parse JSON/CSV trong bộ nhớ. AgentKit CSV reader đã được smoke riêng, không được gán kết quả đó cho phiên bản upstream hoặc NCKH.

## Quy tắc lấy và phối hợp

1. Mỗi tài nguyên/record giữ repo, full commit, path, file hash, locator/record ID, loại dữ liệu, ngôn ngữ, domain và rights status. Quyền ở root là điểm khởi đầu; kiểm LICENSE/NOTICE/nguồn nhúng theo file trước redistribution.
2. Chỉ phối hợp sau khi có consumer, schema và mục đích chung. Ưu tiên các nguồn tách namespace cùng một catalog, không ép clinical guideline, UI heuristic và Nature prose thành một bảng đồng nhất.
3. Dedupe bằng stable source key/content fingerprint; ghi mọi chuyển đổi và mapping về bản gốc. Hai bản copy cùng nguồn không được tính hai bằng chứng độc lập. Conflict để riêng cùng provenance, không lấy trung bình hoặc tự chọn cho đẹp.
4. Dịch/chú giải được ghi là transformation có reviewer; không tự gán bản dịch là nguyên bản người Việt hoặc human-gold. Không sinh thêm record thiếu để đủ số lượng.
5. Với ví dụ viết VI/EN: chưa xác minh corpus mẫu thực có quyền ở shortlist. Giữ gap rõ, chọn artifact thật upstream hoặc tài liệu người dùng cấp quyền ở bước thực thi; không thay bằng dataset bịa.
6. Ca kiểm thử tổng hợp lịch sử chỉ dùng chẩn đoán/hồi quy với nhãn cũ. Dataset/corpus mới phải từ nguồn thật hoặc user-supplied; fixture biên kỹ thuật muốn tạo thêm phải được xin duyệt và tách khỏi dataset/chất lượng khoa học.
7. Chưa nhập dataset, chưa sửa source-lock hay installed skills. Nếu thiếu quyền, reader hoặc domain fit, giữ `not-packaged`/pending, không tìm cách làm cho checkbox xanh bằng data tự tạo.

## Quyết định còn mở

- Shortlist được đề xuất, chưa phải authorization để import hoặc công nhận top thế giới.
- Chưa có corpus VI/EN thực phù hợp, rights-cleared và reviewer người thật; đây là gate cho taste/scientific acceptance.
- Consumer/closure, per-file rights và matched evaluation phải được kiểm ở các phase triển khai; không suy từ bytes/hash hoặc số record.
