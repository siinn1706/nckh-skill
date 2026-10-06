# Public workflow, human review và model routing

Đặc tả ngày 30/09/2026, được người dùng duyệt ngày 01/10/2026 theo [plan chính](plan.md); chưa có lệnh NCKH được cài. `/nckh-*` là public
workflow notation; adapter hiển thị đúng cách gọi host trong [runtime matrix](runtime-compatibility.md).
Đây không phải lệnh shell và không tự đăng ký alias trong lượt lập kế hoạch.

## 1. `/nckh-plan`

`/nckh-plan "task"` nghiên cứu vừa đủ, challenge assumptions, khóa outcome,
constraints, non-goals và acceptance, rồi tạo index ngắn + phase detail khi task
đủ lớn. Sửa nhỏ có thể dùng brief/plan ngắn; không ép bảy phase cho một câu văn.

`/nckh-plan @plan.md --validate` đọc index, mọi phase và input/source liên quan;
kiểm current repo, dependency, permission, owner, scope, test oracle, acceptance,
rollback và state. Kết quả có claim ledger VERIFIED/FAILED/UNVERIFIED, findings,
revision diff và quyết định còn cần user. Plan nội bộ nhất quán khác runtime đã chạy.
Plan quá cũ không được pass chỉ vì frontmatter hợp lệ.

Chỉ dùng một modifier stable ban đầu: `--validate`. Research/red-team là bước
theo rủi ro trong workflow; chưa thêm `--deep`, `--research`, `--red-team`, `--strict`
cho tới khi có khác biệt contract và eval riêng. Không bịa ý nghĩa cho flag lạ.

Plan được ghi research/validation/state cục bộ đúng scope; không tạo sản phẩm cuối,
cài dependency, chạy paid benchmark, thay config global hoặc tự chuyển sang cook.
Findings có bằng chứng và đề xuất sửa không phải bằng chứng người dùng đã duyệt.

## 2. `/nckh-cook`: cùng outcome, hai semantics thật sự khác

| Input | Hành vi |
|---|---|
| `"task" --auto` | Inspect và ghi concise plan, rồi làm đủ authorized task; hỏi khi có material decision chưa giải được. |
| `@plan.md --auto` | Kiểm scope/revision/authority; thực thi mọi phase hợp lệ; tự validate/fix/test; không hỏi routine checkpoints. |
| `@plan.md --interactive` | Thực thi theo phase; dừng tại review boundary đã định trước, giao đúng artifact và câu hỏi review; chờ feedback thật. |
| Không mode | Nếu approved plan đã khóa mode thì giữ; nếu chưa, đề xuất mặc định interactive và nêu trước khi bắt đầu. |
| Cả hai mode | Input conflict; không chọn âm thầm. |

Không có `--no-test` trong NCKH stable. Thiếu công cụ test phải report pending,
không ghi pass. Tên `auto` không tương đương unrestricted shell, quyền admin,
network upload, paid API, commit, publish hay venue submission.

### State và review boundary

`planned → authorized → running → checking → ready-for-review → accepted` là
task progression; phase/artifact/claim gate độc lập. `waiting-human`, `blocked`,
`failed`, `timeout-unknown` không phải success và phải có lý do + next action.

Mỗi interactive boundary phải có:

- Artifact path/hash, phần vừa thay đổi, test/evidence summary và giới hạn.
- Một quyết định cụ thể: approve, request changes hoặc reject; không hỏi “OK?” trống.
- Phạm vi bị khóa sau duyệt và phase downstream chưa được phép chạy.
- Feedback record gắn revision; khi đổi dữ kiện/thiết kế, invalidate descendants.

Ví dụ meaningful boundaries: chốt research protocol trước thu thập, chọn thesis/
outline trước full draft, duyệt visual pilot trước full deck, duyệt UX trước diện
rộng, duyệt thông điệp chiến dịch trước production nội dung. Schema formatting,
routine test rerun hay file-save không tự tạo human checkpoint.

Interactive xử lý **một phase mỗi lượt thực thi phase**, nhưng có thể nối các
phase kỹ thuật không có quyết định người dùng; không hỏi sau mỗi file. Phải có
ít nhất một substantive review boundary trước downstream material work với plan
nhiều phase. `--auto` bỏ pause approval thường lệ cho reversible work đã được cho
phép, vẫn giữ mandatory human-scientific/taste/license/egress/irreversible gates.
Nếu một phase bắt buộc human gold thì auto báo `waiting-human`, không tự chấm thay.

