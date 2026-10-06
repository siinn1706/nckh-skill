"""Actual descriptive partition calculation; preserves the original test-only run."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction

ROOT = Path(__file__).resolve().parent

def binding(name):
    return {"path": name, "sha256": hashlib.sha256((ROOT / name).read_bytes()).hexdigest()}

def write(name, value):
    with (ROOT / name).open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2, allow_nan=False) + "\n")

def calculate():
    rows = json.loads((ROOT / "pilot-data/normalized.json").read_text())
    assert len(rows) == 26 and len({row["year"] for row in rows}) == 26
    predictions = []
    for target in rows:
        history = sorted((row for row in rows if row["year"] < target["year"]), key=lambda row: row["year"])
        for baseline in ("naive", "drift"):
            available = len(history) >= (1 if baseline == "naive" else 2)
            value = None
            if available:
                value = history[-1]["value"]
                if baseline == "drift":
                    changes = [b["value"] - a["value"] for a, b in zip(history, history[1:])]
                    value += sum(changes) / len(changes)
            predictions.append({"sample_id": target["sample_id"], "year": target["year"], "baseline": baseline,
                "target": target["value"], "prediction": value, "absolute_error": abs(value - target["value"]) if available else None,
                "status": "completed" if available else "unknown", "reason": "" if available else "Insufficient preceding observations; no imputation",
                "partition": "train" if target["year"] <= 2019 else "validation" if target["year"] <= 2022 else "test"})
    metrics = {}
    for partition in ("train", "validation", "test"):
        metrics[partition] = {}
        for baseline in ("naive", "drift"):
            selected = [row for row in predictions if row["partition"] == partition and row["baseline"] == baseline]
            completed = [row for row in selected if row["status"] == "completed"]
            metrics[partition][baseline] = {"total": len(selected), "completed": len(completed), "unknown": len(selected) - len(completed),
                "mae": sum(row["absolute_error"] / len(completed) for row in completed), "denominator_policy": "completed-with-coverage"}
    write("partition-supplement-output.json", {"predictions": predictions, "metrics": metrics,
        "scope": "Descriptive retrospective same-series calculation; independent_n=1; blank source units; prior access; no CI/causal/blind efficacy claim"})

def supervise():
    inputs = [binding(name) for name in ("partition-supplement.py", "research-protocol.md", "pilot-data/normalized.json", "split-manifest.json", "environment-v2.json")]
    write("partition-supplement-freeze.json", {"frozen_at": datetime.now(timezone.utc).isoformat(), "inputs": inputs,
        "reason": "Add missing descriptive train/validation partition reporting; original frozen graph and genuine test-only receipt remain unchanged",
        "output": "partition-supplement-output.json", "selection": "fixed baseline formulas and original train/validation/test year boundaries",
        "no_history_policy": "unknown with explicit reason; no imputation", "grants": "existing local stdlib offline pilot authority"})
    started = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    argv = [sys.executable, "-I", str(Path(__file__).resolve()), "--calculate"]
    process = subprocess.Popen(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    stdout, stderr = process.communicate()
    ended = datetime.now(timezone.utc).isoformat()
    for name, data in (("partition-supplement.stdout.txt", stdout), ("partition-supplement.stderr.txt", stderr)):
        with (ROOT / name).open("xb") as stream:
            stream.write(data)
    write("partition-supplement-receipt.json", {"task_id": "vnm-population-chronological-forecast", "inputs": inputs,
        "freeze": binding("partition-supplement-freeze.json"), "argv": argv, "cwd": str(ROOT), "pid": process.pid, "parent_pid": os.getpid(),
        "started_at": started, "ended_at": ended, "wall_seconds": time.monotonic() - clock, "exit_code": process.returncode,
        "status": "completed-unreviewed" if process.returncode == 0 else "failed", "cleanup": "exact owned Popen handle reaped",
        "stdout": binding("partition-supplement.stdout.txt"), "stderr": binding("partition-supplement.stderr.txt"),
        "output": binding("partition-supplement-output.json") if (ROOT / "partition-supplement-output.json").exists() else None,
        "cpu_seconds": None, "peak_memory_bytes": None, "provider_cost": None, "provider_calls": 0,
        "scope": "Supplemental process observation, not research-run-receipt graph promotion; around-launch time, not OS CreationDate"})
    assert process.returncode == 0, "Preserved failed supplemental receipt"
    output = json.loads((ROOT / "partition-supplement-output.json").read_text())
    source = sorted(json.loads((ROOT / "pilot-data/normalized.json").read_text()), key=lambda row: row["year"])
    endpoint_errors = {}
    for row in output["predictions"]:
        index = next(i for i, item in enumerate(source) if item["year"] == row["year"])
        if row["status"] != "completed":
            assert index < (1 if row["baseline"] == "naive" else 2)
            continue
        expected = Fraction(source[index - 1]["value"])
        if row["baseline"] == "drift":
            expected += Fraction(source[index - 1]["value"] - source[0]["value"], index - 1)
        error = abs(expected - row["target"])
        assert abs(float(expected) - row["prediction"]) < 1e-6
        assert abs(float(error) - row["absolute_error"]) < 1e-6
        endpoint_errors.setdefault((row["partition"], row["baseline"]), []).append(error)
    for (partition, baseline), errors in endpoint_errors.items():
        assert abs(float(sum(errors) / len(errors)) - output["metrics"][partition][baseline]["mae"]) < 1e-6
    original = json.loads((ROOT / "pilot-output/predictions.json").read_text())
    for row in original:
        supplement = next(item for item in output["predictions"] if item["sample_id"] == row["sample_id"] and item["baseline"] == row["baseline"])
        assert abs(supplement["prediction"] - row["prediction"]) < 1e-6
    write("partition-supplement-oracle.json", {"output": binding("partition-supplement-output.json"), "oracle": "Independent Fraction endpoint identity, not adjacent-change loop",
        "tolerance_absolute": 1e-6, "predictions": len(output["predictions"]), "completed": 49, "unknown": 3, "original_test_predictions_unchanged": 6,
        "verdict": "pass", "scientific_acceptance": "pending"})
    print(json.dumps({"pid": process.pid, "exit_code": process.returncode, "owned_live": 0, "oracle": "pass", "predictions": 52}))

if __name__ == "__main__":
    calculate() if sys.argv[1:] == ["--calculate"] else supervise()
