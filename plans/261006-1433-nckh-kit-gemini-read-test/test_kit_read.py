"""Read every nckh skill link, hook entrypoint, and catalog resource."""

import ast
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


KIT = Path(__file__).resolve().parents[2] / "nckh-kit"
WORKSPACE = KIT.parent
INSTALLED = WORKSPACE / ".agents" / "skills"
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
RESOURCE_ID = re.compile(r"`(R-[a-z0-9-]+)`")
NATIVE_HOOKS = (
    WORKSPACE / ".cursor" / "hooks.json",
    WORKSPACE / ".agents" / "hooks.json",
    WORKSPACE / ".codex" / "hooks.json",
    WORKSPACE / ".claude" / "settings.local.json",
)
PROBE = r"""
import importlib.util, json, os, sys
from pathlib import Path
out = []
for item in json.loads(os.environ["NCKH_PROBE_ROOTS"]):
    shared = Path(item)
    script = shared / "scripts" / "search-resource.py"
    catalog_path = shared / "core" / "registry" / "catalog" / "resources.json"
    if not script.is_file() or not catalog_path.is_file():
        out.append({"root": item, "error": "reader or catalog missing"})
        continue
    for name in list(sys.modules):
        if name == "core" or name.startswith("core.") or name == "nckh_probe_reader":
            del sys.modules[name]
    sys.path.insert(0, str(shared))
    try:
        spec = importlib.util.spec_from_file_location("nckh_probe_reader", script)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except Exception as exc:
        out.append({"root": item, "error": "catalog/reader load: " + str(exc)})
        continue
    for resource in catalog["resources"]:
        rels = [resource["path"], *resource.get("requires", [])]
        missing = [rel for rel in rels if not (shared / rel).is_file()]
        if missing:
            out.append({"root": item, "id": resource["resource_id"], "error": "missing file", "paths": missing})
            continue
        try:
            mod._verify_source(resource, shared)
        except Exception as exc:
            out.append({"root": item, "id": resource["resource_id"], "error": str(exc)})
json.dump(out, sys.stdout)
"""


def _text(path):
    return path.read_text(encoding="utf-8")


def _links(path):
    broken = []
    try:
        text = _text(path)
    except (OSError, UnicodeError) as exc:
        return [f"{path}: {exc}"]
    for match in LINK.finditer(text):
        raw = match.group(1).strip()
        if raw.startswith("<") and raw.endswith(">"):
            raw = raw[1:-1].strip()
        raw = raw.split()[0]
        if raw.startswith(("#", "http://", "https://", "mailto:")):
            continue
        relative = raw.split("#", 1)[0].split("?", 1)[0]
        if not relative:
            continue
        target = (path.parent / relative).resolve()
        if not target.is_file():
            broken.append(f"{path} -> {raw}")
    return broken


def _skill_dirs(root):
    return sorted(path.parent for path in root.glob("nckh-*/SKILL.md"))


def _payload(project, host):
    if host == "cursor":
        return {"hook_event_name": "preToolUse", "conversation_id": "fixture",
                "workspace_roots": [str(project)], "tool_name": "Write",
                "tool_input": {"file_path": "draft.md"}, "loop_count": 0}
    if host == "agy":
        return {"conversationId": "fixture", "workspacePaths": [str(project)],
                "toolCall": {"name": "Write", "args": {"path": "draft.md"}}, "executionNum": 1}
    return {"hook_event_name": "PreToolUse", "session_id": "fixture", "cwd": str(project),
            "model": "unverified", "turn_id": "fixture-turn", "tool_name": "Write",
            "tool_input": {"file_path": "draft.md"}, "stop_hook_active": False}


