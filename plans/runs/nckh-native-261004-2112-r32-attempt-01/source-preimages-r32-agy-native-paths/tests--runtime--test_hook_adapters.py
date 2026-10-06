import importlib
import json
import unittest
from pathlib import Path

from core.schema import ContractError
from tests.hooks.test_runner import payload
from core.paths import atomic_json, temporary_tree
from hooks.runner import invoke


class HookAdapterTests(unittest.TestCase):
    def test_agy_pretool_preserves_native_permission_checks(self):
        with temporary_tree() as project:
            context = {"schema_version": 1, "task_id": "native-permission-contract",
                       "brief": {"mode": "auto"}, "allowed_operations": ["write"],
                       "tool_operations": {"Write": "write"}}
            for mapping, expected in [({"Write": "write"}, "allow"), ({}, "manual")]:
                context["tool_operations"] = mapping
                atomic_json(project / "context.json", context)
                (wire, code), receipt = invoke("agy", "PreToolUse", json.dumps(payload(project, "agy")).encode(),
                                               project=project, context_reference="context.json")
                self.assertEqual(receipt["decision"], expected)
                self.assertEqual(code, 0)
                self.assertEqual(wire, {"decision": "ask"})
                self.assertNotIn("permissionOverrides", wire)

    def test_host_specific_denial_and_stop_shapes(self):
        with temporary_tree() as project:
            for host in ("claude", "codex", "cursor", "agy"):
                codec = importlib.import_module("hooks.codecs." + host)
                event = "preToolUse" if host == "cursor" else "PreToolUse"
                decoded = codec.decode(payload(project, host), event)
                self.assertEqual(decoded["phase"], "preflight")
                output, code = codec.encode(event, {"decision": "block", "reason_codes": ["fixture-deny"]})
                self.assertEqual(code, 0)
                if host in {"claude", "codex"}:
                    self.assertEqual(output["hookSpecificOutput"]["permissionDecision"], "deny")
                    self.assertFalse(set(output) & {"continue", "stopReason", "suppressOutput"})
                else:
                    self.assertEqual(output["permission" if host == "cursor" else "decision"], "deny")
                stop = "stop" if host == "cursor" else "Stop"
                output, _ = codec.encode(stop, {"decision": "advisory", "reason_codes": ["fixture-advice"]})
                self.assertEqual(output, {"decision": "stop"} if host == "agy" else {})
                self.assertNotIn("followup_message", output)

    def test_inactive_templates_follow_each_config_shape(self):
        root = Path(__file__).resolve().parents[2]
        for host in ("claude", "codex", "cursor", "agy"):
            template = json.loads((root / "hooks/templates" / (host + ".json")).read_text(encoding="utf8"))
            self.assertFalse(template["enabled"] or template["registered"] or template["trusted"])
            if host == "agy":
                self.assertFalse(template["config"]["nckh"]["enabled"])
                self.assertNotIn("hooks", template["config"])
            elif host == "cursor":
                self.assertTrue(template["config"]["hooks"]["preToolUse"][0]["failClosed"])
            else:
                self.assertIn("hooks", template["config"]["hooks"]["PreToolUse"][0])
