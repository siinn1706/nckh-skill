# Benchmark protocol

Freeze question, task, suite/system/release, component rights, independent units,
available modalities, labels/qrels, availability/split/fitting, baselines/ablations,
budgets and metrics. Pin actual acquired bytes and rights per component. A reference
card grants neither acquisition nor execution. Record missing/unknown fields with
reasons and retain failures, null results and prior holdout exposure.

[RCAEval](https://github.com/phamquiluan/RCAEval) distinguishes suites/systems and
service/indicator annotations. Its [licensing](https://github.com/phamquiluan/RCAEval#licensing)
must be checked per code/data component: root license is insufficient for unresolved
CausalRCA/RUN code. These are metadata references; no baseline code is transplanted.

[AIOpsLab](https://github.com/microsoft/AIOpsLab) is a methodology reference for
environment, workload/fault, telemetry, action interface and oracle. Running a cluster,
injecting faults or using cloud resources requires a task-specific grant and rollback.

Inputs and effective environment versions are task artifacts, outside source/dist.
Keep protocol, actual execution, metrics, scientific review and native/human acceptance
as separate records. Dated snapshots do not establish current benchmark support.
