---
title: "Phase 5: Đánh giá và đóng gói"
status: pending
---

# Phase 5: Đánh giá và đóng gói

## Overview

**Priority:** P1 · **Estimate:** 3–5 ngày, ước tính không cam kết · **Status:** pending.

Phase này sở hữu final review gate, evaluation harness/fixtures, compatibility
review, package manifest và release/rollback record. Nó không biến schema/lint,
notebook, synthetic fixture hay một worker local thành bằng chứng implementation,
human gold, real run hoặc scientific quality. Mọi kết quả phải ghi raw counts,
inputs, reviewer/receipt và giới hạn; thiếu human/resource/license gate giữ trạng
thái pending.

**Context:** [synthesis](../reports/synthesis-260930-0905-skill-kit-selection.md),
[design proposal](../reports/brainstorm-260930-0905-skill-kit-contract.md),
[nature risks](../reports/researcher-260930-0905-nature-skills.md),
[visual handoff](./phase-04-slides-and-scientific-visuals.md),
[routing, hooks and budgets](./design-routing-hooks-cost.md),
[failure catalog and coverage](./standards-and-failure-catalog.md).
Mọi file dưới đây là **CREATE tương lai; hiện chưa tồn tại** và chỉ phase này sở hữu,
trừ các registry P1 được đọc/ghi theo quy trình change review.

## Key insights and requirements

- So sánh matched `no-skill`, upstream worker được phép, wrapper package và
  fallback; tách routing success khỏi task quality, safety, cost và human effort.
- VI taste phải có human gold/holdout do người dùng hoặc native reviewer chấm;
  English phải có expert/domain review khi cần. Self-score không phải gold.
- Holdout phải cô lập theo tài liệu/tác giả/chủ đề/claim family; đã xem holdout
  để sửa thì chuyển thành development và tạo holdout mới.
- Fault suite phải gồm DOI/quote/retraction/abstract-only, source injection,
  certainty/number/unit drift, venue/ranking isolation, provider/egress/license,
  plan-only authority và editable output QA.
- Upstream update là candidate: resolve catalog thật, hash instruction/reference/
  script/dependency closure, qualify capability bị ảnh hưởng; chỉ dùng accepted
  snapshot nếu còn tồn tại và được phép giữ. Không freeze, auto-install/update,
  hoặc rollback global.
- Kết quả package phải phân biệt `draft`, `evidence-pending`,
  `human-reviewed`, `ready-for-selected-venue`; không gọi `publish-ready` sớm.

### Aggregate acceptance, isolation and budget

<!-- Updated: approved red-team findings 2, 3, 4, 6, 7, 10, 11; user approval 2026-09-30. -->

Acceptance record lưu từng gate `pass|fail|pending|not-applicable` kèm căn cứ và
owner. `accepted-for-scope` chỉ khi mọi gate bắt buộc của scope có pass;
`not-applicable` phải có lý do theo brief. `human-reviewed` chỉ mô tả đã được đọc,
không ghi đè fail/pending. Claim, source freshness, venue conflict hay QA stale
không được che bằng đổi tên trạng thái. Giữ mọi requested deliverable; không tự
bỏ hạng mục khó để giảm denominator hoặc làm kết quả thành accepted.

Trước quality run khóa case coverage, rubric/threshold, reviewer, route/model,
nguồn, budget và stop rule. Thiếu human reviewer/threshold/rights thì gate pending,
không cản các deterministic checks có ích. Tối đa ba vòng development mặc định;
mỗi vòng chỉ đổi một yếu tố, vượt giới hạn cần quyết định mới. Holdout labels và
reviewer notes không nằm trong writer context/tool-readable scope khi host hỗ trợ
isolation; nếu không enforce được thì không nhận blind evaluation. Ghi exposure,
group split theo author/document/topic/claim family và replacement lineage; test
đã dùng để sửa trở thành development, không còn holdout.

