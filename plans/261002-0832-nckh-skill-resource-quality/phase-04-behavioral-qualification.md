---
title: "Phase 4: Matched behavioral qualification"
status: in-progress
---

# Phase 4: Matched behavioral qualification

## Overview

<!-- Historical plan amendments: R2/R4/R5/R7, 2026-10-02; execution authorized 2026-10-02 -->

Đo đóng góp của resources bằng cặp có/không resource trên **cùng base code và instruction policy**, sau khi P3 có package/consumer thật. Tách deterministic structure, agent behavior, native/runtime, human taste/science và release; không biến parser/build/147-1 thành quality proof. Không áp tổng deadline 15 phút cho tác vụ. Timeout từng case/process là budget riêng: adapter hiện tại chỉ cho 1–900 giây/ca và development-only; ca dài hơn cần route được duyệt hoặc giữ pending/NOT_CALLABLE. Preparation/checker đã được triển khai trong lượt cook; provider/native/human run chờ inputs và authority cho cấu hình thực tế.

## Frozen evidence và comparison

- Giữ nguyên `plans/evaluation/direct-skill-tests/development-corpus.json` (37 × 4 = 148, hash `bbb6d312df45c4bad75bef5b5e8b5a42202dfcf0122382ee59e51ce84c63de84`) cùng first-round 137/4/7, latest 147/1/0, CRO `noindex` fail và diagnostics. Đây là exposed synthetic development trên installed revision 14, không human gold/holdout/baseline.
- Package source revision 18 không kế thừa chứng nhận revision 14. Mỗi condition phải pin subject revision/source-lock, base code/instruction-policy hash, resource registry/closure, corpus/input/split, case IDs, prompt/wrapper, model requested/resolved/effective, config/seed nếu route có hỗ trợ, budget và evidence class; output/trace/receipt có hash riêng. Unknown effective model giữ unknown, không tự chứng nhận matched.
- Phép đo resource chính là resource-off/on trên cùng base code/instruction policy, input/split, wrapper/model, rubric và budget/process policy; chỉ treatment resource khai báo được khác. Mỗi closure/config/artifact có hash riêng, không ép hai artifact khác nhau chung hash. So sánh installed revision 14 → candidate chỉ là **migration/history comparison**, không chứng minh tác dụng nhân quả của resource; không best-of-N hoặc đổi oracle hồi tố.
- `nckh-kit/evals/baselines/baselines.json:3` đang `not-run`/`source_pins` rỗng; `nckh-kit/core/evaluation.py:64-73` giữ qualification pending, cost unknown, accepted count 0. Chỉ user/reviewer chọn threshold mới được đóng baseline.
- Runtime audit `plans/reports/code-reviewer-261002-0832-nckh-runtime-evals.md` đã được tích hợp vào P1: negative oracle/family/protocol/holdout guards phải repair và regression-pass trước qualification. Report không còn là “chưa đọc”; native/OS/effective-model acceptance vẫn là gate riêng.

## Condition mapping và evidence boundary

| Existing variant / comparison | Frozen condition mapping | Interpretation |
|---|---|---|
| `no-skill` | Real no-skill subject with matched input/split/model/budget and its own wrapper/closure/config hashes | Baseline comparator; not the isolated resource effect. |
| `nckh-same-agent` | Preserve variant; pair `same-agent/resource-off` and `same-agent/resource-on` on one pinned base code/instruction policy | Within-pair resource ablation; fixed same-agent wrapper, no code/evaluator rewrite between arms. |
| `nckh-selective-delegation` | Preserve variant; pair `selective-delegation/resource-off` and `selective-delegation/resource-on` on the same pinned base, fixed delegation policy/budget | Separate within-pair ablation; record actual delegation/usage, do not pool away wrapper differences. |
| `relevant permitted upstream` | Map to `selected-permitted-upstream`: actual repository/skill subject, full pin, licensed closure and reviewed runnable route | Borrowing patterns/resources alone is not an upstream baseline. No permitted subject/route → pending, not a relabeled NCKH run. |
| Historical installed revision 14 → candidate | Separately label migration comparison and pin each subject/evaluator/input/receipt | Descriptive history only; revision confounding prevents attributing the delta to resources. |

