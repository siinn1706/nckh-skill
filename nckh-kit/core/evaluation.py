"""Case validation and honest evidence aggregation; no autonomous paid runs."""

import json
from pathlib import Path

from core.build import load_json, validate_catalog, verify_source_lock
from core.paths import contained
from core.schema import ContractError, validate_record


BASELINES = {"no-skill", "relevant permitted upstream", "nckh-same-agent", "nckh-selective-delegation"}
WRITERS = ("nckh-humanwrite", "nckh-paperwrite")
WRITER_SURFACES = ("claude-code", "codex-cli", "codex-desktop", "codex-ide",
                   "cursor-cli", "cursor-ide", "agy-cli", "agy-ide")
WRITER_ROUTES = ("ui-slash", "native-menu", "headless-prompt", "implicit")
WRITER_SCENARIOS = ("output-en", "output-vi", "conflicting-flags", "no-flag-explicit-target",
                    "no-flag-brief", "no-flag-draft", "no-flag-ambiguous",
                    "cross-language-fidelity", "english-resource-vi-output", "bilingual-compatibility")
RESEARCH_ROUTES = {
    "scientific-dataset": ("nckh-dataset", "nckh-dataset"),
    "database-migration": ("nckh-dataset", "nckh-data"),
    "scientific-split-from-db": ("nckh-data", "nckh-dataset"),
    "scientific-estimand": ("nckh-statistics", "nckh-statistics"),
    "funnel-kpi": ("nckh-statistics", "nckh-analytics"),
    "marketing-ab-test": ("nckh-statistics", "nckh-experiment"),
    "signal-normalization": ("nckh-telemetry", "nckh-telemetry"),
    "incident-cause-ranking": ("nckh-telemetry", "nckh-aiops"),
    "failing-code-test": ("nckh-telemetry", "nckh-debug"),
    "scientific-protocol": ("nckh-method", "nckh-method"),
    "authorized-local-attempt": ("nckh-cook", "nckh-cook"),
    "research-environment": ("nckh-devops", "nckh-devops"),
}


def validate_research_matrix(record, identities):
    """Check declared ownership scenarios, without a semantic routing engine."""
    validate_record("research-domain-scenarios", record)
    rows = record["scenarios"]
    if len(rows) != len(RESEARCH_ROUTES) or {row["id"] for row in rows} != set(RESEARCH_ROUTES):
        raise ContractError("research matrix requires exact supplemental scenario membership")
    for row in rows:
        requested, owner = RESEARCH_ROUTES[row["id"]]
        if row["requested_owner"] != requested or row["expected_owner"] != owner or not {requested, owner} <= identities.keys():
            raise ContractError("research matrix ownership differs from approved route")
        route = "execute-own-scope" if requested == owner else "reject-and-handoff-no-execution"
        if row["expected_route"] != route or not row["no_side_effect_oracle"] or not row["oracle"]:
            raise ContractError("research scenario requires its ownership and no-side-effect oracle")
        if row["status"] != "not-run" or row["receipt_reference"] is not None:
            raise ContractError("supplemental expected routes cannot claim observed agent behavior")
    return {"scenarios": len(rows), "evidence_class": "static", "observed_behavior": "unverified"}


