# Validation — NCKH portable proposal và baseline hiện có

> **Cập nhật 01/10/2026:** Người dùng đã duyệt thay plan; [NCKH portable](../260930-1910-nckh-portable-skill-kit/plan.md) là kế hoạch chính. Các mục 1–7 bên dưới giữ nguyên bằng chứng và trạng thái lịch sử ngày 30/09; approval hiện tại nằm ở mục 8. Không có quyền cook hoặc kết quả nghiệm thu triển khai mới.

As-of 30/09/2026, Asia/Saigon. Scope: research, critique và plan validation; **không implementation**.
Input authority là objective người dùng trong attachment và [plan gốc](../260930-0905-vietnamese-research-skill-kit/plan.md).
Output là [proposal riêng chờ duyệt](../260930-1910-nckh-portable-skill-kit/plan.md), không tự thay quyết định cũ.

## Kết luận

Plan cũ **hợp lệ về cấu trúc nhưng không đủ cho objective mở rộng**. Giữ lại nền
evidence/VI–EN/venue/visuals/authorization; cần redesign ownership, catalog, model
routing, runtime packaging và installer. Không recommend cook plan cũ cho scope mới.
Proposal có 7 phase, 37 skill identities và tests/evals theo phase; chưa có package
hoặc chứng cứ runtime/human quality của NCKH.

Không tìm thấy tài liệu định danh V2/V3. File thực có tiêu đề **Blueprint v1.0**;
trong đó có roadmap Version 0.1/0.2/0.3, không phải hai bản V2/V3 đã xác minh.
Không tuyên bố review những file chưa được cung cấp.

## 1. Evidence scope và validation method

- Đọc blueprint, index, cả năm phase cũ, hai design details và các accepted
  red-team/validation records; re-read active index sau compact.
- Đọc installed AgentKit selected skill bodies + manifests, nghiên cứu upstream
  public docs và official docs của bốn runtime; chỉ version/help probes, không
  consumer prompt, hook install hay paid run.
- Skill `ak-plan --validate` yêu cầu user xác nhận trước sửa quyết định/phase.
  Vì vậy chỉ append validation record vào index cũ; proposal/phase mới tách riêng.
- Old plan đã có Red Team Review với evidence: theo validate guard không giả chạy
  lại 15 behavioral checks mỗi phase đã duyệt. Review tập trung delta của objective.
- Proposal phase checks là kiểm contract/readiness: owner, dependency, future paths,
  validation oracle và safety. Future paths được đánh dấu rõ, không coi chúng là
  source/test đang tồn tại. New implementation contracts chưa có behavior để trace.

Evidence classes: `VERIFIED` với local/source/doc scope, `FAILED` khi baseline
không đáp ứng objective mới, `UNVERIFIED` cho consumer/runtime/human chưa chạy.
Documented capability không được đổi nhãn thành tested compatibility.

## 2. Findings phải đổi trong proposal, không tự sửa baseline

| # | Finding và evidence baseline | Đánh giá theo objective mới | Owner đề xuất |
|---|---|---|---|
| 1 | Old index L17 và routing design L18 chọn wrapper quanh AgentKit | FAILED: không có NCKH-owned portable source/closure và upstream optional như hướng mới | Architecture/P1/P5 |
| 2 | Old index L17, old P1 L127–128 chỉ research-plan/research-cook | FAILED: public namespace và three-kit workflow chưa được mô tả | Workflow/P1 |
| 3 | Old index L25, routing design L135–158 có 20k/40k và % caps | FAILED: trái yêu cầu mới không hard-code 40k; đây là policy từng được duyệt, chỉ đề xuất supersede | Workflow/model/P1 |
| 4 | Old P3 L58 và L161 gọi same-model critic non-independent | NEEDS REFINEMENT: giữ caveat human independence, bổ sung independence theo context/role/source; không cấm review cùng model có lý do | Model routing/P1/P2 |
| 5 | Old P1 L108 chỉ nói auto nếu có sau này không bỏ gate; chưa có full auto/interactive contract | FAILED: chưa đủ phase execution, meaningful review artifact và feedback/resume semantics | Workflow/P1 |
| 6 | Old index L37/L71 giữ runtime/package selection pending, old P1 L162 chỉ chosen runtime | FAILED FOR NEW SCOPE: yêu cầu giờ nêu đủ Claude/Codex/Cursor/Agy và per-surface differences | Matrix/P5 |
| 7 | Five old phases không có Engineer/Marketing catalogs hoặc tooling Xia đầy đủ | FAILED: research-only modules không bao phủ requested product | Catalog/P3/P4 |
| 8 | Five old phases không có two-shell installer transaction/update/doctor/uninstall UX | FAILED: không có owned manifests, idempotency/conflict/crash recovery acceptance | Installer/P6 |
| 9 | Old eval là no-skill/upstream/wrapper domain evaluation, không có per-skill/per-host three-kit coverage | FAILED: cần mở rộng eval, không bỏ human/holdout safeguards hiện có | P1–P7 |
| 10 | Blueprint v1.0 dùng source/page verified fields và taste score | DESIGN RISK, không bug đã chạy: phải tách identity/support/human quality; giữ các sửa đổi đã có trong plan cũ | Contracts/P1/P2 |

