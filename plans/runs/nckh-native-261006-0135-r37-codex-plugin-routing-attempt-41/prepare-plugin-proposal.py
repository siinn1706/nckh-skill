"""Prepare an inactive, hash-bound project/plugin native experiment for review."""

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
KIT = WORK / "nckh-kit"
PROJECT = WORK / "plans/runs/nckh-native-261005-0658-r34-codex-file-attempt-01/project-02"
PACKAGE = Path(r"C:/Users/USER\.codex\visualizations\2026\10\04\01a104fc-f969-7f43-b1e0-1a6774f0e0c8\nckh-hooks-r37-1640-attempt-02\extracted\on-standalone\codex")
EXPECTED = "629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb"
PLUGIN = "nckh-native-hook-probe"
MARKETPLACE = "nckh-native-project-plugins"
PROPOSAL = RUN / "proposal"
EVIDENCE_RELATIVE = ".nckh-native-codex-plugin-duplicate"
EVENTS = ("SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop")
sys.dont_write_bytecode = True
sys.path.insert(0, str(KIT))
from core.build import verify_source_lock
from core.hook_config import payload_from_bundle
from core.paths import contained, digest_file, digest_record

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists()
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf8")


assert digest_record(verify_source_lock(KIT)) == EXPECTED
assert not PROPOSAL.exists()
payload = payload_from_bundle(PACKAGE)
plugin_root = PROPOSAL / "plugins" / PLUGIN
runtime_root = plugin_root / "hooks/runtime"
for relative, expected in payload["members"].items():
    target = contained(runtime_root, relative)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(contained(PACKAGE, relative), target)
    assert digest_file(target) == expected
observer = (RUN / "probe-observer.py").read_bytes()
target = plugin_root / "hooks/probe-observer.py"
target.write_bytes(observer)
write(plugin_root / "plugin.json", {
    "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", "name": PLUGIN,
    "version": "0.0.0", "description": "Owned temporary native hook idempotency probe.",
    "extensions": {"com.openai": {"hooks": "./hooks/hooks.json"}}})
write(PROPOSAL / "marketplace.json", {"name": MARKETPLACE, "plugins": [{"name": PLUGIN,
    "source": {"source": "local", "path": "./plugins/" + PLUGIN},
    "policy": {"installation": "AVAILABLE", "authentication": "ON_USE"}, "category": "Productivity"}]})
project_hooks, plugin_hooks = {}, {}
context_relative = EVIDENCE_RELATIVE + "/context.json"
receipt_relative = EVIDENCE_RELATIVE + "/policy-receipts"
for event in EVENTS:
    common = ["--event", event, "--project", str(PROJECT), "--context", context_relative,
        "--receipt-dir", receipt_relative, "--evidence", str(PROJECT / EVIDENCE_RELATIVE)]
    project_cmd = subprocess.list2cmdline([sys.executable, "-X", "utf8", "-B",
        str(PROJECT / "plugins" / PLUGIN / "hooks/probe-observer.py"), *common,
        "--runner", str(PROJECT / "plugins" / PLUGIN / "hooks/runtime" / payload["runner"]),
        "--callback-source", "project"])
    plugin_cmd = subprocess.list2cmdline([sys.executable, "-X", "utf8", "-B",
        "${PLUGIN_ROOT}/hooks/probe-observer.py", *common,
        "--runner", "${PLUGIN_ROOT}/hooks/runtime/" + payload["runner"], "--callback-source", "plugin"])
    for groups, command in ((project_hooks, project_cmd), (plugin_hooks, plugin_cmd)):
        groups[event] = [{"matcher": ".*", "hooks": [{"type": "command", "command": command, "timeout": 5}]}]
write(PROPOSAL / "project-hooks.json", {"hooks": project_hooks})
write(plugin_root / "hooks/hooks.json", {"hooks": plugin_hooks})
write(PROPOSAL / "context.json", {"schema_version": 1, "task_id": "native-project-plugin-idempotency",
    "brief": {"mode": "auto"}, "tool_operations": {"apply_patch": "write"}, "allowed_operations": ["write"]})
(PROPOSAL / "project-config.toml").write_text('[plugins."' + PLUGIN + '@' + MARKETPLACE + '"]\nenabled = true\n', encoding="utf8")
members = {p.relative_to(PROPOSAL).as_posix(): digest_file(p) for p in sorted(PROPOSAL.rglob("*")) if p.is_file()}
cache_prefix = Path(r"C:/Users/USER\.codex\plugins\cache") / MARKETPLACE / PLUGIN
assert not cache_prefix.exists(), "Existing cache slot; inspect ownership before proposing installation"
recipe = {
    "status": "prepared-inactive-awaiting-cache-authority", "source_revision": 37, "source_lock_hash": EXPECTED,
    "proposal_root": str(PROPOSAL), "proposal_members": members, "proposal_tree_hash": digest_record(members),
    "native_host": "codex-cli", "native_version": "0.154.0", "plugin_name": PLUGIN, "marketplace_name": MARKETPLACE,
    "project": str(PROJECT), "cache_prefix": str(cache_prefix), "cache_preimage": "absent",
    "proposed_project_files": {
        ".agents/plugins/marketplace.json": "marketplace.json", ".codex/config.toml": "project-config.toml",
        ".codex/hooks.json": "project-hooks.json", EVIDENCE_RELATIVE + "/context.json": "context.json",
        "plugins/" + PLUGIN + "/": "plugins/" + PLUGIN + "/"},
    "events": list(EVENTS), "native_prerequisite": "hooks/list must identify project and plugin sources, exact pluginId and current hashes before any model turn",
    "maximum_model_turns": 1, "maximum_requested_native_tools": 1, "model": "gpt-5.6-luna", "effort": "medium",
    "oracle": "Require one project and one plugin callback on each selected event for the same native input/session/tool ID, one idempotent policy receipt per event, one actual patch execution, exact marker bytes; otherwise retain unqualified outcome",
    "context_and_payload_changes": "none after approval without new preview", "trust_route": "existing native-trusted project; invocation-only hook trust bypass",
    "new_trust_keys": "not-proposed", "persistent_global_enablement": "not-proposed",
    "required_new_authority": "native creation/removal of this test plugin cache and associated native installation metadata outside workspace; project test files within existing grant",
    "global_direct_controller_writes": "not-proposed", "cleanup": "native remove exact owned plugin identity; matching-byte project cleanup; preserve user edits/history; verify native cache/config/metadata and process identities",
    "executed": False, "provider_prompts": 0, "installed_update": "not-performed", "full_native_gate": "unchecked",
    "official_source": "https://developers.openai.com/plugins/build/plugins", "controller_sha256": digest_file(Path(__file__))}
write(RUN / "plugin-proposal.json", recipe)
print(json.dumps({"status": recipe["status"], "files": len(members), "tree_hash": recipe["proposal_tree_hash"], "cache_prefix": str(cache_prefix), "model_prompts": 0}), flush=True)
