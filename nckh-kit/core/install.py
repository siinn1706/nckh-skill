"""Owned skill transactions with preview, locks, recovery and edit preservation."""

import json
import os
import shutil
import tempfile
import tomllib
import uuid
import warnings
from copy import deepcopy
from contextlib import ExitStack, contextmanager
from pathlib import Path

from core.build import closure, load_json, verify_bundle
from core.models import PROFILES
from core.native import agent_filename, configured_agent
from core.paths import (_is_link_like, atomic_json, contained, device_identity, digest_bytes, digest_file,
                        digest_record, no_links, owned_target, skill_id)
from core.schema import ContractError, validate


SURFACE_HOST = {"claude-code": "claude", "codex-desktop": "codex", "codex-cli": "codex",
                "codex-ide": "codex", "cursor-ide": "cursor", "cursor-cli": "cursor",
                "agy-cli": "agy", "agy-ide": "agy"}


def tree_hash(path):
    path = Path(path)
    if path.is_symlink():
        return "symlink:" + str(path.resolve()) + ":" + tree_hash(path.resolve())
    no_links(path)
    if not path.exists():
        return None
    if path.is_file():
        return "file:" + digest_file(path)
    if not path.is_dir():
        raise ContractError(f"destination is not a regular file or directory: {path}")
    records = []
    for member in path.rglob("*"):
        no_links(member)
        if member.is_file():
            records.append({"path": member.relative_to(path).as_posix(), "sha256": digest_file(member)})
    return digest_record(sorted(records, key=lambda record: record["path"]))


def canonical(path):
    return os.path.normcase(str(Path(path).absolute())).casefold()


def read_index(state_dir):
    path = contained(state_dir, "ownership.json")
    if not path.exists():
        return {"schema_version": 1, "items": {}, "installs": {}, "policies": {}}
    value = load_json(path)
    if type(value.get("schema_version")) is not int or value["schema_version"] != 1 or set(value) != {"schema_version", "items", "installs", "policies"}:
        raise ContractError("unknown/corrupt ownership manifest")
    if any(not isinstance(value[key], dict) for key in ("items", "installs", "policies")):
        raise ContractError("invalid ownership collections")
    return value


def _scan_home(home):
    """Link-free home for a project install's global-root scan, or None for the legacy scan.

    Home is only read to find home-level roots; a link-like component there must not
    block a project install, so the target falls back to the scan that classifies by
    ``Path.home()`` and a warning names the linked component.
    """
    try:
        return str(no_links(home))
    except ContractError as error:
        warnings.warn(f"home directory not recorded for the visibility scan ({error}); "
                      "pass --home with a link-free path to scan its global roots", stacklevel=3)
        return None


def inspect_target_paths(package, surfaces, *, scope, project, home):
    """Read unverified path specs; plan_install authenticates their bundle bytes."""
    if scope not in {"project", "global"} or not surfaces or not set(surfaces) <= SURFACE_HOST.keys():
        raise ContractError("explicit valid runtime/scope required")
    base = no_links(project if scope == "project" else home)
    # A global install's base already is home; only a project install records it.
    scan_home = _scan_home(home) if scope == "project" else None
    targets = []
    for surface in sorted(set(surfaces)):
        host = SURFACE_HOST[surface]
        bundle = Path(package) if (Path(package) / "manifest.json").is_file() else Path(package) / host
        adapter = load_json(contained(bundle, "adapter.json"))
        spec = adapter["surfaces"][surface]
        root = contained(base, spec[scope])
        target = {"surface": surface, "host": host, "bundle": str(no_links(bundle)),
                  "root": str(root), "base": str(base)}
        if scan_home is not None:
            target["home"] = scan_home
        targets.append(target)
    return targets


def resolve_targets(package, surfaces, *, scope, project, home):
    return refresh_targets(inspect_target_paths(package, surfaces, scope=scope, project=project, home=home), scope)


def install_identity(targets, scope):
    return digest_record({"surfaces": [t["surface"] for t in targets],
                          "roots": [t["root"] for t in targets], "scope": scope})[:24]


VISIBILITY_PRUNE_DIRS = frozenset({".git", "node_modules", ".venv", "venv", "site-packages",
                                  "__pycache__", "dist", "build", ".tox", "appdata"})
VISIBILITY_MAX_DEPTH = 8


def linked_directory(path):
    """Same link test as no_links: cloud placeholders are traversed, name surrogates are not."""
    return _is_link_like(os.lstat(path))


def nested_visibility_roots(base, roots):
    """Visit bounded project descendants and never traverse linked/vendor trees."""
    relatives = [Path(relative) for relative in roots]
    def walk_error(error):
        raise ContractError("cannot inspect project visibility: " + str(error)) from error
    for directory, children, _ in os.walk(base, topdown=True, followlinks=False, onerror=walk_error):
        current = Path(directory)
        depth = len(current.relative_to(base).parts)
        children[:] = [name for name in children
                       if depth < VISIBILITY_MAX_DEPTH and name.casefold() not in VISIBILITY_PRUNE_DIRS
                       and not linked_directory(current / name)]
        for relative in relatives:
            if (len(current.parts) >= len(relative.parts)
                    and current.parts[-len(relative.parts):] == relative.parts):
                yield current
                # Definitions inside a skill/agent root cannot contain nested projects.
                children[:] = []


VISIBILITY_ACKNOWLEDGEABLE = frozenset({"ancestor", "global"})


