import json
import subprocess
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from core.paths import atomic_json, temporary_tree
from hooks.runner import invoke, record_once


ROOT = Path(__file__).resolve().parents[2]


def payload(project, host="codex", event="PreToolUse", path="draft.md"):
    if host == "cursor":
        return {"hook_event_name": "preToolUse" if event == "PreToolUse" else "stop", "conversation_id": "fixture",
                "workspace_roots": [str(project)], "tool_name": "Write", "tool_input": {"file_path": path}, "loop_count": 0}
    if host == "agy":
        return {"conversationId": "fixture", "workspacePaths": [str(project)], "toolCall": {"name": "Write", "args": {"path": path}}, "executionNum": 1}
    return {"hook_event_name": event, "session_id": "fixture", "cwd": str(project), "model": "unverified",
            "turn_id": "fixture-turn", "tool_name": "Write", "tool_input": {"file_path": path}, "stop_hook_active": False}


class HookRunnerTests(unittest.TestCase):
    def setUp(self):
        self.tree = temporary_tree()
        self.project = self.tree.__enter__()
        self.addCleanup(self.tree.__exit__, None, None, None)
        atomic_json(self.project / "context.json", {"schema_version": 1, "task_id": "fixture",
            "tool_operations": {"Write": "write"}, "allowed_operations": ["write"], "brief": {"mode": "auto"}})

    def call(self, data, host="codex", name="PreToolUse"):
        return invoke(host, name, json.dumps(data).encode(), project=self.project, context_reference="context.json")

    def test_allow_preserves_native_permissions_and_deny_has_no_raw_data(self):
        (wire, code), receipt = self.call(payload(self.project))
        self.assertEqual((wire, code), ({}, 0))
        raw = payload(self.project, path="private/manuscript.md")
        raw.update(transcript_path="never-read", prompt="never-export", command="never-execute", grant=True)
        (wire, code), receipt = self.call(raw)
        self.assertEqual(wire["hookSpecificOutput"]["permissionDecision"], "deny")
        serialized = json.dumps(receipt)
        for private in ("private/manuscript.md", "never-read", "never-export", "never-execute", str(self.project)):
            self.assertNotIn(private, serialized)
        self.assertEqual(receipt["native_host_response"], "unobserved")

    def test_malformed_oversized_unsupported_and_wrong_project_degrade(self):
        for data in (b'{"a":1,"a":2}', b"x" * 65537, b"[]", b"{broken", b'{"a":1e999}', b'\xff'):
            (wire, _), receipt = invoke("codex", "PreToolUse", data, project=self.project, context_reference="context.json")
            self.assertEqual(receipt["status"], "degraded-failed")
            self.assertEqual(wire["hookSpecificOutput"]["permissionDecision"], "deny")
        raw = payload(self.project)
        raw["cwd"] = str(self.project.parent)
        self.assertEqual(self.call(raw)[1]["status"], "degraded-failed")
        self.assertEqual(self.call(payload(self.project), name="Unknown")[0][1], 3)

    def test_stop_never_continues_and_receipt_is_idempotent(self):
        (wire, _), receipt = self.call(payload(self.project, event="Stop"), name="Stop")
        self.assertEqual(wire, {})
        self.assertEqual(record_once(self.project, "receipts", receipt), "recorded")
        self.assertEqual(record_once(self.project, "receipts", receipt), "duplicate-suppressed")
        self.assertEqual(len(list((self.project / "receipts").glob("*.json"))), 1)

    def test_actual_isolated_runner_ignores_payload_commands(self):
        raw = payload(self.project)
        raw["tool_input"]["command"] = "create-an-unapproved-file"
        process = subprocess.run([sys.executable, "-I", str(ROOT / "hooks/runner.py"), "--host", "codex",
            "--event", "PreToolUse", "--project", str(self.project), "--context", "context.json"],
            input=json.dumps(raw).encode(), cwd=self.project, capture_output=True, timeout=10)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(json.loads(process.stdout), {})
        self.assertEqual([p.name for p in self.project.iterdir()], ["context.json"])

    def test_concurrent_duplicate_receipts_and_failed_attempts_are_preserved(self):
        _, receipt = self.call(payload(self.project))
        with ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(lambda _: record_once(self.project, "receipts", receipt), range(6)))
        self.assertEqual(results.count("recorded"), 1)
        self.assertEqual(results.count("duplicate-suppressed"), 5)
        (_, _), failure = invoke("codex", "PreToolUse", b"{broken", project=self.project, context_reference="context.json")
        self.assertEqual(record_once(self.project, "receipts", failure), "recorded")
        self.assertEqual(record_once(self.project, "receipts", failure), "recorded")
        self.assertEqual(len(list((self.project / "receipts").glob("*.json"))), 3)
