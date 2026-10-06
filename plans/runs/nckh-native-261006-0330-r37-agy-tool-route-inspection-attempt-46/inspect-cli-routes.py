"""Inspect native CLI help with owned process tracking and no model prompt."""

import argparse
import hashlib
import importlib.util
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PRIOR = RUN.parent / "nckh-native-261006-0300-r37-cursor-workspace-unsupported-event-attempt-45"
PROJECT = WORK / "plans/runs/nckh-native-261005-0005-r34-attempt-01/projects/agy-model"
CLI = Path(r"C:/Users/USER\AppData\Local\agy\bin\agy.exe")
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()

def save_new(path, value):
    with path.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def setup():
    assert CLI.is_file() and PROJECT.is_dir() and not (PROJECT / ".agents/hooks.json").exists()
    assert len(read(PRIOR / "process-final-audit.json")["tracked"]) == 2008
    target = RUN / "owned-cli-command.py"
    assert not target.exists()
    shutil.copyfile(PRIOR / "owned-cli-command.py", target)
    audit = (PRIOR / "audit-owned-processes.ps1").read_text(encoding="utf8")
    assert audit.count("nckh-native-261006-0240-r37-cursor-workspace-duplicates-attempt-44") == 1
    audit = audit.replace("nckh-native-261006-0240-r37-cursor-workspace-duplicates-attempt-44", PRIOR.name).replace("1803", "2008")
    audit = audit.replace("plans\\runs\\nckh-native-261005-0128-r34-cursor-events-attempt-02\\projects\\main",
        "plans\\runs\\nckh-native-261005-0005-r34-attempt-01\\projects\\agy-model")
    with (RUN / "audit-owned-processes.ps1").open("x", encoding="utf8") as stream:
        stream.write(audit)
    protected = [Path(r"C:/Users/USER\.gemini\antigravity-cli\settings.json"), Path(r"C:/Users/USER\.agents\hooks.json")]
    save_new(RUN / "frozen-brief.json", {
        "source_revision": 37, "source_lock_hash": read(PRIOR / "preparation.json")["source_lock_hash"],
        "scope": "read-only installed AGY CLI version/help; adaptive agent help only from observed native syntax",
        "project": str(PROJECT), "CLI": str(CLI), "CLI_executable_sha256": sha(CLI),
        "commands": [[str(CLI), "--version"], [str(CLI), "--help"]],
        "maximum_model_turns": 0, "model_prompts": 0, "tool_requests": 0,
        "global_direct_writes": False, "hook_activation": "not-performed",
        "protected_configs": [{"path": str(path), "sha256": sha(path) if path.is_file() else None} for path in protected],
        "controller_sha256": sha(Path(__file__)), "ownership_helper_sha256": sha(target),
        "full_native_gate": "unchecked", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    })
    print(json.dumps({"status": "prepared-read-only-AGY-inspection", "model_prompts": 0}))

def inspect():
    audit = read(RUN / "process-preflight-audit.json")
    assert audit["matching_count"] == audit["tracked_live_count"] == 0
    assert len(audit["tracked"]) == 2008
    spec = importlib.util.spec_from_file_location("owned_agy_inspection", RUN / "owned-cli-command.py")
    owned = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(owned)
    for name, argv in zip(("agy-version", "agy-help"), read(RUN / "frozen-brief.json")["commands"]):
        record, stdout, stderr = owned.run_command(name, argv, cwd=PROJECT, timeout=45)
        assert record["exit_code"] == 0 and record["process_exited"] and not record["owned_handle_stop_performed"]
        print(stdout.decode("utf8", errors="replace"), flush=True)

def inventory():
    version = (RUN / "commands/agy-version.stdout.txt").read_text(encoding="utf8").strip()
    help_text = (RUN / "commands/agy-help.stderr.txt").read_text(encoding="utf8")
    assert version == "1.2.17" and "List available agents" in help_text
    assert "  agents " in help_text and "  --agent " in help_text
    save_new(RUN / "agent-inventory-brief.json", {
        "scope": "read-only agent help and listed-agent inventory from observed native help",
        "commands": [[str(CLI), "agents", "--help"], [str(CLI), "agents"]],
        "version_evidence_sha256": sha(RUN / "commands/agy-version.stdout.txt"),
        "help_evidence_sha256": sha(RUN / "commands/agy-help.stderr.txt"),
        "model_prompts": 0, "hook_activation": "not-performed", "global_direct_writes": False,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(), "controller_sha256": sha(Path(__file__)),
    })
    spec = importlib.util.spec_from_file_location("owned_agy_inventory", RUN / "owned-cli-command.py")
    owned = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(owned)
    for name, argv in zip(("agy-agents-help", "agy-agents"), read(RUN / "agent-inventory-brief.json")["commands"]):
        record, stdout, stderr = owned.run_command(name, argv, cwd=PROJECT, timeout=45)
        assert record["exit_code"] == 0 and record["process_exited"] and not record["owned_handle_stop_performed"]
        print(stdout.decode("utf8", errors="replace"), flush=True)
        print(stderr.decode("utf8", errors="replace"), flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["setup", "inspect", "inventory"])
    action = parser.parse_args().action
    {"setup": setup, "inspect": inspect, "inventory": inventory}[action]()
