from tests._lab import lab_root
import os
import stat
import subprocess
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from core import paths
from core.paths import contained, no_links, temporary_tree
from core.schema import ContractError

_PLAIN_DIRECTORY = SimpleNamespace(st_mode=stat.S_IFDIR | 0o755, st_reparse_tag=0)


class PathReparseTests(unittest.TestCase):
    def setUp(self):
        context = temporary_tree(lab_root())
        self.base = context.__enter__()
        self.addCleanup(context.__exit__, None, None, None)
        self.root = self.base / "root"
        self.outside = self.base / "outside"
        self.root.mkdir()
        self.outside.mkdir()
        (self.outside / "secret.txt").write_text("outside", encoding="utf-8")
        self.link = self.root / "link"

    def remove_link(self):
        if os.path.lexists(self.link):
            # rmdir/unlink drop the link itself and never touch the target.
            try:
                os.rmdir(self.link)
            except OSError:
                os.unlink(self.link)

    def assert_link_rejected(self):
        with self.assertRaisesRegex(ContractError, "linked path is not allowed"):
            contained(self.root, "link/secret.txt")
        with self.assertRaisesRegex(ContractError, "linked path is not allowed"):
            no_links(self.link)
        with self.assertRaisesRegex(ContractError, "linked path is not allowed"):
            contained(self.link, "secret.txt")
        self.assertTrue((self.outside / "secret.txt").is_file())

    @unittest.skipUnless(os.name == "nt", "directory junctions exist only on Windows")
    def test_junction_to_outside_root_rejected_by_contained(self):
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(self.link), str(self.outside)],
                                capture_output=True, text=True, timeout=30)
        self.addCleanup(self.remove_link)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.link / "secret.txt").is_file())
        self.assert_link_rejected()

    def test_symlink_to_outside_root_rejected_or_skipped_with_reason(self):
        try:
            os.symlink(self.outside, self.link, target_is_directory=True)
        except OSError as error:
            if getattr(error, "winerror", None) == 1314:
                self.skipTest("symlink creation needs SeCreateSymbolicLinkPrivilege (WinError 1314)")
            raise
        self.addCleanup(self.remove_link)
        self.assert_link_rejected()

    def lstat_with_tag(self, tagged, tag):
        def fake_lstat(current):
            if Path(current) == tagged:
                return SimpleNamespace(st_mode=stat.S_IFDIR | 0o755, st_reparse_tag=tag)
            return _PLAIN_DIRECTORY
        return patch.object(paths.os, "lstat", side_effect=fake_lstat)

    def test_name_surrogate_reparse_tags_rejected(self):
        tagged = Path(os.path.abspath(self.root / "tagged"))
        # Symlink, mount point (junction), WSL LX symlink.
        for tag in (0xA000000C, 0xA0000003, 0xA000001D):
            with self.subTest(tag=hex(tag)), self.lstat_with_tag(tagged, tag):
                with self.assertRaisesRegex(ContractError, "linked path is not allowed"):
                    contained(self.root, "tagged/file.txt")
                with self.assertRaisesRegex(ContractError, "linked path is not allowed"):
                    no_links(tagged)

    def test_non_surrogate_reparse_tag_allowed(self):
        tagged = Path(os.path.abspath(self.root / "tagged"))
        # Cloud files placeholder: the object stays at its own path.
        with self.lstat_with_tag(tagged, 0x9000001A):
            self.assertEqual(contained(self.root, "tagged/file.txt"), tagged / "file.txt")
            self.assertEqual(no_links(tagged), tagged)

    def test_contained_rejects_traversal_and_accepts_case_variant_root(self):
        for relative in ("../outside/secret.txt", "a/../../outside", "./a", "a//b", "",
                         "/abs", "a\\b", "C:/x", "a/."):
            with self.subTest(relative=relative), self.assertRaises(ContractError):
                contained(self.root, relative)
        variant = str(self.root).swapcase() if os.name == "nt" else str(self.root)
        target = contained(variant, "sub/file.txt")
        self.assertEqual(target, Path(os.path.abspath(variant)) / "sub" / "file.txt")
        self.assertEqual(os.path.normcase(target), os.path.normcase(self.root / "sub" / "file.txt"))


if __name__ == "__main__":
    unittest.main()
