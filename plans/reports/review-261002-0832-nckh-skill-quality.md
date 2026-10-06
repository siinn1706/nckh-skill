# Review NCKH: tài nguyên, năng lực và bằng chứng

Ngày: 02/10/2026, Asia/Saigon. Phạm vi: review và lập kế hoạch; không sửa/cài lại skill, không chạy provider, không publish.

## Kết luận

Bộ NCKH dùng được như một **candidate thử nghiệm có nguyên tắc và đã có quan sát chạy thực tế**, nhưng chưa đủ bằng chứng để gọi là bộ chuyên gia đã được kiểm định hoặc tốt hơn AgentKit/base model. Vấn đề không phải thiếu đuôi CSV/JSON. Cần thêm chiều sâu chuyên môn có chọn lọc, nối tài nguyên vào consumer/đóng gói, và đánh giá đóng góp thật của skill.

Giữ kiến trúc NCKH độc lập và 37 identities trong [plan hiện hành](../260930-1910-nckh-portable-skill-kit/plan.md). Plan wrapper ngày 30/09 trước đó đã bị thay thế; không quay lại kiến trúc cũ hoặc loại Engineer/Marketing.

## Hợp đồng của lượt này

- Outcome: chỉ rõ điều đã tốt, thiếu sót có bằng chứng, ý nghĩa từng loại tài nguyên và kế hoạch cải thiện khả thi.
- Constraints: giữ 37 identities, plan/cook và quyền người dùng; giữ VI/EN, venue isolation, fidelity, private data và toàn bộ lịch sử kiểm thử. Theo bổ sung trực tiếp: dataset phải lấy từ nguồn skill thật được chọn lọc, không tự sinh dữ liệu hay nhãn gold.
- Non-goals: không triển khai plan, nhập nguyên kho upstream, cài dependency, đổi model/config, benchmark trả phí, cập nhật bản đã cài hoặc nâng stable.
- Acceptance: kiểm tra source và installed artifacts; đối chiếu AgentKit/nature-skills/nguồn chính thức; report có vị trí bằng chứng; plan index ngắn và phase riêng; kiểm tra cấu trúc không bị gọi là bằng chứng chất lượng.

## Inventory hiện tại

Nguồn chính: [source lock revision 18](../../nckh-kit/core/registry/source-lock/source-lock.json), canonical hash `f52a03676b29fbd5434673a0f831dcae397fe879131beec00f35d3ca9b4d472d`.

| Bề mặt | Quan sát trực tiếp | Ý nghĩa |
|---|---|---|
| Source được pin | 184 file: 75 MD, 71 JSON, 36 Python, 1 PowerShell, 1 shell | Package không chỉ có Markdown. Không tính dist, history và receipts vào số này. |
| `nckh-kit/skills` | 37 `SKILL.md` và 7 reference MD; entry 37–42 dòng | Lớp chỉ dẫn rất mỏng. Độ ngắn không tự là lỗi, nhưng chưa có nhiều ví dụ/phương pháp cụ thể. |
| `.agents/skills/nckh-*` đã cài | 257 MD và 52 JSON, không có Python/CSV/JSONL | Shared contracts/schemas được đóng vào closure từng skill. Script của package không mặc nhiên được cài theo. |
| Corpus phát triển riêng | 148 yêu cầu có passages, CSV, HTML, source cards và code fixtures | Đã có data kiểm thử ở `plans/evaluation/`, không phải reusable knowledge trong skill. |