def visibility_conflicts(targets, skill_ids, *, scope="project", agents=False):
    """Check parent/nested/compatibility roots, not merely the direct destination.

    Each visible path carries its source kind: ``destination`` (written by this
    install), ``nested`` (any other root inside or directly at the install base,
    including a sibling home-level root beside a global destination), ``global``
    (a root directly under the home directory seen from a project install) or
    ``ancestor`` (a root above the install base). A project install reads home from
    its target; when that home is not an ancestor of the project, its roots are
    probed as ``global`` too. A target recorded without home (an older plan or
    install) keeps the earlier scan, classifying by ``Path.home()`` only.
    """
    target_paths = {}
    for target in targets:
        root = Path(target["agent_destination"] if agents else target["root"])
        for identity in skill_ids:
            name = agent_filename(target["host"], identity) if agents else identity
            target_paths.setdefault(identity, set()).add(canonical(root / name))
    conflicts = []
    for target in targets:
        base = Path(target["base"])
        recorded_home = target.get("home") if scope == "project" else None
        home_path = base if scope == "global" else Path(recorded_home or Path.home())
        home = canonical(home_path)
        roots = set(target["adapter"]["compatibility_project"])
        roots.update(surface["global"] for surface in target["adapter"]["surfaces"].values())
        if agents:
            roots = {root.replace("/skills", "/agents") for root in roots}
        destination = Path(target["agent_destination"] if agents else target["root"])
        candidates = {canonical(destination): (destination, "destination")}
        if scope == "project" and base.exists():
            for root in nested_visibility_roots(base, roots):
                candidates.setdefault(canonical(root), (root, "nested"))
        for parent in [base, *base.parents]:
            # A global install's base is home, so other roots there are siblings of the
            # destination and block exactly like roots at a project base.
            if parent == base:
                kind = "nested"
            else:
                kind = "global" if canonical(parent) == home else "ancestor"
            for rel in roots:
                candidates.setdefault(canonical(parent / rel), (parent / rel, kind))
        if recorded_home and home not in {canonical(parent) for parent in [base, *base.parents]}:
            for rel in roots:
                candidates.setdefault(canonical(home_path / rel), (home_path / rel, "global"))
        for root, _ in candidates.values():
            no_links(root)
        for identity in skill_ids:
            visible = {}
            names = [identity + ".md", identity + ".toml"] if agents else [identity]
            for root, kind in candidates.values():
                for name in names:
                    path = root / name
                    key = canonical(path)
                    if key in target_paths[identity]:
                        visible[key] = (str(path), "destination")
                    elif path.exists() or path.is_symlink():
                        visible[key] = (str(path), kind)
            if len(visible) > 1:
                rows = sorted(visible.values())
                conflicts.append({"skill": identity, "physical_paths": [path for path, _ in rows],
                                  "sources": [{"path": path, "source": kind} for path, kind in rows],
                                  "surface": target["surface"], "reason": "duplicate visible definitions; no native dedup proof"})
    return conflicts


def acknowledgeable_visibility(conflict):
    """Only a single destination plus ancestor/global copies may be accepted by the user."""
    kinds = [row["source"] for row in conflict["sources"]]
    return kinds.count("destination") <= 1 and set(kinds) - {"destination"} <= VISIBILITY_ACKNOWLEDGEABLE


def _visibility_key(conflict):
    return (conflict["skill"], conflict["surface"],
            tuple(sorted((row["path"], row["source"]) for row in conflict["sources"])))


