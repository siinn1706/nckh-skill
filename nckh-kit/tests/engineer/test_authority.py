import unittest

from core.guards import require_operation, xia_mode
from core.schema import ContractError


class EngineerTests(unittest.TestCase):
    def test_xia_modes_and_unknown_flags(self):
        self.assertEqual(xia_mode(["--compare"]), "report-only")
        self.assertEqual(xia_mode([]), "plan-only")
        for flags in [["--fast"], ["--auto"], ["--copy"], ["--compare", "--port"]]:
            with self.assertRaises(ContractError):
                xia_mode(flags)

    def test_diagnosis_and_review_do_not_grant_product_writes(self):
        for grant in [{"diagnose", "local-report-write"}, {"review", "local-report-write"}]:
            with self.assertRaises(ContractError):
                require_operation("product-write", grant=grant)

    def test_backup_is_required_even_when_data_change_is_authorized(self):
        with self.assertRaises(ContractError):
            require_operation("data-change", grant={"data-change"})
        require_operation("data-change", grant={"data-change"}, backup_reference="verified-backup")