Resume đọc durable state và actual artifacts, đối soát outstanding handles trước
retry; source/file presence không chứng minh phase hoàn tất. Feedback trong PDF,
repo hay worker report không cấp quyền như lời người dùng.

## 3. Xia: upstream thực tế và adaptation có chủ đích

Nguồn đã đọc trực tiếp: installed `ak-xia` 1.0.1 và [upstream research](../reports/researcher-260930-1910-agentkit-port-evidence.md).

| Upstream mode | Behavior đọc được | NCKH đã duyệt |
|---|---|---|
| `--compare` | So sánh, report-only; không implementation plan | Giữ nghĩa report-only; kết thúc bằng PORT/MERGE/EXTENSION/DROP recommendation. |
| `--port` (default) | Viết lại theo stack local, tạo plan, không implement | Tạo NCKH adaptation plan sau challenge/license/dependency analysis. |
| `--improve` | Phân tích cải thiện, tạo plan, không implement | Tạo plan thay đổi có claim/eval để so với nguồn và baseline. |
| `--copy` | Minimal-transplant plan | Không expose ở NCKH stable; dễ bị hiểu là bỏ challenge/license. |
| `--fast` | Bỏ research/challenge, auto-approve | Không port speed mode này; mâu thuẫn challenge-before-port. |
| `--auto` | Tự qua routine gates, vẫn chỉ plan | Không cần thêm trong tool NCKH ban đầu; không có quyền cook. |

Không đổi semantics `/ak-xia` đã cài. Tên đã duyệt riêng **`/nckh-xia`**, nguồn
`skills/tooling/nckh-xia/`, là một tool workflow Engineer dùng chung, không mega router.
Quyết định namespace đã được duyệt ngày 01/10/2026; không cài alias `/ak-xia` cho NCKH
và không ghi đè skill upstream. Người dùng vẫn có thể dùng `/ak-xia` upstream nguyên bản;
phê duyệt này chưa cho phép tạo hoặc cài `/nckh-xia`.

Pipeline: resolve repo/ref/path → source manifest → map local equivalents → trace
behavior/dependencies/side effects → challenge fit/rights/cost → disposition →
report hoặc `/nckh-plan` handoff. Không chạy script lấy từ repo. Alias `agentkit`
chỉ dùng sau khi registry resolve được origin/path/revision; không hiểu chuỗi đó
là repo GitHub tự nhiên. Private upstream thiếu quyền vẫn dùng installed snapshot
và ghi giới hạn, không giả đã fetch latest.

Input ví dụ dự kiến: `/nckh-xia <resolved-agentkit-path> "ak-plan" --compare`,
`/nckh-xia <repo> "feature" --port`. Khi compare muốn đi tiếp, dùng nckh-plan với
report; không bí mật tạo plan trong compare-only. No code ở mọi mode xia.

## 4. Delegation là quyết định, không là bước mặc định

Trước spawn ghi một hoặc nhiều lý do: cheaper eligible model, stronger reasoning,
fresh context, independent check, true parallel work, specialist tools/instructions.
Cùng model + cùng purpose + không có lợi ích isolation/parallelism/check thì không
spawn. Chuyển deterministic checks cho script, không LLM.

Agent roles là template, không một agent cho từng skill:

| Role | Tier gợi ý | Khi cần context riêng |
|---|---|---|
| Explorer | fast | Repo/source lookup hẹp, output paths/evidence; không tự ra architecture decision. |
| Researcher | worker | Tập nguồn độc lập; tổng hợp phức tạp có thể nâng deep. |
| Maker | worker | Writer/implementer theo domain đã chốt, file ownership rõ. |
| Planner | deep | Kiến trúc/phương pháp có trade-off thật; thường root làm, không spawn dư. |
| Reviewer | worker hoặc deep theo risk | Blind-to-rationale/fresh-context review, tests/claim support độc lập với lời writer. |
| Taste critic | worker | Chỉ critic style; không thay human preference hoặc tự sửa fact. |

Role không hard-code model. `fast`, `worker`, `deep`, `inherit` là logical tiers,
không là four vendors hay quy tắc dùng model nhỏ bất chấp risk. `inherit` là lựa
chọn được ghi rõ, không là silent fallback cho mọi delegation.

Packet: task, source/input paths+hashes, scope/ownership, acceptance, constraints,
host tools, egress, model policy, budget, timezone/language/cwd, report destination,
stop rules. Không full-history fork mặc định. Ghi host-inherited instructions nếu
không tránh được. Permission của child không vượt parent; không nested spawn mặc định.

