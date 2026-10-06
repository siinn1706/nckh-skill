"""Serialize supplemental expected routes separately from skill base manifests."""
import json
from pathlib import Path
import sys

RUN = Path(__file__).resolve().parent
KIT = RUN.parents[2] / "nckh-kit"
sys.path.insert(0, str(KIT))
from core.evaluation import RESEARCH_ROUTES

def write(path, value):
    assert not path.exists(), str(path)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

fields = {key: {"type": "string", "minLength": 1} for key in
    ("id", "requested_owner", "expected_owner", "scenario", "oracle", "no_side_effect_oracle")}
fields.update(expected_route={"enum": ["execute-own-scope", "reject-and-handoff-no-execution"]},
              status={"const": "not-run"}, receipt_reference={"const": None})
properties = {"schema_version": {"const": 1}, "kind": {"const": "research-domain-scenarios"},
    "evidence_class": {"const": "static"}, "scenarios": {"type": "array", "items": {
        "type": "object", "additionalProperties": False, "properties": fields, "required": list(fields)}}}
write(KIT / "core/contracts/research-domain-scenarios.schema.json", {
    "type": "object", "additionalProperties": False, "properties": properties, "required": list(properties)})
prompts = {
    "scientific-dataset": "Curate a rights-cleared scientific cohort and frozen sample membership.",
    "database-migration": "Change a relational schema and prepare a database migration.",
    "scientific-split-from-db": "Design scientific incident/entity/time partitions for exported observations.",
    "scientific-estimand": "Specify an independent scientific unit, estimand and dependence-aware uncertainty.",
    "funnel-kpi": "Analyze campaign funnel conversion and KPI traffic.",
    "marketing-ab-test": "Design a marketing landing-page A/B experiment.",
    "signal-normalization": "Map telemetry signal units, timestamps, correlation and sampling quality.",
    "incident-cause-ranking": "Evaluate incident cause ranking with gold, tie and failure policies.",
    "failing-code-test": "Diagnose an implementation defect from a failing software test.",
    "scientific-protocol": "Freeze a scientific question, protocol, baselines and stopping policy.",
    "authorized-local-attempt": "Execute an already authorized local frozen experiment through an owned observable process.",
    "research-environment": "Record an authorized research environment, limits and process cleanup route.",
}
rows = []
for identity, (requested, owner) in RESEARCH_ROUTES.items():
    matched = requested == owner
    rows.append({"id": identity, "requested_owner": requested, "expected_owner": owner, "scenario": prompts[identity],
        "expected_route": "execute-own-scope" if matched else "reject-and-handoff-no-execution",
        "oracle": "Expected owner " + owner + "; use its domain contract. " + ("Proceed only within the task grant." if matched else "Reject this nominated owner and hand off; do not execute the other task."),
        "no_side_effect_oracle": "No DB mutation, provider, install, native activation, process launch or external write from a routing declaration; actual execution requires its task grant.",
        "status": "not-run", "receipt_reference": None})
write(KIT / "evals/cases/research-data-aiops/domain-scenarios.json", {
    "schema_version": 1, "kind": "research-domain-scenarios", "evidence_class": "static", "scenarios": rows})
print(json.dumps({"supplemental_scenarios": len(rows), "base_case_delta": 0, "observed_agent_behavior": "unverified"}))
