"""Synthetic receipt fixtures test integrity only, never native qualification."""

import copy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

from core.build import closure
from core.paths import digest_file, temporary_tree
from core.schema import ContractError as CoreContractError, validate_record


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("visual_binding_checker", ROOT / "scripts/check-visual-engine.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
ContractError = checker.ContractError


class VisualEngineBindingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = temporary_tree()
        self.project = self.temporary.__enter__()
        self.addCleanup(self.temporary.__exit__, None, None, None)
        self.executable = Path(sys.executable).resolve()
        self.write("probe/input.svg", b'<svg xmlns="http://www.w3.org/2000/svg"><text>Fixture</text></svg>')
        self.write("probe/render.png", checker.PNG_SIGNATURE + b"synthetic-integrity-fixture")
        self.write("probe/version.stdout", b"synthetic renderer 1\n")
        for name in ("version.stderr", "render.stdout", "render.stderr"):
            self.write("probe/" + name, b"")
        self.engine = {"executable": str(self.executable), "sha256": digest_file(self.executable),
                       "version": "synthetic renderer 1"}
        self.version_receipt = self.receipt([str(self.executable), "--version"], "version")
        self.render_receipt = self.receipt([str(self.executable), "-o", "probe/render.png", "probe/input.svg"], "render")
        self.render_receipt.update(input_sha256=digest_file(self.project / "probe/input.svg"),
                                   render_sha256=digest_file(self.project / "probe/render.png"))
        self.write_json("probe/version.json", self.version_receipt)
        self.write_json("probe/render.json", self.render_receipt)
        self.binding = {
            "schema_version": 1,
            "scope": {"project_root": str(self.project), "task_id": "chart-task", "host": "codex"},
            "format": "svg", "engine": self.engine, "capabilities": ["svg-render"],
            "observations": {"version_receipt": self.ref("probe/version.json"),
                             "render_receipt": self.ref("probe/render.json"),
                             "input_svg": self.ref("probe/input.svg"),
                             "render_png": self.ref("probe/render.png")},
        }
        self.save_binding()

    def write(self, relative, data):
        path = self.project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def write_json(self, relative, value):
        self.write(relative, json.dumps(value, ensure_ascii=False).encode("utf-8"))

    def ref(self, relative):
        return {"path": relative, "sha256": digest_file(self.project / relative)}

    def receipt(self, command, name):
        return {"command": command, "exit_status": 0, "executable_sha256": self.engine["sha256"],
                "version": self.engine["version"], "stdout": self.ref(f"probe/{name}.stdout"),
                "stderr": self.ref(f"probe/{name}.stderr"), "status": "completed-unreviewed",
                "cleanup": "owned-process-group-closed"}

    def save_binding(self):
        self.write_json("probe/binding.json", self.binding)

    def save_receipt(self, name, receipt):
        self.write_json(f"probe/{name}.json", receipt)
        self.binding["observations"][name + "_receipt"] = self.ref(f"probe/{name}.json")
        self.save_binding()

    def check(self, **kwargs):
        options = {"project": str(self.project), "task": "chart-task", "host": "codex",
                   "binding": "probe/binding.json", "capability": "svg-render"}
        options.update(kwargs)
        return checker.check_binding(**options)

    def test_default_extension_is_unavailable_and_route_is_closed(self):
        record = json.loads((ROOT / "extensions/native-documents/contract.json").read_text())
        validate_record("extension", record)
        self.assertEqual(record["status"], "unavailable")
        self.assertIsNone(record["engine_binding"])
        changed = copy.deepcopy(record)
        changed["runtime_binding"]["certified"] = True
        with self.assertRaises(CoreContractError):
            validate_record("extension", changed)

    def test_valid_binding_reports_integrity_without_authority_or_global_promotion(self):
        result = self.check()
        self.assertEqual(result["status"], "integrity-verified")
        self.assertEqual(result["global_status"], "unavailable")
        self.assertEqual(result["authorization"], "not-established-by-checker")
        self.assertEqual(result["acceptance"], "pending-independent-gates")

    def test_project_task_and_host_mismatches_fail(self):
        for field, value in [("task", "another-task"), ("host", "cursor")]:
            with self.subTest(field=field), self.assertRaises(ContractError):
                self.check(**{field: value})
        self.binding["scope"]["project_root"] = str(self.project.parent)
        self.save_binding()
        with self.assertRaises(ContractError):
            self.check()

    def test_missing_duplicate_and_unsupported_capabilities_fail(self):
        for value in [[], ["svg-render", "svg-render"], ["native-editability"], ["svg-render", "publish"]]:
            with self.subTest(capabilities=value):
                self.binding["capabilities"] = value
                self.save_binding()
                with self.assertRaises(ContractError):
                    self.check()
        with self.assertRaises(ContractError):
            self.check(capability="publish")

    def test_unknown_fields_boolean_version_and_duplicate_json_keys_fail(self):
        original = copy.deepcopy(self.binding)
        for change in [{"certified": True}, {"schema_version": True}]:
            self.binding = {**copy.deepcopy(original), **change}
            self.save_binding()
            with self.assertRaises(ContractError):
                self.check()
        self.write("probe/binding.json", b'{"schema_version":1,"schema_version":1}')
        with self.assertRaises(ContractError):
            self.check()

    def test_missing_observations_and_hash_drift_fail(self):
        for key in self.binding["observations"]:
            with self.subTest(observation=key):
                original = self.binding["observations"][key]["sha256"]
                self.binding["observations"][key]["sha256"] = "0" * 64
                self.save_binding()
                with self.assertRaises(ContractError):
                    self.check()
                self.binding["observations"][key]["sha256"] = original
        del self.binding["observations"]["render_receipt"]
        self.save_binding()
        with self.assertRaises(ContractError):
            self.check()

    def test_executable_missing_hash_drift_and_relative_path_fail(self):
        for change in [{"sha256": "0" * 64}, {"executable": "python"},
                       {"executable": str(self.project / "missing.exe")}]:
            with self.subTest(change=change):
                self.binding["engine"] = {**self.engine, **change}
                self.save_binding()
                with self.assertRaises(ContractError):
                    self.check()

    def test_receipt_engine_version_exit_and_cleanup_mismatches_fail(self):
        for change in [{"version": "another version"}, {"executable_sha256": "0" * 64},
                       {"command": [str(self.project / "missing.exe"), "--version"]},
                       {"exit_status": 1}, {"exit_status": False}, {"cleanup": "unknown"},
                       {"status": "observed"}, {"certified": True}]:
            with self.subTest(change=change):
                receipt = {**copy.deepcopy(self.version_receipt), **change}
                self.save_receipt("version", receipt)
                with self.assertRaises(ContractError):
                    self.check()

    def test_version_stdout_and_log_hashes_must_match(self):
        self.write("probe/version.stdout", b"another version\n")
        with self.assertRaises(ContractError):
            self.check()
        self.version_receipt["stdout"] = self.ref("probe/version.stdout")
        self.save_receipt("version", self.version_receipt)
        with self.assertRaises(ContractError):
            self.check()

    def test_receipt_input_output_hash_and_command_mismatches_fail(self):
        self.write("probe/another.svg", b"<svg />")
        for change in [{"input_sha256": "0" * 64}, {"render_sha256": "0" * 64},
                       {"command": [str(self.executable), "-o", "probe/render.png", "probe/another.svg"]},
                       {"command": [str(self.executable), "--output=probe/render.png", "--unknown", "probe/input.svg"]},
                       {"command": [str(self.executable), "-o", "probe/render.png", "-o", "probe/render.png", "probe/input.svg"]}]:
            with self.subTest(change=change):
                self.save_receipt("render", {**copy.deepcopy(self.render_receipt), **change})
                with self.assertRaises(ContractError):
                    self.check()

    def test_svg_and_png_content_are_checked_after_hashes_match(self):
        self.write("probe/input.svg", b"<html />")
        self.binding["observations"]["input_svg"] = self.ref("probe/input.svg")
        self.save_binding()
        with self.assertRaises(ContractError):
            self.check()
        self.write("probe/input.svg", b"<svg />")
        self.binding["observations"]["input_svg"] = self.ref("probe/input.svg")
        self.write("probe/render.png", b"not a PNG")
        self.binding["observations"]["render_png"] = self.ref("probe/render.png")
        self.save_binding()
        with self.assertRaises(ContractError):
            self.check()

    def test_reference_traversal_absolute_and_alternate_separator_fail(self):
        for relative in ["../escape.json", str(self.project / "probe/version.json"),
                         "probe\\version.json", "probe/./version.json", "probe//version.json"]:
            with self.subTest(path=relative):
                self.binding["observations"]["version_receipt"]["path"] = relative
                self.save_binding()
                with self.assertRaises(ContractError):
                    self.check()

    def test_command_operands_cannot_escape_project(self):
        for operand in ["../outside.svg", str(self.executable)]:
            with self.subTest(operand=operand):
                changed = copy.deepcopy(self.render_receipt)
                changed["command"][-1] = operand
                self.save_receipt("render", changed)
                with self.assertRaises(ContractError):
                    self.check()

    def test_symlink_observation_is_rejected(self):
        target = self.project / "probe/linked.svg"
        try:
            target.symlink_to(self.project / "probe/input.svg")
        except OSError as error:
            self.skipTest(f"host does not permit a real symlink fixture: {error}")
        self.binding["observations"]["input_svg"]["path"] = "probe/linked.svg"
        self.save_binding()
        with self.assertRaises(ContractError):
            self.check()

    def test_closure_contains_checker_validator_contract_and_schema(self):
        members = {path.relative_to(ROOT).as_posix()
                   for path in closure(ROOT, [ROOT / "skills/core/nckh-visuals/SKILL.md"])}
        self.assertTrue({"scripts/check-visual-engine.py", "core/schema.py",
                         "core/contracts/visual-engine-binding.schema.json",
                         "core/contracts/extension.schema.json",
                         "extensions/native-documents/contract.json"} <= members)

    def test_extracted_checker_works_with_isolated_python_from_other_cwd(self):
        extracted = self.project / "extracted/references/_shared"
        for relative in ["scripts/check-visual-engine.py", "core/schema.py",
                         "core/contracts/visual-engine-binding.schema.json",
                         "core/contracts/extension.schema.json", "extensions/native-documents/contract.json"]:
            destination = extracted / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, destination)
        working = self.project / "unrelated-cwd"
        working.mkdir()
        env = {**os.environ, "PYTHONPATH": str(self.project / "unavailable-import-root")}
        command = [sys.executable, "-I", str(extracted / "scripts/check-visual-engine.py"),
                   "--project", str(self.project), "--task", "chart-task", "--host", "codex",
                   "--binding", "probe/binding.json", "--capability", "svg-render"]
        result = subprocess.run(command, cwd=working, env=env, capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(json.loads(result.stdout)["status"], "integrity-verified")
        self.assertFalse(list(extracted.rglob("__pycache__")))
        self.binding["scope"]["task_id"] = "other-task"
        self.save_binding()
        failed = subprocess.run(command, cwd=working, env=env, capture_output=True, text=True, timeout=20)
        self.assertEqual(failed.returncode, 1, failed.stderr + failed.stdout)
        self.assertFalse(json.loads(failed.stdout)["fallback"])


if __name__ == "__main__":
    unittest.main()
