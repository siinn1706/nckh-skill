import unittest
from copy import deepcopy
from pathlib import Path

from core.build import load_json
from core.evaluation import validate_writer_matrix
from core.guards import writer_request
from core.schema import ContractError


class WriterMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = load_json(Path(__file__).resolve().parents[2] / "evals/cases/runtime/writer-invocation-matrix.json")

    def test_planned_membership_is_separate_from_behavior(self):
        result = validate_writer_matrix(self.matrix)
        self.assertEqual((result["native_cells"], result["scenario_cells"]), (256, 20))
        self.assertEqual(result["observed_behavior"], "unverified")

    def test_missing_extra_duplicate_and_wrong_identity_fail(self):
        for group in ("native_cases", "scenario_cases"):
            for mutation in ("missing", "extra", "duplicate", "wrong-id"):
                matrix = deepcopy(self.matrix)
                if mutation == "missing":
                    matrix[group].pop()
                elif mutation == "extra":
                    matrix[group].append(deepcopy(matrix[group][0]))
                elif mutation == "duplicate":
                    matrix[group][-1] = deepcopy(matrix[group][0])
                else:
                    matrix[group][0]["id"] += "/unknown"
                with self.subTest(group=group, mutation=mutation), self.assertRaises(ContractError):
                    validate_writer_matrix(matrix)

    def test_wrong_owner_protected_delta_and_false_receipt_fail(self):
        for field, value in (("expected_owner", "nckh-paperwrite"), ("action", "section"),
                             ("protected_fields", ["citations"]), ("no_side_effect_oracle", ""),
                             ("receipt_reference", "fake.json"), ("status", "pass"),
                             ("authorization", True)):
            matrix = deepcopy(self.matrix)
            matrix["native_cases"][0][field] = value
            with self.subTest(field=field), self.assertRaises(ContractError):
                validate_writer_matrix(matrix)

    def test_actions_language_priority_conflict_and_bilingual_override(self):
        for action, owner in (("polish", "nckh-humanwrite"), ("translate", "nckh-humanwrite"),
                              ("section", "nckh-paperwrite"), ("revision-response", "nckh-paperwrite")):
            result = writer_request(action, explicit_target="en", brief_locale="vi", draft_locale="vi")
            self.assertEqual((result["owner"], result["output_locale"]), (owner, "en"))
            self.assertEqual(writer_request(action, brief_locale="vi", draft_locale="en")["output_locale"], "vi")
            self.assertEqual(writer_request(action, draft_locale="vi")["output_locale"], "vi")
            self.assertEqual(writer_request(action)["status"], "ask-one-question-no-write")
            self.assertEqual(writer_request(action, args=["--en", "--vi"])["status"], "conflict-no-write")
            self.assertEqual(writer_request(action, explicit_target="bilingual")["output_locale"], "bilingual")
            self.assertEqual(writer_request(action, args=["--vi"], explicit_target="bilingual")["output_locale"], "vi")
        with self.assertRaises(ContractError):
            writer_request("search")

    def test_scenario_locale_and_conflict_oracles_cannot_drift(self):
        for scenario, field, value in (("conflicting-flags", "expected_route", "nckh-humanwrite"),
                                      ("english-resource-vi-output", "resource_locale", "vi"),
                                      ("no-flag-ambiguous", "args", ["--en"])):
            matrix = deepcopy(self.matrix)
            row = next(row for row in matrix["scenario_cases"] if row["scenario"] == scenario)
            row[field] = value
            with self.subTest(scenario=scenario), self.assertRaises(ContractError):
                validate_writer_matrix(matrix)
