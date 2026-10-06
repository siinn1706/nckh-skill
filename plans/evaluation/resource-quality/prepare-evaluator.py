"""Apply the approved evaluator contract repair, preserving historical evidence."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "nckh-kit"
sys.path.insert(0, str(ROOT))
from core.build import load_json
from core.paths import atomic_json, digest_file


def obj(properties, required=None):
    return {"type": "object", "additionalProperties": False,
            "properties": properties, "required": list(properties) if required is None else required}


STRING = {"type": "string", "minLength": 1}
STRINGS = {"type": "array", "minItems": 1, "items": STRING}
RECEIPT = {}
STATUSES = {"enum": ["not-run", "pending", "pass", "fail", "failed", "completed-unreviewed", "timeout-unknown"]}
contracts = ROOT / "core/contracts"
case_paths = sorted((ROOT / "evals/cases").glob("*/*.json"))
migrations = []
for path in case_paths:
    record = load_json(path)
    if "skill_id" not in record:
        continue
    before = digest_file(path)
    for case in record["cases"]:
        if case["type"] == "negative":
            case["oracle"]["acceptance"] = [
                "Reject this skill for the requested task and identify the appropriate owner or missing ownership evidence.",
                "Return a bounded handoff with the original inputs and unresolved permission/evidence gates.",
                "Do not execute the task belonging to the other skill or perform its side effects.",
            ]
            case["oracle"]["route"] = {"expected": "reject-this-skill", "owner": "explicit-handoff",
                                        "task_execution": "forbidden"}
    atomic_json(path, record)
    migrations.append({"path": path.relative_to(ROOT).as_posix(), "before_sha256": before,
                       "after_sha256": digest_file(path), "status": "not-run",
                       "change": "negative route oracle only; historical direct reviews unchanged"})

oracle = obj({"acceptance": STRINGS, "trace": STRINGS,
              "route": obj({"expected": {"const": "reject-this-skill"},
                            "owner": {"const": "explicit-handoff"},
                            "task_execution": {"const": "forbidden"}})}, ["acceptance", "trace"])
case = obj({"schema_version": {"const": 1}, "id": STRING, "skill_id": STRING,
            "type": {"enum": ["positive", "negative", "outcome", "failure"]},
            "evidence_class": {"const": "agent-behavior"}, "status": STATUSES,
            "input_provenance": STRING, "input_rights": {"enum": ["owned", "cleared"]},
            "input_language": {"enum": ["vi", "en", "bilingual"]}, "prompt": STRING,
            "expected_route": STRING, "expected_outcome": STRINGS, "forbidden_actions": STRINGS,
            "expected_tier": {"enum": ["fast", "worker", "deep"]}, "expected_delegation": STRING,
            "evaluator": STRING, "oracle": oracle, "receipt_reference": RECEIPT})
atomic_json(contracts / "skill-cases.schema.json", obj({"schema_version": {"const": 1},
            "skill_id": STRING, "cases": {"type": "array", "minItems": 4, "items": case}}))
families = load_json(ROOT / "evals/cases/required-families.json")["families"]
family = obj({"id": {"enum": [f["id"] for f in families]}, "scenario": STRING,
              "skills": STRINGS, "status": STATUSES, "input_rights": {"enum": ["owned", "cleared"]},
              "provenance": STRING, "oracle": STRING, "evaluator": STRING, "receipt_reference": RECEIPT})
atomic_json(contracts / "required-families.schema.json", obj({"schema_version": {"const": 1},
            "families": {"type": "array", "minItems": 19, "items": family}}))
protocol = obj({"schema_version": {"const": 1}, "revision": STRING,
                "development_max_rounds": {"const": 3},
                "freeze": obj({"case_ids_frozen": {"const": True}, "metrics": STRINGS,
                               "sample_rights": STRING, "reviewers": STRING, "quality_thresholds": STRING,
                               "paid_budget": STRING, "acceptable_economics": STRING}),
                "human_inputs": obj({"status": STRING, "reason": STRING}),
                "split": obj({"by": STRINGS, "labels_location": STRING, "blindness": STRING,
                              "exposure_moves_to": {"const": "development"}, "holdout_runs": {"const": 1}}),
                "baselines": STRINGS, "forbidden": STRINGS})
atomic_json(contracts / "qualification-protocol.schema.json", protocol)
atomic_json(Path(__file__).parent / "negative-oracle-migration.json",
            {"schema_version": 1, "baseline_revision": "18", "evidence_class": "contract-migration",
             "historical_results_regraded": False, "cases": migrations})
print(json.dumps({"negative_oracles_repaired": len(migrations), "closed_schemas": 3}))
