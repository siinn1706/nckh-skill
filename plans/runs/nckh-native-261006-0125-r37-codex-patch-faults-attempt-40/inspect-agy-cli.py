"""Refresh read-only CLI capabilities without a model prompt or profile changes."""
import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("agy_readonly_owned", RUN / "owned-cli-command.py")
owned = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owned)
owned.RUN = RUN
result, stdout, stderr = owned.run_command("agy-cli-help", [r"C:/Users/USER\AppData\Local\agy\bin\agy.exe", "--help"], cwd=RUN)
print(json.dumps({"status": result["status"], "exit_code": result["exit_code"], "model_prompts": 0,
    "help_chars": len(stdout), "stdout_path": str(RUN / "commands/agy-cli-help.stdout.txt")}), flush=True)
