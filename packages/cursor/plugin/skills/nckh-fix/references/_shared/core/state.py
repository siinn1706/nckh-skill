"""Durable progression and evidence invalidation, never a permission sandbox."""

from copy import deepcopy
from dataclasses import dataclass

from core.paths import digest_record
from core.schema import ContractError


TRANSITIONS = {
    "planned": {"authorized"}, "authorized": {"running"},
    "running": {"checking", "failed", "timeout-unknown"},
    "checking": {"running", "ready-for-review", "failed", "waiting-human"},
    "ready-for-review": {"accepted", "running", "waiting-human"},
    "waiting-human": {"authorized", "running", "checking"},
    "failed": {"authorized"}, "timeout-unknown": {"checking", "failed"},
    "accepted": set(), "blocked": {"authorized"},
}


@dataclass(frozen=True)
class HostGrant:
    reference: str
    scope_hash: str
    operations: frozenset


def new_task(brief, *, mode, revision):
    if mode not in {"auto", "interactive"}:
        raise ContractError("select exactly one execution mode")
    return {"schema_version": 2, "status": "planned", "mode": mode,
            "scope_hash": digest_record(brief), "revision": revision,
            "authorization_reference": None, "gates": [], "attempts": [],
            "review": None, "history": []}


def transition(task, target, *, grant=None, operation="local-product-write"):
    result = deepcopy(task)
    if target not in TRANSITIONS.get(task["status"], set()):
        raise ContractError(f"illegal transition {task['status']} -> {target}")
    if target in {"authorized", "running"}:
        if not isinstance(grant, HostGrant) or not grant.reference:
            raise ContractError("live host authorization reference is required")
        if grant.scope_hash != task["scope_hash"] or operation not in grant.operations:
            raise ContractError("authorization does not cover this scope/operation")
        result["authorization_reference"] = grant.reference
        if any(a["status"] in {"running", "timeout-unknown"} for a in task["attempts"]):
            raise ContractError("reconcile outstanding attempts before retry")
        review = task.get("review")
        if task["mode"] == "interactive" and review and review["decision"] != "approve":
            raise ContractError("interactive downstream awaits feedback")
        if review and review["revision"] != task["revision"]:
            raise ContractError("review belongs to a stale revision")
    if target == "accepted":
        if aggregate(task["gates"], task["revision"]) != "accepted-for-scope":
            raise ContractError("mandatory acceptance gates are incomplete/stale")
        if task["mode"] == "interactive":
            review = task.get("review")
            if not review or review["decision"] != "approve" or review["revision"] != task["revision"]:
                raise ContractError("interactive acceptance needs current approval")
    result["history"].append({"from": task["status"], "to": target,
                              "revision": task["revision"]})
    result["status"] = target
    return result


def aggregate(gates, revision):
    required = [g for g in gates if g["required"]]
    if not required:
        return "pending"
    if any(g["status"] == "fail" for g in required):
        return "failed"
    if any(g["status"] != "pass" or g["revision"] != revision for g in required):
        return "pending"
    if any(not g.get("evidence_reference") for g in required):
        return "pending"
    return "accepted-for-scope"


def invalidate(task, changed_ids, *, revision):
    result = deepcopy(task)
    affected = set(changed_ids)
    while True:
        extended = affected | {g["id"] for g in result["gates"]
                                if affected.intersection(g.get("depends_on", []))}
        if extended == affected:
            break
        affected = extended
    result["history"].append({"event": "invalidation", "revision": task["revision"],
                              "affected": sorted(affected)})
    for gate in result["gates"]:
        if gate["id"] in affected:
            gate["previous_evidence"] = gate.get("evidence_reference")
            gate["status"] = "stale"
        elif gate["revision"] == task["revision"]:
            gate["revision"] = revision
    result.update(revision=revision, status="planned", authorization_reference=None, review=None)
    return result


def review_boundary(task, *, artifact, artifact_hash, locked_scope):
    if task["status"] not in {"checking", "ready-for-review"}:
        raise ContractError("review boundary requires a checked artifact")
    result = deepcopy(task)
    result["review"] = {"artifact": artifact, "artifact_hash": artifact_hash,
                        "locked_scope": locked_scope, "revision": task["revision"],
                        "decision": "pending", "feedback_reference": None}
    result["status"] = "waiting-human"
    return result


def feedback(task, *, decision, revision, artifact_hash, human_reference):
    if decision not in {"approve", "request-changes", "reject"} or not human_reference:
        raise ContractError("record a real human decision/reference")
    result = deepcopy(task)
    review = result.get("review")
    if not review or revision != task["revision"] or artifact_hash != review["artifact_hash"]:
        raise ContractError("feedback does not identify the current artifact")
    review.update(decision=decision, feedback_reference=human_reference)
    return result