Manifest must declare the treatment and all conditions **before running**. Same-base excludes repair/instruction-policy changes between resource-off/on; treatment switches only declared resource access/dependency closure. A changed base/wrapper/evaluator/model or unknown matching evidence invalidates the isolated resource claim, while the raw result is retained with that limit. Keep/map every existing baseline variant explicitly; an unavailable variant stays pending with cause, not silently dropped.

## Development và protected holdout invariants

`evals/protocols/qualification.json` retains at most **3 development rounds**, **1 protected holdout run**, and exposure → development. Map conditions/rounds in the frozen manifest; do not reset round counts to tune a new arm. P1 repairs only helper/contract guards: without a real freeze, return pending/error. `core/agent_runs.py:154,163-168` remains development-only; protected holdout execution stays **pending/NOT_CALLABLE** until a separate private route, rights-cleared inputs and human grant exist. Building a new protected-holdout engine is outside this plan. Raw traces/holdout remain in an authorized private store outside source/dist/agent workspace; only redacted references belong in project evidence.

## Requirements

- [x] Reuse existing 148 records only for development smoke; create a separately hashed condition/subject/input/split/wrapper/model/resource manifest with same-base off/on pairs and preserved baseline mappings. Never overwrite old definitions or label exposed data as protected holdout; retain the 3-round/1-holdout/exposure invariants and current development-only route.
- [x] Add negative/failure checks for resource unread, stale hash, wrong consumer, wrong locale/genre, unsupported claim, copied-rights gap and CWD/PYTHONPATH leak. Deterministic checks can validate slots/hash/schema, not semantic truth.
- [ ] Human/domain review queue separately freezes VI taste, EN fidelity, scientific/domain and visual rubric, reviewer identity/rights/threshold. No model score becomes human gold.
- [x] For visuals, retain distinction: direct development already produced actual SVG/PNG and source-map evidence; missing native binding does not mean “no visual output”, but target-editor round trip, accessibility and human scientific meaning remain separate gates.
- [x] Preserve CRO `nckh-cro:positive` failure and hash-bound answer/native/trace match. The owner selected CRO canonical/noindex inspection; `cro-scope-amendment.json` records the decision using the original task with no historical rerun/regrade. Broader crawl/search analysis remains with SEO.
- [x] New evaluation inputs must be real sourced/user-supplied tasks/artifacts or explicit approved fixtures with rights/provenance; do not generate a synthetic dataset to raise coverage. Existing synthetic 148 remains diagnostic only.
- [ ] Complete actual host/OS/model/budget/right grants, compatible per-case route and independent receipt review before provider/native/human runs; these inputs remain pending. Longer-than-900-second cases remain pending/NOT_CALLABLE until an approved route/adapter with named owner/tests exists; do not impose a total 15-minute deadline or run unbounded. Runtime audit repairs are prerequisites, not qualification.

## File ownership

| Owner | Exact paths | Responsibility |
|---|---|---|
| P4 baseline | `nckh-kit/evals/baselines/`; `nckh-kit/evals/results/` | Same-base treatment and existing-variant mappings; separate migration comparison; subject/closure/config/output hashes per condition, preserve old results. |
| P4 rubric | `nckh-kit/evals/rubrics/`; `nckh-kit/evals/cases/runtime/` only for new separately reviewed cells | Human/domain/native rubric and explicit pending gates; no source skill edits. |
| P4 project evidence | `plans/evaluation/resource-quality/` | Redacted manifests/receipts/review references only; raw traces/holdout in separately authorized private store outside workspace; never mutate direct-history. |
| Existing lane owner | `plans/evaluation/direct-skill-tests/` | Read-only historical evidence; no rerun/regrade in place. |
| P4 route owner, conditional separate grant | `nckh-kit/core/agent_runs.py`; `nckh-kit/tests/release/test_agent_runs.py`; `nckh-kit/tests/release/test_runner.py`; `nckh-kit/docs/qualification.md` | Only if a longer-case route change is selected and authorized: own budget/timeout/process-cleanup compatibility tests and docs before run. No automatic removal of bounds and no new holdout engine. |

## Data flow and steps

