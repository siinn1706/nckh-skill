"""Read native metadata after disabling only the two previously trusted test hooks."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("native_qualification", RUN / "qualification-run.py")
qualification = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qualification)
project = RUN / "projects/codex"
rpc = qualification.CodexRPC("codex-native-cleanup-discovery", project, isolated=True)
try:
    initialization = rpc.request("initialize", {"clientInfo": {"name": "nckh-native-cleanup", "version": "r30"},
                                               "capabilities": {"experimentalApi": True}})
    response = rpc.request("hooks/list", {"cwds": [str(project)]})
    entries = [row for entry in response.get("result", {}).get("data", []) for row in entry.get("hooks", [])
               if row.get("sourcePath", "").casefold() == str(project / ".codex/hooks.json").casefold()]
    record = {"recorded_at": qualification.timestamp(), "initialization_error": initialization.get("error"),
              "discovery_error": response.get("error"), "project_hooks": entries,
              "ui_actions": ["disable-exact-project-PreToolUse", "disable-exact-project-SessionStart"],
              "trust_revocation": "not-exposed-in-ui-trust-hashes-remain", "native_callbacks": "none-observed",
              "model_turns": 0, "global_user_definitions": "not-edited"}
    qualification.save(RUN / "codex-native-cleanup-observation.json", record)
    print(json.dumps({"project_hooks": [{key: row.get(key) for key in
                       ("eventName", "enabled", "trustStatus", "currentHash")} for row in entries]}))
finally:
    rpc.close()
