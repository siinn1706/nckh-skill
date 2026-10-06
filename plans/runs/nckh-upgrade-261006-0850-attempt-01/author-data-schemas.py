"""Author closed dataset/split/telemetry schemas in the supported subset."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "nckh-kit/core/contracts"


def text(): return {"type": "string", "minLength": 1}
def string(): return {"type": "string"}
def integer(): return {"type": "integer", "minimum": 0}
def number(): return {"type": "number"}
def enum(*values): return {"enum": list(values)}
def array(item): return {"type": "array", "items": item}
def obj(**fields): return {"type": "object", "additionalProperties": False, "properties": fields, "required": list(fields)}
def binding(): return obj(path=text(), sha256={"type": "string", "pattern": "^[a-f0-9]{64}$"})


schemas = {}
schemas["dataset-manifest"] = obj(
    schema_version={"const": 1}, id=text(), task_id=text(), stage=enum("metadata", "curated"),
    sources=array(obj(id=text(), locator=text(), version=text(), retrieved_at=text(),
                      rights=enum("pending", "local-use-cleared", "redistributable"), rights_reference=string(),
                      access=enum("metadata-only", "public", "supplied-private"), archive_sha256=string())),
    modalities=array(enum("metrics", "logs", "traces", "tabular", "text", "simulation")),
    fields=array(obj(name=text(), type=enum("string", "number", "integer", "boolean"), unit=string(),
                     unknown_reason=string(), missing_tokens=array({}))),
    raw=array(binding()), normalized=array(binding()), sample_index=array(binding()),
    raw_layout=array(obj(path=text(), format=enum("canonical-json-array", "worldbank-api-v2", "jsonl", "csv"), rows=integer())),
    counts=obj(raw=integer(), retained=integer(), excluded=integer(), quarantined=integer()),
    quarantine=array(obj(sample_id=text(), source_locator=text(), reason=text(), original_sha256=text())),
    missingness=array(obj(field=text(), missing=integer(), zero=integer(), reason=string())),
    transforms=array(obj(id=text(), code=binding(), config=binding(), inputs=array(binding()),
                         outputs=array(binding()), input_rows=integer(), output_rows=integer(),
                         excluded_rows=integer(), quarantined_rows=integer())),
    labels=obj(access=enum("none", "protected-evaluation-only", "pending"), provenance=string(),
               annotator=string(), adjudication=string(), references=array(binding()), feature_fields=array(text()), reason=string()),
    release=obj(status=enum("metadata-only", "local-only", "redistributable", "pending"), limitations=array(text())),
)
schemas["split-manifest"] = obj(
    schema_version={"const": 1}, id=text(), task_id=text(), dataset=binding(), purpose=text(),
    independence_axes=array(enum("sample", "group", "entity", "incident", "time")),
    partitions=array(obj(name=enum("train", "validation", "test"), membership=binding(), count=integer())),
    exclusions=array(obj(sample_id=text(), reason=text())), temporal=obj(required={"type": "boolean"}, embargo=number(), reason=string()),
    fitting=obj(preprocessing=enum("train", "not-applicable"), threshold=enum("validation", "not-applicable"),
                selection=enum("validation", "not-applicable"), rationale=text()),
    features=array(obj(sample_id=text(), task=enum("forecasting", "rca", "anomaly", "retrieval", "agent"),
                       kind=enum("observation", "gold-label"), available_at=number(), decision_at=number(),
                       diagnostic_window_end=number(), reason=string())),
    holdout=obj(access=enum("sealed", "prior-access-disclosed", "development"), owner=text(), reason=text()),
    frozen_at=text(), amendments=array(obj(at=text(), reason=text(), invalidated=array(text()))),
)
schemas["telemetry-manifest"] = obj(
    schema_version={"const": 1}, id=text(), task_id=text(), stage=enum("metadata", "normalized", "not-applicable"), reason=string(),
    modalities=array(enum("metrics", "logs", "traces")), sources=array(binding()), outputs=array(binding()),
    normalization=array(obj(code=binding(), config=binding(), inputs=array(binding()), outputs=array(binding()),
                            input_rows=integer(), output_rows=integer(), dropped_rows=integer())),
    semantic_conventions=obj(version=text(), locator=text(), status=enum("stable", "development", "mixed", "unknown"), reason=string()),
    time=obj(origin=enum("unix-seconds", "unix-nanoseconds", "iso8601", "unknown"), timezone=string(),
             precision=string(), alignment=enum("measured", "unknown", "not-applicable"), skew=number(), tolerance=number(), reason=string()),
    signals=array(obj(id=text(), modality=enum("metrics", "logs", "traces"), source_name=text(), target_name=text(),
                      source_unit=string(), normalized_unit=string(), unit_status=enum("known", "unknown"), reason=string(),
                      source_type=enum("gauge", "counter", "rate", "event", "span", "unknown"),
                      aggregation=enum("none", "sum", "mean", "delta", "rate"), monotonic={"type": "boolean"},
                      conversion=array(obj(code=binding(), config=binding(), factor=number())), resets=array(text()))),
    sampling=obj(policy=text(), retention=text(), cardinality_limit=integer(), limitations=array(text())),
    correlation=obj(required_keys=array(enum("resource_id", "trace_id", "span_id")), missing_ids=array(text()), duplicate_ids=array(text())),
    joins=array(obj(id=text(), cardinality=enum("one-to-one", "one-to-many", "many-to-one", "many-to-many"),
                    many_to_many_allowed={"type": "boolean"}, left_ids=array(text()), right_ids=array(text()),
                    pairs=array(obj(left=text(), right=text(), delta=number())), tolerance=number(),
                    retained=integer(), unmatched_left=integer(), unmatched_right=integer(), dropped=integer(), rationale=text())),
    quality=obj(samples=integer(), missing=integer(), zeros=integer(), duplicate_ids=array(text()), gaps=array(text()), limitations=array(text())),
)
for name, schema in schemas.items():
    (ROOT / f"{name}.schema.json").write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
print("dataset-manifest, split-manifest, telemetry-manifest schemas authored")