Đánh giá cost theo accepted task ở quality floor đã khóa, không theo lần gọi rẻ
nhất. Bao gồm controller, mọi subagent/hook/provider, retry, verification và công
sửa người dùng; unknown giữ unknown. Đo thêm peak kit-context từng worker và pool
đang dùng, cumulative skill-token consumption, cached/uncached coverage và latency.
Giới hạn context 20k–40k / 10%–20% là chính sách người dùng, không phải kết quả
benchmark hay quy luật phổ quát. Không giảm evidence/human gate để đạt budget.

## Architecture and data flow

| Stage | Input | Transform and gate | Output |
|---|---|---|---|
| Review | artifacts/claims/visuals + receipts + profile | final evidence, fidelity, venue, style, asset and editability review; consolidate comments without self-approval | prioritized findings + acceptance state |
| Evaluation | locked baselines, cases, human gold, holdout | run matched routes under equal budget; record raw counts, quality, edits, latency/tool/cost where measured | eval report with uncertainty and limits |
| Compatibility | installed catalog + accepted registry + candidate hashes | inspect drift and requalify affected adapter/domain; no silent version swap | accepted/candidate/rejected mapping |
| Packaging | accepted files, licenses/notices, schemas, eval receipts | manifest paths/hashes, dependency/rights/egress declaration, safe release bundle | package candidate + release/rollback record |
| Handoff | package + open blockers + decisions | maintainer/user signoff only for explicit gates | `pending`, `accepted-for-scope`, `blocked`, never universal compliance |

## Requirements

1. `research-review` must review logic, evidence, style/taste, domain, venue,
   license/provenance and visuals as separate dimensions with severity and owner.
2. Evaluation reports must disclose baseline, task/version, worker/runtime/hash,
   reviewer identities/roles, raw counts, missing data, budget and open gates.
3. Package manifest must include source/skill/license provenance, registry hashes
   and regeneration/rollback instructions. Private task artifacts, full texts,
   taste samples, holdout labels, generated user manuscripts and raw receipts are
   excluded by default. Only explicitly allowlisted, rights-cleared redacted
   examples/eval summaries may enter a distribution; a local audit manifest can
   reference private receipts without bundling them.
4. Compatibility policy must distinguish installed-versus-accepted versions and
   preserve last-known accepted only when a permitted snapshot exists; missing
   snapshot means capability pending/disabled, not invented fallback.
5. Human review, external resource, licensing/release, venue and lecturer/API
   gates remain explicit; technical tests cannot close them.
6. Evaluation must measure plan/cook separation and safe egress, not just prose
   similarity or token count. No claim of improvement without matched evidence.
7. Evaluate catalog-only selection on natural VI/EN requests, optional tags and
   near misses; test hook fail/absent/reentrant behavior and subagent permission,
   timeout reconciliation and shared-budget races, not merely prompt wording.
8. Measure hard-cap behavior before dispatch and on resume/context injection;
   cached tokens still occupy context. All worker overhead counts toward the
   shared pool; lack of billing or token telemetry cannot become zero cost.

## Related files — ownership (future, not existing)

| Action | Absolute path | Ownership / purpose |
|---|---|---|
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\skills\research-review\SKILL.md` | Final multi-dimensional review and handoff |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\evals\manifest.yaml` | Case, baseline, holdout, reviewer and gate manifest |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\evals\baselines.md` | Matched no-skill/upstream/wrapper protocol |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\evals\rubrics\vi-taste.md` | Human Vietnamese taste rubric |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\evals\rubrics\en-fidelity.md` | EN scientific fidelity/domain rubric |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\evals\rubrics\evidence-and-safety.md` | Claim/evidence/egress fault rubric |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\evals\rubrics\visual-editability.md` | Native/render/editability rubric |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\evals\rubrics\routing-hooks-cost.md` | Automatic selection, hook enforcement, shared context and cost evaluation |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\evals\cases\README.md` | Rights-safe case inventory and holdout boundary |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\scripts\validate-package.py` | Static package/provenance/link validation |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\scripts\check-compatibility.py` | Registry/candidate drift qualification helper |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\maintenance\compatibility-review.md` | Human update/rollback procedure |
| CREATE | `C:/Users/USER\Downloads\test-skill\research-skill-kit\docs\operating-and-release.md` | Plan/cook, rights, egress and release runbook |