def plan_install(targets, index, *, kits, mode, profile, scope, replace_skills=(), keep_edited=False,
                 capabilities=None, operation="install", candidate_evidence=None, with_agents=False,
                 acknowledge_ancestor_visibility=False):
    if not kits or not set(kits) <= {"core", "engineer", "marketing"}:
        raise ContractError("explicit kit selection required")
    if mode not in {"copy", "symlink"} or profile not in PROFILES:
        raise ContractError("explicit copy/symlink and model policy required")
    if operation not in {"install", "update", "config-models"}:
        raise ContractError("explicit install/update operation required")
    targets = refresh_targets(targets, scope)
    if profile == "custom" and (not with_agents or not (capabilities or {}).get("native_models")):
        raise ContractError("custom native model mapping unavailable/unverified; do not claim applied")
    install_id = install_identity(targets, scope)
    if operation in {"update", "config-models"} and install_id not in index["installs"]:
        raise ContractError("update requires an existing owned install")
    desired, entries, roots, resolutions = {}, [], {t["root"] for t in targets}, {}
    for target in targets:
        if mode == "symlink" and not (capabilities or {}).get("symlink_qualified", {}).get(target["surface"]):
            raise ContractError("symlink target/OS qualification missing; select copy explicitly")
        manifest = target["manifest"]
        available = {s["id"]: s for s in manifest["skills"]}
        chosen = {s["id"] for s in available.values() if s["kit"] in kits or s["kit"] == "tooling" and "engineer" in kits}
        if set(kits) & {"engineer", "marketing"}:
            chosen.update({"nckh-plan", "nckh-cook", "nckh-review", "nckh-handoff"})
        if not chosen <= available.keys():
            raise ContractError("bundle does not contain selected kit dependencies")
        for skill in sorted(chosen):
            source = contained(target["bundle"], "skills/" + skill_id(skill))
            expected = tree_hash(source)
            if expected != available[skill]["tree_hash"]:
                raise ContractError("skill tree hash differs from build manifest")
            final_hash = expected if mode == "copy" else "symlink:" + str(source.resolve()) + ":" + expected
            path = owned_target(target["root"], skill)
            no_links(path.parent)
            key = canonical(path)
            candidate = {"skill": skill, "physical_path": str(path), "canonical_path": key,
                         "kind": "skill",
                         "source": str(source), "tree_hash": final_hash, "mode": mode,
                         "representation": "shared-neutral", "visible_surfaces": [target["surface"]],
                         "owners": [install_id], "symlink_target": str(source.resolve()) if mode == "symlink" else None,
                         "precedence_evidence": "unverified", "action": None, "before_hash": None}
            previous = desired.get(key) or index["items"].get(key)
            if previous and previous["tree_hash"] != final_hash:
                if key in desired or set(previous["owners"]) - {install_id}:
                    raise ContractError("same physical path has differing projections/shared owners; conflict before write")
            if previous and set(previous["visible_surfaces"]) != {target["surface"]}:
                required_surfaces = set(previous["visible_surfaces"]) | {target["surface"]}
                if not required_surfaces <= set((capabilities or {}).get("qualified_neutral_consumers", [])):
                    raise ContractError("shared visibility consumers require actual neutral/dedup qualification")
            if key in desired:
                desired[key]["visible_surfaces"] = sorted(set(desired[key]["visible_surfaces"]) | {target["surface"]})
                continue
            current_hash = tree_hash(path)
            old = index["items"].get(key)
            candidate["before_hash"] = current_hash
            if current_hash is None:
                candidate["action"] = "create"
            elif old is None:
                candidate["action"] = "conflict"
            elif current_hash == final_hash:
                candidate["action"] = "unchanged"
            elif current_hash != old["tree_hash"]:
                candidate["action"] = "replace" if skill in replace_skills else "keep-edited" if keep_edited else "conflict"
            else:
                candidate["action"] = "replace"
            if old:
                candidate["owners"] = sorted(set(old["owners"]) | {install_id})
                candidate["visible_surfaces"] = sorted(set(old["visible_surfaces"]) | {target["surface"]})
                if candidate["action"] == "replace" and set(old["owners"]) - {install_id}:
                    raise ContractError("cannot update shared content without its other owners")
                if operation == "install" and candidate["action"] == "replace" and old["tree_hash"] != final_hash:
                    candidate["action"] = "conflict"
            desired[key] = candidate
            entries.append(candidate)
        if with_agents:
            agent_root = contained(target["base"], target["adapter"].get("agent_global_root", target["adapter"]["agent_root"])
                                   if scope == "global" else target["adapter"]["agent_root"])
            roots.add(str(agent_root))
            target["agent_destination"] = str(agent_root)
            for agent in manifest["agents"]:
                name = agent_filename(target["host"], agent["id"])
                path = no_links(agent_root / name)
                source = contained(target["bundle"], agent["path"])
                instructions = contained(target["bundle"], agent["instructions_path"]).read_text(encoding="utf-8")
                content, resolution = configured_agent(target["host"], agent["role"], agent["description"], instructions,
                                                       profile=profile, capabilities=capabilities or {})
                resolutions[target["surface"] + "/" + agent["id"]] = resolution
                final_hash = "file:" + digest_bytes(content.encode("utf-8"))
                key = canonical(path)
                old, current = index["items"].get(key), tree_hash(path)
                previous = desired.get(key)
                if previous:
                    if previous["tree_hash"] != final_hash:
                        raise ContractError("conflicting native agent projections")
                    previous["visible_surfaces"] = sorted(set(previous["visible_surfaces"]) | {target["surface"]})
                    continue
                action = "create" if current is None else "conflict" if old is None else "unchanged" if current == final_hash else (
                    "replace" if agent["id"] in replace_skills else "keep-edited" if keep_edited else "conflict") if current != old["tree_hash"] else "replace"
                if old and action == "replace" and (operation == "install" or set(old["owners"]) - {install_id}):
                    action = "conflict"
                candidate = {"skill": agent["id"], "kind": "native-agent", "file_name": name, "physical_path": str(path),
                             "canonical_path": key, "source": str(source), "content": content, "tree_hash": final_hash,
                             "mode": "copy", "representation": "host-specific", "visible_surfaces": sorted(set(old["visible_surfaces"] if old else []) | {target["surface"]}),
                             "owners": sorted(set(old["owners"] if old else []) | {install_id}), "symlink_target": None,
                             "precedence_evidence": "unverified", "action": action, "before_hash": current}
                desired[key] = candidate
                entries.append(candidate)
    duplicates = visibility_conflicts(targets, {item["skill"] for item in entries if item["kind"] == "skill"}, scope=scope)
    if with_agents:
        duplicates += visibility_conflicts(targets, {item["skill"] for item in entries if item["kind"] == "native-agent"}, scope=scope, agents=True)
    # Update and model configuration keep an acknowledgement already recorded for this
    # install, but only for the identical skill, surface and source paths; any new or
    # changed duplicate needs the flag again.
    recorded = ({_visibility_key(row) for row in index["installs"][install_id].get("acknowledged_visibility", [])}
                if operation in {"update", "config-models"} else set())
    acknowledged = [row for row in duplicates if acknowledgeable_visibility(row)
                    and (acknowledge_ancestor_visibility or _visibility_key(row) in recorded)]
    blocking = [row for row in duplicates if row not in acknowledged]
    if blocking:
        raise ContractError("duplicate visibility: " + json.dumps(blocking, ensure_ascii=False)
                            + "; remove or rename the non-destination copies listed under sources; only ancestor/global "
                            "copies may be accepted with --acknowledge-ancestor-visibility, destination/nested duplicates never")
    provenance = [{"surface": target["surface"], "host": target["host"],
                   **{key: target["manifest"][key] for key in
                      ("package_version", "source_lock_hash", "adapter_revision", "closure_hash")},
                   "manifest_hash": digest_record(target["manifest"])} for target in targets]
    if operation == "config-models" and (index["installs"][install_id]["provenance"] != provenance or
            any(entry["kind"] == "skill" and entry["action"] not in {"unchanged", "keep-edited"} for entry in entries)):
        raise ContractError("model configuration cannot update skill content or package provenance; run update first")
    if operation == "update" and any(entry["action"] in {"create", "replace"} for entry in entries):
        validate_candidate_evidence(candidate_evidence, provenance, entries)
    return {"schema_version": 1, "operation": operation, "install_id": install_id, "scope": scope, "kits": sorted(kits),
            "mode": mode, "profile": profile, "roots": sorted(roots),
            "surfaces": [t["surface"] for t in targets], "entries": entries,
            "conflicts": [e["physical_path"] for e in entries if e["action"] == "conflict"],
            "index_hash": digest_record(index), "provenance": provenance,
            "target_specs": [{key: target[key] for key in ("surface", "bundle", "root", "base", "home") if key in target}
                             for target in targets],
            "options": {"replace_skills": sorted(set(replace_skills)), "keep_edited": keep_edited,
                        "capabilities": deepcopy(capabilities or {}), "candidate_evidence": deepcopy(candidate_evidence),
                        "acknowledge_ancestor_visibility": bool(acknowledge_ancestor_visibility)},
            "acknowledged_visibility": acknowledged,
            "with_agents": with_agents, "native_resolutions": resolutions,
            "model_state": "policy-configured; native model/effort applied/effective unverified",
            "plugin_state": "not-installed/not-registered/not-enabled/not-trusted", "native_smoke": "not-run"}


