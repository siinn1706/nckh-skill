# Signals, time and joins

OpenTelemetry [semantic conventions](https://opentelemetry.io/docs/specs/semconv/)
were observed at 1.44.0 on 2026-10-06; re-resolve the selected instrumentation's
version and field stability for each task. This reference does not pin a deployed
SDK or claim all conventions stable.

The [metrics data model](https://opentelemetry.io/docs/specs/otel/metrics/data-model/)
distinguishes instrument/aggregation and temporality. Preserve source units, monotonic
counter semantics, resets and aggregation windows. Converting units binds actual
code/config/factor; unknown units remain unknown. Capture normalization inputs/outputs
and source/output/dropped counts independently of unit conversion.

Record clock origin, timezone, precision, skew and tolerance as observed, with unknown
reasons when unavailable. Correlation keys are source identities, not labels or causes.
Explicit joins reconcile actual pairs, unmatched records and cardinality; a reasoned
many-to-many allowance does not remove time/identity checks. Sampling/retention/gaps
limit downstream evaluation. Schema acceptance does not certify semantic equivalence
or causal meaning; preserve original private observations and redaction limits.