P5 owns the files above and consumes all previous phases read-only. P1 owns
`shared/registry/source-lock.yaml`, `shared/registry/compatibility.yaml`,
`shared/registry/worker-capabilities.yaml`, `shared/provenance/manifest-schema.yaml`
and generic profile templates; P5 may propose registry changes only through a
reviewed change record, never silently edit them.

## Implementation steps (future execution)

1. Lock case IDs, baseline routes, version/hash inputs, budgets and rubric before
   any candidate comparison; record what is development versus holdout.
2. Obtain explicit rights/consent for personal VI samples, English papers,
   figures and PPTX; otherwise use synthetic fixtures only for deterministic
   guards, not as human taste/evidence/EN-quality gold or completion evidence.
3. Build fault cases for unsupported claims, quote/metadata conflict, retraction,
   abstract-only limits, ranking unknown, venue leakage, source injection,
   translation drift, visual non-editability and denied egress.
4. Run/authorize each baseline and wrapper route under equal task/profile scope;
   capture receipts and human annotation, never infer quality from presence/pass.
5. Score routing, safety, evidence fidelity, VI taste, EN scientific quality,
   visual QA, edit effort, latency/cost and failure rates separately; report
   unknown/insufficient data instead of filling a metric.
6. Re-run affected cases for an upstream candidate whose catalog, instruction,
   dependency, provider, schema or policy hash changed; do not requalify all
   capabilities by assumption.
7. Assemble package manifest/notices and verify all links, hashes, redactions,
   generated-source paths and license/asset records.
8. Produce go/no-go handoff with unresolved user decisions and rollback choice;
   do not publish, install, commit or submit as part of this phase.
9. Map dependency/rule/contract revisions to affected eval families and downstream
   artifacts; qualification creates a reviewed promotion record with trusted
   origin, not a claim that hashing verifies authorship. Check mid-run drift too.
10. Verify packaging by explicit allowlist and resolved paths, including junctions,
    symlinks, private stores and retention policy. Preserve originals and quarantine
    rollback candidate outputs; never silently accept their old receipts.
11. Run matched single-agent versus selective-subagent and no-hook versus hook
    routes only under real host support, equal scope and approved budget. Record
    quality, false blocks, token coverage and cost per accepted task; do not force
    a new model/provider or claim savings from planning arithmetic.

## Todo

- [ ] Lock baselines, case manifest, holdout boundaries and reviewer roles.
- [ ] Obtain rights/consent or mark human-quality gates pending.
- [ ] Define fault, routing, fidelity, visual, update and plan/cook test cases.
- [ ] Define compatibility candidate/accepted/rollback records.
- [ ] Define package manifest, notices, redaction and release/rollback checklist.
- [ ] Freeze thresholds, reviewer/holdout exposure policy and three-round stop rule.
- [ ] Define catalog-routing, hook failure, shared context-cap and cost-per-accepted-task evaluation.

## Validation and test matrix (planned, not run)

