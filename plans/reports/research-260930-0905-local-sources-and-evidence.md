# Nguồn gốc, bằng chứng và giới hạn của bộ skill cá nhân

Ngày đối chiếu: 30/09/2026, múi giờ Asia/Saigon. Đây là nghiên cứu phục vụ kế hoạch; chưa tạo, cài hay đánh giá hiệu quả bộ skill mới.

## Kết luận

Nên tạo một bộ skill có lõi bằng chứng nhỏ, các năng lực viết/nghiên cứu độc lập và hồ sơ quy chuẩn nạp theo nhiệm vụ. AgentKit cung cấp quy trình, quản lý phạm vi và cách đánh giá; blueprint cung cấp hạt nhân văn phong tiếng Việt; ZIP cung cấp kinh nghiệm cộng tác với mentor. Không nguồn nào trong số này được dùng làm quy chuẩn khoa học phổ quát.

## 1. Hợp đồng công việc

- **Đầu ra:** nghiên cứu có truy xuất nguồn; ma trận giữ/sửa/không lấy; kiến trúc đề xuất; kế hoạch chia phase, kiểm thử và điều kiện nghiệm thu.
- **Ràng buộc:** chỉ lập kế hoạch; giữ cả năm mục tiêu người dùng; quy chuẩn journal/conference phải được chọn khi dùng; ưu tiên nguồn chính chủ; không hứa loại bỏ hoàn toàn ảo giác.
- **Ngoài phạm vi lượt này:** viết/cài skill, cài extension, chỉnh cấu hình toàn cục, chạy mô hình/API trả phí, làm slide/ảnh mẫu, huấn luyện mô hình, đăng kho công khai hoặc nộp bài.
- **Nghiệm thu lượt lập kế hoạch:** mỗi nguồn người dùng đưa có trạng thái đọc; nguồn bổ sung có lý do chọn; quy tắc bằng chứng và cách ly venue cụ thể; plan index ngắn, phase đầy đủ; liên kết và cấu trúc được kiểm tra. Chất lượng sản phẩm tương lai chỉ được xác nhận sau đánh giá thực tế.
- **Điểm dừng goal:** giao bộ tài liệu kế hoạch đã kiểm tra và nêu rõ lựa chọn còn chờ người dùng, không tự chuyển sang triển khai.

## 2. Phạm vi đã đọc

| Nguồn | Phạm vi đọc trực tiếp | Dấu vết phiên bản |
|---|---|---|
| `vietnamese-writing-research-skills-blueprint.md` | Toàn bộ 1.368 dòng, gồm 28 mục; giữ nguyên file gốc | SHA256 `0E54218DBBB56B0C06A34B17854573C7DE8CBD7371321219945847F2A3811F8F` |
| `C:/Users/USER/Downloads/nckh-quy-chuan-skill.zip` | Toàn bộ 3 entry: `SKILL.md`, `scripts/build_check.sh`, `scripts/p3_invariants_check.py`; đọc trong bộ nhớ, không chạy | SHA256 `2AF342582DCC2F9053A94B63FE3EA854B6E367F9492D19C4BC21727F609EB441` |
| AgentKit engineer | Toàn bộ manifest bản cache cho Codex: 103 skill export; đọc sâu các module liên quan ở mục 4 | CLI 2.19.0, kit manifest 0.2.0 |
| AgentKit marketing | Toàn bộ manifest bản cache cho Codex: 82 skill export, có phần trùng engineer; không cộng thành số skill duy nhất | CLI 2.19.0, kit manifest 0.2.0 |
| Runtime skill catalog | Kiểm kê metadata 169 thư mục có `SKILL.md` cấp đầu tại `.agents/skills`; gồm cả kỹ năng ngoài AgentKit | Snapshot tại thời điểm nghiên cứu; không khẳng định đã đọc sâu tất cả |
| PaperPop | Trang Chrome Web Store của tác giả, bản 1.8.5 cập nhật 19/08/2026; trang chủ chỉ trả HTML không có nội dung đọc được | Chỉ xác minh mô tả sản phẩm, chưa cài/thử extension |
| Unpaywall | Nội dung lập chỉ mục của trang sản phẩm, FAQ và data-format chính chủ | Mở trực tiếp một số URL chỉ nhận trang cần JavaScript; không coi đó là thử API |

Nguồn `nature-skills` và các kho bổ sung được ghi riêng trong hai báo cáo nghiên cứu cùng thư mục. Mỗi báo cáo phân biệt đọc toàn bộ với đọc chọn lọc; không coi README là bằng chứng các tính năng đã chạy thành công.

