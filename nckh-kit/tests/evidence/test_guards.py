import unittest
from pathlib import Path

from core.guards import (FACT_DIMENSIONS, active_venue, check_claim_bundle,
                         check_visual_receipt, factual_delta, ranking_known)
from core.paths import digest_file, temporary_tree
from core.schema import ContractError, validate_record


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.source = {"sha256": "a" * 64, "status": "current", "access": "full-text", "doi": "real-id"}
        self.evidence = {"source_id": "s1", "source_sha256": "a" * 64,
                         "locator": {"value": "p. 3"}, "context": "observed scope", "ocr": "not-applicable"}
        self.claim = {"verdict": "supported", "evidence_ids": ["e1"]}

    def check(self, **kw):
        return check_claim_bundle(self.claim, {"e1": self.evidence}, {"s1": self.source}, **kw)

    def test_real_identity_cannot_override_contradicted_claim(self):
        self.claim["verdict"] = "contradicted"
        self.assertEqual(self.check(), "pending")

    def test_missing_page_abstract_ocr_retraction_are_not_accepted(self):
        self.evidence["locator"]["value"] = ""
        self.assertEqual(self.check(), "pending")
        self.evidence["locator"]["value"] = "p.3"
        self.source["access"] = "abstract"
        self.assertEqual(self.check(), "pending")
        self.source["access"] = "full-text"
        self.evidence["ocr"] = "unverified"
        self.assertEqual(self.check(exact_quote=True), "pending")
        self.source["status"] = "retracted"
        self.assertEqual(self.check(), "pending")

    def test_changed_source_or_edition_is_stale(self):
        self.source["sha256"] = "b" * 64
        self.assertEqual(self.check(), "stale")
        self.source["sha256"] = "a" * 64
        self.source["edition"] = "second"
        self.evidence["edition"] = "first"
        self.assertEqual(self.check(), "stale")

    def test_factual_delta_is_separate_from_taste(self):
        before = dict.fromkeys(FACT_DIMENSIONS, "unchanged")
        after = dict(before, certainty="causally proves", denominators="100 rather than 20")
        result = factual_delta(before, after)
        self.assertEqual(result["status"], "pending-evidence")
        self.assertEqual(set(result["changes"]), {"certainty", "denominators"})
        self.assertEqual(result["semantic_fidelity"], "unverified")

    def test_ranking_and_venue_are_not_inferred_or_unioned(self):
        self.assertFalse(ranking_known({"doi": "x", "quartile": "Q1"}))
        with self.assertRaises(ContractError):
            active_venue([{"venue_id": "journal"}, {"venue_id": "conference"}])

    def test_visual_qa_binds_final_bytes(self):
        with temporary_tree() as tmp:
            files = {key: Path(tmp) / key for key in ["source", "data", "artifact", "render", "manifest"]}
            for file in files.values():
                file.write_bytes(b"actual fixture bytes")
            receipt = {"hashes": {k: digest_file(p) for k, p in files.items()},
                       "viewer_version": "fixture", "font_version": "fixture", "qa_run_reference": "fixture-run"}
            self.assertIn("hashes-current", check_visual_receipt(receipt, files))
            files["artifact"].write_bytes(b"edited after QA")
            self.assertEqual(check_visual_receipt(receipt, files), "stale")

    def test_source_schema_rejects_unknown_or_fabricated_version_fields(self):
        with self.assertRaises(ContractError):
            validate_record("source", {"schema_version": 2})