| Gate | Required result |
|---|---|
| no-skill/upstream/wrapper matched task | raw counts and scope comparable; no fabricated improvement |
| VI taste holdout | human ratings/agreements/uncertainty recorded; self-score not gold |
| EN scientific fidelity | numbers, units, modality, terminology, citations and limits preserved or blocked |
| anti-hallucination faults | zero accepted fabricated quote/DOI/page/method/result in the locked fault set |
| source/retraction/ranking faults | unknown/contradiction visible; no false Q1/Q2 pass |
| venue isolation | changing venue/year/track resets profile; no rule leakage |
| plan-only/cook authority | only authorized planning/research/validation/journal/task records; no implementation or additional paid/egress authority |
| update drift | changed hash becomes candidate; only qualified capability can be accepted |
| visual/editability | source and render both pass; image-only output never passes editable gate |
| privacy/license/egress | denied or unclear path is blocked; receipts redacted and asset rights visible |
| package validation | all links/hashes/licenses/statuses resolve; no secret/private data |
| pending gate renamed human-reviewed or accepted | aggregate acceptance fails; required gates cannot be bypassed |
| holdout accessed during tuning or labels tool-readable | mark exposed; replace with traceable unexposed holdout or report no blind eval |
| fourth development round without approval | stop with results/open gaps; no unbounded autoresearch |
| stale source policy / artifact / dependency | invalidate affected gates and descendants; no cached pass |
| private draft/holdout/URL token in release bundle | package blocked; allowlist/redaction/path check required |
| no tags on a VI/EN request | automatic capability selection; no need to name internal modules |
| explicit tag points to wrong format/unavailable worker | explain conflict, keep scope; no silent override or auto-install |
| hook is disabled, crashes or matches no actual tool | critical side effect prevented elsewhere or route unavailable; advisory hook not called enforcement |
| parallel reservations exceed shared context/cost cap | serialize/replan before dispatch; no per-agent budget multiplication |
| context under 40k but above 20% of smaller model window | hard-cap fail; both absolute and relative constraints apply |
| missing token/window/billing telemetry | bounded estimate visibly unverified; no ratio/savings/zero-cost claim |

Thresholds for subjective quality, acceptable cost and release scope remain user
decisions; missing thresholds do not become silently passing defaults.

## Risk, security and rollback

| Risk (likelihood × impact) | Mitigation / stop condition |
|---|---|
| Self-evaluation or benchmark leakage (M × H) | Separate writer/critic roles, locked holdout and human gold; rotate holdout after exposure. |
| Rights/consent missing (M × H) | Stop human-quality/release claims; use only deterministic synthetic guards and mark pending. |
| Upstream drift breaks safety/quality (M × H) | Hash closure, affected-case requalification, accepted mapping and explicit candidate state. |
| False “ready” from technical pass (M × H) | Independent evidence/visual/human gates and status vocabulary; no publish claim. |
| Sensitive data/credentials in eval or receipts (M × H) | Redaction, allowlisted egress, access-controlled artifacts and deletion policy; stop on leak. |
| License/asset redistribution violation (M × H) | Per-file notice/ledger; exclude uncleared assets and proprietary Office content. |
| Cost/latency unknown (M × M) | Measure only observed runs; budget/timeout; no invented economics or auto-retry paid calls. |

Rollback selects the last accepted package/worker mapping with a valid receipt,
or disables the capability and preserves its failure record. It never rewrites
global AgentKit, deletes user originals, promotes holdout to gold, or hides a
failed report. Stop release if any critical gate lacks owner, evidence, rights,
or a reversible path.
Rollback marks candidate-dependent outputs quarantined and downstream acceptance
stale; it preserves failed evidence and never revokes user-owned credentials.

## Success criteria and human decisions

- [ ] Evaluation report distinguishes routing, task quality, safety, human effort,
  cost and uncertainty using real observed data only.
- [ ] All required fault classes and plan/cook/update/visual/license gates have
  pass/fail/pending evidence; no missing gate is treated as pass.
- [ ] Package manifest is reproducible from source/skill/dependency hashes,
  receipts and notices, with rollback and regeneration instructions.
- [ ] Maintainer can accept, reject or keep candidate upstream capability without
  touching global installation or claiming universal venue compliance.
- [ ] Catalog-first plan/cook, hooks and subagents satisfy the locked context and
  cost contract without reducing requested scope, quality or human-review gates.

Human decisions remain open: runtime packaging/distribution scope; rights to
personal VI/EN samples, figures and reviewer data; target PPTX/viewers; venue and
ranking profile per task; human/domain reviewer availability; and evaluation
budget/provider authorization. Phase remains pending until those decisions and
their evidence are recorded.
