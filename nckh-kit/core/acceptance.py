"""Shared personal-use acceptance profile and owner-feedback binding.

This module validates the local acceptance profile against the approved catalog.
It does not run a model, call a provider, assign scientific quality, or turn an
owner verdict into stable qualification.
"""

from copy import deepcopy
import json
import re
from pathlib import Path

from core.build import APPROVED_IDENTITIES, load_json, validate_catalog
from core.paths import contained, skill_id as validate_skill_id
from core.schema import ContractError


PROFILE_PATH = "core/profiles/acceptance/personal-use.json"
CATALOG_PATH = "core/registry/catalog/skills.json"
POLICY_PATH = "core/policies/acceptance-policy.md"
QUALIFICATION_PATH = "evals/protocols/qualification.json"
VERDICTS = ("pass", "fail", "pending", "not-applicable")
GATE_IDS = (
    "identity-route",
    "positive-behavior",
    "output-facts",
    "authority-side-effects",
    "receipt-feedback",
)
SOURCE_ID = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*$")


def _load_json(path):
    try:
        return load_json(path)
    except (OSError, json.JSONDecodeError) as error:
        raise ContractError(f"cannot read acceptance JSON: {path}: {error}") from error


def _require_string(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"acceptance profile field is empty: {field}")
    return value


def _require_string_list(value, field, *, allow_empty=False):
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ContractError(f"acceptance profile field is not a nonempty list: {field}")
    for index, item in enumerate(value):
        _require_string(item, f"{field}[{index}]")
    return value


def _validate_sources(profile):
    sources = profile.get("sources")
    if not isinstance(sources, dict) or not sources:
        raise ContractError("acceptance profile has no source definitions")
    for source_id, source in sources.items():
        if not isinstance(source_id, str) or not SOURCE_ID.fullmatch(source_id):
            raise ContractError(f"invalid acceptance source ID: {source_id!r}")
        if not isinstance(source, dict):
            raise ContractError(f"acceptance source is not an object: {source_id}")
        _require_string(source.get("title"), f"sources.{source_id}.title")
        urls = _require_string_list(source.get("urls"), f"sources.{source_id}.urls")
        for url in urls:
            if not re.match(r"^https?://[^\s]+$", url):
                raise ContractError(f"acceptance source URL is not absolute: {source_id}")
        _require_string(source.get("citation"), f"sources.{source_id}.citation")
        _require_string(source.get("applicability"), f"sources.{source_id}.applicability")
        _require_string(source.get("limitations"), f"sources.{source_id}.limitations")
        _require_string(source.get("retrieved_on"), f"sources.{source_id}.retrieved_on")
    return sources


def _validate_skill_rows(profile, catalog=None):
    skills = profile.get("skills")
    if not isinstance(skills, dict) or set(skills) != APPROVED_IDENTITIES:
        raise ContractError("acceptance profile must contain the exact 43 approved skills")
    source_ids = set(profile["sources"])
    catalog_rows = validate_catalog(catalog) if catalog is not None else {}
    for identity, row in skills.items():
        validate_skill_id(identity)
        if not isinstance(row, dict):
            raise ContractError(f"acceptance skill row is not an object: {identity}")
        _require_string(row.get("kit"), f"skills.{identity}.kit")
        if row["kit"] not in {"core", "engineer", "marketing", "tooling"}:
            raise ContractError(f"acceptance skill has unknown kit: {identity}")
        if row.get("catalog_status") != "experimental":
            raise ContractError(f"acceptance skill status changed: {identity}")
        expected_eval_ids = [f"{identity}:{case_type}"
                             for case_type in ("positive", "negative", "outcome", "failure")]
        if row.get("eval_ids") != expected_eval_ids:
            raise ContractError(f"acceptance eval IDs do not match catalog contract: {identity}")
        criteria = row.get("criteria")
        if not isinstance(criteria, dict):
            raise ContractError(f"acceptance criteria missing: {identity}")
        for criterion in ("positive", "negative", "failure_or_output", "authority"):
            _require_string(criteria.get(criterion), f"skills.{identity}.criteria.{criterion}")
        refs = _require_string_list(row.get("source_ids"), f"skills.{identity}.source_ids")
        if not set(refs) <= source_ids:
            missing = sorted(set(refs) - source_ids)
            raise ContractError(f"acceptance source reference is undefined for {identity}: {missing}")
        if catalog is not None:
            catalog_row = catalog_rows.get(identity)
            if catalog_row is None:
                raise ContractError(f"acceptance profile has unknown identity: {identity}")
            if row["kit"] != catalog_row["kit"] or row["catalog_status"] != catalog_row["status"]:
                raise ContractError(f"acceptance catalog metadata mismatch: {identity}")
            if row["eval_ids"] != catalog_row["eval_ids"]:
                raise ContractError(f"acceptance eval IDs differ from catalog: {identity}")
    if catalog is not None and set(skills) != set(catalog_rows):
        missing = sorted(set(catalog_rows) - set(skills))
        extra = sorted(set(skills) - set(catalog_rows))
        raise ContractError(f"acceptance/catalog identity mismatch: missing={missing}, extra={extra}")
    return skills


