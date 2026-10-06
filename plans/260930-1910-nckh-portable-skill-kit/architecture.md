# NCKH Skill Kit — kiến trúc đã duyệt

Thiết kế ngày 30/09/2026, được người dùng duyệt ngày 01/10/2026, Asia/Saigon.
Đây là thiết kế đã duyệt, không phải package đã triển khai; quyền cook vẫn chưa có.
Đọc cùng [catalog](skill-catalog.md), [workflow/model](workflow-and-model-routing.md),
[runtime matrix](runtime-compatibility.md) và [installer/eval/migration](installer-evaluation-migration.md).

## 1. Kết luận và phạm vi

Đã duyệt chuyển từ wrapper bắt buộc AgentKit sang bộ NCKH có source-of-truth riêng,
chọn lọc ý tưởng upstream, kiểm license và viết lại hợp đồng phù hợp. Adapter gọi
AgentKit hoặc công cụ đang cài là extension tùy chọn, không là dependency bắt buộc.
Đây là **kiến trúc hiện hành**, thay quyết định wrapper cũ theo [approval record trong plan](plan.md).

Giữ toàn bộ research/evidence, Việt–Anh, literary studies, Q1/Q2 theo task,
venue isolation, taste và scientific visuals đã có. Bổ sung Engineer, Marketing,
bốn host adapters, model profiles, installer và đánh giá từng skill. Không clone
AgentKit, xây agent server, tự cài MCP, sửa runtime global, gọi paid eval hay publish.
Không có cờ `--yagni`; việc gộp skill chỉ đổi owner/giao diện, không bỏ chức năng.

## 2. Critique những gì thực sự có trên đĩa

Workspace có blueprint **v1.0** và plan năm phase, không có tài liệu mang định danh
V2/V3 đã xác minh. Vì vậy đây là critique baseline hiện có; không dựng một lịch sử
V2/V3 giả. Nếu V2/V3 là hai tệp khác, cần đối chiếu bổ sung trước tuyên bố đã review chúng.

| Điểm trong baseline | Giữ hoặc đổi trong thiết kế đã duyệt | Vì sao |
|---|---|---|
| Blueprint tách nhiều tên đọc/claim/citation/fact/polish | Gộp thành research, evidence, write với modes có owner | Ít entrypoint hơn nhưng vẫn kiểm riêng identity, entailment, quote và fidelity. |
| Blueprint `verified: true` và taste scalar | Không dùng như gate tổng hợp | Metadata match không chứng minh claim; model taste score không phải human gold. |
| Wrapper + live AgentKit catalog là đường chính | NCKH source riêng, extension upstream optional | Portable bundle phải hoạt động khi không có AgentKit và khi catalog thay đổi. |
| Hai tên `research-plan`/`research-cook` | Chọn `nckh-plan`/`nckh-cook` | Hai primitive áp dụng cả nghiên cứu, kỹ thuật và marketing. |
| Hard/soft context 20k–40k và phần trăm cố định | Minimum sufficient context theo host/model/task | Không đồng nhất window của các model; không cộng window nhiều agent thành một context thật. |
| Cùng model bị gọi chung là non-independent | Ghi riêng model, context, nguồn và human independence | Fresh-context review cùng model có ích nhưng không phải reviewer khoa học độc lập. |
| Runtime/package scope chưa chốt | Ma trận theo surface/version và capability probes | App, CLI, IDE và agy không được gộp thành một “hỗ trợ” chung. |
| Chưa có Engineer/Marketing/installer | Hai catalog gọn, build closure và transaction installer | Đây là scope mới thực chất, không thể coi plan năm phase cũ đã bao phủ. |
| Eval nằm chủ yếu cuối roadmap | Mỗi skill có eval ngay phase sở hữu; cuối chỉ qualification | Lint/link pass không được dùng thay behavioral, human hoặc host acceptance. |
| Source/claim provenance, authorization, timeout, privacy, visual QA | Giữ và phân owner lại | Đây là các ràng buộc đã duyệt; thay tên không xóa invariant. |

Không khẳng định cấu trúc mới tự giảm hallucination/cost. Đây là giả thuyết thiết kế
cần matched eval; chưa có kết quả runtime hoặc human taste trong lượt này.

