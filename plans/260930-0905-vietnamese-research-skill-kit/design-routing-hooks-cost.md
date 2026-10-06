# Plan → cook: tự chọn skill, hook, subagent và ngân sách

Ngày 30/09/2026, Asia/Saigon. Đây là đặc tả để triển khai sau, không phải runtime
đã tồn tại. P1 sở hữu router/adapter/budget contracts; P5 sở hữu phép đánh giá.
Người dùng đã yêu cầu luồng hai bước, tag tùy chọn, hooks/subagents và context
skill dưới khoảng 20k–40k, tương ứng 10%–20% context window.

## 1. Giao diện người dùng và lựa chọn kiến trúc

Chỉ hai entrypoint thường dùng: `research-plan` và `research-cook`. `plan`/`cook`
ở đây là tên luồng, không tự đăng ký alias đè `ak-plan`/`ak-cook`. Mười module
domain là nội bộ; người dùng không cần nhớ hay tag chúng. Tag thủ công được ưu
tiên khi capability thích hợp và có sẵn, nhưng không cấp quyền, đổi venue hoặc
bỏ kiểm chất lượng. Không tag thì tự chọn từ live catalog. Tag sai định dạng
hoặc trỏ tới skill không khả dụng phải được báo; chỉ dùng fallback phù hợp đã
được cho phép, nếu không thì giữ `NOT_CALLABLE`/cần lựa chọn. Không tự cài skill.

Giữ wrapper có hợp đồng quanh AgentKit. Không chọn router thuần chỉ trả tên
skill vì thiếu artifact acceptance; không fork cả kit vì tăng bảo trì và mất
lợi ích upstream. Không chọn always-on multi-agent vì overhead không hợp với
tác vụ sửa văn nhỏ. Subagent/hook là phương tiện theo rủi ro, không phải dấu
hiệu chất lượng tự thân.

```text
User: plan [request, optional tags]
  → brief + live catalog → capability shortlist → selected instructions
  → small execution plan + route/budget/rule profiles → user authorizes cook
User: cook [plan]
  → revalidate scope/versions/budget → scoped worker(s)
  → deterministic checks + evidence/style/visual review → scoped handoff
```

Trong plan-only, các worker nghiên cứu có thể đọc nguồn công khai và tạo hồ sơ
plan/research/validation/journal theo quyền đã có. Không tạo bài/slide hoàn chỉnh,
cài hook, thay cấu hình, chạy provider trả phí hay tự chuyển sang cook.

## 2. Catalog-first routing: `listskill` là cơ chế, không phải API bịa

1. Lấy live installed catalog từ host trước. CLI list/search chỉ là nguồn kiểm kê
   bổ sung sau khi đọc help thực tế; catalog rỗng ở sai scope không chứng minh
   máy không có skill. Ghi nguồn, thời điểm, completeness và phạm vi inventory.
2. Normalize brief thành artifact, language, genre/study design, edit scope,
   evidence need, venue, privacy, output format, quality và budget. Từ khóa VI/EN
   và đồng nghĩa chỉ giúp tìm ứng viên; khớp từ không đủ chọn worker.
3. So metadata theo capability, exclusions, output/editability, availability,
   permission, accepted revision và cost coverage. Một primary owner mỗi intent;
   thêm helper chỉ khi có phần việc/check riêng. Không tìm trên marketplace hoặc
   tải skill mới chỉ vì catalog không khớp; báo gap và fallback được phép.
4. Đọc đầy đủ `SKILL.md` và references bắt buộc của ứng viên được chọn trước dùng.
   Budget không cho phép cắt chỉ dẫn. Nếu dependency bắt upload/cron/coding ngoài
   brief thì chọn route khác hoặc dừng; không tuyên bố dùng skill rồi bỏ luật của nó.
5. Ghi route decision: capability, skill ID/namespace/origin, lý do chọn/loại,
   instruction/dependency hashes, actual invocation interface, permissions,
   predicted context/cost class, verification owner và fallback đã kiểm.
