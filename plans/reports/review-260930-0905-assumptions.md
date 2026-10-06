# Review assumptions và scope — skill kit Việt–Anh

## Phạm vi và quy ước

- Đã đọc đủ 6 file kế hoạch, 2 báo cáo nền và blueprint gốc; chỉ review plan, không sửa kế hoạch, không chạy code/provider/test.
- `VERIFIED` dưới đây chỉ là khớp với record/FS hiện có, không phải behavioral pass. `PROPOSED` là hợp đồng tương lai; `UNVERIFIED` cần runtime, nguồn, quyền hoặc người thật; `FAILED` là mệnh đề/gate chưa đứng vững vì lỗ hổng thiết kế nêu ở dưới.

## Full-tier validation ledger

Đã lấy mẫu 15 mệnh đề có nội dung/phase (75 mệnh đề tổng cộng), không gọi đây là 75 test.

| Phạm vi mẫu | N | VERIFIED | FAILED | UNVERIFIED | PROPOSED | Dải bằng chứng |
|---|---:|---:|---:|---:|---:|---|
| P1 nền tảng/adapter | 15 | 4 | 2 | 3 | 6 | `phase-01-start.md:26-66,104-141` |
| P2 evidence/research | 15 | 3 | 1 | 4 | 7 | `phase-02-evidence-and-research.md:27-75,121-139` |
| P3 VI/EN writing | 15 | 3 | 1 | 4 | 7 | `phase-03-vietnamese-and-english-writing.md:28-80,127-145` |
| P4 visuals | 15 | 3 | 1 | 4 | 7 | `phase-04-slides-and-scientific-visuals.md:27-70,116-134` |
| P5 eval/package | 15 | 3 | 2 | 4 | 6 | `phase-05-evaluation-and-packaging.md:28-69,125-142` |
| **Tổng** | **75** | **16** | **7** | **19** | **33** | Không phải test execution |

## Scope Auditor — state creation/use và lifetime

| State/site trong plan | Lifetime được nói/được suy ra | Nơi tạo/dùng | Rủi ro còn hở |
|---|---|---|---|
| `brief`, plan revision/hash, permission record | task; caller/session chưa định nghĩa | P1 architecture/entrypoints (`phase-01-start.md:28-30,46-49`) | File có thể tồn tại nhưng approval/owner/expiry/revocation/concurrency không có; cook chưa có authorization artifact bắt buộc. |
| resolution/worker candidate và execution receipt | run/task; accepted mapping thuộc package | P1 (`phase-01-start.md:47-49,109-112`) | Chưa có capability invocation schema/caller scope; route có thể chỉ `NOT_CALLABLE`. |
| source/search manifest, reader cards, claim ledger, outline | task/corpus; P2 → P3/P4 | P2 (`phase-02-evidence-and-research.md:50-58`) | `source_id`/profile namespace, retention và chống tái dùng chéo task chưa được quy định. |
| venue/profile, style profile, terminology ledger | task hoặc project; không có session lifetime | P1/P2/P3 (`phase-02-evidence-and-research.md:72-75`; `phase-03-vietnamese-and-english-writing.md:50,64-75,157`) | Glossary/profile/ranking có thể leak từ task A sang B; chưa có reset, copy-on-write, lock hay merge policy. |
| source-lock, compatibility, worker-capabilities, manifest schema | package; installed state là upstream/global | P1/P5 (`phase-01-start.md:85-90`; `phase-05-evaluation-and-packaging.md:88-92`) | P5 đề xuất registry change nhưng không nêu atomicity/owner/version transition; shared mutable registry dễ ảnh hưởng concurrent run. |
| human gold, holdout, eval manifest/rubric | package/evaluation; holdout cần rotate sau exposure | P5 (`phase-05-evaluation-and-packaging.md:28-33,76-82,148-149`) | Không có access boundary, reviewer scope, identity/consent/retention hoặc xử lý thiếu rater. |
| artifact, render, package manifest, rollback record | run → package/release | P1/P4/P5 (`phase-04-slides-and-scientific-visuals.md:46-50`; `phase-05-evaluation-and-packaging.md:48-52,60-65`) | Chưa có allowlist dữ liệu được đóng gói, deletion/retention và tách private manuscript khỏi package artifact. |
| caller/session state | **Không có site/lifetime rõ ràng** | Chỉ có “user allowed” và “runtime/model nếu biết” (`phase-01-start.md:28-37`) | Đây là khoảng trống xuyên suốt: không biết ai được tiếp tục/resume, scope quyền tới đâu, hay session nào được phép thấy state nào. |

## Findings

### High — F1: “Thin wrapper” chưa có invocation contract khả dụng

