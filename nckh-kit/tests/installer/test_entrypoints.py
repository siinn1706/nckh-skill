from tests._lab import lab_root
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
from unittest.mock import patch

from core.paths import atomic_json, temporary_tree
from tests._bundles import copy_bundle


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("nckh_installer_entry", ROOT / "installer/nckh-installer.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)


class EntrypointTests(unittest.TestCase):
    def test_shell_skips_unusable_first_interpreter_and_honors_override(self):
        shell = (Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Git/bin/bash.exe"
                 if os.name == "nt" else Path(shutil.which("sh") or "/bin/sh"))
        if not shell.is_file():
            self.skipTest("shell unavailable")
        with temporary_tree(lab_root()) as root:
            stub = root / "python3"
            stub.write_text("#!/bin/sh\nexit 2\n", encoding="utf-8")
            stub.chmod(0o755)
            environment = dict(os.environ)
            # Git Bash needs a POSIX PATH element; all other entries retain the host defaults.
            if os.name == "nt":
                shell_root = "/" + root.drive[0].lower() + root.as_posix()[2:]
                command = [str(shell), "-c", 'PATH="$1:$PATH"; export PATH; sh "$2" list-skills', "nckh-test", shell_root, str(ROOT / "installer/install.sh")]
            else:
                environment["PATH"] = str(root) + os.pathsep + environment.get("PATH", "")
                command = [str(shell), str(ROOT / "installer/install.sh"), "list-skills"]
            process = subprocess.run(command, capture_output=True, text=True, env=environment, timeout=30)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(len(json.loads(process.stdout)["skills"]), 43)
            self.assertIn("NCKH Python:", process.stderr)
            environment["NCKH_PYTHON"] = sys.executable
            process = subprocess.run(command, capture_output=True, text=True, env=environment, timeout=30)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertIn(sys.executable, process.stderr)

    def test_default_package_supports_repository_and_published_layout(self):
        with temporary_tree(lab_root()) as root:
            kit = root / "nckh-kit"
            kit.mkdir()
            package = root / "packages/codex"
            copy_bundle(package, "codex", ["core"], root=ROOT)
            with patch.object(entry, "ROOT", kit):
                self.assertEqual(entry.default_package(), root / "packages")
                shutil.copytree(package, kit / "dist/codex")
                self.assertEqual(entry.default_package(), kit / "dist")
                shutil.rmtree(root / "packages")
                self.assertEqual(entry.default_package(), kit / "dist")
                shutil.rmtree(kit / "dist")
                with self.assertRaisesRegex(entry.ContractError, "supply --package"):
                    entry.default_package()

    def test_no_arguments_returns_guidance_without_writes(self):
        with temporary_tree(lab_root()) as root:
            before = list(root.iterdir())
            stdout = io.StringIO()
            with redirect_stdout(stdout), patch.object(entry, "ROOT", root):
                self.assertEqual(entry.main([]), 2)
            self.assertIn("--help", stdout.getvalue())
            self.assertIn("list-skills", stdout.getvalue())
            self.assertIn("--dry-run", stdout.getvalue())
            self.assertEqual(list(root.iterdir()), before)

    def test_preview_rejects_tampered_default_bundle_before_any_project_write(self):
        with temporary_tree(lab_root()) as root:
            kit = root / "nckh-kit"
            kit.mkdir()
            package = root / "packages/codex"
            copy_bundle(package, "codex", ["core"], root=ROOT)
            project = root / "project"
            project.mkdir()
            skill = package / "skills/nckh-plan/SKILL.md"
            skill.write_bytes(skill.read_bytes() + b"\ntampered candidate\n")
            args = ["install", "--runtime", "codex-cli", "--scope", "project", "--project", str(project),
                    "--kits", "core", "--mode", "copy", "--models", "balanced", "--dry-run"]
            with patch.object(entry, "ROOT", kit), redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(entry.main(args), 4)
            self.assertEqual(list(project.iterdir()), [])

    def test_project_install_defaults_to_non_blocking_hooks_and_off_skips_them(self):
        with temporary_tree(lab_root()) as root:
            package = root / "package"
            copy_bundle(package / "codex", "codex", ["core"], root=ROOT)
            home = root / "home"
            home.mkdir()
            for setting in (None, "off"):
                project = root / ("default" if setting is None else "off")
                project.mkdir()
                args = ["install", "--package", str(package), "--runtime", "codex-cli", "--scope", "project",
                        "--project", str(project), "--home", str(home), "--kits", "core", "--mode", "copy",
                        "--models", "balanced"]
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

    def test_global_advisory_hooks_rejected_before_visibility_scan(self):
        with temporary_tree(lab_root()) as root:
            home = root / "home"
            (home / ".agents/skills/nckh-plan").mkdir(parents=True)
            (root / ".agents/skills/nckh-plan").mkdir(parents=True)
            before = sorted(path.relative_to(root) for path in root.rglob("*"))
            args = ["install", "--package", str(root / "package"), "--runtime", "codex-cli", "--scope", "global",
                    "--home", str(home), "--kits", "core", "--mode", "copy", "--models", "balanced"]
            for extra in (["--dry-run"], ["--yes"], ["--dry-run", "--hooks", "advisory"]):
                with self.subTest(extra=extra):
                    stderr = io.StringIO()
                    with (patch.object(entry, "inspect_target_paths", side_effect=AssertionError("scanned targets")),
                          patch.object(entry, "plan_install", side_effect=AssertionError("scanned visibility")),
                          redirect_stdout(io.StringIO()), redirect_stderr(stderr)):
                        self.assertEqual(entry.main(args + extra), 4)
                    self.assertIn("automatic hooks require project scope", stderr.getvalue())
                    self.assertNotIn("duplicate visibility", stderr.getvalue())
            self.assertEqual(sorted(path.relative_to(root) for path in root.rglob("*")), before)

    def test_doctor_and_uninstall_accept_explicit_state_without_scope(self):
        with temporary_tree(lab_root()) as root:
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
                        self.assertEqual(json.loads(wrapped.stderr.splitlines()[-1]), json.loads(direct.stderr))
                    else:
                        self.assertEqual(json.loads(wrapped.stdout), json.loads(direct.stdout))
