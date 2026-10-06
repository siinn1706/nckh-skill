import json
import os
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path

from core.build import build_host, hook_source_mapping, verify_bundle
from core.hook_config import payload_from_bundle, preview_config
from core.paths import atomic_json, digest_record, temporary_tree
from core.schema import ContractError
from tests.hooks.test_runner import payload


ROOT = Path(__file__).resolve().parents[2]


class HookClosureTests(unittest.TestCase):
    def invoke(self, script, args, project, stdin=None):
        environment = dict(os.environ, PYTHONPATH=str(ROOT))
        return subprocess.run([sys.executable, "-I", str(script), *args], input=stdin,
                              cwd=project, env=environment, capture_output=True, timeout=20)

    def context(self, project):
        atomic_json(project / "context.json", {"schema_version": 1, "task_id": "diagnostic",
            "tool_operations": {"Write": "write"}, "allowed_operations": ["write"], "brief": {"mode": "auto"}})

    def test_all_host_isolated_entrypoints_and_inactive_plugin_projection(self):
        for host in ("claude", "codex", "cursor", "agy"):
            with self.subTest(host=host), temporary_tree() as package, temporary_tree() as project:
                self.assertFalse(project.resolve().is_relative_to(ROOT))
                bundle = package / host
                manifest = build_host(ROOT, host, ["core"], bundle, include_plugin=True, include_resources=False)
                hook = manifest["hooks"]
                self.assertEqual(set(hook["members"]), set(hook_source_mapping(host)))
                self.assertFalse(hook["enabled"] or hook["registered"] or hook["trusted"])
                self.context(project)
                event_name = "preToolUse" if host == "cursor" else "PreToolUse"
                raw = json.dumps(payload(project, host=host)).encode()
                common = ["--host", host, "--event", event_name, "--project", str(project), "--context", "context.json"]
                for prefix in ("", hook["projection_root"] + "/"):
                    process = self.invoke(bundle / (prefix + hook["entrypoint"]), common, project, raw)
                    self.assertEqual(process.returncode, 0, process.stderr)
                    expected = {"decision": "ask"} if host == "agy" else {}
                    self.assertEqual(json.loads(process.stdout), expected)
                    config = self.invoke(bundle / (prefix + hook["config_entrypoint"]), ["preview", "--host", host,
                        "--package", str(bundle), "--project", str(project), "--context", "context.json"], project)
                    self.assertEqual(config.returncode, 0, config.stderr + config.stdout)
                    self.assertFalse(json.loads(config.stdout)["preview"]["enabled"])
                neutral = {"schema_version": 1, "phase": "preflight", "host": host, "tool": "Write", "paths": ["private/input.md"],
                    "session_key": digest_record("diagnostic"), "task_key": digest_record("diagnostic"),
                    "artifact_sha256": digest_record(None), "stop_active": False}
                manual = self.invoke(bundle / hook["manual_entrypoint"], ["--project", str(project), "--context", "context.json"],
                                     project, json.dumps(neutral).encode())
                self.assertEqual(manual.returncode, 3, manual.stderr)
                self.assertEqual(json.loads(manual.stdout)["decision"], "block")
                self.assertEqual({p.name for p in project.iterdir()}, {"context.json"})
                self.assertFalse((bundle / "plugin/hooks/hooks.json").exists())
                verify_bundle(bundle)

    def test_on_off_resources_keep_the_identical_pinned_hook_closure(self):
        with temporary_tree() as package:
            enabled = build_host(ROOT, "codex", ["core"], package / "on")
            disabled = build_host(ROOT, "codex", ["core"], package / "off", include_resources=False)
            self.assertEqual(enabled["source_lock_hash"], disabled["source_lock_hash"])
            for path in enabled["hooks"]["members"]:
                self.assertEqual((package / "on" / path).read_bytes(), (package / "off" / path).read_bytes())
            self.assertNotEqual(enabled["closure_hash"], disabled["closure_hash"])

    def test_missing_tampered_import_schema_and_extra_members_fail(self):
        with temporary_tree() as package, temporary_tree() as project:
            bundle = package / "codex"
            manifest = build_host(ROOT, "codex", ["core"], bundle, include_resources=False)
            self.context(project)
            for path in ("hooks/_shared/core/schema.py", "hooks/_shared/core/contracts/resource-provenance.schema.json",
                         "hooks/templates/codex.json"):
                original = (bundle / path).read_bytes()
                (bundle / path).unlink()
                with self.subTest(path=path), self.assertRaises(ContractError):
                    verify_bundle(bundle)
                if path.endswith("schema.py"):
                    failed = self.invoke(bundle / manifest["hooks"]["entrypoint"], ["--host", "codex", "--event", "PreToolUse",
                        "--project", str(project), "--context", "context.json"], project, json.dumps(payload(project)).encode())
                    self.assertNotEqual(failed.returncode, 0)
                (bundle / path).write_bytes(original + b"\n")
                with self.assertRaises(ContractError):
                    payload_from_bundle(bundle)
                (bundle / path).write_bytes(original)
            (bundle / "hooks/unowned.py").write_text("unexpected = True\n", encoding="utf8")
            with self.assertRaises(ContractError):
                verify_bundle(bundle)

    def test_rehashed_hook_omission_and_transformed_bytes_cannot_bypass_pins(self):
        with temporary_tree() as package:
            bundle = package / "codex"
            original = build_host(ROOT, "codex", ["core"], bundle, include_resources=False)
            for kind in ("omit-record", "omit-member", "enabled", "wrong-host"):
                record = deepcopy(original)
                if kind == "omit-record":
                    record.pop("hooks")
                elif kind == "omit-member":
                    record["hooks"]["members"].pop()
                elif kind == "enabled":
                    record["hooks"]["enabled"] = True
                else:
                    record["hooks"]["host"] = "agy"
                atomic_json(bundle / "manifest.json", record)
                with self.subTest(kind=kind), self.assertRaises(ContractError):
                    verify_bundle(bundle)
            record = deepcopy(original)
            path = "hooks/runner.py"
            (bundle / path).write_bytes(b"raise RuntimeError('modified hook')\n")
            from core.paths import digest_file
            next(row for row in record["files"] if row["path"] == path)["sha256"] = digest_file(bundle / path)
            record["closure_hash"] = digest_record(record["files"])
            atomic_json(bundle / "manifest.json", record)
            with self.assertRaises(ContractError):
                verify_bundle(bundle)

    def test_packaged_config_preview_binds_source_without_project_mutation(self):
        with temporary_tree() as package, temporary_tree() as project:
            bundle = package / "codex"
            build_host(ROOT, "codex", ["core"], bundle, include_resources=False)
            self.context(project)
            before = {p.relative_to(project).as_posix(): p.read_bytes() for p in project.rglob("*") if p.is_file()}
            preview = preview_config(project, "codex", payload_from_bundle(bundle), context_reference="context.json")
            self.assertFalse(preview["registered"] or preview["enabled"] or preview["trusted"])
            self.assertEqual(before, {p.relative_to(project).as_posix(): p.read_bytes() for p in project.rglob("*") if p.is_file()})