def owned_entry_path(entry, roots):
    path = Path(entry["physical_path"])
    if not path.is_absolute() or canonical(path.parent) not in {canonical(root) for root in roots}:
        raise ContractError("owned destination escapes exact roots")
    if entry.get("kind", "skill") == "skill":
        expected = owned_target(path.parent, entry["skill"])
    elif entry["kind"] == "native-agent":
        if entry["file_name"] not in {entry["skill"] + ".md", entry["skill"] + ".toml"}:
            raise ContractError("invalid native agent filename")
        skill_id(entry["skill"])
        expected = no_links(path.parent / entry["file_name"])
    else:
        raise ContractError("unknown owned artifact kind")
    if expected != path:
        raise ContractError("owned artifact identity/path mismatch")
    return path


def refresh_targets(targets, scope):
    if scope not in {"project", "global"} or not targets:
        raise ContractError("invalid target scope")
    result = []
    for target in targets:
        surface = target["surface"]
        if surface not in SURFACE_HOST:
            raise ContractError("unknown target surface")
        bundle = no_links(target["bundle"])
        manifest = verify_bundle(bundle)
        adapter = load_json(contained(bundle, "adapter.json"))
        host = SURFACE_HOST[surface]
        if manifest["host"] != host or surface not in adapter["surfaces"]:
            raise ContractError("bundle does not match target surface")
        base = no_links(target["base"])
        root = contained(base, adapter["surfaces"][surface][scope])
        if canonical(root) != canonical(target["root"]):
            raise ContractError("target root differs from its adapter and scope")
        refreshed = {"surface": surface, "host": host, "bundle": str(bundle),
                     "manifest": manifest, "adapter": adapter, "root": str(root), "base": str(base)}
        if scope == "project" and target.get("home") and (scan_home := _scan_home(target["home"])):
            refreshed["home"] = scan_home
        result.append(refreshed)
    if len({target["surface"] for target in result}) != len(result):
        raise ContractError("duplicate target surface")
    return sorted(result, key=lambda target: target["surface"])


def validate_candidate_evidence(evidence, provenance, entries):
    if not isinstance(evidence, dict):
        raise ContractError("changed update requires candidate provenance and affected-check evidence")
    validate(evidence, load_json(Path(__file__).parents[1] / "installer/schemas/candidate-evidence.schema.json"))
    if evidence["evidence_class"] == "synthetic-fixture" or evidence["qualification"] != "accepted-for-scope":
        raise ContractError("update needs accepted checks for its explicit scope; fixture-only or pending evidence cannot promote it")
    if any(evidence["closure_hashes"].get(record["host"]) != record["closure_hash"] or
           evidence["source_lock_hashes"].get(record["host"]) != record["source_lock_hash"] for record in provenance):
        raise ContractError("candidate evidence belongs to a different source/artifact revision")
    affected = {entry["skill"] for entry in entries if entry["action"] in {"create", "replace"}}
    if not affected <= set(evidence["affected_skills"]):
        raise ContractError("candidate checks do not cover changed skills")
    receipts = []
    for check in evidence["checks"]:
        if not Path(check["receipt"]).is_absolute():
            raise ContractError("candidate check receipt must use an absolute reviewed path")
        path = no_links(check["receipt"])
        if not path.is_absolute() or digest_file(path) != check["receipt_sha256"]:
            raise ContractError("candidate check receipt is missing, changed or not an absolute reviewed path")
        receipt = load_json(path)
        validate(receipt, load_json(Path(__file__).parents[1] / "installer/schemas/check-receipt.schema.json"))
        if receipt["status"] != "pass" or receipt["closure_hashes"] != evidence["closure_hashes"] or receipt["source_lock_hashes"] != evidence["source_lock_hashes"]:
            raise ContractError("candidate check receipt does not cover this exact artifact/source revision")
        if not set(evidence["affected_skills"]) <= set(receipt["affected_skills"]):
            raise ContractError("candidate receipt omits affected identities")
        receipts.append(receipt)
    classes = {receipt["evidence_class"] for receipt in receipts}
    if evidence["evidence_class"] not in classes:
        raise ContractError("candidate evidence class has no matching typed receipt; cannot escalate static evidence")
    return {"status": "current", "evidence_classes": sorted(classes),
            "input_classes": sorted({receipt["input_class"] for receipt in receipts}),
            "scopes": sorted({receipt["scope"] for receipt in receipts}),
            "qualification": "accepted-for-stated-check-scope-only"}


