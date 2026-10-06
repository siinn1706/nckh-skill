"""Lock-independent actual authored pack behavior and adverse contract cases."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

from core.owned_resources import read_pack, validate_pack_rows, validate_owned_source, validate_owned_provenance
from core.paths import temporary_tree
from core.research_io import ArtifactReader, ResearchLimits
from core.resources import registry, verify_provenance
from core.schema import ContractError

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("research_pack_lookup", ROOT / "scripts/search-resource.py")
lookup_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lookup_module)


class ResearchPackContractTests(unittest.TestCase):
    def setUp(self):
        self.resources = {row["resource_id"]: row for row in registry(ROOT)["resources"] if row["source_kind"] == "owned-reference"}
        self.resource = copy.deepcopy(self.resources["R-statistical-recipes"])

    def lookup(self, resource=None, **options):
        row = resource or self.resource
        args = {"resource_id": row["resource_id"], "consumer": row["consumers"][0], "domain": row["domain"], "locale": row["locale"], "genre": row["genre"]}
        args.update(options)
        return lookup_module.lookup(**args)

    def test_all_exact_bindings_read_actual_records(self):
        self.assertEqual(4, len(self.resources))
        self.assertEqual(14, sum(len(read_pack(row, ROOT)) for row in self.resources.values()))
        for row in self.resources.values():
            for consumer in row["consumers"]:
                result = self.lookup(row, consumer=consumer)
                self.assertEqual("matched", result["status"])
                self.assertTrue(result["resource_read"])
                self.assertTrue(result["records"])

    def test_query_selects_actual_card_not_suite_generalization(self):
        result = self.lookup(self.resources["R-aiops-benchmark-cards"], query="RE2-SS")
        self.assertEqual(1, len(result["records"]))
        self.assertIn("logs", json.dumps(result["records"]))
        self.assertNotIn('"traces"', json.dumps(result["records"]))

    def test_off_never_needs_registry_or_resource_files(self):
        with temporary_tree(ROOT.parent) as folder:
            result = self.lookup(root=Path(folder), resource_access="off")
        self.assertEqual("resource-disabled", result["status"])
        self.assertFalse(result["resource_read"])

    def test_mismatches_do_not_open_resource_files(self):
        with temporary_tree(ROOT.parent) as folder:
            root = Path(folder)
            path = root / "core/registry/catalog/resources.json"
            path.parent.mkdir(parents=True)
            path.write_bytes((ROOT / "core/registry/catalog/resources.json").read_bytes())
            (path.parent / "skills.json").write_bytes((ROOT / "core/registry/catalog/skills.json").read_bytes())
            for options in ({"consumer": "nckh-data"}, {"locale": "vi"}, {"genre": "marketing-copy"}):
                with self.assertRaises(ValueError):
                    self.lookup(root=root, **options)
            result = self.lookup(root=root, domain="marketing")
            self.assertFalse(result["resource_read"])

    def test_private_unknown_fields_rejected(self):
        rows = copy.deepcopy(read_pack(self.resource, ROOT))
        for name in ("raw_logs", "gold", "code", "instructions", "provider_trace"):
            rows[0][name] = "not allowed"
            with self.assertRaises(ContractError):
                validate_pack_rows(self.resource, rows)
            del rows[0][name]

    def test_duplicate_ids_and_wrong_kind_rejected(self):
        rows = copy.deepcopy(read_pack(self.resource, ROOT))
        rows[1]["id"] = rows[0]["id"]
        with self.assertRaises(ContractError):
            validate_pack_rows(self.resource, rows)
        rows = read_pack(self.resource, ROOT)
        rows[0]["kind"] = "telemetry-field"
        with self.assertRaises(ContractError):
            validate_pack_rows(self.resource, rows)

    def test_context_and_contribution_membership_drift(self):
        for name, value in (("domain", "marketing"), ("language", "vi"), ("consumer", ["nckh-data"]), ("source_ids", ["unreviewed"])):
            rows = read_pack(self.resource, ROOT)
            rows[0][name] = value
            with self.assertRaises(ContractError):
                validate_pack_rows(self.resource, rows)

    def test_missing_reverse_contribution_binding_rejected(self):
        rows = read_pack(self.resource, ROOT)
        rows[0]["source_ids"].pop()
        with self.assertRaises(ContractError):
            validate_pack_rows(self.resource, rows)

    def test_domain_mismatch_query_and_output_are_bounded(self):
        with self.assertRaises(ValueError):
            self.lookup(domain="marketing", query="x" * 4097)
        with self.assertRaises(ContractError):
            self.lookup(domain="marketing", limits=ResearchLimits(output_bytes=1))

    def test_exact_serializer_includes_indentation_and_newline(self):
        reader = ArtifactReader(ROOT, ResearchLimits(output_bytes=15))
        self.assertLessEqual(len(reader.output({"x": 1234567})), 15)
        with self.assertRaises(ContractError):
            reader.output({"x": 1234567}, indent=2, newline=True)

    def test_unknown_registry_consumer_cannot_read(self):
        with temporary_tree(ROOT.parent) as root:
            path = root / "core/registry/catalog/resources.json"
            path.parent.mkdir(parents=True)
            catalog = json.loads((ROOT / "core/registry/catalog/resources.json").read_text())
            for row in catalog["resources"]:
                if row["resource_id"] == self.resource["resource_id"]:
                    row["consumers"].append("nckh-unknown")
            path.write_text(json.dumps(catalog))
            (path.parent / "skills.json").write_bytes((ROOT / "core/registry/catalog/skills.json").read_bytes())
            with self.assertRaises(ValueError):
                self.lookup(root=root, consumer="nckh-unknown")

    def test_hash_and_notice_bindings_cannot_drift(self):
        for field in ("sha256", "notice_sha256", "license_sha256"):
            row = copy.deepcopy(self.resource)
            row["source"][field] = "0" * 64
            with self.assertRaises(ContractError):
                validate_owned_source(row)

    def test_unknown_commit_cannot_masquerade_as_pin(self):
        row = copy.deepcopy(self.resource["owned_provenance"])
        row["contributions"][0]["version_kind"] = "git-commit"
        with self.assertRaises(ContractError):
            validate_owned_provenance(row, self.resource["source"]["sha256"])

    def test_owned_variant_cannot_claim_public_mit_rights(self):
        for field, value in (("license", "MIT"), ("rights_scope", "redistributable"), ("license_kind", "verbatim-upstream")):
            row = copy.deepcopy(self.resource)
            row["source"][field] = value
            with self.assertRaises(ContractError):
                validate_owned_source(row)

    def test_pin_requires_owned_original_notice(self):
        provenance = self.resource["owned_provenance"]
        files = {ref["path"]: {"sha256": ref["sha256"], "rights": "owned-local-package"} for ref in (provenance["rights_record"], provenance["attribution_record"])}
        pin = {"sha256": self.resource["source"]["sha256"], "rights": "owned-reference", "provenance": provenance}
        verify_provenance(ROOT, self.resource["path"], pin, files, check_files=True)
        files[provenance["rights_record"]["path"]]["rights"] = "copied-upstream"
        with self.assertRaises(ContractError):
            verify_provenance(ROOT, self.resource["path"], pin, files)

    def test_unexpected_record_membership_and_source_keys_fail(self):
        row = copy.deepcopy(self.resource)
        row["owned_provenance"]["record_ids"].append("invented")
        with self.assertRaises(ContractError):
            validate_owned_source(row)
        row = copy.deepcopy(self.resource)
        row["source"]["upstream_path"] = "copied.py"
        with self.assertRaises(ContractError):
            validate_owned_source(row)

    def test_nonfinite_duplicate_json_and_depth_rejected(self):
        for data in ('{"x":NaN}', '{"x":1e999}', '{"x":1,"x":2}', '[' * 66 + '0' + ']' * 66):
            with self.assertRaises(ContractError):
                ArtifactReader(ROOT).parse(data)

    def test_actual_per_file_aggregate_record_and_output_caps(self):
        for limits in (ResearchLimits(file_bytes=1), ResearchLimits(aggregate_bytes=1), ResearchLimits(records=1), ResearchLimits(output_bytes=1)):
            with self.assertRaises(ContractError):
                self.lookup(limits=limits)

    def test_query_budget_rejects_oversize(self):
        with self.assertRaises(ValueError):
            self.lookup(query="x " * 65)


if __name__ == "__main__":
    unittest.main()
