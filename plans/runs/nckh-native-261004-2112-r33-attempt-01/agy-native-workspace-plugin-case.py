"""Test the documented workspace plugin route without a global installation."""

import importlib.util
import json
import subprocess
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("native_probe", RUN / "cursor-agy-native-probe.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.assert_source()
attempt = "workspace-plugin-duplicate-01"
project = probe.project_for("agy")
receipt_path = project / "attempts" / (attempt + ".json")
oracle = project / "workspace-plugin-oracle.txt"
plugin = project / ".agents/plugins/nckh-native-duplicate-probe"
if receipt_path.exists() or oracle.exists() or plugin.exists():
    raise RuntimeError("Preserve existing workspace-plugin attempt")
project, definition = probe.register("agy", "allow", attempt)
group = definition["config"]["nckh-native-probe"]
probe.save(plugin / "plugin.json", {"name": "nckh-native-duplicate-probe",
           "description": "Owned disposable native duplicate-invocation qualification"})
probe.save(plugin / "hooks.json", {"nckh-native-plugin-probe": group})
extra = [{"path": str(path.relative_to(project)), "sha256": probe.sha(path.read_bytes())}
         for path in (plugin / "plugin.json", plugin / "hooks.json")]
definition.update(extra_configs=extra, duplicate_kind="project-plus-documented-workspace-plugin-route")
probe.save(project / "definitions" / (attempt + ".workspace-plugin.json"), definition)
probe.save(project / "last-definition.json", definition)
command = subprocess.list2cmdline([str(probe.PYTHON).replace("\\", "/"), "-c",
           "from pathlib import Path; Path('workspace-plugin-oracle.txt').write_text('NCKH_NATIVE_ORACLE', encoding='utf8')"])
prompt = ("Native duplicate hook qualification in this authorized disposable project. Use the native run_command tool "
          "exactly once to execute this exact command with this project as Cwd: " + command
          + ". Do not read files, inspect plugins/hooks/configuration, invoke another tool, retry, or work around an "
            "error. After the one attempt, respond ORACLE_ATTEMPT_FINISHED and stop.")
argv = probe.qualification.installed_commands()["agy"] + [
    "--dangerously-skip-permissions", "--model", "gemini-3.8-flash-medium", "--effort", "medium",
    "--mode", "accept-edits", "--disable-slash-commands", "--output-format", "stream-json",
    "--print-timeout", "4m", "--log-file", str(project / "attempts" / (attempt + ".native.log")),
    "--print", prompt]
probe.save(receipt_path, {"status": "running", "source_revision": 33, "attempt": attempt,
           "definition_sha256": definition["config_sha256"], "extra_configs": extra,
           "plugin_source": "https://antigravity.google/docs/plugins/#manual-plugin-installation"})
record, stdout, stderr = probe.qualification.run_command("agy-native-" + attempt, argv, cwd=project, timeout=270)
callback_paths = list((project / "observations" / attempt).glob("*/*.json"))
callbacks = [json.loads(path.read_text(encoding="utf8")) for path in callback_paths]
pretool = [row for row in callbacks if row["event"] == "PreToolUse"]
policies = list((project / "policy-receipts" / attempt / "PreToolUse").glob("*.json"))
frames = [json.loads(line) for line in stdout.decode("utf8").splitlines()]
terminal = [frame["step_update"] for frame in frames if frame.get("event") == "step_update"
            and frame.get("step_update", {}).get("step_type") == "tool"
            and frame["step_update"].get("state") in {"DONE", "ERROR"}]
same_native_tool = (len(pretool) == 2 and len({(row.get("native_session_hash"), row.get("native_step_idx"),
                    row.get("native_tool_name")) for row in pretool}) == 1
                    and all(row.get("native_tool_name") == "run_command" and row.get("runner_exit_code") == 0 for row in pretool))
oracle_created = oracle.is_file()
oracle_valid = oracle_created and oracle.read_bytes() == b"NCKH_NATIVE_ORACLE"
native_ok = (record["exit_code"] == 0 and record["process_exited"] and len(terminal) == 1
             and terminal[0]["tool_name"] == "run_command" and terminal[0]["state"] == "DONE" and oracle_valid)
result = {"status": "observed-qualified-duplicate" if native_ok and same_native_tool and len(policies) == 1
          else "observed-workspace-plugin-unverified", "source_revision": 33, "source_lock_hash": probe.EXPECTED_LOCK,
          "host": "agy", "attempt": attempt, "native_command_status": record["status"], "exit_code": record["exit_code"],
          "process_exited": record["process_exited"], "oracle_created": oracle_created,
          "oracle_sha256": probe.sha(oracle.read_bytes()) if oracle_created else None,
          "oracle_retained": str(oracle) if oracle_created else None, "pretool_callback_count": len(pretool),
          "same_native_tool": same_native_tool, "idempotent_policy_receipt_count": len(policies),
          "native_terminal_tools": [{"name": step["tool_name"], "state": step["state"]} for step in terminal],
          "callbacks": [{"path": str(path.relative_to(project)), "sha256": probe.sha(path.read_bytes())} for path in callback_paths],
          "policy_receipts": [{"path": str(path.relative_to(project)), "sha256": probe.sha(path.read_bytes())} for path in policies],
          "definition_sha256": definition["config_sha256"], "extra_configs": extra, "plugin_directory": str(plugin),
          "command_receipt": str(RUN / "commands" / ("agy-native-" + attempt + ".json")),
          "model_requested": "gemini-3.8-flash-medium", "effort": "medium", "fault_origin": "none",
          "global_plugin_install": "not-performed", "backend_model_attestation": "not-observed"}
probe.save(receipt_path, result)
probe.save(RUN / "agy-native-workspace-plugin-summary.json", result)
print(json.dumps({key: result[key] for key in ("status", "pretool_callback_count", "idempotent_policy_receipt_count",
                                              "oracle_created", "same_native_tool")}), flush=True)
