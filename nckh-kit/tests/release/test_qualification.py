import unittest
from copy import deepcopy
from pathlib import Path

from core.build import load_json
from core.evaluation import (development_round, validate_cases, validate_case_manifest,
                             validate_required_families, validate_protocol)
from core.schema import ContractError


class QualificationTests(unittest.TestCase):
    def test_complete_catalog_case_coverage_does_not_mark_quality_pass(self):
        result = validate_cases(Path(__file__).resolve().parents[2])
        self.assertEqual(result["identities"], 43)
        self.assertEqual(result["skill_cases"], 172)
        self.assertEqual(result["required_families"], 19)
        self.assertEqual(result["rubrics"], 5)
        self.assertEqual(result["rubric_approval"], "pending")
        self.assertEqual(result["installer_acceptance_cases"], 10)
        self.assertEqual(result["installer_os_qualification"], "unverified")
        self.assertEqual(result["qualification"], "pending")
        self.assertEqual(result["cost"], "unknown")
        self.assertEqual(result["cost_per_accepted_task"], "undefined")

    def test_exposed_holdout_and_development_limit(self):
        protocol = load_json(Path(__file__).resolve().parents[2] / "evals/protocols/qualification.json")
        self.assertEqual(development_round(protocol, changes=1, exposed_holdout=True)["split"], "development")
        with self.assertRaises(ContractError):
            development_round(protocol, changes=4, exposed_holdout=True)
        for round_number in [1, 0, True, -1]:
            with self.subTest(round=round_number), self.assertRaises(ContractError):
                development_round(protocol, changes=round_number)

    def test_all_negative_oracles_require_rejection_and_handoff(self):
        root = Path(__file__).resolve().parents[2]
        identities = {r["id"]: r for r in load_json(root / "core/registry/catalog/skills.json")["skills"]}
        count = 0
        for path in (root / "evals/cases").glob("*/*.json"):
            record = load_json(path)
            if "skill_id" not in record:
                continue
            validate_case_manifest(record, identities)
            broken = deepcopy(record)
            negative = next(c for c in broken["cases"] if c["type"] == "negative")
            negative["oracle"].pop("route")
            with self.subTest(skill=record["skill_id"]), self.assertRaises(ContractError):
                validate_case_manifest(broken, identities)
            count += 1
        self.assertEqual(count, 43)

    def test_required_families_validate_fields_and_identity_mapping(self):
        root = Path(__file__).resolve().parents[2]
        identities = {r["id"]: r for r in load_json(root / "core/registry/catalog/skills.json")["skills"]}
        cases = {c for r in identities.values() for c in r["eval_ids"]}
        original = load_json(root / "evals/cases/required-families.json")
        validate_required_families(original, identities, dict.fromkeys(cases))
        for field, value in [("skills", ["nckh-unknown"]), ("scenario", 1), ("input_rights", "public"),
                             ("status", "pass"), ("receipt_reference", {}), ("oracle", "")]:
            broken = deepcopy(original)
            broken["families"][0][field] = value
            with self.subTest(field=field), self.assertRaises(ContractError):
                validate_required_families(broken, identities, dict.fromkeys(cases))

    def test_protocol_is_closed_and_preserves_round_split_and_baselines(self):
        root = Path(__file__).resolve().parents[2]
        original = load_json(root / "evals/protocols/qualification.json")
        validate_protocol(original)
        for field in original:
            broken = deepcopy(original)
            broken.pop(field)
            with self.subTest(missing=field), self.assertRaises(ContractError):
                validate_protocol(broken)
        for field, value in [("development_max_rounds", 4), ("baselines", ["no-skill"]), ("extra", True)]:
            broken = deepcopy(original)
            broken[field] = value
            with self.subTest(field=field), self.assertRaises(ContractError):
                validate_protocol(broken)
