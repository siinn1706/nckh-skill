"""Verify the frozen inactive proposal without executing a hook or installing it."""

import ctypes
import hashlib
import json
import tomllib
from ctypes import wintypes
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
canonical = lambda value: hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf8")).hexdigest()
proposal = read(RUN / "plugin-proposal.json")
root = Path(proposal["proposal_root"])
members = {path.relative_to(root).as_posix(): sha(path) for path in sorted(root.rglob("*")) if path.is_file()}
assert members == proposal["proposal_members"] and len(members) == 33
assert canonical(members) == proposal["proposal_tree_hash"]
assert sha(RUN / "prepare-plugin-proposal.py") == proposal["controller_sha256"]
assert not Path(proposal["cache_prefix"]).exists(), "Cache preimage changed; new preview required"
package = Path(r"C:/Users/USER\.codex\visualizations\2026\10\04\01a104fc-f969-7f43-b1e0-1a6774f0e0c8\nckh-hooks-r37-1640-attempt-02\extracted\on-standalone\codex")
runtime = root / "plugins" / proposal["plugin_name"] / "hooks/runtime"
payload = {path.relative_to(runtime).as_posix(): sha(path) for path in runtime.rglob("*") if path.is_file()}
assert len(payload) == 26
for relative, expected in payload.items():
    assert sha(package / relative) == expected, relative
compiled = 0
for relative in members:
    path = root / relative
    if path.suffix == ".json":
        read(path)
    elif path.suffix == ".py":
        compile(path.read_text(encoding="utf8"), str(path), "exec")
        compiled += 1
plugin = read(root / "plugins" / proposal["plugin_name"] / "plugin.json")
assert plugin["name"] == proposal["plugin_name"]
assert plugin["extensions"]["com.openai"]["hooks"] == "./hooks/hooks.json"
marketplace = read(root / "marketplace.json")
assert marketplace["name"] == proposal["marketplace_name"] and len(marketplace["plugins"]) == 1
entry = marketplace["plugins"][0]
assert entry["source"] == {"source": "local", "path": "./plugins/" + proposal["plugin_name"]}
assert entry["policy"] == {"installation": "AVAILABLE", "authentication": "ON_USE"}
config = tomllib.loads((root / "project-config.toml").read_text(encoding="utf8"))
identity = proposal["plugin_name"] + "@" + proposal["marketplace_name"]
assert config == {"plugins": {identity: {"enabled": True}}}
project = Path(proposal["project"])
project_preimages = {}
for relative in proposal["proposed_project_files"]:
    target = project / relative
    assert not target.exists(), "Existing proposed target; do not overwrite: " + relative
    project_preimages[relative] = "absent"
native_config = tomllib.loads(Path(r"C:/Users/USER\.codex\config.toml").read_text(encoding="utf8"))
trusted = [value for key, value in native_config.get("projects", {}).items() if str(Path(key).resolve()).casefold() == str(project.resolve()).casefold()]
assert len(trusted) == 1 and trusted[0].get("trust_level") == "trusted"
assert identity not in native_config.get("plugins", {})
kernel = ctypes.WinDLL("shell32", use_last_error=True)
kernel.CommandLineToArgvW.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(ctypes.c_int)]
kernel.CommandLineToArgvW.restype = ctypes.POINTER(wintypes.LPWSTR)
free = ctypes.WinDLL("kernel32", use_last_error=True).LocalFree
free.argtypes = [wintypes.HLOCAL]
free.restype = wintypes.HLOCAL
command_checks = []
for source, hooks_path in (
    ("project", root / "project-hooks.json"),
    ("plugin", root / "plugins" / proposal["plugin_name"] / "hooks/hooks.json"),
):
    hooks = read(hooks_path)["hooks"]
    assert set(hooks) == set(proposal["events"])
    for event, groups in hooks.items():
        assert len(groups) == 1 and groups[0]["matcher"] == ".*"
        handlers = groups[0]["hooks"]
        assert len(handlers) == 1
        handler = handlers[0]
        assert handler["type"] == "command" and handler["timeout"] == 5
        command = handler["command"]
        size = ctypes.c_int()
        argv = kernel.CommandLineToArgvW(command, ctypes.byref(size))
        assert argv
        try:
            parts = [argv[index] for index in range(size.value)]
        finally:
            free(argv)
        assert parts[1:4] == ["-X", "utf8", "-B"]
        assert parts[parts.index("--event") + 1] == event
        assert parts[parts.index("--callback-source") + 1] == source
        assert parts[parts.index("--project") + 1] == str(project)
        observer = parts[4]
        runner = parts[parts.index("--runner") + 1]
        if source == "plugin":
            assert observer == "${PLUGIN_ROOT}/hooks/probe-observer.py"
            assert runner == "${PLUGIN_ROOT}/hooks/runtime/hooks/runner.py"
        else:
            assert observer == str(project / "plugins" / proposal["plugin_name"] / "hooks/probe-observer.py")
            assert runner == str(project / "plugins" / proposal["plugin_name"] / "hooks/runtime/hooks/runner.py")
        command_checks.append({"source": source, "event": event, "command_sha256": hashlib.sha256(command.encode()).hexdigest(), "windows_argv_roundtrip": True})
schema = read(RUN / "native-schema/v2/HooksListResponse.json")["definitions"]
assert {"project", "plugin", "sessionFlags"} <= set(schema["HookSource"]["enum"])
assert {"eventName", "currentHash", "source", "sourcePath", "pluginId", "timeoutSec", "trustStatus"} <= set(schema["HookMetadata"]["properties"])
record = {
    "status": "verified-inactive-proposal-static-preparation-only",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "proposal_sha256": sha(RUN / "plugin-proposal.json"), "proposal_tree_hash": canonical(members),
    "proposal_files": len(members), "unchanged_packaged_payload_files": len(payload), "python_files_compiled_in_memory": compiled,
    "project_target_preimages": project_preimages, "cache_preimage": "absent", "native_trusted_project_reused": True,
    "command_checks": command_checks,
    "windows_placeholder_delivery": "unverified; installed native host must resolve the plugin command and deliver a genuine lifecycle callback before a model turn",
    "native_metadata_cleanup": "native uninstall only; retention or changed unrelated state must be reported, not overwritten",
    "global_state": {"config_sha256": sha(Path(r"C:/Users/USER\.codex\config.toml")), "hooks_sha256": sha(Path(r"C:/Users/USER\.codex\hooks.json"))},
    "model_prompts": 0, "hook_executions": 0, "native_installation": "not-performed", "full_native_gate": "unchecked",
    "verifier_sha256": sha(Path(__file__)),
}
target = RUN / "verified-plugin-proposal.json"
with target.open("x", encoding="utf8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({key: record[key] for key in ("status", "proposal_files", "unchanged_packaged_payload_files", "python_files_compiled_in_memory", "model_prompts")}))
