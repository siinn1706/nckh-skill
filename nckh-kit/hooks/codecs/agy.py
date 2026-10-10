"""AGY named-group hooks/camelCase input; failure exit semantics remain unverified.

AGY has no prompt event, so routing hints never run here. PostToolUse has no
context channel either: an EOL/BOM finding is recorded in the receipt only.
"""

from core.paths import digest_record
from core.schema import ContractError

EVENTS = {"PreToolUse": "preflight", "PostToolUse": "pre-delivery", "PreInvocation": "advisory",
          "PostInvocation": "advisory", "Stop": "stop"}
TOOL_PATH_FIELDS = {"write_to_file": "TargetFile", "replace_file_content": "TargetFile",
                    "multi_replace_file_content": "TargetFile", "view_file": "AbsolutePath",
                    "list_dir": "DirectoryPath", "find_by_name": "SearchDirectory", "grep_search": "SearchPath"}
PATH_FIELDS = ("TargetFile", "AbsolutePath", "DirectoryPath", "SearchDirectory", "SearchPath", "file_path", "path")
WRITE_TOOLS = frozenset({"write_to_file", "replace_file_content", "multi_replace_file_content"})
SKILL_INVOCATION = None
SKILL_ROOTS = (".agents/skills",)


def decode(payload, event_name):
    if event_name not in EVENTS:
        raise ContractError("unsupported AGY event")
    if (not isinstance(payload.get("conversationId"), str) or not isinstance(payload.get("workspacePaths"), list)
            or not all(isinstance(root, str) for root in payload["workspacePaths"])):
        raise ContractError("AGY conversation/workspace fields missing")
    call = payload.get("toolCall", {})
    if event_name in {"PreToolUse", "PostToolUse"} and (not isinstance(call, dict)
            or not isinstance(call.get("name"), str) or not call["name"] or not isinstance(call.get("args"), dict)):
        raise ContractError("AGY toolCall fields missing")
    args = call.get("args", {})
    required_path = TOOL_PATH_FIELDS.get(call.get("name"))
    if required_path and required_path not in args:
        raise ContractError("AGY native tool path missing")
    paths = []
    for field in PATH_FIELDS:
        if field in args:
            if not isinstance(args[field], str) or not args[field]:
                raise ContractError("AGY tool path malformed")
            paths.append(args[field])
    return {"phase": EVENTS[event_name], "tool": call.get("name", ""), "raw_paths": paths,
            "reported_roots": payload["workspacePaths"], "session_key": digest_record(payload["conversationId"]),
            "stop_active": payload.get("executionNum", 0) > 1, "prompt": None}


def encode(event_name, decision):
    # Only PreToolUse can deny; every other event, degraded or not, stays advisory.
    if event_name == "PreToolUse":
        if decision["decision"] in {"block", "pending"}:
            return {"decision": "deny", "reason": "; ".join(decision["reason_codes"])}, 0
        return {"decision": "ask"}, 0
    if event_name == "Stop":
        return {"decision": "stop"}, 0
    # No permissionOverrides, injected tool/user messages or forced continuation.
    return {}, 0