Manifest AgentKit đã đọc tại `C:/Users/USER/.agentkit/cache/kits/{engineer|marketing}/codex/2.19.0/{engineer|marketing}/kit.yaml`. Những bản cache cũ không được dùng thay cho bản này. Nội dung skill đang thực sự áp dụng được đọc từ `C:/Users/USER/.agents/skills/` theo đường dẫn người dùng chỉ định.

## 3. Blueprint: giữ hạt nhân, sửa các giả định chưa được đo

Giữ sự tách biệt đọc nguồn, rút bằng chứng, lập luận, viết, phản biện và đánh bóng câu chữ. Giữ quy tắc không nâng mức chắc chắn; không bịa DOI, số trang, lời trích hay câu thơ; giữ thuật ngữ nhất quán và phân biệt quan sát văn bản với diễn giải.

Các điều chỉnh cần đưa vào thiết kế:

1. Không biến 16 tên năng lực thành 16 skill bắt buộc. Có thể gom chức năng gần nhau thành chế độ, nhưng vẫn giữ vai trò và đầu ra kiểm chứng riêng.
2. `verified: true` là quá thô. Tồn tại nguồn, khớp metadata, đã đọc toàn văn, độ đúng lời trích, nguồn hỗ trợ claim, tình trạng đính chính/rút bài và điều kiện Q1/Q2 phải là các trường riêng.
3. `Taste score` là nhận xét theo rubric, không phải số đo khách quan hay máy phát hiện AI. Cần cặp bài ẩn danh và người dùng chấm; tự chấm chỉ là tín hiệu chẩn đoán.
4. Không khẳng định cấu trúc object chắc chắn “giảm hallucination đáng kể” trước khi có đối chứng. Đây là giả thuyết thiết kế cần đo.
5. Đối với nguồn không có trang, dùng locator ổn định như mục, đoạn, dòng, chương hoặc timestamp. Không bịa số trang chỉ để thỏa điều kiện trích trực tiếp.
6. Bổ sung viết học thuật tiếng Anh, chuyển ngữ bảo toàn ý, slide chỉnh sửa được, hình khoa học và hồ sơ venue; blueprint chưa bao phủ đầy đủ các mục này.
7. Giữ nhánh văn học: văn bản gốc, ấn bản, người dịch/biên tập, đoạn hoặc câu cụ thể, giới hạn so sánh. Không ép sách, văn bản cổ hoặc nguồn sơ cấp vào thang Q1/Q2 của tạp chí; khi chính sách strict không cho phép ngoại lệ, hỏi và dừng chấp nhận nguồn đó.

## 4. AgentKit: phần nên kế thừa

Đây là đối chiếu nguồn, không phải yêu cầu chạy toàn bộ các workflow dưới đây.

| Module đã đọc | Phần có giá trị | Điều phải sửa hoặc không mang sang |
|---|---|---|
| `ak-plan`, `ak-brainstorm`, `ak-xia` | Hợp đồng đầu ra; nghiên cứu trước khi sao chép; quyết định có căn cứ; phase độc lập | Không ép mọi sửa câu ngắn chạy chuỗi lập kế hoạch dài; không tự triển khai sau plan |
| `ak-research`, `ak-docs-seeker` | Nguồn chính chủ, phiên bản, bất đồng và điều kiện dừng tìm kiếm | Nghiên cứu giải pháp kỹ thuật không đồng nghĩa systematic review khoa học |
| `ak-fable-thinking` và `research-taste.md` | Phân biệt quan sát, suy ra, kiến thức cũ, giả định; tìm bằng chứng phản bác | Các mô tả ưu thế mô hình trong tài liệu không phải benchmark đã kiểm chứng ở dự án này |
| `ak-fable-thinking/references/content-taste.md` | Chọn người đọc/xưng hô; tránh dịch máy; giữ giọng tác giả; sửa nhỏ có kiểm tra dữ kiện | Danh sách sáo ngữ là heuristic, không phải cấm từ tuyệt đối; văn học không phải đoạn nào cũng cần số liệu hay câu mở kiểu báo cáo |
| `ak-copywriting` và `references/writing-styles.md` | Các chiều giọng, nhịp, từ vựng; tách trích xuất phong cách khỏi nội dung | Không đưa AIDA/PAS, CTA, urgency, “bold claims” vào bài NCKH; ví dụ số liệu marketing không phải bằng chứng |
| `ak-brand` | Hồ sơ giọng cá nhân và tính nhất quán | Không kéo cả chiến dịch, tracking và brand-token machinery vào bộ viết văn |
| `ak-write` | Phân luồng viết mới/chỉnh sửa/audit | Không nhầm “publish-ready” với đã xuất bản; không áp SEO lên paper |
| `ak-slides` | Kể chuyện bằng slide, phân cấp, biểu đồ có dữ liệu | Skill này xuất HTML; không được giao HTML rồi gọi là PPTX |
| `ak-diagram` | Graph có cấu trúc, luồng dữ liệu, SVG/HTML xác định được | Cam kết hình không chồng lấp trong nguồn chưa được chạy lại; đồ thị đúng layout chưa chứng minh đúng khoa học |
| `ak-ai-multimodal`, `ak-ai-artist` | Chọn công cụ theo khả năng, nguồn ảnh, kiểm soát provider | Không ép mọi sơ đồ thành ảnh sinh; không giữ tên model/pricing cũ; không xem khóa có sẵn là đồng ý gửi bản thảo ra ngoài |
| `ak-skill-creator` và `references/testing-and-iteration.md` | So sánh không-skill/gốc/ứng viên; tách routing, chất lượng, chi phí; holdout; consumer độc lập | Lint hay validator không chứng minh skill tốt hơn; dùng rubric học thuật/văn phong phù hợp thay bộ đo code |
| `ak-autoresearch` | Thay một biến, đo, giữ/bỏ; giới hạn vòng và điều kiện dừng | Chưa có metric/baseline thì không chạy vòng vô hạn; chưa được phép thì không gọi provider |
| OpenAI `skill-creator` cài sẵn | Progressive disclosure; metadata phân biệt intent; không đưa mẹo chung dài dòng vào skill | Không sao chép đường dẫn/runtime riêng thành phụ thuộc bắt buộc |

