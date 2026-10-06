"""Lock-independent ownership declarations; no native behavior is simulated."""
from copy import deepcopy
from pathlib import Path
import unittest

from core.build import APPROVED_IDENTITIES, load_json
from core.evaluation import RESEARCH_ROUTES, validate_research_matrix
from core.schema import ContractError

ROOT = Path(__file__).resolve().parents[2]

class ResearchMatrixTests(unittest.TestCase):
    def setUp(self):
        self.record = load_json(ROOT / "evals/cases/research-data-aiops/domain-scenarios.json")
        self.identities = dict.fromkeys(APPROVED_IDENTITIES)

    def test_exact_scenarios_remain_unobserved_and_separate_from_base_ids(self):
        result = validate_research_matrix(self.record, self.identities)
        self.assertEqual(result["scenarios"], 12)
        self.assertEqual(result["observed_behavior"], "unverified")
        self.assertTrue(all(":" not in row["id"] for row in self.record["scenarios"]))

    def test_near_miss_owners_require_rejection_handoff_and_no_execution(self):
        for row in self.record["scenarios"]:
            expected = RESEARCH_ROUTES[row["id"]]
            self.assertEqual((row["requested_owner"], row["expected_owner"]), expected)
            if expected[0] == expected[1]:
                continue
            broken = deepcopy(self.record)
            next(item for item in broken["scenarios"] if item["id"] == row["id"])["expected_route"] = "execute-own-scope"
            with self.subTest(scenario=row["id"]), self.assertRaises(ContractError):
                validate_research_matrix(broken, self.identities)

    def test_missing_duplicate_unknown_owner_and_fabricated_receipt_rejected(self):
        for mutation in ("missing", "duplicate", "owner", "receipt", "field"):
            broken = deepcopy(self.record)
            if mutation == "missing": broken["scenarios"].pop()
            elif mutation == "duplicate": broken["scenarios"][-1] = deepcopy(broken["scenarios"][0])
            elif mutation == "owner": broken["scenarios"][0]["expected_owner"] = "nckh-unknown"
            elif mutation == "receipt": broken["scenarios"][0]["receipt_reference"] = "unobserved.json"
            else: broken["provider_called"] = True
            with self.subTest(mutation=mutation), self.assertRaises(ContractError):
                validate_research_matrix(broken, self.identities)

if __name__ == "__main__":
    unittest.main()
