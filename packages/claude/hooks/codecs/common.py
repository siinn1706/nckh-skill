"""Shared documented snake-case fields; each host owns its event inventory."""

from core.paths import digest_record
from core.schema import ContractError


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
            "stop_active": payload.get("stop_hook_active", False)}


def encode_snake(event_name, decision):
    reason = "; ".join(decision["reason_codes"])
    if event_name == "PreToolUse" and decision["decision"] in {"block", "pending"}:
        return {"hookSpecificOutput": {"hookEventName": event_name, "permissionDecision": "deny", "permissionDecisionReason": reason}}, 0
    if event_name == "UserPromptSubmit" and decision["decision"] == "block":
        return {"decision": "block", "reason": reason}, 0
    if event_name in {"SessionStart", "UserPromptSubmit", "PostToolUse"} and decision["decision"] != "allow":
        return {"hookSpecificOutput": {"hookEventName": event_name, "additionalContext": reason}}, 0
    return {}, 0