Các SHA256 mẫu của entrypoint đã đọc: `ak-plan` = `81DF1AB9FB73A0A90CFD8DEF643C3B856C12CD59DEF78D9014B329D134620813`; `ak-skill-creator` = `9ECF4F18E83EA346EAD065960716C06E30D6E48F27317085BECE7DCF64E01D18`; `ak-copywriting` = `79A86C11A416783A360FA70028B5C526E202BB2E31144017A179E60EBA41E9FE`; `ak-slides` = `0D68B142993A99B50A52B823ADB6E2AB60E7FD7DECC7EF0C292D15611706BE50`; `ak-fable-thinking` = `1DD4579C3BF144BCFA190BE7E66310BFB43A690E7EFF88AAE12EE8724530A422`.

Hai manifest có `tier: paid`; một số skill ghi MIT, skill-creator ghi Apache-2.0 và MIT, các mục khác có điều khoản riêng. Không suy ra quyền phát hành lại toàn bộ kit từ quyền sử dụng hoặc từ một frontmatter. Kế hoạch cần khóa provenance và đọc license cấp file trước mọi sao chép/phân phối. Ưu tiên dùng qua capability đang cài hoặc viết adapter/hướng dẫn gốc; không đóng gói lại cả bộ.

## 5. ZIP: tách kinh nghiệm dùng chung khỏi quy tắc một paper

| Phân loại | Nội dung | Quyết định |
|---|---|---|
| Dùng chung có điều kiện | Làm trên bản mới nhất; giữ bản chính; vùng mentor bảo vệ; diff; không tự đổi kết quả; báo việc chưa làm | Đưa vào hợp đồng chỉnh sửa và cộng tác |
| Hồ sơ dự án riêng | MAPR2026, Byzantine/FL, đúng ba thuật toán, đúng caption, thứ tự subsection, từ cấm, năm 2025–2026, loại trừ nhà xuất bản/tạp chí | Chỉ lưu thành profile do người dùng chọn, không thành mặc định |
| Hồ sơ trình bày riêng | `align*`, không DOI/URL trong BibTeX hiển thị, mỗi citation một lần ở p3, abstract một đoạn, conclusion ba đoạn | Không gọi đây là quy chuẩn IEEE chung; giữ DOI trong sổ nguồn dù renderer có ẩn |
| Không kế thừa | Không tìm được nguồn thì xóa citation nhưng giữ nguyên câu có vẻ là sự thật | Phải hạ claim, ghi chưa xác minh hoặc xin nguồn; không rửa claim bằng cách bỏ citation |
| Không kế thừa làm chân lý | Hình/văn luôn đúng, code không được dùng làm căn cứ | Bảo toàn phạm vi tác giả cho phép, nhưng ghi riêng xung đột giữa dữ liệu, code, hình và văn; không xác nhận kết quả chưa kiểm |
| Không kế thừa làm kiểm định thống kê | So chênh lệch trung bình với độ lệch chuẩn rồi kết luận vượt trội | Cần thiết kế thực nghiệm, effect size, uncertainty và phép kiểm phù hợp; không suy p-value từ hình |

