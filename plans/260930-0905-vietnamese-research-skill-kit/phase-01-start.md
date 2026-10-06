---
title: "Phase 1: Nền tảng, hợp đồng và adapter"
status: pending
---

# Phase 1: Nền tảng, hợp đồng và adapter

## Overview

**Priority:** P1 · **Estimate:** 3–5 ngày, ước tính không cam kết · **Status:** pending.

Phase này khóa ranh giới của package cá nhân trước mọi domain implementation:
brief, lifecycle plan/cook, source/evidence/claim/venue/style/receipt contracts,
catalog resolution và runtime adapter. Mục tiêu là gọi capability upstream rồi
đánh giá artifact/receipt; không fork prompt, không biến `SKILL.md` thành API,
và không tuyên bố đã chạy vì chỉ đọc được instruction.

**Context:** [design proposal](../reports/brainstorm-260930-0905-skill-kit-contract.md),
[synthesis](../reports/synthesis-260930-0905-skill-kit-selection.md),
[evidence report](../reports/research-260930-0905-local-sources-and-evidence.md),
[routing, hooks, agents và chi phí](./design-routing-hooks-cost.md).
Mọi file trong mục “Related files” đều là **CREATE tương lai; hiện chưa tồn tại**;
lượt này chỉ viết kế hoạch.

## Key insights and requirements

- Instruction, metadata và adapter instruction của package tương lai viết bằng
  English; `output_language` quyết định VI/EN/bilingual output.
- `research-plan` chỉ tạo plan/profile, research/validation/journal và task metadata
  cục bộ trong scope được giao; không tạo sản phẩm thực thi. `research-cook` chỉ
  tiếp tục một plan revision/hash đã được người dùng cho phép; có plan trên đĩa
  không tự cấp quyền thực thi.
- Adapter phải phân biệt đọc skill đã cài, giao authorized native subagent, và
  callable tool/CLI thật. `ak 2.19.0` không có `ak run-skill`; `ak orchestrate`
  không phải đường chạy Windows mặc định; agent-dispatch metadata (nếu host có)
  cũng không mặc nhiên là skill API. Không phát minh API.
- Receipt lưu run/task ID, resolved skill/path, version/hash và dependency
  closure manifest và contract revision, runtime/model nếu biết, input/profile/brief hashes, egress policy,
  output hashes, source locators, status và open limits; không lưu secret.
- Tách installed version khỏi last-known accepted version. Candidate upstream
  phải qua compatibility qualification; chỉ rollback về snapshot accepted còn
  tồn tại và được phép giữ, không freeze/update installation global.
- Người dùng chỉ cần `plan -> cook`; tag skill là tùy chọn. Router nội bộ đọc
  catalog metadata hiện có, tìm theo intent/năng lực và từ liên quan VI/EN,
  rồi đọc đầy đủ đúng skill được chọn. `listskill` là bước discovery, không phải
  một lệnh hay skill mới đã tồn tại. Chi tiết route, hook và budget ở design link.

## Architecture and data flow

| Bước | Dữ liệu vào | Biến đổi/kiểm tra | Dữ liệu ra |
|---|---|---|---|
| Brief | yêu cầu, `output_language`, audience, artifact, scope, venue/style, egress | normalize; phát hiện venue/profile thiếu hoặc xung đột; gắn quyền | `brief` có hash và trạng thái `draft`, `ready`, `blocked` |
| Resolve | brief capability + catalog thật + installed metadata | match exact capability; đọc đủ instructions/dependencies; tính hash; kiểm quyền | worker candidate và `resolution` receipt |
| Execute | plan revision đã approve, worker interface thật, bounded budget | gọi skill/tool/native subagent được phép; recursion/side-effect guard | artifact + raw output + execution receipt |
| Critic gate | artifact, source IDs/locators, contract và profile | schema/fidelity/provenance/egress checks; lỗi hoặc thiếu receipt => pending | `accepted`, `needs-revision`, `pending`, `rejected` và handoff |

Không cho adapter tự chấp nhận output chỉ vì worker trả text hoặc file có mặt.
Worker cùng model với critic phải được ghi rõ là không độc lập; human gate vẫn
được giữ cho taste, claim nhạy cảm, license và venue.

