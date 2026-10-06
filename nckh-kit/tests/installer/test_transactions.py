import json
import os
import shutil
import subprocess
import sys
import tomllib
import unittest
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from core.build import build_host, verify_bundle
from core.install import (commit_install, doctor, plan_install, read_index,
                          resolve_targets, rollback, target_lock, tree_hash, uninstall)
from core.paths import atomic_json, digest_file, digest_record, temporary_tree
from core.schema import ContractError


class TransactionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle_context = temporary_tree()
        cls.package = cls.bundle_context.__enter__()
        root = Path(__file__).resolve().parents[2]
        build_host(root, "codex", ["core"], cls.package / "codex")
        build_host(root, "agy", ["core"], cls.package / "agy")

    @classmethod
    def tearDownClass(cls):
        cls.bundle_context.__exit__(None, None, None)

    def setUp(self):
        self.context = temporary_tree()
        self.root = self.context.__enter__()
        self.project = self.root / "Dự án có dấu và spaces"
        self.project.mkdir()
        self.home = self.root / "home"
        self.home.mkdir()
        self.state = self.root / "state"
        self.targets = resolve_targets(self.package, ["codex-cli"], scope="project", project=self.project, home=self.home)

    def tearDown(self):
        self.context.__exit__(None, None, None)

    def plan(self, **kwargs):
        return plan_install(self.targets, read_index(self.state), kits=["core"], mode="copy",
                            profile="balanced", scope="project", **kwargs)

    def test_dry_run_unicode_and_doctor_are_read_only(self):
        plan = self.plan()
        self.assertEqual({e["action"] for e in plan["entries"]}, {"create"})
        self.assertFalse(self.state.exists())
        self.assertFalse((self.project / ".agents").exists())
        self.assertEqual(doctor(self.state)["items"], [])
        self.assertFalse(self.state.exists())

    def test_doctor_reports_broken_closure_native_syntax_and_candidate_drift(self):
        installed = commit_install(self.plan(with_agents=True), self.state)
        before_index = (self.state / "ownership.json").read_bytes()
        clean = doctor(self.state)
        self.assertEqual(clean["installs"][0]["candidate_integrity"], "current")
        self.assertEqual(clean["installs"][0]["visibility_conflicts"], [])
        self.assertEqual({row["closure_or_syntax"] for row in clean["items"]}, {"self-contained", "valid-toml"})
        write = self.project / ".agents/skills/nckh-write/SKILL.md"
        write.write_text("[missing source](missing.md)", encoding="utf-8")
        maker = self.project / ".codex/agents/nckh-maker.toml"
        maker.write_text('model = "unterminated', encoding="utf-8")
        broken = doctor(self.state)
        for path in [write.parent, maker]:
            row = next(row for row in broken["items"] if row["path"] == str(path))
            self.assertEqual(row["status"], "edited/missing/stale")
            self.assertEqual(row["closure_or_syntax"], "invalid")
        with patch("core.install.verify_bundle", side_effect=ContractError("injected candidate drift")):
            self.assertEqual(doctor(self.state)["installs"][0]["candidate_integrity"], "unavailable-or-invalid")
        self.assertEqual((self.state / "ownership.json").read_bytes(), before_index)
        self.assertEqual(read_index(self.state)["installs"][installed["install_id"]]["operation"], "install")

    def test_install_rerun_is_content_noop_and_uninstall_preserves_edits(self):
        result = commit_install(self.plan(), self.state)
        plan = self.plan()
        self.assertEqual({e["action"] for e in plan["entries"]}, {"unchanged"})
        self.assertEqual(commit_install(plan, self.state)["changes"], 0)
        file = self.project / ".agents/skills/nckh-write/SKILL.md"
        file.write_text("user-owned revised content", encoding="utf-8")
        conflict = self.plan()
        self.assertTrue(conflict["conflicts"])
        with self.assertRaises(ContractError):
            commit_install(conflict, self.state)
        residue = uninstall(self.state, result["install_id"], dry_run=False)
        self.assertEqual(residue["status"], "uninstalled-with-residue")
        self.assertEqual(file.read_text(encoding="utf-8"), "user-owned revised content")
        self.assertTrue((self.project / ".agents/skills").is_dir())

    def test_partial_install_rolls_back_exact_owned_changes(self):
        with self.assertRaises(OSError):
            commit_install(self.plan(), self.state, fail_after=2)
        self.assertEqual(read_index(self.state)["items"], {})
        self.assertFalse((self.project / ".agents/skills/nckh-cook").exists())
        journal = json.loads((self.state / "journal.json").read_text())
        self.assertEqual(journal["status"], "rolled-back")

    def test_lock_never_kills_or_overwrites_other_owner(self):
        with target_lock(self.state):
            with self.assertRaises(ContractError):
                with target_lock(self.state):
                    pass
        self.assertEqual(json.loads((self.state / "installer.lock").read_text())["state"], "released")

    def test_different_state_directories_serialize_same_physical_target(self):
        roots = [self.targets[0]["root"]]
        with target_lock(self.state, roots):
            with self.assertRaises(ContractError):
                with target_lock(self.root / "other-state", roots):
                    pass

    def test_interrupted_uninstall_restores_files_and_ownership(self):
        result = commit_install(self.plan(), self.state)
        before = read_index(self.state)
        with self.assertRaises(OSError):
            uninstall(self.state, result["install_id"], dry_run=False, fail_after=2)
        self.assertEqual(read_index(self.state), before)
        self.assertTrue((self.project / ".agents/skills/nckh-cook/SKILL.md").exists())

    def test_unmanaged_same_name_is_conflict_even_with_same_bytes(self):
        import shutil
        target = self.project / ".agents/skills/nckh-plan"
        target.parent.mkdir(parents=True)
        shutil.copytree(self.package / "codex/skills/nckh-plan", target)
        self.assertTrue(self.plan()["conflicts"])

    def test_shared_consumers_need_qualification_and_survive_other_uninstall(self):
        first = commit_install(self.plan(), self.state)
        agy_targets = resolve_targets(self.package, ["agy-cli"], scope="project", project=self.project, home=self.home)
        with self.assertRaises(ContractError):
            plan_install(agy_targets, read_index(self.state), kits=["core"], mode="copy", profile="balanced", scope="project")
        second_plan = plan_install(agy_targets, read_index(self.state), kits=["core"], mode="copy", profile="balanced", scope="project",
                                   capabilities={"qualified_neutral_consumers": ["codex-cli", "agy-cli"]})
        second = commit_install(second_plan, self.state)
        uninstall(self.state, first["install_id"], dry_run=False)
        self.assertTrue((self.project / ".agents/skills/nckh-plan/SKILL.md").is_file())
        self.assertEqual(len(read_index(self.state)["items"]), 16)
        uninstall(self.state, second["install_id"], dry_run=False)
        self.assertEqual(read_index(self.state)["items"], {})

    def test_unknown_custom_or_symlink_does_not_silently_fallback(self):
        for mode, profile in [("symlink", "balanced"), ("copy", "custom")]:
            with self.assertRaises(ContractError):
                plan_install(self.targets, read_index(self.state), kits=["core"], mode=mode, profile=profile, scope="project")

    def test_later_user_edit_is_not_overwritten_by_rollback(self):
        commit_install(self.plan(), self.state)
        journal = json.loads((self.state / "journal.json").read_text())
        file = self.project / ".agents/skills/nckh-plan/SKILL.md"
        file.write_text("edit after commit", encoding="utf-8")
        with self.assertRaises(ContractError):
            rollback(self.state, journal, allowed_roots=[self.targets[0]["root"]])
        self.assertEqual(file.read_text(encoding="utf-8"), "edit after commit")

    def test_owned_update_accepts_new_candidate_without_overwriting_edits(self):
        import shutil
        commit_install(self.plan(), self.state)
        candidate = self.root / "candidate"
        shutil.copytree(self.package / "codex", candidate)
        path = candidate / "skills/nckh-write/SKILL.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nOriginal synthetic update fixture.\n", encoding="utf-8")
        manifest = json.loads((candidate / "manifest.json").read_text())
        for record in manifest["files"]:
            if record["path"] == "skills/nckh-write/SKILL.md":
                record["sha256"] = digest_file(path)
        for skill in manifest["skills"]:
            if skill["id"] == "nckh-write":
                skill["tree_hash"] = tree_hash(path.parent)
        manifest["closure_hash"] = digest_record(manifest["files"])
        atomic_json(candidate / "manifest.json", manifest)
        targets = resolve_targets(candidate, ["codex-cli"], scope="project", project=self.project, home=self.home)
        options = dict(kits=["core"], mode="copy", profile="balanced", scope="project")
        self.assertTrue(plan_install(targets, read_index(self.state), **options)["conflicts"])
        with self.assertRaises(ContractError):
            plan_install(targets, read_index(self.state), operation="update", **options)
        verified = verify_bundle(candidate)
        receipt_path = self.root / "candidate-check.json"
        receipt = {"schema_version": 1, "evidence_class": "static", "input_class": "synthetic-fixture",
                   "scope": "candidate bundle integrity only", "status": "pass", "command": ["core.build.verify_bundle"], "exit_status": 0,
                   "closure_hashes": {"codex": verified["closure_hash"]}, "source_lock_hashes": {"codex": verified["source_lock_hash"]},
                   "affected_skills": ["nckh-write"], "limitations": ["Synthetic update input; no native or human acceptance."]}
        atomic_json(receipt_path, receipt)
        evidence = {"schema_version": 1, "evidence_class": "static", "qualification": "accepted-for-scope",
                    "closure_hashes": {"codex": manifest["closure_hash"]},
                    "source_lock_hashes": {"codex": manifest["source_lock_hash"]},
                    "affected_skills": ["nckh-write"],
                    "checks": [{"id": "fixture-tree-guard", "result": "pass", "receipt": str(receipt_path), "receipt_sha256": digest_file(receipt_path)}]}
        with self.assertRaises(ContractError):
            plan_install(targets, read_index(self.state), operation="update", candidate_evidence={**evidence, "qualification": "pending"}, **options)
        with self.assertRaises(ContractError):
            plan_install(targets, read_index(self.state), operation="update", candidate_evidence={**evidence, "evidence_class": "synthetic-fixture"}, **options)
        for overstated_class in ["deterministic", "agent-behavior", "native"]:
            with self.subTest(evidence_class=overstated_class), self.assertRaisesRegex(ContractError, "typed receipt"):
                plan_install(targets, read_index(self.state), operation="update", candidate_evidence={**evidence, "evidence_class": overstated_class}, **options)
        plan = plan_install(targets, read_index(self.state), operation="update", candidate_evidence=evidence, **options)
        self.assertEqual(next(e for e in plan["entries"] if e["skill"] == "nckh-write")["action"], "replace")
        before_index = read_index(self.state)
        receipt_bytes = receipt_path.read_bytes()
        atomic_json(receipt_path, {**receipt, "scope": "changed after preview"})
        with self.assertRaisesRegex(ContractError, "receipt"):
            commit_install(plan, self.state)
        self.assertEqual(read_index(self.state), before_index)
        receipt_path.write_bytes(receipt_bytes)
        commit_install(plan, self.state)
        self.assertEqual(tree_hash(path.parent), tree_hash(self.project / ".agents/skills/nckh-write"))
        self.assertEqual(read_index(self.state)["installs"][plan["install_id"]]["provenance"][0]["closure_hash"], manifest["closure_hash"])
        configuration = plan_install(targets, read_index(self.state), operation="config-models", with_agents=True, **options)
        commit_install(configuration, self.state)
        diagnostics = doctor(self.state)["installs"][0]
        self.assertEqual(diagnostics["candidate_receipts"]["status"], "current")
        self.assertEqual(diagnostics["candidate_receipts"]["input_classes"], ["synthetic-fixture"])
        before_index = (self.state / "ownership.json").read_bytes()
        receipt_path.unlink()
        diagnostics = doctor(self.state)["installs"][0]
        self.assertEqual(diagnostics["candidate_integrity"], "current")
        self.assertEqual(diagnostics["candidate_receipts"]["status"], "invalid-or-stale")
        self.assertEqual(diagnostics["candidate_receipts"]["qualification"], "unverified")
        self.assertEqual((self.state / "ownership.json").read_bytes(), before_index)

    def test_commit_rejects_forged_outside_target_before_writing(self):
        plan = self.plan()
        outside = self.root / "private/nckh-plan"
        plan["entries"][0]["physical_path"] = str(outside)
        with self.assertRaises(ContractError):
            commit_install(plan, self.state)
        self.assertFalse(outside.parent.exists())
        self.assertFalse(self.state.exists())

    def test_stale_install_ownership_rejected_before_transaction(self):
        stale = self.plan()
        commit_install(deepcopy(stale), self.state)
        before = read_index(self.state)
        with self.assertRaisesRegex(ContractError, "ownership changed"):
            commit_install(stale, self.state)
        self.assertEqual(read_index(self.state), before)

    def test_missing_backup_preserves_current_tree_and_restores_index(self):
        plan = self.plan()
        commit_install(plan, self.state)
        before = read_index(self.state)
        target = Path(plan["entries"][0]["physical_path"])
        current_hash = tree_hash(target)
        journal = {"schema_version": 1, "id": "missing-backup", "status": "committing", "roots": plan["roots"],
                   "index_before": before, "changes": [{"physical_path": str(target), "before_hash": "old-fixture-hash",
                   "after_hash": current_hash, "backup": "transactions/missing-backup/backup-0", "progress": "written"}]}
        atomic_json(self.state / "ownership.json", {**before, "policies": {}})
        with self.assertRaises(ContractError):
            rollback(self.state, journal, allowed_roots=plan["roots"])
        self.assertEqual(tree_hash(target), current_hash)
        self.assertEqual(read_index(self.state), before)
        self.assertEqual(doctor(self.state)["recovery"]["status"], "rollback-conflict")

    def test_uninstall_reloads_owners_after_acquiring_lock(self):
        result = commit_install(self.plan(), self.state)
        real_lock = target_lock

        @contextmanager
        def owner_added_before_lock(state_dir, roots):
            index = read_index(state_dir)
            for item in index["items"].values():
                item["owners"].append("second-owner-fixture")
            index["installs"]["second-owner-fixture"] = deepcopy(index["installs"][result["install_id"]])
            atomic_json(self.state / "ownership.json", index)
            with real_lock(state_dir, roots):
                yield

        with patch("core.install.target_lock", owner_added_before_lock):
            removed = uninstall(self.state, result["install_id"], dry_run=False)
        self.assertEqual({item["action"] for item in removed["actions"]}, {"retain-shared"})
        self.assertTrue((self.project / ".agents/skills/nckh-plan/SKILL.md").exists())
        self.assertEqual(next(iter(read_index(self.state)["items"].values()))["owners"], ["second-owner-fixture"])

    def test_kernel_lock_released_by_crashed_process(self):
        source = Path(__file__).resolve().parents[2]
        script = "import os,sys; sys.path.insert(0,sys.argv[1]); from core.install import target_lock; from pathlib import Path\nwith target_lock(Path(sys.argv[2])):\n os._exit(17)\n"
        child = subprocess.Popen([sys.executable, "-c", script, str(source), str(self.state)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            stdout, stderr = child.communicate(timeout=15)
            self.assertEqual(child.returncode, 17, stderr.decode())
        finally:
            if child.poll() is None:
                child.terminate()
                child.communicate(timeout=10)
        with target_lock(self.state):
            pass
        self.assertEqual(json.loads((self.state / "installer.lock").read_text())["pid"], os.getpid())

    def test_different_surface_roots_share_discovery_serialization(self):
        with target_lock(self.state, [self.project / ".agents/skills"]):
            with self.assertRaises(ContractError):
                with target_lock(self.root / "other-state", [self.project / ".claude/skills"]):
                    pass

    def test_partial_kernel_owner_record_is_recoverable(self):
        self.state.mkdir()
        (self.state / "installer.lock").write_bytes(b'{"schema_version": 1, "lock_protocol": "kernel-advisory-v1", "pid":')
        with target_lock(self.state):
            pass
        self.assertEqual(json.loads((self.state / "installer.lock").read_text())["state"], "released")

    def test_cross_device_preflight_is_read_only_for_install_and_uninstall(self):
        plan = self.plan()
        def different_device(path):
            return 2 if Path(path) == self.state else 1
        with patch("core.install.device_identity", different_device):
            with self.assertRaises(ContractError):
                commit_install(plan, self.state)
        self.assertFalse(self.state.exists())
        result = commit_install(plan, self.state)
        before = read_index(self.state)
        with patch("core.install.device_identity", different_device):
            with self.assertRaises(ContractError):
                uninstall(self.state, result["install_id"], dry_run=False)
        self.assertEqual(read_index(self.state), before)

    def test_native_model_config_is_owned_transaction_and_uninstall_preserves_user_edit(self):
        initial = self.plan(with_agents=True)
        installed = commit_install(initial, self.state)
        maker = self.project / ".codex/agents/nckh-maker.toml"
        self.assertNotIn("model", tomllib.loads(maker.read_text(encoding="utf-8")))
        self.assertFalse((self.project / ".codex/config.toml").exists())
        observed = {"per_agent_override": True, "evidence_reference": "synthetic unit fixture; not native evidence",
                    "as_of": "2026-10-01", "allowed_models": ["fixture-model"],
                    "models": [{"id": "fixture-model", "tiers": ["fast", "worker", "deep"], "efforts": ["high"], "availability": "observed"}],
                    "mapping": {tier: {"model": "fixture-model", "effort": "high"} for tier in ["fast", "worker", "deep"]}}
        plan = plan_install(self.targets, read_index(self.state), kits=["core"], mode="copy", profile="custom", scope="project",
                            with_agents=True, operation="config-models", capabilities={"native_models": {"codex": observed}})
        before = maker.read_bytes()
        first_agent_write = next(number + 1 for number, entry in enumerate(plan["entries"])
                                 if entry["kind"] == "native-agent" and entry["action"] not in {"unchanged", "keep-edited"})
        with self.assertRaises(OSError):
            commit_install(plan, self.state, fail_after=first_agent_write)
        self.assertEqual(maker.read_bytes(), before)
        commit_install(plan, self.state)
        parsed = tomllib.loads(maker.read_text(encoding="utf-8"))
        self.assertEqual(parsed["model"], "fixture-model")
        self.assertEqual(parsed["model_reasoning_effort"], "high")
        self.assertEqual(next(iter(read_index(self.state)["policies"].values()))["effective"], "unknown")
        maker.write_text(maker.read_text(encoding="utf-8") + "\n# user fixture edit\n", encoding="utf-8")
        uninstall(self.state, installed["install_id"], dry_run=False)
        self.assertTrue(maker.exists())
        self.assertFalse((self.project / ".codex/agents/nckh-reviewer.toml").exists())
