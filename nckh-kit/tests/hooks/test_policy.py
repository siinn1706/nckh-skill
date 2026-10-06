import unittest
from copy import deepcopy

from core.guards import FACT_DIMENSIONS
from core.hook_policy import evaluate
from core.paths import digest_file, digest_record, temporary_tree
from core.schema import ContractError


def event(phase="preflight", tool="Write", paths=()):
    return {"schema_version": 1, "phase": phase, "host": "codex", "tool": tool, "paths": list(paths),
            "session_key": digest_record("test-session"), "task_key": digest_record("test-task"),
            "artifact_sha256": digest_record("test-artifact"), "stop_active": False}


class HookPolicyTests(unittest.TestCase):
    def test_boundaries_do_not_accept_payload_authority(self):
        context = {"schema_version": 1, "tool_operations": {"Write": "write"}, "allowed_operations": ["write"], "brief": {"mode": "auto"}}
        with temporary_tree() as project:
            self.assertEqual(evaluate(event(), context, project=project)["decision"], "allow")
            for path in ("../outside", "private/draft.md", "holdout/data.json", ".env", "keys/private.key", ".aws/credentials"):
                with self.subTest(path=path):
                    self.assertEqual(evaluate(event(paths=[path]), context, project=project)["decision"], "block")
            context["brief"]["mode"] = "plan-only"
            self.assertEqual(evaluate(event(), context, project=project)["decision"], "block")
            broken = {**event(), "grant": True}
            with self.assertRaises(ContractError):
                evaluate(broken, context, project=project)

    def test_unknown_shell_route_and_missing_context_remain_manual_or_pending(self):
        with temporary_tree() as project:
            self.assertEqual(evaluate(event(tool="Bash"), {"schema_version": 1}, project=project)["decision"], "manual")
            self.assertEqual(evaluate(event(), {}, project=project)["decision"], "pending")
            context = {"schema_version": 1, "tool_operations": {"Write": "generate-visual"}, "allowed_operations": ["generate-visual"], "brief": {"domain": "research"}}
            self.assertEqual(evaluate(event(), context, project=project)["decision"], "pending")
            context["brief"]["visual_purpose"] = {"artifact_role": "logo"}
            self.assertEqual(evaluate(event(), context, project=project)["decision"], "block")
            self.assertEqual(list(project.iterdir()), [])

    def test_delivery_checks_factual_and_protected_delta_without_rewrite(self):
        slots = dict.fromkeys(FACT_DIMENSIONS, [])
        context = {"schema_version": 1, "fidelity": {"before": slots, "after": deepcopy(slots),
            "protected_before": ["quote"], "protected_after": ["quote"]}}
        with temporary_tree() as project:
            (project / "draft.md").write_text("Actual diagnostic draft bytes", encoding="utf8")
            context["artifact"] = {"path": "draft.md", "sha256": digest_file(project / "draft.md")}
            final_event = {**event("pre-delivery"), "artifact_sha256": context["artifact"]["sha256"]}
            result = evaluate(final_event, context, project=project)
            self.assertEqual(result["decision"], "advisory")
            self.assertEqual(result["semantic_fidelity"], "unverified")
            context["fidelity"]["protected_after"] = ["changed"]
            self.assertEqual(evaluate(final_event, context, project=project)["decision"], "pending")
            self.assertEqual(evaluate(event("stop"), context, project=project)["decision"], "advisory")
            (project / "draft.md").write_text("Changed final bytes", encoding="utf8")
            self.assertEqual(evaluate(final_event, context, project=project)["reason_codes"], ["artifact-final-bytes-missing-or-stale"])