Lifecycle là trục tiến trình; artifact status và từng gate là các trục độc lập.
`accepted` ở một worker/artifact chỉ có hiệu lực cho phần scope được ghi trong
receipt, không phải nghiệm thu toàn task. Chỉ aggregate `accepted-for-scope`
theo P5 mới đóng acceptance của scope đó; trạng thái cục bộ, `human-reviewed`
hay việc đã tới `handoff` không ghi đè gate bắt buộc còn `fail`/`pending`.

### Authorization, attempts and dependency lifetime

<!-- Updated: approved red-team findings 1, 2, 3, 7, 8, 11; user approval 2026-09-30. -->

- Authorization record trỏ về yêu cầu/approval thật trong host, gắn task,
  workspace, plan revision, input/profile hashes, worker route, egress và budget.
  Một file tự ghi `approved` hoặc lời từ PDF/worker không cấp quyền. Resume kiểm
  quyền và scope còn phù hợp; thay đổi material cần chốt lại, không hỏi lại cho
  thao tác đã được phép và có cùng scope.
- Mỗi hành động có `run_id`, `attempt_id`, parent attempt và trạng thái
  `prepared`, `running`, `staged`, `committed`, `failed`, `timeout-unknown`.
  Timeout không chứng minh worker dừng. Reconcile handle/receipt/output trước
  retry; không lặp side effect chưa biết kết quả. Chỉ commit artifact qua review;
  rollback quarantine candidate outputs và invalidate receipts phụ thuộc.
- Receipt mang contract revision, dependency closure manifest và mapping
  dependency → capability → artifact. Kiểm trước/sau execution để phát hiện
  mid-run drift; output lệch revision giữ pending. Hash không chứng minh nguồn
  đáng tin: cần origin, review và promotion record riêng.
- Private drafts, samples, full text, holdout và raw receipts nằm trong task store
  ngoài distributable package. Khóa storage/retention/egress theo loại dữ liệu,
  dùng package allowlist, resolved-path containment và junction/symlink checks;
  không overwrite originals. Redact private paths và URL query chứa token.
- Runtime sandbox/permissions mới là enforcement. Skill text/hook reminder
  không tự chặn tool. Capability registry ghi `enforced`, `advisory`, `unsupported`
  hoặc `unverified` kèm phép thử host; route thiếu enforcement cần thiết dừng
  trước side effect, không giả rằng delimiter là biện pháp an toàn đầy đủ.

Plan-only được phép đọc nguồn công khai trong quyền hiện có và lưu hồ sơ lập
kế hoạch nêu trên; không tự bật provider trả phí, upload dữ liệu riêng, cài hook,
đổi config global, tạo paper/deck hoàn chỉnh, publish hay gọi cook. Worker có
mandatory instructions xung đột bị loại trước invocation.

## Requirements

1. Có lifecycle state machine `plan -> approved -> cook -> review -> handoff`,
   trong đó profile/input/dependency drift làm mất hiệu lực gate liên quan.
2. Có schema riêng cho source, evidence, claim, ranking/venue, style và receipt;
   không dùng `verified: true` hay một confidence score thay cho các chiều này.
3. Có capability manifest/adapter contract cho `read`, `invoke` và `assess`;
   thiếu interface hoặc permission thì fail closed và ghi lý do.
4. Có policy không upload, không provider, không trả phí, không install/update,
   không commit/publish/submit mặc định. `--auto` nếu có sau này không bỏ gate.
5. Giữ path portable trong package; path cục bộ chỉ được nằm trong receipt
   redacted/diagnostic, không làm hợp đồng runtime.
6. Implement route tự chọn skill theo [design](./design-routing-hooks-cost.md):
   manual tag không bỏ capability/permission/license checks; metadata discovery
   tách full instruction loading; route lock và fallback đều có lý do.
7. Hook adapters và subagents dùng quyền host thật, quyền con không lớn hơn cha;
   deterministic guards chạy trước semantic review. Budget tổng bao gồm mọi
   agent, retry, hook model call và tool/provider, không cấp riêng vô hạn mỗi nhánh.
