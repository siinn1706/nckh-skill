"""Every catalog skill belongs to a required case family; checked on the live tree without the source lock."""
import unittest
from pathlib import Path

from core.build import load_json, validate_catalog
from core.evaluation import load_regression_cases, validate_case_manifest, validate_required_families

ROOT = Path(__file__).resolve().parents[2]


class FamilyCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.identities = validate_catalog(load_json(ROOT / "core/registry/catalog/skills.json"))
        cls.record = load_json(ROOT / "evals/cases/required-families.json")
        cls.families = cls.record["families"]

    def test_every_catalog_skill_in_some_family(self):
        mapped = {skill for family in self.families for skill in family["skills"]}
        self.assertEqual(len(self.identities), 43)
        self.assertEqual(sorted(set(self.identities) - mapped), [])
        self.assertEqual(sorted(mapped - set(self.identities)), [])

    def test_family_count_stays_24(self):
        self.assertEqual(len(self.families), 24)
        self.assertEqual(len({family["id"] for family in self.families}), 24)

    def test_family_cases_belong_to_family_skills(self):
        regression = load_regression_cases(ROOT, self.identities)
        base = {}
        for path in sorted((ROOT / "evals/cases").glob("*/*.json")):
            record = load_json(path)
            if "skill_id" in record and record.get("kind") is None:
                base.update(validate_case_manifest(record, self.identities))
        validate_required_families(self.record, self.identities, base, regression)
        for family in self.families:
            for case_id in family["family_cases"]:
                with self.subTest(family=family["id"], case=case_id):
                    self.assertIn(case_id, regression)
                    self.assertIn(regression[case_id]["skill_id"], family["skills"])


if __name__ == "__main__":
    unittest.main()
