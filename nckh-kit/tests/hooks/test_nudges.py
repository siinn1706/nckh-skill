from tests._lab import lab_root
import importlib
import json
import time
import unittest
from pathlib import Path
from unittest import mock

from core import edit_guard, route_hint
from core.paths import atomic_json, temporary_tree
from hooks.runner import invoke


ROOT = Path(__file__).resolve().parents[2]
PROMPT_EVENT = {"claude": "UserPromptSubmit", "codex": "UserPromptSubmit", "cursor": "beforeSubmitPrompt"}
DENY_MARKERS = ('"deny"', '"block"', '"continue": false')


def fix_cue():
    boundaries = route_hint.load_boundaries(ROOT / "core/registry/catalog/route-boundaries.json")
    return next(boundary["vi_cues"]["nckh-fix"][0] for boundary in boundaries if "nckh-fix" in boundary["vi_cues"])


def event(project, host, name, **extra):
    if host == "cursor":
        record = {"hook_event_name": name, "conversation_id": "fixture", "workspace_roots": [str(project)], "loop_count": 0}
    elif host == "agy":
        record = {"conversationId": "fixture", "workspacePaths": [str(project)], "executionNum": 1}
    else:
        record = {"hook_event_name": name, "session_id": "fixture", "cwd": str(project), "model": "unverified",
                  "turn_id": "fixture-turn", "stop_hook_active": False}
    record.update(extra)
    return record


