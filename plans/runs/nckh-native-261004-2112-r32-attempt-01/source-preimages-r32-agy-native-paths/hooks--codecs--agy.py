"""AGY named-group hooks/camelCase input; failure exit semantics remain unverified."""

from core.paths import digest_record
from core.schema import ContractError

EVENTS = {"PreToolUse": "preflight", "PostToolUse": "pre-delivery", "PreInvocation": "advisory",
          "PostInvocation": "advisory", "Stop": "stop"}


def decode(payload, event_name):
    if event_name not in EVENTS:
        raise ContractError("unsupported AGY event")
    if (not isinstance(payload.get("conversationId"), str) or not isinstance(payload.get("workspacePaths"), list)
            or not all(isinstance(root, str) for root in payload["workspacePaths"])):
        raise ContractError("AGY conversation/workspace fields missing")
    call = payload.get("toolCall", {})
    if event_name in {"PreToolUse", "PostToolUse"} and (not isinstance(call, dict) or not call.get("name") or not isinstance(call.get("args"), dict)):
        raise ContractError("AGY toolCall fields missing")
    args = call.get("args", {})
    path = args.get("file_path", args.get("path"))
    return {"phase": EVENTS[event_name], "tool": call.get("name", ""), "raw_paths": [path] if isinstance(path, str) else [],
            "reported_roots": payload["workspacePaths"], "session_key": digest_record(payload["conversationId"]),
            "stop_active": payload.get("executionNum", 0) > 1}


def encode(event_name, decision):
    if event_name == "PreToolUse":
        if decision["decision"] in {"block", "pending"}:
            return {"decision": "deny", "reason": "; ".join(decision["reason_codes"])}, 0
        return {"decision": "ask"}, 0
    if event_name == "Stop":
        return {"decision": "stop"}, 0
    # No permissionOverrides, injected tool/user messages or forced continuation.
    return {}, 0
