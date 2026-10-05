"""Model selection from supplied capabilities, without provider calls."""

import math

from core.schema import ContractError


PROFILES = {"auto", "cost-optimized", "balanced", "quality-first", "custom"}
REASONS = {"cheaper-eligible", "stronger-reasoning", "fresh-context",
           "independent-check", "parallel-work", "specialist-tools"}


def delegation_allowed(reasons, *, same_model, same_purpose):
    if not reasons or not set(reasons) <= REASONS:
        return False
    if same_model and same_purpose:
        return bool(set(reasons) & {"fresh-context", "independent-check", "parallel-work", "specialist-tools"})
    return True


def resolve_model(*, tier, profile, requested, effort, capabilities, allowed_models):
    if tier not in {"fast", "worker", "deep", "inherit"} or profile not in PROFILES:
        raise ContractError("invalid logical tier/profile")
    result = {"tier": tier, "profile": profile, "requested_model": requested,
              "requested_effort": effort, "resolved_model": None,
              "resolved_effort": None, "effective_model": "unknown",
              "effective_effort": "unknown", "observation": "not-run",
              "cost": "unknown", "window": "unknown", "reason": None}
    if requested == "inherit" and tier == "inherit":
        result.update(resolved_model="inherit", reason="explicit native inheritance")
        return result
    if capabilities.get("per_agent_override") is not True:
        result["reason"] = "per-agent control unverified or unsupported; use same-agent only if outcome permits"
        return result
    models = capabilities.get("models", [])
    if not isinstance(models, list):
        raise ContractError("observed model inventory must be an array")
    for model in models:
        if (not isinstance(model, dict) or not isinstance(model.get("id"), str)
                or not isinstance(model.get("tiers"), list) or not set(model["tiers"]) <= {"fast", "worker", "deep", "inherit"}
                or not isinstance(model.get("efforts", []), list)
                or any(not isinstance(item, str) for item in model.get("efforts", []))):
            raise ContractError("invalid observed model capability record")
    candidates = [m for m in models
                  if m["id"] in allowed_models and tier in m["tiers"]
                  and m.get("availability") == "observed"]
    if requested and requested != "auto":
        candidates = [m for m in candidates if m["id"] == requested]
    if effort is not None:
        candidates = [m for m in candidates if effort in m.get("efforts", [])]
    if profile == "cost-optimized":
        candidates = [m for m in candidates if m.get("quality_floor_pass") is True
                      and type(m.get("cost")) in {int, float} and math.isfinite(m["cost"]) and m["cost"] >= 0]
        candidates.sort(key=lambda m: m["cost"])
    if not candidates:
        result["reason"] = "no authorized, available model/effort for required tier; no downgrade"
        return result
    result.update(resolved_model=candidates[0]["id"], resolved_effort=effort,
                  reason="eligible capability mapping; effective settings require actual receipt")
    return result
