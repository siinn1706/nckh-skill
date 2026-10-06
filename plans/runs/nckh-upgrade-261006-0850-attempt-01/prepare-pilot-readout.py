"""Bind actual pilot outputs, domain readouts and process cleanup evidence."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
KIT = RUN.parents[2] / "nckh-kit"
sys.path.insert(0, str(KIT))
from core.experiments import validate_experiment_manifest
from core.statistics import validate_statistical_analysis
from core.aiops import validate_aiops_evaluation

def bind(name): return {"path": name, "sha256": hashlib.sha256((RUN / name).read_bytes()).hexdigest()}
def save(name, value):
    path = RUN / name
    if path.exists(): raise RuntimeError("retain prior readout; use distinct attempt name")
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    return bind(name)

manifest = json.loads((RUN / "experiment-manifest.json").read_text())
run = json.loads((RUN / "receipts/pilot-attempt-01.json").read_text())
run_ref = bind("receipts/pilot-attempt-01.json")
stats_output = json.loads((RUN / "pilot-output/statistics.json").read_text())
statistics = json.loads((RUN / "statistical-analysis.json").read_text())
statistics.update(stage="readout", result=stats_output["result"], denominators=stats_output["denominators"], runs=[run_ref], outputs=[bind("pilot-output/statistics.json")])
statistics["inputs"] = [row for row in manifest["inputs"] if row["kind"] in {"dataset", "split"}]
statistics["assumptions"][0].update(status="assessed", evidence_or_reason="Production code selects preceding calendar-year observations; six predictions independently reconciled with Fraction oracle. Historical publication availability remains unverified and is not claimed.")
stats_ref = save("statistical-readout.json", statistics)
evaluation = json.loads((RUN / "aiops-evaluation.json").read_text())
evaluation.update(stage="readout", predictions=[bind("pilot-output/predictions.json")], results=[bind("pilot-output/metrics.json")], runs=[run_ref])
evaluation_ref = save("aiops-readout.json", evaluation)
readout = {**manifest, "stage": "readout", "freeze": bind("experiment-manifest.json"), "receipts": [run_ref], "outputs": [row["reference"] for row in run["outputs"]]}
readout_ref = save("experiment-readout.json", readout)
checks = {"statistics": validate_statistical_analysis(statistics, project=RUN), "aiops": validate_aiops_evaluation(evaluation, project=RUN), "experiment": validate_experiment_manifest(readout, project=RUN)}
save("p6-domain-readout-checks.json", checks)
cleanup = {"schema_version": 1, "observed_at": datetime.now(timezone.utc).isoformat(), "owned_processes": [{"pid": run["process"]["pid"], "identity_started_at": run["started_at"], "argv": run["argv"], "cwd": run["cwd"], "port": None,
    "exit_code": run["exit_code"], "state": "reaped", "evidence": run_ref}], "owned_live": 0,
    "scope": "Exact supervisor-owned Popen handle reaped; no background server, cluster, provider or descendants launched. CIM inventory unavailable under sandbox; no claim about unrelated user processes."}
cleanup_ref = save("cleanup.json", cleanup)
metrics = json.loads((RUN / "pilot-output/metrics.json").read_text())
predictions = json.loads((RUN / "pilot-output/predictions.json").read_text())
text = "# Actual offline pilot readout\n\nTask: `vnm-population-chronological-forecast`. One dated World Bank Vietnam population series: 26 retained observations (2000–2025); frozen train20/validation3/test3. Source unit fields are blank and remain blank.\n\n"
text += "Actual supervised Python process: PID " + str(run["process"]["pid"]) + ", exit0, completed-unreviewed; monotonic elapsed " + str(run["resources"]["wall_seconds"]) + " seconds. CPU/peak memory/provider cost were not measured; provider unused. The exact owned handle was reaped; owned-live0.\n\n"
text += "| Target | Baseline | Prediction | Observed value | Absolute error |\n|---|---|---:|---:|---:|\n"
for row in predictions:
    text += f"| {row['sample_id']} | {row['baseline']} | {row['prediction']:.6f} | {row['target']} | {abs(row['prediction']-row['target']):.6f} |\n"
text += "\n| Baseline | Test MAE (source numerical scale) | Completed / issued |\n|---|---:|---|\n"
for baseline, value in metrics["baselines"].items():
    text += f"| {baseline} | {value['metrics']['mae']:.6f} | 3/3 |\n"
text += f"\nPaired drift-minus-naive absolute-error mean: **{stats_output['result']['estimate']:.6f}**, descriptive over these three target years. One country series is the independent unit; yearly errors are temporally dependent. No p value, standard error or confidence interval is computed.\n\n"
text += "Algorithms were fixed before this run: last-observation naive and expanding historical mean annual change. Each prediction uses only preceding calendar-year observations. All six predictions, both MAEs and the signed contrast matched an independent exact-rational endpoint oracle within an explicit absolute tolerance of1e-6.\n\n"
text += "Prior access is disclosed. Calendar-year ordering in a retrospective snapshot does not prove historical publication availability or data vintage. This is a development demonstration of the artifact chain; it does not establish blind holdout performance, generalization, incident RCA efficacy, identified cause or real-system effects. Telemetry is not applicable. Scientific, owner, full native and provider acceptance remain separate pending/not-callable gates.\n\n"
text += "Evidence: [frozen graph](experiment-manifest.json), [actual process receipt](receipts/pilot-attempt-01.json), [stdout](receipts/pilot-attempt-01.stdout.txt), [stderr](receipts/pilot-attempt-01.stderr.txt), [predictions](pilot-output/predictions.json), [metrics](pilot-output/metrics.json), [independent oracle](p6-numerical-oracle.json), [statistics readout](statistical-readout.json), [AIOps readout](aiops-readout.json), [graph readout](experiment-readout.json), [domain checks](p6-domain-readout-checks.json), [cleanup](cleanup.json).\n\n"
text += "The pilot's first genuine process attempt completed without runtime failure. Earlier acquisition404/network failures and P5/P6 test-fixture failures remain in their original logs and counsel; they are not reclassified as successful experiment runs. Changed data/code/config/metrics require a new frozen graph and invalidate dependent receipts.\n"
(RUN / "pilot-readout.md").write_text(text, encoding="utf-8")
save("paperwrite-evidence-handoff.json", {"schema_version": 1, "task_id": manifest["task_id"], "evidence": [stats_ref, evaluation_ref, readout_ref, cleanup_ref, bind("pilot-readout.md"), bind("p6-numerical-oracle.json")],
    "supported": "Descriptive arithmetic on one dated series and observed process/artifact integrity", "unsupported": ["blind holdout efficacy", "generalization", "causal identification", "human/scientific/native signoff"], "scientific_acceptance": "pending"})
print(json.dumps(checks))
