"""Finish declared native cases sequentially within each owned host project."""

import argparse
import importlib.util
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--host", choices=["cursor", "agy"], required=True)
args = parser.parse_args()
path = Path(__file__).resolve().parent / "cursor-agy-native-probe.py"
spec = importlib.util.spec_from_file_location("native_probe", path)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
remaining = ["timeout", "crash", "unsupported-codec", "uncovered-tool", "duplicate"] if args.host == "cursor" else ["crash", "unsupported-codec", "uncovered-tool", "duplicate"]
for mode in remaining:
    probe.observe(args.host, mode, mode + "-01")
