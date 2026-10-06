---
title: "NCKH Skill Kit portable — kế hoạch đã duyệt"
description: "Kế hoạch chính cho NCKH Core, Engineer và Marketing; đã cấp quyền cook --auto ngày 01/10/2026."
status: in-progress
priority: P1
effort: "28–45 ngày công ước tính; chưa gồm thời gian chờ human/native gates"
tags: [research, writing, engineering, marketing, portability]
blockedBy: []
blocks: []
created: 2026-09-30
---

# NCKH Skill Kit portable

## Overview

**COOK AUTHORIZED — `--auto`, 01/10/2026 (Asia/Saigon).** Người dùng đã gọi `/goal` với `ak-codex-goal`, `ak-cook`, plan này và `--auto`. Đây là kế hoạch chính, thay [plan cũ đã superseded](../260930-0905-vietnamese-research-skill-kit/plan.md): NCKH sở hữu source riêng, build self-contained artifacts cho Claude Code, Codex, Cursor và Antigravity. Native/human/paid/release gates cần bằng chứng riêng.

## Outcome và boundaries

- 10 Core + 13 Engineer + 13 Marketing + 1 tooling; hai primitive plan/cook; cùng-agent mặc định và delegation có lý do.
- Giữ evidence-first, VI/EN/literary studies, Q1/Q2 theo task, venue isolation, human taste, native scientific visuals, privacy và 11 invariant đã duyệt.
- Không clone catalog, mega command, four hand-maintained copies, universal 40k cap, fake evidence hoặc silent overwrite.
- Lệnh cook mới cho phép tạo package, scripts/tests và artifacts trong workspace; không cấp quyền cài vào host thật, paid/provider eval, commit hoặc publish.

## Design và evidence

| Tài liệu | Sở hữu |
|---|---|
| [Kiến trúc](architecture.md) | Critique baseline v1.0, bảy component types, source-of-truth, repository tree. |
| [Catalog](skill-catalog.md) | Toàn bộ 37 identities, boundaries và PORT/MERGE/EXTENSION/DROP. |
| [Workflow/model](workflow-and-model-routing.md) | Plan/validate, auto/interactive, Xia, delegation, model profiles. |
| [Runtime matrix](runtime-compatibility.md) | Paths, invocation, agents, models/effort, plugins/hooks và giới hạn bằng chứng. |
| [Installer/eval/migration](installer-evaluation-migration.md) | Wizard, transaction, recovery, per-skill eval và migration. |
| [AgentKit research](../reports/researcher-260930-1910-agentkit-port-evidence.md) | Installed/upstream scope và disposition catalog. |
| [Runtime research](../reports/researcher-260930-1910-runtime-compatibility.md) | Nguồn chính thức và local version/help probes. |

## Phases

| # | Phase | Effort ban đầu | Depends on |
|---|---|---|---|
| 1 | [Contracts, workflow và model policy](phase-01-start.md) | 4–6 ngày | Thiết kế và cook --auto đã duyệt |
| 2 | [Core research, writing và visuals](phase-02-core-research-writing-visuals.md) | 5–8 ngày | P1 |
| 3 | [Engineer và Xia](phase-03-engineer-and-xia.md) | 4–6 ngày | P1–P2 |
| 4 | [Marketing](phase-04-marketing.md) | 3–5 ngày | P1–P2; độc lập P3 |
| 5 | [Runtime adapters và closure build](phase-05-runtime-adapters-and-build.md) | 4–7 ngày | P1–P4; preflight ở P1 |
| 6 | [Installer và recovery](phase-06-installer-and-recovery.md) | 4–6 ngày | P5 |
| 7 | [Qualification và migration](phase-07-qualification-and-migration.md) | 4–7 ngày | P1–P6 |

Checkboxes trong từng phase là trạng thái công việc hiện hành; toàn plan vẫn **in-progress** vì acceptance gates còn mở. Package [source/docs](../../nckh-kit/docs/index.md), tests và commands hiện có. [Local receipts](../../nckh-kit/docs/qualification.md) ghi revision/kết quả thực, tách khỏi native/human qualification. Agent sau đọc phase và recheck source/quyền trước tiếp tục.

## Success Criteria

