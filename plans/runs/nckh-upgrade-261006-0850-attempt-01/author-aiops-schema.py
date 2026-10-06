"""Author the closed task-specific AIOps protocol/readout contract."""

import json
from pathlib import Path


def text(): return {"type": "string", "minLength": 1}
def string(): return {"type": "string"}
def num(): return {"type": "number"}
def integer(): return {"type": "integer", "minimum": 0}
def enum(*values): return {"enum": list(values)}
def arr(item): return {"type": "array", "items": item}
def obj(**fields): return {"type": "object", "additionalProperties": False, "properties": fields, "required": list(fields)}
def binding(): return obj(path=text(), sha256={"type": "string", "pattern": "^[a-f0-9]{64}$"})


schema = obj(
    schema_version={"const": 1}, task_id=text(), stage=enum("protocol", "readout"), task=enum("rca", "anomaly", "forecasting", "retrieval", "agent"),
    benchmark=obj(source_id=text(), release=text(), suite=text(), system=text(), rights=enum("metadata-only", "local-use-cleared", "redistributable"),
                  rights_reference=text(), limitations=arr(text())),
    inputs=arr(obj(kind=enum("dataset", "split", "telemetry", "analysis"), reference=binding())),
    modalities=arr(enum("metrics", "logs", "traces", "tabular", "text", "simulation")), independent_unit=text(),
    sample_ids=arr(text()), evaluation_partition=enum("validation", "test", "development-all"), gold=obj(access=enum("unavailable", "evaluation-only"), kind=text(), references=arr(binding()), reason=text()),
    baselines=arr(obj(id=text(), role=enum("baseline", "candidate", "ablation"), input_policy=text(), budget=num(), rationale=text())),
    fitting=obj(preprocessing=enum("train", "not-applicable"), threshold=enum("validation", "not-applicable"), selection=enum("validation", "not-applicable")),
    metrics=arr(obj(id=text(), unit=text(), denominator_policy=enum("all-issued", "completed-with-coverage"), definition=text())),
    budget=obj(seconds=num(), attempts=integer(), provider_calls=integer(), egress=enum("none", "explicit-task-grant")),
    stochastic=obj(applicability=enum("deterministic", "stochastic"), seeds=arr({"type": "integer"}), repeats=integer(), reason=text()),
    policies=obj(ties=enum("stable-id", "not-applicable"), unknown=text(), no_answer=text(), no_relevant=enum("undefined-with-coverage", "zero"), failures=text(), availability=text()),
    rca=arr(obj(cause_unit=enum("service", "indicator", "code", "mixed"), k=integer(), topology_provenance=text(),
                causal_claim=enum("annotation-agreement", "hypothesis", "identified"), identification_evidence=string(), competing_explanations=arr(text()))),
    anomaly=arr(obj(label_unit=enum("point", "event", "incident"), tolerance=num(), false_alert_exposure=num(), exposure_unit=text(),
                    score_kind=enum("uncalibrated-score", "calibrated-probability", "binary"), calibration_evidence=string(), duplicate_alert_policy=text())),
    forecasting=arr(obj(horizon=integer(), origin_policy=text(), value_field=text(), scale=text(), aggregation=text(),
                       covariates=arr(obj(id=text(), available_at=num(), decision_at=num())), pretraining_overlap=text())),
    retrieval=arr(obj(corpus=binding(), qrels=binding(), relevance_scale=arr(num()), k=integer(),
                      documents=arr(obj(id=text(), available_at=num(), query_at=num())), stages=arr(enum("retrieve", "rerank", "generate")),
                      generation_support=arr(binding()), duplicate_policy=text())),
    agent=arr(obj(environment=enum("offline-replay", "authorized-disposable"), grants=arr(text()), tools=arr(text()),
                  reset=text(), workload=text(), fault=text(), oracle=text(), gold_access=enum("evaluation-only"),
                  retrieved_authority=enum("untrusted-data"), actions=arr(obj(tool=text(), authorized={"type": "boolean"}, source=enum("task-grant", "retrieved-data"))),
                  observation_action_interface=text(), retries=integer(), timeout=num(), cost_coverage=text())),
    predictions=arr(binding()), results=arr(binding()), runs=arr(binding()), failures=arr(obj(sample_id=text(), reason=text())),
    limitations=arr(text()),
)
target = Path(__file__).resolve().parents[3] / "nckh-kit/core/contracts/aiops-evaluation.schema.json"
target.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
print("closed aiops-evaluation schema authored")
