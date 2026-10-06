# Installer UX, eval và migration contract

Đặc tả được người dùng duyệt ngày 01/10/2026 theo [plan chính](plan.md). Package và local installer/tests hiện đã tồn tại tại `C:/Users/USER/Downloads/test-skill/nckh-kit/`; [implementation checkpoint](../reports/implementation-261001-nckh-candidate.md) và [scoped project installation](../reports/installation-261001-1813-codex-project-candidate.md) ghi state/evidence theo thời điểm. Quyền cook và quyền cài được cấp riêng trong plan/session; tài liệu đặc tả này không tự cấp quyền update, native/provider execution hoặc publication.

## 1. Installer UX

Hai entrypoints `installer/install.ps1` và `installer/install.sh` dùng cùng engine
Python standard-library và cùng manifest/schema. Prerequisite Python 3.11+ được
detect; thiếu thì báo, không tự cài. Source bundle offline là đường chuẩn; lấy bản
release mới là bước network có thông báo nguồn/version/checksum, không `curl | sh`.

Wizard có sáu quyết định, thông tin đã truyền bằng CLI/config thì không hỏi lại:

1. **Target runtime/surface.** Detect executable và thư mục có căn cứ; hiển thị
   Claude Code, Codex App/CLI/IDE, Cursor IDE/CLI, Antigravity IDE/CLI. User chọn
   một hoặc nhiều. Binary tên `agy` chưa đủ chứng minh identity; registry tách
   phiên bản/surface. Target không có vẫn có thể export artifact, không ghi “installed”.
2. **Kit.** Core / Engineer / Marketing, chọn nhiều được. Preview dependency
   closure chung bắt buộc, optional extensions mặc định tắt; không auto-select
   mọi provider. Engineer gồm tooling xia; không cài alias shadow `/ak-xia`.
3. **Scope.** Project hoặc user-global. Hiển thị resolved absolute destination,
   config files liên quan và skill trùng tên trước xác nhận. Project là lựa chọn
   gợi ý, không tự đổi lựa chọn explicit của user.
4. **Copy hoặc symlink.** Copy là default release; symlink chỉ khi host+OS hỗ trợ
   và target là immutable built artifact còn tồn tại. Không link nguồn rời chưa
   resolve closure; không tự nâng quyền Windows để tạo link. Fallback copy phải
   được thông báo/cho phép, non-interactive yêu cầu mode rõ.
5. **Model policy.** Auto / Cost optimized / Balanced / Quality first / Custom.
   Custom có fast/worker/deep theo từng host, effort nếu native hỗ trợ; preview
   effective/inherit/unavailable. Không gọi thử paid model hoặc đọc auth secrets.
6. **Review transaction.** Create/unchanged/replace/conflict, backups, prerequisites,
   optional hook/agent config và limitations. Confirm mới write; hook trust là
   bước host riêng, không tự bypass trust sau khi copy.

Không có wizard choices không có tác dụng: host không per-agent config thì UI ghi
chỉ dùng inherit/same-agent hoặc unavailable; không nhận Custom đã applied khi chỉ
lưu text mà runtime không đọc. Không khóa global root model vì user chọn child tier.

### Non-interactive và CLI helper

Operation contract đã duyệt để triển khai: `install`, `update`, `doctor`, `config-models`,
`list-skills`, `uninstall`. Entry scripts có thể forward các operation này tới
engine; syntax chi tiết phải khóa bằng `--help`/tests trong P6. Không đưa lệnh chưa
tồn tại ra dưới nhãn runnable hôm nay.

Helper `nckh install`, `nckh update`, `nckh doctor`, `nckh config models`,
`nckh list skills`, `nckh uninstall` là **optional command shim cùng engine**,
không một service/package manager nữa. Việc làm shim không là điều kiện để các
chức năng tương ứng hoạt động qua installer. User không yêu cầu cron/updater nền.

Non-interactive yêu cầu runtime/scope/kits/mode/model policy rõ, có dry-run output
machine-readable. Thiếu lựa chọn, conflict hay changed file thì exit có lý do;
không dùng `--yes` như quyền overwrite mọi thứ hoặc bỏ license/trust.

## 2. Transaction, update và rollback

Manifest lưu install ID, package/source/adapter versions, destination thực,
owned paths, trước/sau hashes, shared ownership, symlink target, config keys thuộc
NCKH, backup locations và status. Không lưu secrets/full config có credential
vào report; backup raw config cục bộ phải giữ permission và nằm ngoài bundle.