def validate_writer_matrix(record):
    """Validate planned cells, never promote unobserved behavior into a receipt."""
    validate_record("writer-invocation-matrix", record)
    expected_native = {f"{surface}/{writer}/{entry}/{route}/{locale}"
                       for surface in WRITER_SURFACES for writer in WRITERS
                       for entry in (writer, "nckh-write") for route in WRITER_ROUTES for locale in ("en", "vi")}
    expected_scenarios = {f"{writer}/{scenario}" for writer in WRITERS for scenario in WRITER_SCENARIOS}
    for group, expected in (("native_cases", expected_native), ("scenario_cases", expected_scenarios)):
        rows = record[group]
        if len(rows) != len(expected) or {row["id"] for row in rows} != expected:
            raise ContractError(f"writer matrix {group} requires exact membership without duplicates")
        for row in rows:
            if row["expected_owner"] != row["writer"]:
                raise ContractError("writer action has the wrong owner")
            if (row["writer"] == "nckh-humanwrite" and row["action"] not in {"polish", "translate"}
                    or row["writer"] == "nckh-paperwrite" and row["action"] not in {"outline", "section", "argument", "reporting", "revision-response"}):
                raise ContractError("writer action/owner mismatch")
            if not FACT_FIELDS <= set(row["protected_fields"]) or not row["no_side_effect_oracle"]:
                raise ContractError("writer protected fields/no-side-effect oracle missing")
            if row["entrypoint"] not in {row["writer"], "nckh-write"}:
                raise ContractError("writer entrypoint mismatch")
            if group == "native_cases":
                if row["id"] != f"{row['surface']}/{row['writer']}/{row['entrypoint']}/{row['invocation']}/{row['output_locale']}":
                    raise ContractError("writer matrix ID does not bind its route")
                if row["surface"].split("-", 1)[0] != row["host"]:
                    raise ContractError("writer surface/host mismatch")
            else:
                if row["id"] != f"{row['writer']}/{row['scenario']}":
                    raise ContractError("writer scenario ID mismatch")
                scenario = row["scenario"]
                if scenario == "conflicting-flags" and (set(row["args"]) != {"--en", "--vi"} or row["expected_route"] != "conflict-no-write"):
                    raise ContractError("conflicting writer flags must stop before editing")
                if scenario == "no-flag-ambiguous" and (row["args"] or row["expected_route"] != "ask-one-question-no-write"):
                    raise ContractError("ambiguous locale must not edit")
                if scenario == "english-resource-vi-output" and (row["resource_locale"] != "en" or row["output_locale"] != "vi"):
                    raise ContractError("resource locale must remain independent of output locale")
            if row["status"] in {"not-run", "not-callable"}:
                if row["receipt_reference"] is not None or row["receipt_sha256"] is not None:
                    raise ContractError("unobserved writer cell has a false receipt")
                if row["status"] == "not-callable" and not row["reason"]:
                    raise ContractError("unsupported route requires a reason")
            else:
                raise ContractError("native/behavioral writer results require a separately verified run receipt; this matrix is planned")
    return {"native_cells": len(record["native_cases"]), "scenario_cells": len(record["scenario_cases"]),
            "evidence_class": "static", "observed_behavior": "unverified"}


FACT_FIELDS = {"numbers", "units", "denominators", "negation", "modality", "certainty",
               "population", "time", "causality", "terminology", "citations", "limitations", "protected-regions"}


def validate_case_manifest(record, identities):
    validate_record("skill-cases", record)
    if record["skill_id"] not in identities or len(record["cases"]) != 4:
        raise ContractError("case manifest requires one approved identity and four cases")
    cases = {}
    for case in record["cases"]:
        if (case["skill_id"] != record["skill_id"] or case["id"] != case["skill_id"] + ":" + case["type"]
                or case["id"] in cases):
            raise ContractError("duplicate or mismatched case identity/type")
        receipt = case["receipt_reference"]
        if receipt is not None and (not isinstance(receipt, str) or not receipt.strip()):
            raise ContractError("case receipt must be a nonempty reference or null")
        if case["status"] != "not-run" and not receipt:
            raise ContractError("case result has no actual receipt")
        if case["type"] == "negative":
            if case["expected_route"] != "reject-this-skill" or "route" not in case["oracle"]:
                raise ContractError("negative oracle must require rejection, ownership handoff and no task execution")
            acceptance = " ".join(case["oracle"]["acceptance"]).casefold()
            if not all(text in acceptance for text in ("reject", "owner", "handoff", "do not execute")):
                raise ContractError("negative acceptance does not cover the declared rejection route")
        elif case["expected_route"] != case["skill_id"] or "route" in case["oracle"]:
            raise ContractError("non-negative case requires its skill route")
        cases[case["id"]] = case
    return cases


def validate_required_families(record, identities, cases):
    validate_record("required-families", record)
    families = record["families"]
    if len(families) != 19 or len({f["id"] for f in families}) != 19:
        raise ContractError("all 19 unique required case families must remain")
    for family in families:
        if len(set(family["skills"])) != len(family["skills"]):
            raise ContractError("duplicate family skill mapping")
        for identity in family["skills"]:
            if identity not in identities or not set(identities[identity]["eval_ids"]) <= cases.keys():
                raise ContractError("required family maps to unknown skill/cases")
        receipt = family["receipt_reference"]
        if receipt is not None and (not isinstance(receipt, str) or not receipt.strip()):
            raise ContractError("family receipt must be a nonempty reference or null")
        if family["status"] != "not-run" and not receipt:
            raise ContractError("family result requires an actual receipt")
    return families


def validate_protocol(protocol):
    validate_record("qualification-protocol", protocol)
    if len(protocol["baselines"]) != 4 or set(protocol["baselines"]) != BASELINES:
        raise ContractError("all four approved baseline variants must remain")
    if set(protocol["split"]["by"]) != {"document", "author", "topic", "claim-family"}:
        raise ContractError("qualification partition axes changed")
    required = {"provider/human run before its freeze and grant", "inventing human labels",
                "tuning on protected holdout", "weakening cases to pass"}
    if not required <= set(protocol["forbidden"]):
        raise ContractError("qualification safety/holdout invariants missing")
    return protocol


