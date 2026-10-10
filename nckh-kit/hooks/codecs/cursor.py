"""Cursor lower-camel events/flat handlers; failClosed only for documented permission hooks.

beforeSubmitPrompt documents only `continue`/`user_message`, with no channel to add
context, so a routing hint for a prompt is recorded in the receipt as `delivered: false`
and never sent.
postToolUse carries an EOL/BOM nudge through `additional_context`.
"""

from core.paths import digest_record
from core.schema import ContractError

EVENTS = {"sessionStart": "advisory", "beforeSubmitPrompt": "advisory", "preToolUse": "preflight",
          "postToolUse": "pre-delivery", "stop": "stop"}
# Cursor's write-tool path field is undocumented; decode reads file_path/path when present.
WRITE_TOOLS = frozenset({"Write"})
# Mirrors the adapter invocation `/NAME` and its compatibility_project roots.
SKILL_INVOCATION = "/{skill}"
SKILL_ROOTS = (".cursor/skills", ".agents/skills", ".claude/skills", ".codex/skills")


def decode(payload, event_name):
    if event_name not in EVENTS or payload.get("hook_event_name") != event_name:
        raise ContractError("unsupported/mismatched Cursor hook event")
    if (not isinstance(payload.get("conversation_id"), str) or not isinstance(payload.get("workspace_roots"), list)
            or not all(isinstance(root, str) for root in payload["workspace_roots"])):
        raise ContractError("Cursor conversation/workspace fields missing")
    tool = payload.get("tool_name", "")
    fields = payload.get("tool_input", {})
    if event_name in {"preToolUse", "postToolUse"} and (not tool or not isinstance(fields, dict)):
        raise ContractError("Cursor tool fields missing")
    path = fields.get("file_path", fields.get("path"))
    prompt = payload.get("prompt") if event_name == "beforeSubmitPrompt" else None
    return {"phase": EVENTS[event_name], "tool": tool, "raw_paths": [path] if isinstance(path, str) else [],
            "reported_roots": payload["workspace_roots"], "session_key": digest_record(payload["conversation_id"]),
            "stop_active": payload.get("loop_count", 0) > 0, "prompt": prompt if isinstance(prompt, str) else None}


def encode(event_name, decision):
    # Only preToolUse and beforeSubmitPrompt can stop the host; other events stay advisory.
    reason = "; ".join(decision["reason_codes"])
    if event_name == "preToolUse" and decision["decision"] in {"block", "pending"}:
        return {"permission": "deny", "user_message": reason}, 0
    if event_name == "beforeSubmitPrompt" and decision["decision"] == "block":
        return {"continue": False, "user_message": reason}, 0
    if event_name in {"sessionStart", "postToolUse"}:
        nudge = decision.get("nudge_text")
        return {"additional_context": nudge + "\n" + reason if nudge and reason else nudge or reason}, 0
    return {}, 0
