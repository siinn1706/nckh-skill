"""Author the explicitly supported closed statistical contract."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "nckh-kit"


def text():
    return {"type": "string", "minLength": 1}


def string():
    return {"type": "string"}


def integer():
    return {"type": "integer", "minimum": 0}


def array(item):
    return {"type": "array", "items": item}


def obj(**properties):
    return {"type": "object", "additionalProperties": False, "properties": properties, "required": list(properties)}


def enum(*values):
    return {"enum": list(values)}


binding = obj(path=text(), sha256={"type": "string", "pattern": "^[a-f0-9]{64}$"})
schema = obj(
    schema_version={"const": 1}, task_id=text(), stage=enum("plan", "readout"), protocol=binding,
    question=text(), estimand=text(), population=text(),
    unit=obj(kind=text(), mapping_field=enum("sample_id", "entity_id", "incident_id", "group_id"), observation_ids=array(text()), independent_ids=array(text()), independent_n=integer(),
             nesting=array(obj(observation_id=text(), independent_id=text())), independence_evidence=string()),
    inputs=array(obj(kind=enum("dataset", "split"), reference=binding)),
    design=obj(claim_type=enum("descriptive", "predictive", "associational", "causal", "simulation"),
               dependence=enum("independent", "clustered", "temporal", "clustered-temporal", "unknown"),
               identification_evidence=string(), rationale=text()),
    estimator=obj(name=text(), required_assumptions=array(text()), rationale=text()),
    assumptions=array(obj(id=text(), requirement=text(), status=enum("pending", "assessed", "violated", "not-applicable"),
                          evidence_or_reason=string(), limitations=array(text()))),
    effect=obj(metric=text(), contrast=text(), scale=text()),
    missingness=obj(policy=text(), rationale=text()),
    uncertainty=obj(method=text(), unit=text(), replications=integer(), status=enum("planned", "computed", "not-applicable", "failed"), reason=string()),
    multiplicity=obj(family=array(text()), policy=text(), rationale=text()),
    comparison=obj(mode=enum("none", "paired", "unpaired"), baseline_units=array(text()), candidate_units=array(text()), reason=string()),
    stopping=obj(rule=text(), frozen_at=text(), amendments=array(obj(at=text(), reason=text(), previous_rule=text(), new_rule=text()))),
    seed=obj(status=enum("specified", "not-applicable"), value={"description": "Integer when specified, otherwise null; owner validates."}, reason=string()),
    denominators=obj(total=integer(), completed=integer(), failed=integer(), missing=integer()),
    runs=array(binding), outputs=array(binding),
    result=obj(status=enum("planned", "computed", "failed"), **{name: {"description": "Finite number or null, validated by owner."}
               for name in ("estimate", "standard_error", "interval_lower", "interval_upper")}),
    failures=array(text()), limitations=array(text()),
)
schema["title"] = "Scientific statistical analysis plan or actual bound readout"
path = ROOT / "core/contracts/statistical-analysis.schema.json"
path.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
print(path)
