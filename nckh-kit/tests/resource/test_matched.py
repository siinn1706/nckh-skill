import importlib.util
import shutil
import unittest
from copy import deepcopy
from pathlib import Path

from core.build import load_json
from core.paths import atomic_json, digest_file, temporary_tree
from core.schema import ContractError


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = Path(__file__).parent / "fixtures/matched"
spec = importlib.util.spec_from_file_location("matched_comparison", ROOT / "scripts/compare-matched.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class MatchedTests(unittest.TestCase):
    def setUp(self):
        self.temporary = temporary_tree()
        self.context = self.temporary.__enter__()
        self.addCleanup(self.temporary.__exit__, None, None, None)
        copied = {}
        for name, source in {
            "corpus": FIXTURE_ROOT / "corpus.json",
            "reviews": FIXTURE_ROOT / "controller-reviews.json",
            "initial": FIXTURE_ROOT / "initial-freeze.json",
            "linkage": FIXTURE_ROOT / "direct-linkage.json",
        }.items():
            target = self.context / (name + ".json")
            shutil.copyfile(source, target)
            copied[name] = {"path": target.name, "sha256": digest_file(target)}
        corpus = load_json(self.context / "corpus.json")
        reviews = load_json(self.context / "reviews.json")
        rounds = {}
        for row in reviews["reviews"]:
            rounds[row["skill_id"]] = max(rounds.get(row["skill_id"], 0), row["round"])
        common = {key: self.record(key + ".json", {"test_contract": key})
                  for key in checker.HASH_FIELDS - {"config", "wrapper", "corpus", "output", "resource_closure"}}
        common["corpus"] = copied["corpus"]
        rows = []
        for identity in sorted(checker.CONDITIONS):
            variant = checker.VARIANTS[identity]
            access = identity.split("/")[-1].removeprefix("resource-") if "/" in identity else {"no-skill": "none", "selected-permitted-upstream": "upstream"}[identity]
            references = {key: None for key in checker.HASH_FIELDS}
            references.update(deepcopy(common))
            references["wrapper"] = self.record(variant.replace(" ", "-") + ".json", {"test_wrapper": variant})
            references["resource_closure"] = self.record(access + ".json", {"test_resource_access": access})
            references["config"] = self.record(identity.replace("/", "-") + "-config.json",
                                                {"condition": identity, "resource_access": access,
                                                 "model": {"requested": None, "resolved": None, "effective": None}, "seed": None})
            rows.append({"id": identity, "variant": variant, "resource_access": access, "status": "not-run",
                         "subject_revision": "21", "references": references,
                         "hashes": {key: value["sha256"] if value else None for key, value in references.items()},
                         "model": {"requested": None, "resolved": None, "effective": None},
                         "gates": dict.fromkeys(["rights", "reviewers", "thresholds", "host_route", "provider_budget", "process_budget"]),
                         "pending_reason": "Engineering contract fixture; no task was executed."})
        self.manifest = {"schema_version": 1, "status": "frozen-preparation", "treatment": "resource-access", "conditions": rows,
                         "inputs": {"corpus_reference": copied["corpus"], "case_ids": [row["id"] for row in corpus["cases"]],
                                    "rights": "historical-owned-synthetic-development-only", "split": "exposed-development"},
                         "migration": {"comparison": "migration-history-only", "installed_revision": "14", "candidate_revision": "21",
                                       "initial_freeze_reference": copied["initial"], "direct_linkage_reference": copied["linkage"],
                                       "causal_resource_claim": False},
                         "round_lineage": {"direct_reviews_sha256": copied["reviews"]["sha256"], "direct_reviews_reference": copied["reviews"],
                                           "rounds_observed": rounds, "new_round_allocated": None, "development_max_rounds": 3, "holdout_runs": 1},
                         "human_queue_reference": self.record("human-queue.json", {"status": "pending"}), "holdout": "pending/NOT_CALLABLE"}

    def record(self, name, value):
        target = self.context / name
        atomic_json(target, value)
        return {"path": name, "sha256": digest_file(target)}

    def compare(self, manifest=None):
        return checker.compare(self.manifest if manifest is None else manifest, work_context=self.context)

    def row(self, manifest, identity="same-agent/resource-off"):
        return next(row for row in manifest["conditions"] if row["id"] == identity)

    def test_preparation_preserves_all_variants_without_quality_acceptance(self):
        result = self.compare()
        self.assertEqual(result["integrity"], "pass")
        self.assertEqual(len(result["conditions"]), 6)
        self.assertEqual(result["accepted_task_count"], 0)
        self.assertEqual(result["resource_benefit"], "unknown")
        self.assertEqual(result["qualification"], "pending")

    def test_missing_conditions_and_fields_fail(self):
        for identity in checker.CONDITIONS:
            broken = deepcopy(self.manifest)
            broken["conditions"] = [row for row in broken["conditions"] if row["id"] != identity]
            with self.subTest(condition=identity), self.assertRaises(ContractError):
                self.compare(broken)
        for key in self.manifest:
            broken = deepcopy(self.manifest)
            broken.pop(key)
            with self.subTest(field=key), self.assertRaises(ContractError):
                self.compare(broken)

    def test_variant_treatment_and_field_types_fail(self):
        for field, value in [("variant", "no-skill"), ("resource_access", "none"), ("subject_revision", True),
                             ("pending_reason", ""), ("model", {"requested": 42, "resolved": None, "effective": None})]:
            broken = deepcopy(self.manifest)
            self.row(broken)[field] = value
            with self.subTest(field=field), self.assertRaises(ContractError):
                self.compare(broken)

    def test_real_reference_hash_missing_file_and_escape_fail(self):
        for path, digest in [("missing.json", "0" * 64), ("../corpus.json", "0" * 64), ("corpus.json", "0" * 64)]:
            broken = deepcopy(self.manifest)
            broken["inputs"]["corpus_reference"] = {"path": path, "sha256": digest}
            with self.subTest(path=path), self.assertRaises(ContractError):
                self.compare(broken)

    def test_pair_rejects_changed_base_wrapper_model_and_budget(self):
        for field in ["base_code", "wrapper"]:
            broken = deepcopy(self.manifest)
            row = self.row(broken)
            reference = self.record("changed-" + field + ".json", {"changed": field})
            row["references"][field], row["hashes"][field] = reference, reference["sha256"]
            with self.subTest(field=field), self.assertRaises(ContractError):
                self.compare(broken)
        for field in ["model", "budget"]:
            broken = deepcopy(self.manifest)
            row = self.row(broken)
            if field == "model":
                row["model"]["requested"] = "different-model"
            else:
                row["gates"]["provider_budget"] = self.record("budget.json", {"status": "test-contract"})
            with self.subTest(field=field), self.assertRaises(ContractError):
                self.compare(broken)

    def test_pair_rejects_config_confounds_even_with_valid_file_hashes(self):
        broken = deepcopy(self.manifest)
        row = self.row(broken)
        config = load_json(self.context / row["references"]["config"]["path"])
        config["seed"] = 11
        reference = self.record("changed-config.json", config)
        row["references"]["config"], row["hashes"]["config"] = reference, reference["sha256"]
        with self.assertRaises(ContractError):
            self.compare(broken)

    def test_completed_observation_needs_actual_output_reference(self):
        broken = deepcopy(self.manifest)
        self.row(broken)["status"] = "completed-unreviewed"
        with self.assertRaises(ContractError):
            self.compare(broken)

    def test_history_cannot_reset_rounds_or_rename_migration(self):
        for field in ["round", "limit", "migration"]:
            broken = deepcopy(self.manifest)
            if field == "round":
                skill = next(key for key, value in broken["round_lineage"]["rounds_observed"].items() if value > 1)
                broken["round_lineage"]["rounds_observed"][skill] = 1
            elif field == "limit":
                broken["round_lineage"]["holdout_runs"] = True
            else:
                broken["migration"]["causal_resource_claim"] = True
            with self.subTest(field=field), self.assertRaises(ContractError):
                self.compare(broken)

    def test_substituted_identity_and_holdout_labels_fail(self):
        broken = deepcopy(self.manifest)
        original = broken["inputs"]["case_ids"][0].split(":")[0]
        broken["inputs"]["case_ids"] = [identity.replace(original + ":", "nckh-substitute:") for identity in broken["inputs"]["case_ids"]]
        with self.assertRaises(ContractError):
            self.compare(broken)
        broken = deepcopy(self.manifest)
        broken["inputs"]["split"] = "protected-holdout"
        with self.assertRaises(ContractError):
            self.compare(broken)
