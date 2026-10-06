"""Pinned, self-contained artifact closure; no installation or provider execution."""

import json
import os
import re
import time
from pathlib import Path

from core import VERSION
from core.native import ROLES, agent_filename, encode_agent
from core.paths import (atomic_json, contained, digest_bytes, digest_file,
                        digest_record, no_links, skill_id, temporary_tree, unique_paths)
from core.schema import ContractError, validate, validate_record
from core.resources import (REGISTRY_PATH, registry, resource_edges, resource_members,
                            resource_provenance, verify_provenance)


LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SOURCE_AREAS = ("skills", "core/contracts", "core/policies", "core/workflows",
                "core/profiles", "core/registry/catalog", "core/registry/compatibility",
                "agents", "adapters", "extensions", "installer", "scripts", "tests",
                "evals/cases", "evals/baselines", "evals/protocols", "evals/rubrics", "docs", "hooks")
SECRET = re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:sk-proj-|ghp_)[A-Za-z0-9_-]{24,}")

BASE_IDENTITIES = frozenset({
    "nckh-plan", "nckh-cook", "nckh-review", "nckh-handoff", "nckh-research",
    "nckh-evidence", "nckh-method", "nckh-write", "nckh-taste", "nckh-visuals",
    "nckh-scout", "nckh-debug", "nckh-fix", "nckh-test", "nckh-code-review",
    "nckh-security", "nckh-context", "nckh-docs", "nckh-frontend", "nckh-backend",
    "nckh-data", "nckh-devops", "nckh-git", "nckh-xia", "nckh-market-research",
    "nckh-brand", "nckh-marketing-plan", "nckh-campaign", "nckh-launch", "nckh-content",
    "nckh-copy", "nckh-seo", "nckh-email", "nckh-social", "nckh-analytics",
    "nckh-cro", "nckh-experiment",
})
APPROVED_IDENTITIES = BASE_IDENTITIES | {"nckh-humanwrite", "nckh-paperwrite"}

# Every local import and contract needed by the three isolated hook entrypoints.
HOOK_SHARED_SOURCES = (
    "core/__init__.py", "core/hook_policy.py", "core/hook_config.py", "core/guards.py",
    "core/paths.py", "core/schema.py", "core/build.py", "core/resources.py",
    "core/native.py", "core/models.py", "core/contracts/hook-event.schema.json",
    "core/contracts/hook-decision.schema.json", "core/contracts/brief.schema.json",
    "core/contracts/catalog.schema.json", "core/contracts/resource-registry.schema.json",
    "core/contracts/resource-provenance.schema.json", "installer/schemas/bundle.schema.json",
    "installer/schemas/bundle-v2.schema.json",
)


def hook_source_mapping(host):
    if host not in {"claude", "codex", "cursor", "agy"}:
        raise ContractError("unknown hook closure host")
    mapping = {"hooks/_shared/" + source: source for source in HOOK_SHARED_SOURCES}
    mapping.update({source: source for source in (
        "hooks/__init__.py", "hooks/runner.py", "hooks/codecs/__init__.py",
        f"hooks/codecs/{host}.py", f"hooks/templates/{host}.json")})
    if host in {"claude", "codex"}:
        mapping["hooks/codecs/common.py"] = "hooks/codecs/common.py"
    mapping.update({"hooks/hook-preflight.py": "scripts/hook-preflight.py",
                    "hooks/configure-hooks.py": "scripts/configure-hooks.py"})
    return mapping


