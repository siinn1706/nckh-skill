# Actual offline pilot readout

Task: `vnm-population-chronological-forecast`. One dated World Bank Vietnam population series: 26 retained observations (2000–2025); frozen train20/validation3/test3. Source unit fields are blank and remain blank.

Actual supervised Python process: PID 31900, exit0, completed-unreviewed; monotonic elapsed 0.06199999999989814 seconds. CPU/peak memory/provider cost were not measured; provider unused. The exact owned handle was reaped; owned-live0.

| Target | Baseline | Prediction | Observed value | Absolute error |
|---|---|---:|---:|---:|
| VNM:2023 | naive | 99680655.000000 | 100352192 | 671537.000000 |
| VNM:2023 | drift | 100704593.363636 | 100352192 | 352401.363636 |
| VNM:2024 | naive | 100352192.000000 | 100987686 | 635494.000000 |
| VNM:2024 | drift | 101360808.565217 | 100987686 | 373122.565217 |
| VNM:2025 | naive | 100987686.000000 | 101598527 | 610841.000000 |
| VNM:2025 | drift | 101980755.791667 | 101598527 | 382228.791667 |

| Baseline | Test MAE (source numerical scale) | Completed / issued |
|---|---:|---|
| drift | 369250.906840 | 3/3 |
| naive | 639290.666667 | 3/3 |

Paired drift-minus-naive absolute-error mean: **-270039.759827**, descriptive over these three target years. One country series is the independent unit; yearly errors are temporally dependent. No p value, standard error or confidence interval is computed.

Algorithms were fixed before this run: last-observation naive and expanding historical mean annual change. Each prediction uses only preceding calendar-year observations. All six predictions, both MAEs and the signed contrast matched an independent exact-rational endpoint oracle within an explicit absolute tolerance of1e-6.

Prior access is disclosed. Calendar-year ordering in a retrospective snapshot does not prove historical publication availability or data vintage. This is a development demonstration of the artifact chain; it does not establish blind holdout performance, generalization, incident RCA efficacy, identified cause or real-system effects. Telemetry is not applicable. Scientific, owner, full native and provider acceptance remain separate pending/not-callable gates.

Evidence: [frozen graph](experiment-manifest.json), [actual process receipt](receipts/pilot-attempt-01.json), stdout (historical evidence path: `receipts/pilot-attempt-01.stdout.txt`; unavailable in the cleaned checkout), stderr (historical evidence path: `receipts/pilot-attempt-01.stderr.txt`; unavailable in the cleaned checkout), [predictions](pilot-output/predictions.json), [metrics](pilot-output/metrics.json), [independent oracle](p6-numerical-oracle.json), [statistics readout](statistical-readout.json), [AIOps readout](aiops-readout.json), [graph readout](experiment-readout.json), [domain checks](p6-domain-readout-checks.json), [cleanup](cleanup.json).

The pilot's first genuine process attempt completed without runtime failure. Earlier acquisition404/network failures and P5/P6 test-fixture failures remain in their original logs and counsel; they are not reclassified as successful experiment runs. Changed data/code/config/metrics require a new frozen graph and invalidate dependent receipts.