- **Location:** `phase-01-start.md:31-34,46-49,61-66,104-108`; `plans/reports/synthesis-260930-0905-skill-kit-selection.md:75`.
- **Flaw/failure condition:** P1 cho phép skill API, native tool hoặc authorized subagent nhưng không chốt route nào trên host, request/response/error schema, ai cấp quyền, hay enforcement của egress/recursion. Record nền còn xác nhận `ak` không có `run-skill`, agent-dispatch chưa phải skill API và chưa có consumer run. Cook vì vậy có thể chỉ trả `NOT_CALLABLE`, trong khi P2–P4 vẫn mô tả worker execution.
- **Suggested fix:** Thêm capability matrix theo host: route thật, input/output contract, caller authorization scope, allowlist, timeout/side-effect semantics và receipt. Nếu không có route thì package phải ở trạng thái `planning-only/NOT_CALLABLE`, chặn các acceptance phụ thuộc worker; không suy invocation từ tên hoặc `SKILL.md`.

### High — F2: Plan/cook authority và caller scope chưa đủ để chống stale/foreign resume

- **Location:** `phase-01-start.md:28-30,46-49,57-58`; `plans/reports/brainstorm-260930-0905-skill-kit-contract.md:17-20,73-77`.
- **Flaw/failure condition:** Plan có `draft|ready|blocked` và cook “được người dùng cho phép”, nhưng không có approval record/token, actor/caller identity, project/package binding, expiry, revocation hoặc lock. Một file plan đúng hash có thể bị caller khác, session cũ hoặc task khác resume; drift có thể chỉ làm mất gate sau khi worker đã được gọi.
- **Suggested fix:** Đặc tả immutable authorization record gồm `task_id`, `plan_hash`, input/profile/dependency hashes, caller scope, approver, timestamp/expiry, revocation và concurrency rule. Cook phải từ chối missing/expired/revoked/foreign approval trước resolve/worker; tách plan file khỏi approval receipt.

### High — F3: Thu gọn blueprint thành “mode” chưa có coverage gate; dễ mất full research pipeline

- **Location:** Blueprint liệt kê các capability riêng `literature-review`, `research-gap`, `research-methodology`, `peer-reviewer`, `comparison-engine`, `final-audit` tại `vietnamese-writing-research-skills-blueprint.md:68-91,451-533,865-908`; plan chỉ tạo các module P2 tại `phase-02-evidence-and-research.md:62-75,81-92` và gom mode ở `plans/reports/brainstorm-260930-0905-skill-kit-contract.md:35`.
- **Flaw/failure condition:** Không có bảng ánh xạ capability gốc → module/mode → input/output → worker route → fault/eval case. Request research-gap, methodology hoặc peer review có thể rơi vào generic reasoning/review mà vẫn bị coi là đủ scope; static contract pass nhưng chức năng yêu cầu bị mất.
- **Suggested fix:** Thêm coverage matrix bắt buộc cho toàn blueprint: mỗi capability ghi owner, mode name, contract, route, acceptance/fault cases và trạng thái included/deferred/blocked. P5 chỉ được `accepted-for-scope` khi mọi mục user đã chọn có route/evidence; không tự cắt scope.

### High — F4: Pure-prose/creative bypass có thể bỏ sót factual claim mới

- **Location:** `phase-03-vietnamese-and-english-writing.md:38-44,50-54,76-80,100-102,131-132`.
- **Flaw/failure condition:** Brief tự chọn “no factual change” để bỏ P2, nhưng plan không có preflight độc lập xác định writer đã thêm fact/claim hay chỉ sửa câu. Một task gắn nhãn pure-prose vẫn có thể chứa ngày, tên, số liệu hoặc claim mới và đi thẳng tới `draft`; fidelity chỉ nói tới “supplied facts”.
- **Suggested fix:** Khóa `content_mode` trong approval; chạy factuality/claim preflight và human escalation trước khi bypass. Chỉ cho phép pure-prose khi không có claim mới; hễ có factual delta thì chuyển P2, giữ fiction marker và status `evidence-pending` nếu chưa đủ evidence.

### High — F5: Venue/ranking/source conflicts chỉ được “báo” nhưng chưa có blocking precedence

- **Location:** `phase-02-evidence-and-research.md:34-42,72-75,104-107`; `plans/reports/brainstorm-260930-0905-skill-kit-contract.md:55-57`; `phase-04-slides-and-scientific-visuals.md:68-70`.
- **Flaw/failure condition:** Plan yêu cầu một profile đích, tách mentor/project overlay và báo conflict, nhưng không định nghĩa trạng thái conflict, owner quyết định, precedence, freshness của policy/ranking hay cách chặn downstream. Khi journal rule, reporting checklist và mentor rule lệch nhau, implementation có thể vô tình lấy union/điều kiện lỏng nhất; Q1/Q2 hoặc “compliant” bị pass sai.
- **Suggested fix:** Thêm profile resolution record với layer/hash/revision/freshness; conflict hard-block thành `CONFLICT|AUTHOR_INPUT_NEEDED`, không union. Tách source eligibility, journal ranking và reporting checklist thành policy owners riêng; reset profile theo task.

