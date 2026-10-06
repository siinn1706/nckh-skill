"""Claude Code documented command-hook fields; native coverage remains unverified."""

from hooks.codecs.common import decode_snake, encode_snake

EVENTS = {"SessionStart": "advisory", "UserPromptSubmit": "advisory", "PreToolUse": "preflight",
          "PostToolUse": "pre-delivery", "Stop": "stop"}


def decode(payload, event_name):
    return decode_snake(payload, event_name, EVENTS)


def encode(event_name, decision):
    return encode_snake(event_name, decision)
