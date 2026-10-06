"""Independent exact-rational oracle for the actual fixed-baseline pilot."""
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

RUN = Path(__file__).resolve().parent
observed = json.loads((RUN / "pilot-data/normalized.json").read_text())
predictions = json.loads((RUN / "pilot-output/predictions.json").read_text())
metrics = json.loads((RUN / "pilot-output/metrics.json").read_text())
output = json.loads((RUN / "pilot-output/statistics.json").read_text())
expected = {}
checks = []
for row in predictions:
    target = next(value for value in observed if value["sample_id"] == row["sample_id"])
    history = sorted((value for value in observed if value["year"] < target["year"]), key=lambda value: value["year"])
    naive = Fraction(history[-1]["value"])
    # Telescoping endpoint arithmetic differs from the production adjacent-change loop.
    drift = naive + Fraction(history[-1]["value"] - history[0]["value"], len(history) - 1)
    value = {"naive": naive, "drift": drift}[row["baseline"]]
    assert math.isclose(row["prediction"], float(value), rel_tol=0, abs_tol=1e-6)
    assert row["target"] == target["value"] and row["origin"] < target["year"]
    error = abs(value - target["value"])
    expected[(row["baseline"], row["sample_id"])] = error
    checks.append({"baseline": row["baseline"], "sample_id": row["sample_id"], "exact_prediction": str(value), "exact_absolute_error": str(error), "absolute_tolerance": 1e-6})
for baseline in ("naive", "drift"):
    values = [value for (name, identity), value in expected.items() if name == baseline]
    mae = sum(values, Fraction()) / len(values)
    assert math.isclose(metrics["baselines"][baseline]["metrics"]["mae"], float(mae), rel_tol=0, abs_tol=1e-6)
    assert metrics["baselines"][baseline]["counts"] == {"total": 3, "completed": 3, "failed": 0, "unknown": 0}
identities = {identity for name, identity in expected}
contrast = sum((expected[("drift", identity)] - expected[("naive", identity)] for identity in identities), Fraction()) / len(identities)
assert math.isclose(output["result"]["estimate"], float(contrast), rel_tol=0, abs_tol=1e-6)
assert output["denominators"] == {"total": 3, "completed": 3, "failed": 0, "missing": 0}
result = {"schema_version": 1, "contract": "pass", "predictions": len(checks), "checks": checks,
    "exact_mean_difference": str(contrast), "oracle_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "inputs": [{"path": path, "sha256": hashlib.sha256((RUN / path).read_bytes()).hexdigest()} for path in ("pilot-data/normalized.json", "pilot-output/predictions.json", "pilot-output/metrics.json", "pilot-output/statistics.json")],
    "scope": "Independent numerical reconciliation; no inferential/scientific efficacy acceptance"}
target = RUN / "p6-numerical-oracle.json"
with target.open("x", encoding="utf-8") as stream: stream.write(json.dumps(result, indent=2) + "\n")
print(json.dumps({"predictions": len(checks), "contract": "pass", "mean_difference": float(contrast)}))
