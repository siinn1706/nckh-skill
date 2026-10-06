"""Freeze the actual permitted offline pilot graph before launching computation."""
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
KIT = RUN.parents[2] / "nckh-kit"
sys.path.insert(0, str(KIT))
from core.experiments import validate_experiment_manifest

def bind(path):
    return {"path": path, "sha256": hashlib.sha256((RUN / path).read_bytes()).hexdigest()}

def save(path, record):
    target = RUN / path
    if target.exists(): raise RuntimeError("preserve prior graph artifact")
    target.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return bind(path)

environment = json.loads((RUN / "environment.json").read_text())
environment.update(observed_at=datetime.now(timezone.utc).isoformat(), python=platform.python_version(), runtime_path=sys.executable)
environment["trusted_input_caps"]["records"] = 10000
environment["cap_scope"] = "Pre-freeze controller choice: 10,000 aggregate JSON objects/array members for repeated full graph validation; source observations remain exactly26. Earlier environment observation with1000 cap preserved."
environment_ref = save("environment-v2.json", environment)
config = {"data": "pilot-data/normalized.json", "evaluation": "aiops-evaluation.json", "outputs": {
    "predictions": "pilot-output/predictions.json", "metrics": "pilot-output/metrics.json", "statistics": "pilot-output/statistics.json"},
    "algorithms": "last observation naive; preceding-observation expanding mean annual change", "tuning": "none", "input_access": "prior access disclosed"}
config_ref = save("pilot-config.json", config)
parents = {}
inputs = []
for kind, name in (("dataset", "dataset-manifest.json"), ("split", "split-manifest.json"), ("telemetry", "telemetry-manifest.json"), ("analysis", "statistical-analysis.json"), ("evaluation", "aiops-evaluation.json")):
    parents[kind] = json.loads((RUN / name).read_text())
    inputs.append({"kind": kind, "reference": bind(name)})
references = {}
def collect(value):
    if isinstance(value, dict):
        if set(value) == {"path", "sha256"}: references[value["path"]] = value
        for item in value.values(): collect(item)
    elif isinstance(value, list):
        for item in value: collect(item)
collect(parents)
code = [bind("pilot-code.py"), bind("record-pilot-attempt.py"), bind("numerical-pilot-oracle.py")]
used = {"research-protocol.md", environment_ref["path"], config_ref["path"], *[ref["path"] for ref in code], *[row["reference"]["path"] for row in inputs]}
artifacts = [ref for path, ref in references.items() if path not in used]
rights = bind("pilot-data/rights.md")
if rights["path"] not in {ref["path"] for ref in artifacts}: artifacts.append(rights)
manifest = {"schema_version": 1, "task_id": parents["evaluation"]["task_id"], "experiment_id": "offline-vnm-population-fixed-baselines",
    "stage": "plan", "frozen_at": datetime.now(timezone.utc).isoformat(), "freeze": None, "protocol": bind("research-protocol.md"),
    "inputs": inputs, "code": code, "config": [config_ref], "environment": environment_ref, "artifacts": artifacts,
    "baselines": ["naive", "drift"], "metrics": ["mae"], "oracles": ["separate Fraction arithmetic over actual observed inputs"],
    "output_semantics": "computed-from-observed-data", "simulation": {"applicability": "not-used", "label": "", "generator": "", "parameters": [], "seed": None,
        "replications": 0, "warmup": "", "conservation": "", "uncertainty": "", "validity_limits": ["No simulation or real-system effect claimed"]},
    "limits": {"provider_calls": 0, "egress": "none", "attempts": 2, **environment["trusted_input_caps"]},
    "grants": ["User /goal ak-cook --auto for this project", "P1 selected CC-BY-4.0 dated World Bank series; offline stdlib arithmetic only"],
    "cleanup_route": "Supervisor-owned Popen handle communicates/reaps exact child; no persistent process or external side effects",
    "amendments": [], "expected_outputs": [{"kind": kind, "path": path} for kind, path in config["outputs"].items()], "receipts": [], "outputs": [],
    "limitations": ["one dependent country series", "blank source units retained", "prior access and retrospective source vintage disclosed", "no blind holdout, incident efficacy, generalization or causal claim", "native/provider/owner/scientific acceptance separate and pending"]}
checks = validate_experiment_manifest(manifest, project=RUN)
manifest_ref = save("experiment-manifest.json", manifest)
save("p6-freeze-checks.json", {"manifest": manifest_ref, "checks": checks})
print(json.dumps(checks))
