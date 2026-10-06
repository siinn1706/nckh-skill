"""Capture current CLI metadata using the previously verified owned process monitor."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-2255-r37-agy-read-tools-attempt-32"
PROJECT = WORK / "plans/runs/nckh-native-261005-0005-r34-attempt-01/projects/agy-model"
AGY = r"C:/Users/USER\AppData\Local\agy\bin\agy.exe"
spec = importlib.util.spec_from_file_location("owned_cli_metadata", BASE / "owned-cli-command.py")
owned = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owned)
owned.RUN = RUN
assert not (PROJECT / ".agents/hooks.json").exists()
for name, argv in (("agy-current-help", ["--help"]), ("agy-current-version", ["--version"])):
    outcome, stdout, stderr = owned.run_command(
        name, [AGY, "--log-file", str(RUN / (name + ".native.log")), *argv], cwd=PROJECT, timeout=60
    )
    print(json.dumps({"command": name, "exit_code": outcome["exit_code"],
                      "stdout": stdout.decode("utf8", errors="replace")[:20000], "model_prompts": 0}), flush=True)
    assert outcome["exit_code"] == 0, "Preserve failed metadata command before further work"