6. Cook resolve lại availability/hash/scope trước chạy. Reuse catalog snapshot
   không đổi trong cùng task; refresh khi host/catalog/config thay, resume hoặc
   lookup không còn đúng. Đổi material authority/format/quality cần sửa plan;
   thay worker trong các lựa chọn đã duyệt vẫn phải qua compatibility và receipt.
7. Dispatch qua actual host tools hoặc cùng agent đọc-và-thực-hiện skill. Đọc
   file không phải đã execute, tool metadata không chứng minh một consumer run.
   Thiếu route trả `NOT_CALLABLE`; không phát minh `ak run-skill`.

AgentKit router đang cài có cùng nguyên tắc live catalog, one-owner và workflow
ngắn; tận dụng nó nếu hợp đồng tương thích. Không bắt người dùng gọi thêm router
ngoài `plan → cook`. Nguồn hiện tại: local `ak-agentkit/SKILL.md` và các references
chaining/subagent; [báo cáo runtime](../reports/researcher-260930-1706-hooks-agents-cost.md)
phân biệt tài liệu chính thức với khả năng local chưa thử.

## 3. Hook contract: ít hook, guard rõ và không nhân chi phí

Bảng sau dùng **semantic event của kit**, không khẳng định đây là tên event mà
mọi host hỗ trợ. Adapter phải map sang hook/API có thật hoặc explicit workflow
gate. Core không phụ thuộc một chuỗi tên event dùng chung Codex/Claude.

| Semantic event | Việc hữu ích | Loại kiểm / chi phí | Khi thất bại |
|---|---|---|---|
| Task start / resume | Restore brief, route lock, approval scope, versions, pool | Local record/hash checks; không nạp toàn bộ library | Missing/stale record chặn affected action, không tự tạo approval |
| Before skill load / delegate | Full dependency size, ownership, child permissions, pool reservation | Deterministic selection/budget check | Serialize, smaller valid route hoặc plan revision; không truncate |
| Before external call / write | Scope, path containment, egress, paid-call reservation | Synchronous host/adapter enforcement | Fail closed với operation cần quyền; reminder không đủ |
| After read / edit / worker result | Record sources/receipt, factual delta, stale descendants | Schema/hash/number checks trước; semantic critic chỉ phần cần | Stage output; source/claim pending nếu chưa kiểm |
| Before handoff | Required gates, exact artifact hashes, human decisions | Aggregate deterministic check + scoped review | Không accepted nếu còn mandatory fail/pending |
| Compact / stop | Persist minimal state, settle known usage, track outstanding handles | Bounded local state; không lưu raw secrets/manuscripts | Báo state incomplete; không hook-loop ép tiếp tục |

Không gọi LLM từ mọi `PostToolUse` hay mỗi lần gõ câu. Dedupe theo
`run_id/event_id/input_hash`; guard reentrancy/recursion, timeout, output size và
side effects. Async hook chỉ dùng logging/telemetry, không dùng để chặn một call
đã chạy. Đối với checks quyết định quyền/budget, hook crash/no-match/disabled
phải được actual adapter/host guard xử lý trước operation; nếu không chứng minh
được thì route không hỗ trợ tác vụ cần enforcement đó.

