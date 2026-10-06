import importlib.util
import json
import os
import unittest
from copy import deepcopy
from pathlib import Path

from core.paths import atomic_json, digest_file, temporary_tree
from core.resources import (REGISTRY_PATH, _validate_source, registry,
                            resource_provenance, verify_provenance)
from core.schema import ContractError


ROOT = Path(os.environ.get("NCKH_RESOURCE_TEST_ROOT", Path(__file__).resolve().parents[2]))
spec = importlib.util.spec_from_file_location("real_source_reader", ROOT / "scripts/search-resource.py")
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


class RealSourceTests(unittest.TestCase):
    def test_ambiguous_and_nonfinite_json_is_rejected(self):
        for text in ['{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', '{"x":1e999}']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                reader.strict_json(text)

    def test_legacy_commit_license_and_verbatim_guards_remain(self):
        base = registry(ROOT)["resources"][0]
        for field, value in [("version", "z" * 40), ("license", "CC-BY-4.0"),
                             ("license_kind", "owned-rights-record")]:
            row = deepcopy(base)
            row["source"][field] = value
            with self.subTest(field=field), self.assertRaises(ContractError):
                _validate_source(row)
            with self.subTest(reader_field=field), self.assertRaises(ValueError):
                reader._verify_source(row, ROOT)
        row = deepcopy(base)
        row["copied_vs_reauthored"] = "normalized-with-lineage"
        with self.assertRaises(ContractError):
            _validate_source(row)

    def test_unrecorded_support_dependency_cannot_become_owned(self):
        with temporary_tree() as isolated:
            catalog = json.loads((ROOT / REGISTRY_PATH).read_text(encoding="utf-8"))
            catalog["resources"][0]["requires"].append("core/profiles/resources/unrecorded-response.xml")
            atomic_json(isolated / REGISTRY_PATH, catalog)
            atomic_json(isolated / "core/registry/catalog/skills.json",
                        json.loads((ROOT / "core/registry/catalog/skills.json").read_text(encoding="utf-8")))
            with self.assertRaisesRegex(ContractError, "resource/rights"):
                registry(isolated, check_files=False)

    def test_metadata_only_record_rejects_private_task_content(self):
        resource = {"copied_vs_reauthored": "metadata-only-reference"}
        for key in ["problem_statement", "patch", "test_patch", "issue_body", "dataset_row", "code",
                    "body", "issue_text_reference"]:
            data = json.dumps({"source_id": "probe", "nested": {key: "private"}}).encode("utf-8")
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "private fields"):
                reader._jsonl_records(resource, {}, data, "")

    def test_extracted_metadata_scope_and_packaged_lineage_are_bound(self):
        provenance = {
            "source_kind": "retrieved-snapshot", "repository": "https://example.test/source",
            "version": "snapshot", "upstream_path": "response", "upstream_sha256": "b" * 64,
            "as_of": "2026-10-03", "license": "CC-BY-4.0",
            "license_path": "core/profiles/resources/rights.md", "license_sha256": "d" * 64,
            "notice_path": "", "notice_sha256": "", "redistribution": "permitted-with-notices",
            "review_reference": "review", "version_kind": "api-snapshot",
            "rights_scope": "redistributable", "retrieved_at": "2026-10-03T00:00:00Z",
            "retrieval_timezone": "UTC", "copied_vs_reauthored": "normalized-with-lineage",
            "artifact_sha256": "a" * 64, "upstream_sha256s": ["b" * 64],
            "lineage": [{"kind": "source-response", "locator": "response", "sha256": "b" * 64}]
        }
        pin = {"rights": "copied-upstream", "sha256": "a" * 64, "provenance": provenance}
        files = {provenance["license_path"]: {"sha256": "d" * 64}}
        relative = "core/profiles/resources/derived.jsonl"
        verify_provenance(ROOT, relative, pin, files)
        broken = deepcopy(pin)
        broken["provenance"]["copied_vs_reauthored"] = "metadata-only-reference"
        with self.assertRaisesRegex(ContractError, "unresolved"):
            verify_provenance(ROOT, relative, broken, files)
        raw = "core/profiles/resources/raw.json"
        provenance["lineage"][0]["path"] = raw
        files[raw] = {"sha256": "c" * 64, "rights": "owned-local-package"}
        with self.assertRaisesRegex(ContractError, "pinned lineage"):
            verify_provenance(ROOT, relative, pin, files)
        files[raw]["sha256"] = "b" * 64
        with self.assertRaisesRegex(ContractError, "third-party"):
            verify_provenance(ROOT, relative, pin, files)
        files[raw] = {"sha256": "b" * 64, "rights": "copied-upstream",
                      "provenance": {"upstream_sha256": "b" * 64}}
        verify_provenance(ROOT, relative, pin, files)
        with temporary_tree() as isolated:
            path = isolated / raw
            path.parent.mkdir(parents=True)
            path.write_text("drift", encoding="utf-8")
            with self.assertRaisesRegex(ContractError, "lineage bytes changed"):
                verify_provenance(isolated, relative, pin, files, check_files=True)

    def test_real_snapshot_records_and_context_guards(self):
        snapshots = [row for row in registry(ROOT)["resources"] if row["source_kind"] == "retrieved-snapshot"]
        self.assertGreaterEqual(len(snapshots), 5)
        observed = {}
        for row in snapshots:
            args = {"domain": row["domain"], "locale": row["locale"], "genre": row["genre"], "root": ROOT}
            result = reader.lookup(row["resource_id"], row["consumers"][0], **args)
            self.assertTrue(result["resource_read"])
            self.assertTrue(result["records"])
            self.assertEqual(result["resource_sha256"], row["source"]["sha256"])
            observed[row["resource_id"]] = result
            unmatched = reader.lookup(row["resource_id"], row["consumers"][0], query="zz-no-actual-snapshot-record", **args)
            self.assertEqual(unmatched["records"], [])
            wrong_domain = reader.lookup(row["resource_id"], row["consumers"][0], **{**args, "domain": "unrelated-domain"})
            self.assertFalse(wrong_domain["resource_read"])
            with self.assertRaisesRegex(ValueError, "locale/genre"):
                reader.lookup(row["resource_id"], row["consumers"][0], **{**args, "locale": "wrong-locale"})
            off = reader.lookup(row["resource_id"], row["consumers"][0], **{**args, "root": ROOT / "absent"},
                                resource_access="off")
            self.assertFalse(off["resource_read"])
        vi = [record["content"] for result in observed.values() for record in result["records"]
              if record["content"].get("actual_passage") is True]
        self.assertEqual({row["source_id"] for row in vi},
                         {"vi-wikisource-179899", "vi-wikisource-19383", "vi-wikisource-71961"})
        self.assertTrue(all(row["text"] and row["parent_oldid"] for row in vi))

    def test_snapshot_pin_rejects_unresolved_rights(self):
        mapping = resource_provenance(ROOT)
        path, provenance = next((path, value) for path, value in mapping.items()
                                if value["source_kind"] == "retrieved-snapshot"
                                and value.get("copied_vs_reauthored") == "normalized-with-lineage")
        files = {relative: {"sha256": digest_file(ROOT / relative)}
                 for relative in {provenance["license_path"], provenance["notice_path"]} if relative}
        pin = {"rights": "copied-upstream", "sha256": digest_file(ROOT / path), "provenance": provenance}
        verify_provenance(ROOT, path, pin, files)
        for change in [{"rights_scope": "reference-only", "redistribution": "permitted-with-notices"},
                       {"rights_scope": "reference-only", "redistribution": "reference-only"},
                       {"version_kind": "unknown"}, {"retrieval_timezone": ""}]:
            broken = deepcopy(pin)
            broken["provenance"].update(change)
            with self.subTest(change=change), self.assertRaises(ContractError):
                verify_provenance(ROOT, path, broken, files)