[Agent Skills specification](https://agentskills.io/specification) chỉ bắt buộc `SKILL.md`; scripts/references/assets là tùy chọn. File data không tự huấn luyện model và không hữu ích nếu không có đường đọc hoặc thao tác tiêu thụ nó.

## Bằng chứng hành vi: hai bộ phải được phân biệt

[Package case validation](validation-261002-0832-nckh-case-structure.json) báo 37 identities, 148 case definitions, 19 families, 224 native cells; case definitions của lane này vẫn `not-run`.

Nhưng [direct development report](testing-261001-direct-skill-development.md) và [aggregate JSON](../evaluation/direct-skill-tests/results.json) ghi một lane chạy khác đã hoàn thành. Đã đọc lại source report, aggregate, review records và đối chiếu hash [corpus](../evaluation/direct-skill-tests/development-corpus.json): `bbb6d312df45c4bad75bef5b5e8b5a42202dfcf0122382ee59e51ce84c63de84`.

| Phạm vi quan sát | Pass | Fail | Pending |
|---|---:|---:|---:|
| Vòng đầu của direct development | 137 | 4 | 7 |
| Quan sát gần nhất, có diagnostic follow-ups | 147 | 1 | 0 |

Đây là **controller-agent review trên exposed synthetic development cases**, subject là installed revision 14; không phải đánh giá mù, human gold, protected holdout hoặc so sánh no-skill/upstream. Wrapper cũng nhắc ranh giới và chỉ định skill, bốn ca chia sẻ session, diagnostics đổi điều kiện catalog. Do đó 147/148 không phải tỷ lệ chất lượng độc lập hay tác động nhân quả của NCKH. Source revision 18 không tự thừa hưởng chứng nhận của installed revision 14.

## Findings và giới hạn cần xử lý

### 1. P2 — Data/resource packaging chưa hỗ trợ hướng mở rộng được hỏi

`nckh-kit/core/build.py:45` chỉ pin `.md/.json/.yaml/.toml/.py/.ps1/.sh`; `.csv/.jsonl/.svg` không nằm trong source inventory. `core/build.py:127` chỉ lần theo Markdown links; script imports và file data không tự thành dependency. `core/build.py:58` gán cùng một nhãn `owned-local-package`, còn `core/build.py:92` yêu cầu `copied_third_party_content` là false.

Impact: thêm CSV/JSONL đơn thuần không tạo một skill data-driven có thể đóng gói. Builder hiện dừng an toàn với unlicensed/unpinned member; chưa thấy tài nguyên hiện hành bị mất. Copy tài nguyên bên ngoài rồi freeze có nguy cơ gắn sai nguồn/quyền. Cần dependency/rights contract tường minh, allowlist hẹp, kiểm tra từ bản extract sạch; không mở rộng thành copy-all.

### 2. P1 — Portable evaluation có oracle mâu thuẫn và validation quá yếu

`nckh-kit/evals/cases/research-writing-visuals/nckh-write.json:16` yêu cầu sửa một đoạn tiếng Việt nhưng không cung cấp đoạn; positive/outcome trùng prompt. Audit xác nhận **37/37 negative cases** yêu cầu reject nhưng oracle lặp tiêu chí positive. `core/evaluation.py:27-28` chỉ kiểm truthiness; `:41-43` chỉ đếm 19 family IDs, không kiểm nội dung/family-skill mapping; protocol shape cũng chưa đầy đủ. Vì vậy cấu trúc pass dù test contract có lỗi. Corpus concrete bên ngoài đã giải quyết phần input cho direct lane, nên không kết luận dự án chưa có data.

Impact: package tự thân chưa mang được bài kiểm tra đầu ra tái hiện tương đương. Plan cần regression cho oracle/family/protocol validation và mapping case/input/oracle/subject/receipt. Giữ bản cũ/lịch sử khi version hóa; không đổi `not-run` thành pass hàng loạt. Synthetic corpus cũ chỉ là diagnostic evidence, không dùng làm dataset nguồn mới theo yêu cầu người dùng. Chi tiết: [runtime/evaluation audit](code-reviewer-261002-0832-nckh-runtime-evals.md).

### 3. P2 — Instruction coverage rộng nhưng tri thức chuyên môn chưa được cụ thể hóa

`nckh-kit/core/profiles/style/vi.md:3` và `en.md:3` mô tả nguyên tắc đúng nhưng chưa có ví dụ đối chiếu theo genre, vì sao sửa/không sửa, hoặc tình huống ngoại lệ. `skills/core/nckh-write/references/fidelity-and-glossary.md:3` yêu cầu khai báo factual slots nhưng chưa có artifact mẫu nối trực tiếp với thao tác được kiểm tra. Cả 13 Engineer và 13 Marketing skill chưa có reference chuyên biệt nằm trong thư mục riêng.

Impact: model phải tự bổ sung nhiều phương pháp từ tri thức nền; quan sát hiện tại chưa tách được phần hữu ích do skill. Đây là khoảng trống thiết kế cần thử nghiệm, không phải bằng chứng rằng câu trả lời hiện tại dở. Ưu tiên annotated examples, decision guides, artifact templates và deterministic helpers có consumer; không kéo dài mọi file hay bắt mọi skill có CSV.

### 4. P1 đối với tuyên bố chất lượng — Chưa có matched baseline và human/domain acceptance

`nckh-kit/evals/baselines/baselines.json:3` còn `not-run`, `source_pins` rỗng. Direct report mục Native route and isolation mô tả explicit loading, wrapper effects và shared context; aggregate ghi `holdout: none`, `stable_accepted_task_count: 0` và `human_acceptance: not-evaluated`.

Impact: chưa thể nói bộ mới hơn upstream, giảm hallucination, tiết kiệm token, hoặc tiếng Việt hay hơn. Cần matched no-skill/current-NCKH/candidate/selected-permitted-upstream, giữ chất lượng tối thiểu trước tối ưu chi phí. Người dùng chọn reviewer/corpus riêng khi đánh giá taste/science; không giả tạo gold.

### 5. P2 — CRO có failure thật, nhưng chưa đủ căn cứ sửa trách nhiệm skill

`plans/evaluation/direct-skill-tests/workspaces/round-1/nckh-cro/request-1/site.html:1` có `noindex`. [Review record](../evaluation/direct-skill-tests/controller-reviews.json) giữ fail vì câu trả lời bỏ sót. Đã đối chiếu hash answer, native receipt và trace của CRO với review record: cả ba khớp. Tuy nhiên `nckh-kit/skills/marketing/nckh-seo/SKILL.md:31` sở hữu canonical/index, còn CRO sở hữu conversion friction.

Impact: phải xem lại mục tiêu/oracle và cross-skill handoff trước khi chọn sửa CRO hay tạo ca SEO liên quan. Không xóa failure, không đổi expectation hồi tố, không dùng một fail này để kết luận toàn bộ CRO yếu.

## Những phần nên giữ

- Phân biệt identity/ranking, claim support, methodological validity và acceptance; không lấy DOI/Q1 hay checksum làm chứng nhận đúng.
- Quyền plan/review/cook, privacy, preservation, failed receipts và per-revision gates được viết rõ.
- Build closure, source pins, transactional ownership và chương trình kiểm thử đã có; tái sử dụng thay vì xây framework mới.
- Có output thật và case reviews trong direct development; có thất bại được giữ lại. Catalog 37 skill hiện xuất hiện trong runtime này, không suy ra mọi nested host/OS đều discover được.

## CSV/JSON nên dùng khi nào?

| Tài nguyên | Khi hữu ích cho NCKH | Không nên dùng để |
|---|---|---|
| Markdown | Phương pháp, hướng dẫn lựa chọn, ví dụ có giải thích và giới hạn | Thay mọi bước tính/kiểm tra lặp bằng prose |
| CSV | Task glossary, search/screening log, flat lookup có bộ lọc và người dùng cụ thể | Tạo bảng từ cấm VI hoặc universal Nature rules |
| JSON/schema | Artifact contracts, provenance, resource dependencies, venue identity | Gọi metadata hợp lệ là evidence hợp lệ |
| JSONL | Example/case records có ID, provenance, split và annotation | Đóng gói manuscript riêng, nhãn holdout hoặc model scores thành human gold |
| Python | Parse/validate, count/dedup, compare declared slots, lookup có tests | Tự chứng nhận semantic support hoặc scientific truth |

## Đối chiếu và phương án

Chi tiết upstream ở [nature/related resources](researcher-261002-0832-nature-resources.md) và [AgentKit resources](researcher-261002-0836-agentkit-resources.md). Học cách nối SKILL → reference/data → tool → artifact → verification; không học số lượng file hoặc import nguyên repo.

Bổ sung theo yêu cầu không bịa dataset: [shortlist ba nguồn và tài nguyên đã kiểm nội dung/hash](researcher-261002-0832-source-shortlist.md). K-Dense có registry 15 reporting guidelines và 8 publisher profiles; UI UX Pro Max có 119 dòng UX guidelines với reader. Nature mạnh ở phương pháp/reference/QA, không phải corpus khoa học được gắn nhãn. Đây là thứ tự ưu tiên theo domain fit, không phải kết luận top 1–3 toàn cầu. Chỉ phối hợp sau khi kiểm compatibility, per-record provenance và quyền; thiếu data phù hợp thì ghi thiếu, không tự sinh bù.

Ba ví dụ đã kiểm tra cho thấy ba mục đích khác nhau:

- AgentKit `ak-ui-ux-pro-max` có `csv.DictReader` và tìm kiếm BM25 trên các bảng UI/UX; smoke read-only trả đúng `ux-guidelines.csv`. Đây là lookup data thực sự được tiêu thụ.
- Nature writing có [manifest theo task/paper type/section/language/journal](https://raw.githubusercontent.com/Yuan1z0825/nature-skills/84880815fb37317b3766bff2c2abba395b8993c3/skills/nature-writing/manifest.yaml); Nature figure có scripts kiểm tra figure. GitHub API đã xác minh full HEAD `84880815fb37317b3766bff2c2abba395b8993c3`. Học cách chọn reference và QA, không áp chuẩn một journal thành chuẩn phổ quát.
- K-Dense [claim-evidence CSV](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/scientific-writing/assets/claim_evidence_template.csv) chỉ là header và một dòng placeholder; [source manifest JSON](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/scientific-writing/assets/source_manifest_template.json) bắt đầu ở `unverified`. Đây là **biểu mẫu**, không phải kho bài báo/nhãn đúng đã được chuẩn bị sẵn. Anthropic [eval schema](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/references/schemas.md) nối prompt, input files, expectation và grading, là pattern phù hợp để liên kết corpus NCKH hiện có.

| Phương án | Giả định quyết định | Hỏng trước tiên khi | Kết luận |
|---|---|---|---|
| Giữ prompt gần nguyên, chỉ dọn docs/evals | Base model đã đủ phương pháp, skill chỉ cần giới hạn | Task khó cần ví dụ/domain procedure mà chưa được chỉ dẫn | Rẻ nhưng chưa giải quyết chiều sâu mà người dùng quan tâm. |
| Bổ sung chọn lọc theo consumer và gap đã đo | Resource mới cải thiện artifact mà không hại fidelity/authority | Candidate không vượt quality floor hoặc resource không được dùng | Đề xuất; dễ bỏ từng resource không hữu ích. |
| Port lớn CSV/script/library upstream | Quyền, dependency và policy tương thích trên mọi host | License, path, provider hoặc venue-specific rules không khớp | Không chọn; chi phí cao, trái yêu cầu không gom cả kho. |

Better approach so với thêm CSV cho đủ hình thức: lập resource-to-consumer matrix cho toàn bộ 37 identities, bổ sung đúng nơi có ích và kiểm tra từ bản đóng gói. Chi phí chuyển là case/provenance/build contract cụ thể, không phải đổi kiến trúc độc lập.

## Kiểm tra trong lượt review

- `python evals/run-evals.py --validate-only`: pass về cấu trúc, revision 18; receipt riêng ở link phía trên.
- `python -m unittest tests.evidence.test_guards tests.release.test_qualification tests.build.test_closure`: 19 tests, 32.574s, OK. Không chạy provider hoặc suite hành vi mới.
- AgentKit body lint: 44 Markdown nguồn, zero heuristic findings. Không chứng minh instruction quality.
- AgentKit `quick_validate.py` cho installed `nckh-write`: chưa chạy được vì thiếu PyYAML; exit 1. Không cài dependency trong lượt review. Routing-aware lint cũng chưa được xác minh.
- Session-usage scan chọn `nckh-write`, 01–02/10, loại session hiện tại: 5 matched read spans trong 3 session. Median/p90 thời lượng là 2.366,439/18.981,706 giây, lượt hội thoại 35/201, tool calls 34/185, output tokens 47.125/341.139. `exec` chiếm 279 calls và 1.353,1 giây tool wait; có 23 error signals và 2 duplicate calls. Đây có thể là đọc để audit hoặc tác vụ chained, không dùng làm isolated skill-performance baseline. Codex subagent tokens không được quy thuộc ở đây; không diễn giải zero là không có chi phí. Không audit sâu timing/cost từ raw transcripts, không kết luận token saving.
- Không có Git repository tại workspace; dùng source-lock và file hashes cho integrity. Không tạo commit.

## Câu hỏi còn mở trước triển khai

1. Với CRO/SEO, người dùng muốn giữ ownership hiện tại và explicit handoff hay mở rộng CRO? Giữ nguyên failure lịch sử trong cả hai lựa chọn.
2. Corpus VI/EN dùng để cá nhân hóa và reviewer nào có quyền chốt taste/domain? Khi chưa chọn, chỉ đánh giá development, không human acceptance.
3. Chọn host/model và ngân sách cho matched evaluation khi thực hiện phase đó. Lượt review này không tạo quyền chạy mới.
