"""Run unchanged deterministic tests and expose failures when they occur."""

import sys
import unittest
from pathlib import Path

ROOT = Path(r"C:/Users/USER\Downloads\test-skill\nckh-kit")
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from core.paths import atomic_json


class DiagnosticResult(unittest.TextTestResult):
    def addError(self, test, error):
        super().addError(test, error)
        self.stream.writeln(self._exc_info_to_string(error, test))
        self.stream.flush()

    def addFailure(self, test, error):
        super().addFailure(test, error)
        self.stream.writeln(self._exc_info_to_string(error, test))
        self.stream.flush()


suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py", top_level_dir=str(ROOT))
result = unittest.TextTestRunner(verbosity=2, resultclass=DiagnosticResult).run(suite)
atomic_json(Path(sys.argv[1]), {
    "tests": result.testsRun,
    "successful": result.wasSuccessful(),
    "errors": [{"test": test.id(), "traceback": trace} for test, trace in result.errors],
    "failures": [{"test": test.id(), "traceback": trace} for test, trace in result.failures],
    "skipped": [{"test": test.id(), "reason": reason} for test, reason in result.skipped],
})
sys.exit(0 if result.wasSuccessful() and result.testsRun > 0 else 1)
