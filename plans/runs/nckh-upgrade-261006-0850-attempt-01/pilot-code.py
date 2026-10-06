"""Fixed offline arithmetic on a disclosed retrospective observation snapshot."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--config", required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent
config = json.loads((root / args.config).read_text())
rows = json.loads((root / config["data"]).read_text())
protocol = json.loads((root / config["evaluation"]).read_text())
selected = set(protocol["sample_ids"])
assert len(rows) == 26 and len(selected) == 3
assert all(type(row["value"]) is int and row["unit"] == "" for row in rows)
predictions = []
for target in rows:
    if target["sample_id"] not in selected:
        continue
    history = [row for row in rows if row["year"] < target["year"]]
    history.sort(key=lambda row: row["year"])
    assert len(history) >= 2 and history[-1]["year"] == target["year"] - 1
    naive = history[-1]["value"]
    annual_changes = [right["value"] - left["value"] for left, right in zip(history, history[1:])]
    drift = naive + sum(annual_changes) / len(annual_changes)
    for baseline, value in (("naive", naive), ("drift", drift)):
        predictions.append({"sample_id": target["sample_id"], "baseline": baseline, "status": "completed", "prediction": value,
            "target": target["value"], "ranking": [], "accepted": [], "ties": [], "relevance": {}, "origin": target["year"] - 1,
            "target_time": target["year"], "available_at": target["year"] - 1, "delay": None, "reason": ""})
assert len(predictions) == 6
metrics = {"schema_version": 1, "task_id": protocol["task_id"], "task": "forecasting", "baselines": {}}
errors = {}
for baseline in ("drift", "naive"):
    values = [row for row in predictions if row["baseline"] == baseline]
    errors[baseline] = {row["sample_id"]: abs(row["prediction"] - row["target"]) for row in values}
    count = len(values)
    metrics["baselines"][baseline] = {"counts": {"total": count, "completed": count, "failed": 0, "unknown": 0},
        "metrics": {"mae": sum(value / count for value in errors[baseline].values())},
        "metric_coverage": {"mae": {"defined": count, "undefined": 0, "failed_or_unknown": 0}}}
differences = {identity: errors["drift"][identity] - errors["naive"][identity] for identity in sorted(selected)}
statistics = {"schema_version": 1, "task_id": protocol["task_id"], "result": {"status": "computed",
    "estimate": sum(value / len(differences) for value in differences.values()), "standard_error": None, "interval_lower": None, "interval_upper": None},
    "denominators": {"total": 3, "completed": 3, "failed": 0, "missing": 0}}
for name, value in (("predictions", predictions), ("metrics", metrics), ("statistics", statistics)):
    target = root / config["outputs"][name]
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2, allow_nan=False) + "\n")
print(json.dumps({"task_id": protocol["task_id"], "observations": 26, "target_years": 3, "predictions": 6,
    "semantics": "computed from observed dated data; retrospective development demonstration, source units blank", "provider_calls": 0}))
