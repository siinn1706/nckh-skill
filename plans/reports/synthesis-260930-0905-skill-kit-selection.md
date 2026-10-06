# Tổng hợp lựa chọn: lớp skill cá nhân trên nền AgentKit

Ngày 30/09/2026, Asia/Saigon; cập nhật sau lượt duyệt 11 chỉnh sửa. Chỉ nghiên cứu và lập kế hoạch; chưa triển khai. Bản này bao gồm các bổ sung trực tiếp: giữ cập nhật AgentKit qua wrapper; instructions English; plan/cook tự chọn skill; hooks/subagents có kiểm soát; official rule cards và budget context 20k–40k / 10%–20%.

## 1. Phương án ưu tiên

**Không gộp nguyên nhiều bộ prompt. Xây lớp điều phối và tiêu chuẩn riêng, dùng upstream như các năng lực thay thế được.** AgentKit tiếp tục được maintainer cập nhật; bộ cá nhân chịu trách nhiệm lựa chọn phiên bản tương thích, giữ brief/venue/style/evidence và quyết định nhận hay trả sửa đầu ra.

Hai entrypoint `research-plan` và `research-cook` bao quanh 10 module chuyên môn trong [hợp đồng thiết kế](brainstorm-260930-0905-skill-kit-contract.md). Đây là tên dự kiến, chưa phải lệnh đã cài. Module viết/đọc/visual có thể là adapter mỏng; chỉ viết mới phần còn thiếu, nhất là gu Việt và kiểm chứng xuyên nguồn.

Người dùng không cần gọi từng module. `listskill` là discovery nội bộ từ live
catalog: match capability/từ liên quan VI/EN, shortlist, đọc đúng instructions,
ghi route vào plan; cook revalidate rồi thực hiện. Tag thủ công là tùy chọn,
không thay quyền hay bỏ gate. Không phát minh thêm một CLI `skill-listskill`.

`SKILL.md`, metadata, quy tắc và adapter instructions của bộ tương lai dùng **English**. Bản mẫu tiếng Việt và nguyên văn nguồn giữ ngôn ngữ gốc. Đầu ra do `output_language` và audience/style profile quyết định, không do ngôn ngữ prompt của skill. Tài liệu kế hoạch hiện tại dùng tiếng Việt để duyệt.

```text
research-plan -> kế hoạch + profile + quyền sử dụng -> người dùng cho phép thực hiện
                                                           |
                                                     research-cook
                                                           |
                           resolve skill -> gọi worker -> nhận artifact/receipt
                                                           |
                                          evidence / fidelity / visual review
                                              |                       |
                                           bàn giao             sửa hữu hạn / dừng
```

Lập plan không tự cấp quyền cook. Cook không tự cài skill, upload bản thảo, trả phí, commit, đăng bài hay nộp journal. Không thể dùng điểm tự chấm của writer để tự thông qua mọi bước.

## 2. Nguồn nào đóng góp phần nào

Đây là xếp ưu tiên theo **phù hợp với mục tiêu**, không phải bảng chứng minh “skill tốt nhất thế giới”. Mức nổi tiếng, badge official hoặc README tự nhận chất lượng không thay thế benchmark trên dữ liệu của người dùng.

