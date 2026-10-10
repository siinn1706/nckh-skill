import importlib.util
import io
import json
import os
import subprocess
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

from core.paths import temporary_tree
from core.schema import ContractError
from tests._lab import lab_root


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("nckh_evaluation_entry", ROOT / "evals/run-evals.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)


class RunnerTests(unittest.TestCase):
    def test_dirty_lab_fails_once_before_dispatching_suite(self):
        with temporary_tree(lab_root()) as root:
            (root / ".cursor/skills/nckh-plan").mkdir(parents=True)
            output = root / "preflight.json"
            with patch.dict(os.environ, {"NCKH_TEST_ROOT": str(root)}), patch.object(entry.subprocess, "run") as run, redirect_stderr(io.StringIO()):
                self.assertEqual(entry.main(["--run-deterministic", "--output", str(output)]), 3)
            run.assert_not_called()
            record = json.loads(output.read_text(encoding="utf-8"))
            self.assertIn("NCKH_TEST_ROOT", record["error"])
            self.assertEqual(record["stage"], "lab-preflight")
            self.assertNotIn("deterministic", record)

    def test_lab_preflight_failure_records_stage(self):
        with temporary_tree() as root:
            output = root / "preflight-stage.json"
            failure = ContractError("injected unwritable lab root; set NCKH_TEST_ROOT")
            with patch("tests._lab.lab_root", side_effect=failure), patch.object(entry.subprocess, "run") as run, redirect_stderr(io.StringIO()):
                code = entry.main(["--run-deterministic", "--output", str(output)])
            run.assert_not_called()
            result = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(code, 3)
            self.assertEqual(result["status"], "fail")
            self.assertEqual(result["stage"], "lab-preflight")
            self.assertIn("injected unwritable lab root", result["error"])
            self.assertNotIn("deterministic", result)

    def test_timeout_status_is_independent_of_ambient_lab_root(self):
        with temporary_tree() as root:
            dirty = root / "dirty-root"
            (dirty / ".cursor/skills/nckh-plan").mkdir(parents=True)
            owned = root / "owned-lab"
            owned.mkdir()
            output = root / "ambient-timeout.json"
            timeout = subprocess.TimeoutExpired("owned deterministic fixture", 900, output=b"partial", stderr=b"")
            with patch.dict(os.environ, {"NCKH_TEST_ROOT": str(dirty)}), patch("tests._lab.lab_root", return_value=owned),                     patch.object(entry.subprocess, "run", side_effect=timeout) as run, redirect_stderr(io.StringIO()):
                code = entry.main(["--run-deterministic", "--output", str(output)])
            run.assert_called_once()
            self.assertEqual(run.call_args.kwargs["timeout"], 900)
            result = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(code, 3)
            self.assertEqual(result["status"], "timeout-unknown")
            self.assertEqual(result["deterministic"]["status"], "timeout-unknown")
            self.assertNotIn("stage", result)

    def test_timeout_retains_partial_output_without_a_pass(self):
        with temporary_tree() as root:
            output = root / "timeout-check.json"
            timeout = subprocess.TimeoutExpired("owned deterministic fixture", 900, output=b"injected partial output", stderr=b"injected timeout")
            owned = root / "owned-lab"
            owned.mkdir()
            with patch("tests._lab.lab_root", return_value=owned), patch.object(entry.subprocess, "run", side_effect=timeout), redirect_stderr(io.StringIO()):
                code = entry.main(["--run-deterministic", "--output", str(output)])
            result = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(code, 3)
            self.assertEqual(result["status"], "timeout-unknown")
            self.assertEqual(result["deterministic"]["status"], "timeout-unknown")
            self.assertIsNone(result["deterministic"]["exit_status"])
            self.assertIn("injected partial output", result["deterministic"]["output"])
            self.assertEqual(result["qualification"], "pending")

    def test_validation_failure_retains_failed_receipt(self):
        with temporary_tree() as root:
            output = root / "failed-check.json"
            with patch.object(entry, "validate_cases", side_effect=ContractError("injected missing source pin")), redirect_stderr(io.StringIO()):
                code = entry.main(["--validate-only", "--output", str(output)])
            result = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(code, 3)
            self.assertEqual(result["status"], "fail")
            self.assertEqual(result["error"], "injected missing source pin")
            self.assertNotIn("deterministic", result)
            self.assertNotIn("qualification", result)