### High — F6: Human gold/holdout là blocker thực tế nhưng chưa có operational entry gate

- **Location:** `phase-05-evaluation-and-packaging.md:28-33,48-50,96-108,141-142,173-177`; `plan.md:62-70`.
- **Flaw/failure condition:** Plan đã ghi rõ quyền, reviewer và budget còn pending (không nên coi là đã pass), nhưng chưa quy định điều kiện tối thiểu để P5 bắt đầu: reviewer availability/independence, sample size, inter-rater/disagreement, consent, confidentiality, holdout access và xử lý thiếu rater. Không có các điều kiện này, “human gold/holdout” chỉ là tên fixture và không thể đóng gate taste/EN/visual/release.
- **Suggested fix:** Thêm `HUMAN_GATE_BLOCKED` preflight trước mọi quality claim: named reviewer roles, consent/right-to-use, split/size/rotation, annotation rubric, disagreement/abstention rule, access/retention và budget. Nếu thiếu người/quyền, chỉ report deterministic guards; không claim personalization, gold hoặc release readiness.

### High — F7: Upstream update policy thiếu impact map/closure semantics, dễ freeze hoặc accept sai

- **Location:** `phase-01-start.md:38-40,109-110,166-167`; `phase-05-evaluation-and-packaging.md:37-40,63-65,109-111`; `plans/reports/synthesis-260930-0905-skill-kit-selection.md:50-58`.
- **Flaw/failure condition:** Plan yêu cầu hash instruction/reference/script/dependency closure và requalify “capability bị ảnh hưởng”, nhưng chưa định nghĩa closure traversal, digest algorithm, shared-dependency impact map, snapshot retention/permission hay acceptance owner. Closure quá rộng sẽ biến mọi upstream update thành freeze; closure thiếu sẽ để candidate mới chạy dưới accepted label.
- **Suggested fix:** Đặc tả immutable closure manifest/digest, dependency-to-capability graph, change impact states, qualification owner/case set và snapshot retention. Candidate chỉ đổi accepted sau receipt/eval của capability bị ảnh hưởng; không mutation global và không dùng fallback không tồn tại.

### Medium — F8: English-authored instruction chưa có thiết kế đo đủ để tách hiệu ứng

- **Location:** `phase-03-vietnamese-and-english-writing.md:42-44,143-145`; `phase-05-evaluation-and-packaging.md:28-31,48-50,58-69`.
- **Flaw/failure condition:** Plan đúng khi nói English instruction không tự là bằng chứng, nhưng “cùng task, kiểm soát instruction/output language” chưa chỉ rõ giữ cố định model/worker/runtime/context, thứ tự/randomization, blind rating, sample power hay effect uncertainty. Kết quả sau này không thể quy kết instruction language thay vì upstream drift, prompt/context hoặc reviewer.
- **Suggested fix:** Thêm matched factorial/A-B protocol: cùng input/profile/worker/model/runtime/budget, chỉ đổi instruction language, output language cố định; blind human/domain scoring, raw error classes và uncertainty. Không kết luận English tốt hơn nếu thiếu comparator hoặc rater.

### Medium — F9: Evidence/asset/private-sample retention chưa thành contract có thể kiểm

- **Location:** `phase-02-evidence-and-research.md:64-66,149-156`; `phase-05-evaluation-and-packaging.md:60-62,98-100,152-153`.
- **Flaw/failure condition:** Reader/evidence cần excerpt, values, notes, figure/table links; package cần generated artifacts/receipts, nhưng chưa có field-level storage class, excerpt/full-text limit, access control, retention/deletion hoặc artifact allowlist. Khi đóng package, full text, private draft hoặc licensed figure có thể lọt vào manifest/receipt dù plan nói “redact”.
- **Suggested fix:** Định nghĩa storage/egress matrix theo source/license: metadata/hash vs permitted excerpt vs private transient; retention/deletion owner, access scope và package allowlist. Gate packaging khi thiếu rights/retention evidence, không chỉ dựa vào redaction.

## Unresolved questions

1. Host nào có callable route thật cho từng capability, và caller authorization/egress được host enforce ở đâu?
2. Ai là owner của approval/registry/profile state, lifetime/namespace nào áp dụng khi hai task/session chạy đồng thời?
3. Reviewer, holdout rights/size, venue-policy source/freshness và accepted snapshot retention sẽ được cấp trước P5 hay giữ package ở trạng thái blocked?