def _materialize_hooks(root, output, host, lock, files, include_plugin):
    mapping = hook_source_mapping(host)
    for target, source in mapping.items():
        pin = lock["files"].get(source)
        if not pin or pin["rights"] != "owned-local-package":
            raise ContractError("hook closure has an unpinned or unresolved member")
        data = contained(root, source).read_bytes()
        if digest_bytes(data) != pin["sha256"] or SECRET.search(data):
            raise ContractError("hook closure source drift or secret")
        destination = contained(output, target)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        files.append({"path": target, "sha256": pin["sha256"], "source_path": source,
                      "source_sha256": pin["sha256"], "rights": "owned-local-package"})
    projection = "plugin/references/nckh-hooks" if include_plugin else "not-projected"
    if include_plugin:
        for record in list(files):
            if record["path"] not in mapping:
                continue
            target = projection + "/" + record["path"]
            destination = contained(output, target)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(contained(output, record["path"]).read_bytes())
            files.append({**record, "path": target})
    return {"host": host, "entrypoint": "hooks/runner.py", "manual_entrypoint": "hooks/hook-preflight.py",
            "config_entrypoint": "hooks/configure-hooks.py", "codec": f"hooks/codecs/{host}.py",
            "template": f"hooks/templates/{host}.json", "members": sorted(mapping),
            "projection_root": projection, "state": "packaged-inactive", "mode": "advisory",
            "enabled": False, "registered": False, "trusted": False, "native_qualification": "unverified"}


def _verify_hooks(manifest, lock, records):
    hook = manifest.get("hooks")
    has_source = any(source.startswith("hooks/") for source in lock["files"])
    if hook is None:
        if has_source:
            raise ContractError("candidate hook closure was omitted")
        return set()
    if manifest["schema_version"] != 2 or not has_source or hook["host"] != manifest["host"]:
        raise ContractError("hook closure host/version/source mismatch")
    mapping = hook_source_mapping(manifest["host"])
    if (len(hook["members"]) != len(mapping) or set(hook["members"]) != set(mapping)
            or hook["entrypoint"] != "hooks/runner.py" or hook["manual_entrypoint"] != "hooks/hook-preflight.py"
            or hook["config_entrypoint"] != "hooks/configure-hooks.py"
            or hook["codec"] != f"hooks/codecs/{manifest['host']}.py"
            or hook["template"] != f"hooks/templates/{manifest['host']}.json"):
        raise ContractError("hook closure requires the exact bounded host inventory")
    expected_projection = "plugin/references/nckh-hooks" if manifest["plugin"]["projected"] else "not-projected"
    if hook["projection_root"] != expected_projection:
        raise ContractError("hook inactive projection mismatch")
    file_map = {row["path"]: row for row in records}
    allowed = set()
    for target, source in mapping.items():
        for path in (target, expected_projection + "/" + target) if expected_projection != "not-projected" else (target,):
            row = file_map.get(path, {})
            if (row.get("source_path") != source or row.get("sha256") != lock["files"].get(source, {}).get("sha256")
                    or row.get("rights") != "owned-local-package"):
                raise ContractError("hook dependency missing, transformed or unpinned")
            allowed.add(path)
    return allowed


def validate_catalog(catalog):
    validate_record("catalog", catalog)
    entries = {row["id"]: row for row in catalog["skills"]}
    if len(catalog["skills"]) != 39 or set(entries) != APPROVED_IDENTITIES:
        raise ContractError("catalog requires the exact 37 baseline identities and two writers, without duplicates")
    return entries


def load_json(path):
    def reject_constant(value):
        raise ContractError(f"nonfinite JSON constant: {value}")

    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ContractError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(Path(path).read_text(encoding="utf-8"),
                      parse_constant=reject_constant, object_pairs_hook=unique_keys)


def source_members(root):
    root = no_links(root).resolve()
    declared = resource_members(root)
    files = []
    for area in SOURCE_AREAS:
        base = contained(root, area)
        for path in base.rglob("*"):
            no_links(path)
            if path.is_file() and path.relative_to(root).as_posix().startswith("core/profiles/resources/") and path.relative_to(root).as_posix() not in declared:
                raise ContractError("unregistered data/support file in resource namespace")
            if path.is_file() and path.suffix in {".md", ".json", ".yaml", ".toml", ".py", ".ps1", ".sh"}:
                files.append(path.relative_to(root).as_posix())
    files.extend(path.relative_to(root).as_posix() for path in contained(root, "core").glob("*.py"))
    files.append("evals/run-evals.py")
    files.extend(sorted(declared - set(files)))
    unique_paths(files)
    return sorted(files)