| Nguồn | Phần giữ lại | Cách tích hợp ưu tiên | Điều không mang sang |
|---|---|---|---|
| AgentKit engineer + marketing | Plan/contract, research, critique, voice dimensions, diagram, eval và maintenance | **Gọi bản đang cài đã được chấp nhận** qua adapter; không phân phối lại paid kit | Mặc định coding cho prose; AIDA/CTA/SEO cho khoa học; HTML giả làm PPTX |
| [nature-skills](https://github.com/Yuan1z0825/nature-skills) | Reader anchors, source ledger, polishing giữ ý, citation/data/statistics gates, paper-to-PPTX và figure QA | Gọi module tương thích hoặc adapt từng phần có phép; pin nguồn đã xem | Chinese/Nature/CNS defaults, tự động chấm chất lượng bằng rank, cron và asset chưa rõ quyền |
| [K-Dense scientific-writing](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md) và citation-management | Claim–evidence binding, uncertainty, source/metadata audit, human accountability | Chọn lọc contract; worker chỉ khi đáp ứng confidentiality và human gates | Không nạp toàn bộ collection; không coi citation đúng là claim đúng |
| [Orchestra presenting-conference-talks](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/main/20-ml-paper-writing/presenting-conference-talks/SKILL.md) | Storyboard/talk script/speaker notes; hướng PPTX chỉnh sửa được và Beamer | Bổ sung cho nature-paper2ppt + engine native | Không universal hóa quy tắc ML/systems hoặc màu gợi ý thành quy định hội nghị |
| OpenAI runtime skills; [public skills catalog](https://github.com/openai/skills) | Skill authoring, xử lý artifact native, render/inspect và khả năng tích hợp sẵn có | Gọi qua runtime nếu có; license theo đúng package/file | Không nhầm catalog GitHub với mọi plugin cài cục bộ; không copy mặc định |
| [OpenAI visualization plugin](https://github.com/openai/plugins/tree/main/plugins/build-web-data-visualization) | Tham khảo model/geometry, provenance và regeneration contract | Reference-only cho các path chưa chốt license | Không suy diagram phần mềm đúng nghĩa là đã kiểm cơ chế khoa học |
| [Anthropic skills](https://github.com/anthropics/skills), [official plugins](https://github.com/anthropics/claude-plugins-official) | Tham khảo packaging, progressive disclosure, workflow native trong môi trường được phép | Đối chiếu khả năng; không nhập nội dung Office vào bundle riêng | [PPTX LICENSE](https://github.com/anthropics/skills/blob/main/skills/pptx/LICENSE.txt) có điều khoản riêng hạn chế sao chép/derivative/distribution; không suy mọi file Apache-2.0 |
| [Trussary Vietnamese](https://github.com/trussary/vietnamese-language-skill) | Register, locale và thuật ngữ kỹ thuật | Tham khảo/chọn lọc phần MIT đã kiểm; confidence về adoption còn hạn chế | Không coi generic technical Vietnamese là giọng riêng hoặc quy chuẩn cho văn học |
| [blader/humanizer](https://github.com/blader/humanizer) | Phát hiện câu rập khuôn và edit giữ nội dung | Heuristic phụ cho critic, không phải lõi | Không AI-detector, không cam kết bypass detector, không thay taste corpus |
| [PaperPop](https://chromewebstore.google.com/detail/pdmgonafkgopgipcmgfpfobgknbofnpn?hl=en), [Scholar](https://scholar.google.com/intl/en-gb/scholar/about.html), [Unpaywall](https://unpaywall.org/products/extension) | Discovery/rank hints, tìm nguồn, truy cập OA hợp pháp | Nguồn metadata/đường truy cập tùy chọn; không cần cài extension để có core | Badge không chứng minh Q; bản miễn phí không chứng minh quyền phân phối |
| Blueprint và ZIP của người dùng | Tách đọc–nghĩ–viết–audit; gu Việt; mentor/protected-region/minimal-diff | Blueprint làm requirements; ZIP làm dữ liệu để tách project overlay | Không lấy MAPR/FL, thuật toán/caption/năm nguồn hay script xóa thư mục làm luật chung |
| [STORM](https://github.com/stanford-oval/storm), [PaperQA2](https://github.com/Future-House/paper-qa) | Đối chứng phương pháp cho question/outline hoặc evidence retrieval | Reference; worker tùy chọn nếu có nhu cầu và quyền thật | Không gọi đây là bộ Agent Skills; không đưa cả stack vào mặc định |

K-Dense đã đổi tên repository từ `claude-scientific-skills` sang `scientific-agent-skills`; URL cũ redirect tới kho mới tại lần kiểm. Nhãn “official” chỉ dùng cho kho do chính tổ chức tương ứng quản lý; nature, K-Dense, Orchestra và các nguồn cá nhân không phải bộ do OpenAI/Anthropic phát hành.

## 3. Giữ cập nhật upstream mà vẫn tái lập được

Không cần fork toàn AgentKit để có version control. Bộ cá nhân lưu **bản đã resolve trong lượt chạy** và **bản đã được đánh giá tương thích**, gồm kit/skill version, hash instruction/dependency closure, runtime và các profile dùng cho task.

1. Resolve đúng capability trong catalog thật. Thiếu, trùng tên hoặc đổi tên thì báo rõ; không dùng đường dẫn tuyệt đối trên máy tác giả làm hợp đồng portable.
2. So version/hash với bản đã chấp nhận. Bản mới là candidate, chưa mặc nhiên tương đương bản cũ.
3. Kiểm thay đổi liên quan: instructions, references/scripts, output format, provider, quyền upload, vòng gọi và chi phí.
4. Đánh giá lại capability bị ảnh hưởng trên bộ kiểm development đã khóa. Candidate đạt gate mới được đánh dấu accepted; regression giữ pending.
5. Nếu cần rollback, dùng bản accepted còn sẵn và được phép giữ hoặc fallback đã kiểm. Không hạ cấp/copy/sửa global installation của người dùng; không giả có bản cũ nếu snapshot không tồn tại.

Không dựng updater/watcher riêng trong phạm vi mặc định. Chính sách cập nhật AgentKit do người dùng quản lý; kit cá nhân chỉ phát hiện drift và ngăn nhận sai chất lượng. Vì instruction tiếng Anh hoặc prompt version không bảo đảm hiệu quả, phải đo cả đầu ra cuối.

### Hooks, subagents và context/cost

[Thiết kế chi tiết](../260930-0905-vietnamese-research-skill-kit/design-routing-hooks-cost.md)
chọn guard deterministic trước semantic review, hook đúng capability host, subagent
chỉ cho phần việc/check riêng và một controller giữ quyền, file ownership, budget.
Không gọi model sau mọi tool call; hook reminder không được nhận là sandbox.

Skill context gồm catalog/instructions/references/hook/delegate và phần kế thừa:
soft `min(20k, 10% W)`, hard `min(40k, 20% W)`. Shared pool không nhân theo số
agent; từng context cũng phải đạt trần riêng. Không truncate mandatory rules,
không dùng cache để xóa token khỏi phép đếm. Host/window/tokenizer chưa đo được
thì không certify budget compliance.

Tối ưu cost trên task **accepted đủ scope và quality**, tính controller, agents,
retry, tools/image và verification. Money/time budget là trường riêng, chốt trước
execution; subscription quota khác hóa đơn API. Chưa có số đo savings.

## 4. Các ranh giới không thể gộp

- **Plan/cook:** planned khác approved-for-execution, artifact-created khác accepted; resume phải khớp input/profile/dependency. `ak-cook` hiện thiên về code nên không phải drop-in engine cho paper.
- **Evidence:** metadata, access, quote, entailment, corrections/retractions và source eligibility là các trạng thái khác nhau. Không có bằng chứng phải còn trạng thái chưa xác minh.
- **Q1/Q2:** giữ journal-strict theo lựa chọn người dùng. Phải biết hệ, category, metric-year và evidence. Conference/book/primary literary text cần chính sách riêng được cho phép; không tự tạo “Q1 conference”.
- **Venue:** một profile đích theo venue/year/revision/track/type/stage. Reporting checklist theo study design là lớp khác, project/mentor là overlay khác; conflict phải báo. Không lấy union tất cả quy tắc.
- **Language/taste:** English instruction không ép English output; gu cá nhân cần ví dụ có quyền dùng và người dùng đánh giá. Không dùng linter hoặc model tự chấm làm human gold.
- **Visuals:** chart từ dữ liệu, scientific mechanism diagram và artwork khác nhau. PPTX/SVG/native objects phải đúng mức editability đã hứa; ảnh AI không đại diện dữ liệu thực nghiệm.
- **Standards:** [20 nhóm lỗi và rule cards](../260930-0905-vietnamese-research-skill-kit/standards-and-failure-catalog.md) tách kit integrity, study/reporting, venue và writing heuristic. ICMJE/COPE/Crossref/ASA/DORA không biến thành một format chung; Harvard/UNC/Purdue/Manchester không quyết định gu Việt của người dùng.

## 5. Phần đã biết và phần chưa biết

Đã đọc toàn blueprint và ba entry trong ZIP; kiểm toàn manifest engineer/marketing và đọc sâu nhóm skill liên quan; đọc chọn lọc nguồn chính chủ theo manifest của các báo cáo. Không khẳng định audit toàn bộ mọi collection hoặc thử thực thi tính năng được README mô tả.

Revision nature đã ghim: `84880815fb37317b3766bff2c2abba395b8993c3`; Apache-2.0 ở root không bao phủ tự động figure asset bên thứ ba. Các URL branch `main` khác là snapshot theo ngày; phải khóa commit/license trước khi copy hay chạy. Cặp URL raw có lúc bị chặn, một số Nature/IEEE policy không lấy được nội dung hiện hành. Nguồn không đọc được vẫn pending, không suy rule từ snippets.

`ak 2.19.0` live help xác nhận `ak skills` không cung cấp `run-skill`; `ak orchestrate` external process supervision chỉ hỗ trợ Darwin. Vì vậy adapter Windows phải dùng khả năng thực của host, không phải lệnh suy đoán. Catalog tool hiện có `mcp__ak_agent_runtime__agent_planner` và `mcp__ak_agent_runtime__agent_researcher`, được mô tả là dispatch agent qua `codex exec`; đây là API giao việc cho **agent**, không phải API gọi mọi skill. Chỉ kiểm metadata, không gọi các tool đó; tính tương thích, quyền và hành vi của route này vẫn chưa kiểm. Chưa có consumer run nào chứng minh wrapper/cook hoạt động.

Không có benchmark hiện tại cho giảm ảo giác, nâng gu Việt, dịch học thuật, tốc độ, giá hay editability đầu ra của kit mới. Plan sẽ định nghĩa matched baselines, fault cases, holdout và human acceptance; tuyệt đối không biến các điều kiện đó thành kết quả đã đạt.

## Nguồn nội bộ và thứ tự đọc

1. [Hợp đồng thiết kế đã cập nhật](brainstorm-260930-0905-skill-kit-contract.md): kiến trúc, ngôn ngữ, plan/cook, receipt, update và nghiệm thu.
2. [Nguồn cục bộ và công cụ bằng chứng](research-260930-0905-local-sources-and-evidence.md): coverage/hash, AgentKit, blueprint, ZIP, Q1/Q2.
3. [Nature-skills](researcher-260930-0905-nature-skills.md): module/file mapping và rủi ro.
4. [Hệ sinh thái bổ sung](researcher-260930-0905-skill-ecosystem.md): ứng viên, license/dependency và lý do chọn.
5. [Hooks, subagents, cost và host limits](researcher-260930-1706-hooks-agents-cost.md): nguồn vendor và local capability evidence, chưa consumer-tested.
6. [Nguồn official và hướng dẫn viết](researcher-260930-1706-official-standards-writing.md): scope, failure checks, false-positive boundaries và policy chưa fetch được.

Các báo cáo nghiên cứu là records tại thời điểm đọc, không phải chính sách runtime. Khi đề xuất kiến trúc ban đầu khác bổ sung mới của người dùng, dùng hợp đồng thiết kế cập nhật và bản tổng hợp này.