def validate_cases(root):
    root = Path(root)
    identities = validate_catalog(load_json(root / "core/registry/catalog/skills.json"))
    cases = {}
    research_path = root / "evals/cases/research-data-aiops/domain-scenarios.json"
    research = validate_research_matrix(load_json(research_path), identities)
    for path in (root / "evals/cases").glob("*/*.json"):
        record = load_json(path)
        if path == research_path:
            continue
        if record.get("kind") == "research-domain-scenarios":
            raise ContractError("research supplemental matrix has a duplicate or misplaced loader route")
        if "skill_id" not in record:
            continue
        validated = validate_case_manifest(record, identities)
        if cases.keys() & validated.keys():
            raise ContractError("duplicate case identity across manifests")
        cases.update(validated)
    if set(cases) != {identity + ":" + kind for identity in identities for kind in ("positive", "negative", "outcome", "failure")}:
        raise ContractError("exactly 172 approved base case IDs required")
    for skill in identities.values():
        if set(skill["eval_ids"]) != {skill["id"] + ":" + t for t in ["positive", "negative", "outcome", "failure"]}:
            raise ContractError("skill requires positive/negative/outcome/failure IDs")
        if not set(skill["eval_ids"]) <= cases.keys():
            raise ContractError("missing required skill case")
        if skill["status"] == "stable":
            raise ContractError("this candidate has no complete scoped stable qualification")
    families = validate_required_families(load_json(root / "evals/cases/required-families.json"), identities, cases)
    protocol = validate_protocol(load_json(root / "evals/protocols/qualification.json"))
    rubrics = load_json(root / "evals/rubrics/catalog.json")
    if len(rubrics["rubrics"]) != 5 or {row["id"] for row in rubrics["rubrics"]} != {"outcome", "vi-taste", "en-fidelity", "domain", "scientific-visuals"}:
        raise ContractError("all five scoped qualification rubrics are required")
    for rubric in rubrics["rubrics"]:
        if not contained(root / "evals/rubrics", rubric["path"]).is_file() or not rubric["reviewer"]:
            raise ContractError("rubric requires real criteria and a reviewer role")
    if rubrics["reviewer_approval"] != "pending" or rubrics["thresholds"] is not None:
        raise ContractError("this candidate has no observed human rubric approval")
    runtime = load_json(root / "evals/cases/runtime/invocation-matrix.json")["cases"]
    writers = validate_writer_matrix(load_json(root / "evals/cases/runtime/writer-invocation-matrix.json"))
    installer = load_json(root / "evals/cases/installer/acceptance.json")
    if {row["os"] for row in installer["os_tracks"]} != {"Windows", "macOS", "Linux"}:
        raise ContractError("all three installer OS tracks must remain visible")
    if not installer["cases"] or len({row["id"] for row in installer["cases"]}) != len(installer["cases"]):
        raise ContractError("installer acceptance requires unique scenarios")
    for case in installer["cases"]:
        if not case.get("scenario") or not case.get("oracle") or case["status"] != "not-run":
            raise ContractError("installer native/OS acceptance has no execution receipt in this candidate")
    if len(runtime) != 224 or len({c["id"] for c in runtime}) != 224:
        raise ContractError("all eight surface/entrypoint/mode/invocation tracks must remain")
    lock = verify_source_lock(root)
    return {"schema_version": 1, "structural_validation": "pass", "evidence_class": "static",
            "identities": len(identities), "skill_cases": len(cases), "required_families": len(families),
            "native_invocation_cells": len(runtime), "source_files_pinned": len(lock["files"]),
            "writer_native_cells": writers["native_cells"], "writer_scenario_cells": writers["scenario_cells"],
            "writer_observed_behavior": writers["observed_behavior"],
            "research_domain_scenarios": research["scenarios"], "research_observed_behavior": research["observed_behavior"],
            "rubrics": len(rubrics["rubrics"]), "rubric_approval": rubrics["reviewer_approval"],
            "installer_acceptance_cases": len(installer["cases"]), "installer_os_qualification": "unverified",
            "agent_cases_not_run": sum(c["status"] == "not-run" for c in cases.values()),
            "native_cells_not_run": sum(c["status"] == "not-run" for c in runtime),
            "qualification": "pending", "human_freeze": protocol["freeze"],
            "cost": "unknown", "accepted_task_count": 0, "cost_per_accepted_task": "undefined"}


def development_round(protocol, *, changes, exposed_holdout=False):
    validate_protocol(protocol)
    if type(changes) is not int or changes < 1 or type(exposed_holdout) is not bool:
        raise ContractError("development round must be an integer starting at one with explicit exposure")
    if changes > protocol["development_max_rounds"]:
        raise ContractError("new human authorization required after three development rounds")
    if not exposed_holdout:
        raise ContractError("protected holdout pending/NOT_CALLABLE: private route, freeze, rights and human grant required")
    return {"split": "development",
            "blindness": "unverified", "human_gold": "unverified"}