Không có kết luận “plan cũ sai hết”: accepted source/claim provenance, task-scoped
ranking/venue, literary primary text, factual delta, private store, real permissions,
timeout reconciliation, exact visual QA và human holdout được giữ.

## 3. Research conclusions có căn cứ

| Claim | Status và scope | Evidence |
|---|---|---|
| Workspace hiện chỉ có blueprint/plans, không phải package NCKH triển khai | VERIFIED local inventory; recheck trước cook | Blueprint + baseline/candidate inventory |
| AgentKit local manifests có 103 Engineer, 82 Marketing, union 146 unique IDs | VERIFIED manifest inventory, không bằng chứng đã chạy 146 skills | [AgentKit report](researcher-260930-1910-agentkit-port-evidence.md) |
| Installed ak-xia 1.0.1: compare report-only; port/improve plan-only | VERIFIED installed instructions + upstream documentation; chưa consumer-run | [Xia official guide](https://docs.agentkit.best/en/stable/kits/engineer/skills/xia), AgentKit report |
| Upstream latest/installed paid kit/public repo parity | UNVERIFIED; local 2.19.0 không tự là newest | AgentKit freshness limits |
| Codex desktop enabled skills có slash menu; CLI/IDE skill docs còn nêu /skills và $ | VERIFIED documentation; không giả UI đã mở trong lượt này | [Desktop slash docs](https://learn.chatgpt.com/docs/reference/slash-commands), [build skills](https://learn.chatgpt.com/docs/build-skills) |
| Codex per-agent model/reasoning, current native spawn surface | VERIFIED docs/tool availability; custom NCKH agent effective config chưa tested | [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [matrix](../260930-1910-nckh-portable-skill-kit/runtime-compatibility.md) |
| Cursor IDE launcher khác standalone Agent CLI | VERIFIED local help/version | [Runtime report](researcher-260930-1910-runtime-compatibility.md) |
| Agy CLI/IDE global skill roots khác nhau, custom agent aliases không phải tùy ý mọi model ID | VERIFIED docs scope; runtime model/config còn probe pending | Runtime report + [Antigravity skills](https://www.antigravity.google/docs/skills?tab=ide) |
| Hook events/error/tool coverage không portable và không complete enforcement | VERIFIED docs scope; NCKH enforcement chưa tested | Runtime report + [Codex hooks](https://learn.chatgpt.com/docs/hooks) |
| Cross-runtime NCKH execution, lower cost, VI taste quality, scientific validity | UNVERIFIED; không có benchmark/human/native evidence trong lượt này | Open gates, không claimed result |

## 4. Traceability đủ 12 output

| Requested output | Owning deliverable |
|---|---|
| 1. Critique V2/V3 hiện tại | [Architecture §2](../260930-1910-nckh-portable-skill-kit/architecture.md); chỉ actual baseline v1.0/unversioned plan, V2/V3 chưa được cung cấp. |
| 2. AgentKit + four runtime findings | [AgentKit](researcher-260930-1910-agentkit-port-evidence.md), [runtime research](researcher-260930-1910-runtime-compatibility.md), Codex section trong matrix. |
| 3. Compatibility matrix | [Runtime compatibility](../260930-1910-nckh-portable-skill-kit/runtime-compatibility.md). |
| 4. Proposed architecture | [Architecture](../260930-1910-nckh-portable-skill-kit/architecture.md), seven component types. |
| 5. Final proposed catalog | [Catalog](../260930-1910-nckh-portable-skill-kit/skill-catalog.md), 10 + 13 + 13 + 1. |
| 6. Plan/cook/Xia semantics | [Workflow](../260930-1910-nckh-portable-skill-kit/workflow-and-model-routing.md); upstream ak-xia preserved, nckh-xia proposed separately. |
| 7. Model-routing strategy | Workflow §4–6 + runtime matrix, five profiles and logical tiers. |
| 8. Installer UX | [Installer contract](../260930-1910-nckh-portable-skill-kit/installer-evaluation-migration.md) §1–2 + P6. |
| 9. Final proposed repository structure | Architecture §6; every future implementation subtree assigned in phases. |
| 10. Eval strategy | Installer/eval §3 + phase-owned tests + P7 qualification. |
| 11. Migration | Installer/eval §4 + P7, all 11 accepted invariants retained. |
| 12. Milestones/build order | [Short index](../260930-1910-nckh-portable-skill-kit/plan.md) + seven linked phases, 35 unchecked tasks. |

“Final proposed” chốt nội dung tài liệu để duyệt, không đồng nghĩa user-approved
hoặc stable. Expanded product scope không bị thu hẹp vì delivery lượt này chỉ Markdown.

## 5. Quyết định chưa được user duyệt

Một material architecture choice: dùng proposal độc lập thay wrapper bắt buộc
AgentKit, cùng namespace/catalog/shared installer đã mô tả. Trade-off: bớt phụ
thuộc runtime AgentKit nhưng NCKH phải tự sở hữu contracts, adapters, license,
tests và maintenance. Python 3.11+ giúp dùng một engine stdlib nhưng là prerequisite
cho installer; thiếu Python dừng, không tự cài. Đây không là quyền implementation.

Interview state: **chưa có câu trả lời mới**. Câu hỏi cần gửi khi bàn giao:
“Bạn có duyệt hướng NCKH độc lập với AgentKit, namespace/catalog và installer
chung trong bản đề xuất này để thay plan cũ không?” Không ghi một lựa chọn giả là
approval. Sau duyệt mới ghi supersession và propagation; cook là authorization riêng.

Human gates cho execution/eval giữ mở: corpus/sample/asset rights, reviewer và
protected holdout, runtime/OS lab, paid budget, actual model availability, task-specific
venue/ranking. Bốn runtime đã là required design scope, không hỏi lại có cần chúng không.

## 6. Kiểm tra thực tế trong lượt này

- `ak plan validate` baseline: exit 0, valid true.
- `ak plan validate` candidate: exit 0, valid true.
- `ak plan parse` candidate: 7 phases, 35 tasks, 0 done, 0% implementation.
  Files dùng pending; parser biểu diễn phase chưa làm là todo, không là completed.
- CLI scaffold tạo file thành công; cập nhật global AgentKit plan index báo access
  denied. Không đổi AGENTKIT_HOME, quyền hoặc runtime config để lách; local Markdown
  là canonical cho review. Không tuyên bố dashboard/global index đã đồng bộ.
- Baseline hash comparison trước append index: 9/9 đúng. Sau append, tám protected
  files (blueprint, five phases, two design details) vẫn giữ nguyên SHA-256; old
  index chỉ được thêm validation notice và links.
- Final static pass trên 19 Markdown files: 103 local links, 0 missing; 37 catalog
  rows, 37 unique IDs, 0 duplicates; 19 required case families; 0 scaffold
  placeholders. Candidate index 70 dòng, seven phase frontmatters đều pending.
- Seven phases đều có đủ 17 contract/readiness fields đã kiểm: title/frontmatter,
  pending status, priority, effort, dependency, context links, architecture,
  requirements, ownership, absolute paths, steps, todo, acceptance, future-validation
  label, test command, safety/rollback và next steps. Đây là 119 presence checks,
  **không phải 119 behavioral tests**.
- Final table-structure pass trên cả 19 files: 0 column errors. Một enum pipe
  trong runtime researcher report đã được escape; không đổi source semantics.
- Dependency map P1→P2→P3/P4→P5→P6→P7 đã rà không cycle; P3/P4 có ownership riêng,
  shared registry chỉ integrate tuần tự. Tám test suites đều là future paths,
  chưa tồn tại và **không được chạy trong lượt docs-only**.
- Không có live task-management mutation surface được tìm thấy; 35 checklist
  tasks là state authority, không tạo chat/issue giả để mô phỏng task hydration.
- Local journal được tạo và `ak journal validate` trả ok true; AgentWiki publish skipped.
- [Independent synthesis review](review-260930-1910-nckh-proposal-consistency.md)
  đã trả 9 findings; adjudication bên dưới. Không coi commands dự kiến trong phase
  là tests đã chạy. Native/human probes vẫn thuộc future execution, không yêu cầu
  thực thi chúng để hoàn thành objective nghiên cứu/thiết kế này.

### Adjudication của review độc lập

| Finding | Kết luận controller và thay đổi proposal |
|---|---|
| F-01 Xia namespace | Giữ pending user decision, không auto-adopt. Gate đã có trong architecture §7/workflow §3/index; đây là proposed public-contract choice, không lỗi đã implement. Không tạo alias shadow upstream. |
| F-02 UI/headless invocation | Bổ sung matrix cho ba logical entrypoints, tám surfaces và UI/menu/headless/implicit; native NCKH receipt của mọi cell còn unverified. |
| F-03 shared/compatibility roots | Bổ sung physical path, visible surfaces, owners, representation/precedence; neutral qualified sharing hoặc conflict-before-write. Cursor compatibility roots được liệt kê rõ; không last-writer-wins. |
| F-04 auto permissions | Bổ sung per-host preservation mapping và auto_policy fields; cấm blanket bypass/force từ auto, tool/egress coverage và mandatory approval tests. |
| F-05 model config/effective proof | Bổ sung target/request/encoding/resolution/observation contract; configured khác applied/effective, missing telemetry giữ unknown. |
| F-06 plugin lifecycle | Bổ sung projected/copied/registered/enabled/trusted/session-only/tested như fields riêng; không coi file-copy/session-load là persistent trusted install. |
| F-07 OS matrix | Bổ sung Windows/macOS/Linux design/fixture/native status và future lab owners; mọi native/installer cell pending. Không giảm scope để tạo pass. |
| F-08 routing conflicts | Thêm case family thứ 19: no-tag/valid/conflicting/unsupported tag, catalog thiếu, cùng trigger và direct skill vs plan/cook intent. |
| F-09 receipt dimensions | Mở rộng receipt host/surface/invocation/mode/model/permission/egress/plugin/exit/evidence dimensions; raw private material ở private store. |

P1/P5/P6/P7 đã nhận delta tương ứng; P2/P3/P4 boundaries không đổi. Những thay
đổi này chỉ làm rõ proposal của lượt này, không áp vào baseline đã duyệt. Không
đảo các quyết định đã verify: four-host design scope, same-agent default,
source-of-truth, human gates và no-code boundary vẫn giữ nguyên.

## 7. Whole-Plan Consistency Sweep

Delta set: wrapper → owned source; research-* → nckh-*; fixed caps → per-context
sufficiency; five → seven phases; research-only → three kits; generic runtime →
four host/surface adapters; vague auto → explicit two modes; Xia no-code/mode
semantics; tests with owners; installer transaction; same-model independence labels.

Rà toàn index và mọi phase, cả five design documents; occurrences thuật ngữ cũ
chỉ hợp lệ trong critique/migration/history. Protected baseline được giữ riêng nên
khác architecture proposal có chủ ý, không giả chúng đã được merge.

Sau integration đã re-read index và cả bảy phase, rà five design documents,
rerun structure/parse/link/table/catalog/status checks. Independent follow-up
xác nhận F02–F09 đã resolved ở mức contract và không có concrete contradiction
mới; F01 vẫn là user decision, không auto-correction. Số unresolved contradiction
trong proposal: 0; số approval mới nhận: 0. Không còn yêu cầu implementation
phát sinh từ review.

Pending cuối: user decision + future native/human/paid/license acceptance. Không
được đọc structural pass hay completion của báo cáo này thành quyền cook.

## 8. Validation Session 1 — 2026-10-01: phê duyệt thay kế hoạch

Timezone: Asia/Saigon. Trigger: người dùng xác nhận bản đề xuất sau bàn giao.
Có một câu hỏi duyệt ở lượt trước; lượt cập nhật này không hỏi lại hoặc tự mở rộng scope.

### Questions & Answers

1. **[Architecture / scope]** Bạn có duyệt hướng NCKH độc lập với AgentKit, namespace/catalog và installer chung trong bản đề xuất này để thay plan cũ không?
   - Hình thức: một câu hỏi xác nhận trực tiếp, không có danh sách lựa chọn.
   - **Answer nguyên văn:** “tôi duyệt, thay đổi plan đi”.
   - Rationale: đủ quyền promote bản đề xuất thành kế hoạch chính và cập nhật authority; không phải yêu cầu triển khai.

### Confirmed Decisions

- NCKH sở hữu source chuẩn; AgentKit là extension/nguồn tham khảo tùy chọn.
- Chốt 37 identities (10 Core + 13 Engineer + 13 Marketing + 1 tooling), namespace `nckh-*`, gồm `nckh-xia` riêng; giữ nguyên upstream `ak-xia` và không tạo alias shadow.
- Chốt hai primitive plan/cook, auto/interactive semantics, minimum sufficient context, same-agent default và model profiles theo thiết kế đã review.
- Chốt installer hai shell dùng chung Python standard-library engine, prerequisite Python 3.11+, không tự cài Python.
- Chốt bảy phase, 35 task, 19 eval case families cùng toàn bộ evidence/VI–EN/visual/privacy/authorization/holdout invariants được giữ trong migration map.
- Không cấp quyền cook, install, sửa runtime config, paid eval, commit hoặc publication. Native/human/license/paid/lab gates chưa đóng.

### Propagation và authority

- Promote bộ `260930-1910-nckh-portable-skill-kit/` tại chỗ; không tạo thêm bản sao plan hoặc đổi đường dẫn các tài liệu đã bàn giao.
- Cập nhật index, năm design documents và bảy phase. `pending` vẫn là trạng thái triển khai; không tick task vì mới duyệt thiết kế.
- Index `260930-0905-vietnamese-research-skill-kit/plan.md` ghi SUPERSEDED và trỏ tới plan chính; năm phase/two design details cũ và blueprint giữ nguyên để truy nguyên.
- P1 ghi rõ thiết kế đã duyệt, chỉ còn quyền cook riêng và các prerequisite thực tế; P3 chốt namespace Xia; P6 bỏ gate duyệt lại prerequisite Python; P7 phân biệt supersession tài liệu đã xong với package promotion/migration chưa diễn ra.
- Các báo cáo nghiên cứu/review ngày 30/09 là historical evidence, không được sửa lại thành runtime acceptance. Quyết định namespace F-01 đã được user giải quyết; không còn là câu hỏi chờ duyệt.

### Whole-Plan Consistency Sweep

- Đã đọc lại `plan.md` và cả bảy `phase-*.md` sau propagation; đối chiếu năm design documents và redirect ở index cũ. Sáu delta đã rà: authority, namespace/catalog, installer prerequisite, phase state, quyền thực thi và documentary supersession so với package migration. Không còn mâu thuẫn chưa giải quyết.
- `ak plan validate` trả `valid: true` cho plan chính và index lịch sử; parser thấy 7 phase, 35 task, 0 done, 0% implementation. `pending` trong files tương ứng `todo` ở parser, không phải chờ duyệt lại thiết kế.
- Static pass trên 19 Markdown files: 123 local links, 0 missing; 0 lỗi cột bảng; 37 catalog rows/37 unique identities; 19 eval case families; 7 phase approval markers và 7 frontmatters pending. Index chính dài 79 dòng.
- So SHA-256 trước/sau lượt cập nhật: blueprint, năm phase cũ và hai design details cũ đều không đổi (8/8). Index cũ là redirect/historical record, không xóa nội dung baseline.
- `nckh-kit/` và `research-skill-kit/` vẫn chưa tồn tại. Không chạy các lệnh test tương lai trong phase, native consumer, human review hoặc paid eval để ghi pass giả.
- Journal ngày 01/10/2026 đã lưu và `ak journal validate` trả `ok: true`; AgentWiki publish skipped. Không cập nhật global plan-store index trong lượt này; local Markdown là authority, không tuyên bố dashboard đã đồng bộ.
- Không có live task-management mutation surface phù hợp; 35 checklist tasks tiếp tục là state authority. Không tạo goal/chat/issue hay process nền để thay thế task hydration.

Kết luận: đã hoàn tất thay kế hoạch theo approval. Bước thực thi kế tiếp chỉ bắt đầu khi người dùng yêu cầu cook riêng; các gate runtime/lab, rights, reviewer và budget giữ nguyên.
