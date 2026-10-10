import os
import unittest
from pathlib import Path
from unittest.mock import patch

from core.paths import temporary_tree
from core.schema import ContractError
import tests._lab as lab
from tests._lab import assert_clean_ancestors, lab_root


class LabTests(unittest.TestCase):
    def test_dirty_ancestor_fails_with_actionable_override(self):
        with temporary_tree(lab_root()) as root:
            skill = root / ".cursor/skills/nckh-plan"
            skill.mkdir(parents=True)
            with self.assertRaisesRegex(ContractError, "NCKH_TEST_ROOT"):
                assert_clean_ancestors(root / "project")

    def test_override_is_validated_and_temporary_tree_inherits_it(self):
        with temporary_tree(lab_root()) as root:
            with patch.dict(os.environ, {"NCKH_TEST_ROOT": str(root)}):
                self.assertEqual(lab_root(), root)
                with temporary_tree() as child:
                    self.assertEqual(child.parent, root)
            self.assertEqual(list(root.iterdir()), [])

    def test_unwritable_candidate_falls_back_with_reason(self):
        real_touch = Path.touch
        with temporary_tree(lab_root()) as root:
            first, second = root / "first", root / "second"

            def touch(path, *args, **kwargs):
                if path.parent == first:
                    raise PermissionError(13, "injected denial", str(path))
                return real_touch(path, *args, **kwargs)

            environ = {key: value for key, value in os.environ.items() if key != "NCKH_TEST_ROOT"}
            with patch.dict(os.environ, environ, clear=True), patch.object(lab, "_selected", None),                     patch.object(lab, "_candidates", return_value=[first, second]), patch.object(Path, "touch", touch):
                self.assertEqual(lab_root(), second)
                self.assertEqual(lab._selected, second)
            self.assertEqual(list(second.iterdir()), [])
            with patch.dict(os.environ, environ, clear=True), patch.object(lab, "_selected", None),                     patch.object(lab, "_candidates", return_value=[first]), patch.object(Path, "touch", touch):
                with self.assertRaises(ContractError) as raised:
                    lab_root()
            self.assertIn(str(first), str(raised.exception))
            self.assertIn("injected denial", str(raised.exception))
            self.assertIn("NCKH_TEST_ROOT", str(raised.exception))

    def test_unwritable_override_fails_before_tests(self):
        with temporary_tree(lab_root()) as root:
            override = root / "override"
            with patch.dict(os.environ, {"NCKH_TEST_ROOT": str(override)}),                     patch.object(Path, "touch", side_effect=PermissionError(13, "injected denial")):
                with self.assertRaises(ContractError) as raised:
                    lab_root()
            message = str(raised.exception)
            self.assertIn(str(override), message)
            self.assertIn("NCKH_TEST_ROOT", message)
            self.assertEqual(list(override.iterdir()), [])
