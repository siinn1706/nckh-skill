"""Project-only, hash-bound hook configuration; skill installation and trust are separate."""

import json
import os
import shlex
import subprocess
import sys
import uuid
from copy import deepcopy
from pathlib import Path

from core.paths import (atomic_bytes, atomic_json, contained, digest_bytes, digest_file,
                        digest_record, exclusive_file_lock, no_links)
from core.schema import ContractError
from hooks.runner import strict_json

TARGETS = {"claude": ".claude/settings.local.json", "codex": ".codex/hooks.json",
           "cursor": ".cursor/hooks.json", "agy": ".agents/hooks.json"}
SURFACES = {"claude": {"claude-code"}, "codex": {"codex-cli", "codex-desktop", "codex-ide"},
            "cursor": {"cursor-cli", "cursor-ide"}, "agy": {"agy-cli", "agy-ide"}}
EVENTS = {"claude": ("SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop"),
          "codex": ("SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop"),
          "cursor": ("sessionStart", "beforeSubmitPrompt", "preToolUse", "postToolUse", "stop"),
          "agy": ("PreToolUse", "PostToolUse", "PreInvocation", "PostInvocation", "Stop")}
STATE = ".nckh-state/hooks/ownership.json"
MAX_CONFIG_BYTES = 1048576
FINAL_TRANSACTION_STATES = {"committed", "rolled-back", "recovered"}