## 3. Bảy loại thành phần, không dùng thay nhau

| Thành phần | Sở hữu | Không sở hữu | Vị trí source dự kiến |
|---|---|---|---|
| Policy | Không bịa; quyền, provenance, uncertainty, originals | Trình tự mọi tác vụ hoặc lựa chọn model | `core/policies/` |
| Skill | Outcome reusable, trigger, inputs/outputs, stop rules | Một runtime hoặc một model bắt buộc | `skills/{core,engineer,marketing,tooling}/` |
| Agent | Specialist packet, context/tool scope riêng khi có lý do | Mọi skill; automatic fan-out | `agents/` |
| Model profile | Tier → model/effort có thật theo runtime và quyền | Chất lượng đã được chứng minh; quyền tăng phí | `core/profiles/models/` |
| Script/tool | Hash, validate, render, copy, diff deterministic | Quyết định claim có đúng về khoa học | `installer/`, `tests/`, script cục bộ skill |
| Workflow | Thứ tự, state, review/approval/resume và fan-in | Implementation riêng cho mỗi host | `core/workflows/` |
| Eval | Case, rubric, trace, pass/fail/pending, human review | Prompt tự chứng thực, evidence giả | `evals/` |

Mỗi skill có một owner/outcome rõ. Mặc định cùng agent đọc đủ instruction rồi làm;
chỉ tạo specialist khi hợp đồng delegation cho thấy lợi ích. Deterministic script
không được bọc thêm LLM agent để tạo vẻ “multi-agent”.

## 4. Nguồn duy nhất và artifact self-contained

```text
Canonical skill + selected policy/contracts + agent profiles
                       |
              dependency closure build
                       |
            host-specific immutable artifact
                       |
        install preview -> user choice -> transaction
                       |
        observed host capability -> task -> evidence -> acceptance
```

Build phải resolve closure theo manifest có revision/hash, không dựa vào đường
dẫn máy tác giả. Cấm missing references, dependency cycles, case-fold collision,
đường dẫn ra ngoài bundle và secret/private fixtures. Shared material chỉ có một
bản source; build có thể materialize bản sao trong `references/_shared/` của từng
skill nếu host chỉ bảo đảm skill-local references. Đây là output sinh tự động,
không phải bốn bản skill bảo trì bằng tay.

Không nhúng mọi guideline vào mọi `SKILL.md`. Metadata ngắn để chọn skill; body
là workflow mạnh; reference chỉ đọc khi route cần. Khi chọn một skill, phải đọc
đủ body và references bắt buộc. Budget không cho phép cắt các luật bắt buộc.

Hai chế độ tiêu thụ:

- **Standalone folders:** artifact từng host đã đủ dependency; cùng-agent là
  fallback chuẩn. Không cần AgentKit, service nền hoặc account mới.
- **Native plugin:** đóng gói cùng artifact khi host/version hỗ trợ và người dùng
  chọn. Plugin manifest/hook schema là adapter, không là core content authority.

`core/` là thư viện policy/contracts, khác **Core kit** là nhóm skill. Chọn Engineer
hay Marketing tự thêm closure chung tối thiểu và hiển thị rõ trong preview; không
tự cài toàn bộ research/visual extensions. Full selection có 37 skill identities:
10 Core + 13 Engineer + 13 Marketing + 1 tooling; tooling xia được chọn cùng Engineer.
Không phải mọi identity đều nạp full instruction cùng lúc.

## 5. Evidence và state tối thiểu

Pipeline factual: **source → evidence → claim → synthesis → prose**. Bản thảo có
sẵn đi qua audit/factual delta, không phải xóa rồi viết lại mọi thứ. Pure style
edit không tự chạy literature search; facts được cung cấp vẫn phải giữ nguyên.

| Record | Nội dung tối thiểu |
|---|---|
| Source | ID, origin, bản/version/hash đã đọc, access level, rights, status/as-of; DOI chỉ khi có thật. |
| Evidence | Source/version, excerpt hoặc value gốc, locator theo loại, context, OCR/visual-check status. |
| Claim | Statement/type/scope, evidence IDs, support/contradiction/insufficient/unverified, allowed certainty. |
| Profile | Venue/year/track và revision; style/locale riêng; task-scoped glossary; không union venue. |
| Task state | Plan revision/hash, scope, mode, authorization reference, phase/artifact gates, outstanding attempts. |
| Receipt | Host/surface/version, logical entrypoint/mode và actual invocation; skill/agent/plugin identities; requested/resolved/effective model+effort hoặc unknown; permission/sandbox, tool/egress trace, exit/output status (N/A nếu host không có), input/output/closure hashes, checks, cost coverage, evidence class và limitations. |