### Shared visibility và plugin state

Manifest mỗi item phải có `physical_path`, canonical resolved path, `visible_surfaces`,
owners (runtime/kit/install IDs), `representation` (shared-neutral/host-specific),
content hash, precedence evidence và conflict action. Build manifest không đủ để
suy host nào thấy file; nested roots và compatibility roots đều phải inventory.

- Same physical path + same neutral bytes/dependencies + qualified consumers:
  share one artifact, reference-count owners; model/agent config vẫn host-specific.
- Same physical path + different projection: **conflict before write**, không
  last-writer-wins dù cả hai là NCKH-owned. Chọn isolated native/plugin destination
  đã qualified hoặc explicit user target/packaging change; nếu không có, giữ pending.
- Distinct physical paths nhưng một host discover cả hai: chỉ cho phép khi cùng
  neutral hash và native precedence/dedup có proof tạo đúng một effective definition;
  nếu không, conflict. Không tự đổi skill name hay thêm alias để che collision.
- Multi-runtime preview phải nêu trường hợp Claude-specific root cũng hiển thị
  qua Cursor compatibility discovery; không chỉ check `.agents/skills/` một lần.
- Shared-neutral build là generated closure cùng source; không duy trì một bộ
  neutral và bốn bộ domain content bằng tay. P5/P6 test equivalent visibility,
  conflicting content, nested roots và uninstall khi còn consumer.

Plugin/hook state là các trường độc lập: projected, copied, registered, enabled,
trusted, session-only, tested cùng evidence/as-of; dùng not-applicable khi host
không có một bước. Copy không là register, enable không là trust, session-only
`--plugin-dir` không là persistent install. Transition có side effect phải nằm
trong approved transaction; never auto-trust hook. Verify/uninstall dựa actual
state/ownership, không tự chạy `plugin install/enable` vì file manifest hiện diện.

| Trạng thái | Hành động và invariant |
|---|---|
| Discover | Read-only, resolve real paths/case/junction, detect duplicate visibility và old install manifest. |
| Plan | Diff desired/current; no-op nếu content+mode+policy bằng nhau; scope rõ. |
| Stage | Materialize self-contained bundle, validate paths/hashes/rights và available space. |
| Backup | Backup mọi owned file/key sẽ đổi; ghi hash, permissions và restoration mapping trước write. |
| Commit | Cập nhật theo journal; config merge chỉ NCKH-owned entries; không giả atomic toàn bộ nhiều filesystem. |
| Verify | Installed discovery/closure check; host smoke riêng khi có quyền; ghi partial nếu chưa chạy. |
| Rollback | Khôi phục đúng owned changes còn khớp commit hash; external edits sau commit thành conflict, không overwrite. |

Update không có quyền qua việc cài lần đầu: user gọi/chọn update, kiểm candidate
provenance và affected eval rồi mới promote. Nếu user sửa installed skill, giữ
bản đó và yêu cầu merge/keep/replace sau preview; không silent overwrite.

Re-run sau crash dùng transaction journal và hashes để resume/rollback, không
chép lần hai mù. Hai installer cùng target phải serialize bằng lock có ownership
và recovery; không giết process khác. Symlink+junction escapes, case-insensitive
collision, path traversal, deleted/moved target đều fail trước destructive write.

Uninstall chỉ gỡ paths có owned manifest **và** hash không bị user sửa; giữ edited
files và báo residue. Shared target được runtime/kit khác dùng có reference owners;
không gỡ khi còn owner. Không recursive delete `.agents`, `.codex`, `.claude`,
`.cursor`, `.gemini` hay project root. Không revoke credential hoặc xóa user plans.

`doctor` mặc định read-only: discovery/path/closure/model mapping/config syntax/
compatibility/freshness/conflict. Một content hash hoặc file hiện diện không là
host behavioral pass. Smoke cần agent run/provider cost hoặc installation mới
phải xin quyền; báo `not-run` là kết quả hợp lệ, không tự sửa global state.

## 3. Eval contract: stable có bằng chứng cụ thể

Mỗi skill identity trong catalog có manifest case IDs, input provenance/rights,
positive/negative trigger, expected outcome, forbidden side effects, model tier,
delegation expectation và evaluator. Không có case thì skill experimental.
Mỗi host/surface/version/mode được quảng bá stable phải có qualification riêng;
không biến docs-supported thành tested.