def _json_bytes(record):
    return (json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf8")


def _unfinished(project):
    directory = contained(project, ".nckh-state/hooks/transactions")
    if directory.exists():
        for path in directory.glob("*.json"):
            record = strict_json(_bytes(path))
            if record.get("status") not in FINAL_TRANSACTION_STATES:
                raise ContractError("unfinished hook transaction; review and recover its matching journal first")


def _bytes(path):
    path = no_links(path)
    if not path.exists():
        return None
    if not path.is_file() or path.stat().st_size > MAX_CONFIG_BYTES:
        raise ContractError("hook config/state oversized or not a file")
    return path.read_bytes()


def _hash(data):
    return digest_bytes(data) if data is not None else None


def _parent(path):
    path = no_links(path).parent
    while not path.exists():
        path = path.parent
    stat = path.stat()
    return {"path": str(path.resolve()), "device": stat.st_dev, "inode": stat.st_ino}


def _validate_parent(record):
    path = no_links(record["path"])
    stat = path.stat()
    if stat.st_dev != record["device"] or stat.st_ino != record["inode"]:
        raise ContractError("config parent identity changed after preview")


def _state(project):
    data = _bytes(contained(project, STATE))
    record = strict_json(data) if data is not None else {"schema_version": 1, "configs": {}}
    if set(record) != {"schema_version", "configs"} or record["schema_version"] != 1 or not isinstance(record["configs"], dict):
        raise ContractError("unknown hook ownership; no write")
    return record, _hash(data)


def payload_from_bundle(package):
    from core.build import verify_bundle
    package = no_links(package).resolve()
    manifest = verify_bundle(package)
    hook = manifest.get("hooks")
    if not hook:
        raise ContractError("bundle has no inactive hook payload")
    records = {row["path"]: row for row in manifest["files"]}
    members = {path: records[path]["sha256"] for path in hook["members"]}
    return {"root": str(package), "host": manifest["host"], "members": members,
            "closure_hash": digest_record(members), "runner": hook["entrypoint"],
            "package_manifest_hash": digest_record(manifest)}


def preview_install_hooks(targets, project, *, setting="advisory", scope="project"):
    """Prepare independent owned hook transactions before skill installation."""
    if setting == "off":
        return []
    if setting != "advisory":
        raise ContractError("installer hooks must be advisory or off")
    if scope != "project":
        raise ContractError("automatic hooks require project scope; use --hooks off for global skills")
    previews = []
    seen = set()
    for target in targets:
        host = target["host"]
        if host in seen:
            continue
        seen.add(host)
        preview = preview_config(project, host, payload_from_bundle(Path(target["bundle"])),
                                 events=EVENTS[host], surface=target["surface"], mode="advisory")
        owned = _state(Path(project))[0]["configs"].get(host)
        if owned and owned.get("mode", "enforce") != "advisory":
            raise ContractError("existing enforcement hooks require an explicit mode change; no automatic downgrade")
        previews.append(preview)
    return previews


def apply_install_hooks(previews, *, grant_reference):
    results = []
    for previous in previews:
        _validate_parent(previous["resolved_parent"])
        # Earlier host writes change shared ownership; recompute without widening
        # the confirmed target config, context, interpreter or hook definitions.
        fresh = preview_config(Path(previous["project"]), previous["host"], previous["payload"],
            events=[row["event"] for row in previous["definitions"]],
            context_reference=previous["context_reference"], surface=previous["surface"], mode="advisory")
        for key in ("before_hash", "context_hash", "python_sha256", "after", "definitions"):
            if fresh[key] != previous[key]:
                raise ContractError("hook inputs changed after install preview; re-preview")
        result = apply_config(fresh, approved_hash=digest_record(fresh), grant_reference=grant_reference)
        results.append({"host": fresh["host"], "mode": "advisory", "status": result["status"],
                        "configured_enabled": True, "native_qualification": "unverified", "trusted": False})
    return results


def _verify_payload(payload):
    root = no_links(payload["root"])
    if (payload["host"] not in TARGETS or not payload["members"] or len(payload["members"]) > 64
            or digest_record(payload["members"]) != payload["closure_hash"]
            or payload["runner"] not in payload["members"]):
        raise ContractError("hook payload manifest invalid")
    for relative, expected in payload["members"].items():
        path = contained(root, relative)
        if not relative.startswith("hooks/") or not path.is_file() or digest_file(path) != expected:
            raise ContractError("hook payload missing, changed or escaping")


def _definition(host, event, argv, *, mode="enforce"):
    command = subprocess.list2cmdline(argv) if os.name == "nt" else shlex.join(argv)
    timeout = 20 if host == "cursor" and event == "preToolUse" else 5
    handler = {"type": "command", "command": command, "timeout": timeout}
    if host == "claude":
        handler["command"] = argv[0]
        handler["args"] = argv[1:]
    if host == "cursor":
        if event == "preToolUse":
            handler["failClosed"] = mode == "enforce"
        if event == "stop":
            handler["loop_limit"] = 1
        return handler
    if host == "agy" and event not in {"PreToolUse", "PostToolUse"}:
        return handler
    return {"matcher": ".*", "hooks": [handler]}


def _entries(config, host, event, *, create=False):
    if host == "agy":
        area = config.setdefault("nckh", {"enabled": True}) if create else config.get("nckh", {})
    else:
        area = config.setdefault("hooks", {}) if create else config.get("hooks", {})
    if not isinstance(area, dict):
        raise ContractError("host hook/group root is not an object")
    rows = area.setdefault(event, []) if create else area.get(event, [])
    if not isinstance(rows, list):
        raise ContractError("host event definitions are not an array")
    return rows


def preview_config(project, host, payload, *, action="apply", events=None,
                   context_reference=".nckh-state/hooks/context/current.json", host_version="unverified", surface="unverified", python=None,
                   mode="enforce"):
    project = no_links(project).resolve()
    if not project.is_dir() or host not in TARGETS or action not in {"apply", "remove"}:
        raise ContractError("explicit existing project/host/action required")
    if surface != "unverified" and surface not in SURFACES[host]:
        raise ContractError("selected native surface differs from hook host")
    if mode not in {"advisory", "enforce"}:
        raise ContractError("unknown hook mode")
    _unfinished(project)
    _verify_payload(payload)
    if payload["host"] != host:
        raise ContractError("hook payload/host mismatch")
    config_path = contained(project, TARGETS[host])
    before = _bytes(config_path)
    config = strict_json(before) if before is not None else ({"version": 1} if host == "cursor" else {})
    if host == "cursor" and config.get("version") != 1:
        raise ContractError("unsupported Cursor hook version")
    index, index_hash = _state(project)
    owned = index["configs"].get(host)
    if action == "remove" and owned:
        mode = owned.get("mode", "enforce")
    updated = deepcopy(config)
    definitions = []
    if owned:
        if owned["target"] != TARGETS[host] or owned["closure_hash"] != payload["closure_hash"]:
            raise ContractError("owned payload differs; remove its matching owned version first")
        if host == "agy" and digest_record(config.get("nckh")) != owned["group_hash"]:
            raise ContractError("rollback-conflict: AGY owned group was edited")
        for row in owned["definitions"]:
            entries = _entries(updated, host, row["event"])
            matches = [number for number, item in enumerate(entries) if digest_record(item) == row["definition_hash"]]
            if len(matches) != 1:
                raise ContractError("rollback-conflict: owned definition missing, edited or duplicated")
            entries.pop(matches[0])
    elif action == "remove":
        raise ContractError("no owned hook configuration to remove")
    elif host == "agy" and "nckh" in updated:
        raise ContractError("unknown owner of existing AGY nckh group")
    runtime_relative = f".nckh-state/hooks/{host}/{payload['closure_hash']}"
    runtime = contained(project, runtime_relative)
    interpreter = no_links(python or sys.executable).resolve()
    if not interpreter.is_file():
        raise ContractError("controller-selected Python unavailable")
    context_path = contained(project, context_reference)
    context_hash = _hash(_bytes(context_path))
    if action == "apply":
        selected = tuple(events or (EVENTS[host][2 if host != "agy" else 0],))
        if not selected or len(set(selected)) != len(selected) or not set(selected) <= set(EVENTS[host]):
            raise ContractError("unsupported or duplicate selected events")
        for event in selected:
            argv = [str(interpreter), "-I", str(contained(runtime, payload["runner"])), "--host", host,
                    "--event", event, "--project", str(project), "--context", context_reference,
                    "--receipt-dir", f".nckh-state/hooks/events/{host}", "--mode", mode]
            definition = _definition(host, event, argv, mode=mode)
            entries = _entries(updated, host, event, create=True)
            if any(item == definition for item in entries):
                raise ContractError("unknown ownership or duplicate project/plugin definition")
            entries.append(definition)
            definitions.append({"id": f"nckh:{host}:{event}:policy", "event": event,
                "json_pointer": f"/nckh/{event}/{len(entries)-1}" if host == "agy" else f"/hooks/{event}/{len(entries)-1}",
                "definition_hash": digest_record(definition)})
    else:
        for row in owned["definitions"]:
            area = updated.get("nckh", {}) if host == "agy" else updated.get("hooks", {})
            if not area.get(row["event"]):
                area.pop(row["event"], None)
        if host == "agy":
            updated.pop("nckh", None)
        elif updated.get("hooks") == {}:
            updated.pop("hooks", None)
    delete_config = bool(action == "remove" and owned["created_config"] and _hash(before) == owned["installed_config_hash"])
    return {"schema_version": 1, "action": action, "project": str(project), "host": host,
        "host_version": host_version, "surface": surface, "target": TARGETS[host], "config_path": str(config_path),
        "resolved_parent": _parent(config_path), "before_hash": _hash(before), "ownership_hash": index_hash,
        "before": config, "after": updated, "delete_config": delete_config, "definitions": definitions,
        "payload": payload, "runtime_relative": runtime_relative, "context_reference": context_reference,
        "context_hash": context_hash, "python_path": str(interpreter), "python_sha256": digest_file(interpreter),
        "mode": mode, "registered": False, "enabled": False, "trusted": False, "native_qualification": "unverified"}


def _references(data, runtime):
    if data is None:
        return False
    needle = str(runtime).replace("\\", "/").casefold()
    def visit(value):
        if isinstance(value, str):
            return needle in value.replace("\\", "/").casefold()
        if isinstance(value, dict):
            return any(visit(item) for item in value.values())
        if isinstance(value, list):
            return any(visit(item) for item in value)
        return False
    return visit(strict_json(data))


def _payload_referenced(project, runtime):
    # Preserve a payload used by any known host, including new unowned entries.
    for target in TARGETS.values():
        try:
            if _references(_bytes(contained(project, target)), runtime):
                return True
        except (ContractError, OSError):
            return True
    return False


def _cleanup_payload(runtime, members):
    for relative, expected in members.items():
        path = contained(runtime, relative)
        if path.is_file() and digest_file(path) == expected:
            path.unlink()
    for path in sorted((p for p in runtime.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
        no_links(path)
        if not any(path.iterdir()):
            path.rmdir()
    if runtime.exists() and not any(runtime.iterdir()):
        runtime.rmdir()


def _restore_transaction(project, journal_path, journal):
    host = journal.get("host")
    if (host not in TARGETS or journal.get("target") != TARGETS[host]
            or journal.get("project") != str(project)
            or journal.get("runtime_relative") != f".nckh-state/hooks/{host}/{journal.get('closure_hash')}"):
        raise ContractError("recovery journal target/ownership mismatch")
    _validate_parent(journal["resolved_parent"])
    restores = []
    for name, target in (("config", TARGETS[host]), ("index", STATE)):
        path = contained(project, target)
        current = _hash(_bytes(path))
        before_hash = journal[name + "_before_hash"]
        after_hash = journal[name + "_after_hash"]
        if current not in {before_hash, after_hash}:
            journal["status"] = "rollback-conflict"
            atomic_json(journal_path, journal)
            return journal
        backup = journal_path.with_suffix("." + name + ".preimage")
        data = _bytes(backup) if before_hash is not None else None
        if _hash(data) != before_hash:
            raise ContractError("recovery preimage missing or changed")
        if current != before_hash:
            restores.append((path, current, data))
    for path, expected, data in restores:
        if _hash(_bytes(path)) != expected:
            journal["status"] = "rollback-conflict"
            atomic_json(journal_path, journal)
            return journal
        if data is None:
            if path.exists():
                path.unlink()
        else:
            atomic_bytes(path, data)
    runtime = contained(project, journal["runtime_relative"])
    if journal["staged_new_payload"] and runtime.exists() and not _payload_referenced(project, runtime):
        _cleanup_payload(runtime, journal["members"])
    journal["status"] = "rolled-back"
    atomic_json(journal_path, journal)
    return journal


def recover_config(project, transaction_reference, *, approved_hash):
    """Restore interrupted owned writes only while both current hashes still match."""
    project = no_links(project).resolve()
    path = contained(project, transaction_reference)
    directory = contained(project, ".nckh-state/hooks/transactions")
    if path.parent != directory or path.suffix != ".json":
        raise ContractError("recovery requires an owned transaction journal")
    with exclusive_file_lock(contained(project, ".nckh-state/hooks/config.lock")):
        journal = strict_json(_bytes(path))
        if digest_record(journal) != approved_hash or journal["status"] in FINAL_TRANSACTION_STATES:
            raise ContractError("recovery journal changed or is already final")
        result = _restore_transaction(project, path, journal)
        if result["status"] == "rolled-back":
            result["status"] = "recovered"
            atomic_json(path, result)
        return result


def apply_config(preview, *, approved_hash, grant_reference=None, native_verified=False, fail_at=None):
    if approved_hash != digest_record(preview):
        raise ContractError("approved preview hash differs")
    mode = preview.get("mode", "enforce")
    if preview["action"] == "apply":
        if not grant_reference:
            raise ContractError("activation requires a human grant")
        if mode == "enforce" and (not native_verified or preview["host_version"] == "unverified"
                or preview["surface"] == "unverified" or preview["context_hash"] is None):
            raise ContractError("enforcement requires context and verified native event/version evidence")
    project = no_links(preview["project"]).resolve()
    if preview["target"] != TARGETS.get(preview["host"]) or str(contained(project, preview["target"])) != preview["config_path"]:
        raise ContractError("configuration target changed")
    state_path = contained(project, STATE)
    config_path = contained(project, preview["target"])
    payload = preview["payload"]
    if preview["runtime_relative"] != f".nckh-state/hooks/{preview['host']}/{payload['closure_hash']}":
        raise ContractError("owned runtime target changed")
    runtime = contained(project, preview["runtime_relative"])
    journal_path = contained(project, ".nckh-state/hooks/transactions/" + approved_hash + "-" + uuid.uuid4().hex + ".json")
    with exclusive_file_lock(contained(project, ".nckh-state/hooks/config.lock")):
        _validate_parent(preview["resolved_parent"])
        _verify_payload(payload)
        before = _bytes(config_path)
        index_before = _bytes(state_path)
        index, index_hash = _state(project)
        if (_hash(before) != preview["before_hash"] or index_hash != preview["ownership_hash"]
                or _hash(_bytes(contained(project, preview["context_reference"]))) != preview["context_hash"]
                or digest_file(no_links(preview["python_path"])) != preview["python_sha256"]):
            raise ContractError("changed after preview; no config write, re-preview")
        recomputed = preview_config(project, preview["host"], payload, action=preview["action"],
            events=[row["event"] for row in preview["definitions"]] if preview["action"] == "apply" else None,
            context_reference=preview["context_reference"], host_version=preview["host_version"],
            surface=preview["surface"], python=preview["python_path"], mode=mode)
        if digest_record(recomputed) != approved_hash:
            raise ContractError("preview operations/ownership changed; no write")
        config_after = None if preview["delete_config"] else _json_bytes(preview["after"])
        old = index["configs"].get(preview["host"])
        if preview["action"] == "apply":
            index["configs"][preview["host"]] = {"target": preview["target"], "closure_hash": payload["closure_hash"],
                "members": payload["members"], "runtime_relative": preview["runtime_relative"],
                "definitions": preview["definitions"], "created_config": old["created_config"] if old else before is None,
                "installed_config_hash": _hash(config_after), "group_hash": digest_record(preview["after"].get("nckh")),
                "registered": True, "enabled": True, "trusted": False, "mode": mode,
                "native_qualification": "unverified" if mode == "advisory" else "caller-evidence-required"}
        else:
            index["configs"].pop(preview["host"])
        index_after = _json_bytes(index)
        for name, data in (("config", before), ("index", index_before)):
            if data is not None:
                atomic_bytes(journal_path.with_suffix("." + name + ".preimage"), data)
        journal = {"schema_version": 1, "preview_hash": approved_hash, "status": "staging",
            "project": str(project), "host": preview["host"], "target": preview["target"],
            "resolved_parent": preview["resolved_parent"], "grant_reference": grant_reference,
            "config_before_hash": _hash(before), "config_after_hash": _hash(config_after),
            "index_before_hash": _hash(index_before), "index_after_hash": _hash(index_after),
            "closure_hash": payload["closure_hash"], "members": payload["members"],
            "runtime_relative": preview["runtime_relative"],
            "staged_new_payload": preview["action"] == "apply" and not runtime.exists()}
        atomic_json(journal_path, journal)
        try:
            if preview["action"] == "apply":
                if runtime.exists():
                    actual = {p.relative_to(runtime).as_posix() for p in runtime.rglob("*") if p.is_file()}
                    if actual != set(payload["members"]) or any(digest_file(contained(runtime, rel)) != sha for rel, sha in payload["members"].items()):
                        raise ContractError("stable owned payload collision/drift")
                else:
                    runtime.mkdir(parents=True)
                    for rel, sha in payload["members"].items():
                        data = contained(payload["root"], rel).read_bytes()
                        if digest_bytes(data) != sha:
                            raise ContractError("payload changed during staging")
                        atomic_bytes(contained(runtime, rel), data)
                if fail_at == "payload":
                    raise ContractError("injected payload failure")
            no_links(config_path)
            _validate_parent(preview["resolved_parent"])
            if preview["action"] == "apply" and any(digest_file(contained(runtime, rel)) != sha for rel, sha in payload["members"].items()):
                raise ContractError("staged hook payload changed before config write")
            if _hash(_bytes(config_path)) != preview["before_hash"]:
                raise ContractError("config changed immediately before write")
            if preview["delete_config"]:
                config_path.unlink()
            else:
                atomic_bytes(config_path, config_after)
            journal.update(status="config-written")
            atomic_json(journal_path, journal)
            if fail_at == "config":
                raise ContractError("injected config failure")
            if _hash(_bytes(state_path)) != _hash(index_before):
                raise ContractError("ownership changed immediately before write")
            atomic_bytes(state_path, index_after)
            if fail_at == "index":
                raise ContractError("injected ownership failure")
            journal["status"] = "committed"
            atomic_json(journal_path, journal)
        except (ContractError, OSError) as error:
            journal = _restore_transaction(project, journal_path, journal)
            raise ContractError("hook transaction failed; " + journal["status"]) from error
        if preview["action"] == "remove" and not _payload_referenced(project, runtime):
            _cleanup_payload(runtime, payload["members"])
        return journal
