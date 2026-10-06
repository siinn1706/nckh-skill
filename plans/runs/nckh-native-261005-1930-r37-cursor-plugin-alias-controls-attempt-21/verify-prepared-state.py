"""Reconcile the prepared state after a controller output-preservation failure."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("alias_prepared_state", RUN / "cursor-alias-runtime.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
prep = probe.read(RUN / "preparation.json")
stage = probe.read(RUN / "stage.json")
definition = probe.read(RUN / "definitions/session.json")
assert prep == probe.read(RUN / "frozen-brief.json")
assert prep["status"] == "prepared-one-native-plugin-prompt-stop-alias-control"
assert probe.digest_file(probe.CONFIG) == definition["config_sha256"]
assert probe.digest_file(probe.EVIDENCE / "context-allow.json") == prep["context_sha256"]
assert probe.digest_file(probe.EVIDENCE / "probe-control.json") == prep["control_sha256"]
for entry in stage["staged_members"] + definition["extra_configs"]:
    assert probe.digest_file(probe.contained(probe.PROJECT, entry["path"])) == entry["sha256"]
for name in ("controller", "runtime", "definition", "hypothesis"):
    assert probe.digest_file(probe.WORK / prep[name]["path"]) == prep[name]["sha256"]
assert set(definition["plugin_config"]["hooks"]) == {"UserPromptSubmit", "Stop"}
assert all(handlers[0]["hooks"][0]["timeout"] == 5 for handlers in definition["plugin_config"]["hooks"].values())
version = probe.read(RUN / "commands/cursor-file-version.json")
assert version["process_exited"] and version["exit_code"] == 0
metadata = probe.read(RUN / "native-metadata.json")
assert all((probe.digest_file(Path(row["path"])) if Path(row["path"]).is_file() else None) == row["sha256"]
    for row in metadata["protected_config"])
assert not (RUN / "prompt-intent-alias.json").exists()
probe.atomic_json(RUN / "preparation-terminal-reconciliation.json", {"status": "verified-prepared-state-after-controller-output-loss",
    "version_command_exit_code": 0, "outer_prepare_helper_exit_code": "not-retained",
    "outer_handle": "69965 missing on subsequent poll", "source_lock_hash": probe.EXPECTED,
    "preparation": probe.bind(RUN / "preparation.json"), "failure": probe.bind(RUN / "preparation-controller-observation-failure.json"),
    "missing_handle": probe.bind(RUN / "preparation-terminal-observation-02.json"), "preparation_rerun": False,
    "model_prompts_submitted": 0, "protected_global_configs_unchanged": True})
audit = (RUN / "audit-before-native.ps1").read_text(encoding="utf8")
assert audit.count("'process-preflight.json'") == 1
with (RUN / "audit-before-launch.ps1").open("x", encoding="utf8") as stream:
    stream.write(audit.replace("'process-preflight.json'", "'prelaunch-process-audit.json'"))
print(json.dumps({"status": "verified-prepared-state-after-controller-output-loss", "preparation_rerun": False, "model_prompts": 0}))
