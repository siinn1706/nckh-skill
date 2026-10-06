"""Synthetic contract fixtures never count as observed runs or scientific evidence."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import shutil
import sys
import unittest

from core.experiments import manifest_bindings, validate_experiment_manifest, validate_run_receipt
from core.paths import temporary_tree
from core.research_io import ArtifactReader, ResearchLimits
from core.schema import ContractError
from tests.research.test_aiops import forecast_readout_fixture
from tests.research.test_datasets import save_fixture

ROOT = Path(__file__).resolve().parents[2]
def bind(root, name):
    return {"path": name, "sha256": hashlib.sha256((root / name).read_bytes()).hexdigest()}

def experiment_fixture(root):
    evaluation = forecast_readout_fixture(root)
    parents = {row["kind"]: json.loads((root / row["reference"]["path"]).read_text()) for row in evaluation["inputs"]}
    (root / "rights.md").write_text("Synthetic fixture; no real data or runtime grant")
    parents["dataset"]["sources"][0]["rights_reference"] = "rights.md"
    dataset_ref = save_fixture(root, "dataset.json", parents["dataset"])
    parents["split"]["dataset"] = dataset_ref
    evaluation["benchmark"]["rights_reference"] = "rights.md"
    evaluation.update(stage="protocol", predictions=[], results=[], runs=[], failures=[])
    evaluation["inputs"] = [{"kind": kind, "reference": save_fixture(root, kind + ".json", value)} for kind, value in parents.items()]
    evaluation_ref = save_fixture(root, "evaluation.json", evaluation)
    (root / "protocol.md").write_text("Synthetic frozen protocol; no measured run")
    # The statistics fixture protocol was separately bound in the existing helper.
    parents["analysis"]["protocol"] = bind(root, "protocol.md")
    analysis_ref = save_fixture(root, "analysis.json", parents["analysis"])
    evaluation["inputs"] = [{"kind": row["kind"], "reference": analysis_ref if row["kind"] == "analysis" else row["reference"]} for row in evaluation["inputs"]]
    evaluation_ref = save_fixture(root, "evaluation.json", evaluation)
    refs = {}
    def collect(value):
        if isinstance(value, dict):
            if set(value) == {"path", "sha256"}:
                refs[value["path"]] = value
            for item in value.values(): collect(item)
        elif isinstance(value, list):
            for item in value: collect(item)
    collect(parents)
    collect(evaluation)
    inputs = [*evaluation["inputs"], {"kind": "evaluation", "reference": evaluation_ref}]
    used = {"protocol.md", "code.json", "config.json", *[row["reference"]["path"] for row in inputs]}
    return {"schema_version": 1, "task_id": "fixture-task", "experiment_id": "synthetic-graph", "stage": "plan",
        "frozen_at": "2026-10-06T09:00:00+07:00", "freeze": None, "protocol": bind(root, "protocol.md"), "inputs": inputs,
        "code": [bind(root, "code.json")], "config": [bind(root, "config.json")], "environment": save_fixture(root, "environment.json", {"fixture": "not an actual environment"}),
        "artifacts": [ref for path, ref in refs.items() if path not in used] + [bind(root, "rights.md")],
        "baselines": [row["id"] for row in evaluation["baselines"]], "metrics": [row["id"] for row in evaluation["metrics"]],
        "oracles": ["frozen synthetic prediction arithmetic"], "output_semantics": "computed-from-observed-data",
        "simulation": {"applicability": "not-used", "label": "", "generator": "", "parameters": [], "seed": None,
            "replications": 0, "warmup": "", "conservation": "", "uncertainty": "", "validity_limits": []},
        "limits": {"provider_calls": 0, "egress": "none", "attempts": 2, "file_bytes": 8 * 1024 * 1024, "aggregate_bytes": 32 * 1024 * 1024,
            "records": 100000, "output_bytes": 2 * 1024 * 1024}, "grants": ["synthetic test fixture only"],
        "cleanup_route": "owning temporary_tree context", "amendments": [],
        "expected_outputs": [{"kind": "predictions", "path": "predictions.json"}, {"kind": "metrics", "path": "results.json"}],
        "receipts": [], "outputs": [], "limitations": ["Synthetic fixture only; no genuine run or scientific acceptance"]}

def receipt_fixture(root, manifest):
    manifest_ref = save_fixture(root, "manifest.json", manifest)
    (root / "stdout.txt").write_text("synthetic fixture stdout")
    (root / "stderr.txt").write_text("")
    return {"schema_version": 1, "task_id": manifest["task_id"], "run_id": "synthetic-run", "attempt_id": "synthetic-attempt",
        "manifest": manifest_ref, "inputs": manifest_bindings(manifest), "argv": ["recorded-fixture-only"], "cwd": str(root),
        "environment": manifest["environment"], "started_at": "2026-10-06T09:00:01+07:00", "ended_at": "2026-10-06T09:00:02+07:00",
        "timezone": "Asia/Saigon", "exit_code": 0, "status": "completed-unreviewed",
        "process": {"pid": 1, "parent_pid": 2, "identity_started_at": "2026-10-06T09:00:01+07:00", "cleanup": "exited", "evidence": "synthetic fixture, never an actual process observation"},
        "stdout": bind(root, "stdout.txt"), "stderr": bind(root, "stderr.txt"),
        "outputs": [{"reference": bind(root, name), "kind": kind, "count": count} for name, kind, count in (("predictions.json", "predictions", 2), ("results.json", "metrics", 1))],
        "resources": {"wall_seconds": 1, "cpu_seconds": None, "peak_memory_bytes": None, "provider_cost": None, "coverage": "synthetic chronology only"},
        "output_semantics": "computed-from-observed-data", "failure_reason": "", "deviation_reason": "",
        "reconciliation": {"status": "reaped", "observed_at": "2026-10-06T09:00:02+07:00", "reason": "synthetic fixture"}}

class ExperimentTests(unittest.TestCase):
    def test_plan_remains_not_run(self):
        with temporary_tree(ROOT.parent) as root:
            self.assertEqual("not-run", validate_experiment_manifest(experiment_fixture(root), project=root)["execution"])

    def test_frozen_graph_and_receipt_readout(self):
        with temporary_tree(ROOT.parent) as root:
            manifest = experiment_fixture(root)
            run = receipt_fixture(root, manifest)
            run_ref = save_fixture(root, "receipt.json", run)
            readout = {**manifest, "stage": "readout", "freeze": run["manifest"], "receipts": [run_ref], "outputs": [row["reference"] for row in run["outputs"]]}
            result = validate_experiment_manifest(readout, project=root)
            self.assertEqual("completed-unreviewed", result["execution"])
            self.assertEqual("pending", result["scientific_acceptance"])

    def test_unknown_fields_and_external_paths_fail(self):
        with temporary_tree(ROOT.parent) as root:
            manifest = experiment_fixture(root)
            for change in (lambda row: row.update(execute=True), lambda row: row["code"][0].update(path="../escape.py")):
                mutated = copy.deepcopy(manifest)
                change(mutated)
                with self.assertRaises(ContractError): validate_experiment_manifest(mutated, project=root)

    def test_code_config_data_and_rights_drift_invalidate(self):
        for path in ("code.json", "config.json", "raw.json", "rights.md"):
            with temporary_tree(ROOT.parent) as root:
                manifest = experiment_fixture(root)
                (root / path).write_text("changed")
                with self.assertRaises(ContractError): validate_experiment_manifest(manifest, project=root)

    def test_transitive_bindings_and_parent_lineage_required(self):
        with temporary_tree(ROOT.parent) as root:
            manifest = experiment_fixture(root)
            manifest["artifacts"] = [ref for ref in manifest["artifacts"] if ref["path"] != "normalized.json"]
            with self.assertRaisesRegex(ContractError, "transitive"): validate_experiment_manifest(manifest, project=root)

    def test_artifact_cannot_raise_trusted_caps(self):
        with temporary_tree(ROOT.parent) as root:
            manifest = experiment_fixture(root)
            with self.assertRaisesRegex(ContractError, "raise"): validate_experiment_manifest(manifest, project=root, reader=ArtifactReader(root, ResearchLimits(records=100)))

    def test_declared_lower_cap_applies(self):
        with temporary_tree(ROOT.parent) as root:
            manifest = experiment_fixture(root)
            manifest["limits"]["file_bytes"] = 1
            with self.assertRaises(ContractError): validate_experiment_manifest(manifest, project=root)

    def test_plan_cannot_invent_output_or_scheduled_run(self):
        with temporary_tree(ROOT.parent) as root:
            manifest = experiment_fixture(root)
            manifest["outputs"] = [bind(root, "results.json")]
            with self.assertRaises(ContractError): validate_experiment_manifest(manifest, project=root)

    def test_terminal_run_requires_exit_and_reconciliation(self):
        with temporary_tree(ROOT.parent) as root:
            manifest = experiment_fixture(root)
            original = receipt_fixture(root, manifest)
            for change in (lambda row: row.update(exit_code=1), lambda row: row["process"].update(cleanup="running"), lambda row: row["reconciliation"].update(status="pending"), lambda row: row.update(ended_at="2026-10-05T09:00:00+07:00")):
                row = copy.deepcopy(original); change(row)
                with self.assertRaises(ContractError): validate_run_receipt(row, manifest, original["manifest"], project=root)

    def test_timeout_and_failed_partial_outputs_preserved(self):
        with temporary_tree(ROOT.parent) as root:
            manifest = experiment_fixture(root)
            row = receipt_fixture(root, manifest)
            row.update(status="failed", exit_code=-1, failure_reason="synthetic timeout observation", outputs=[])
            self.assertEqual("failed", validate_run_receipt(row, manifest, row["manifest"], project=root)["status"])
            row["failure_reason"] = ""
            with self.assertRaises(ContractError): validate_run_receipt(row, manifest, row["manifest"], project=root)

    def test_run_output_counts_and_exact_input_hashes(self):
        with temporary_tree(ROOT.parent) as root:
            manifest = experiment_fixture(root); original = receipt_fixture(root, manifest)
            for change in (lambda row: row["outputs"][0].update(count=0), lambda row: row["inputs"].pop(), lambda row: row["inputs"][0].update(sha256="0" * 64)):
                row = copy.deepcopy(original); change(row)
                with self.assertRaises(ContractError): validate_run_receipt(row, manifest, original["manifest"], project=root)

    def test_simulation_label_requires_generator_and_parameters(self):
        with temporary_tree(ROOT.parent) as root:
            manifest = experiment_fixture(root)
            manifest["output_semantics"] = "simulation"
            with self.assertRaisesRegex(ContractError, "simulation"): validate_experiment_manifest(manifest, project=root)

    def test_simulation_parameters_are_frozen_run_inputs(self):
        with temporary_tree(ROOT.parent) as root:
            manifest = experiment_fixture(root)
            parameters = save_fixture(root, "simulation-parameters.json", {"fixture": "not measured"})
            manifest.update(output_semantics="simulation", simulation={"applicability": "simulation",
                "label": "simulation/not observed measurements", "generator": "fixture", "parameters": [parameters],
                "seed": 42, "replications": 2, "warmup": "none", "conservation": "fixture", "uncertainty": "none",
                "validity_limits": ["fixture only"]})
            self.assertEqual(validate_experiment_manifest(manifest, project=root)["execution"], "not-run")
            run = receipt_fixture(root, manifest)
            run["output_semantics"] = "simulation"
            self.assertEqual(validate_run_receipt(run, manifest, run["manifest"], project=root)["contract"], "pass")
            run["inputs"] = [ref for ref in run["inputs"] if ref != parameters]
            with self.assertRaisesRegex(ContractError, "every exact frozen"):
                validate_run_receipt(run, manifest, run["manifest"], project=root)

    def test_retry_keeps_distinct_partial_outputs_and_success(self):
        with temporary_tree(ROOT.parent) as root:
            manifest = experiment_fixture(root)
            manifest["expected_outputs"] = [{"attempt_id": attempt, "kind": kind, "path": attempt + "-" + name}
                for attempt in ("first", "second") for kind, name in (("predictions", "predictions.json"), ("metrics", "results.json"))]
            self.assertEqual(validate_experiment_manifest(manifest, project=root)["execution"], "not-run")
            first = receipt_fixture(root, manifest)
            first.update(attempt_id="first", run_id="first-run", status="failed", exit_code=1, failure_reason="synthetic partial failure")
            first["outputs"] = [{"kind": "predictions", "reference": save_fixture(root, "first-predictions.json", []), "count": 0}]
            second = receipt_fixture(root, manifest)
            second.update(attempt_id="second", run_id="second-run")
            for item in second["outputs"]:
                name = item["reference"]["path"]
                item["reference"] = save_fixture(root, "second-" + name, json.loads((root / name).read_text()))
            receipts = [save_fixture(root, attempt + "-receipt.json", row) for attempt, row in (("first", first), ("second", second))]
            readout = {**manifest, "stage": "readout", "freeze": first["manifest"], "receipts": receipts,
                       "outputs": [item["reference"] for row in (first, second) for item in row["outputs"]]}
            self.assertEqual(validate_experiment_manifest(readout, project=root)["execution"], "preserved-failures")
            second["outputs"][0] = first["outputs"][0]
            with self.assertRaisesRegex(ContractError, "expected artifact paths"):
                validate_run_receipt(second, manifest, second["manifest"], project=root)

    def test_attempt_routes_reject_mixed_missing_and_excess_declarations(self):
        with temporary_tree(ROOT.parent) as root:
            manifest = experiment_fixture(root)
            manifest["expected_outputs"][0]["attempt_id"] = "first"
            with self.assertRaisesRegex(ContractError, "mix"):
                validate_experiment_manifest(manifest, project=root)
            manifest["expected_outputs"][1]["attempt_id"] = "second"
            with self.assertRaisesRegex(ContractError, "each evaluation attempt"):
                validate_experiment_manifest(manifest, project=root)

    def test_checker_never_executes_recorded_commands_or_overwrites(self):
        with temporary_tree(ROOT.parent) as root:
            manifest = experiment_fixture(root)
            save_fixture(root, "manifest.json", manifest)
            argv = [sys.executable, "-I", str(ROOT / "scripts/check-research-artifacts.py"), "--project", str(root), "--task", manifest["task_id"], "--manifest", "manifest.json", "--output", "check.json"]
            result = subprocess.run(argv, cwd=root, capture_output=True)
            self.assertEqual(0, result.returncode, result.stderr.decode())
            self.assertFalse(json.loads(result.stdout)["commands_executed"])
            before = bind(root, "check.json")
            result = subprocess.run(argv, cwd=root, capture_output=True)
            self.assertEqual(1, result.returncode)
            self.assertEqual(before, bind(root, "check.json"))

    def test_isolated_readers_preserve_complete_helper_tree(self):
        from core.build import SCRIPT_REQUIREMENTS
        with temporary_tree(ROOT.parent) as root:
            project, package, cwd = root / "project", root / "package", root / "cwd"
            for path in (project, package, cwd): path.mkdir()
            manifest = experiment_fixture(project)
            save_fixture(project, "manifest.json", manifest)
            for script in ("scripts/search-resource.py", "scripts/check-research-artifacts.py"):
                for name in [script, *SCRIPT_REQUIREMENTS[script]]:
                    target = package / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(ROOT / name, target)
            def tree():
                return {path.relative_to(package).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                        for path in package.rglob("*") if path.is_file()}
            before = tree()
            commands = [
                [sys.executable, "-I", str(package / "scripts/search-resource.py"), "--resource-id", "R-statistical-recipes",
                    "--consumer", "nckh-statistics", "--domain", "scientific-statistics", "--genre", "statistical-recipe", "--resource-access", "off", "--json"],
                [sys.executable, "-I", str(package / "scripts/check-research-artifacts.py"), "--project", str(project),
                    "--task", manifest["task_id"], "--manifest", "manifest.json", "--output", "check.json"],
            ]
            for argv in commands:
                with self.subTest(script=argv[2]):
                    result = subprocess.run(argv, cwd=cwd, capture_output=True)
                    self.assertEqual(result.returncode, 0, result.stderr.decode())
                    self.assertEqual(tree(), before)
                    self.assertEqual(list(cwd.iterdir()), [])
            self.assertTrue((project / "check.json").is_file())

if __name__ == "__main__":
    unittest.main()