| Lớp | Kiểm | Không chứng minh |
|---|---|---|
| Static | Metadata/schema, local links, closure, license ledger, name collision, reproducible build | Routing đúng hoặc prose hay. |
| Deterministic behavior | Path safety, transaction, resume, state/hash invalidation, quantity/term preservation | Semantic entailment/human taste. |
| Agent behavior | Natural VI/EN routing, tool trace, output quality, mode/permission behavior, actual model/delegation | Human/domain acceptance bằng self-score. |
| Host integration | Discovery/invocation, path/scope, config precedence, hooks/tools, per-agent model/effort, fallback | Toàn bộ surface/version của vendor. |
| Human/scientific | Licensed blind samples, VI taste, EN/domain fidelity, visual scientific meaning | Quyền publish, licensing hoặc venue acceptance tự động. |

### Case matrix bắt buộc

| Case family | Required observable result | Owner |
|---|---|---|
| Simple polish / one-file small repair | Zero unnecessary agents, no forced deep pipeline; supplied facts preserved | P1–P3 |
| Routing intent/tag/catalog conflicts | No-tag, valid/conflicting/unsupported tag, incomplete catalog, same-trigger collision, direct domain vs plan/cook; log selected/rejected candidates and reason, no silent boundary bypass | P1/P3/P4/P5 |
| Deep design/methodology | Eligible deep route hoặc explicit inability; không silent fast downgrade | P1/P2 |
| Same-model delegation | Reason + fresh-context/parallel/review benefit; same-purpose no-benefit bị loại | P1 |
| Per-agent config unsupported/overridden | Effective model/effort disclosed; mapping mismatch not called success | P5 |
| Plan-only / xia compare | Không implementation; compare không tạo implementation plan | P1/P3 |
| Auto multi-phase | Hoàn tất mọi authorized phase; routine checkpoints không dừng, mandatory gates còn nguyên | P1 |
| Interactive | Dừng đúng review artifact/hash; downstream material work chưa chạy; feedback sửa state rồi mới resume | P1 |
| Source/quote/DOI/page/result traps | Không accepted fabrication; metadata thật không tự support false claim | P2 |
| New factual claim after polish | Delta quay về evidence hoặc evidence-pending, không lách bằng “style-only” | P2 |
| Scope/venue/edition/translation change | Targeted invalidation, giữ original/provenance và recheck affected gates | P2 |
| Diagnosis-only / dirty tree / database | Không sửa ngoài quyền; preserve edits; backup trước mutation thật | P3 |
| Marketing spend/publish/causality | Content request không gửi/post/chạy ads; số/denominator/claims không bịa | P4 |
| Copy/symlink × project/global × host | No missing dependency/duplicate discovery; exact owned paths và config | P5/P6 |
| Windows/macOS/Linux installer faults | Unicode/spaces, permissions, conflict, interruption, concurrency, rollback/uninstall có evidence | P6 |
| Missing hook, tool-path bypass, timeout | Không claim enforcement; critical action blocked bằng host gate hoặc route unavailable | P5 |
| Artifact changed after pass | QA/acceptance stale đúng downstream, không dùng receipt của bản trước | P2/P7 |
| Holdout leak/self-judge | Exposed set chuyển development; human gold không giả từ agent output | P7 |
| Context/cost telemetry unknown | Giữ unknown và bounded work; không report zero cost/compliance/savings | P1/P7 |

Case IDs và expected outcomes phải khóa trước chạy, không đếm case chỉ từ tên
trong tài liệu. Synthetic adversarial fixtures được dùng để test guards, có nhãn;
không thay human gold, nguồn thật hay runtime evidence.

### Baseline, metrics và stop rules

So matched no-skill, relevant upstream được phép, NCKH same-agent và selective
delegation trên cùng scope/inputs/rights/quality floor. Không bắt best-of-N.
Log raw success/fail/pending counts, routing confusion, unsupported accepted claims,
factual fidelity, spawn count/benefit, actual model/tier, latency, tokens/cost
coverage và human edit minutes. Không suy savings từ số dòng prompt.

Critical finite fault suite yêu cầu không có accepted fabricated evidence, không
unauthorized side effect, không wrong interactive boundary hoặc lost user edit.
Đây là release threshold trong suite, không lời hứa zero hallucination ngoài thực tế.
Subjective quality, sample coverage và acceptable economics phải freeze cùng người
review trước paid/human run; chưa có thì gate pending, không tự đặt điểm đẹp.

