"""Claude Code documented command-hook fields; native coverage remains unverified."""

from hooks.codecs.common import decode_snake, encode_snake

EVENTS = {"SessionStart": "advisory", "UserPromptSubmit": "advisory", "PreToolUse": "preflight",
          "PostToolUse": "pre-delivery", "Stop": "stop"}
WRITE_TOOLS = frozenset({"Write", "Edit", "MultiEdit"})
# Mirrors the adapter invocation `/NAME` and its compatibility_project roots.
SKILL_INVOCATION = "/{skill}"
SKILL_ROOTS = (".claude/skills",)


def decode(payload, event_name):
    return decode_snake(payload, event_name, EVENTS)


def encode(event_name, decision):
    return encode_snake(event_name, decision)
