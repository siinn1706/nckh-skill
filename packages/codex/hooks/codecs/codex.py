"""Codex release hook contract; no trust mutation or hosted-tool coverage claim."""

from hooks.codecs.common import decode_snake, encode_snake
from core.hook_policy import MAX_EVENT_BYTES, MAX_PATHS
from core.schema import ContractError

EVENTS = {"SessionStart": "advisory", "UserPromptSubmit": "advisory", "PreToolUse": "preflight",
          "PostToolUse": "pre-delivery", "Stop": "stop"}
WRITE_TOOLS = frozenset({"apply_patch"})
# Mirrors the adapter invocation `$NAME` and its compatibility_project roots.
SKILL_INVOCATION = "${skill}"
SKILL_ROOTS = (".agents/skills",)


def patch_paths(command):
    if not isinstance(command, str) or "\x00" in command or len(command.encode("utf8")) > MAX_EVENT_BYTES:
        raise ContractError("bounded Codex patch text missing or invalid")
    lines = command.strip().splitlines()
    if len(lines) < 3 or lines[0] != "*** Begin Patch" or lines[-1] != "*** End Patch":
        raise ContractError("unsupported Codex patch envelope")
    paths = []
    operation = None
    can_move = False
    headers = {"*** Add File: ": "add", "*** Update File: ": "update", "*** Delete File: ": "delete"}
    for line in lines[1:-1]:
        header = next((prefix for prefix in headers if line.startswith(prefix)), None)
        if header is not None:
            path = line[len(header):].strip()
            operation = headers[header]
            can_move = operation == "update"
        elif line.startswith("*** Move to: "):
            if not can_move:
                raise ContractError("unsupported Codex patch move position")
            path = line[len("*** Move to: "):].strip()
            can_move = False
        else:
            if line.startswith("***") and not (operation == "update" and line == "*** End of File"):
                raise ContractError("unsupported Codex patch marker")
            if (operation is None or operation == "delete" or
                    (operation == "add" and not line.startswith("+")) or
                    (operation == "update" and line and not line.startswith((" ", "+", "-", "@@", "*** End of File")))):
                raise ContractError("unsupported Codex patch body")
            can_move = False
            continue
        if not path or len(paths) >= MAX_PATHS:
            raise ContractError("bounded Codex patch paths missing or exceeded")
        paths.append(path)
    if not paths:
        raise ContractError("Codex patch has no file paths")
    return paths


def decode(payload, event_name):
    if not isinstance(payload.get("model"), str):
        raise ContractError("Codex model field missing")
    if event_name in {"PreToolUse", "PostToolUse", "Stop", "UserPromptSubmit"} and not isinstance(payload.get("turn_id"), str):
        raise ContractError("Codex turn identifier missing")
    decoded = decode_snake(payload, event_name, EVENTS)
    if event_name in {"PreToolUse", "PostToolUse"} and decoded["tool"] == "apply_patch":
        fields = payload["tool_input"]
        if not isinstance(fields, dict):
            raise ContractError("Codex native patch input missing")
        paths = patch_paths(fields.get("command"))
        for key in ("file_path", "path"):
            if key in fields:
                if not isinstance(fields[key], str) or not fields[key]:
                    raise ContractError("Codex patch path alias invalid")
                paths.append(fields[key])
        decoded["raw_paths"] = list(dict.fromkeys(paths))
    return decoded


def encode(event_name, decision):
    # This documented subset uses hookSpecificOutput, never forbidden PreToolUse fields.
    return encode_snake(event_name, decision)
