from tests._lab import lab_root
import json
import os
import subprocess
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from pathlib import Path

from core.build import build_host, hook_source_mapping, verify_bundle
from core.hook_config import payload_from_bundle, preview_config
from core.paths import atomic_json, digest_record, temporary_tree
from core.schema import ContractError
from tests._bundles import copy_bundle
from tests.hooks.test_nudges import fix_cue
from tests.hooks.test_runner import payload


ROOT = Path(__file__).resolve().parents[2]
# Prompt event, expected invocation and project skill root for hosts with a prompt hook.
PROMPT_EVENTS = {"claude": ("UserPromptSubmit", "/nckh-fix", ".claude/skills"),
                 "codex": ("UserPromptSubmit", "$nckh-fix", ".agents/skills"),
                 "cursor": ("beforeSubmitPrompt", "/nckh-fix", ".cursor/skills")}


class HookClosureTests(unittest.TestCase):
    def invoke(self, script, args, project, stdin=None):
        environment = dict(os.environ, PYTHONPATH=str(ROOT))
        return subprocess.run([sys.executable, "-I", str(script), *args], input=stdin,
                              cwd=project, env=environment, capture_output=True, timeout=20)

    def context(self, project):
        atomic_json(project / "context.json", {"schema_version": 1, "task_id": "diagnostic",
            "tool_operations": {"Write": "write"}, "allowed_operations": ["write"], "brief": {"mode": "auto"}})

    def test_all_host_isolated_entrypoints_and_inactive_plugin_projection(self):
        hosts = ("claude", "codex", "cursor", "agy")
        with temporary_tree(lab_root()) as packages, ThreadPoolExecutor(len(hosts)) as executor:
            # The four independent bundles build concurrently; each host is still checked in its own subtest.
            builds = {host: executor.submit(build_host, ROOT, host, ["core"], packages / host,
                                            include_plugin=True, include_resources=False) for host in hosts}
            for host in hosts:
                with self.subTest(host=host), temporary_tree(lab_root()) as project:
                    self.assertFalse(project.resolve().is_relative_to(ROOT))
                    bundle = packages / host
                    manifest = builds[host].result()
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
                    self.assertLessEqual(len(hook["members"]), 64)
                    if host in PROMPT_EVENTS:
                        codec_name, invocation, root = PROMPT_EVENTS[host]
                        skill = project / root / "nckh-fix/SKILL.md"
                        skill.parent.mkdir(parents=True)
                        skill.write_text("---\nname: nckh-fix\n---\n", encoding="utf8")
                        prompt = payload(project, host=host)
                        prompt.update(hook_event_name=codec_name, prompt=f"Giúp mình {fix_cue()} trong app.py nhé")
                        process = self.invoke(bundle / hook["entrypoint"], ["--host", host, "--event", codec_name,
                            "--project", str(project), "--context", "missing.json", "--mode", "advisory",
                            "--receipt-dir", "receipts"],
                            project, json.dumps(prompt).encode())
                        self.assertEqual(process.returncode, 0, process.stderr)
                        wire = json.loads(process.stdout)
                        if host == "cursor":
                            self.assertEqual(wire, {})
                        else:
                            self.assertIn(invocation, wire["hookSpecificOutput"]["additionalContext"])
                        receipts = [json.loads(path.read_text(encoding="utf8")) for path in (project / "receipts").glob("*.json")]
                        self.assertEqual([receipt["nudge"]["skills"] for receipt in receipts], [["nckh-fix"]])
                    self.assertFalse((bundle / "plugin/hooks/hooks.json").exists())
                    verify_bundle(bundle)

    def test_on_off_resources_keep_the_identical_pinned_hook_closure(self):
        with temporary_tree(lab_root()) as package:
            enabled = copy_bundle(package / "on", "codex", ["core"], root=ROOT)
            disabled = copy_bundle(package / "off", "codex", ["core"], include_resources=False, root=ROOT)
            self.assertEqual(enabled["source_lock_hash"], disabled["source_lock_hash"])
            for path in enabled["hooks"]["members"]:
                self.assertEqual((package / "on" / path).read_bytes(), (package / "off" / path).read_bytes())
            self.assertNotEqual(enabled["closure_hash"], disabled["closure_hash"])

    def test_missing_tampered_import_schema_and_extra_members_fail(self):
        with temporary_tree(lab_root()) as package, temporary_tree(lab_root()) as project:
            bundle = package / "codex"
            manifest = copy_bundle(bundle, "codex", ["core"], include_resources=False, root=ROOT)
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
        with temporary_tree(lab_root()) as package:
            bundle = package / "codex"
            original = copy_bundle(bundle, "codex", ["core"], include_resources=False, root=ROOT)
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
        with temporary_tree(lab_root()) as package, temporary_tree(lab_root()) as project:
            bundle = package / "codex"
            copy_bundle(bundle, "codex", ["core"], include_resources=False, root=ROOT)
            self.context(project)
            before = {p.relative_to(project).as_posix(): p.read_bytes() for p in project.rglob("*") if p.is_file()}
            preview = preview_config(project, "codex", payload_from_bundle(bundle), context_reference="context.json")
            self.assertFalse(preview["registered"] or preview["enabled"] or preview["trusted"])
            self.assertEqual(before, {p.relative_to(project).as_posix(): p.read_bytes() for p in project.rglob("*") if p.is_file()})