- [ ] Từng stable skill có positive/negative/outcome/failure eval và source/rights ledger.
- [ ] Plan-only/Xia không implement; auto và interactive đạt đúng review/authorization boundaries, feedback/resume durable.
- [ ] Mỗi runtime/surface được quảng bá có evidence thực về discovery, invocation, model/effort, hooks/fallback và mode; docs/help không thay acceptance.
- [ ] Build reproducible, closure đủ; copy/symlink và project/global install idempotent, giữ user edits, rollback/uninstall an toàn trên OS được quảng bá.
- [ ] Scientific/VI taste/EN fidelity/visual gates có human/domain evidence; unknown cost và chưa kiểm không thành pass.

## Quyết định đã duyệt và gates còn mở

- Đã duyệt NCKH độc lập, namespace `nckh-*` gồm `nckh-xia` riêng không shadow `ak-xia`, catalog 37 identities và shared Python installer (3.11+, không tự cài). Giữ toàn bộ workflow/model/eval/migration contracts trong các tài liệu liên kết.
- Đã có quyền cook `--auto` từ lệnh `/goal` ngày 01/10/2026. Quyền này không đóng native/human/paid/license acceptance gates.
- Runtime/OS lab, reviewers, sample/redistribution rights và paid eval budget khóa trước run tương ứng; không cần chọn một venue/model chung cho mọi task.
- Không tìm thấy bản định danh V2/V3; critique chỉ bao phủ blueprint v1.0 và plan thực có trên đĩa.

## Validation Log

### Session 1 — 2026-10-01

Người dùng trả lời câu hỏi duyệt bằng: “tôi duyệt, thay đổi plan đi”. Đã promote bộ tài liệu này và propagate phê duyệt vào bảy phase; giữ năm phase cũ làm lịch sử, không cook hai kiến trúc. [Validation report, mục 8](../reports/validation-260930-1910-nckh-plan-review.md) ghi đầy đủ câu hỏi, câu trả lời, phạm vi và kiểm tra sau cập nhật.

### Whole-Plan Consistency Sweep

Trước cook đã đọc index và bảy phase, rà design documents: cấu trúc và 123 liên kết nội bộ trên 19 file đạt; catalog giữ 37 identities và 19 case families. Ở checkpoint đó, bảy phase và 35 task triển khai còn pending. Đây là historical plan integrity evidence; không thay quyền hoặc acceptance gates.

<!-- Design superseded the previous plan; cook --auto was separately authorized on 2026-10-01. -->

<!-- slug: nckh-portable-skill-kit -->

## Execution Log — 2026-10-01

Cook --auto đã bắt đầu. Workspace ban đầu chưa có package hoặc Git repository; Python 3.12.10. Goal native đang active. Contract/state tests đầu tiên: 9 test pass; đây là deterministic evidence, không phải agent/native/human acceptance. Index AgentKit mặc định không ghi được do sandbox; dùng index rebuildable trong workspace, giữ plan files là authority.

Source/scripts cho 37 identities, four adapters, optional native roles/plugins và owned installer đã triển khai. Local deterministic receipts được giữ theo source-lock; hai explicit-loaded agent development probes và independent installer reviews nằm ở [reports](../reports/). Rubrics là proposals, không human gold. Chưa có corpus VI/EN/reviewers; native/OS/paid/rights/release gates vẫn mở. Current candidate facts được ghi ở qualification record (historical evidence path: `../../nckh-kit/evals/results/candidate.json`; unavailable in the cleaned checkout) sau build/verification.

[Implementation checkpoint](../reports/implementation-261001-nckh-candidate.md): current source 181 pins; 65/65 deterministic tests pass; four hosts build twice with identical hashes; final `dist` có 2,554 file checksum records. Codex project dry-run preview có 43 entries và zero conflict; chưa commit installation. Plan/goal vẫn in-progress, stable/public distribution NO-GO.

Sau checkpoint ban đầu, người dùng trả lời **“Cho phép cài vào project này”** cho preview Codex project gồm 37 skills và 6 vai trò, copy, balanced/inherit. [Installation record](../reports/installation-261001-1813-codex-project-candidate.md) ghi giao dịch 43 mục đã committed; doctor xác nhận 43 current và post-install preview có 43 unchanged, zero conflict. Đây là quyền cài scoped cho project này và bằng chứng file installation; native consumption, human/OS qualification, paid/provider và publication gates vẫn mở. Plan giữ 28/36 tasks và in-progress.

