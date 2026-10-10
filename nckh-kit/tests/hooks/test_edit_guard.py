from tests._lab import lab_root
import json
import os
import subprocess
import time
import unittest

from core import edit_guard
from core.edit_guard import (MAX_PER_SESSION, MAX_SNAPSHOT_BYTES, SNAPSHOT_ROOT, STALE_SECONDS,
                             advice_text, compare, snapshot)
from core.hook_policy import MAX_PATHS as POLICY_MAX_PATHS
from core.paths import digest_record, temporary_tree
from core.schema import ContractError


HOST = "claude"
SESSION = digest_record("edit-guard-session")
OTHER = digest_record("edit-guard-other-session")


def session_dir(project, session=SESSION, host=HOST):
    return project / SNAPSHOT_ROOT / host / session[:16]


class EditGuardTests(unittest.TestCase):
    def setUp(self):
        self._tree = temporary_tree(lab_root())
        self.project = self._tree.__enter__()
        self.addCleanup(self._tree.__exit__, None, None, None)

    def write(self, relative, data):
        path = self.project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def edit(self, relative, before, after):
        self.write(relative, before)
        snapshot(self.project, HOST, SESSION, [relative])
        self.write(relative, after)
        return compare(self.project, HOST, SESSION, [relative])

    def test_crlf_to_lf_reported(self):
        findings = self.edit("writing.txt", b"a\r\nb\r\n", b"a\nb\nc\n")
        self.assertEqual(findings, [{"path": "writing.txt", "eol_before": "crlf", "eol_after": "lf",
                                     "bom_before": "none", "bom_after": "none"}])
        text = advice_text(findings)
        self.assertIn("writing.txt was crlf/no BOM before this edit and is now lf.", text)
        self.assertTrue(text.startswith("nckh EOL/BOM guard (advisory): "))
        self.assertIn("check-receipt.py inventory", text)

    def test_bom_loss_reported(self):
        findings = self.edit("bom.md", b"\xef\xbb\xbfx\r\n", b"y\r\n")
        self.assertEqual(findings[0]["bom_before"], "utf-8")
        self.assertEqual(findings[0]["bom_after"], "none")
        self.assertIn("bom.md was crlf/utf-8 BOM before this edit and is now no BOM", advice_text(findings))

    def test_bom_added_reported(self):
        findings = self.edit("plain.md", b"x\n", b"\xef\xbb\xbfx\r\n")
        self.assertEqual((findings[0]["bom_after"], findings[0]["eol_after"]), ("utf-8", "crlf"))
        self.assertIn("is now crlf/utf-8 BOM", advice_text(findings))

    def test_unchanged_eol_no_finding(self):
        self.assertEqual(self.edit("same.txt", b"a\r\n", b"different content\r\nmore\r\n"), [])
        self.assertEqual(advice_text([]), "")

    def test_new_file_no_finding(self):
        records = snapshot(self.project, HOST, SESSION, ["new.txt"])
        self.assertEqual(records[0]["exists"], False)
        self.write("new.txt", b"a\n")
        self.assertEqual(compare(self.project, HOST, SESSION, ["new.txt"]), [])

    def test_deleted_file_no_finding(self):
        path = self.write("gone.txt", b"a\r\n")
        snapshot(self.project, HOST, SESSION, ["gone.txt"])
        path.unlink()
        self.assertEqual(compare(self.project, HOST, SESSION, ["gone.txt"]), [])
        self.assertEqual(list(session_dir(self.project).iterdir()), [])

    def test_too_large_skipped(self):
        path = self.write("large.bin", b"")
        with open(path, "wb") as stream:
            stream.truncate(MAX_SNAPSHOT_BYTES + 1)
        records = snapshot(self.project, HOST, SESSION, ["large.bin"])
        self.assertEqual(records[0]["skipped"], "too-large")
        self.write("large.bin", b"a\r\n")
        self.assertEqual(compare(self.project, HOST, SESSION, ["large.bin"]), [])

    def test_snapshot_at_size_limit_is_recorded_quickly(self):
        self.write("limit.txt", b"line\r\n" * (MAX_SNAPSHOT_BYTES // 6))
        started = time.perf_counter()
        records = snapshot(self.project, HOST, SESSION, ["limit.txt"])
        elapsed = time.perf_counter() - started
        self.assertEqual((records[0]["exists"], records[0]["eol"]), (True, "crlf"))
        self.assertLess(elapsed, 2.0)

    def test_snapshot_consumed_after_compare(self):
        self.write("a.txt", b"a\n")
        snapshot(self.project, HOST, SESSION, ["a.txt"])
        stored = list(session_dir(self.project).iterdir())
        self.assertEqual(len(stored), 1)
        record = json.loads(stored[0].read_text(encoding="utf8"))
        self.assertEqual(set(record), {"path", "exists", "sha256", "eol", "bom", "size", "taken_at"})
        self.assertEqual(compare(self.project, HOST, SESSION, ["a.txt"]), [])
        self.assertEqual(list(session_dir(self.project).iterdir()), [])
        self.write("a.txt", b"a\r\n")
        self.assertEqual(compare(self.project, HOST, SESSION, ["a.txt"]), [])

    def test_per_session_cap_evicts_oldest(self):
        names = [f"f{index:03}.txt" for index in range(MAX_PER_SESSION + 2)]
        for name in names:
            self.write(name, b"x\r\n")
        for index, name in enumerate(names):
            snapshot(self.project, HOST, SESSION, [name], now=1_000_000 + index)
        self.assertEqual(len(list(session_dir(self.project).iterdir())), MAX_PER_SESSION)
        for name in names:
            self.write(name, b"x\n")
        self.assertEqual(compare(self.project, HOST, SESSION, names[:2]), [])
        self.assertEqual(len(compare(self.project, HOST, SESSION, names[2:4])), 2)

    def test_stale_sessions_pruned(self):
        self.write("a.txt", b"a\n")
        now = 2_000_000_000.0
        old = now - STALE_SECONDS - 60
        snapshot(self.project, HOST, OTHER, ["a.txt"], now=old)
        stale = session_dir(self.project, OTHER)
        os.utime(stale, (old, old))
        fresh_key = digest_record("edit-guard-fresh-session")
        snapshot(self.project, HOST, fresh_key, ["a.txt"], now=now - 60)
        fresh = session_dir(self.project, fresh_key)
        os.utime(fresh, (old, old))
        snapshot(self.project, HOST, SESSION, ["a.txt"], now=now)
        self.assertFalse(stale.exists())
        self.assertTrue(fresh.exists())
        self.assertTrue(session_dir(self.project).exists())

    def test_prune_keeps_foreign_files(self):
        self.write("a.txt", b"a\n")
        now = 2_000_000_000.0
        old = now - STALE_SECONDS - 60
        snapshot(self.project, HOST, OTHER, ["a.txt"], now=old)
        stale = session_dir(self.project, OTHER)
        (stale / "keep.txt").write_bytes(b"not a snapshot")
        os.utime(stale, (old, old))
        snapshot(self.project, HOST, SESSION, ["a.txt"], now=now)
        self.assertEqual([path.name for path in stale.iterdir()], ["keep.txt"])

    def stale_session(self, label, old):
        key = digest_record(label)
        snapshot(self.project, HOST, key, ["a.txt"], now=old)
        directory = session_dir(self.project, key)
        return directory

    def test_prune_removes_stale_temporaries_of_atomic_writes(self):
        self.write("a.txt", b"a\n")
        now = 2_000_000_000.0
        old = now - STALE_SECONDS - 60
        stale = self.stale_session("killed-writer", old)
        leftover, recent = stale / ".nckh-k3x_9q2z", stale / ".nckh-ab12cd34"
        leftover.write_bytes(b"{")
        os.utime(leftover, (old, old))
        os.utime(stale, (old, old))
        snapshot(self.project, HOST, SESSION, ["a.txt"], now=now)
        self.assertFalse(stale.exists())
        # A temporary younger than the stale age may still belong to a live writer.
        stale = self.stale_session("live-writer", old)
        (stale / recent.name).write_bytes(b"{")
        os.utime(stale / recent.name, (now - 60, now - 60))
        os.utime(stale, (old, old))
        snapshot(self.project, HOST, SESSION, ["a.txt"], now=now)
        self.assertEqual([path.name for path in stale.iterdir()], [recent.name])

    def test_prune_not_starved_by_unremovable_sessions(self):
        self.write("a.txt", b"a\n")
        now = 2_000_000_000.0
        old = now - STALE_SECONDS - 3600
        for index in range(edit_guard.MAX_PRUNE_SESSIONS + 2):
            stuck = self.stale_session(f"foreign-{index}", old)
            (stuck / "keep.txt").write_bytes(b"not a snapshot")
            os.utime(stuck, (old - 60, old - 60))
        removable = self.stale_session("removable", old)
        os.utime(removable, (old, old))
        snapshot(self.project, HOST, SESSION, ["a.txt"], now=now)
        self.assertFalse(removable.exists())

    def test_discard_drops_snapshot_without_writing_state(self):
        self.write("a.txt", b"a\n")
        snapshot(self.project, HOST, SESSION, ["a.txt"])
        edit_guard.discard(self.project, HOST, SESSION, ["a.txt"])
        self.assertEqual(list(session_dir(self.project).iterdir()), [])
        edit_guard.discard(self.project, HOST, OTHER, ["a.txt", "new.txt"])
        self.assertFalse(session_dir(self.project, OTHER).exists())
        with self.assertRaises(ContractError):
            edit_guard.discard(self.project, HOST, SESSION, ["../outside.txt"])

    def test_path_escape_rejected(self):
        for path in ("../outside.txt", "/abs.txt", "C:/x.txt", "a\\b.txt", "./a.txt", ""):
            with self.subTest(path=path), self.assertRaises(ContractError):
                snapshot(self.project, HOST, SESSION, [path])
            with self.subTest(path=path, phase="compare"), self.assertRaises(ContractError):
                compare(self.project, HOST, SESSION, [path])
        with self.assertRaises(ContractError):
            snapshot(self.project, "../claude", SESSION, ["a.txt"])
        with self.assertRaises(ContractError):
            snapshot(self.project, HOST, "../" + SESSION[3:], ["a.txt"])
        with self.assertRaises(ContractError):
            snapshot(self.project, HOST, SESSION, [f"p{index}.txt" for index in range(POLICY_MAX_PATHS + 1)])
        self.assertFalse((self.project / ".nckh-state").exists())

    def test_link_not_followed(self):
        outside = self.write("outside/target.txt", b"a\r\n")
        try:
            os.symlink(outside, self.project / "link.txt")
            relative = "link.txt"
        except OSError:
            if os.name != "nt":
                raise
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(self.project / "linkdir"),
                                     str(outside.parent)], capture_output=True)
            if result.returncode:
                self.skipTest("host cannot create a symlink or junction fixture")
            relative = "linkdir/target.txt"
        self.assertEqual(snapshot(self.project, HOST, SESSION, [relative]), [])
        outside.write_bytes(b"a\n")
        self.assertEqual(compare(self.project, HOST, SESSION, [relative]), [])
        self.assertEqual(outside.read_bytes(), b"a\n")

    def test_unicode_path_vietnamese(self):
        relative = "bài viết/Tiếng Việt có dấu.md"
        findings = self.edit(relative, "xin chào\r\n".encode("utf8"), "xin chào\n".encode("utf8"))
        self.assertEqual(findings[0]["path"], relative)
        self.assertIn(relative, advice_text(findings))

    def test_mixed_eol_profile_reported_as_mixed(self):
        findings = self.edit("mixed.txt", b"a\r\nb\r\n", b"a\r\nb\nc\n")
        self.assertEqual((findings[0]["eol_before"], findings[0]["eol_after"]), ("crlf", "mixed"))

    def test_advice_lists_at_most_three_files(self):
        findings = [{"path": f"f{index}.txt", "eol_before": "crlf", "eol_after": "lf",
                     "bom_before": "none", "bom_after": "none"} for index in range(5)]
        text = advice_text(findings)
        self.assertIn("f2.txt", text)
        self.assertNotIn("f3.txt", text)
        self.assertIn("2 more file(s)", text)

    def test_path_limit_matches_hook_policy(self):
        self.assertEqual(edit_guard.MAX_PATHS, POLICY_MAX_PATHS)


if __name__ == "__main__":
    unittest.main()
