from tests._lab import lab_root
import importlib
import json
import subprocess
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest import mock

from core.paths import atomic_json, temporary_tree
from core.schema import ContractError
from core.hook_policy import MAX_CONTEXT_BYTES
from hooks import runner
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


def event_payload(project, host, name):
    """A minimal well-formed payload for any event a host codec declares."""
    if host == "agy":
        return {"conversationId": "fixture", "workspacePaths": [str(project)],
                "toolCall": {"name": "Write", "args": {"path": "draft.md"}}, "executionNum": 1}
    record = payload(project, host=host)
    record["hook_event_name"] = name
    return record


class HookRunnerTests(unittest.TestCase):
    def setUp(self):
        self.tree = temporary_tree(lab_root())
        self.project = self.tree.__enter__()
        self.addCleanup(self.tree.__exit__, None, None, None)
        atomic_json(self.project / "context.json", {"schema_version": 1, "task_id": "fixture",
            "tool_operations": {"Write": "write"}, "allowed_operations": ["write"], "brief": {"mode": "auto"}})

    def call(self, data, host="codex", name="PreToolUse"):
        return invoke(host, name, json.dumps(data).encode(), project=self.project, context_reference="context.json")

    def test_advisory_reports_denials_and_bad_input_without_denying_native_tools(self):
        for host in ("claude", "codex", "cursor", "agy"):
            name = "preToolUse" if host == "cursor" else "PreToolUse"
            for raw in (json.dumps(payload(self.project, host=host, path="private/input.md")).encode(), b"invalid"):
                with self.subTest(host=host, raw=raw):
                    (wire, code), receipt = invoke(host, name, raw, project=self.project,
                                                 context_reference="context.json", mode="advisory")
                    self.assertEqual(code, 0)
                    self.assertEqual(receipt["hook_mode"], "advisory")
                    self.assertNotIn('"deny"', json.dumps(wire))
                    self.assertNotIn('"continue": false', json.dumps(wire))
                    self.assertEqual(receipt["decision"], "block")

    def test_advisory_missing_context_retains_failure_and_exits_successfully(self):
        (wire, code), receipt = invoke("codex", "PreToolUse", json.dumps(payload(self.project)).encode(),
                                     project=self.project, context_reference="missing.json", mode="advisory")
        self.assertEqual(code, 0)
        self.assertEqual(receipt["status"], "degraded-no-context")
        self.assertNotIn("permissionDecision", json.dumps(wire))

    def test_missing_context_is_distinct_from_invalid_input(self):
        raw = json.dumps(payload(self.project)).encode()
        for mode in ("advisory", "enforce"):
            with self.subTest(mode=mode):
                _, missing = invoke("codex", "PreToolUse", raw, project=self.project,
                                    context_reference="missing.json", mode=mode)
                self.assertEqual(missing["status"], "degraded-no-context")
                self.assertEqual(missing["reason_codes"], ["hook-context-unavailable"])
                _, invalid = invoke("codex", "PreToolUse", b"{broken", project=self.project,
                                    context_reference="missing.json", mode=mode)
                self.assertEqual(invalid["status"], "degraded-failed")
                self.assertEqual(invalid["reason_codes"], ["hook-input-or-context-invalid"])
        (self.project / "oversized.json").write_bytes(b" " * (MAX_CONTEXT_BYTES + 1))
        _, oversized = invoke("codex", "PreToolUse", raw, project=self.project, context_reference="oversized.json")
        self.assertEqual(oversized["status"], "degraded-no-context")
        (self.project / "broken.json").write_bytes(b"{broken")
        _, corrupt = invoke("codex", "PreToolUse", raw, project=self.project, context_reference="broken.json")
        self.assertEqual(corrupt["status"], "degraded-failed")
        self.assertFalse((self.project / "missing.json").exists())

    def test_missing_context_enforce_mode_still_blocks(self):
        for host in ("claude", "codex", "cursor", "agy"):
            name = "preToolUse" if host == "cursor" else "PreToolUse"
            with self.subTest(host=host):
                (wire, code), receipt = invoke(host, name, json.dumps(payload(self.project, host=host)).encode(),
                                               project=self.project, context_reference="missing.json")
                self.assertEqual(receipt["decision"], "block")
                self.assertEqual(receipt["hook_mode"], "enforce")
                self.assertEqual(receipt["status"], "degraded-no-context")
                self.assertNotEqual(wire, {})
                self.assertNotIn('"advisory"', json.dumps(wire))
        (wire, _), _ = invoke("codex", "PreToolUse", json.dumps(payload(self.project)).encode(),
                              project=self.project, context_reference="missing.json")
        self.assertEqual(wire["hookSpecificOutput"]["permissionDecision"], "deny")

    def missing_context_receipt(self, session="fixture", path="draft.md"):
        raw = payload(self.project, path=path)
        raw["session_id"] = session
        return invoke("codex", "PreToolUse", json.dumps(raw).encode(), project=self.project,
                      context_reference="missing.json", mode="advisory")[1]

    def test_degraded_no_context_deduplicated_per_session(self):
        first = self.missing_context_receipt()
        self.assertEqual(first["phase"], "preflight")
        self.assertEqual(record_once(self.project, "receipts", first), "recorded")
        self.assertEqual(record_once(self.project, "receipts", first), "duplicate-suppressed")
        # A different event in the same session is the same degraded condition.
        self.assertEqual(record_once(self.project, "receipts", self.missing_context_receipt(path="other.md")),
                         "duplicate-suppressed")
        self.assertEqual(record_once(self.project, "receipts", self.missing_context_receipt(session="second")), "recorded")
        hinted = dict(first, nudge={"kind": "route-hint", "skills": ["nckh-fix"]})
        self.assertEqual(record_once(self.project, "receipts", hinted), "recorded")
        self.assertEqual(record_once(self.project, "receipts", hinted), "duplicate-suppressed")
        self.assertEqual(len(list((self.project / "receipts").glob("*.json"))), 3)

    def test_degraded_failed_kept_per_attempt(self):
        _, failure = invoke("codex", "PreToolUse", b"{broken", project=self.project,
                            context_reference="context.json", mode="advisory")
        self.assertEqual(failure["status"], "degraded-failed")
        for _ in range(3):
            self.assertEqual(record_once(self.project, "receipts", failure), "recorded")
        self.assertEqual(len(list((self.project / "receipts").glob("*.json"))), 3)

    def test_receipt_cap_reached(self):
        receipts = self.project / "receipts"
        receipts.mkdir()
        with mock.patch.object(runner, "RECEIPT_CAP", 3):
            # Checked and per-attempt receipts never count toward the cap and are never capped.
            _, failure = invoke("codex", "PreToolUse", b"{broken", project=self.project, context_reference="context.json")
            _, checked = self.call(payload(self.project))
            for index in range(4):
                self.assertEqual(record_once(self.project, "receipts", failure), "recorded")
            self.assertEqual(record_once(self.project, "receipts", checked), "recorded")
            first = self.missing_context_receipt()
            self.assertEqual(record_once(self.project, "receipts", first), "recorded")
            capped = sorted(receipts.glob(runner.CAPPED_PREFIX + "*.json"))
            self.assertEqual(len(capped), 1)
            for session in ("second", "third"):
                self.assertEqual(record_once(self.project, "receipts", self.missing_context_receipt(session=session)),
                                 "recorded")
            self.assertFalse((receipts / runner.CAP_MARKER).exists())
            late = self.missing_context_receipt(session="late")
            self.assertEqual(record_once(self.project, "receipts", late), "cap-reached")
            marker = json.loads((receipts / runner.CAP_MARKER).read_text(encoding="utf8"))
            self.assertEqual((marker["status"], marker["cap"], marker["host"]), ("cap-reached", 3, "codex"))
            self.assertEqual(marker["reason_codes"], ["hook-receipt-cap-reached"])
            self.assertEqual(record_once(self.project, "receipts", self.missing_context_receipt(session="later")),
                             "cap-reached")
            self.assertEqual(len(list(receipts.glob(runner.CAPPED_PREFIX + "*.json"))), 3)
            # Enforce-relevant receipts still record after the cap is hit.
            self.assertEqual(record_once(self.project, "receipts", failure), "recorded")
            self.assertEqual(len(list(receipts.glob("*.json"))), 5 + 1 + 3 + 1)
            for path in receipts.glob(runner.CAPPED_PREFIX + "*.json"):
                path.unlink()
            self.assertEqual(record_once(self.project, "receipts", first), "recorded")
            self.assertEqual(record_once(self.project, "receipts", first), "duplicate-suppressed")

    def test_enforce_degraded_event_matrix(self):
        gating = {"claude": {"PreToolUse", "UserPromptSubmit"}, "codex": {"PreToolUse", "UserPromptSubmit"},
                  "cursor": {"preToolUse", "beforeSubmitPrompt"}, "agy": {"PreToolUse"}}
        for host, gated in gating.items():
            codec = importlib.import_module("hooks.codecs." + host)
            for name in codec.EVENTS:
                for mode in ("enforce", "advisory"):
                    with self.subTest(host=host, event=name, mode=mode):
                        (wire, code), receipt = invoke(host, name, json.dumps(event_payload(self.project, host, name)).encode(),
                                                       project=self.project, context_reference="missing.json", mode=mode)
                        self.assertEqual(receipt["status"], "degraded-no-context")
                        self.assertEqual(receipt["decision"], "block")
                        self.assertEqual(code, 0)
                        serialized = json.dumps(wire)
                        blocked = any(marker in serialized for marker in ('"deny"', '"block"', '"continue": false'))
                        self.assertEqual(blocked, mode == "enforce" and name in gated)

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

    def test_concurrent_first_receipts_in_fresh_directories_preserve_idempotence(self):
        _, receipt = self.call(payload(self.project))
        with ThreadPoolExecutor(max_workers=6) as pool:
            for index in range(150):
                relative = "fresh-receipts-" + str(index)
                results = list(pool.map(lambda _: record_once(self.project, relative, receipt), range(6)))
                self.assertEqual(results.count("recorded"), 1)
                self.assertEqual(results.count("duplicate-suppressed"), 5)
                records = list((self.project / relative).glob("*.json"))
                self.assertEqual(len(records), 1)
                self.assertEqual(json.loads(records[0].read_text(encoding="utf8")), receipt)
        with self.assertRaises(ContractError):
            record_once(self.project, "../outside-receipts", receipt)
