from tests._lab import lab_root
import json
import os
import stat
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from core import install
from core.install import (acknowledgeable_visibility, inspect_target_paths, linked_directory,
                          nested_visibility_roots, refresh_targets, visibility_conflicts)
from core.paths import temporary_tree

ROOT = Path(__file__).resolve().parents[2]
SURFACE, HOST = "codex-cli", "codex"
ADAPTER = json.loads((ROOT / "adapters" / HOST / "adapter.json").read_text(encoding="utf-8"))
GLOBAL_ROOT = ADAPTER["surfaces"][SURFACE]["global"]
PROJECT_ROOT = ADAPTER["surfaces"][SURFACE]["project"]
CLOUD_TAG = 0x9000701A  # IO_REPARSE_TAG_CLOUD_7: no name-surrogate bit
MOUNT_POINT_TAG = 0xA0000003  # IO_REPARSE_TAG_MOUNT_POINT (junction): name surrogate


def project_target(project, home=None):
    target = {"surface": SURFACE, "host": HOST, "adapter": ADAPTER, "base": str(project),
              "root": str(project / PROJECT_ROOT)}
    if home is not None:
        target["home"] = str(home)
    return target


def sources(conflict):
    return {row["path"]: row["source"] for row in conflict["sources"]}


class VisibilityHomeTests(unittest.TestCase):
    def setUp(self):
        self.tree = temporary_tree(lab_root())
        self.root = self.tree.__enter__()
        self.addCleanup(self.tree.__exit__, None, None, None)
        self.project = self.root / "work" / "proj"
        self.project.mkdir(parents=True)
        self.home = self.root / "home"
        self.home.mkdir()

    def home_copy(self, home=None):
        path = (home or self.home) / GLOBAL_ROOT / "nckh-plan"
        path.mkdir(parents=True)
        return path

    def test_project_outside_home_sees_home_level_root_as_global(self):
        copy = self.home_copy()
        [conflict] = visibility_conflicts([project_target(self.project, self.home)], {"nckh-plan"}, scope="project")
        self.assertEqual(sources(conflict), {str(self.project / PROJECT_ROOT / "nckh-plan"): "destination",
                                             str(copy): "global"})
        self.assertEqual(visibility_conflicts([project_target(self.project, self.home)], {"nckh-other"},
                                              scope="project"), [])

    def test_home_level_conflict_acknowledgeable(self):
        self.home_copy()
        nested = self.project / "child" / PROJECT_ROOT / "nckh-plan"
        [conflict] = visibility_conflicts([project_target(self.project, self.home)], {"nckh-plan"}, scope="project")
        self.assertTrue(acknowledgeable_visibility(conflict))
        nested.mkdir(parents=True)
        [conflict] = visibility_conflicts([project_target(self.project, self.home)], {"nckh-plan"}, scope="project")
        self.assertEqual(sorted(sources(conflict).values()), ["destination", "global", "nested"])
        self.assertFalse(acknowledgeable_visibility(conflict))

    def test_project_inside_home_unchanged(self):
        home = self.root / "work"
        copy = self.home_copy(home)
        ancestor = self.root / GLOBAL_ROOT / "nckh-plan"
        ancestor.mkdir(parents=True)
        recorded = visibility_conflicts([project_target(self.project, home)], {"nckh-plan"}, scope="project")
        with mock.patch.object(Path, "home", return_value=home):
            legacy = visibility_conflicts([project_target(self.project)], {"nckh-plan"}, scope="project")
        self.assertEqual(recorded, legacy)
        self.assertEqual(sources(recorded[0]), {str(self.project / PROJECT_ROOT / "nckh-plan"): "destination",
                                                str(copy): "global", str(ancestor): "ancestor"})

    def test_target_without_home_falls_back(self):
        # A target recorded before home was stored classifies by Path.home() and
        # keeps the earlier ancestry-only scan.
        copy = self.home_copy(self.root)
        with mock.patch.object(Path, "home", return_value=self.root):
            [conflict] = visibility_conflicts([project_target(self.project)], {"nckh-plan"}, scope="project")
        self.assertEqual(sources(conflict)[str(copy)], "global")
        self.home_copy()
        with mock.patch.object(Path, "home", return_value=self.home):
            [conflict] = visibility_conflicts([project_target(self.project)], {"nckh-plan"}, scope="project")
        self.assertEqual(sources(conflict)[str(copy)], "ancestor")
        self.assertNotIn(str(self.home / GLOBAL_ROOT / "nckh-plan"), sources(conflict))

    def test_target_paths_record_and_refresh_home(self):
        bundle = self.root / "bundle"
        bundle.mkdir()
        (bundle / "manifest.json").write_text("{}", encoding="utf-8")
        (bundle / "adapter.json").write_text(json.dumps(ADAPTER), encoding="utf-8")
        [target] = inspect_target_paths(bundle, [SURFACE], scope="project", project=self.project, home=self.home)
        self.assertEqual(target["home"], str(self.home))
        with mock.patch.object(install, "verify_bundle", return_value={"host": HOST}):
            [refreshed] = refresh_targets([target], "project")
            self.assertEqual(refreshed["home"], str(self.home))
            legacy = {key: value for key, value in target.items() if key != "home"}
            [refreshed] = refresh_targets([legacy], "project")
            self.assertNotIn("home", refreshed)

    def linked_home(self):
        """Patch no_links so the home directory reports a link-like component."""
        real = install.no_links
        home = self.home

        def no_links(path):
            if Path(path) == home or home in Path(path).parents:
                raise install.ContractError(f"linked path is not allowed: {home}")
            return real(path)
        return mock.patch.object(install, "no_links", side_effect=no_links)

    def bundle(self):
        bundle = self.root / "bundle"
        bundle.mkdir()
        (bundle / "manifest.json").write_text("{}", encoding="utf-8")
        (bundle / "adapter.json").write_text(json.dumps(ADAPTER), encoding="utf-8")
        return bundle

    def test_linked_home_falls_back_to_legacy_scan_for_project_install(self):
        bundle = self.bundle()
        with self.linked_home(), self.assertWarnsRegex(UserWarning, "home directory .*linked path is not allowed"):
            [target] = inspect_target_paths(bundle, [SURFACE], scope="project", project=self.project, home=self.home)
        self.assertNotIn("home", target)
        self.assertEqual(target["base"], str(self.project))
        recorded = dict(target, home=str(self.home))
        with mock.patch.object(install, "verify_bundle", return_value={"host": HOST}), self.linked_home(),                 self.assertWarnsRegex(UserWarning, "home directory"):
            [refreshed] = refresh_targets([recorded], "project")
        self.assertNotIn("home", refreshed)

    def test_global_install_does_not_record_home(self):
        bundle = self.bundle()
        [target] = inspect_target_paths(bundle, [SURFACE], scope="global", project=self.project, home=self.home)
        self.assertNotIn("home", target)
        self.assertEqual(target["base"], str(self.home))

    def test_cloud_placeholder_directory_traversed(self):
        placeholder = self.project / "OneDrive"
        nested = placeholder / "child" / PROJECT_ROOT
        nested.mkdir(parents=True)
        real_lstat = os.lstat

        def fake_lstat(tag):
            def lstat(path, *args, **kwargs):
                if Path(path) == placeholder:
                    return SimpleNamespace(st_mode=stat.S_IFDIR | 0o755, st_reparse_tag=tag,
                                           st_file_attributes=getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))
                return real_lstat(path, *args, **kwargs)
            return lstat

        with mock.patch.object(install.os, "lstat", side_effect=fake_lstat(CLOUD_TAG)):
            self.assertFalse(linked_directory(placeholder))
            self.assertIn(nested, list(nested_visibility_roots(self.project, [PROJECT_ROOT])))
        with mock.patch.object(install.os, "lstat", side_effect=fake_lstat(MOUNT_POINT_TAG)):
            self.assertTrue(linked_directory(placeholder))
            self.assertNotIn(nested, list(nested_visibility_roots(self.project, [PROJECT_ROOT])))


if __name__ == "__main__":
    unittest.main()
