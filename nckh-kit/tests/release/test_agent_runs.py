import importlib.util
import io
import json
import subprocess
import sys
import unittest
from copy import deepcopy
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest.mock import patch

from core.agent_runs import FREEZE_FIELDS, load_cases, prepare_agent_run, run_agent_cases
from core.build import load_json, verify_source_lock
from core.install import process_alive
from core.paths import atomic_json, digest_file, digest_record, temporary_tree
from core.processes import run_owned_command
from core.schema import ContractError


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("agent_evaluation_entry", ROOT / "evals/run-evals.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)


class AgentRunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The source lock is read-only for the whole run; hash it once for every frozen budget fixture.
        cls.source_lock_hash = digest_record(verify_source_lock(ROOT))

    def recipe(self, area, *, frozen=False):
        workspace, store = area / "workspace", area / "private"
        workspace.mkdir()
        store.mkdir()
        interface = area / "interface.json"
        atomic_json(interface, {"kind": "owned deterministic subprocess fixture", "native_qualification": "none"})
        ref = {"path": str(interface), "sha256": digest_file(interface)}
        refs = {name: ref if frozen else None for name in FREEZE_FIELDS}
        if frozen:
            budget = area / "budget.json"
            atomic_json(budget, {"schema_version": 1, "kind": "provider-run-budget",
                                "scope": {"source_lock_hash": self.source_lock_hash, "case_ids": ["nckh-plan:positive"]},
                                "mode": "time-and-case-bound-unknown-cost", "unknown_cost_accepted": True,
                                "max_cases": 1, "max_seconds_per_case": 10,
                                "funding_scope_reference": "owned local Python subprocess fixture only; no provider or human qualification"})
            refs["provider_budget"] = {"path": str(budget), "sha256": digest_file(budget)}
        return {"schema_version": 1, "surface": "codex-cli", "host_version": "deterministic-fixture; no native host",
                "argv": [str(Path(sys.executable).resolve()), "-c", "import json,sys; value=json.load(sys.stdin); print(json.dumps({'fixture': True, 'input': value}))"],
                "executable_sha256": digest_file(sys.executable), "driver_references": [], "transport": "json-stdin",
                "interface_reference": ref, "workspace": str(workspace), "private_store": str(store),
                "case_ids": ["nckh-plan:positive"], "round": 1, "timeout_seconds": 10,
                "freeze_references": refs,
                "requested_model": "inherit", "requested_effort": "inherit"}

    def test_preview_does_not_spawn_or_create_run_files(self):
        with temporary_tree() as area:
            recipe = self.recipe(area)
            plan = prepare_agent_run(ROOT, recipe)
            self.assertEqual(plan["maximum_attempts"], 1)
            self.assertEqual(len(plan["blockers"]), 6)
            self.assertEqual(plan["qualification"], "pending")
            self.assertEqual(list((area / "private").iterdir()), [])

    def test_no_flags_or_recipe_fields_can_replace_live_opt_in(self):
        with temporary_tree() as area:
            recipe = self.recipe(area, frozen=True)
            plan = prepare_agent_run(ROOT, recipe)
            with self.assertRaisesRegex(ContractError, "live operator"):
                run_agent_cases(ROOT, recipe, approved_plan_hash=digest_record(plan))
            recipe["authorized"] = True
            with self.assertRaisesRegex(ContractError, "unknown or incomplete"):
                prepare_agent_run(ROOT, recipe)
            self.assertEqual(list((area / "private").iterdir()), [])

    def test_pending_freeze_stops_even_an_exact_confirmed_plan(self):
        with temporary_tree() as area:
            recipe = self.recipe(area)
            plan = prepare_agent_run(ROOT, recipe)
            with self.assertRaisesRegex(ContractError, "missing freeze reference"):
                run_agent_cases(ROOT, recipe, approved_plan_hash=digest_record(plan), allow_provider=True)
            self.assertEqual(list((area / "private").iterdir()), [])

    def test_changed_command_or_reference_invalidates_preview(self):
        with temporary_tree() as area:
            recipe = self.recipe(area, frozen=True)
            plan = prepare_agent_run(ROOT, recipe)
            recipe["argv"][-1] = "raise SystemExit(7)"
            with self.assertRaisesRegex(ContractError, "exact reviewed plan hash"):
                run_agent_cases(ROOT, recipe, approved_plan_hash=digest_record(plan), allow_provider=True)
            Path(recipe["interface_reference"]["path"]).write_text("changed fixture", encoding="utf-8")
            with self.assertRaisesRegex(ContractError, "reference is missing or changed"):
                prepare_agent_run(ROOT, recipe)
            self.assertEqual(list((area / "private").iterdir()), [])

    def test_unsafe_flags_unknown_cases_and_public_traces_are_rejected(self):
        with temporary_tree() as area:
            recipe = self.recipe(area)
            recipe["argv"].append("--dangerously-bypass-hook-trust")
            with self.assertRaisesRegex(ContractError, "bypass"):
                prepare_agent_run(ROOT, recipe)
            recipe["argv"].pop()
            recipe["case_ids"] = ["missing:positive"]
            with self.assertRaisesRegex(ContractError, "unknown case"):
                prepare_agent_run(ROOT, recipe)
            recipe["case_ids"] = ["nckh-plan:positive"]
            recipe["private_store"] = recipe["workspace"]
            with self.assertRaisesRegex(ContractError, "outside source"):
                prepare_agent_run(ROOT, recipe)

    def test_batch_wrapper_and_round_overrun_are_not_callable(self):
        with temporary_tree() as area:
            recipe = self.recipe(area)
            batch = area / "owned.cmd"
            batch.write_text("exit /b 0", encoding="utf-8")
            recipe["argv"][0], recipe["executable_sha256"] = str(batch), digest_file(batch)
            with self.assertRaisesRegex(ContractError, "NOT_CALLABLE"):
                prepare_agent_run(ROOT, recipe)
            recipe["argv"][0], recipe["executable_sha256"] = str(Path(sys.executable).resolve()), digest_file(sys.executable)
            recipe["round"] = 4
            with self.assertRaisesRegex(ContractError, "development-round"):
                prepare_agent_run(ROOT, recipe)

    def test_actual_fixture_transport_retains_raw_trace_without_agent_acceptance(self):
        with temporary_tree() as area:
            recipe = self.recipe(area, frozen=True)
            plan = prepare_agent_run(ROOT, recipe)
            result = run_agent_cases(ROOT, recipe, approved_plan_hash=digest_record(plan), allow_provider=True)
            self.assertEqual(result["status"], "completed-unreviewed")
            self.assertEqual(result["evidence_class"], "unclassified-command-observation")
            self.assertEqual(result["accepted_task_count"], 0)
            self.assertEqual(result["cost"], "unknown")
            self.assertEqual(result["model"]["effective"], "unknown")
            attempt = result["attempts"][0]
            raw = json.loads(Path(attempt["stdout_reference"]).read_bytes())
            self.assertTrue(raw["fixture"])
            self.assertEqual(raw["input"]["case_id"], "nckh-plan:positive")
            self.assertNotIn("oracle", raw["input"])
            self.assertNotIn("expected_outcome", raw["input"])
            self.assertEqual(digest_file(attempt["stdout_reference"]), attempt["stdout_hash"])
            self.assertEqual(load_json(Path(result["private_record"])), result)
            self.assertFalse(process_alive(attempt["pid"]))

    def test_actual_nonzero_process_retains_failure(self):
        with temporary_tree() as area:
            result = run_owned_command([sys.executable, "-c", "import sys; print('owned fixture failure', file=sys.stderr); sys.exit(7)"],
                                       area, b"", area / "out.bin", area / "error.bin", timeout=10)
            self.assertEqual(result["status"], "fail")
            self.assertEqual(result["exit_status"], 7)
            self.assertIn(b"owned fixture failure", (area / "error.bin").read_bytes())

    def test_case_change_between_reads_cannot_dispatch_a_stale_cached_input(self):
        with temporary_tree() as area:
            recipe = self.recipe(area, frozen=True)
            plan = prepare_agent_run(ROOT, recipe)
            frozen = load_cases(ROOT)
            changed = deepcopy(frozen)
            changed["nckh-plan:positive"]["prompt"] = "owned fault fixture: changed input between reads"
            with patch("core.agent_runs.load_cases", side_effect=[frozen, changed, frozen]):
                result = run_agent_cases(ROOT, recipe, approved_plan_hash=digest_record(plan), allow_provider=True)
            self.assertEqual(result["status"], "fail")
            self.assertIn("cached case input", result["error"])
            self.assertEqual(result["attempts"], [])
            self.assertEqual(list(Path(result["private_record"]).parent.glob("*-stdout.bin")), [])

    def test_command_arguments_stay_in_private_record_and_out_of_cli_receipts(self):
        with temporary_tree() as area:
            recipe = self.recipe(area, frozen=True)
            marker = "owned-fixture-private-argument"
            recipe["argv"].append(marker)
            path, output_path = area / "recipe.json", area / "summary.json"
            atomic_json(path, recipe)
            with redirect_stdout(io.StringIO()) as output:
                self.assertEqual(entry.main(["--prepare-agent-run", "--recipe", str(path)]), 0)
            preview = json.loads(output.getvalue())
            self.assertNotIn(marker, output.getvalue())
            self.assertEqual(preview["command"]["argv_hash"], digest_record(recipe["argv"]))
            with redirect_stdout(io.StringIO()) as output:
                code = entry.main(["--run-agent", "--recipe", str(path), "--allow-provider",
                                   "--approve-plan-hash", preview["plan_hash"], "--output", str(output_path)])
            self.assertEqual(code, 0)
            self.assertNotIn(marker, output.getvalue())
            self.assertNotIn(marker, output_path.read_text(encoding="utf-8"))
            result = load_json(output_path)
            command = load_json(Path(result["private_command_record"]))
            self.assertEqual(command["argv"], recipe["argv"])

    def test_budget_scope_and_unsupported_monetary_limit_do_not_dispatch(self):
        with temporary_tree() as area:
            recipe = self.recipe(area, frozen=True)
            path = Path(recipe["freeze_references"]["provider_budget"]["path"])
            budget = load_json(path)
            budget["mode"] = "monetary-cap"
            atomic_json(path, budget)
            recipe["freeze_references"]["provider_budget"]["sha256"] = digest_file(path)
            plan = prepare_agent_run(ROOT, recipe)
            with self.assertRaisesRegex(ContractError, "monetary billing cap"):
                run_agent_cases(ROOT, recipe, approved_plan_hash=digest_record(plan), allow_provider=True)
            budget["scope"]["case_ids"] = []
            atomic_json(path, budget)
            recipe["freeze_references"]["provider_budget"]["sha256"] = digest_file(path)
            with self.assertRaisesRegex(ContractError, "every case"):
                prepare_agent_run(ROOT, recipe)
            self.assertEqual(list((area / "private").iterdir()), [])

    def test_timeout_keeps_partial_trace_and_stops_owned_descendant(self):
        with temporary_tree() as area:
            script = "import subprocess,sys,time; child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(120)']); print(child.pid,flush=True); time.sleep(120)"
            result = run_owned_command([sys.executable, "-c", script], area, b"",
                                       area / "out.bin", area / "error.bin", timeout=1)
            self.assertEqual(result["status"], "timeout-unknown")
            self.assertIsNone(result["exit_status"])
            child_pid = int((area / "out.bin").read_bytes().strip())
            self.assertFalse(process_alive(result["pid"]))
            self.assertFalse(process_alive(child_pid))

    def test_malformed_or_extra_budget_bounds_stop_before_dispatch(self):
        with temporary_tree() as area:
            recipe = self.recipe(area, frozen=True)
            path = Path(recipe["freeze_references"]["provider_budget"]["path"])
            original = load_json(path)
            for value in (["invalid-budget"], {**original, "max_cost": 1}, {**original, "scope": None}):
                with self.subTest(value=value):
                    atomic_json(path, value)
                    recipe["freeze_references"]["provider_budget"]["sha256"] = digest_file(path)
                    with self.assertRaises(ContractError):
                        prepare_agent_run(ROOT, recipe)
            self.assertEqual(list((area / "private").iterdir()), [])

    def test_lifecycle_errors_keep_an_incomplete_private_receipt_without_exposing_arguments(self):
        for status, error_type in (("timeout-unknown", subprocess.TimeoutExpired), ("fail", subprocess.CalledProcessError)):
            with self.subTest(status=status), temporary_tree() as area:
                recipe = self.recipe(area, frozen=True)
                marker = "owned-fixture-private-error-argument"
                recipe["argv"].append(marker)
                plan = prepare_agent_run(ROOT, recipe)
                error = error_type(recipe["argv"], 5) if status == "timeout-unknown" else error_type(7, recipe["argv"])
                with patch("core.agent_runs.run_owned_command", side_effect=error):
                    result = run_agent_cases(ROOT, recipe, approved_plan_hash=digest_record(plan), allow_provider=True)
                self.assertEqual(result["status"], status)
                self.assertEqual(result["attempts"][0]["status"], status)
                self.assertIsNone(result["attempts"][0]["exit_status"])
                self.assertTrue(result["attempts"][0]["process_cleanup"].startswith("unverified"))
                self.assertEqual(result["accepted_task_count"], 0)
                self.assertNotIn(marker, json.dumps(result))
                self.assertEqual(load_json(Path(result["private_record"])), result)

    def test_case_read_failure_after_preview_closes_the_private_run_receipt(self):
        with temporary_tree() as area:
            recipe = self.recipe(area, frozen=True)
            plan = prepare_agent_run(ROOT, recipe)
            with patch("core.agent_runs.load_cases", side_effect=[load_cases(ROOT), ValueError("owned case-read fault fixture")]):
                result = run_agent_cases(ROOT, recipe, approved_plan_hash=digest_record(plan), allow_provider=True)
            self.assertEqual(result["status"], "fail")
            self.assertEqual(result["attempts"], [])
            self.assertEqual(load_json(Path(result["private_record"])), result)
            self.assertEqual(list(Path(result["private_record"]).parent.glob("*-stdout.bin")), [])

    def test_cli_preview_and_mixed_execution_flags_do_not_run_a_driver(self):
        with temporary_tree() as area:
            recipe = self.recipe(area)
            path = area / "recipe.json"
            atomic_json(path, recipe)
            with redirect_stdout(io.StringIO()) as output:
                code = entry.main(["--prepare-agent-run", "--recipe", str(path)])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output.getvalue())["status"], "preview")
            self.assertEqual(list((area / "private").iterdir()), [])
            with redirect_stderr(io.StringIO()):
                self.assertEqual(entry.main(["--validate-only", "--allow-provider"]), 3)
