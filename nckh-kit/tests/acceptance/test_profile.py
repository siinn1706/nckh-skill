import json
import re
import unittest
from copy import deepcopy
from pathlib import Path

from core.acceptance import (_load_json, acceptance_profile_path, bind_owner_feedback,
                             load_profile, lookup, validate_profile)
from core.build import APPROVED_IDENTITIES, closure, load_json, validate_catalog
from core.paths import temporary_tree
from core.schema import ContractError


class AcceptanceProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[2]
        cls.profile = load_profile(cls.root)
        cls.catalog = load_json(cls.root / "core/registry/catalog/skills.json")

    def test_profile_covers_exact_catalog_and_resolves_sources(self):
        identities = {row["id"]: row for row in self.catalog["skills"]}
        self.assertEqual(len(self.profile["skills"]), 43)
        self.assertEqual(set(self.profile["skills"]), set(identities))
        self.assertEqual(len(self.profile["sources"]), 36)
        for identity, row in self.profile["skills"].items():
            with self.subTest(skill=identity):
                self.assertEqual(row["kit"], identities[identity]["kit"])
                self.assertEqual(row["eval_ids"], identities[identity]["eval_ids"])
                self.assertTrue(set(row["source_ids"]) <= set(self.profile["sources"]))
                for source_id in row["source_ids"]:
                    source = self.profile["sources"][source_id]
                    self.assertTrue(source["urls"])
                    self.assertTrue(all(url.startswith(("http://", "https://")) for url in source["urls"]))
                    self.assertTrue(source["applicability"])
                    self.assertTrue(source["limitations"])

    def test_lookup_returns_skill_criteria_and_scoped_source_records(self):
        result = lookup(self.root, "nckh-write")
        self.assertEqual(result["lane"], "personal-use")
        self.assertEqual(result["skill_id"], "nckh-write")
        self.assertEqual([gate["id"] for gate in result["common"]["gates"]], [
            "identity-route", "positive-behavior", "output-facts",
            "authority-side-effects", "receipt-feedback",
        ])
        self.assertIn("PUB-IEEE", result["sources"])
        self.assertTrue(result["sources"]["PUB-IEEE"]["applicability"])
        self.assertTrue(result["skill"]["criteria"]["positive"])

    def test_exact_membership_rejects_missing_replacement_and_duplicate_ids(self):
        self.assertEqual(set(self.profile["skills"]), APPROVED_IDENTITIES)
        for mutation in ("missing", "replacement", "duplicate"):
            broken = deepcopy(self.catalog)
            if mutation == "missing":
                broken["skills"].pop()
            elif mutation == "replacement":
                broken["skills"][0]["id"] = "nckh-unknown"
            else:
                broken["skills"][-1] = deepcopy(broken["skills"][0])
            with self.subTest(mutation=mutation), self.assertRaises(ContractError):
                validate_catalog(broken)
        broken = deepcopy(self.profile)
        broken["skills"]["nckh-unknown"] = broken["skills"].pop("nckh-plan")
        with self.assertRaises(ContractError):
            validate_profile(broken)

    def test_unknown_source_or_missing_applicability_fails_closed(self):
        broken = deepcopy(self.profile)
        broken["skills"]["nckh-plan"]["source_ids"] = ["SOURCE-NOT-DEFINED"]
        with self.assertRaises(ContractError):
            validate_profile(broken, catalog=self.catalog)
        broken = deepcopy(self.profile)
        source_id = broken["skills"]["nckh-plan"]["source_ids"][0]
        broken["sources"][source_id]["applicability"] = ""
        with self.assertRaises(ContractError):
            validate_profile(broken, catalog=self.catalog)

    def test_duplicate_json_keys_and_boolean_version_are_rejected(self):
        with temporary_tree() as temporary:
            path = Path(temporary) / "duplicate-profile.json"
            path.write_text('{"schema_version": 0, "schema_version": 1}', encoding="utf-8")
            with self.assertRaises(ContractError):
                _load_json(path)
        broken = deepcopy(self.profile)
        broken["schema_version"] = True
        with self.assertRaises(ContractError):
            validate_profile(broken, catalog=self.catalog)

    def test_policy_profile_link_is_reachable_from_all_skill_closures(self):
        policy = self.root / "core/policies/acceptance-policy.md"
        policy_text = policy.read_text(encoding="utf-8")
        match = re.search(r"\]\(\.\./profiles/acceptance/personal-use\.json\)", policy_text)
        self.assertIsNotNone(match)
        profile_path = acceptance_profile_path(self.root)
        self.assertEqual(profile_path, self.root / "core/profiles/acceptance/personal-use.json")
        for row in self.catalog["skills"]:
            identity = row["id"]
            skill_path = self.root / row["path"] / "SKILL.md"
            with self.subTest(skill=identity):
                skill_text = skill_path.read_text(encoding="utf-8")
                self.assertIn("../../../core/policies/acceptance-policy.md", skill_text)
                members = {path.relative_to(self.root).as_posix() for path in closure(self.root, [skill_path])}
                self.assertIn("core/profiles/acceptance/personal-use.json", members)

    def test_owner_feedback_absence_and_binding(self):
        current = {"revision": "r1", "artifact_hash": "a" * 64, "input_hashes": ["b" * 64]}
        pending = bind_owner_feedback(None, **current)
        self.assertEqual(pending["status"], "pending-personal-review")
        self.assertEqual(pending["verdict"], "pending")
        recorded = bind_owner_feedback({
            **current,
            "verdict": "pass",
            "feedback_reference": "owner-note-1",
            "comment": "Artifact is usable for the stated personal task.",
        }, **current)
        self.assertEqual(recorded["status"], "recorded")
        self.assertEqual(recorded["verdict"], "pass")
        for changed in [
            {**current, "revision": "r2"},
            {**current, "artifact_hash": "c" * 64},
            {**current, "input_hashes": ["d" * 64]},
        ]:
            with self.subTest(changed=changed), self.assertRaises(ContractError):
                bind_owner_feedback({
                    **changed,
                    "verdict": "pass",
                    "feedback_reference": "owner-note-1",
                    "comment": "Mismatch must fail closed.",
                }, **current)

    def test_personal_use_does_not_mutate_historical_qualification_boundary(self):
        protocol_path = self.root / "evals/protocols/qualification.json"
        protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
        self.assertEqual(protocol["development_max_rounds"], 3)
        self.assertEqual(set(protocol["split"]["by"]), {"document", "author", "topic", "claim-family"})
        self.assertIn("inventing human labels", protocol["forbidden"])
        self.assertEqual(self.profile["qualification_boundary"]["catalog_status_remains"], "experimental")
        self.assertEqual(self.profile["qualification_boundary"]["protocol_mutation"], "forbidden")