def freeze_sources(root, inspirations=None):
    root = no_links(root)
    lock_path = contained(root, "core/registry/source-lock/source-lock.json")
    previous = load_json(lock_path) if lock_path.exists() else None
    if inspirations is None:
        inspirations = previous.get("inspirations", []) if previous else []
    provenance = resource_provenance(root)
    files = {rel: {"sha256": digest_file(contained(root, rel)), "rights": "copied-upstream" if rel in provenance else "owned-local-package",
                   **({"provenance": provenance[rel]} if rel in provenance else {})}
             for rel in source_members(root)}
    if previous and previous["files"] == files and previous["inspirations"] == list(inspirations):
        return previous
    revision = str(int(previous["revision"]) + 1) if previous else "1"
    result = {"schema_version": 2 if provenance or previous and previous["schema_version"] == 2 else 1,
              "revision": revision, "release_rights": "local-package-only",
              "origin": "original NCKH instructions and code from owner-approved design",
              "copied_third_party_content": bool(provenance), "inspirations": list(inspirations),
              "files": files}
    if previous:
        previous_hash = digest_record(previous)
        archive = contained(root, f"core/registry/source-lock/history/{previous['revision']}-{previous_hash}.json")
        if archive.exists() and load_json(archive) != previous:
            raise ContractError("source lock history collision; preserve the previous pin")
        if not archive.exists():
            atomic_json(archive, previous)
        result["previous_lock_hash"] = previous_hash
    atomic_json(lock_path, result)
    return result


def verify_source_lock(root):
    lock = load_json(contained(root, "core/registry/source-lock/source-lock.json"))
    verify_lock_structure(root, lock)
    if set(lock["files"]) != set(source_members(root)):
        raise ContractError("source lock inventory changed; review and freeze the new revision")
    for rel, record in lock["files"].items():
        verify_provenance(root, rel, record, lock["files"], check_files=True)
        if digest_file(contained(root, rel)) != record["sha256"]:
            raise ContractError(f"source drift/rights unresolved: {rel}")
    if {rel: pin["provenance"] for rel, pin in lock["files"].items() if pin["rights"] == "copied-upstream"} != resource_provenance(root):
        raise ContractError("source registry provenance differs from the frozen rights contract")
    return lock


def verify_lock_structure(root, lock):
    required = {"schema_version", "revision", "release_rights", "origin", "copied_third_party_content", "inspirations", "files"}
    if (set(lock) - required - {"previous_lock_hash"} or not required <= lock.keys()
            or type(lock.get("schema_version")) is not int or lock["schema_version"] not in {1, 2}
            or lock.get("release_rights") != "local-package-only" or not isinstance(lock.get("files"), dict)
            or type(lock.get("copied_third_party_content")) is not bool or not isinstance(lock.get("origin"), str)
            or not isinstance(lock["revision"], str) or not lock["revision"].isdigit()
            or not isinstance(lock["inspirations"], list)):
        raise ContractError("unknown source lock, origin declaration or packaging rights")
    copied = any(r.get("rights") == "copied-upstream" for r in lock["files"].values() if isinstance(r, dict))
    if copied != lock["copied_third_party_content"] or lock["schema_version"] == 1 and copied:
        raise ContractError("source lock version/copied-content declaration mismatch")
    if "previous_lock_hash" in lock and not re.fullmatch(r"[a-f0-9]{64}", str(lock["previous_lock_hash"])):
        raise ContractError("invalid previous source lock hash")
    for relative, record in lock["files"].items():
        contained(root, relative)
        if not isinstance(record, dict) or not re.fullmatch(r"[a-f0-9]{64}", str(record.get("sha256"))):
            raise ContractError("invalid source pin/rights record")
        verify_provenance(root, relative, record, lock["files"])


def reference_path(root, current, href):
    href = href.strip("<>").split("#", 1)[0]
    if not href or re.match(r"^[a-z]+://", href):
        return None
    if "\\" in href or ":" in href or "?" in href:
        raise ContractError(f"invalid local reference: {href}")
    candidate = no_links(Path(current).parent / href).resolve()
    if not candidate.is_relative_to(root.resolve()) or not candidate.is_file():
        raise ContractError(f"missing or escaping reference: {current}: {href}")
    return candidate