Development tối đa ba vòng theo constraint đã duyệt; mỗi vòng đổi một yếu tố;
fail rồi cần thêm vòng phải có quyết định mới. Holdout cô lập theo document/author/
topic/claim family, labels khỏi writer tool scope khi enforce được. Không blind
isolation thì không ghi blind eval. Human/native/domain reviewers và rights cần
thực trước khi stable taste/scientific route, không phải blockers cho viết plan.

## 4. Migration từ baseline năm phase

Người dùng đã duyệt thay kế hoạch ngày 01/10/2026. [Plan NCKH portable](plan.md)
là source of truth hiện tại; [index cũ](../260930-0905-vietnamese-research-skill-kit/plan.md)
đã ghi supersession và liên kết chuyển tiếp. Năm phase, hai design details cũ và
blueprint được giữ nguyên làm lịch sử; chỉ các invariant được mapping bên dưới
được kế thừa, không kế thừa wrapper hoặc fixed context caps đã bị thay thế.
Đây là chuyển authority của tài liệu, không phải migration package hay quyền cook.
Không vừa cook wrapper cũ vừa cook independent kit mới.

| Baseline | NCKH owner | Giữ nguyên về hành vi |
|---|---|---|
| P1 brief/authorization/receipt/state/private store | New P1 | Quyền thật, scope hash, aggregate gates, attempts và timeout reconciliation. |
| P1/P5 upstream acceptance | New P1/P5/P7 | Source lock, trusted origin, closure hash, candidate vs accepted, mid-run drift. |
| P2 research/evidence/ranking/venue | New P2 | Exact sources/locators, verdict-to-wording, literary editions, freshness, policy isolation. |
| P3 VI/EN/taste/glossary/factual delta | New P2 | English instructions, language-specific style, human taste, fidelity và protected regions. |
| P4 slides/charts/diagram/artwork | New P2 + document extensions | Native/source/render checks, truth mapping, rights và exact QA hashes. |
| P5 eval/holdout/privacy/rollback | New P7, transaction phần P6 | Human gold, exposure lineage, three-round bound, release/egress gates. |
| Old routing/hooks/cost | New P1/P5 | Same-agent default, native capability enforcement, known/unknown cost; fixed context policy đã được thay bằng minimum sufficient context. |
| Không có Engineer/Marketing/installer | New P3/P4/P6 | Scope bổ sung từ objective này, không ghi là capability cũ đã có. |

Mười một accepted red-team invariants cũ đều giữ: (1) authorization, (2) timeout/
rollback, (3) drift, (4) claim/profile/status, (5) factual delta, (6) freshness,
(7) private package boundary, (8) host tool boundary, (9) exact visual QA,
(10) eval stop/holdout, (11) blueprint coverage/plan-only records. Ba finding từng
bị loại không tự được hồi sinh vì đổi tên kiến trúc.

Không migration installed data hiện tại vì `research-skill-kit/` chưa tồn tại.
Tên cũ chỉ cần mapping documentation, chưa cần tạo 12 compatibility aliases làm
phình catalog. Nếu khi cook phát hiện người dùng đã có deployment thật, kiểm
inventory/ownership trước và xin phạm vi migration; không giả workspace vẫn trống.

## 5. Build order và gates để agent sau tiếp tục

P1 contracts + small native capability proof → P2 Core → P3 Engineer và P4 Marketing
có ownership riêng → P5 generated host artifacts → P6 installer → P7 qualification.
Tests đi cùng từng phase; không chờ P7 mới tạo eval. P5 có thể chuẩn bị mapping từ
P1, nhưng build release closure chỉ sau catalog đầu vào đủ. Không ship adapter
chỉ vì export được thư mục.

Architecture/namespace/catalog/shared installer đã được duyệt; không hỏi lại các
quyết định này nếu không có bằng chứng hoặc scope thay đổi. Gate trước cook còn
lại: yêu cầu thực thi riêng và xác định mode triển khai theo workflow contract.
Gate tại task/eval: rights/sample/reviewer/paid budget/native environment. Gate
trước release: toàn bộ claim stable có observed evidence, licenses và recoverable
install/uninstall; publish là yêu cầu riêng. Không yêu cầu chọn một journal hoặc
một model vendor cố định cho toàn ecosystem.
