import importlib.util
import os
import unittest
from pathlib import Path


ROOT = Path(os.environ.get("NCKH_RESOURCE_TEST_ROOT", Path(__file__).resolve().parents[2]))
spec = importlib.util.spec_from_file_location("resource_reader", ROOT / "scripts/search-resource.py")
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


class ConsumerTests(unittest.TestCase):
    def lookup(self, identity, consumer, **kwargs):
        return reader.lookup(identity, consumer, root=ROOT, **kwargs)

    def test_real_ui_records_and_no_match_preserve_provenance(self):
        result = self.lookup("R-ui-lookup", "nckh-frontend", query="keyboard navigation", domain="ui", genre="ui-heuristic")
        self.assertTrue(result["resource_read"])
        self.assertIn("41", {r["record_id"] for r in result["records"]})
        self.assertEqual(result["records"][0]["provenance"]["version"], "09170eec67eefd46a7ae85de61b40c194020f997")
        unmatched = self.lookup("R-ui-lookup", "nckh-frontend", query="zz-no-existing-item", domain="ui", genre="ui-heuristic")
        self.assertEqual(unmatched["status"], "no-applicable-record")

    def test_reporting_matches_design_and_refuses_generic_cs_domain(self):
        result = self.lookup("R-reporting-lookup", "nckh-method", study_design="randomized_trial", domain="clinical-health", genre="reporting-reference")
        self.assertEqual([r["record_id"] for r in result["records"]], ["consort-2025"])
        result = self.lookup("R-reporting-lookup", "nckh-method", study_design="randomized_trial", domain="cs", genre="reporting-reference")
        self.assertEqual(result["records"], [])

    def test_stale_publishers_keep_warnings_and_exact_context_gate(self):
        for venue, warning in [("science", "historical-live-access-blocked"), ("acs", "legacy-2006-guidance")]:
            result = self.lookup("R-publisher-profile", "nckh-visuals", domain="publication-planning", genre="publisher-profile",
                                 venue=venue, stage="revised" if venue == "science" else "submission", year="2026", track="journal", article_type="research")
            self.assertIn(warning, result["warnings"])
            self.assertEqual(result["policy_applicability"], "unverified")
        with self.assertRaises(ValueError):
            self.lookup("R-publisher-profile", "nckh-visuals", domain="publication-planning", genre="publisher-profile", venue="nature")

    def test_unknown_venue_and_wrong_stage_do_not_manufacture_profiles(self):
        for venue, stage in [("unknown", "submission"), ("nature", "submission")]:
            result = self.lookup("R-publisher-profile", "nckh-visuals", domain="publication-planning", genre="publisher-profile",
                                 venue=venue, stage=stage, year="2026", track="journal", article_type="research")
            self.assertEqual(result["status"], "no-applicable-record")

    def test_consumer_locale_and_genre_mismatch_fail(self):
        for kwargs in [{"consumer": "nckh-cro"}, {"locale": "vi"}, {"genre": "scientific-gold"}]:
            args = {"consumer": "nckh-frontend", "locale": "en", "genre": "ui-heuristic", "domain": "ui", "query": "keyboard"}
            args.update(kwargs)
            with self.subTest(args=kwargs), self.assertRaises(ValueError):
                self.lookup("R-ui-lookup", **args)

    def test_nature_reference_is_advice_and_resource_off_does_not_read_files(self):
        result = self.lookup("R-nature-reference", "nckh-write", domain="scientific-writing", genre="writing-advice")
        self.assertIn("English source", result["records"][0]["content"]["text"])
        off = reader.lookup("R-nature-reference", "nckh-write", domain="scientific-writing", genre="writing-advice",
                            resource_access="off", root=ROOT / "does-not-exist")
        self.assertFalse(off["resource_read"])
        self.assertEqual(off["status"], "resource-disabled")