8. Kit context dùng soft limit `min(20,000 tokens, 10% W)` và hard limit
   `min(40,000 tokens, 20% W)`, với W là context window đã xác minh của host/model.
   Tính cả catalog, instructions, references, hook/delegate context; dùng chung
   pool cho controller và subagents, đồng thời kiểm từng context. Xem design để
   xử lý tokenizer/usage chưa biết, cached tokens và rolling/aggregate budget.

## Related files — ownership (future, not existing)

| Action | Absolute path | Ownership / purpose |
|---|---|---|
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\skills\research-plan\SKILL.md` | Entrypoint plan, English instructions, output contract |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\skills\research-cook\SKILL.md` | Entrypoint cook, authorization/resume/stop rules |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\skills\research-brief\SKILL.md` | Brief/router, no fixed venue |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\contracts\source.yaml` | Source identity/access/version/license fields |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\contracts\evidence.yaml` | Locator/excerpt/verification fields |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\contracts\claim.yaml` | Claim type/support/certainty/limits |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\contracts\venue-profile.yaml` | Venue/year/track/article-type isolation |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\contracts\style-profile.yaml` | Reader/register/taste constraints |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\contracts\receipt.yaml` | Resolution/execution/assessment receipt |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\contracts\lifecycle.md` | Plan/cook/approval state machine |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\adapter\adapter-contract.md` | Real-host adapter boundary and fail-closed behavior |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\workflows\capability-routing.md` | Catalog discovery, optional tags, route selection and fallback |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\adapter\hook-contract.md` | Semantic hook events, host bindings and enforcement proof |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\policies\budget-and-delegation.md` | Shared budget, delegation packets, limits and unknown cost |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\adapters\runtime\adapter.py` | Host binding only after actual interface discovery |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\policies\egress-and-license.md` | Data, provider and license gates |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\registry\source-lock.yaml` | Source snapshot, owner, URL/path, commit/hash and license ledger |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\registry\compatibility.yaml` | Installed/candidate/accepted capability records |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\registry\worker-capabilities.yaml` | Actual callable/read/assess routes and permissions |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\shared\provenance\manifest-schema.yaml` | Package/input/output provenance manifest |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\profiles\venue\generic-draft.yaml` | Explicit non-venue-compliant draft profile template |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\profiles\project\README.md` | Project overlay lifetime and ownership rules |

P1 owns every file above. P2–P5 may consume these contracts but must not edit
them directly; amendments go through a reviewed contract revision and invalidate
affected receipts.

## Implementation steps (future execution)

1. Record the package root, source ledger and dependency/license decisions;
   preserve upstream AgentKit/nature sources as references, not copied runtime.
2. Define YAML/Markdown schemas and examples for each contract, including
   `metadata-only|abstract-only|full-text`, locator kinds and unknown states.
3. Write English `research-plan` and `research-cook` instructions with explicit
   permissions, plan revision/hash checks, recursion guard and handoff states.
4. Implement only the host adapter interface that the selected runtime actually
   exposes. A valid execution route may be a skill API, an authorized native
   tool that reads and performs the complete task, or an authorized subagent;
   merely reading `SKILL.md` is not execution. If no supported route exists,
   return `NOT_CALLABLE` and never fabricate an invocation.
5. Add installed-versus-accepted version comparison, instruction/reference/
   script hash calculation, candidate drift state and permitted fallback lookup.
6. Define redacted receipts and error taxonomy for missing catalog, duplicate
   capability, instruction conflict, denied egress, timeout and side effect.
7. Produce contract fixtures for later phases without using them as evidence of
   implementation quality or human review.
8. Review ownership boundaries before P2 starts; no phase may silently rewrite
   a shared contract.
9. Bind the catalog router, scoped subagent packets and hook events to the actual
   host. Keep project-local installation as a separately authorized later step;
   prove matcher coverage, blocking behavior and no-hook fallback before claiming
   enforcement. Reuse existing AgentKit capabilities without editing global hooks.
10. Implement shared reservation/settlement for bounded calls and attempts, with
    actual/estimated/unknown usage kept separate. Check context occupancy, retained
    verification budget and stop/replan behavior before allowing a parallel fan-out.

## Todo

