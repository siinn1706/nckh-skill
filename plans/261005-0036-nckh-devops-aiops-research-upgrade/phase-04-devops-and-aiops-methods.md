---
phase: 4
title: "DevOps research environment và AIOps methods/evaluation"
status: completed
priority: P1
effort: 3-4 ngày công
dependencies: [phase-02-research-and-statistics, phase-03-scientific-datasets-and-telemetry]
---

# P4 — DevOps research environment và AIOps methods/evaluation

## Context và outcome

Đọc [primary references](../reports/researcher-261005-0036-primary-aiops-sources.md), [scientific transfer](../reports/researcher-261005-0036-scientific-sources.md), [other kits](../reports/researcher-261005-0036-other-resource-kits.md) và [matrix](./acceptance-matrix.md). Bổ sung AIOps owner cho RCA/anomaly/forecasting/retrieval/agent research; DevOps sở hữu reproducible environment/resources/process/cleanup, không operational autopilot.

`KIT = C:/Users/USER/Downloads/test-skill/nckh-kit`; `RUN` kế thừa P1 absolute attempt root. Components từ ClaudeKit chỉ nguồn chỉ ra gap; no source transplant vì root proprietary/confidential. Independent design dựa public primary references.

## Ownership và files

AIOps-DevOps owner ghi specialty files dưới đây. Security/debug chỉ linked handoff qua controller, không mở rộng production services.

| Action | Absolute named path | Change |
|---|---|---|
| Create | `KIT/skills/core/nckh-aiops/SKILL.md` | Thin scientific AIOps owner |
| Create | `KIT/skills/core/nckh-aiops/references/benchmark-protocols.md`, `KIT/skills/core/nckh-aiops/references/rca-anomaly-and-forecasting.md`, `KIT/skills/core/nckh-aiops/references/retrieval-and-agent-evaluation.md` | Task-specific protocol/baseline/metric/trust/readout references |
| Create | `KIT/core/contracts/aiops-evaluation.schema.json`, `KIT/core/aiops.py` | Closed protocol/readout records + invariants/metric binding |
| Create | `KIT/tests/research/test_aiops.py` | Proposed ranking/temporal/task/trust/failure checks |
| Modify | `KIT/skills/engineer/nckh-devops/SKILL.md` | Link research environment reference; retain authority/process/rollback |
| Create | `KIT/skills/engineer/nckh-devops/references/research-environment.md` | Actual runtime/resource/workload/config evidence |
| Modify by controller | `KIT/skills/engineer/nckh-debug/SKILL.md`, `KIT/skills/engineer/nckh-security/SKILL.md`, `KIT/skills/engineer/nckh-test/SKILL.md` | Link scientific handoff/trust boundaries only where relevant |
| Create at cook | `RUN/aiops-evaluation.json`, `RUN/environment.md` | Protocol/readout or pending records; no benchmark launch implied |

## Requirements và architecture

`aiops-evaluation` v1: stage `protocol|readout`, task `rca|anomaly|forecasting|retrieval|agent`, benchmark release/suite/system/source refs+rights, available modalities, dataset/split/telemetry/analysis bindings, independent unit, gold/label/qrels access, baseline/ablations, preprocessing/threshold/available-at-time policy, budgets/seeds/repeats applicability, metrics/denominators/ties/unknown/failures, predictions/run refs, uncertainty và limitations. Typed owner validator requires applicable fields per task; no unsupported JSON Schema keywords.