Existing AgentKit hooks chỉ reuse qua interface được hỗ trợ; không sửa bản global
hoặc bọc lặp một guard đã hoạt động. Local source đã đọc có reminder/fail-open
behavior, nên không suy chúng là security boundary. Test coverage phải gồm shell,
MCP/native tool và subagent paths thực sự có, không chỉ một matcher tên `Write`.
Theo [Codex hooks](https://developers.openai.com/codex/hooks), hosted tools như
WebSearch không đi qua cùng đường local tool hook; `write_stdin` không chạy lại
`PreToolUse`, và một số đường tool chuyên biệt có thể opt out. Vì vậy không lấy
một matcher pass làm bằng chứng mọi egress/write đều bị chặn; adapter phải kiểm
đúng đường thao tác, quyền host và continuation thực tế. Đây là caveat riêng của
host/version, không chuyển nguyên semantics sang Claude hay SDK khác.
Hook installation/configuration là bước triển khai cần cho phép riêng; không
thực hiện trong lượt plan này. Không tự dựng proxy/auth server.

## 4. Subagents: mở có lý do, đóng có bằng chứng

- Controller giữ brief, authorization, route/budget pool, merge và user decisions.
  Reader/researcher có thể chia nguồn không chồng nhau; writer không tự accept.
  Evidence reviewer, taste critic và visual inspector chỉ mở khi tạo thêm phép
  kiểm hữu ích hoặc cần fresh context. Simple polish thường đi same-agent.
- Mỗi packet có task, input paths/hashes, output contract, read/write scope,
  acceptance, rule/profile revision, source authority boundary, tools/egress,
  allocation/timeout/stop rule, cwd, timezone, output language và report path.
  Không fork toàn hội thoại; tuy nhiên vẫn tính phần host bắt buộc kế thừa vào budget.
- Quyền con là giao của parent authorization và host permissions. Không truyền
  ambient credentials hoặc chính sách allow-all. Child không tự spawn mặc định;
  fan-out tối đa nằm trong budget/profile đã duyệt và giới hạn host.
- Một owner cho một file/artifact. Fan-in kiểm receipt/source, reconcile mâu thuẫn
  và chạy check trên artifact hợp nhất; report `DONE` không thay cho evidence.
  Khác model không tự chứng minh độc lập; ghi model/provider/context/exposure.
- Timeout-unknown đối soát cùng handle, không spawn bản thay thế chỉ vì hết thời
  gian quan sát. Stop/cleanup chỉ tài nguyên kit thực sự sở hữu. Một human decision
  là terminal wait cho route, không tạo vòng agent hỏi nhau.

## 5. Context budget: ràng buộc thực, không chỉ viết con số trong prompt

### Phạm vi đếm

`K_i` là token skill-related thực sự trong context i: catalog metadata, active
skill bodies, loaded references, upstream mandatory instructions, role/delegation
prompts, hook injections, routing/skill tool schemas và phần lặp kế thừa. Tính cả
catalog/upstream host tự đưa vào nếu chúng thuộc phần skill; không bỏ chúng khỏi
mẫu số để báo tiết kiệm. Cached tokens vẫn chiếm context. File trên đĩa nhưng chưa
nạp không tính; summary không làm nội dung cũ biến mất khỏi context hiện tại.

`W_i` là context window được xác minh cho model/runtime; `H_i` là overhead host
không thuộc skill; `D_i` là source/task text; `O_i` là chỗ dành cho output và phần
reasoning mà host tính trong window. Kiểm cả `K_i + H_i + D_i + O_i <= W_i`.
20k–40k là budget skill, **không phải tổng token tích lũy của cả dự án**; tổng phí
và token đọc/viết vẫn có budget riêng. Không coi việc chuyển data sang subagent là
miễn context/miễn phí.

### Các trần đồng thời

- Mỗi context: soft `min(20,000, floor(0.10 × W_i))`; hard
  `min(40,000, floor(0.20 × W_i))`. Đây là upper bounds, không phải mục tiêu phải dùng hết.
- Pool toàn task lấy W của controller theo cùng công thức. Tổng K của controller
  và các worker còn giữ context/chuẩn bị resume không vượt pool hard limit.
  Không cấp mỗi agent 40k. Allocation phải thỏa cả trần riêng lẫn trần pool.
- Mặc định hoạt động dưới soft limit. Chỉ dùng phần 20% khi route/quality nhu cầu
  đã ghi trong plan và vẫn trong grant/budget; không âm thầm mở rộng tới 40k cho mọi task.
- Context cũ chỉ giải phóng allocation khi thực sự retire/reset hoặc có host
  compaction xác nhận. Retained idle agents vẫn tính; cumulative token/chi phí
  lịch sử vẫn giữ, không reset khi đổi agent hoặc đổi tên run.

Ví dụ giả định W = 200k, không phải model đã đo: controller 8k + reader 6k +
reviewer 4k = 18k skill context trong pool. W = 128k thì soft 12.8k, hard 25.6k;
40k vẫn sai dù chưa vượt absolute ceiling. W lớn hơn không nâng absolute ceiling
trên 40k. Những phép tính này là contract tests, không phải savings benchmark.

### Đo và xử lý vượt trần

Serialize packet thực tế rồi đếm bằng tokenizer/usage của model khi có; ghi
`measured|estimated|partial|unknown`, window source, tokenizer revision và buffer.
Không dùng chars/4 cho tiếng Việt như phép đếm chính xác. Host overhead bị ẩn
hoặc catalog tự inject không đo được thì không certify budget-compliant; giữ
conservative bound, hạn chế thêm context/fan-out và yêu cầu runtime measurement
trước nghiệm thu. Không báo đã đạt cap trong chính cuộc chat lập kế hoạch này.

Chặn trước load/dispatch khi size đã biết vượt trần. Theo thứ tự: bỏ optional
reference không cần, giảm shortlist, reuse exact-revision evidence, serialize
workers, chuyển sang fresh phase-scoped context có state tối thiểu, chọn worker
nhỏ hơn nhưng đáp ứng đủ hợp đồng. Không cắt rules, đổi scope, bỏ citations hay
hạ chất lượng để vừa budget. Nếu chỉ dẫn bắt buộc và host baseline đã vượt cap,
đánh dấu runtime/profile không tương thích; không tự sửa global settings hoặc
mượn ngân sách context của bước khác để che vi phạm.

## 6. Tối ưu chi phí với chất lượng làm ràng buộc

Mục tiêu là giảm chi phí cho **task được nghiệm thu đủ scope** ở cùng quality
floor, đồng thời báo completion rate và latency. Không tối ưu số token/lần gọi
riêng lẻ, không loại case thất bại khỏi phép đo.

`cost_per_accepted_task = all_attempt_cost / accepted_task_count`.
Tử số gồm planning, discovery, controller, toàn bộ agents, hooks, tools, image,
cache writes/reads, retry và review; công sửa người dùng báo riêng theo phút hoặc
quy đổi chỉ khi có rate được đồng ý. Denominator bằng 0: report undefined, không
coi là 0 hay một tiết kiệm. Subscription quota/credits khác hóa đơn API; trường
không quan sát được giữ unknown và có coverage ratio, không tự nhân giá API.

Budget record có token/money/time/tool-call/call-count limits, price source/date,
reserved verification allowance và stop rule. Reserve trước dispatch, settle
theo actual known usage; reconcile pending cost trước lặp. Khi telemetry/host
không enforce hard monetary cap được, nói rõ giới hạn, dùng bounded authorized
calls; không hứa tuyệt đối không overshoot một in-flight request.

Tiết kiệm theo thứ tự: deterministic checks; metadata discovery + progressive
disclosure; exact-revision cache; narrow evidence retrieval; same-agent khi đủ;
selective subagent/model routing dựa trên matched eval; render/image pilot; batch
offline chỉ khi deadline/privacy cho phép. Prompt cache chỉ giảm chi phí khi
provider thực sự hỗ trợ/hit; không làm nguồn hết lỗi thời. Không mặc định
best-of-N, parallel full-manuscript rewrites hoặc LLM-as-judge sau mọi tool call.

## 7. Nghiệm thu và các quyết định trước triển khai

P5 phải có tests no-tag VI/EN routing, manual-tag conflict, incomplete catalog,
mandatory instructions vượt cap, inherited/idle context, smaller W, hook crash,
matcher bypass, duplicate event, budget race, timeout-unknown, stale receipt và
cost unknown. Matched comparison single-agent/selective agents chỉ được gọi tốt
hơn khi cùng scope và quality gates; luôn báo raw counts và uncertainty.

Chưa có benchmark/consumer run. Còn phải xác nhận target host adapter, tokenizer/
window visibility, money/time budget, reviewer và phép gọi provider. Đây là gates
cho triển khai/task thật, không cản hoàn tất tài liệu kế hoạch.