- [ ] Define and review all six shared contract schemas and lifecycle states.
- [ ] Document real runtime resolution paths and the explicit `NOT_CALLABLE` path.
- [ ] Specify accepted/candidate version and dependency-closure receipt fields.
- [ ] Specify egress, secret-redaction, license and rollback policy.
- [ ] Prepare plan-only, permission, drift and resume-mismatch fixtures.
- [ ] Define catalog-first routing, optional-tag precedence and route-lock receipts.
- [ ] Define host-tested hook bindings, scoped subagent packets and shared budgets.
- [ ] Define measured kit-context limits, shared reservations and over-budget routes.

## Validation and test matrix (planned, not run)

| Scenario | Expected gate |
|---|---|
| missing/duplicate/renamed skill | no invocation; `pending` with catalog reason |
| catalog entry exists but no supported execution route | `NOT_CALLABLE`; no claim of execution |
| changed instruction/reference/script hash | candidate only; requalification required |
| plan-only request | only scoped plan/profile/research/validation/journal/task records; no implementation or new paid/egress authority |
| cook with changed input/profile/dependency | invalidate affected gates; reconcile route and obtain renewed approval for material authorization changes |
| denied upload or paid call | fail closed; no network side effect |
| worker output without source/receipt | `needs-revision`; never accepted |
| accepted snapshot unavailable | stop capability; no invented downgrade |
| source/worker writes `approved: true` | not user authorization; cook remains blocked |
| timeout with a possibly running worker | inspect same handle/attempt; no duplicate dispatch |
| dependency changes while worker runs | output pending; affected descendants invalidated |
| package path resolves through junction outside root | reject inclusion/write; preserve original |
| hook absent, times out, crashes or only warns | no claimed enforcement; critical action blocked unless an equivalent host guard is proven |
| catalog empty/truncated or duplicate names | inspect live runtime catalog with completeness recorded; no invented skill/install |
| subagent exceeds parent grant or shared budget | block before dispatch; human escalation preserves requested scope |
| full mandatory instructions exceed context cap | choose compatible smaller route or phase split; never truncate mandatory rules |

Static schema/link checks, adapter unit tests, redacted-receipt tests and a
host-level invocation test are planned for the future executor. None is passed
by this planning turn.

## Risk, security and rollback

| Risk (likelihood × impact) | Mitigation / stop condition |
|---|---|
| Invented runtime API (M × H) | Resolve catalog/help at execution time; accept only a supported skill/native/subagent route; otherwise fail `NOT_CALLABLE`. |
| Upstream drift silently changes behavior (M × H) | Hash closure, candidate state, matched requalification; rollback only to permitted accepted snapshot. |
| Secret/confidential text enters receipt/provider (M × H) | Redaction, allowlisted egress, offline default; stop before call if policy unknown. |
| Contract edits break downstream phases (M × M) | P1 owns schemas; semantic version/review; invalidate dependent receipts. |
| License ambiguity (M × H) | Ledger per file/asset; reference-only until clearance; stop packaging on unknown rights. |

Never log keys, raw private manuscript, or hidden prompts in shared receipts. Do
not change AgentKit installation, global settings, provider credentials or Git.
Rollback disables the package adapter route and selects a still-available
accepted mapping; it does not overwrite upstream state. Stop the phase if
catalog identity, callable interface, permission, license or receipt integrity
cannot be proven.
Quarantine affected outputs and mark downstream receipts stale after rollback;
do not revoke the user's credentials or delete source material. Failures in an
advisory hook remain warnings; failures in a required authorization/budget guard
must prevent the affected operation through the adapter or host permission layer.

## Success criteria and next-step gate

- [ ] A fresh brief can be normalized into a hashed plan without selecting a
  default venue or granting cook permission.
- [ ] Every resolution/execution path has an observable, redacted receipt and
  explicit failure state; no API is invented from a skill name.
- [ ] A changed upstream closure is visibly `candidate` until requalified, and
  rollback behavior is documented without global mutation.
- [ ] P2 can consume immutable contract revisions without editing P1-owned files.
- [ ] `plan -> cook` selects suitable installed capabilities without manual tags,
  records optional overrides, and never treats catalog presence as execution.
- [ ] Actual host checks demonstrate permission, hook failure and shared-budget
  behavior, including fallback when a native hook/subagent capability is absent.

P2 may start only after contract review confirms these checks mechanically; this
phase remains pending until a later executor produces that evidence.