def validate_plan_paths(plan):
    targets = refresh_targets(plan["target_specs"], plan["scope"])
    roots = {canonical(no_links(root)) for root in plan["roots"]}
    expected_roots = {canonical(target["root"]) for target in targets}
    if plan["with_agents"]:
        expected_roots.update(canonical(contained(target["base"], target["adapter"].get("agent_global_root", target["adapter"]["agent_root"])
                             if plan["scope"] == "global" else target["adapter"]["agent_root"])) for target in targets)
    if roots != expected_roots:
        raise ContractError("transaction roots differ from reviewed adapter targets")
    seen = set()
    for entry in plan["entries"]:
        target = owned_entry_path(entry, plan["roots"])
        if canonical(target) != entry["canonical_path"]:
            raise ContractError("transaction target identity/path mismatch")
        if entry["canonical_path"] in seen:
            raise ContractError("duplicate transaction target")
        seen.add(entry["canonical_path"])
        sources = {str(contained(spec["bundle"], "skills/" + entry["skill"] if entry["kind"] == "skill" else
                                "native/agents/" + agent_filename(spec["host"], entry["skill"]))) for spec in targets
                   if spec["surface"] in entry["visible_surfaces"]}
        if str(no_links(entry["source"])) not in sources:
            raise ContractError("transaction source escapes its verified bundle")
    if [{"surface": target["surface"], "host": target["host"],
         **{key: target["manifest"][key] for key in ("package_version", "source_lock_hash", "adapter_revision", "closure_hash")},
         "manifest_hash": digest_record(target["manifest"])} for target in targets] != plan["provenance"]:
        raise ContractError("candidate changed after transaction preview")
    return targets


def preflight_volumes(state_dir, roots):
    state_dir = no_links(state_dir)
    for root in roots:
        root = no_links(root)
        if state_dir.is_relative_to(root) or root.is_relative_to(state_dir):
            raise ContractError("transaction state and installed skill roots must be separate")
        if device_identity(root) != device_identity(state_dir):
            raise ContractError("state/staging and targets must share a device; choose a state directory on the target volume")


def process_alive(pid):
    if type(pid) is not int or pid <= 0:
        return None
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = kernel.OpenProcess(0x1000, False, pid)
        if not handle:
            return False if ctypes.get_last_error() == 87 else None
        try:
            code = wintypes.DWORD()
            return code.value == 259 if kernel.GetExitCodeProcess(handle, ctypes.byref(code)) else None
        finally:
            kernel.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return None


