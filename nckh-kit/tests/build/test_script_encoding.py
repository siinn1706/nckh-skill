"""Every shipped script must survive a legacy cp1252 console with Vietnamese input."""
from tests._lab import lab_root
import contextlib
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from core.build import SCRIPT_REQUIREMENTS, closure
from core.ledger import eol_profile
from core.paths import digest_bytes, temporary_tree


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests/contracts/fixtures/plans"
# Scripts that rebuild or re-freeze the kit would mutate the source tree or run for
# minutes, so only their argparse/help surface is exercised under cp1252.
HELP_ONLY = {"build-artifacts.py", "freeze-source-lock.py"}
NEW_SCRIPTS = ("scripts/check-plan.py", "scripts/check-receipt.py")


def cp1252_env():
    env = {key: value for key, value in os.environ.items() if key not in {"PYTHONPATH", "PYTHONUTF8"}}
    env.update(PYTHONIOENCODING="cp1252", PYTHONUTF8="0")
    return env


class ScriptEncodingTests(unittest.TestCase):
    def setUp(self):
        self.tree = temporary_tree(lab_root())
        self.root = self.tree.__enter__()
        self.addCleanup(self.tree.__exit__, None, None, None)
        self.work = self.root / "Dự án Báo cáo Lab 2"
        self.work.mkdir()

    def run_script(self, script, *args, cwd=None):
        command = [sys.executable, "-I", str(script), *map(str, args)]
        return subprocess.run(command, cwd=cwd or self.work, env=cp1252_env(), stdin=subprocess.DEVNULL,
                              capture_output=True, timeout=60)

    def assertSurvives(self, result, codes, label):
        stderr = result.stderr.decode("utf-8", "replace")
        self.assertNotIn("UnicodeEncodeError", stderr, label)
        self.assertNotIn("Traceback", stderr, label)
        self.assertIn(result.returncode, codes, f"{label}: {stderr}")

    def visual_engine_case(self):
        from tests.evidence import test_visual_engine_binding as visual
        project = self.work / "hình"
        project.mkdir()
        fixture = visual.VisualEngineBindingTests("test_closure_contains_checker_validator_contract_and_schema")
        with patch.object(visual, "temporary_tree", lambda: contextlib.nullcontext(project)):
            fixture.setUp()
        return ["--project", project, "--task", "chart-task", "--host", "codex",
                "--binding", "probe/binding.json", "--capability", "svg-render"], {0}

    def research_case(self):
        from tests.research.test_datasets import save_fixture
        from tests.research.test_experiments import experiment_fixture
        project = self.work / "thí nghiệm"
        project.mkdir()
        manifest = experiment_fixture(project)
        save_fixture(project, "bản-kê.json", manifest)
        return ["--project", project, "--task", manifest["task_id"], "--manifest", "bản-kê.json",
                "--output", "kiểm-tra.json"], {0}

    def receipt_cases(self):
        data = "Tiêu đề báo cáo\r\nGhi chú đầu\r\n".encode("utf-8")
        documents = self.work / "Tài liệu"
        documents.mkdir()
        (documents / "Mẫu báo cáo.txt").write_bytes(data)
        record = {"path": "Mẫu báo cáo.txt", "sha256_before": digest_bytes(data), "sha256_after": digest_bytes(data),
                  "eol_before": eol_profile(data), "eol_after": eol_profile(data), "mutation": "none"}
        receipt = {"schema_version": 2, "id": "biên-nhận", "evidence_class": "deterministic", "host": "local",
                   "surface": "shell", "version": "1", "logical_entrypoint": "xuất.py", "mode": "auto",
                   "actual_invocation": "python xuất.py", **{key: "không" for key in (
                       "requested_model", "resolved_model", "effective_model", "requested_effort",
                       "resolved_effort", "effective_effort", "permission_mode", "sandbox",
                       "tool_trace_reference", "egress_trace_reference", "output_status", "cost_coverage")},
                   "exit_status": "0", "cost": "0", "as_of": "2026-10-08", "skill_ids": [], "agent_ids": [],
                   "plugin_ids": [], "input_hashes": [], "output_hashes": [], "checks": ["đã đọc"],
                   "limitations": [], "closure_hash": "0" * 64,
                   "command_results": [{"command": "python xuất.py; python kiểm.py", "shell": "pwsh", "cwd": ".",
                                        "exit_status": 0, "stdout_sha256": "0" * 64, "stderr_sha256": "0" * 64,
                                        "expected_nonzero": False}],
                   "input_files": [record], "output_files": []}
        (self.work / "biên-nhận.json").write_text(json.dumps(receipt, ensure_ascii=False), encoding="utf-8")
        return [(["inventory", "--root", documents, "--output", self.work / "trước.json"], {0}),
                (["verify", "--receipt", self.work / "biên-nhận.json", "--workspace", documents], {1})]

    def oracle_cases(self):
        from core.ledger import inventory
        workspace = self.work / "Không gian chấm"
        workspace.mkdir()
        shutil.copyfile(ROOT / "evals/cases/regression/fixtures/r43/brief.txt", workspace / "brief.txt")
        (self.work / "kiểm-kê-trước.json").write_text(json.dumps(inventory(workspace)), encoding="utf-8")
        (self.work / "phản-hồi.txt").write_text("Việc này thuộc nckh-humanwrite; tôi handoff, không sửa.",
                                                encoding="utf-8")
        common = ["--case-id", "nckh-copy:negative:near-miss-humanwrite", "--workspace", workspace,
                  "--before", self.work / "kiểm-kê-trước.json"]
        return [(common + ["--response", self.work / "phản-hồi.txt"], {0}), (common, {1})]

    def cases(self, name):
        directory = self.work / "Thư mục trống"
        directory.mkdir(exist_ok=True)
        missing = self.work / "không-có.json"
        if name in HELP_ONLY:
            return [(["--help"], {0})]
        if name == "check-plan.py":
            plan = self.work / "Kế hoạch Lab 2"
            if not plan.exists():
                shutil.copytree(FIXTURES / "lab02-single-file", plan)
            return [([plan], {1})]
        if name == "check-receipt.py":
            return self.receipt_cases()
        if name == "check-case-oracle.py":
            return self.oracle_cases()
        if name == "check-research-artifacts.py":
            return [self.research_case()]
        if name == "check-visual-engine.py":
            return [self.visual_engine_case()]
        if name == "search-resource.py":
            return [(["--resource-id", "R-statistical-recipes", "--consumer", "nckh-statistics", "--domain",
                      "scientific-statistics", "--genre", "statistical-recipe", "--resource-access", "off",
                      "--query", "kiểm định thống kê", "--json"], {0})]
        if name == "compare-matched.py":
            return [(["--manifest", missing, "--work-context", directory], {3})]
        if name == "configure-hooks.py":
            return [(["preview", "--project", directory, "--host", "claude", "--context", "ngữ-cảnh.json"], {3})]
        if name == "hook-preflight.py":
            return [(["--project", directory, "--context", "ngữ-cảnh.json"], {3})]
        if name == "resource-smoke.py":
            return [(["--bundle", directory / "gói", "--cwd", directory], {3})]
        self.fail(f"no cp1252 case for new script {name}; add one before shipping it")

    def test_scripts_survive_cp1252_stdout_with_vietnamese_input(self):
        scripts = sorted(path for path in (ROOT / "scripts").glob("*.py") if path.name != "__init__.py")
        self.assertTrue({"check-plan.py", "check-receipt.py"} <= {path.name for path in scripts})
        for script in scripts:
            for args, codes in self.cases(script.name):
                with self.subTest(script=script.name, args=args[:1]):
                    result = self.run_script(script, *args)
                    self.assertSurvives(result, codes, script.name)
                    if result.stdout.strip() and script.name not in HELP_ONLY:
                        json.loads(result.stdout.decode("utf-8"))

    def test_new_scripts_are_in_skill_closure(self):
        members = {path.relative_to(ROOT).as_posix() for path in closure(ROOT, [ROOT / s for s in NEW_SCRIPTS])}
        for script in NEW_SCRIPTS:
            self.assertIn(script, SCRIPT_REQUIREMENTS)
            self.assertTrue({script, *SCRIPT_REQUIREMENTS[script]} <= members, script)
        extracted = self.root / "skill/references/_shared"
        for relative in members:
            target = extracted / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        plan = self.work / "Kế hoạch"
        shutil.copytree(FIXTURES / "valid-two-phase", plan)
        result = self.run_script(extracted / "scripts/check-plan.py", plan)
        self.assertSurvives(result, {0}, "extracted check-plan")
        self.assertEqual(json.loads(result.stdout)["verdict"], "VERIFIED")
        result = self.run_script(extracted / "scripts/check-receipt.py", "inventory", "--root", plan,
                                 "--output", self.work / "trước.json")
        self.assertSurvives(result, {0}, "extracted check-receipt")
        self.assertEqual(len(json.loads((self.work / "trước.json").read_text(encoding="ascii"))["files"]), 4)
        self.assertFalse(list(extracted.rglob("__pycache__")))


if __name__ == "__main__":
    unittest.main()
