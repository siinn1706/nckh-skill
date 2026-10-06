import json
import subprocess
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

from core.hook_config import SURFACES, TARGETS, _definition, apply_config, preview_config, recover_config
from core.paths import atomic_json, digest_file, digest_record, exclusive_file_lock, temporary_tree
from core.schema import ContractError


class HookConfigTests(unittest.TestCase):
    def setUp(self):
        self.tree = temporary_tree()
        self.root = self.tree.__enter__()
        self.addCleanup(self.tree.__exit__, None, None, None)
        self.project = self.root / "project"
        self.project.mkdir()
        self.package = self.root / "package"
        (self.package / "hooks").mkdir(parents=True)
        (self.package / "hooks/runner.py").write_text('"""Owned staging-byte fixture, not a native hook."""\n', encoding="utf8")
        self.members = {"hooks/runner.py": digest_file(self.package / "hooks/runner.py")}
        atomic_json(self.project / ".nckh-state/hooks/context/current.json", {"schema_version": 1})

    def payload(self, host):
        return {"root": str(self.package), "host": host, "members": self.members,
            "closure_hash": digest_record(self.members), "runner": "hooks/runner.py", "package_manifest_hash": digest_record("unit fixture")}

    def preview(self, host="codex", action="apply"):
        return preview_config(self.project, host, self.payload(host), action=action, host_version="isolated-unit-fixture",
                              surface=sorted(SURFACES[host])[0])

    def apply(self, preview, **kwargs):
        return apply_config(preview, approved_hash=digest_record(preview), grant_reference="isolated-unit-test-authority",
                            native_verified=True, **kwargs)

    def seed(self, host):
        event = "preToolUse" if host == "cursor" else "PreToolUse"
        record = {"user_value": "retain"}
        if host == "agy":
            record["user-owned"] = {"enabled": True, event: [{"hooks": [{"command": "user-owned"}]}]}
        else:
            record["hooks"] = {event: [{"command": "user-owned"}]}
            if host == "cursor":
                record["version"] = 1
        atomic_json(self.project / TARGETS[host], record)
        return record

    def test_preview_is_read_only_and_apply_requires_separate_activation(self):
        before = {str(p): digest_file(p) for p in self.project.rglob("*") if p.is_file()}
        preview = self.preview()
        self.assertEqual(before, {str(p): digest_file(p) for p in self.project.rglob("*") if p.is_file()})
        self.assertFalse(preview["registered"] or preview["enabled"] or preview["trusted"])
        with self.assertRaises(ContractError):
            apply_config(preview, approved_hash=digest_record(preview))

    def test_advisory_can_activate_without_native_claims_and_context(self):
        (self.project / ".nckh-state/hooks/context/current.json").unlink()
        preview = preview_config(self.project, "cursor", self.payload("cursor"), mode="advisory")
        handler = preview["after"]["hooks"]["preToolUse"][0]
        self.assertFalse(handler["failClosed"])
        self.assertIn("--mode advisory", handler["command"])
        result = apply_config(preview, approved_hash=digest_record(preview), grant_reference="unit-test-advisory-request")
        self.assertEqual(result["status"], "committed")
        state = json.loads((self.project / ".nckh-state/hooks/ownership.json").read_text())
        self.assertEqual(state["configs"]["cursor"]["mode"], "advisory")
        self.assertEqual(state["configs"]["cursor"]["native_qualification"], "unverified")
        self.assertTrue(state["configs"]["cursor"]["enabled"])
        removal = preview_config(self.project, "cursor", self.payload("cursor"), action="remove")
        apply_config(removal, approved_hash=digest_record(removal))

    def test_advisory_still_requires_human_confirmation(self):
        preview = preview_config(self.project, "codex", self.payload("codex"), mode="advisory")
        with self.assertRaises(ContractError):
            apply_config(preview, approved_hash=digest_record(preview))

    def test_claude_exec_arguments_preserve_spaces_quotes_and_shell_characters(self):
        values = [r"C:\project with spaces\draft.json", "literal & value", "$(unexpanded)", "single ' and double \" quotes"]
        argv = [sys.executable, "-I", "-c", "import json,sys; print(json.dumps(sys.argv[1:]))", *values]
        definition = _definition("claude", "PreToolUse", argv)
        handler = definition["hooks"][0]
        observed = subprocess.run([handler["command"], *handler["args"]], cwd=self.project,
                                  capture_output=True, text=True, check=True, timeout=10)
        self.assertEqual(json.loads(observed.stdout), values)
        self.assertEqual(definition["matcher"], ".*")

    def test_four_host_owned_merges_and_removes_preserve_unowned_fields(self):
        for host in TARGETS:
            original = self.seed(host)
            self.assertEqual(self.apply(self.preview(host))["status"], "committed")
            state = json.loads((self.project / ".nckh-state/hooks/ownership.json").read_text())
            self.assertFalse(state["configs"][host]["trusted"])
            self.assertEqual(self.apply(self.preview(host, "remove"))["status"], "committed")
            self.assertEqual(json.loads((self.project / TARGETS[host]).read_text()), original)

    def test_changed_after_preview_and_duplicate_or_invalid_json_are_untouched(self):
        original = self.seed("codex")
        preview = self.preview()
        original["user_value"] = "changed-after-preview"
        atomic_json(self.project / TARGETS["codex"], original)
        current = (self.project / TARGETS["codex"]).read_bytes()
        with self.assertRaises(ContractError):
            self.apply(preview)
        self.assertEqual((self.project / TARGETS["codex"]).read_bytes(), current)
        for data in (b"{invalid", b'{"hooks":{},"hooks":{}}'):
            (self.project / TARGETS["codex"]).write_bytes(data)
            with self.assertRaises(ContractError):
                self.preview()
            self.assertEqual((self.project / TARGETS["codex"]).read_bytes(), data)

    def test_partial_failures_restore_matching_config_state_and_payload(self):
        self.seed("codex")
        before = (self.project / TARGETS["codex"]).read_bytes()
        for stage in ("payload", "config", "index"):
            preview = self.preview()
            with self.subTest(stage=stage), self.assertRaises(ContractError):
                self.apply(preview, fail_at=stage)
            self.assertEqual((self.project / TARGETS["codex"]).read_bytes(), before)
            self.assertFalse((self.project / preview["runtime_relative"]).exists())
        self.assertEqual(len(list((self.project / ".nckh-state/hooks/transactions").glob("*.json"))), 3)

    def test_user_edits_and_unknown_ownership_are_conflicts(self):
        self.apply(self.preview())
        path = self.project / TARGETS["codex"]
        record = json.loads(path.read_text())
        record["hooks"]["PreToolUse"][0]["hooks"][0]["command"] = "user-edited"
        atomic_json(path, record)
        before = path.read_bytes()
        with self.assertRaisesRegex(ContractError, "rollback-conflict"):
            self.preview(action="remove")
        self.assertEqual(path.read_bytes(), before)
        atomic_json(self.project / TARGETS["agy"], {"nckh": {"enabled": False}})
        with self.assertRaises(ContractError):
            self.preview("agy")

    def test_concurrent_apply_has_one_commit_and_one_conflict(self):
        preview = self.preview()
        def attempt(_):
            try:
                return self.apply(preview)["status"]
            except ContractError:
                return "conflict"
        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertCountEqual(list(pool.map(attempt, range(2))), ["committed", "conflict"])

    def test_shared_agents_and_later_unowned_definition_survive_removal(self):
        shared = self.project / ".agents/skills/user-owned/SKILL.md"
        shared.parent.mkdir(parents=True)
        shared.write_text("user-owned bytes", encoding="utf8")
        self.apply(self.preview("agy"))
        self.apply(self.preview("codex"))
        path = self.project / TARGETS["codex"]
        record = json.loads(path.read_text())
        record["hooks"]["PreToolUse"].append({"command": "later-user-hook"})
        atomic_json(path, record)
        self.apply(self.preview("codex", "remove"))
        self.assertEqual(json.loads(path.read_text())["hooks"]["PreToolUse"], [{"command": "later-user-hook"}])
        self.assertTrue((self.project / TARGETS["agy"]).exists())
        self.assertEqual(shared.read_text(), "user-owned bytes")

    def test_forged_operations_and_payload_drift_do_not_write_config(self):
        preview = self.preview()
        preview["after"]["unowned-overwrite"] = True
        with self.assertRaises(ContractError):
            self.apply(preview)
        preview = self.preview()
        (self.package / "hooks/runner.py").write_text("changed", encoding="utf8")
        with self.assertRaises(ContractError):
            self.apply(preview)
        self.assertFalse((self.project / TARGETS["codex"]).exists())

    def test_interrupted_transaction_recovers_matching_preimages_and_keeps_later_edits(self):
        original = self.seed("codex")
        before = (self.project / TARGETS["codex"]).read_bytes()
        preview = self.preview()
        from core.hook_config import atomic_json as real_write
        def interrupt_after_config(path, record):
            if record.get("status") == "config-written":
                raise KeyboardInterrupt("simulated interruption after durable config write")
            return real_write(path, record)
        with patch("core.hook_config.atomic_json", side_effect=interrupt_after_config), self.assertRaises(KeyboardInterrupt):
            self.apply(preview)
        journal_path = next((self.project / ".nckh-state/hooks/transactions").glob("*.json"))
        journal = json.loads(journal_path.read_text())
        with self.assertRaisesRegex(ContractError, "unfinished"):
            self.preview()
        result = recover_config(self.project, journal_path.relative_to(self.project).as_posix(), approved_hash=digest_record(journal))
        self.assertEqual(result["status"], "recovered")
        self.assertEqual((self.project / TARGETS["codex"]).read_bytes(), before)
        self.assertFalse((self.project / preview["runtime_relative"]).exists())
        preview = self.preview()
        with patch("core.hook_config.atomic_json", side_effect=interrupt_after_config), self.assertRaises(KeyboardInterrupt):
            self.apply(preview)
        journal_path = next(path for path in (self.project / ".nckh-state/hooks/transactions").glob("*.json")
                            if json.loads(path.read_text())["status"] == "staging")
        journal = json.loads(journal_path.read_text())
        original["later_user_edit"] = "retain"
        atomic_json(self.project / TARGETS["codex"], original)
        edited = (self.project / TARGETS["codex"]).read_bytes()
        self.assertEqual(recover_config(self.project, journal_path.relative_to(self.project).as_posix(),
            approved_hash=digest_record(journal))["status"], "rollback-conflict")
        self.assertEqual((self.project / TARGETS["codex"]).read_bytes(), edited)

    def test_remove_preserves_payload_referenced_by_another_host(self):
        preview = self.preview()
        self.apply(preview)
        runtime = self.project / preview["runtime_relative"]
        atomic_json(self.project / TARGETS["claude"], {"hooks": {"PreToolUse": [
            {"hooks": [{"type": "command", "command": str(runtime / "hooks/runner.py")}]}]}})
        self.apply(self.preview(action="remove"))
        self.assertTrue((runtime / "hooks/runner.py").is_file())
