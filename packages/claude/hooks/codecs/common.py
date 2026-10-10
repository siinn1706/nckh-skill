"""Shared documented snake-case fields; each host owns its event inventory."""

from core.paths import digest_record
from core.schema import ContractError

PROMPT_EVENTS = {"UserPromptSubmit"}
CONTEXT_EVENTS = {"SessionStart", "UserPromptSubmit", "PostToolUse"}


def prompt_field(payload, event_name, prompt_events):
    """Return the prompt string of a prompt event, otherwise None."""
    prompt = payload.get("prompt") if event_name in prompt_events else None
    return prompt if isinstance(prompt, str) else None


def context_text(decision):
    """Join an optional nudge with the reason codes of a non-allow decision."""
    parts = [decision["nudge_text"]] if decision.get("nudge_text") else []
    if decision["decision"] != "allow" and decision["reason_codes"]:
        parts.append("; ".join(decision["reason_codes"]))
    return "\n".join(parts)


def decode_snake(payload, event_name, events):
    if event_name not in events or payload.get("hook_event_name") != event_name:
        raise ContractError("unsupported/mismatched hook event")
    if not isinstance(payload.get("session_id"), str) or not isinstance(payload.get("cwd"), str):
        raise ContractError("hook session/cwd missing")
    tool = payload.get("tool_name", "")
    fields = payload.get("tool_input", {})
    if event_name in {"PreToolUse", "PostToolUse"} and (not isinstance(tool, str) or not tool or "tool_input" not in payload):
        raise ContractError("tool fields missing")
    path = fields.get("file_path", fields.get("path")) if isinstance(fields, dict) else None
    return {"phase": events[event_name], "tool": tool, "raw_paths": [path] if isinstance(path, str) else [],
            "reported_roots": [payload["cwd"]], "session_key": digest_record(payload["session_id"]),
            "stop_active": payload.get("stop_hook_active", False),
            "prompt": prompt_field(payload, event_name, PROMPT_EVENTS)}


def encode_snake(event_name, decision):
    """Map a decision to the documented snake-case wire.

    Only PreToolUse (deny) and UserPromptSubmit (block) can stop the host, so an
    enforce-mode block fails closed only there. SessionStart, UserPromptSubmit and
    PostToolUse carry advisory context: an optional nudge first, then the reason
    codes of any non-allow decision. Stop never forces continuation and returns {}.
    """
    reason = "; ".join(decision["reason_codes"])
    if event_name == "PreToolUse" and decision["decision"] in {"block", "pending"}:
        return {"hookSpecificOutput": {"hookEventName": event_name, "permissionDecision": "deny", "permissionDecisionReason": reason}}, 0
    if event_name == "UserPromptSubmit" and decision["decision"] == "block":
        return {"decision": "block", "reason": reason}, 0
    if event_name in CONTEXT_EVENTS and (decision["decision"] != "allow" or decision.get("nudge_text")):
        return {"hookSpecificOutput": {"hookEventName": event_name, "additionalContext": context_text(decision)}}, 0
    return {}, 0
