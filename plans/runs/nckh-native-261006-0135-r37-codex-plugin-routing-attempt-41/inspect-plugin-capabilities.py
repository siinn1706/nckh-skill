"""Inspect installed plugin registration commands without a model prompt or install."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PRIOR = WORK / "plans/runs/nckh-native-261006-0125-r37-codex-patch-faults-attempt-40"
PROJECT = WORK / "plans/runs/nckh-native-261005-0658-r34-codex-file-attempt-01/project-02"
spec = importlib.util.spec_from_file_location("plugin_owned", PRIOR / "owned-cli-command.py")
owned = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owned)
owned.RUN = RUN
codex = json.loads((PRIOR / "commands/codex-version.json").read_text(encoding="utf8"))["command"][0]
cases = [
    ("plugin-add-help", ["plugin", "add", "--help"]),
    ("plugin-list-help", ["plugin", "list", "--help"]),
    ("plugin-marketplace-help", ["plugin", "marketplace", "--help"]),
]
for name, args in cases:
    record, stdout, stderr = owned.run_command(name, [codex, *args], cwd=PROJECT)
    assert record["exit_code"] == 0
    print(json.dumps({"command": name, "stdout": stdout.decode("utf8"), "stderr": stderr.decode("utf8")}), flush=True)
