import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from core.paths import atomic_json, temporary_tree
from core.build import build_host


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("nckh_installer_entry", ROOT / "installer/nckh-installer.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)


class EntrypointTests(unittest.TestCase):
    def test_project_install_defaults_to_non_blocking_hooks_and_off_skips_them(self):
        with temporary_tree() as root:
            package = root / "package"
            build_host(ROOT, "codex", ["core"], package / "codex")
            for setting in (None, "off"):
                project = root / ("default" if setting is None else "off")
                project.mkdir()
                args = ["install", "--package", str(package), "--runtime", "codex-cli", "--scope", "project",
                        "--project", str(project), "--kits", "core", "--mode", "copy", "--models", "balanced"]
                if setting:
                    args.extend(["--hooks", setting])
                stdout, stderr = io.StringIO(), io.StringIO()
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    code = entry.main(args + ["--dry-run"])
                self.assertEqual(code, 0, stderr.getvalue())
                self.assertEqual(list(project.iterdir()), [])
                stdout, stderr = io.StringIO(), io.StringIO()
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    code = entry.main(args + ["--yes"])
                self.assertEqual(code, 0, stderr.getvalue() + stdout.getvalue())
                config = project / ".codex/hooks.json"
                if setting == "off":
                    self.assertFalse(config.exists())
                else:
                    record = json.loads(config.read_text())
                    self.assertIn("PreToolUse", record["hooks"])
                    self.assertIn("PostToolUse", record["hooks"])
                    self.assertIn("--mode advisory", json.dumps(record))
                    self.assertEqual(json.loads(stdout.getvalue())["hooks"][0]["mode"], "advisory")

    def test_doctor_and_uninstall_accept_explicit_state_without_scope(self):
        with temporary_tree() as root:
            state = root / "Trạng thái có spaces"
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = entry.main(["doctor", "--state-dir", str(state)])
            self.assertEqual(code, 0, stderr.getvalue())
            self.assertEqual(json.loads(stdout.getvalue())["status"], "read-only")
            self.assertFalse(state.exists())

            index = {"schema_version": 1, "items": {}, "policies": {},
                     "installs": {"owned-fixture": {"roots": []}}}
            atomic_json(state / "ownership.json", index)
            before = (state / "ownership.json").read_bytes()
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = entry.main(["uninstall", "--state-dir", str(state), "--install-id", "owned-fixture", "--dry-run"])
            self.assertEqual(code, 0, stderr.getvalue())
            self.assertEqual(json.loads(stdout.getvalue()), {"status": "preview", "actions": []})
            self.assertEqual((state / "ownership.json").read_bytes(), before)
            self.assertEqual({path.name for path in state.iterdir()}, {"ownership.json"})

    @unittest.skipUnless(os.name == "nt", "PowerShell entrypoint evidence requires Windows")
    def test_powershell_forwards_help_json_and_exit_status(self):
        shells = [command for name in ["powershell", "pwsh"] if (command := shutil.which(name))]
        self.assertTrue(shells, "Windows entrypoint verification needs PowerShell")
        engine = [sys.executable, str(ROOT / "installer/nckh-installer.py")]
        for shell in shells:
            wrapper = [shell, "-NoProfile", "-NonInteractive", "-File", str(ROOT / "installer/install.ps1")]
            for arguments in [["--help"], ["list-skills"], ["doctor"]]:
                with self.subTest(shell=Path(shell).name, arguments=arguments):
                    direct = subprocess.run(engine + arguments, cwd=ROOT, capture_output=True, text=True, timeout=30)
                    wrapped = subprocess.run(wrapper + arguments, cwd=ROOT, capture_output=True, text=True, timeout=30)
                    self.assertEqual(wrapped.returncode, direct.returncode, wrapped.stderr)
                    if arguments == ["--help"]:
                        self.assertEqual(wrapped.stdout, direct.stdout)
                    elif direct.returncode:
                        self.assertEqual(json.loads(wrapped.stderr), json.loads(direct.stderr))
                    else:
                        self.assertEqual(json.loads(wrapped.stdout), json.loads(direct.stdout))
