import os
import shutil
import subprocess
import sys
import unittest
from tests._bundles import copy_bundle
from tests._lab import lab_root
from copy import deepcopy
from pathlib import Path

from core.build import (build_host, closure, freeze_sources, load_json, source_members,
                        verify_bundle, verify_lock_structure, verify_source_lock)
from core.install import plan_install, read_index, refresh_targets, resolve_targets
from core.paths import atomic_json, digest_record, temporary_tree
from core.resources import REGISTRY_PATH, registry
from core.schema import ContractError


ROOT = Path(os.environ.get("NCKH_RESOURCE_TEST_ROOT", Path(__file__).resolve().parents[2]))


def copy_source(target):
    for relative in source_members(ROOT) + ["core/registry/source-lock/source-lock.json"]:
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, path)


class ResourceClosureTests(unittest.TestCase):
    def test_legacy_lock_remains_readable_and_copied_cannot_be_relabelled(self):
        history = ROOT / "core/registry/source-lock/history"
        if history.exists():
            for path in history.glob("*.json"):
                if load_json(path)["schema_version"] == 1:
                    verify_lock_structure(ROOT, load_json(path))
        lock = verify_source_lock(ROOT)
        copied = next(p for p in lock["files"].values() if p["rights"] == "copied-upstream")
        broken = deepcopy(lock)
        broken["copied_third_party_content"] = False
        with self.assertRaises(ContractError):
            verify_lock_structure(ROOT, broken)
        broken = deepcopy(lock)
        for pin in broken["files"].values():
            if pin["rights"] == "copied-upstream":
                pin["rights"] = "owned-local-package"
                break
        with self.assertRaises(ContractError):
            verify_lock_structure(ROOT, broken)

    def test_unlisted_data_and_rights_or_hash_drift_fail_before_freeze(self):
        with temporary_tree() as source:
            copy_source(source)
            (source / "core/profiles/resources/unlisted.csv").write_text("unlisted\n", encoding="utf-8")
            with self.assertRaises(ContractError):
                source_members(source)
        for field, value in [("redistribution", "blocked-rights"), ("version", "short"), ("license_sha256", "0" * 64)]:
            with temporary_tree() as source:
                copy_source(source)
                catalog = load_json(source / REGISTRY_PATH)
                catalog["resources"][0]["source"][field] = value
                atomic_json(source / REGISTRY_PATH, catalog)
                with self.subTest(field=field), self.assertRaises(ContractError):
                    freeze_sources(source)

    def test_explicit_resource_edges_detect_cycles_and_private_or_escaping_paths(self):
        with temporary_tree() as source:
            copy_source(source)
            resources = registry(source)["resources"]
            first, second = resources[0]["path"], resources[1]["path"]
            with self.assertRaises(ContractError):
                closure(source, [source / first], requires={first: [second], second: [first]})
            for relative in ["../private.csv", "evals/results/receipt.json", "core/profiles/resources/extra.csv"]:
                catalog = load_json(source / REGISTRY_PATH)
                catalog["resources"][0]["requires"].append(relative)
                atomic_json(source / REGISTRY_PATH, catalog)
                with self.subTest(path=relative), self.assertRaises(ContractError):
                    registry(source)
                atomic_json(source / REGISTRY_PATH, load_json(ROOT / REGISTRY_PATH))

    def test_v2_bundle_and_all_installer_consumers_share_rights_validation(self):
        with temporary_tree() as package, temporary_tree(lab_root()) as environment:
            bundle = package / "codex"
            manifest = copy_bundle(bundle, "codex", ["core", "engineer"], root=ROOT)
            self.assertEqual(manifest["schema_version"], 2)
            targets = resolve_targets(package, ["codex-cli"], scope="project", project=environment, home=environment)
            refresh_targets(targets, "project")
            plan = plan_install(targets, read_index(environment / "state"), kits=["core"], mode="copy", profile="balanced", scope="project")
            self.assertEqual(plan["operation"], "install")
            self.assertEqual(plan["conflicts"], [])
            self.assertEqual(plan["native_smoke"], "not-run")
            copied = next(row for row in manifest["files"] if row["rights"] == "copied-upstream")
            (bundle / copied["path"]).write_bytes(b"tampered data")
            for check in [lambda: verify_bundle(bundle), lambda: refresh_targets(targets, "project"),
                          lambda: resolve_targets(package, ["codex-cli"], scope="project", project=environment, home=environment),
                          lambda: plan_install(targets, read_index(environment / "state"), kits=["core"], mode="copy", profile="balanced", scope="project")]:
                with self.assertRaises(ContractError):
                    check()
            self.assertFalse((environment / ".agents").exists())

    def test_on_off_same_source_and_instruction_policy_with_distinct_closure(self):
        with temporary_tree() as on, temporary_tree() as off:
            enabled = copy_bundle(on, "codex", ["core", "engineer"], root=ROOT)
            disabled = build_host(ROOT, "codex", ["core", "engineer"], off, include_resources=False)
            self.assertEqual(enabled["source_lock_hash"], disabled["source_lock_hash"])
            self.assertNotEqual(enabled["closure_hash"], disabled["closure_hash"])
            self.assertEqual(disabled["resources"], [])
            self.assertFalse(any(r["rights"] == "copied-upstream" for r in disabled["files"]))
            on_code = {r["path"]: r["sha256"] for r in enabled["files"] if r["source_path"].endswith(".py")}
            off_code = {r["path"]: r["sha256"] for r in disabled["files"] if r["source_path"].endswith(".py")}
            self.assertEqual(on_code, off_code)
            script = next(r["path"] for r in disabled["files"] if r["source_path"] == "scripts/search-resource.py")
            with temporary_tree() as outside:
                process = subprocess.run([sys.executable, "-I", str(off / script), "--resource-id", "R-nature-reference",
                                          "--consumer", "nckh-write", "--domain", "scientific-writing", "--genre", "writing-advice",
                                          "--resource-access", "off"], cwd=outside, capture_output=True, text=True, timeout=30)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertIn('"resource_read": false', process.stdout)
            for row in enabled["skills"]:
                self.assertEqual((on / "skills" / row["id"] / "SKILL.md").read_bytes(),
                                 (off / "skills" / row["id"] / "SKILL.md").read_bytes())
            for field, value in [("format", "csv" if enabled["resources"][0]["format"] != "csv" else "json"),
                                 ("expected_artifact", "unsupported acceptance claim")]:
                broken = deepcopy(enabled)
                broken["resources"][0][field] = value
                atomic_json(on / "manifest.json", broken)
                with self.subTest(field=field), self.assertRaises(ContractError):
                    verify_bundle(on)
            broken = deepcopy(enabled)
            broken["resources"].pop()
            atomic_json(on / "manifest.json", broken)
            with self.assertRaises(ContractError):
                verify_bundle(on)