@contextmanager
def exclusive_lock(lock):
    lock = no_links(lock)
    lock.parent.mkdir(parents=True, exist_ok=True)
    nonce = uuid.uuid4().hex
    descriptor = os.open(lock, os.O_CREAT | os.O_RDWR, 0o600)
    acquired = False
    try:
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(descriptor, msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            acquired = True
        except OSError as error:
            raise ContractError("installer target is locked by a live operation; retry after it finishes") from error
        os.lseek(descriptor, 0, os.SEEK_SET)
        prior = os.read(descriptor, os.fstat(descriptor).st_size)
        if prior:
            try:
                old = json.loads(prior.decode("utf-8"))
            except (ValueError, UnicodeError) as error:
                if not prior.startswith(b'{"schema_version": 1, "lock_protocol": "kernel-advisory-v1"'):
                    raise ContractError("unrecognized lock metadata; preserve its owner and journal") from error
                old = {"lock_protocol": "kernel-advisory-v1"}
            if old.get("lock_protocol") != "kernel-advisory-v1" and process_alive(old.get("pid")) is not False:
                raise ContractError("legacy lock owner is live or unknown; preserve its lock and journal")
        owner = {"schema_version": 1, "lock_protocol": "kernel-advisory-v1", "pid": os.getpid(),
                 "nonce": nonce, "state": "active"}
        _write_lock(descriptor, owner)
        yield
    finally:
        if acquired:
            try:
                if "owner" in locals():
                    _write_lock(descriptor, {**owner, "state": "released"})
            finally:
                if os.name == "nt":
                    os.lseek(descriptor, 0, os.SEEK_SET)
                    msvcrt.locking(descriptor, msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(descriptor, fcntl.LOCK_UN)
                os.close(descriptor)
        else:
            os.close(descriptor)


def _write_lock(descriptor, owner):
    data = json.dumps(owner).encode("utf-8")
    os.lseek(descriptor, 0, os.SEEK_SET)
    os.write(descriptor, data)
    os.ftruncate(descriptor, len(data))
    os.fsync(descriptor)


@contextmanager
def target_lock(state_dir, roots=(), *, cleanup_empty_roots=False):
    with ExitStack() as stack:
        user_key = digest_record(canonical(Path.home()))[:16]
        shared_area = no_links(Path(tempfile.gettempdir()) / ("nckh-installer-locks-" + user_key))
        shared_area.mkdir(mode=0o777 if os.name == "nt" else 0o700, exist_ok=True)
        if os.name != "nt" and shared_area.stat().st_uid != os.getuid():
            raise ContractError("installer coordination directory belongs to another user")
        stack.enter_context(exclusive_lock(shared_area / "visibility.lock"))
        ordered = sorted({canonical(root): Path(root) for root in roots}.values(), key=str)
        lock_paths = sorted({canonical(root.parent / ".nckh-install.lock"): root.parent / ".nckh-install.lock"
                             for root in ordered}.values(), key=str)
        with ExitStack() as target_stack:
            for lock_path in lock_paths:
                target_stack.enter_context(exclusive_lock(lock_path))
            target_stack.enter_context(exclusive_lock(Path(state_dir) / "installer.lock"))
            yield
        # Root locks are closed; the shared visibility lock still serializes installers.
        if cleanup_empty_roots:
            for root in ordered:
                lock = root.parent / ".nckh-install.lock"
                if root.is_dir() and not any(root.iterdir()):
                    root.rmdir()
                if (not root.exists() and lock.is_file()
                        and set(root.parent.iterdir()) == {lock}):
                    metadata = load_json(lock)
                    if metadata.get("lock_protocol") == "kernel-advisory-v1" and metadata.get("state") == "released":
                        lock.unlink()


def recover_outstanding(state_dir, roots):
    path = Path(state_dir) / "journal.json"
    if path.exists():
        old = load_json(path)
        if old["status"] not in {"committed", "rolled-back"}:
            rollback(state_dir, old, allowed_roots=roots)
            raise ContractError("previous attempt rolled back; re-preview current inputs before retry")


def safe_remove_owned(path, roots):
    path = Path(path).absolute()
    no_links(path.parent)
    identity = path.stem if path.suffix in {".md", ".toml"} else path.name
    if canonical(path.parent) not in {canonical(root) for root in roots} or not skill_id(identity):
        raise ContractError("refusing deletion outside exact owned skill roots")
    if path.is_symlink():
        path.unlink()
    else:
        no_links(path)
        if path.is_file():
            path.unlink()
        else:
            shutil.rmtree(path)


def rollback(state_dir, journal, *, allowed_roots):
    state_dir = no_links(state_dir)
    if {canonical(root) for root in journal["roots"]} - {canonical(root) for root in allowed_roots}:
        raise ContractError("recovery roots are outside the current target grant")
    conflicts, prepared = [], []
    area = contained(state_dir, "transactions/" + journal["id"])
    preflight_volumes(state_dir, allowed_roots)
    seen = set()
    for change in journal["changes"]:
        target = Path(change["physical_path"])
        if not target.is_absolute() or canonical(target.parent) not in {canonical(root) for root in allowed_roots}:
            raise ContractError("journal target escapes recovery scope")
        identity = target.stem if target.suffix in {".md", ".toml"} else target.name
        skill_id(identity)
        no_links(target.parent)
        if canonical(target) in seen:
            raise ContractError("invalid or duplicate journal target")
        seen.add(canonical(target))
        if change["backup"]:
            backup = contained(state_dir, change["backup"])
            if backup.parent != area or not backup.name.startswith("backup-"):
                raise ContractError("journal backup escapes its owned transaction area")
    for change in reversed(journal["changes"]):
        target = Path(change["physical_path"])
        current = tree_hash(target)
        backup = contained(state_dir, change["backup"]) if change["backup"] else None
        if current == change["before_hash"]:
            continue
        if current not in {None, change["after_hash"]}:
            conflicts.append({"path": str(target), "reason": "later edit", "current_hash": current})
            continue
        if change["before_hash"] is not None and (backup is None or tree_hash(backup) != change["before_hash"]):
            conflicts.append({"path": str(target), "reason": "backup missing or changed", "current_hash": current})
            continue
        prepared.append((change, target, backup, current))
    for change, target, backup, current in prepared:
        if tree_hash(target) != current:
            conflicts.append({"path": str(target), "reason": "edit during recovery", "current_hash": tree_hash(target)})
            continue
        if current is not None:
            safe_remove_owned(target, allowed_roots)
        if change["before_hash"] is not None:
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(backup, target)
    journal["status"] = "rollback-conflict" if conflicts else "rolled-back"
    journal["recovery_conflicts"] = conflicts
    if journal.get("index_before") is not None:
        atomic_json(Path(state_dir) / "ownership.json", journal["index_before"])
    atomic_json(Path(state_dir) / "journal.json", journal)
    if conflicts:
        raise ContractError("rollback preserves unresolved targets; inspect journal conflicts: " +
                            ", ".join(conflict["path"] for conflict in conflicts))
    return journal


def commit_install(plan, state_dir, *, fail_after=None):
    targets = validate_plan_paths(plan)
    if plan["conflicts"]:
        raise ContractError("preview has conflicts; --yes cannot authorize overwrite")
    state_dir = no_links(state_dir)
    preflight_volumes(state_dir, plan["roots"])
    with target_lock(state_dir, plan["roots"]):
        recover_outstanding(state_dir, plan["roots"])
        index = read_index(state_dir)
        if digest_record(index) != plan["index_hash"]:
            raise ContractError("ownership changed after preview; re-preview before mutation")
        options = plan["options"]
        reviewed = plan_install(targets, index, kits=plan["kits"], mode=plan["mode"], profile=plan["profile"],
                                scope=plan["scope"], operation=plan["operation"], with_agents=plan["with_agents"], **options)
        if reviewed != plan:
            raise ContractError("transaction changed after preview; re-preview before mutation")
        expected_bytes = sum(len(e["content"].encode("utf-8")) if e["kind"] == "native-agent" else
                             sum(p.stat().st_size for p in Path(e["source"]).rglob("*") if p.is_file())
                             for e in plan["entries"] if e["action"] in {"create", "replace"})
        if shutil.disk_usage(state_dir).free < expected_bytes:
            raise ContractError("insufficient staging space")
        txn_id = uuid.uuid4().hex
        area = contained(state_dir, "transactions/" + txn_id)
        area.mkdir(parents=True)
        journal = {"schema_version": 1, "id": txn_id, "status": "staging", "roots": plan["roots"],
                   "operation": plan["operation"], "changes": [], "index_before": deepcopy(index)}
        atomic_json(state_dir / "journal.json", journal)
        for number, entry in enumerate(plan["entries"]):
            if tree_hash(entry["physical_path"]) != entry["before_hash"]:
                raise ContractError("target changed after preview; re-preview before mutation")
            if entry["action"] in {"unchanged", "keep-edited"}:
                continue
            stage = area / ("stage-" + str(number))
            if entry["kind"] == "native-agent":
                stage.write_text(entry["content"], encoding="utf-8", newline="\n")
            elif entry["mode"] == "copy":
                shutil.copytree(entry["source"], stage, copy_function=shutil.copy2)
            else:
                os.symlink(entry["source"], stage, target_is_directory=True)
            if tree_hash(stage) != entry["tree_hash"]:
                raise ContractError("staged content differs from pinned bundle")
        journal["status"] = "committing"
        atomic_json(state_dir / "journal.json", journal)
        try:
            for number, entry in enumerate(plan["entries"]):
                if entry["action"] in {"unchanged", "keep-edited"}:
                    continue
                target = Path(entry["physical_path"])
                if tree_hash(target) != entry["before_hash"]:
                    raise ContractError("target changed during commit; preserve concurrent edit")
                target.parent.mkdir(parents=True, exist_ok=True)
                backup_rel = f"transactions/{txn_id}/backup-{number}" if entry["before_hash"] is not None else None
                change = {"physical_path": str(target), "before_hash": entry["before_hash"],
                          "after_hash": entry["tree_hash"], "backup": backup_rel, "progress": "prepared"}
                journal["changes"].append(change)
                atomic_json(state_dir / "journal.json", journal)
                if backup_rel:
                    os.replace(target, contained(state_dir, backup_rel))
                os.replace(area / ("stage-" + str(number)), target)
                change["progress"] = "written"
                atomic_json(state_dir / "journal.json", journal)
                if fail_after == number + 1:
                    raise OSError("injected deterministic interruption")
            for entry in plan["entries"]:
                record = {key: value for key, value in entry.items() if key not in {"source", "content", "action", "before_hash"}}
                if entry["action"] == "keep-edited":
                    record["tree_hash"] = index["items"][entry["canonical_path"]]["tree_hash"]
                elif tree_hash(entry["physical_path"]) != entry["tree_hash"]:
                    raise ContractError("installed verification failed")
                index["items"][entry["canonical_path"]] = record
            retained_evidence = options["candidate_evidence"]
            if retained_evidence is None and plan["operation"] == "config-models":
                retained_evidence = index["installs"][plan["install_id"]].get("candidate_evidence")
            index["installs"][plan["install_id"]] = {"scope": plan["scope"], "surfaces": plan["surfaces"],
                                                        "kits": plan["kits"], "roots": plan["roots"], "mode": plan["mode"],
                                                        "operation": plan["operation"], "provenance": plan["provenance"],
                                                        "candidate_evidence": retained_evidence, "with_agents": plan["with_agents"],
                                                        "target_specs": deepcopy(plan["target_specs"]),
                                                        "acknowledged_visibility": deepcopy(plan["acknowledged_visibility"])}
            index["policies"][plan["install_id"]] = {"profile": plan["profile"], "state": "configured",
                                                         "applied": "unverified", "effective": "unknown",
                                                         "native_resolutions": plan["native_resolutions"]}
            atomic_json(state_dir / "ownership.json", index)
            journal["status"] = "committed"
            atomic_json(state_dir / "journal.json", journal)
        except (OSError, ContractError):
            rollback(state_dir, journal, allowed_roots=plan["roots"])
            raise
        return {"status": "native-configured" if plan["operation"] == "config-models" else "installed", "install_id": plan["install_id"], "changes": len(journal["changes"]),
                "native_smoke": "not-run", "model_effective": "unknown", "journal": str(state_dir / "journal.json")}


def _uninstall_actions(index, install_id):
    install = index["installs"].get(install_id)
    if install is None:
        raise ContractError("unknown install ID; refuse unowned deletion")
    actions = []
    for key, item in index["items"].items():
        if install_id not in item["owners"]:
            continue
        owned_entry_path(item, install["roots"])
        others = set(item["owners"]) - {install_id}
        current = tree_hash(item["physical_path"])
        action = "retain-shared" if others else "already-missing" if current is None else "remove" if current == item["tree_hash"] else "retain-edited"
        actions.append({"key": key, "path": item["physical_path"], "action": action})
    return install, actions


def uninstall(state_dir, install_id, *, dry_run=True, fail_after=None):
    state_dir = no_links(state_dir)
    index = read_index(state_dir)
    install, actions = _uninstall_actions(index, install_id)
    preflight_volumes(state_dir, install["roots"])
    if dry_run:
        return {"status": "preview", "actions": actions}
    with target_lock(state_dir, install["roots"], cleanup_empty_roots=True):
        recover_outstanding(state_dir, install["roots"])
        locked_roots = install["roots"]
        index = read_index(state_dir)
        install, actions = _uninstall_actions(index, install_id)
        if {canonical(root) for root in locked_roots} != {canonical(root) for root in install["roots"]}:
            raise ContractError("uninstall roots changed; re-preview before mutation")
        txn_id = uuid.uuid4().hex
        area = contained(state_dir, "transactions/" + txn_id)
        area.mkdir(parents=True)
        journal = {"schema_version": 1, "id": txn_id, "status": "committing", "roots": install["roots"],
                   "changes": [], "index_before": deepcopy(index), "operation": "uninstall"}
        atomic_json(Path(state_dir) / "journal.json", journal)
        try:
            for number, entry in enumerate(actions):
                item = index["items"][entry["key"]]
                if entry["action"] == "remove":
                    if tree_hash(entry["path"]) != item["tree_hash"]:
                        raise ContractError("uninstall target changed after preview")
                    backup_rel = f"transactions/{txn_id}/backup-{number}"
                    change = {"physical_path": entry["path"], "before_hash": item["tree_hash"],
                              "after_hash": None, "backup": backup_rel, "progress": "prepared"}
                    journal["changes"].append(change)
                    atomic_json(Path(state_dir) / "journal.json", journal)
                    os.replace(entry["path"], contained(state_dir, backup_rel))
                    change["progress"] = "written"
                    atomic_json(Path(state_dir) / "journal.json", journal)
                    del index["items"][entry["key"]]
                    if fail_after == number + 1:
                        raise OSError("injected deterministic uninstall interruption")
                elif entry["action"] == "already-missing":
                    del index["items"][entry["key"]]
                elif entry["action"] == "retain-shared":
                    item["owners"].remove(install_id)
            if not any(a["action"] == "retain-edited" for a in actions):
                index["installs"].pop(install_id)
                index["policies"].pop(install_id, None)
            atomic_json(Path(state_dir) / "ownership.json", index)
            journal["status"] = "committed"
            atomic_json(Path(state_dir) / "journal.json", journal)
        except (OSError, ContractError):
            rollback(state_dir, journal, allowed_roots=install["roots"])
            raise
    return {"status": "uninstalled-with-residue" if any(a["action"] == "retain-edited" for a in actions) else "uninstalled", "actions": actions}


def doctor(state_dir):
    index = read_index(state_dir)
    rows = []
    for item in index["items"].values():
        roots = [root for owner in item["owners"] for root in index["installs"][owner]["roots"]]
        path = owned_entry_path(item, roots)
        row = {"path": str(path), "owners": item["owners"], "visible_surfaces": item["visible_surfaces"]}
        row["status"] = "current" if tree_hash(path) == item["tree_hash"] else "edited/missing/stale"
        if not path.exists():
            row["closure_or_syntax"] = "missing"
        elif item.get("kind", "skill") == "skill":
            try:
                resolved = path.resolve() if path.is_symlink() else path
                closure(resolved, [contained(resolved, "SKILL.md")])
                row["closure_or_syntax"] = "self-contained"
            except (ContractError, OSError) as error:
                row.update(closure_or_syntax="invalid", error=str(error))
        elif path.suffix == ".toml":
            try:
                fields = tomllib.loads(path.read_text(encoding="utf-8"))
                row["closure_or_syntax"] = "valid-toml"
                row["configured_fields"] = {key: fields[key] for key in ["model", "model_reasoning_effort", "sandbox_mode"] if key in fields}
            except (ValueError, OSError) as error:
                row.update(closure_or_syntax="invalid", error=str(error))
        else:
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
                if not lines or lines[0] != "---":
                    raise ValueError("missing native frontmatter")
                end = lines.index("---", 1)
                fields = {}
                for line in lines[1:end]:
                    key, value = line.split(":", 1)
                    if key in fields:
                        raise ValueError("duplicate native frontmatter field")
                    fields[key] = json.loads(value)
                row["closure_or_syntax"] = "valid-generated-frontmatter"
                row["configured_fields"] = {key: fields[key] for key in ["model", "effort", "readonly", "commandExecutionPolicy"] if key in fields}
            except (ValueError, OSError) as error:
                row.update(closure_or_syntax="unverified-edited-format", error=str(error))
        rows.append(row)
    installs = []
    for identity, install in index["installs"].items():
        row = {"install_id": identity, "provenance": install.get("provenance", []),
               "acknowledged_visibility": install.get("acknowledged_visibility", []),
               "native_freshness": "unverified; pinned adapters are not live host evidence"}
        if install.get("candidate_evidence"):
            try:
                row["candidate_receipts"] = validate_candidate_evidence(install["candidate_evidence"], install["provenance"], [])
            except (ContractError, OSError, ValueError) as error:
                row["candidate_receipts"] = {"status": "invalid-or-stale", "error": str(error), "qualification": "unverified"}
        else:
            row["candidate_receipts"] = {"status": "not-provided", "qualification": "unverified"}
        if install.get("target_specs"):
            try:
                targets = refresh_targets(install["target_specs"], install["scope"])
                provenance = [{"surface": target["surface"], "host": target["host"],
                               **{key: target["manifest"][key] for key in ("package_version", "source_lock_hash", "adapter_revision", "closure_hash")},
                               "manifest_hash": digest_record(target["manifest"])} for target in targets]
                row["candidate_integrity"] = "current" if provenance == install["provenance"] else "changed"
                identities = {item["skill"] for item in index["items"].values() if identity in item["owners"] and item.get("kind", "skill") == "skill"}
                row["visibility_conflicts"] = visibility_conflicts(targets, identities, scope=install["scope"])
                if install.get("with_agents"):
                    for target in targets:
                        target["agent_destination"] = str(contained(target["base"], target["adapter"].get("agent_global_root", target["adapter"]["agent_root"])
                                                                  if install["scope"] == "global" else target["adapter"]["agent_root"]))
                    agents = {item["skill"] for item in index["items"].values() if identity in item["owners"] and item.get("kind") == "native-agent"}
                    row["visibility_conflicts"] += visibility_conflicts(targets, agents, scope=install["scope"], agents=True)
            except (ContractError, OSError, ValueError) as error:
                row.update(candidate_integrity="unavailable-or-invalid", error=str(error))
        else:
            row["candidate_integrity"] = "unverified; earlier ownership record has no source location"
        installs.append(row)
    journal_path = contained(state_dir, "journal.json")
    recovery = load_json(journal_path) if journal_path.exists() else None
    return {"status": "read-only", "items": rows, "installs": installs, "policies": index["policies"],
            "recovery": {"status": recovery["status"], "conflicts": recovery.get("recovery_conflicts", []),
                         "instruction": "re-run the operation to recover its journal; unresolved edits/backups require reconciliation"} if recovery else None,
            "native_smoke": "not-run", "native_model_effective": "unknown", "hook_enforcement": "unverified"}