Goal continuation kế tiếp có [discovery/repeat/spec audit](../reports/audit-261001-1813-native-progress-and-runner-gap.md): live Codex catalog expose đủ 37 IDs; actual PowerShell repeat zero changes và hash/ownership/policy không đổi. Chưa có native invocation/model evidence. Audit phát hiện phần opt-in agent runner adapters trong ownership P7 chưa được triển khai; còn việc local implementation trước external gates. Giữ nguyên scope, task counts và bản revision 14 đã cài; không đánh dấu goal complete/blocked.

[Runner checkpoint](../reports/implementation-261001-nckh-agent-runner-candidate.md) đã đóng gap implementation này: opt-in command adapter, private traces và owned timeout cleanup; 79/79 deterministic tests đạt ở revision 17, 184 source pins. Four-host build lặp khớp hash; artifacts mới ở `dist-runner`, 2,554 checksum records. Bản revision 14 đã cài và 43 mục ownership được đối chiếu giữ nguyên. Agent/native/human/provider acceptance vẫn pending; plan giữ 28/36 tasks và in-progress.

[Journal-repair checkpoint](../reports/implementation-261001-nckh-runner-journal-repair.md) sửa hai lỗi nhật ký sau case-read/lifecycle-wait failure. Revision 18 giữ 184 pins; 81/81 deterministic tests đạt, four-host build lặp khớp và artifacts ở `dist-runner-cleanup`. Bằng chứng/artifacts của revision 14/17 và 43 mục đã cài giữ nguyên. Completion audit của cả bảy phase giữ tám Todo chưa đủ bằng chứng; goal chưa complete, không có provider/publication grant mới.

Native goal đã chuyển **blocked** sau [ba lượt impasse audit liên tiếp](../reports/goal-qualification-impasse-audit.json): human/sample/rights/threshold/budget và native/OS qualification inputs vẫn thiếu, source revision 18 và receipts giữ nguyên. Plan files tiếp tục **in-progress, 28/36**; cần các đầu vào và scoped authority tương ứng để tiếp tục nghiệm thu. Source/build và bản revision 14 đã cài được giữ nguyên; scope đầy đủ của plan không thay đổi.

Người dùng tiếp đó cấp quyền: **“bạn sẽ trực tiếp ra thử prompt để test, trực tiếp tự test skill luôn, ngân sách vô hạn, phạm vi chỉ trong project này”**. Tiếp tục development evaluation bằng prompt và dữ liệu tổng hợp do agent soạn, native Codex execution và agent review; mọi workspace/trace của lượt này nằm trong project. Quyền này giải quyết blocker về đầu vào/quyền provider cho lượt development; không tạo human gold, protected holdout hay bằng chứng cho runtime/OS khác. Native goal API hiện chỉ có complete/blocked/paused, không có thao tác resume; công việc tiếp tục theo chỉ thị mới và plan vẫn in-progress. Bản đã cài revision 14 được dùng làm đối tượng thử; receipts revision 18 giữ nguyên.

## Direct testing checkpoint — 2026-10-02

[Báo cáo tự test](../reports/testing-261001-direct-skill-development.md): đủ 37 skills × bốn tình huống = 148 prompt đã chạy/chấm; latest 147 pass, một fail CRO bỏ sót `noindex`. First-round failures/pending và sáu diagnostic với điều kiện đã ghi vẫn được giữ. Theo yêu cầu không giới hạn cook ở 15 phút, harness không có deadline mặc định; cook mới hoàn tất sau hơn 20 phút. Source revision 18 và toàn bộ 43 mục đã cài revision 14 giữ nguyên; owned processes đã đối chiếu và cấu hình tạm đã dọn.

P3/P4 đã hoàn tất phần viết/chạy/lưu development evidence. Plan hiện **in-progress, 30/36 Todo**, chưa có phase được nghiệm thu đầy đủ; human/domain, protected holdout/baseline và full runtime/OS/model gates tiếp tục mở. Native goal API giữ blocked, không có exposed resume operation; checkpoint này ghi công việc đã làm theo grant mới, không đánh dấu toàn goal complete.
