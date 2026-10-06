# Offline chronological forecast protocol

Task: vnm-population-chronological-forecast. Frozen 06/10/2026, Asia/Saigon.

Use the existing, hash-bound World Bank Vietnam population snapshot with 26 actual annual observations. Preserve the blank source unit and prior access disclosure. This supplied scientific-project route demonstrates the artifact chain; it is not incident telemetry or a blind efficacy benchmark.

Use years 2000-2019 for the train partition, 2020-2022 for validation and 2023-2025 for test. Keep actual year memberships. Forecast each target using only earlier observations, with last-observation naive and expanding historical mean annual-change baselines fixed before execution. No threshold/model selection on test.

Report actual per-year absolute error, MAE per partition/baseline and paired error differences on exactly the same target years. The independent unit is one country series; yearly forecast errors are temporally dependent. Do not compute an IID interval, causal effect or real-system superiority claim. No stochastic seed or repetitions apply to these arithmetic baselines.

Run only local stdlib computations on contained copies with actual code/config/environment/argv/outputs/receipts and failure history. No network ingestion, provider, package install, cloud, cluster, fault injection, private logs or publication. Source rights/raw/normalized hashes and caps are bound by pilot-selection-v2.json. Scientific/domain/owner review stays separate.
