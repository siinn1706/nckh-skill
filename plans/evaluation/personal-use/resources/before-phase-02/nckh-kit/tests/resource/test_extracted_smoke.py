import importlib.util
import os
import shutil
import unittest
from pathlib import Path

from core.build import build_host, verify_bundle
from core.paths import temporary_tree
from core.schema import ContractError


ROOT = Path(os.environ.get("NCKH_RESOURCE_TEST_ROOT", Path(__file__).resolve().parents[2]))
spec = importlib.util.spec_from_file_location("resource_smoke", ROOT / "scripts/resource-smoke.py")
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)


class ExtractedSmokeTests(unittest.TestCase):
    def test_real_read_after_archive_extraction_outside_repo(self):
        with temporary_tree() as environment:
            built, extracted, cwd = environment / "built", environment / "extracted", environment / "empty-cwd"
            cwd.mkdir()
            build_host(ROOT, "codex", ["core", "engineer"], built, include_plugin=True)
            archive = shutil.make_archive(str(environment / "bundle"), "zip", built)
            shutil.unpack_archive(archive, extracted)
            verify_bundle(extracted)
            for invalid_cwd in [ROOT, extracted]:
                with self.subTest(cwd=invalid_cwd), self.assertRaises(ContractError):
                    smoke.smoke(extracted, invalid_cwd)
            result = smoke.smoke(extracted, cwd)
            self.assertEqual({r["resource_id"] for r in result["observations"]},
                             {"R-ui-lookup", "R-reporting-lookup", "R-publisher-profile", "R-nature-reference"})
            self.assertTrue(all(r["resource_read"] for r in result["observations"]))
            self.assertEqual(result["qualification"], "pending")
            self.assertEqual(list(cwd.iterdir()), [])