1. Freeze same-base off/on treatment, all condition mappings/hashes/rounds and reviewer/rights/threshold references. Keep migration and actual upstream comparisons separately identified.
2. Check callable route, per-case/process budget and cleanup before running. Existing adapter is usable only for compatible development cases within 1–900 seconds; longer cases or private holdout remain pending/NOT_CALLABLE until the corresponding approved route exists. Run the frozen case IDs only after operator approval; keep raw traces private and redact summaries.
3. Review deterministic artifact checks independently; record pass/fail/pending/timeout-unknown and actual command/cleanup status.
4. Route VI/EN taste, domain/science and visual outputs to named human reviewers; keep `human_acceptance=not-evaluated` until actual review.
5. Compare quality floor first, then cost/time if effective model/billing is observed. Resource benefit claims require the within-base off/on pair and matched evidence; one direct lane, revision 14 migration or adoption of upstream patterns is insufficient.
6. Decide `candidate`, `experimental`, or `NO-GO`; stable/public remains blocked by unresolved native/OS/rights/human gates.

## Validation and run contracts

- Existing structural command: from `nckh-kit`, `python evals/run-evals.py --validate-only`.
- Existing deterministic command: `python evals/run-evals.py --run-deterministic --output evals/results/resource-qualification-local.json`.
- Existing non-provider adapter preview, which writes its output receipt: `python evals/run-evals.py --prepare-agent-run --recipe FILE --output evals/results/resource-agent-preview.json`; `plan_hash` is integrity, not authorization. Current `core/agent_runs.py:102-106` enforces development round and **1–900 seconds per case**, not a whole-task deadline.
- Provider/native execution is **pending actual inputs and grants**. If later granted for a compatible development case, existing syntax requires `python evals/run-evals.py --run-agent --recipe FILE --approve-plan-hash HASH --allow-provider --output ...`; caller/operator must review freeze references and actual human authority. This command does not run protected holdout. No hash/reference/fixture substitutes for consent.
- Longer case route: pin approved interface/driver, explicit process/case/total budget policy, timeout/stop/owned-process cleanup and test evidence under the conditional route owner above before run. Direct history already includes a 1,201.094-second case; it is not runnable through the current 900-second adapter unchanged. Do not truncate the case or silently raise the bound to declare completion.
- Implemented: `python scripts/compare-matched.py --manifest MATCHED_MANIFEST --work-context PROJECT --output RECEIPT`. It checks all six conditions, actual file-reference hashes, preserved historical rounds and within-pair base/wrapper/model/gates/config equality. Pending references stay explicit; output proves manifest integrity, with accepted count 0 and resource benefit unknown. It executes no host/provider or protected holdout.

## Risks, rollback và success

- High: revision/wrapper/session/model confounds resource effect. Mitigate same-base off/on pairs with condition-specific hashes, fixed wrapper/policy/model and independent review; preserve existing variants. Revision migration is separate; mismatched/unobserved factors mean isolated effect unknown.
- High: synthetic/exposed corpus overstates quality. Mitigate protected holdout/human gold as separate pending gates; do not promote from development.
- High: runtime/native/visual route unavailable. Preserve actual artifact and pending native gate; no fake screenshot and no “no output” claim.
- Medium: billing/timeout/process cleanup. No blanket total 15-minute cutoff; keep current 900-second per-case route limit explicit. Longer cases need an approved compatible route; every run has bounded case/process budget, stop and owned-process cleanup. Timeout stays `timeout-unknown`, never auto-retry or unbounded execution.

Done for the authorized comparison scope means each runnable condition has separately hash-bound subject/input/split/wrapper/model/resource closure/config/output and an independently reviewed receipt; same-base ablation, existing variants and migration comparisons are not conflated. Unavailable upstream/long-case/holdout routes remain pending, never marked complete or silently omitted. Failure history/CRO fail and development limits remain; no stable/public release or human/scientific claim is made without its gate. If a required condition remains pending, qualification remains incomplete.

## Rollback

If candidate loses quality floor, shows rights/closure drift, or fails cleanup, mark candidate receipt failed/pending and stop promotion. Retain traces/staged content and revision 18/revision 14 history; coordinate owning phases to restore compatible candidate source/resource/schema/lock together or create a corrective freeze. Never restore a lock alone, erase history, or delete direct-development evidence.

## Execution checkpoint

Matched checker và regression có thật; human queue/wrapper specifications chỉ là preparation. Manifest sáu conditions và actual references đã kiểm integrity. Không allocation round mới, không upstream subject giả, không effective model/output hash tự tạo. Actual corpus/reviewer/threshold/runtime/budget và native/human/holdout/release gates còn pending.