Native config/plugin lifecycle và model proof có field contracts trong [workflow](workflow-and-model-routing.md), [runtime](runtime-compatibility.md) và [installer](installer-evaluation-migration.md). Raw transcript/credentials không nằm trong public receipt; link tới private evidence qua authorized opaque reference khi cần.

Lịch sử nội dung và trạng thái là hai thứ khác nhau: giữ record cũ; ghi invalidation
và revision mới khi nguồn/profile/artifact đổi. Không sửa lại lịch sử thành pass.
`accepted-for-scope` cần tất cả gate bắt buộc pass; `human-reviewed` chỉ ghi sự kiện
review, không ghi đè fail/pending. Không tự loại deliverable khó khỏi scope.

Personal corpus, manuscripts, full text, holdout labels và raw receipts ở private
task store, ngoài `dist/`. Source công khai không tự cho phép redistribution.
Licensing/release, paid APIs, external writes và venue submission giữ gate riêng.

## 6. Repository dự kiến

Root package dự kiến: `C:/Users/USER/Downloads/test-skill/nckh-kit/`.
**Chưa tạo thư mục này.** Các đường dẫn bên dưới là sản phẩm cook tương lai.

```text
nckh-kit/
├── core/
│   ├── policies/
│   ├── contracts/
│   ├── workflows/
│   ├── profiles/{models,style,venue}/
│   └── registry/{catalog,source-lock,compatibility}/
├── skills/
│   ├── core/
│   ├── engineer/
│   ├── marketing/
│   └── tooling/nckh-xia/
├── agents/
├── scripts/build-artifacts.py
├── adapters/{claude,codex,cursor,agy}/
├── extensions/
│   ├── frameworks/
│   ├── providers/
│   ├── native-documents/
│   └── upstream-agentkit/
├── installer/
│   ├── install.ps1
│   ├── install.sh
│   ├── nckh-installer.py
│   ├── manifests/
│   └── schemas/
├── evals/
│   ├── {cases,rubrics,baselines,protocols}/
│   └── run-evals.py
├── tests/{contracts,evidence,engineer,marketing,build,installer,runtime,release}/
├── docs/
└── dist/{claude,codex,cursor,agy}/
```

Đã chọn một engine Python standard-library, yêu cầu Python 3.11 trở lên; hai shell
entrypoints chỉ detect, thu lựa chọn và gọi cùng engine. Thiếu Python thì dừng
với prerequisite rõ, không tự download. Skill đã cài instruction-only không cần
Python để dùng; script capability riêng khai báo dependency riêng. Đây là trade-off
nhỏ gọn/DRY so với installer không prerequisite và phải được hiển thị trước install.
P1 kiểm prerequisites trên ba OS; cùng manifest, transaction contract và tests,
không duy trì hai catalog, hai policy hay hai bản business logic khác nhau.

## 7. Quyết định đã duyệt ngày 01/10/2026

1. NCKH độc lập với AgentKit bắt buộc; upstream trở thành nguồn ý tưởng hoặc extension.
2. Namespace `nckh-*` cho 37 skill identities, gồm `/nckh-xia` riêng; giữ `/ak-xia` của AgentKit, không shadow bằng bản khác.
3. Hai primitive plan/cook; literature review là mode research, brainstorm thuộc plan.
4. Giữ visuals làm một Core route gọn để không mất scope cũ; engines/provider cụ thể ở extensions.
5. Minimum sufficient context; profiles theo capability, không hard-code window/model ID.
6. Bốn host đều có qualification track; không gọi cross-runtime stable khi mới test một host.
7. Hai shell entrypoints dùng chung engine Python standard-library, prerequisite Python 3.11+, thiếu thì dừng và không tự cài.

Phê duyệt thiết kế và thay plan không cấp quyền implementation, cài đặt hoặc gọi eval trả phí.
