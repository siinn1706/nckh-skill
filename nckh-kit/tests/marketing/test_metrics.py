import unittest

from core.guards import experiment_design, metric, require_operation
from core.schema import ContractError


class MarketingTests(unittest.TestCase):
    def test_missing_denominator_or_time_does_not_become_zero(self):
        for denominator, time_range in [(None, "one week"), (0, "one week"), (10, "")]:
            with self.assertRaises(ContractError):
                metric(2, denominator, time_range=time_range, population="users")
        result = metric(2, 10, time_range="2026-09", population="eligible users")
        self.assertEqual(result["rate"], .2)
        self.assertEqual(result["causal_lift"], "unverified")

    def test_drafting_does_not_grant_marketing_mutations(self):
        for operation in ["spend", "send", "publish", "upload-contacts", "change-traffic"]:
            with self.assertRaises(ContractError):
                require_operation(operation, grant={"draft", "analyze"})

    def test_experiment_protocol_and_peeking(self):
        with self.assertRaises(ContractError):
            experiment_design({"hypothesis": "improvement"})
        design = dict.fromkeys(["hypothesis", "unit", "randomization", "allocation", "primary_metric",
                               "denominator", "guardrails", "sample_rationale", "stopping", "analysis"], "specified")
        design["stopping"] = "first-significant-p-value"
        with self.assertRaises(ContractError):
            experiment_design(design)