def validate_profile(profile, *, catalog=None):
    """Validate the profile and, when supplied, its exact catalog mapping."""
    if (not isinstance(profile, dict) or type(profile.get("schema_version")) is not int
            or profile["schema_version"] != 1):
        raise ContractError("unsupported acceptance profile schema")
    for field in ("id", "revision", "lane", "catalog_revision", "catalog_status"):
        _require_string(profile.get(field), field)
    if profile["lane"] != "personal-use" or profile["catalog_status"] != "experimental":
        raise ContractError("acceptance profile lane/status changed")
    if profile.get("verdicts") != list(VERDICTS):
        raise ContractError("acceptance verdict vocabulary changed")

    common = profile.get("common")
    if not isinstance(common, dict):
        raise ContractError("acceptance profile has no common criteria")
    gates = common.get("gates")
    if not isinstance(gates, list) or [gate.get("id") for gate in gates] != list(GATE_IDS):
        raise ContractError("acceptance common gate inventory changed")
    for gate in gates:
        if not isinstance(gate, dict) or gate.get("required_for_personal_use") is not True:
            raise ContractError("personal-use common gates must remain required")
        _require_string(gate.get("check"), f"common.gates.{gate.get('id')}.check")
    _require_string(common.get("hard_gate_policy"), "common.hard_gate_policy")
    _require_string(common.get("threshold_policy"), "common.threshold_policy")

    personal_use = profile.get("personal_use")
    if not isinstance(personal_use, dict) or personal_use.get("owner_final") is not True:
        raise ContractError("personal-use owner-final policy is missing")
    if personal_use.get("external_reviewer_required") is not False:
        raise ContractError("external reviewer must not be a personal-use prerequisite")
    if personal_use.get("protected_holdout_required") is not False:
        raise ContractError("protected holdout must not be a personal-use prerequisite")
    if personal_use.get("absent_feedback_status") != "pending-personal-review":
        raise ContractError("missing owner feedback must remain pending-personal-review")
    if personal_use.get("feedback_mismatch") != "fail-closed":
        raise ContractError("feedback mismatch must fail closed")
    if personal_use.get("fabricated_pass_forbidden") is not True:
        raise ContractError("fabricated pass guard is missing")
    _require_string_list(personal_use.get("feedback_binding"), "personal_use.feedback_binding")
    _require_string_list(personal_use.get("owner_feedback_fields"), "personal_use.owner_feedback_fields")

    boundary = profile.get("qualification_boundary")
    if not isinstance(boundary, dict) or boundary.get("catalog_status_remains") != "experimental":
        raise ContractError("qualification boundary does not preserve experimental catalog status")
    if boundary.get("protocol_mutation") != "forbidden":
        raise ContractError("historical qualification protocol may not be changed by personal-use profile")
    _require_string(boundary.get("stable_scientific_protocol"), "qualification_boundary.stable_scientific_protocol")
    _validate_sources(profile)
    _validate_skill_rows(profile, catalog=catalog)
    return profile


def load_profile(root):
    """Load and validate the self-contained profile against the current catalog."""
    root = Path(root)
    profile = _load_json(contained(root, PROFILE_PATH))
    catalog = _load_json(contained(root, CATALOG_PATH))
    return validate_profile(profile, catalog=catalog)


def lookup(root, identity):
    """Return common criteria, one skill row and its resolved source records."""
    profile = load_profile(root)
    identity = validate_skill_id(identity)
    row = profile["skills"].get(identity)
    if row is None:
        raise ContractError(f"unknown acceptance skill: {identity}")
    return {
        "profile_id": profile["id"],
        "profile_revision": profile["revision"],
        "lane": profile["lane"],
        "skill_id": identity,
        "common": deepcopy(profile["common"]),
        "skill": deepcopy(row),
        "sources": {source_id: deepcopy(profile["sources"][source_id])
                    for source_id in row["source_ids"]},
    }


def acceptance_profile_path(root):
    """Return the contained profile path for closure/reachability checks."""
    return contained(Path(root), PROFILE_PATH)


def bind_owner_feedback(feedback, *, revision, artifact_hash, input_hashes):
    """Bind owner feedback to the exact artifact, inputs and revision.

    Missing feedback is an honest pending record. A recorded owner verdict is
    returned as evidence only; this function never aggregates gates or grants
    stable/scientific acceptance.
    """
    _require_string(revision, "revision")
    _require_string(artifact_hash, "artifact_hash")
    expected_inputs = _require_string_list(list(input_hashes), "input_hashes", allow_empty=True)
    if feedback is None:
        return {
            "status": "pending-personal-review",
            "revision": revision,
            "artifact_hash": artifact_hash,
            "input_hashes": expected_inputs,
            "verdict": "pending",
            "feedback_reference": None,
            "comment": None,
        }
    if not isinstance(feedback, dict):
        raise ContractError("owner feedback must be an object or null")
    for field in ("revision", "artifact_hash", "feedback_reference", "comment"):
        _require_string(feedback.get(field), f"feedback.{field}")
    if feedback["revision"] != revision:
        raise ContractError("owner feedback revision does not match current revision")
    if feedback["artifact_hash"] != artifact_hash:
        raise ContractError("owner feedback artifact hash does not match current artifact")
    if feedback.get("input_hashes") != expected_inputs:
        raise ContractError("owner feedback input hashes do not match current inputs")
    if feedback.get("verdict") not in VERDICTS:
        raise ContractError("owner feedback verdict is outside the acceptance vocabulary")
    result = deepcopy(feedback)
    result["status"] = "recorded"
    return result