def closure(root, initial, *, requires=None):
    root = Path(root).resolve()
    done, active = set(), set()

    def visit(path):
        path = no_links(path).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ContractError(f"missing/escaping closure member: {path}")
        if path in active:
            raise ContractError(f"dependency cycle: {path.relative_to(root)}")
        if path in done:
            return
        active.add(path)
        for relative in (requires or {}).get(path.relative_to(root).as_posix(), []):
            visit(contained(root, relative))
        if path.suffix == ".md":
            for href in LINK.findall(path.read_text(encoding="utf-8")):
                target = reference_path(root, path, href)
                if target:
                    visit(target)
        active.remove(path)
        done.add(path)

    for path in initial:
        visit(path)
    unique_paths(p.relative_to(root).as_posix() for p in done)
    return sorted(done)


def select_skills(catalog, kits):
    entries = validate_catalog(catalog)
    if not set(kits) <= {"core", "engineer", "marketing"} or not kits:
        raise ContractError("select Core, Engineer and/or Marketing")
    selected = {r["id"] for r in entries.values() if r["kit"] in kits or r["kit"] == "tooling" and "engineer" in kits}
    active, done = set(), set()

    def visit(skill):
        if skill in active:
            raise ContractError("catalog dependency cycle")
        if skill not in entries:
            raise ContractError(f"missing catalog dependency: {skill}")
        if skill in done:
            return
        active.add(skill)
        for dependency in entries[skill]["dependencies"]:
            visit(dependency)
        active.remove(skill)
        done.add(skill)

    for skill in selected:
        visit(skill)
    return [entries[skill] for skill in sorted(done)]


def build_host(root, host, kits, output, *, include_plugin=False, include_resources=True):
    root, output = no_links(root), no_links(output)
    if host not in {"claude", "codex", "cursor", "agy"}:
        raise ContractError("unknown build host")
    if output.exists() and any(output.iterdir()):
        raise ContractError("build destination must be empty; preserve prior candidates")
    lock = verify_source_lock(root)
    catalog = validate_record("catalog", load_json(contained(root, "core/registry/catalog/skills.json")))
    adapter = load_json(contained(root, f"adapters/{host}/adapter.json"))
    if output.resolve().is_relative_to(root.resolve()) and any(
            output.resolve().is_relative_to(contained(root, area).resolve()) for area in SOURCE_AREAS):
        raise ContractError("build output cannot replace source material")
    output.parent.mkdir(parents=True, exist_ok=True)
    with temporary_tree(output.parent) as staging:
        manifest = _materialize_host(root, host, kits, staging, lock, catalog, adapter, include_plugin, include_resources)
        verify_bundle(staging)
        if verify_source_lock(root) != lock:
            raise ContractError("source lock changed during build; preserve the previous candidate")
        no_links(output)
        if output.exists():
            output.rmdir()
        _promote_staging(staging, output)
    return manifest


def _promote_staging(staging, output):
    """Briefly retry Windows sharing conflicts for an owned, absent destination."""
    for attempt in range(6):
        staging, output = no_links(staging), no_links(output)
        if staging.parent != output.parent or not staging.is_dir() or output.exists():
            raise ContractError("staging/destination changed before promotion; preserve both")
        try:
            os.replace(staging, output)
            return
        except PermissionError as error:
            if os.name != "nt" or getattr(error, "winerror", None) not in {5, 32, 33} or attempt == 5:
                raise
            time.sleep(0.05 * (2 ** attempt))


