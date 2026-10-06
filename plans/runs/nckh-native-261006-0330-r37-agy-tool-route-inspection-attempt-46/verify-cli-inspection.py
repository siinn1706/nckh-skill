"""Verify native help/inventory evidence without qualifying model or tool execution."""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path": path.relative_to(WORK).as_posix(), "sha256": sha(path)}
frozen = read(RUN / "frozen-brief.json")
inventory_brief = read(RUN / "agent-inventory-brief.json")
audit = read(RUN / "process-final-audit.json")
assert audit["matching_count"] == audit["tracked_live_count"] == 0
assert sha(Path(frozen["CLI"])) == frozen["CLI_executable_sha256"]
assert inventory_brief["controller_sha256"] == sha(RUN / "inspect-cli-routes.py")
commands = []
for name, expected in zip(("agy-version", "agy-help", "agy-agents-help", "agy-agents"), frozen["commands"] + inventory_brief["commands"]):
    path = RUN / "commands" / (name + ".json")
    row = read(path)
    assert row["command"] == expected and row["exit_code"] == 0 and row["process_exited"]
    assert not row["capture_errors"] and not row["owned_handle_stop_performed"]
    stdout = RUN / "commands" / (name + ".stdout.txt")
    stderr = RUN / "commands" / (name + ".stderr.txt")
    assert sha(stdout) == row["stdout_sha256"] and sha(stderr) == row["stderr_sha256"]
    commands.append({"name": name, "receipt": bind(path), "stdout": bind(stdout), "stderr": bind(stderr)})
version = (RUN / "commands/agy-version.stdout.txt").read_text(encoding="utf8").strip()
help_text = (RUN / "commands/agy-help.stderr.txt").read_text(encoding="utf8")
agent_help = (RUN / "commands/agy-agents-help.stdout.txt").read_text(encoding="utf8") + (RUN / "commands/agy-agents-help.stderr.txt").read_text(encoding="utf8")
agents = [line.strip() for line in (RUN / "commands/agy-agents.stdout.txt").read_text(encoding="utf8").splitlines() if line.strip()]
assert version == "1.2.17" and len(agents) == len(set(agents)) == 16
assert "Explore" in agents and "fullstack-developer" in agents
assert "  --agent " in help_text and "  agents " in help_text and "List available agents" in help_text
assert "Usage: agy.exe agent [flags]" in agent_help and "List available agents" in agent_help
assert len((RUN / "commands/agy-help.stdout.txt").read_bytes()) == 0
protected = []
for row in frozen["protected_configs"]:
    path = Path(row["path"])
    current = sha(path) if path.is_file() else None
    assert current == row["sha256"], "Protected configuration changed; inspect before continuing"
    protected.append({**row, "current_sha256": current})
assert not (Path(frozen["project"]) / ".agents/hooks.json").exists()
sys.path.insert(0, str(WORK / "nckh-kit"))
from core.paths import digest_record
lock = read(WORK / "nckh-kit/core/registry/source-lock/source-lock.json")
assert digest_record(lock) == frozen["source_lock_hash"]
record = {
    "status": "verified-read-only-native-AGY-help-and-agent-inventory", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "source_revision": 37, "source_lock_hash": frozen["source_lock_hash"], "source_identity_check_only": True,
    "version": version, "commands": commands, "agent_names": agents, "agent_count": len(agents),
    "native_help_observations": {"session_agent_selector": "--agent", "agents_alias": "agents", "help_stream": "stderr",
        "agent_help_flags": ["-h", "--help"], "per_agent_tool_mapping": "not-exposed-in-observed-help-or-inventory"},
    "effective_selected_agent": "not-established; no session started", "callable_toolset": "unqualified",
    "model_prompts": 0, "tool_requests": 0, "hook_activation": "not-performed", "global_direct_writes": False,
    "process_union_identities": len(audit["tracked"]), "processes_live": 0, "process_stop_performed": False,
    "process_audit": bind(RUN / "process-final-audit.json"), "protected_configs": protected,
    "controller_initial_sha256": frozen["controller_sha256"], "controller_inventory_sha256": inventory_brief["controller_sha256"],
    "controller_adaptation": "added inventory action after reading actual native help; no source-kit change",
    "frozen_brief": bind(RUN / "frozen-brief.json"), "inventory_brief": bind(RUN / "agent-inventory-brief.json"),
    "search35_failed_oracles": "retained; agent names do not prove a callable tool handler",
    "full_native_gate": "unchecked", "review": "inline; no independent reviewer", "verifier": bind(Path(__file__)),
}
with (RUN / "verified-cli-inspection.json").open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": record["status"], "commands": len(commands), "agent_count": len(agents),
    "model_prompts": 0, "process_union": len(audit["tracked"]), "live": 0}))
