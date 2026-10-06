import importlib
import json
import unittest
from pathlib import Path

from core.schema import ContractError
from tests.hooks.test_runner import payload
from core.paths import atomic_json, temporary_tree
from hooks.runner import invoke


class HookAdapterTests(unittest.TestCase):
    def test_codex_native_patch_headers_reach_protected_path_policy(self):
        with temporary_tree() as project:
            atomic_json(project / "context.json", {"schema_version": 1, "task_id": "native-patch-path-policy",
                        "brief": {"mode": "auto"}, "allowed_operations": ["write"],
                        "tool_operations": {"apply_patch": "write"}})
            for operation in ("Add", "Update", "Delete"):
                for target in ("private/oracle.txt", str(project / "holdout/oracle.txt"), "draft.md"):
                    with self.subTest(operation=operation, target=target):
                        body = "+NATIVE_ORACLE\n" if operation == "Add" else "@@\n-before\n+after\n" if operation == "Update" else ""
                        data = payload(project, "codex")
                        data.update(tool_name="apply_patch", tool_input={"command":
                            "*** Begin Patch\n*** " + operation + " File: " + target + "\n" + body + "*** End Patch"})
                        (wire, code), receipt = invoke("codex", "PreToolUse", json.dumps(data).encode(),
                                                      project=project, context_reference="context.json")
                        self.assertEqual(code, 0)
                        if target == "draft.md":
                            self.assertEqual(receipt["decision"], "allow")
                        else:
                            self.assertEqual(receipt["decision"], "block")
                            self.assertIn("private-holdout-credential-path", receipt["reason_codes"])
                            self.assertEqual(wire["hookSpecificOutput"]["permissionDecision"], "deny")
                        self.assertNotIn(target, json.dumps(receipt))
                        self.assertNotIn("NATIVE_ORACLE", json.dumps(receipt))

    def test_codex_native_patch_checks_move_paths_and_cannot_hide_targets_with_aliases(self):
        with temporary_tree() as project:
            atomic_json(project / "context.json", {"schema_version": 1, "task_id": "native-patch-move-policy",
                        "brief": {"mode": "auto"}, "allowed_operations": ["write"],
                        "tool_operations": {"apply_patch": "write"}})
            for source, destination, aliases in (("private/old.md", "draft.md", {}),
                ("draft.md", "credentials/new.md", {}), ("draft.md", "revised.md", {"path": "private/alias.md"}),
                ("private/old.md", "revised.md", {"file_path": "draft.md"}), ("draft.md", "revised.md", {})):
                with self.subTest(source=source, destination=destination, aliases=aliases):
                    data = payload(project, "codex")
                    data.update(tool_name="apply_patch", tool_input={**aliases, "command":
                        "*** Begin Patch\n*** Update File: " + source + "\n*** Move to: " + destination +
                        "\n@@\n-before\n+after\n*** End Patch"})
                    (wire, _), receipt = invoke("codex", "PreToolUse", json.dumps(data).encode(),
                                               project=project, context_reference="context.json")
                    if (source, destination, aliases) == ("draft.md", "revised.md", {}):
                        self.assertEqual(receipt["decision"], "allow")
                    else:
                        self.assertEqual(receipt["decision"], "block")
                        self.assertEqual(wire["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_codex_native_patch_rejects_missing_malformed_escaping_and_excess_paths(self):
        with temporary_tree() as project:
            atomic_json(project / "context.json", {"schema_version": 1, "task_id": "native-patch-input-policy",
                        "brief": {"mode": "auto"}, "allowed_operations": ["write"],
                        "tool_operations": {"apply_patch": "write"}})
            patches = [None, 7, [], "", "echo something", "*** Begin Patch\n*** End Patch",
                "*** Begin Patch\n*** Add File: \n+x\n*** End Patch",
                "*** Begin Patch\n*** Add File: ../outside.txt\n+x\n*** End Patch",
                "*** Begin Patch\n*** Add File: " + str(project.parent / "outside.txt") + "\n+x\n*** End Patch",
                "*** Begin Patch\n*** Add File: safe.txt\n+x\n*** Move to: private/other.txt\n*** End Patch",
                "*** Begin Patch\n*** Update File: safe.txt\n@@\n+x\n*** Move to: private/other.txt\n*** End Patch",
                "*** Begin Patch\n*** Add File: safe.txt\n+x\x00\n*** End Patch",
                "*** Begin Patch\n" + "".join("*** Add File: file-" + str(i) + ".txt\n+x\n" for i in range(17)) + "*** End Patch"]
            for patch in patches:
                with self.subTest(patch=patch):
                    data = payload(project, "codex")
                    data.update(tool_name="apply_patch", tool_input={"command": patch})
                    (wire, _), receipt = invoke("codex", "PreToolUse", json.dumps(data).encode(),
                                               project=project, context_reference="context.json")
                    self.assertEqual(receipt["decision"], "block")
                    self.assertEqual(wire["hookSpecificOutput"]["permissionDecision"], "deny")
            data = payload(project, "codex")
            data.update(tool_name="apply_patch", tool_input={"command":
                "*** Begin Patch\n*** Add File: safe.txt\n+*** Add File: private/body-text.txt\n*** End Patch"})
            (_, _), receipt = invoke("codex", "PreToolUse", json.dumps(data).encode(),
                                    project=project, context_reference="context.json")
            self.assertEqual(receipt["decision"], "allow")

    def test_agy_native_file_and_search_paths_reach_protected_path_policy(self):
        tools = [("write_to_file", "TargetFile", "write"),
                 ("replace_file_content", "TargetFile", "write"),
                 ("multi_replace_file_content", "TargetFile", "write"),
                 ("view_file", "AbsolutePath", "read"),
                 ("list_dir", "DirectoryPath", "read"),
                 ("find_by_name", "SearchDirectory", "read"),
                 ("grep_search", "SearchPath", "read")]
        with temporary_tree() as project:
            atomic_json(project / "context.json", {"schema_version": 1, "task_id": "native-file-path-policy",
                        "brief": {"mode": "auto"}, "allowed_operations": ["read", "write"],
                        "tool_operations": {tool: operation for tool, _, operation in tools}})
            for tool, field, _ in tools:
                for target in ("private/oracle.txt", str(project / "private/oracle.txt"), "draft.md"):
                    with self.subTest(tool=tool, target=target):
                        data = payload(project, "agy")
                        data["toolCall"] = {"name": tool, "args": {field: target}}
                        (wire, code), receipt = invoke("agy", "PreToolUse", json.dumps(data).encode(),
                                                      project=project, context_reference="context.json")
                        self.assertEqual(code, 0)
                        if target == "draft.md":
                            self.assertEqual(receipt["decision"], "allow")
                            self.assertEqual(wire, {"decision": "ask"})
                        else:
                            self.assertEqual(receipt["decision"], "block")
                            self.assertIn("private-holdout-credential-path", receipt["reason_codes"])
                            self.assertEqual(wire["decision"], "deny")
                            self.assertNotIn(target, json.dumps(receipt))

    def test_agy_native_file_paths_reject_missing_malformed_and_escaping_targets(self):
        with temporary_tree() as project:
            atomic_json(project / "context.json", {"schema_version": 1, "task_id": "native-file-path-input",
                        "brief": {"mode": "auto"}, "allowed_operations": ["write"],
                        "tool_operations": {"write_to_file": "write"}})
            for arguments in ({}, {"TargetFile": None}, {"TargetFile": 7}, {"TargetFile": []},
                              {"TargetFile": ""}, {"TargetFile": str(project.parent / "outside.txt")}):
                with self.subTest(arguments=arguments):
                    data = payload(project, "agy")
                    data["toolCall"] = {"name": "write_to_file", "args": arguments}
                    (wire, _), receipt = invoke("agy", "PreToolUse", json.dumps(data).encode(),
                                               project=project, context_reference="context.json")
                    self.assertEqual(receipt["status"], "degraded-failed")
                    self.assertEqual(wire["decision"], "deny")

    def test_agy_native_and_legacy_path_fields_cannot_hide_a_protected_target(self):
        with temporary_tree() as project:
            atomic_json(project / "context.json", {"schema_version": 1, "task_id": "native-file-path-aliases",
                        "brief": {"mode": "auto"}, "allowed_operations": ["write"],
                        "tool_operations": {"write_to_file": "write"}})
            for arguments in ({"TargetFile": "private/oracle.txt", "file_path": "draft.md"},
                              {"TargetFile": "draft.md", "path": "private/oracle.txt"}):
                with self.subTest(arguments=arguments):
                    data = payload(project, "agy")
                    data["toolCall"] = {"name": "write_to_file", "args": arguments}
                    (wire, _), receipt = invoke("agy", "PreToolUse", json.dumps(data).encode(),
                                               project=project, context_reference="context.json")
                    self.assertEqual(receipt["decision"], "block")
                    self.assertEqual(wire["decision"], "deny")

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
