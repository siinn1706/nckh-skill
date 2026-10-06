"""Closed stdlib-compatible graph and actual-run observation schemas."""
import json
from pathlib import Path

KIT = Path(__file__).resolve().parent.parents[2] / "nckh-kit"
string = {"type": "string", "minLength": 1}
text = {"type": "string"}
number = {"type": "number", "minimum": 0}
def array(item): return {"type": "array", "items": item}
def enum(*items): return {"enum": list(items)}
def obj(**fields): return {"type": "object", "additionalProperties": False, "properties": fields, "required": list(fields)}
binding = obj(path=string, sha256={"type": "string", "pattern": "^[a-f0-9]{64}$"})
optional = {"description": "Null or value checked by owning semantic validator"}
simulation = obj(applicability=enum("not-used", "simulation"), label=text, generator=text, parameters=array(binding), seed=optional,
    replications={"type": "integer", "minimum": 0}, warmup=text, conservation=text, uncertainty=text, validity_limits=array(string))
manifest = obj(schema_version={"const": 1}, task_id=string, experiment_id=string, stage=enum("plan", "readout"),
    frozen_at=string, freeze=optional, protocol=binding,
    inputs=array(obj(kind=enum("dataset", "split", "telemetry", "analysis", "evaluation"), reference=binding)),
    code=array(binding), config=array(binding), environment=binding, artifacts=array(binding),
    baselines=array(string), metrics=array(string), oracles=array(string), output_semantics=enum("computed-from-observed-data", "simulation"),
    simulation=simulation, limits=obj(provider_calls={"const": 0}, egress={"const": "none"}, attempts={"type": "integer", "minimum": 1},
        file_bytes={"type": "integer", "minimum": 1}, aggregate_bytes={"type": "integer", "minimum": 1}, records={"type": "integer", "minimum": 1}, output_bytes={"type": "integer", "minimum": 1}),
    grants=array(string), cleanup_route=string, amendments=array(obj(at=string, reason=string, previous_manifest=binding)),
    expected_outputs=array(obj(kind=enum("predictions", "metrics", "statistics", "oracle", "readout"), path=string)),
    receipts=array(binding), outputs=array(binding), limitations=array(string))
receipt = obj(schema_version={"const": 1}, task_id=string, run_id=string, attempt_id=string, manifest=binding, inputs=array(binding),
    argv=array(string), cwd=string, environment=binding, started_at=optional, ended_at=optional, timezone=string,
    exit_code=optional, status=enum("scheduled", "running", "completed-unreviewed", "failed", "cancelled"),
    process=obj(pid=optional, parent_pid=optional, identity_started_at=optional, cleanup=enum("not-started", "running", "exited", "unknown"), evidence=text),
    stdout=optional, stderr=optional, outputs=array(obj(reference=binding, kind=enum("predictions", "metrics", "statistics", "oracle", "readout"), count={"type": "integer", "minimum": 0})),
    resources=obj(wall_seconds=optional, cpu_seconds=optional, peak_memory_bytes=optional, provider_cost=optional, coverage=string),
    output_semantics=enum("computed-from-observed-data", "simulation"), failure_reason=text, deviation_reason=text,
    reconciliation=obj(status=enum("pending", "reaped", "not-started"), observed_at=string, reason=text))
for kind, schema in (("experiment-manifest", manifest), ("research-run-receipt", receipt)):
    (KIT / "core/contracts" / (kind + ".schema.json")).write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