class KitReadTests(unittest.TestCase):
    def test_source_and_installed_skill_links_resolve(self):
        roots = [KIT / "skills", INSTALLED]
        broken = []
        seen = 0
        for root in roots:
            files = list(root.glob("nckh-*/SKILL.md")) if root == INSTALLED else list(root.glob("*/*/SKILL.md"))
            self.assertTrue(files, root)
            for skill in files:
                seen += 1
                text = _text(skill)
                self.assertTrue(text.startswith("---\n"), skill)
                self.assertIn(f"name: {skill.parent.name}", text.split("---", 2)[1])
                broken.extend(_links(skill))
                for extra in skill.parent.rglob("*.md"):
                    if extra != skill:
                        broken.extend(_links(extra))
        self.assertGreaterEqual(seen, 43)
        self.assertEqual(broken, [])

    def test_catalog_skills_exist_in_source_and_cursor_projection(self):
        catalog = json.loads(_text(KIT / "core/registry/catalog/skills.json"))
        missing = []
        for row in catalog["skills"]:
            source = KIT / row["path"] / "SKILL.md"
            if not source.is_file():
                missing.append("source " + row["id"])
            if not (INSTALLED / row["id"] / "SKILL.md").is_file():
                missing.append("installed " + row["id"])
        self.assertEqual(missing, [])

    def test_declared_resources_read(self):
        roots = [str(KIT)]
        for skill in _skill_dirs(INSTALLED):
            shared = skill / "references" / "_shared"
            if (shared / "core/registry/catalog/resources.json").is_file():
                roots.append(str(shared))
        self.assertGreaterEqual(len(roots), 2)
        env = os.environ.copy()
        env["NCKH_PROBE_ROOTS"] = json.dumps(roots)
        proc = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env)
        self.assertEqual(proc.returncode, 0, proc.stderr[-2000:])
        failures = json.loads(proc.stdout)
        self.assertEqual(failures, [])

    def test_resource_lookup_ids_exist_in_nearest_catalog(self):
        missing = []
        source_ids = {row["resource_id"] for row in json.loads(_text(KIT / "core/registry/catalog/resources.json"))["resources"]}
        for path in (KIT / "skills").glob("*/*/references/resource-lookup.md"):
            for identity in RESOURCE_ID.findall(_text(path)):
                if identity not in source_ids:
                    missing.append(f"{path} {identity}")
        for path in INSTALLED.glob("nckh-*/references/resource-lookup.md"):
            catalog_path = path.parents[1] / "references" / "_shared" / "core/registry/catalog/resources.json"
            if not catalog_path.is_file():
                missing.append(f"{path} catalog missing")
                continue
            ids = {row["resource_id"] for row in json.loads(_text(catalog_path))["resources"]}
            for identity in RESOURCE_ID.findall(_text(path)):
                if identity not in ids:
                    missing.append(f"{path.name} in {path.parents[1].name} {identity}")
        self.assertEqual(missing, [])

    def test_hook_sources_parse_and_runner_reads_valid_context(self):
        parsed = []
        for path in list((KIT / "hooks").rglob("*.py")) + [
            KIT / "scripts/hook-preflight.py", KIT / "scripts/configure-hooks.py"
        ]:
            ast.parse(_text(path), filename=str(path))
            parsed.append(path.name)
        for path in (KIT / "hooks/templates").glob("*.json"):
            json.loads(_text(path))
            parsed.append(path.name)
        self.assertIn("runner.py", parsed)
        self.assertIn("agy.json", parsed)
        absent = [str(path.relative_to(WORKSPACE)) for path in NATIVE_HOOKS if not path.is_file()]
        for path in NATIVE_HOOKS:
            if path.is_file():
                json.loads(_text(path))
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "context.json").write_text(json.dumps({
                "schema_version": 1, "task_id": "fixture",
                "tool_operations": {"Write": "write"}, "allowed_operations": ["write"],
                "brief": {"mode": "auto"}}), encoding="utf-8")
            for host, event in (("cursor", "preToolUse"), ("agy", "PreToolUse"),
                                ("claude", "PreToolUse"), ("codex", "PreToolUse")):
                with self.subTest(host=host):
                    proc = subprocess.run(
                        [sys.executable, str(KIT / "hooks/runner.py"), "--host", host, "--event", event,
                         "--project", str(project), "--context", "context.json", "--mode", "enforce"],
                        input=json.dumps(_payload(project, host)).encode(), capture_output=True, cwd=KIT)
                    self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace")[-1500:])
                    self.assertTrue(proc.stdout.strip().startswith(b"{") or proc.stdout.strip() == b"{}")
        self.assertEqual(absent, [str(path.relative_to(WORKSPACE)) for path in NATIVE_HOOKS])

    def test_default_discover_can_import_hook_runner(self):
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_runner.py", "-q"],
            cwd=KIT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, (proc.stderr or proc.stdout)[-2000:])