Review cùng model ở context mới là kiểm tra tách vai trò/context; không gọi đó là
human/domain-independent confirmation. Khác model cũng không tự chứng minh đúng.

## 5. Profile lựa chọn model theo từng host

| Profile | Resolution policy | Guard |
|---|---|---|
| Auto | Host capabilities + task risk + accepted eval lựa chọn eligible tier/model | Không đổi provider/quyền/chi phí ngoài scope; unavailable hiện rõ. |
| Cost optimized | Model rẻ nhất đã đủ quality floor cho từng tier/task | Deep task không xuống fast chỉ để rẻ; chưa có cost telemetry không claim savings. |
| Balanced | Routine fast, production worker, difficult design/review deep | Count overhead/retries/verification, không agent theo số skill. |
| Quality first | Nâng effort/model ở phần reasoning/risk thực sự cần | Simple edit không tự fan-out hay dùng deep reviewer hàng loạt. |
| Custom | User map fast/worker/deep/inherit riêng cho claude/codex/cursor/agy | Validate IDs, availability, effort, billing route; preserve owner choices. |

Resolution: classify task → select tier → check native override support → intersect
user-allowed models → validate effort → estimate full task overhead → run or ask.
Log requested/resolved model/effort, source of availability and fallback reason.
Role-specific config có precedence trên spawn ở một host phải được probe; không
khẳng định requested=model thực sự chạy khi receipt thiếu telemetry.

### Contract model-resolution để P1/P5 triển khai

| Nhóm field | Nội dung bắt buộc |
|---|---|
| Target | host, surface, version, agent role, profile revision, requested tier |
| Request | requested model/effort hoặc inherit, allowed provider/billing scope |
| Encoding | native field/encoding, config path + owned key, precedence, capability evidence/as-of |
| Resolution | resolved model/effort, availability state/source, fallback reason, blocked reason |
| Observation | effective model/effort hoặc unknown, native receipt reference, observed/docs-only/not-run |

`configured` chỉ chứng minh config đã lưu; `applied` cần host đọc đúng config;
`effective` cần actual run receipt. Không ghi effective bằng giá trị requested.
Claude agent effort/CLI effort, Codex custom-agent precedence, Cursor parameterized
model string và Agy custom-agent aliases/CLI effort là bốn encodings riêng. Agy
`max` và arbitrary per-agent model ID không portable chỉ vì CLI help có flag.
Invalid ID, invalid effort, overridden mapping và unavailable deep đều có negative
cases; no silent downgrade. Current host/account có thể không lộ billing/usage,
khi đó ghi unknown và không chứng minh cost-optimized bằng nhãn profile.

Host không per-agent override: giữ same-agent/inherit khi vẫn đáp ứng task và
report limitation. Nếu cần deep mà chỉ có lightweight, hoặc yêu cầu independent
context mà host không có, dừng affected route; không silently downgrade. Tạo tiến
trình CLI riêng là extension riêng cần quyền/budget, không workaround mặc định.

Không hard-code model IDs/giá/window trong core. Installer hiển thị discovery thật
và timestamp; không gọi trial API hoặc đọc secret để đoán subscription. Mapping
chưa verified là pending; `doctor` kiểm read-only khi đủ interface.

## 6. Minimum sufficient context và chi phí

Với mỗi context i: loaded instructions + host/tools + task evidence + output/
reasoning reserve phải nằm trong usable window đã biết. Không có trần universal
40k, không lấy window controller áp cho tất cả child. Nếu W/usage unknown, ghi
unknown, giới hạn fan-out/context bằng scope hữu hạn và không certify compliance.

Metadata discovery, selective source reads, phase-scoped state và full required
instructions thay cho nhồi cả catalog. Cached tokens vẫn chiếm window; cumulative
cost gồm mọi attempts, hooks, agents, tools và retry. Không coi retire context làm
xóa token đã trả phí. Preserve verification reserve; không cắt scope/evidence để fit.

`cost_per_accepted_task = all_attempt_cost / accepted_task_count`; denominator 0
là undefined. Báo cost coverage, human edit time, failure rate và latency. Không
quy đổi subscription credit thành API USD nếu không có dữ liệu billing phù hợp.

Hook là adapter tùy chọn; security dựa host permissions/sandbox và explicit
workflow gates. Hook thiếu/crash/bypass không được âm thầm mở critical operation.
Async logging không chặn side effect; timeout cần reconcile trước retry.