- **RCA:** service/indicator/cause annotation semantics, causal versus symptom hypothesis, topology provenance/inferred edges, top-k/rank tie handling, multiple accepted causes, unknown/no-answer, competing explanations. Correlation/SHAP/topology không là identified cause.
- **Anomaly:** point/event/incident labels/window tolerance, validation-only thresholds, false-alert denominator/cost, detection delay/duplicate alerts, missing windows và normal versus unknown. Scores không mặc định calibrated probabilities; event metric không trộn point counts.
- **Forecasting:** horizon, origin, availability timestamps, rolling/chronological split, baseline naive/seasonal khi applicable, covariate/test/pretraining leakage; scale/aggregation/missing horizons explicit.
- **Retrieval/RAG:** corpus snapshot/release, query/incident representation, qrels/version/relevance scale, document duplication, availability cutoffs, retrieval/rerank/generation stages, recall/MRR/nDCG definitions, tie/no-relevant/abstention policy. Generation/source support cần evidence, không chỉ answer similarity.
- **Agent:** bounded offline replay hoặc explicitly authorized disposable environment; observation/action interface, reset, workload/fault/task oracle, retries/timeout/failure/cost coverage, egress/tools. Retrieved docs/logs/prompts là untrusted data, không cấp grants hoặc cho đọc gold labels; injection cases kiểm authority/side effects thật của selected route, không claim universal native enforcement.

## Implementation steps

1. Author AIOps owner/input-output routes and task-specific refs; reuse dataset/statistics/telemetry artifacts. Pin RCAEval suite/license per code/data component; AIOpsLab chỉ methodology reference khi chưa có allowed environment.
2. Implement closed evaluation schema/validator và narrow metric helpers cần cho verified cases. Freeze task definitions/oracles trước run; no general training library, provider client hoặc mutable score-based admission engine.
3. Specify task baselines/ablations từ question, equal inputs/budget và known assumptions. Fit transforms/thresholds only train/validation; frozen test/gold access owned separately. Forecast/pretrained overlap và historical incident corpus cutoffs giữ riêng.
4. Add DevOps environment record: actual OS/runtime/library/code/config/workload/resource limits, effective CPU/GPU/quota/affinity/scheduler when observable, unknown≠unlimited. No install/cloud/kube context execution từ metadata. Track owned command/PID/port/workspace before allowed process, reuse actual owner, cleanup matching owned processes.
5. Add security/debug/test handoffs: diagnose code versus evaluate incident; secrets/PII/label leakage; poisoning/injection/cost runaway/timeouts; an unavailable driver remains not-callable/manual. No third-party probes.
6. Test ties/multiple gold/no-answer, missing incidents/horizons, threshold/test leakage, future covariate/corpus leakage, failed-run numerator/denominator, untrusted retrieved instruction and label oracle access. Handoff protocol/environment requirements to P5/P6.

## Todo

- [x] Author AIOps skill + task-specific benchmark/evaluation references.
- [x] Implement schema/validator với typed RCA/anomaly/forecasting/retrieval/agent invariants.
- [x] Deepen DevOps environment/resources/process evidence and bounded handoffs.
- [x] Freeze baselines/metrics/tie/no-answer/failure policies trước actual pilot.
- [x] Verify task leakage/trust/ranking/failure cases; handoff P5/P6.

## Verification — future/proposed, chưa chạy

Từ `KIT`: `python -B -m unittest tests.research.test_aiops` sau creating proposed module, domain/schema checks độc lập source lock. Existing authority/marketing regressions `tests.engineer.test_authority`/`tests.marketing.test_metrics` chạy trước freeze chỉ nếu narrowed inspection xác nhận không require pinned source; other pinned checks hoãn P7. Marketing assertions không được đổi để phục vụ scientific scope.

Success: all task branches preserve gold/independent-unit/split constraints; readout binds actual predictions/results and failures; agent instruction injection không trở thành authority từ artifact content. Unit fixtures không certify LLM/RAG/native prevention hoặc benchmark superiority. Actual model/provider runs cần P6 scope/grant, runtime/version verification và separate receipts.

## Risk/security/rollback

RCAEval mixed licensing: no blanket MIT copy; unresolved baselines giữ metadata-only. Ambient cluster credentials không grant workload/fault injection. Simulation/SHAP/RAG conclusions có thể inflate causality: require evidence/identification and labeling. Rollback only matching owned research files/configs/artifacts, preserve failed runs và concurrent baseline; no cluster teardown/process kill ngoài owned grant.