class HookNudgeTests(unittest.TestCase):
    def setUp(self):
        self.tree = temporary_tree(lab_root())
        self.project = self.tree.__enter__()
        self.addCleanup(self.tree.__exit__, None, None, None)
        self.prompt = f"Giúp mình {fix_cue()} trong app.py nhé"

    def install(self, root, skill="nckh-fix"):
        target = self.project / root / skill / "SKILL.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("---\nname: " + skill + "\n---\n", encoding="utf8")

    def run_hook(self, host, name, record, *, mode="advisory", context="missing.json"):
        return invoke(host, name, json.dumps(record).encode(), project=self.project,
                      context_reference=context, mode=mode)

    def prompt_hint(self, host, prompt=None):
        record = event(self.project, host, PROMPT_EVENT[host], prompt=self.prompt if prompt is None else prompt)
        return self.run_hook(host, PROMPT_EVENT[host], record)

    def assert_never_denies(self, wire, code):
        self.assertEqual(code, 0)
        serialized = json.dumps(wire)
        for marker in DENY_MARKERS:
            self.assertNotIn(marker, serialized)

    def test_prompt_hint_claude_codex_additional_context(self):
        for host, root, call in (("claude", ".claude/skills", "/nckh-fix"), ("codex", ".agents/skills", "$nckh-fix")):
            with self.subTest(host=host):
                self.install(root)
                (wire, code), receipt = self.prompt_hint(host)
                self.assert_never_denies(wire, code)
                text = wire["hookSpecificOutput"]["additionalContext"]
                self.assertIn(call, text)
                self.assertIn("nckh routing hint (advisory)", text)
                self.assertEqual(receipt["nudge"], {"kind": "route-hint", "skills": ["nckh-fix"]})
                self.assertNotIn(self.prompt, json.dumps(receipt, ensure_ascii=False))

    def test_prompt_hint_without_controller_context(self):
        self.install(".claude/skills")
        (wire, code), receipt = self.prompt_hint("claude")
        self.assertEqual(receipt["status"], "degraded-no-context")
        text = wire["hookSpecificOutput"]["additionalContext"]
        self.assertTrue(text.startswith("nckh routing hint (advisory)"))
        self.assertIn("hook-context-unavailable", text)
        self.assertEqual(receipt["nudge"]["skills"], ["nckh-fix"])

    def test_prompt_hint_with_controller_context(self):
        self.install(".claude/skills")
        atomic_json(self.project / "context.json", {"schema_version": 1, "task_id": "fixture",
            "tool_operations": {"Write": "write"}, "allowed_operations": ["write"], "brief": {"mode": "auto"}})
        record = event(self.project, "claude", "UserPromptSubmit", prompt=self.prompt)
        (wire, code), receipt = self.run_hook("claude", "UserPromptSubmit", record, context="context.json")
        self.assert_never_denies(wire, code)
        self.assertEqual(receipt["status"], "checked-unreviewed")
        self.assertIn("/nckh-fix", wire["hookSpecificOutput"]["additionalContext"])
        self.assertEqual(receipt["nudge"]["skills"], ["nckh-fix"])

    def test_no_hint_when_skill_not_installed(self):
        self.install(".claude/skills", skill="nckh-plan")
        self.install(".agents/skills")  # a Codex root is not a Claude skill root
        (wire, code), receipt = self.prompt_hint("claude")
        self.assert_never_denies(wire, code)
        self.assertNotIn("nckh routing hint", json.dumps(wire))
        self.assertNotIn("nudge", receipt)

    def test_no_hint_for_explicit_invocation(self):
        self.install(".claude/skills")
        self.install(".agents/skills")
        for host, prompt in (("claude", "/nckh-fix " + self.prompt), ("codex", "$nckh-fix " + self.prompt)):
            with self.subTest(host=host):
                (wire, _), receipt = self.prompt_hint(host, prompt)
                self.assertNotIn("nckh routing hint", json.dumps(wire))
                self.assertNotIn("nudge", receipt)

    def test_cursor_before_submit_prompt_behaviour(self):
        # Cursor has no context channel on beforeSubmitPrompt: the hint is receipt-only.
        self.install(".cursor/skills")
        (wire, code), receipt = self.prompt_hint("cursor")
        self.assertEqual((wire, code), ({}, 0))
        self.assertEqual(receipt["nudge"], {"kind": "route-hint", "skills": ["nckh-fix"], "delivered": False})

    def test_receipt_marks_hint_not_carried_on_the_wire(self):
        # An enforce block replaces the context channel, so the hint never reaches the model.
        self.install(".claude/skills")
        record = event(self.project, "claude", "UserPromptSubmit", prompt=self.prompt)
        (wire, _), receipt = self.run_hook("claude", "UserPromptSubmit", record, mode="enforce")
        self.assertNotIn("nckh routing hint", json.dumps(wire))
        self.assertEqual(receipt["nudge"], {"kind": "route-hint", "skills": ["nckh-fix"], "delivered": False})
        (wire, _), receipt = self.run_hook("claude", "UserPromptSubmit", record, mode="advisory")
        self.assertIn("nckh routing hint", json.dumps(wire))
        self.assertNotIn("delivered", receipt["nudge"])

    def test_agy_has_no_prompt_event(self):
        self.install(".agents/skills")
        for name in ("PreInvocation", "PostInvocation"):
            with self.subTest(event=name):
                record = event(self.project, "agy", name, prompt=self.prompt, toolCall={"name": "x", "args": {}})
                (wire, code), receipt = self.run_hook("agy", name, record)
                self.assertEqual((wire, code), ({}, 0))
                self.assertNotIn("nudge", receipt)

    def write_cycle(self, host, pre, post, tool, tool_input, rewrite):
        record = lambda name: event(self.project, host, name, tool_name=tool, tool_input=tool_input)
        (wire, code), receipt = self.run_hook(host, pre, record(pre))
        self.assert_never_denies(wire, code)
        self.assertNotIn("nudge", receipt)
        rewrite()
        return self.run_hook(host, post, record(post))

    def snapshots_left(self):
        return list((self.project / edit_guard.SNAPSHOT_ROOT).rglob("*.json"))

    def test_eol_pre_post_claude_write(self):
        target = self.project / "notes.md"
        target.write_bytes(b"alpha\r\nbeta\r\n")
        (wire, code), receipt = self.write_cycle("claude", "PreToolUse", "PostToolUse", "Write",
            {"file_path": str(target)}, lambda: target.write_bytes(b"alpha\nbeta\n"))
        self.assert_never_denies(wire, code)
        text = wire["hookSpecificOutput"]["additionalContext"]
        self.assertIn("nckh EOL/BOM guard (advisory)", text)
        self.assertIn("notes.md was crlf", text)
        self.assertEqual(receipt["nudge"]["kind"], "eol-bom")
        self.assertEqual(len(receipt["nudge"]["path_hashes"]), 1)
        self.assertNotIn("notes.md", json.dumps(receipt))
        self.assertEqual(self.snapshots_left(), [])

    def test_recreated_file_ignores_snapshot_left_by_unfinished_edit(self):
        # A denied or rejected write never reaches PostToolUse, so its snapshot stays behind.
        target = self.project / "notes.txt"
        target.write_bytes(b"old\r\n")
        record = lambda name: event(self.project, "claude", name, tool_name="Write",
                                    tool_input={"file_path": "notes.txt"})
        self.run_hook("claude", "PreToolUse", record("PreToolUse"))
        target.unlink()
        self.run_hook("claude", "PreToolUse", record("PreToolUse"))
        target.write_bytes(b"new\n")
        (wire, code), receipt = self.run_hook("claude", "PostToolUse", record("PostToolUse"))
        self.assert_never_denies(wire, code)
        self.assertNotIn("EOL/BOM", json.dumps(wire))
        self.assertNotIn("nudge", receipt)
        self.assertEqual(self.snapshots_left(), [])

    def test_eol_unchanged_has_no_nudge(self):
        target = self.project / "notes.md"
        target.write_bytes(b"alpha\r\nbeta\r\n")
        (wire, _), receipt = self.write_cycle("claude", "PreToolUse", "PostToolUse", "Edit",
            {"file_path": "notes.md"}, lambda: target.write_bytes(b"alpha\r\ngamma\r\n"))
        self.assertNotIn("EOL/BOM", json.dumps(wire))
        self.assertNotIn("nudge", receipt)
        self.assertEqual(self.snapshots_left(), [])

    def test_eol_codex_apply_patch_multi_path(self):
        first, second = self.project / "a.txt", self.project / "b.txt"
        first.write_bytes(b"x\r\n")
        second.write_bytes(b"\xef\xbb\xbfx\n")
        patch = ("*** Begin Patch\n*** Update File: a.txt\n@@\n-x\n+y\n"
                 "*** Update File: b.txt\n@@\n-x\n+y\n*** End Patch")
        def rewrite():
            first.write_bytes(b"y\n")
            second.write_bytes(b"y\n")
        (wire, code), receipt = self.write_cycle("codex", "PreToolUse", "PostToolUse", "apply_patch",
            {"command": patch}, rewrite)
        self.assert_never_denies(wire, code)
        text = wire["hookSpecificOutput"]["additionalContext"]
        self.assertIn("a.txt was crlf", text)
        self.assertIn("b.txt was lf/utf-8 BOM", text)
        self.assertEqual(len(receipt["nudge"]["path_hashes"]), 2)
        self.assertEqual(self.snapshots_left(), [])

    def test_eol_cursor_and_agy_channels(self):
        target = self.project / "notes.md"
        for host, pre, post, tool, fields in (("cursor", "preToolUse", "postToolUse", "Write", {"file_path": "notes.md"}),
                                              ("agy", "PreToolUse", "PostToolUse", "write_to_file", {"TargetFile": "notes.md"})):
            with self.subTest(host=host):
                target.write_bytes(b"alpha\r\n")
                if host == "agy":
                    record = lambda name: event(self.project, host, name, toolCall={"name": tool, "args": fields})
                    self.run_hook(host, pre, record(pre))
                    target.write_bytes(b"alpha\n")
                    (wire, code), receipt = self.run_hook(host, post, record(post))
                    self.assertEqual((wire, code), ({}, 0))  # AGY has no context channel: receipt only
                    self.assertIs(receipt["nudge"]["delivered"], False)
                else:
                    (wire, code), receipt = self.write_cycle(host, pre, post, tool, fields,
                                                            lambda: target.write_bytes(b"alpha\n"))
                    self.assertIn("nckh EOL/BOM guard (advisory)", wire["additional_context"])
                    self.assertNotIn("delivered", receipt["nudge"])
                self.assertEqual(receipt["nudge"]["kind"], "eol-bom")
                self.assertEqual(self.snapshots_left(), [])

    def test_nudge_exception_never_changes_decision(self):
        self.install(".claude/skills")
        target = self.project / "notes.md"
        target.write_bytes(b"alpha\r\n")
        prompt_event = event(self.project, "claude", "UserPromptSubmit", prompt="hello there")
        write_event = event(self.project, "claude", "PreToolUse", tool_name="Write", tool_input={"file_path": "notes.md"})
        for mode in ("advisory", "enforce"):
            with self.subTest(mode=mode):
                baseline = [self.run_hook("claude", name, record, mode=mode)[0]
                            for name, record in (("UserPromptSubmit", prompt_event), ("PreToolUse", write_event))]
                hinted = event(self.project, "claude", "UserPromptSubmit", prompt=self.prompt)
                with mock.patch.object(route_hint, "match", side_effect=RuntimeError("boom")), \
                        mock.patch.object(edit_guard, "snapshot", side_effect=OSError("boom")):
                    failed = [self.run_hook("claude", name, record, mode=mode)
                              for name, record in (("UserPromptSubmit", hinted), ("PreToolUse", write_event))]
                self.assertEqual([wire for wire, _ in failed], baseline)
                self.assertTrue(all("nudge" not in receipt for _, receipt in failed))

    def test_advisory_never_denies_with_nudge(self):
        for root in (".claude/skills", ".agents/skills", ".cursor/skills"):
            self.install(root)
        atomic_json(self.project / "context.json", {"schema_version": 1, "task_id": "fixture",
            "tool_operations": {}, "allowed_operations": [], "brief": {"mode": "auto"}})
        for host in ("claude", "codex", "cursor"):
            for context in ("context.json", "missing.json"):
                with self.subTest(host=host, context=context):
                    record = event(self.project, host, PROMPT_EVENT[host], prompt=self.prompt)
                    (wire, code), receipt = self.run_hook(host, PROMPT_EVENT[host], record, context=context)
                    self.assert_never_denies(wire, code)
                    self.assertEqual(receipt["nudge"]["skills"], ["nckh-fix"])

    def test_prompt_hint_is_bounded_in_time(self):
        self.install(".claude/skills")
        prompt = ("lorem ipsum " * 400) + self.prompt
        started = time.perf_counter()
        self.prompt_hint("claude", prompt)
        self.assertLess(time.perf_counter() - started, 2.0)

    def test_invocation_constants_match_adapters(self):
        for host in ("claude", "codex", "cursor", "agy"):
            with self.subTest(host=host):
                codec = importlib.import_module("hooks.codecs." + host)
                adapter = json.loads((ROOT / "adapters" / host / "adapter.json").read_text(encoding="utf8"))
                self.assertEqual(tuple(codec.SKILL_ROOTS), tuple(adapter["compatibility_project"]))
                if host == "agy":
                    self.assertIsNone(codec.SKILL_INVOCATION)
                    continue
                pattern = codec.SKILL_INVOCATION.replace("{skill}", "NAME")
                self.assertTrue(any(pattern in surface["invocation"] for surface in adapter["surfaces"].values()))
                self.assertNotIn("$NAME" if pattern == "/NAME" else "/NAME",
                                 " ".join(surface["invocation"] for surface in adapter["surfaces"].values()))


if __name__ == "__main__":
    unittest.main()
