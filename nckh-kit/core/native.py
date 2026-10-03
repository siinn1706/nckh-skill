"""Host encodings from reviewed capability inputs; no discovery or model calls."""

import json
import re
import tomllib

from core.models import PROFILES, resolve_model
from core.paths import skill_id
from core.schema import ContractError


ROLES = {"explorer": ("fast", True), "planner": ("deep", True),
         "researcher": ("worker", True), "maker": ("worker", False),
         "reviewer": ("deep", True), "taste-critic": ("worker", True)}
MODEL_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")
EFFORT_ID = re.compile(r"^[a-z][a-z0-9-]*$")


def agent_filename(host, identity):
    if host not in {"claude", "codex", "cursor", "agy"}:
        raise ContractError("unknown native host")
    return skill_id(identity) + (".toml" if host == "codex" else ".md")


def encode_agent(host, identity, description, instructions, *, model="inherit", effort=None, read_only=False):
    agent_filename(host, identity)
    if not isinstance(model, str) or not MODEL_ID.fullmatch(model):
        raise ContractError("invalid native model identifier")
    if effort is not None and (not isinstance(effort, str) or not EFFORT_ID.fullmatch(effort)):
        raise ContractError("invalid native reasoning effort")
    if model == "inherit" and effort is not None:
        raise ContractError("effort override requires an explicitly eligible model")
    if host == "agy" and (model not in {"inherit", "flash", "pro"} or effort is not None):
        raise ContractError("Antigravity custom agents support documented aliases; effort control is unverified")
    if host == "codex":
        fields = {"name": identity, "description": description, "developer_instructions": instructions}
        if model != "inherit":
            fields["model"] = model
        if effort is not None:
            fields["model_reasoning_effort"] = effort
        if read_only:
            fields["sandbox_mode"] = "read-only"
        result = "\n".join(key + " = " + json.dumps(value, ensure_ascii=False) for key, value in fields.items()) + "\n"
        tomllib.loads(result)
        return result
    fields = {"name": identity, "description": description, "model": model}
    if host == "cursor":
        fields["readonly"] = read_only
        if effort is not None:
            fields["model"] = model + "[effort=" + effort + "]"
    elif host == "claude":
        if effort is not None:
            fields["effort"] = effort
        if read_only:
            fields["tools"] = "Read, Glob, Grep, WebFetch, WebSearch"
    else:
        fields.update(mainAgent=False, subagent=True)
        if read_only:
            fields.update(tools=["view_file", "grep_search"], commandExecutionPolicy="off")
    frontmatter = "\n".join(key + ": " + json.dumps(value, ensure_ascii=False) for key, value in fields.items())
    return "---\n" + frontmatter + "\n---\n\n" + instructions


def configured_agent(host, role, description, instructions, *, profile, capabilities):
    if role not in ROLES or profile not in PROFILES:
        raise ContractError("unknown native role/profile")
    tier, read_only = ROLES[role]
    native = capabilities.get("native_models", {}).get(host)
    if native is None:
        if profile == "custom":
            raise ContractError("custom native model mapping unavailable; supply reviewed per-host capabilities")
        result = resolve_model(tier="inherit", profile=profile, requested="inherit", effort=None,
                               capabilities={}, allowed_models=set())
        state = "inherit-only; tier model mapping unavailable"
    else:
        if not isinstance(native, dict) or not native.get("evidence_reference") or not native.get("as_of"):
            raise ContractError("native model availability requires an observed evidence reference and date")
        tier_mapping = native.get("mapping", {}).get(tier)
        if not isinstance(tier_mapping, dict) or set(tier_mapping) != {"model", "effort"}:
            raise ContractError("native mapping must specify model and effort for every required tier")
        if tier_mapping["model"] == "inherit" and tier_mapping["effort"] is not None:
            raise ContractError("explicit inheritance cannot include a model-specific effort")
        result = resolve_model(tier="inherit" if tier_mapping["model"] == "inherit" else tier, profile=profile, requested=tier_mapping["model"],
                               effort=tier_mapping["effort"], capabilities=native,
                               allowed_models=set(native.get("allowed_models", [])))
        if result["resolved_model"] is None:
            raise ContractError("NOT_CALLABLE: " + result["reason"])
        state = "encoded; native application/effective settings unverified"
    text = encode_agent(host, "nckh-" + role, description, instructions,
                        model=result["resolved_model"], effort=result["resolved_effort"], read_only=read_only)
    return text, {**result, "configuration_state": state}