def _materialize_host(root, host, kits, output, lock, catalog, adapter, include_plugin, include_resources=True):
    files, skills, packaged_resources = [], [], []
    resource_catalog = registry(root)["resources"]
    for entry in select_skills(catalog, kits):
        source_dir = contained(root, entry["path"])
        initial = [p for p in source_dir.rglob("*") if p.is_file()]
        declared_resources = [r for r in resource_catalog if entry["id"] in r["consumers"] and r["dependency"] == "required"]
        selected_resources = declared_resources if include_resources else []
        for resource in declared_resources:
            initial.extend(contained(root, relative) for relative in [resource["reader"], REGISTRY_PATH])
        initial.extend(contained(root, r["path"]) for r in selected_resources)
        members = closure(root, initial, requires=resource_edges(root, entry["id"]))
        mapping = {p: Path("skills") / entry["id"] / (p.relative_to(source_dir) if p.is_relative_to(source_dir)
                   else Path("references/_shared") / p.relative_to(root)) for p in members}
        unique_paths(mapping.values())
        skill_files = []
        for source in members:
            relative = source.relative_to(root).as_posix()
            if relative.startswith("evals/") or "/private/" in relative:
                raise ContractError("evaluation/private content cannot enter skill closure")
            if relative not in lock["files"]:
                raise ContractError(f"unlicensed/unpinned closure member: {relative}")
            data = source.read_bytes()
            if digest_bytes(data) != lock["files"][relative]["sha256"]:
                raise ContractError(f"source changed during materialization: {relative}")
            if SECRET.search(data):
                raise ContractError(f"private/secret content in closure: {relative}")
            if source.suffix == ".md":
                def rewrite(match):
                    href = match.group(1)
                    target = reference_path(root, source, href)
                    if not target:
                        return match.group(0)
                    target_relative = os.path.relpath(mapping[target], mapping[source].parent).replace(os.sep, "/")
                    fragment = "#" + href.split("#", 1)[1] if "#" in href else ""
                    return match.group(0).replace("(" + href + ")", "(" + target_relative + fragment + ")")
                data = LINK.sub(rewrite, data.decode("utf-8")).encode("utf-8")
            destination = contained(output, mapping[source].as_posix())
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            record = {"path": mapping[source].as_posix(), "sha256": digest_bytes(data),
                      "source_path": relative, "source_sha256": lock["files"][relative]["sha256"],
                      "rights": lock["files"][relative]["rights"],
                      **({"provenance": lock["files"][relative]["provenance"]} if "provenance" in lock["files"][relative] else {})}
            files.append(record)
            skill_files.append({"path": str(mapping[source].relative_to(Path("skills") / entry["id"])).replace("\\", "/"), "sha256": record["sha256"]})
        skills.append({"id": entry["id"], "kit": entry["kit"], "status": "experimental",
                       "tree_hash": digest_record(sorted(skill_files, key=lambda r: r["path"]))})
        for resource in selected_resources:
            packaged_resources.append({"resource_id": resource["resource_id"], "consumer": entry["id"],
                                       "path": mapping[contained(root, resource["path"])].as_posix(),
                                       "reader": mapping[contained(root, resource["reader"])].as_posix(),
                                       "requires": [mapping[contained(root, rel)].as_posix() for rel in resource["requires"]],
                                       "format": resource["format"], "source_sha256": resource["source"]["sha256"],
                                       "expected_artifact": resource["expected_artifact"]})
    lock_target = output / "source-lock.json"
    atomic_json(lock_target, lock)
    files.append({"path": "source-lock.json", "sha256": digest_file(lock_target),
                  "source_path": "core/registry/source-lock/source-lock.json",
                  "source_sha256": digest_file(contained(root, "core/registry/source-lock/source-lock.json")), "rights": "owned-local-package"})
    adapter_target = output / "adapter.json"
    atomic_json(adapter_target, adapter)
    files.append({"path": "adapter.json", "sha256": digest_file(adapter_target),
                  "source_path": f"adapters/{host}/adapter.json",
                  "source_sha256": lock["files"][f"adapters/{host}/adapter.json"]["sha256"], "rights": "owned-local-package"})
    agents = []
    for role, (tier, read_only) in ROLES.items():
        role_source = contained(root, f"agents/{role}.md")
        dependencies = closure(root, [role_source])
        sections = [role_source, *(path for path in dependencies if path != role_source)]
        instructions = "\n\n".join(LINK.sub(lambda match: match.group(0).split("](", 1)[0] + "]", path.read_text(encoding="utf-8"))
                                  for path in sections)
        description = role_source.read_text(encoding="utf-8").split("\n\n", 2)[1].replace("\n", " ").strip()
        identity = "nckh-" + role
        encoded = encode_agent(host, identity, description, instructions, read_only=read_only)
        paths = {"instructions_path": f"native/roles/{identity}.md", "path": "native/agents/" + agent_filename(host, identity)}
        for path, data in [(paths["instructions_path"], instructions.encode("utf-8")), (paths["path"], encoded.encode("utf-8"))]:
            destination = contained(output, path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            for dependency in dependencies:
                if dependency.relative_to(root).as_posix() not in lock["files"]:
                    raise ContractError("unpinned native agent dependency")
            files.append({"path": path, "sha256": digest_bytes(data), "source_path": f"agents/{role}.md",
                          "source_sha256": lock["files"][f"agents/{role}.md"]["sha256"], "rights": "owned-local-package"})
        agents.append({"id": identity, "role": role, "tier": tier, "read_only": read_only,
                       "description": description, **paths, "sha256": digest_bytes(encoded.encode("utf-8"))})
    plugin = {"projected": False, "manifest_path": "not-projected", "agents_projected": False,
              "copied": False, "registered": False, "enabled": False, "trusted": False,
              "session_only": False, "tested": False, "native_qualification": "unverified"}
    if include_plugin:
        manifest_rel = {"claude": "plugin/.claude-plugin/plugin.json", "cursor": "plugin/.cursor-plugin/plugin.json",
                        "codex": "plugin/plugin.json", "agy": "plugin/plugin.json"}[host]
        plugin_value = {"name": "nckh-kit", "version": VERSION, "description": "Experimental research, engineering and marketing instructions."}
        if host == "codex":
            plugin_value["$schema"] = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
        elif host == "agy":
            plugin_value = {"name": "nckh-kit", "description": plugin_value["description"],
                            "$schema": "https://antigravity.google/schemas/v1/plugin.json"}
        path = contained(output, manifest_rel)
        atomic_json(path, plugin_value)
        files.append({"path": manifest_rel, "sha256": digest_file(path), "source_path": f"adapters/{host}/adapter.json",
                      "source_sha256": lock["files"][f"adapters/{host}/adapter.json"]["sha256"], "rights": "owned-local-package"})
        for record in list(files):
            if not record["path"].startswith("skills/") and not (host != "codex" and record["path"].startswith("native/agents/")):
                continue
            projected = "plugin/" + record["path"].removeprefix("native/")
            destination = contained(output, projected)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(contained(output, record["path"]).read_bytes())
            files.append({**record, "path": projected})
        plugin.update(projected=True, manifest_path=manifest_rel, agents_projected=host != "codex")
    hooks = _materialize_hooks(root, output, host, lock, files, include_plugin)
    files.sort(key=lambda record: record["path"])
    unique_paths(record["path"] for record in files)
    manifest = {"schema_version": 2 if lock["schema_version"] == 2 else 1, "package_version": VERSION, "host": host,
                "adapter_revision": adapter["revision"], "source_lock_hash": digest_record(lock),
                "closure_hash": digest_record(files), "representation": "shared-neutral",
                "release_rights": "local-package-only", "kits": sorted(kits),
                "skills": skills, "agents": agents, "plugin": plugin, "files": files, "native_qualification": "unverified"}
    if manifest["schema_version"] == 2:
        manifest["resources"] = packaged_resources
        manifest["resource_access"] = "on" if include_resources else "off"
        manifest["hooks"] = hooks
    atomic_json(output / "manifest.json", manifest)
    return manifest


def verify_bundle(bundle):
    bundle = no_links(bundle)
    manifest = load_json(contained(bundle, "manifest.json"))
    version = manifest.get("schema_version")
    if type(version) is not int or version not in {1, 2}:
        raise ContractError("unsupported bundle version")
    schema_path = "bundle.schema.json" if version == 1 else "bundle-v2.schema.json"
    validate(manifest, load_json(Path(__file__).parents[1] / "installer/schemas" / schema_path))
    lock = load_json(contained(bundle, "source-lock.json"))
    verify_lock_structure(bundle, lock)
    if version != lock["schema_version"]:
        raise ContractError("bundle/source lock format version mismatch")
    if digest_record(lock) != manifest["source_lock_hash"] or lock.get("release_rights") != "local-package-only":
        raise ContractError("artifact source lock hash/rights mismatch")
    records = manifest["files"]
    identities = [skill_id(record["id"]) for record in manifest["skills"]]
    unique_paths(identities)
    unique_paths(r["path"] for r in records)
    if manifest["closure_hash"] != digest_record(records):
        raise ContractError("artifact manifest hash mismatch")
    actual = set()
    for path in bundle.rglob("*"):
        no_links(path)
        if path.is_file():
            actual.add(path.relative_to(bundle).as_posix())
    expected = {r["path"] for r in records} | {"manifest.json"}
    if actual != expected:
        raise ContractError("artifact has missing or unowned files")
    for record in records:
        path = contained(bundle, record["path"])
        if record["path"] == "source-lock.json":
            if record["source_path"] != "core/registry/source-lock/source-lock.json" or record["source_sha256"] != record["sha256"]:
                raise ContractError("embedded source lock provenance mismatch")
        elif lock["files"].get(record["source_path"], {}).get("sha256") != record["source_sha256"] or lock["files"][record["source_path"]].get("rights") != record["rights"]:
            raise ContractError("artifact source file differs from its embedded pin")
        if record["rights"] == "copied-upstream":
            if record.get("provenance") != lock["files"][record["source_path"]].get("provenance") or record["sha256"] != record["source_sha256"]:
                raise ContractError("copied content provenance/bytes differ from the original pin")
            for path_key, hash_key in [("license_path", "license_sha256"), ("notice_path", "notice_sha256")]:
                provenance = record["provenance"]
                if provenance[path_key] and not any(r["source_path"] == provenance[path_key] and r["source_sha256"] == provenance[hash_key]
                                                   and r["path"].split("/")[:2] == record["path"].split("/")[:2] for r in records):
                    raise ContractError("copied content has no packaged license/attribution for this consumer")
        elif "provenance" in record:
            raise ContractError("owned artifact cannot relabel copied bytes")
        if digest_file(path) != record["sha256"]:
            raise ContractError(f"artifact hash/rights mismatch: {record['path']}")
        if path.suffix == ".md":
            for href in LINK.findall(path.read_text(encoding="utf-8")):
                reference_path(bundle, path, href)
    native_paths = set()
    agent_ids = []
    hashes = {record["path"]: record["sha256"] for record in records}
    hook_paths = _verify_hooks(manifest, lock, records)
    for agent in manifest["agents"]:
        identity = skill_id(agent["id"])
        agent_ids.append(identity)
        if agent["role"] not in ROLES or identity != "nckh-" + agent["role"]:
            raise ContractError("unknown native agent role")
        if agent["path"] != "native/agents/" + agent_filename(manifest["host"], identity) or agent["instructions_path"] != f"native/roles/{identity}.md":
            raise ContractError("native agent path/identity mismatch")
        if hashes.get(agent["path"]) != agent["sha256"] or agent["instructions_path"] not in hashes:
            raise ContractError("native agent file is missing or unregistered")
        instructions = contained(bundle, agent["instructions_path"]).read_text(encoding="utf-8")
        tier, read_only = ROLES[agent["role"]]
        if agent["tier"] != tier or agent["read_only"] != read_only or digest_bytes(
                encode_agent(manifest["host"], identity, agent["description"], instructions, read_only=read_only).encode("utf-8")) != agent["sha256"]:
            raise ContractError("native agent encoding differs from the registered role")
        native_paths.update([agent["path"], agent["instructions_path"]])
    unique_paths(agent_ids)
    if {agent["role"] for agent in manifest["agents"]} != set(ROLES):
        raise ContractError("native agent role inventory incomplete")
    plugin = manifest["plugin"]
    plugin_paths = set()
    if any(plugin[key] for key in ("copied", "registered", "enabled", "trusted", "session_only", "tested")):
        raise ContractError("build cannot claim runtime plugin state")
    if plugin["projected"]:
        manifest_rel = {"claude": "plugin/.claude-plugin/plugin.json", "cursor": "plugin/.cursor-plugin/plugin.json",
                        "codex": "plugin/plugin.json", "agy": "plugin/plugin.json"}[manifest["host"]]
        if plugin["manifest_path"] != manifest_rel or plugin["agents_projected"] != (manifest["host"] != "codex"):
            raise ContractError("plugin projection does not match its host")
        descriptor = load_json(contained(bundle, manifest_rel))
        if descriptor.get("name") != "nckh-kit" or set(descriptor) - {"name", "version", "description", "$schema"}:
            raise ContractError("unexpected plugin manifest components")
        plugin_paths.add(manifest_rel)
        for record in records:
            if record["path"].startswith("skills/") or plugin["agents_projected"] and record["path"].startswith("native/agents/"):
                projected = "plugin/" + record["path"].removeprefix("native/")
                if hashes.get(projected) != record["sha256"]:
                    raise ContractError("plugin differs from the same frozen standalone components")
                plugin_paths.add(projected)
    elif plugin["manifest_path"] != "not-projected" or plugin["agents_projected"]:
        raise ContractError("invalid inactive plugin projection")
    groups = {identity: [] for identity in identities}
    for record in records:
        parts = record["path"].split("/")
        if record["path"] in {"adapter.json", "source-lock.json"} or record["path"] in native_paths or record["path"] in plugin_paths or record["path"] in hook_paths:
            continue
        if len(parts) < 3 or parts[0] != "skills" or parts[1] not in groups:
            raise ContractError("artifact contains an unregistered skill file")
        groups[parts[1]].append({"path": "/".join(parts[2:]), "sha256": record["sha256"]})
    for skill in manifest["skills"]:
        members = groups[skill["id"]]
        if not any(member["path"] == "SKILL.md" for member in members):
            raise ContractError("registered skill has no SKILL.md")
        if digest_record(sorted(members, key=lambda member: member["path"])) != skill["tree_hash"]:
            raise ContractError("registered skill tree hash does not match artifact files")
    if version == 2:
        if manifest["resource_access"] == "off" and manifest["resources"]:
            raise ContractError("resource-off bundle cannot declare enabled resources")
        bindings = set()
        file_map = {r["path"]: r for r in records}
        for resource in manifest["resources"]:
            key = (resource["resource_id"], resource["consumer"])
            if key in bindings or resource["consumer"] not in groups:
                raise ContractError("duplicate or unknown resource consumer binding")
            bindings.add(key)
            for path in [resource["path"], resource["reader"], *resource["requires"]]:
                if path not in file_map or not path.startswith("skills/" + resource["consumer"] + "/"):
                    raise ContractError("resource binding is missing its self-contained dependency")
            config_path = next((p for p in resource["requires"] if file_map[p]["source_path"] == REGISTRY_PATH), None)
            if not config_path:
                raise ContractError("resource binding has no pinned registry")
            declared = load_json(contained(bundle, config_path))["resources"]
            match = [r for r in declared if r["resource_id"] == resource["resource_id"]]
            if len(match) != 1:
                raise ContractError("resource binding differs from the declared registry")
            row = match[0]
            if (resource["consumer"] not in row["consumers"] or row["dependency"] != "required"
                    or resource["source_sha256"] != row["source"]["sha256"]
                    or file_map[resource["path"]]["rights"] != "copied-upstream"
                    or file_map[resource["path"]].get("provenance", {}).get("source_kind") != row["source_kind"]
                    or resource["format"] != row["format"]
                    or resource["expected_artifact"] != row["expected_artifact"]
                    or file_map[resource["path"]]["source_path"] != row["path"]
                    or file_map[resource["reader"]]["source_path"] != row["reader"]
                    or {file_map[p]["source_path"] for p in resource["requires"]} != set(row["requires"])):
                raise ContractError("resource path/reader/rights/consumer binding mismatch")
        declared_bindings = set()
        for record in records:
            if record["path"].startswith("skills/") and record["source_path"] == REGISTRY_PATH:
                identity = record["path"].split("/")[1]
                for row in load_json(contained(bundle, record["path"]))["resources"]:
                    if identity in row["consumers"] and row["dependency"] == "required":
                        declared_bindings.add((row["resource_id"], identity))
        if manifest["resource_access"] == "on" and bindings != declared_bindings:
            raise ContractError("required resource consumer binding was omitted")
        if manifest["resource_access"] == "off" and any(r["rights"] == "copied-upstream" for r in records):
            raise ContractError("resource-off bundle includes copied resource content")
    adapter = load_json(contained(bundle, "adapter.json"))
    if adapter.get("id") != manifest["host"] or adapter.get("revision") != manifest["adapter_revision"]:
        raise ContractError("adapter identity/revision differs from artifact manifest")
    return manifest
