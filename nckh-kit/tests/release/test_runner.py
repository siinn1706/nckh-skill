import importlib.util
import io
import json
import subprocess
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

from core.paths import temporary_tree
from core.schema import ContractError


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("nckh_evaluation_entry", ROOT / "evals/run-evals.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)


class RunnerTests(unittest.TestCase):
    def test_timeout_retains_partial_output_without_a_pass(self):
        with temporary_tree() as root:
            output = root / "timeout-check.json"
            timeout = subprocess.TimeoutExpired("owned deterministic fixture", 900, output=b"injected partial output", stderr=b"injected timeout")
            with patch.object(entry.subprocess, "run", side_effect=timeout), redirect_stderr(io.StringIO()):
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
