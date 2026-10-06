"""Freeze the permissible local pilot's evaluation and observed environment."""

import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
KIT = RUN.parents[2] / "nckh-kit"
sys.path.insert(0, str(KIT))
from core.aiops import validate_aiops_evaluation
from core.statistics import validate_statistical_analysis


def bind(name): return {"path": name, "sha256": hashlib.sha256((RUN / name).read_bytes()).hexdigest()}
def save(name, record):
    (RUN / name).write_text(json.dumps(record, indent=2, allow_nan=False) + "\n", encoding="utf-8")


selection = json.loads((RUN / "pilot-selection-v2.json").read_text())
analysis = json.loads((RUN / "statistical-analysis.json").read_text())
validate_statistical_analysis(analysis)
record = {"schema_version": 1, "task_id": selection["task_id"], "stage": "protocol", "task": "forecasting",
    "benchmark": {"source_id": "worldbank-vnm-SP.POP.TOTL-2000-2025", "release": selection["source_version"], "suite": "development-demonstration",
                  "system": "single-country-population-series", "rights": "redistributable", "rights_reference": "pilot-data/rights.md",
                  "limitations": ["not an incident benchmark", "prior input access", "retrospective snapshot without publication-vintage proof"]},
    "inputs": [{"kind": kind, "reference": bind(name)} for kind, name in (("dataset", "dataset-manifest.json"), ("split", "split-manifest.json"),
                                                                         ("telemetry", "telemetry-manifest.json"), ("analysis", "statistical-analysis.json"))],
    "modalities": ["tabular"], "independent_unit": "one country-series; dependent yearly errors", "sample_ids": ["VNM:2023", "VNM:2024", "VNM:2025"],
    "evaluation_partition": "test", "gold": {"access": "evaluation-only", "kind": "observed target series, no human incident gold",
                                            "references": [bind("pilot-data/normalized.json")], "reason": "targets evaluated after each retrospective origin; no true vintage claim"},
    "baselines": [{"id": name, "role": "baseline" if name == "naive" else "candidate", "input_policy": "same snapshot, observations strictly before target year",
                   "budget": 60, "rationale": "fixed deterministic arithmetic; no tuning"} for name in ("naive", "drift")],
    "fitting": {"preprocessing": "not-applicable", "threshold": "not-applicable", "selection": "not-applicable"},
    "metrics": [{"id": "mae", "unit": "source numerical scale; unit blank", "denominator_policy": "completed-with-coverage",
                 "definition": "arithmetic mean absolute error per fixed baseline on three test target years; report all six outcome rows"}],
    "budget": {"seconds": 60, "attempts": 2, "provider_calls": 0, "egress": "none"},
    "stochastic": {"applicability": "deterministic", "seeds": [], "repeats": 0, "reason": "fixed arithmetic"},
    "policies": {"ties": "not-applicable", "unknown": "retain unknown outcome and coverage", "no_answer": "retain failed/missing forecasts",
                 "no_relevant": "undefined-with-coverage", "failures": "preserve every attempt; no success-only efficacy claim",
                 "availability": "preceding calendar-year index in retrospective snapshot, not observed historical release time"},
    "rca": [], "anomaly": [], "forecasting": [{"horizon": 1, "origin_policy": "expanding historical origins; fixed algorithm with no model selection",
        "value_field": "value", "scale": "blank source unit preserved", "aggregation": "MAE", "covariates": [], "pretraining_overlap": "not-applicable; no pretrained model"}],
    "retrieval": [], "agent": [], "predictions": [], "results": [], "runs": [], "failures": [],
    "limitations": analysis["limitations"] + ["no generalization, causal or system efficacy claim"]}
check = validate_aiops_evaluation(record)
save("aiops-evaluation.json", record)
now = datetime.now(timezone.utc).isoformat()
environment = {"observed_at": now, "os": platform.system(), "release": platform.release(), "architecture": platform.machine(),
    "python": platform.python_version(), "implementation": platform.python_implementation(), "runtime_path": sys.executable,
    "packages": "stdlib only; no task package install", "logical_cpu_count": os.cpu_count(), "effective_cpu_quota": "unknown; not exposed by observation",
    "gpu": "not-used", "memory_limit": "unknown; no imposed process quota observed", "affinity": "unknown; no affinity measurement",
    "scheduler": "unknown", "workload": "26 source observations, fixed offline arithmetic", "network": "no pilot egress", "provider": "not-used",
    "trusted_input_caps": selection["trusted_caps"], "owned_background_processes": [], "observer_pid": os.getpid(),
    "scope": "environment observation before pilot; not a run receipt"}
save("environment.json", environment)
(RUN / "environment.md").write_text("# Observed pilot environment\n\n" + "\n".join(f"- {key}: {value}" for key, value in environment.items())
    + "\n\nNo benchmark/provider/cluster/fault workload was launched. CPU count is not effective entitlement. Actual pilot execution gets its own receipt.\n", encoding="utf-8")
save("p4-protocol-checks.json", check)
print(json.dumps({"protocol": check, "python": environment["python"], "pilot_executed": False}))