Mâu thuẫn đã đọc trực tiếp: phần cấu trúc p3 và `SUBSECTION_ORDER` vẫn có “Algorithm Analysis”, trong khi đoạn quy tắc mới yêu cầu bỏ subsection riêng này. Đây là test case tốt cho conflict detection, không phải tiêu chuẩn được tự động chọn bên thắng.

`build_check.sh` xóa đệ quy đường dẫn đầu ra do đối số cung cấp, không kiểm containment, dùng thư mục tạm cố định và không có fail-fast đáng tin cậy cho toàn chuỗi build. Không chạy hay chuyển nguyên script này. `p3_invariants_check.py` phụ thuộc tên file/caption/hằng số của đúng paper; việc báo ALL INVARIANTS PASS chỉ có ý nghĩa cho tập regex đó, không chứng minh trích dẫn đúng hay paper hợp lệ.

Không có entry LICENSE trong ZIP. Được dùng tài liệu người dùng đưa để phân tích không có nghĩa đã xác định quyền công bố lại.

## 6. PaperPop, Scholar, Unpaywall: ba vai trò khác nhau

- [PaperPop trên Chrome Web Store](https://chromewebstore.google.com/detail/pdmgonafkgopgipcmgfpfobgknbofnpn?hl=en) mô tả hiển thị nhiều bảng xếp hạng, sort/export, tóm tắt AI và mind map. Dùng nhãn hiển thị làm đầu mối kiểm tra, không làm bằng chứng tối hậu về quartile, chất lượng bài hoặc nội dung. Phần mô tả quyền riêng tư là tuyên bố của nhà phát triển, chưa được kiểm toán trong lượt này. Không tự cấu hình đường dẫn download bên thứ ba.
- [Google Scholar](https://scholar.google.com/intl/en-gb/scholar/about.html) tìm nhiều dạng tài liệu, không chỉ bài tạp chí peer-reviewed. Dùng để khám phá/snowballing; lưu query, ngày, phạm vi và lý do chọn, rồi mở nguồn gốc. Không suy peer review hay Q1/Q2 từ việc xuất hiện trên Scholar.
- [Unpaywall](https://unpaywall.org/products/extension) và [FAQ](https://unpaywall.org/faq) hỗ trợ tìm bản truy cập hợp pháp. Theo [data format](https://unpaywall.org/data-format), các location có thể khác phiên bản và license. Phải giữ DOI, host, phiên bản, URL, quyền sử dụng; bản đọc miễn phí không mặc nhiên cho phép đóng gói toàn văn vào repo.

Không cài extension trong lượt này, không scrape Scholar vượt kiểm soát truy cập, không vượt paywall. Có thể hỗ trợ người dùng xuất metadata rồi nhập vào luồng kiểm chứng ở giai đoạn triển khai.

## 7. Hợp đồng độ tin cậy đề xuất

Tách ba quyết định: nguồn đủ điều kiện theo chính sách; đoạn nguồn hỗ trợ phát biểu; phát biểu được diễn đạt với mức chắc chắn phù hợp. Một paper Q1 vẫn có thể không hỗ trợ câu đang trích.

Một hồ sơ nguồn tối thiểu có định danh/metadata, loại tài liệu, phiên bản, đường dẫn hoặc hash bản đã đọc, mức truy cập `metadata-only | abstract-only | full-text`, locator, evidence excerpt, ngày kiểm, license và trạng thái cập nhật. Một claim có evidence IDs, loại quan sát/diễn giải/suy luận, tình trạng hỗ trợ/mâu thuẫn/chưa rõ, giới hạn và câu chữ được phép. Không dùng một điểm confidence duy nhất thay cho các trường này.

Crossref cung cấp [metadata](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) và [dữ liệu Retraction Watch](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/). Metadata khớp chỉ xác minh danh tính nguồn. Kiểm cả notice, quan hệ cập nhật và trang publisher; không tìm thấy record rút bài không phải bằng chứng không có rút bài. Mất mạng hoặc chỉ có abstract phải được thể hiện trong báo cáo.

Q1/Q2 của người dùng được giữ dưới dạng chế độ journal-strict. Khi chưa biết hệ thống, hỏi JCR hay SJR, category, metric/data-year và cách chọn năm trước khi chấp nhận nguồn bằng quartile. [Clarivate](https://clarivate.com/academia-government/blog/a-primer-on-ties-in-the-jcr/) xác nhận một tạp chí có thể có quartile khác theo category. Không trộn JIF quartile, JCI, CiteScore, SJR, CAS hoặc hạng conference. SCImago trả 403 trong lần mở trực tiếp, vì vậy chưa xác minh được một quartile cụ thể và không suy đoán giá trị nào.

Sách, nguồn sơ cấp, preprint, conference và nguồn nền tảng cũ cần chính sách riêng do người dùng chấp nhận; không âm thầm nới “chỉ Q1/Q2”. Với thông tin ngoài NCKH, ưu tiên nguồn official đúng chủ đề và thời điểm; vẫn phân biệt dữ liệu thực nghiệm với lời quảng bá của chủ thể.

## 8. Cách ly venue và an toàn hình khoa học

Profile phải khóa `venue_id`, loại venue, năm/phiên bản hướng dẫn, track hoặc article type, giai đoạn submission/revision/camera-ready, nguồn official và ngày kiểm. Một đầu ra chỉ dùng một profile đích; hồ sơ bài gốc chỉ là dữ liệu chuyển đổi, không phải quy tắc đang hoạt động. Chưa có venue thì hỏi; nếu người dùng muốn nháp không theo venue, gắn nhãn generic và không tuyên bố compliant.

Quy tắc mentor nằm trong project overlay riêng. Xung đột với yêu cầu nộp bài hoặc tính trung thực phải được báo; không dùng “user mới nhất thắng” để biến sai khoa học thành đúng hoặc tuyên bố vẫn tuân thủ venue.

Phân biệt biểu đồ từ dữ liệu, sơ đồ cơ chế và tranh minh họa. Biểu đồ dùng dữ liệu thật và giữ đơn vị/uncertainty. Sơ đồ cần kiểm topology, nhãn, ký hiệu và xuất nguồn chỉnh sửa được. Ảnh sinh có thể dùng cho minh họa khi được phép, không đại diện quan sát/thí nghiệm chưa diễn ra. Chính sách AI/ảnh phải lấy từ venue đang chọn. [Trang chính sách Nature Portfolio](https://www.nature.com/nature-portfolio/editorial-policies) là điểm vào; URL AI và initial submission bị chuyển hướng không đọc được trong lần kiểm, nên không đóng cứng quy tắc hiện hành từ một editorial cũ. Trang IEEE liên quan cũng không đọc trực tiếp được; profile tương ứng phải để pending cho đến khi có bản official kiểm chứng được.

## 9. Rủi ro và phương án

| Cách ghép | Giả định chịu lực | Điểm hỏng đầu tiên | Kết luận |
|---|---|---|---|
| Fork nguyên nature-skills rồi chép AgentKit vào | Quy tắc/phụ thuộc/license tương thích | Context phình, venue lẫn, cập nhật khó, quyền sao chép chưa rõ | Không khuyến nghị làm nền runtime mặc định |
| Cài nhiều bộ độc lập và thêm router | Runtime tự chọn đúng giữa nhiều mô tả trùng | Nhiều skill cùng xử lý prose/citation, chất lượng không đo được | Hữu ích để tham khảo/đối chứng, không giải quyết hết yêu cầu |
| Bộ riêng gọn, chọn module và adapter theo khả năng | Có đủ nguồn được phép dùng và bộ đánh giá thật | Thiếu corpus giọng Việt hoặc verifier đọc nguồn chưa tốt | Khuyến nghị; có thể thay từng module, ít ràng buộc nguồn |

Đây là đề xuất thiết kế, chưa được người dùng duyệt để triển khai. Cải thiện so với ý tưởng clone toàn kho là giữ source lock để tham khảo, viết hợp đồng chung và chỉ đưa phần được kiểm chứng/được phép vào runtime. Chi phí đổi hướng là thêm bước mapping/license/eval; đổi lại không phải bảo trì một bản hợp nhất khổng lồ.

## 10. Giới hạn thao tác và kiểm tra

`ak skills list --kit engineer/marketing --json --no-interactive` trả danh sách rỗng; `ak kit list-kits` mặc định thất bại vì workspace không có `./kits`. Đã tìm đúng cache và đọc hai manifest bằng `--kits-dir`; không sửa cài đặt. Lệnh kiểm kê này không phải kiểm thử hành vi skill. Workspace ban đầu chỉ có blueprint; không có README/docs/source/tests để kế thừa và không tự tạo kiến trúc sản phẩm từ tên thư mục.

## Câu hỏi còn mở

Khi triển khai cần xác nhận runtime ưu tiên, ví dụ văn phong người dùng được quyền cung cấp và môi trường đánh giá. Khi sử dụng skill cho bài cụ thể mới hỏi venue, hệ quartile/category/year và ngoại lệ nguồn; không hỏi một venue duy nhất cho toàn bộ bộ skill.
