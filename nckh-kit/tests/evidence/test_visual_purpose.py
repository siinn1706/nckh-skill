import json
import shutil
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path

from core.guards import check_visual_purpose
from core.paths import atomic_json, digest_file, temporary_tree


ROOT = Path(__file__).resolve().parents[2]


class VisualPurposeTests(unittest.TestCase):
    def setUp(self):
        self.tree = temporary_tree()
        self.project = self.tree.__enter__()
        self.addCleanup(self.tree.__exit__, None, None, None)
        data = self.project / "observations.jsonl"
        shutil.copyfile(ROOT / "core/profiles/resources/worldbank-series.jsonl", data)
        source = json.loads(data.read_text(encoding="utf8").splitlines()[0])
        self.sources = {"E-worldbank": {"file": {"path": data.name, "sha256": digest_file(data)},
            "rights": "CC-BY-4.0", "access": "public-data", "locator": source["locator"], "data_origin": "observed"}}
        self.purpose = {"kind": "chart", "purpose_question": "How does this dated population series change?",
            "research_object": "Viet Nam total population snapshot", "artifact_role": "research-evidence",
            "evidence_ids": ["E-worldbank"], "source_access": "public-data", "data_origin": "observed",
            "inference_labels": [], "non_evidentiary_label": "", "required_marks": ["population-2025"],
            "uncertainty": "Published snapshot may be revised; source blank unit is preserved.",
            "uncertainty_not_applicable_reason": "", "source_to_mark": [{"mark_id": "population-2025",
                "evidence_id": "E-worldbank", "source_sha256": digest_file(data), "origin": "observed-field",
                "pointer": "/0/data/0/value", "value": source["data"][0]["value"], "unit": "", "denominator": None,
                "unit_pointer": "/0/data/0/unit", "denominator_pointer": ""}]}
        self.brief = {"schema_version": 1, "outcome": "Research chart", "domain": "research", "language": "en",
            "scope": [], "constraints": [], "non_goals": [], "acceptance": [], "mode": "auto", "visual_purpose": self.purpose}

    def check(self):
        return check_visual_purpose(self.brief, project=self.project, sources=self.sources)

    def test_actual_dated_observations_and_blank_units_pass_only_integrity(self):
        result = self.check()
        self.assertEqual(result["decision"], "allow")
        self.assertEqual(result["scientific_acceptance"], "pending")
        self.assertEqual(result["native_acceptance"], "unverified")
        self.purpose["source_to_mark"][0]["unit"] = "people"
        self.assertEqual(self.check()["decision"], "block")

    def test_missing_purpose_domain_keyword_and_branding_cannot_authorize_generation(self):
        self.assertEqual(check_visual_purpose({"domain": "research"})["decision"], "pending")
        for role in ("logo", "branding", "ad", "banner", "thumbnail", "generic-artwork"):
            self.purpose["artifact_role"] = role
            before = {p.name: digest_file(p) for p in self.project.iterdir() if p.is_file()}
            self.assertEqual(self.check()["decision"], "block")
            self.assertEqual(before, {p.name: digest_file(p) for p in self.project.iterdir() if p.is_file()})
        self.purpose["artifact_role"] = "research-evidence"
        self.purpose["purpose_question"] = " "
        self.assertEqual(self.check()["decision"], "pending")

    def test_invented_values_missing_marks_rights_and_grant_fields_fail(self):
        original = deepcopy(self.purpose)
        for mutation in ("value", "mark", "rights", "grant", "hash", "path"):
            self.brief["visual_purpose"] = deepcopy(original)
            self.purpose = self.brief["visual_purpose"]
            if mutation == "value":
                self.purpose["source_to_mark"][0]["value"] += 1
            elif mutation == "mark":
                self.purpose["required_marks"].append("unmapped-label")
            elif mutation == "rights":
                self.sources["E-worldbank"]["rights"] = "pending"
            elif mutation == "grant":
                self.purpose["grant"] = True
            elif mutation == "hash":
                self.purpose["source_to_mark"][0]["source_sha256"] = "0" * 64
            else:
                self.sources["E-worldbank"]["file"]["path"] = "../observations.jsonl"
            with self.subTest(mutation=mutation):
                self.assertEqual(self.check()["decision"], "block")
            self.sources["E-worldbank"]["rights"] = "CC-BY-4.0"

    def computation(self, origin):
        code = self.project / "scale-fixture.py"
        code.write_text('import json,sys\nfrom pathlib import Path\np=Path(sys.argv[1]); v=json.loads(p.read_text().splitlines()[0])["data"][0]["value"]\nparams=json.loads(Path(sys.argv[2]).read_text())\nprint(json.dumps({"value":v*params["scale"],"unit":"","denominator":None}))\n', encoding="utf8")
        params = {"scale": 2}
        atomic_json(self.project / "transform.json", params)
        command = [sys.executable, "-I", str(code), str(self.project / "observations.jsonl"), str(self.project / "transform.json")]
        process = subprocess.run(command, cwd=self.project, capture_output=True, timeout=10, check=True)
        output = self.project / "computed.json"
        output.write_bytes(process.stdout)
        def ref(name):
            return {"path": name, "sha256": digest_file(self.project / name)}
        run = {"status": "completed-unreviewed", "exit_status": process.returncode,
            "command": command, "code_sha256": digest_file(code), "source_sha256": digest_file(self.project / "observations.jsonl"),
            "transform_sha256": digest_file(self.project / "transform.json"),
            "output_sha256": digest_file(output), "parameters": params, "cleanup": "owned-subprocess-exited",
            "evidence_class": "actual-local-diagnostic-calculation", "scientific_acceptance": "pending"}
        atomic_json(self.project / "run.json", run)
        self.purpose.update(data_origin=origin, evidence_ids=["E-run"], source_access="owned-run",
            non_evidentiary_label="not observed measurements", uncertainty="",
            uncertainty_not_applicable_reason="Deterministic diagnostic fixture; no observational/statistical estimate.",
            computation={"model": "diagnostic scale model", "version": "1", "run_locator": "owned local unittest process",
                "parameters": params, "code": ref(code.name), "source": ref("observations.jsonl"),
                "transform": ref("transform.json"), "output": ref(output.name), "run_receipt": ref("run.json")})
        self.sources = {"E-run": {"file": ref(output.name), "rights": "owned", "access": "owned-run",
            "locator": "actual fixture stdout", "data_origin": origin}}
        mark = self.purpose["source_to_mark"][0]
        mark.update(evidence_id="E-run", source_sha256=digest_file(output), origin="calculation-output",
            pointer="/value", value=json.loads(process.stdout)["value"], unit_pointer="/unit", denominator_pointer="/denominator")

    def test_real_calculation_and_labeled_simulation_are_distinct_from_observations(self):
        for origin in ("derived", "computational", "simulation"):
            self.computation(origin)
            with self.subTest(origin=origin):
                self.assertEqual(self.check()["decision"], "allow")
                self.purpose["non_evidentiary_label"] = "observed measurements"
                self.assertEqual(self.check()["decision"], "pending")

    def test_fake_run_missing_uncertainty_and_drifted_output_fail(self):
        self.computation("simulation")
        self.purpose["computation"]["run_receipt"]["sha256"] = "0" * 64
        self.assertEqual(self.check()["decision"], "block")
        self.purpose["computation"]["run_receipt"]["sha256"] = digest_file(self.project / "run.json")
        self.purpose["uncertainty_not_applicable_reason"] = ""
        self.assertEqual(self.check()["decision"], "pending")
        self.purpose["uncertainty"] = "Diagnostic model uncertainty remains unreviewed."
        (self.project / "computed.json").write_text('{"value":999}', encoding="utf8")
        self.assertEqual(self.check()["decision"], "block")

    def test_sourced_mechanism_and_non_evidentiary_illustration_need_labels(self):
        atomic_json(self.project / "reference.json", {"claim": "Owned synthetic diagram-reference fixture."})
        reference = {"path": "reference.json", "sha256": digest_file(self.project / "reference.json")}
        self.sources = {"E-ref": {"file": reference, "rights": "owned", "access": "user-supplied", "locator": "/claim", "data_origin": "none"}}
        self.purpose.update(kind="mechanism", artifact_role="mechanism-explanation", data_origin="none", evidence_ids=["E-ref"], source_access="user-supplied", inference_labels=["population-2025"])
        self.purpose["source_to_mark"][0].update(evidence_id="E-ref", source_sha256=reference["sha256"], origin="inference", pointer="/claim", unit_pointer="", value="hypothetical edge")
        self.assertEqual(self.check()["decision"], "allow")

        self.purpose["inference_labels"] = []
        self.assertEqual(self.check()["decision"], "pending")
        self.purpose.update(kind="illustration", artifact_role="research-illustration", non_evidentiary_label="illustrative/non-evidentiary")
        self.purpose["source_to_mark"][0]["origin"] = "illustration"
        self.assertEqual(self.check()["decision"], "allow")

    def test_changed_transform_cannot_reuse_a_prior_run_receipt(self):
        self.computation("derived")
        atomic_json(self.project / "transform.json", {"scale": 3})
        self.purpose["computation"]["transform"]["sha256"] = digest_file(self.project / "transform.json")
        self.assertEqual(self.check()["decision"], "block")
