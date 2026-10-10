import unittest

from core.paths import digest_record
from core.ledger import validate_task_state
from core.schema import ContractError, validate, validate_record
from core.state import (HostGrant, aggregate, feedback, invalidate, new_task,
                        review_boundary, transition)
from core.models import delegation_allowed, resolve_model


class StateTests(unittest.TestCase):
    def setUp(self):
        self.brief = {"outcome": "repair one file", "scope": ["a.py"]}
        self.task = new_task(self.brief, mode="auto", revision="r1")
        self.grant = HostGrant("user-current-turn", digest_record(self.brief),
                               frozenset({"local-product-write"}))

    def test_new_task_matches_current_task_state_contract(self):
        self.assertEqual(self.task["schema_version"], 2)
        validate_record("task-state", self.task)
        self.assertEqual(validate_task_state(self.task)["verdict"], "VERIFIED")
        legacy = dict(self.task, schema_version=1)
        with self.assertRaises(ContractError):
            validate_record("task-state", legacy)

    def test_serialized_authorization_cannot_grant_scope(self):
        with self.assertRaises(ContractError):
            transition(self.task, "authorized", grant={"authorized": True})
        other = HostGrant("user", "different-scope", self.grant.operations)
        with self.assertRaises(ContractError):
            transition(self.task, "authorized", grant=other)

    def test_auto_progresses_without_routine_human_pause(self):
        task = transition(self.task, "authorized", grant=self.grant)
        task = transition(task, "running", grant=self.grant)
        task = transition(task, "checking")
        task["gates"] = [{"id": "regression", "required": True, "status": "pass",
                          "revision": "r1", "evidence_reference": "test-receipt"}]
        task = transition(task, "ready-for-review")
        self.assertEqual(transition(task, "accepted")["status"], "accepted")

    def test_human_review_cannot_mask_failed_gate_or_stale_pass(self):
        gate = {"id": "science", "required": True, "status": "pending", "revision": "r1"}
        self.assertEqual(aggregate([gate], "r1"), "pending")
        gate.update(status="fail", human_reviewed=True)
        self.assertEqual(aggregate([gate], "r1"), "failed")
        gate.update(status="pass", evidence_reference="observed")
        self.assertEqual(aggregate([gate], "r2"), "pending")

    def test_timeout_requires_reconciliation(self):
        task = transition(self.task, "authorized", grant=self.grant)
        task["attempts"] = [{"status": "timeout-unknown", "handle": "h1"}]
        with self.assertRaises(ContractError):
            transition(task, "running", grant=self.grant)
        task["attempts"][0]["status"] = "reconciled-failed"
        self.assertEqual(transition(task, "running", grant=self.grant)["status"], "running")

    def test_invalidation_preserves_history_and_unaffected_checks(self):
        self.task["gates"] = [{"id": "source", "required": True, "status": "pass", "revision": "r1"},
                              {"id": "claim", "required": True, "status": "pass", "revision": "r1", "depends_on": ["source"]},
                              {"id": "layout", "required": True, "status": "pass", "revision": "r1"}]
        task = invalidate(self.task, ["source"], revision="r2")
        self.assertEqual([g["status"] for g in task["gates"]], ["stale", "stale", "pass"])
        self.assertEqual(task["gates"][2]["revision"], "r2")
        self.assertEqual(self.task["gates"][0]["status"], "pass")

    def test_interactive_boundary_binds_real_feedback_and_hash(self):
        self.task.update(mode="interactive", status="checking")
        task = review_boundary(self.task, artifact="pilot.svg", artifact_hash="sha1", locked_scope="pilot")
        with self.assertRaises(ContractError):
            transition(task, "running", grant=self.grant)
        with self.assertRaises(ContractError):
            feedback(task, decision="approve", revision="r1", artifact_hash="wrong", human_reference="user")
        task = feedback(task, decision="approve", revision="r1", artifact_hash="sha1", human_reference="user")
        self.assertEqual(transition(task, "running", grant=self.grant)["status"], "running")


class ModelAndSchemaTests(unittest.TestCase):
    def test_deep_unavailable_never_downgrades(self):
        result = resolve_model(tier="deep", profile="balanced", requested="auto", effort="high",
                               capabilities={"per_agent_override": True, "models": [
                                   {"id": "small", "tiers": ["fast"], "efforts": ["high"], "availability": "observed"}]},
                               allowed_models={"small"})
        self.assertIsNone(result["resolved_model"])
        self.assertEqual(result["effective_model"], "unknown")

    def test_no_benefit_same_model_delegation_is_rejected(self):
        self.assertFalse(delegation_allowed(["cheaper-eligible"], same_model=True, same_purpose=True))
        self.assertTrue(delegation_allowed(["fresh-context"], same_model=True, same_purpose=True))

    def test_schema_subset_rejects_unknown_keywords_and_bool_number(self):
        with self.assertRaises(ContractError):
            validate({}, {"type": "object", "oneOf": []})
        with self.assertRaises(ContractError):
            validate(True, {"type": "integer"})
        with self.assertRaises(ContractError):
            validate({"schema_version": 2}, {"type": "object", "additionalProperties": False,
                     "properties": {"schema_version": {"const": 1}}})

    def test_boolean_versions_and_nonfinite_numbers_rejected(self):
        for schema in [{"const": 1}, {"enum": [1]}, {"const": {"revision": 1}}]:
            with self.assertRaises(ContractError):
                validate({"revision": True} if isinstance(schema.get("const"), dict) else True, schema)
        for value in [float("nan"), float("inf"), -float("inf")]:
            with self.assertRaises(ContractError):
                validate(value, {"type": "number"})
