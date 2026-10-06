import json
import os
import unittest
from unittest.mock import patch
from pathlib import Path

from core.build import _promote_staging, build_host, closure, freeze_sources, select_skills, source_members, verify_bundle
from core.paths import atomic_json, contained, digest_record, temporary_tree
from core.schema import ContractError


class BuildTests(unittest.TestCase):
    def test_source_inventory_accepts_relative_and_absolute_root(self):
        root = Path(__file__).resolve().parents[2]
        self.assertEqual(source_members(root), source_members(os.path.relpath(root, Path.cwd())))

    @unittest.skipUnless(os.name == "nt", "Windows sharing conflict")
    def test_owned_promotion_retries_sharing_conflict_and_preserves_concurrent_destination(self):
        with temporary_tree() as parent:
            staging = parent / "staging"
            staging.mkdir()
            (staging / "owned.txt").write_text("owned candidate", encoding="utf8")
            output = parent / "candidate"
            real_replace = os.replace
            conflict = PermissionError("simulated scanner sharing conflict")
            conflict.winerror = 5
            calls = []
            def transient(source, target):
                calls.append((source, target))
                if len(calls) == 1:
                    raise conflict
                return real_replace(source, target)
            with patch("core.build.os.replace", side_effect=transient), patch("core.build.time.sleep"):
                _promote_staging(staging, output)
            self.assertEqual((output / "owned.txt").read_text(), "owned candidate")
            self.assertEqual(len(calls), 2)
            staging.mkdir()
            (staging / "owned.txt").write_text("next candidate", encoding="utf8")
            with self.assertRaises(ContractError):
                _promote_staging(staging, output)
            self.assertEqual((output / "owned.txt").read_text(), "owned candidate")

    def test_missing_reference_cycle_and_escape_fail(self):
        with temporary_tree() as root:
            a = root / "a.md"
            a.write_text("[missing](missing.md)", encoding="utf-8")
            with self.assertRaises(ContractError):
                closure(root, [a])
            b = root / "b.md"
            a.write_text("[b](b.md)", encoding="utf-8")
            b.write_text("[a](a.md)", encoding="utf-8")
            with self.assertRaises(ContractError):
                closure(root, [a])
            a.write_text("[escape](../outside.md)", encoding="utf-8")
            with self.assertRaises(ContractError):
                closure(root, [a])

    def test_path_traversal_case_and_symlink_guards(self):
        from core.paths import unique_paths
        with temporary_tree() as root:
            for rel in ["../data", "/absolute", "C:/secret", "a\\b", "a/./b"]:
                with self.assertRaises(ContractError):
                    contained(root, rel)
        with self.assertRaises(ContractError):
            unique_paths(["Skill/a.md", "skill/A.md"])

    def test_selected_engineer_adds_only_shared_primitives_and_xia(self):
        root = Path(__file__).resolve().parents[2]
        catalog = json.loads((root / "core/registry/catalog/skills.json").read_text(encoding="utf-8"))
        selected = select_skills(catalog, ["engineer"])
        self.assertEqual(len(selected), 18)
        self.assertIn("nckh-xia", {r["id"] for r in selected})
        self.assertNotIn("nckh-visuals", {r["id"] for r in selected})

    def test_real_bundle_reproducibility_and_tamper_detection(self):
        root = Path(__file__).resolve().parents[2]
        with temporary_tree() as a, temporary_tree() as b:
            first = build_host(root, "codex", ["core"], a)
            second = build_host(root, "codex", ["core"], b)
            self.assertEqual(first, second)
            (a / "skills/nckh-plan/SKILL.md").write_text("user edit", encoding="utf-8")
            with self.assertRaises(ContractError):
                verify_bundle(a)

    def test_manifest_skill_traversal_and_tree_metadata_rejected(self):
        root = Path(__file__).resolve().parents[2]
        with temporary_tree() as bundle:
            original = build_host(root, "codex", ["core"], bundle)
            for field, value in [("id", "../../private"), ("tree_hash", "0" * 64)]:
                manifest = json.loads(json.dumps(original))
                manifest["skills"][0][field] = value
                atomic_json(bundle / "manifest.json", manifest)
                with self.assertRaises(ContractError):
                    verify_bundle(bundle)

    def test_failed_build_cleans_staging_and_preserves_destination(self):
        root = Path(__file__).resolve().parents[2]
        with temporary_tree() as parent:
            output = parent / "candidate"
            output.mkdir()
            with patch("core.build.verify_bundle", side_effect=ContractError("injected verification failure")):
                with self.assertRaises(ContractError):
                    build_host(root, "codex", ["core"], output)
            self.assertEqual(list(parent.iterdir()), [output])
            self.assertEqual(list(output.iterdir()), [])
            build_host(root, "codex", ["core"], output)
            self.assertTrue((output / "manifest.json").exists())

    def test_source_lock_pins_code_and_keeps_previous_revision(self):
        with temporary_tree() as root:
            (root / "core").mkdir()
            (root / "evals").mkdir()
            code = root / "core/original.py"
            code.write_text("fixture = 1\n", encoding="utf-8")
            (root / "evals/run-evals.py").write_text("fixture = 1\n", encoding="utf-8")
            first = freeze_sources(root)
            self.assertIn("core/original.py", first["files"])
            self.assertEqual(freeze_sources(root), first)
            code.write_text("fixture = 2\n", encoding="utf-8")
            second = freeze_sources(root)
            self.assertEqual(int(second["revision"]), int(first["revision"]) + 1)
            archived = list((root / "core/registry/source-lock/history").glob("*.json"))
            self.assertEqual(json.loads(archived[0].read_text()), first)

    def test_plugin_projection_is_same_closure_without_runtime_activation(self):
        root = Path(__file__).resolve().parents[2]
        with temporary_tree() as output:
            manifest = build_host(root, "codex", ["core"], output, include_plugin=True)
            self.assertEqual((output / "plugin/skills/nckh-plan/SKILL.md").read_bytes(), (output / "skills/nckh-plan/SKILL.md").read_bytes())
            self.assertEqual(len(manifest["agents"]), 6)
            self.assertTrue(manifest["plugin"]["projected"])
            self.assertFalse(manifest["plugin"]["registered"])
            self.assertFalse(manifest["plugin"]["agents_projected"])
            self.assertNotIn(str(root), (output / "native/agents/nckh-maker.toml").read_text(encoding="utf-8"))
            verify_bundle(output)

    def test_source_provenance_cannot_disagree_with_embedded_lock(self):
        root = Path(__file__).resolve().parents[2]
        with temporary_tree() as output:
            manifest = build_host(root, "codex", ["core"], output)
            manifest["files"][0]["source_sha256"] = "0" * 64
            manifest["closure_hash"] = digest_record(manifest["files"])
            atomic_json(output / "manifest.json", manifest)
            with self.assertRaises(ContractError):
                verify_bundle(output)

    def test_build_detects_source_drift_after_materialization(self):
        import shutil
        from core.build import _materialize_host
        source = Path(__file__).resolve().parents[2]
        with temporary_tree() as root:
            for member in source_members(source) + ["core/registry/source-lock/source-lock.json"]:
                destination = root / member
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source / member, destination)
            output = root / "candidate"
            def drift(*args, **kwargs):
                manifest = _materialize_host(*args, **kwargs)
                (root / "skills/core/nckh-plan/SKILL.md").write_text("concurrent synthetic edit", encoding="utf-8")
                return manifest
            with patch("core.build._materialize_host", drift):
                with self.assertRaises(ContractError):
                    build_host(root, "codex", ["core"], output)
            self.assertFalse(output.exists())
