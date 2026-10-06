"""Bounded deterministic policy; native permissions and human grants remain authoritative."""

from core.guards import check_visual_purpose, factual_delta, _visual_file
from core.paths import contained
from core.schema import ContractError, validate_record


MAX_EVENT_BYTES = 65536
MAX_CONTEXT_BYTES = 131072
MAX_PATHS = 16
MAX_REFERENCES = 32
MUTATIONS = {"write", "generate-visual", "publish", "provider", "schema-change", "data-change"}


def evaluate(event, context, *, project):
    validate_record("hook-event", event)
    def decision(state, reason):
        return validate_record("hook-decision", {"schema_version": 1, "decision": state,
            "reason_codes": [reason], "evidence_class": "deterministic", "native_enforcement": "unverified",
            "semantic_fidelity": "unverified", "side_effects": "none"})
    if not isinstance(context, dict) or context.get("schema_version") != 1:
        return decision("pending", "controller-context-missing")
    if len(event["paths"]) > MAX_PATHS or len(context.get("references", [])) > MAX_REFERENCES:
        return decision("block", "bounded-input-exceeded")
    for relative in event["paths"]:
        try:
            contained(project, relative)
        except ContractError:
            return decision("block", "project-path-escape")
        pieces = relative.casefold().split("/")
        if (set(pieces) & {"private", "holdout", "credentials", ".ssh", ".aws"}
                or pieces[-1] in {".env", "credentials.json", "secrets.json"}
                or pieces[-1].endswith((".pem", ".key"))):
            return decision("block", "private-holdout-credential-path")
    operation = context.get("tool_operations", {}).get(event["tool"])
    if event["phase"] == "preflight":
        if operation is None:
            return decision("manual", "tool-route-uncovered")
        brief = context.get("brief", {})
        if brief.get("mode") == "plan-only" and operation in MUTATIONS:
            return decision("block", "plan-only-mutation")
        if operation in MUTATIONS and operation not in context.get("allowed_operations", []):
            return decision("pending", "operation-grant-missing")
        if operation == "generate-visual":
            purpose = check_visual_purpose(brief, project=project, sources=context.get("sources"))
            return decision(purpose["decision"], purpose["reason_code"])
        return decision("allow", "declared-route-checks-current")
    if event["phase"] == "pre-delivery":
        try:
            artifact = context["artifact"]
            _visual_file(project, artifact)
            if artifact["sha256"] != event["artifact_sha256"]:
                return decision("pending", "artifact-final-bytes-stale")
        except (ContractError, OSError, KeyError, TypeError):
            return decision("pending", "artifact-final-bytes-missing-or-stale")
        for reference in context.get("references", []):
            if not reference.get("locator") or not reference.get("source_id"):
                return decision("pending", "artifact-source-locator-missing")
            try:
                _visual_file(project, reference["file"])
            except (ContractError, OSError, KeyError):
                return decision("pending", "artifact-source-stale")
        fidelity = context.get("fidelity")
        if fidelity:
            try:
                delta = factual_delta(fidelity["before"], fidelity["after"],
                    protected_before=fidelity["protected_before"], protected_after=fidelity["protected_after"])
            except (ContractError, KeyError):
                return decision("pending", "declared-factual-slots-missing")
            if delta["changes"]:
                return decision("pending", "protected-or-factual-delta")
        if context.get("visual_delivery"):
            purpose = check_visual_purpose(context.get("brief", {}), project=project, sources=context.get("sources"))
            if purpose["decision"] != "allow":
                return decision("pending", purpose["reason_code"])
            if context.get("qa_artifact_sha256") != event["artifact_sha256"]:
                return decision("pending", "figure-qa-stale")
        return decision("advisory", "delivery-bindings-current-review-separate")
    return decision("advisory", "writing-resource-advice-only")
