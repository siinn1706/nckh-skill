---
phase: 2
title: "Research/method sâu hơn và scientific statistics"
status: completed
priority: P1
effort: 2-3 ngày công
dependencies: [phase-01-start]
---

# P2 — Research/method sâu hơn và scientific statistics

## Context và outcome

Từ [scientific source analysis](../reports/researcher-261005-0036-scientific-sources.md), làm sâu search/screening/appraisal, hypothesis/estimand/design và statistical inference. `nckh-statistics` sở hữu analysis plan/readout; method không chạy experiment, paperwrite không tạo evidence. Marketing experiment/analytics giữ hợp đồng hiện tại.

`KIT = C:/Users/USER/Downloads/test-skill/nckh-kit`; `RUN` kế thừa absolute attempt root đã ghi ở P1. Source choices/rights ở [adoption map](./source-adoption-map.md); acceptance cases ở [matrix](./acceptance-matrix.md).

## Ownership và files

Research-statistics owner giữ các files dưới đây. Controller integrate exact catalog/profile/base-case prerequisites ở P5 trước resource reads; P7 reconcile schema package closure/full qualification và docs. Owner không tự freeze/build/install.

| Action | Absolute named path | Change |
|---|---|---|
| Modify | `KIT/skills/core/nckh-research/SKILL.md`, `KIT/skills/core/nckh-research/references/review-modes.md` | Linked software research review, study/report distinction |
| Create | `KIT/skills/core/nckh-research/references/software-research-review.md` | Search export/dedup/screen/quality/appraisal/evidence-gap protocol |
| Modify | `KIT/skills/core/nckh-method/SKILL.md`, `KIT/skills/core/nckh-method/references/method-and-argument.md` | Scientific design references; preserve literary route |
| Create | `KIT/skills/core/nckh-method/references/research-protocol.md`, `KIT/skills/core/nckh-method/references/causal-inference.md` | Hypothesis/rivals/estimand/design/identification/deviations |
| Create | `KIT/skills/core/nckh-statistics/SKILL.md`, `KIT/skills/core/nckh-statistics/references/inference-and-reporting.md` | Thin specialty skill + scoped diagnostics/reporting |
| Create | `KIT/core/contracts/statistical-analysis.schema.json`, `KIT/core/statistics.py` | Closed record + assumption/units/inference/readout binding validators |
| Create | `KIT/tests/research/__init__.py`, `KIT/tests/research/test_statistics.py` | Proposed meaningful statistical contract tests |
| Create at cook | `RUN/research-protocol.md`, `RUN/statistical-analysis.json` | Task records; no generic paper/template quota |

## Requirements và architecture

Research records query/database/version/date/export/access, dedup key, screening exclusion reason, report→study mapping, extraction/appraisal and bounded gap. Systematic review needs frozen protocol; search absence không là novelty. CS/software appraisal theo actual design: benchmark release/unit/split/baseline, contamination, compute/reporting/failure bias; venue/year/track/article type riêng.

Method distinguishes predictive/associational/causal/explanatory/simulation claims. Define competing hypotheses/falsifier, independent unit, nesting, sampling/measurement, confounding/identification, interventions versus graph correlation. Preregister hoặc date freeze hợp lý theo task; amendments giữ chronology.

`statistical-analysis` v1 fields: task/protocol IDs+hashes, stage `plan|readout`, estimand/question, unit/population/nesting, data/split refs, design/assumptions, estimator/metric/effect-size, missingness policy, uncertainty/multiplicity, comparison pairing, stopping, seed/replications applicability, run/output refs, failures, limitations. Owner validator requires readout data/run/results và reconciles denominator; plan không gán observed results. Missing/not-applicable có reason; no global alpha/power/sample-size threshold.

## Implementation steps

1. Reuse evidence/source/claim/brief/acceptance policies; retain locators, correction/retraction and scope limits. Add linked review instructions, không copy toàn literature pipeline hoặc weighted venue prestige rules.
2. Add method references theo scoped question/design anatomy; mark authority/ethics/domain signoff riêng. No lexical causal-lint pass trở thành causal identification pass.
3. Implement new thin statistics owner and closed schema/stdlib validator. Computation packages optional task bindings; không import SciPy/PyMC/Java hoặc install service vào core.
4. Require independent unit/cluster/time design trước estimator; paired comparisons match task IDs/time windows; preserve null/negative/failed calculations. Fold SD không tự trở thành confidence interval; SHAP không tự là causal proof.
5. Write focused falsification tests: window pseudoreplication, missing/zero difference, estimator assumption mismatch, multiplicity/stopping, plan/readout binding, drift và failed-run denominator. Handwritten test fixtures labeled deterministic, không human gold.
6. Handoff analysis contract cho dataset/telemetry/AIOps owners; controller integrate description routing và four statistics base cases in P5 trước named-consumer lookup, P7 verify final frozen integration. Record needs-data gates, không invent results.

## Todo

- [x] Deepen research review/search/appraisal references và bounded gap wording.
- [x] Add research-protocol/causal-design references while preserving literary method.
- [x] Author statistics skill/schema/validator với plan/readout ownership.
- [x] Verify assumptions/uncertainty/missingness/failure/pairing cases.
- [x] Handoff typed analysis protocol and near-miss routes to P3/P4.

## Verification — proposed tests, chưa hiện hữu/chưa chạy

Từ `KIT`: `python -B -m unittest tests.research.test_statistics` sau khi tạo module, thiết kế domain/schema checks độc lập source lock. Shared schema regressions `tests.contracts.test_state`/`tests.evidence.test_guards` chỉ chạy trước freeze nếu narrowed dependency inspection xác nhận không cần pinned source; otherwise hoãn P7 sau candidate freeze. Failures/drift giữ receipts, không bỏ assertions.

Success: stats plan không cần invented results; readout không pass khi thiếu input/run bindings hoặc unit sai; method returns protocol không tự chạy; narrative/scoping/systematic và literature access vẫn phân biệt. Scientific interpretation cần reviewer thật, no model self-score pass.

## Risk/security/rollback

Statistical wrappers có thể tạo false certainty: enforce bounded wording/assumptions và independent review. Không upload private study data cho diagnostics. Revert only owned skill/reference/schema/module edits với preimages; giữ failed receipts; không sửa marketing hoặc writer/visual/hooks baseline. Nếu shared schema integration fail, controller dừng adoption và giữ analysis artifact pending.

## Actual checkpoint — 06/10/2026

Research/software-review and method scientific-protocol/causal-design references are authored; literary route remains. `nckh-statistics`, the closed supported-subset schema and stdlib validator now exist. `core/research_io.py` is a small shared bounded artifact reader for P2–P6, preserving containment/duplicate JSON/nonfinite/cumulative read/output caps without commands, providers or an orchestration engine. At least one actual structured statistical output must match readout values and denominators.

[P2 checks](../runs/nckh-upgrade-261006-0850-attempt-01/p2-checks.json) and actual test output (historical evidence path: `../runs/nckh-upgrade-261006-0850-attempt-01/p2-tests.txt`; unavailable in the cleaned checkout) record 37 passing domain/state/evidence tests, including 20 statistics/read-bound cases. [Pilot protocol](../runs/nckh-upgrade-261006-0850-attempt-01/research-protocol.md) and [statistical plan](../runs/nckh-upgrade-261006-0850-attempt-01/statistical-analysis.json) remain plan-stage, with null results and no runs. Catalog/profile/base-case registration is deferred to P5 by design, final lock/packaging to P7. Source inventory is in progress; r38 is the baseline, not a frozen upgraded candidate. Scientific/domain interpretation remains pending.
