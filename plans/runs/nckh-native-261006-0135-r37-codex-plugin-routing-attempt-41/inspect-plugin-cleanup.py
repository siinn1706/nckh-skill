"""Read the installed cleanup command contract without registration or model work."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
PRIOR = RUN.parent / "nckh-native-261006-0125-r37-codex-patch-faults-attempt-40"
spec = importlib.util.spec_from_file_location("plugin_cleanup_owned", PRIOR / "owned-cli-command.py")
owned = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owned)
owned.RUN = RUN
record = json.loads((RUN / "commands/plugin-schema.json").read_text(encoding="utf8"))
native = record["command"][0]
for name, args in (
    ("plugin-remove-help", ["plugin", "remove", "--help"]),
    ("plugin-marketplace-remove-help", ["plugin", "marketplace", "remove", "--help"]),
):
    result, stdout, stderr = owned.run_command(name, [native, *args], cwd=record["cwd"])
    assert result["exit_code"] == 0
    print(stdout.decode("utf8"), flush=True)

