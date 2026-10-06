import importlib.util
import json
import shutil
import unittest
from pathlib import Path

from core.build import closure
from core.guards import FACT_DIMENSIONS, factual_delta
from core.paths import temporary_tree


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("writer_resource_reader", ROOT / "scripts/search-resource.py")
READER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(READER)
LOOKUPS = {
    "R-nature-reference": {"domain": "scientific-writing", "genre": "writing-advice", "locale": "en"},
    "R-vi-wikisource-passages": {"domain": "language-literary", "genre": "prose-verse-samples", "locale": "vi"},
    "R-pmc-scientific": {"domain": "scientific-writing", "genre": "scientific-research-article", "locale": "en"},
    "R-reporting-lookup": {"domain": "clinical-health", "genre": "reporting-reference", "locale": "en", "study_design": "randomized_trial"},
}
MAPPING = {"nckh-humanwrite": ("R-nature-reference", "R-vi-wikisource-passages", "R-pmc-scientific"),
           "nckh-paperwrite": ("R-nature-reference", "R-pmc-scientific", "R-reporting-lookup")}


class WriterConsumerTests(unittest.TestCase):
    def test_selected_writer_reads_retain_source_provenance(self):
        for writer, packs in MAPPING.items():
            for pack in packs:
                with self.subTest(writer=writer, pack=pack):
                    result = READER.lookup(pack, writer, root=ROOT, **LOOKUPS[pack])
                    self.assertTrue(result["resource_read"])
                    self.assertTrue(result["records"])
                    self.assertTrue(result["records"][0]["provenance"])

    def test_wrong_consumer_locale_genre_and_domain_do_not_read(self):
        for writer, pack in (("nckh-paperwrite", "R-vi-wikisource-passages"),
                             ("nckh-humanwrite", "R-reporting-lookup"),
                             ("nckh-paperwrite", "R-publisher-profile")):
            with self.subTest(writer=writer, pack=pack), self.assertRaises(ValueError):
                READER.lookup(pack, writer, root=ROOT, domain="scientific-writing", genre="writing-advice")
        for field, value in (("locale", "vi"), ("genre", "scientific-gold")):
            kwargs = {**LOOKUPS["R-nature-reference"], field: value}
            with self.subTest(field=field), self.assertRaises(ValueError):
                READER.lookup("R-nature-reference", "nckh-paperwrite", root=ROOT, **kwargs)
        result = READER.lookup("R-nature-reference", "nckh-paperwrite", root=ROOT,
                               **{**LOOKUPS["R-nature-reference"], "domain": "marketing"})
        self.assertFalse(result["resource_read"])

    def test_disabled_resources_do_not_need_a_registry(self):
        for writer, packs in MAPPING.items():
            for pack in packs:
                result = READER.lookup(pack, writer, root=ROOT / "absent-root", resource_access="off", **LOOKUPS[pack])
                self.assertEqual(result["status"], "resource-disabled")
                self.assertFalse(result["resource_read"])

    def test_rights_drift_is_rejected_with_actual_source_bytes(self):
        with temporary_tree() as target:
            shutil.copytree(ROOT / "core/profiles/resources", target / "core/profiles/resources")
            path = target / "core/registry/catalog/resources.json"
            path.parent.mkdir(parents=True)
            shutil.copy2(ROOT / "core/registry/catalog/skills.json", path.parent / "skills.json")
            catalog = json.loads((ROOT / "core/registry/catalog/resources.json").read_text(encoding="utf8"))
            row = next(row for row in catalog["resources"] if row["resource_id"] == "R-nature-reference")
            row["source"]["license_sha256"] = "0" * 64
            path.write_text(json.dumps(catalog), encoding="utf8")
            with self.assertRaises(ValueError):
                READER.lookup("R-nature-reference", "nckh-humanwrite", root=target, **LOOKUPS["R-nature-reference"])

    def test_humanizer_policy_is_direct_and_relocatable_not_a_resource_pack(self):
        entry = ROOT / "skills/core/nckh-humanwrite/SKILL.md"
        policy = ROOT / "skills/core/nckh-humanwrite/references/humanizer-adaptation.md"
        self.assertIn("[Humanizer adaptation](references/humanizer-adaptation.md)", entry.read_text(encoding="utf8"))
        self.assertIn(policy, closure(ROOT, [entry]))
        rows = [line for line in policy.read_text(encoding="utf8").splitlines() if line.startswith("| ")][1:]
        self.assertEqual(len(rows), 6)
        self.assertTrue(all(len(row.split("|")) == 6 and all(part.strip() for part in row.split("|")[1:-1]) for row in rows))
        registry = json.loads((ROOT / "core/registry/catalog/resources.json").read_text(encoding="utf8"))
        self.assertEqual(len(registry["resources"]), 13)

    def test_factual_delta_blocks_lost_negation_number_citation_or_quote(self):
        before = {field: [] for field in FACT_DIMENSIONS}
        before.update(numbers=[12, 30], citations=["[1]"], negation=["not significant"])
        self.assertEqual(factual_delta(before, before, protected_before=["quote"], protected_after=["quote"])["status"], "declared-slots-preserved")
        for field in ("numbers", "citations", "negation"):
            after = {**before, field: []}
            self.assertEqual(factual_delta(before, after)["status"], "pending-evidence")
        self.assertIn("protected_regions", factual_delta(before, before, protected_before=["quote"], protected_after=[])["changes"])
