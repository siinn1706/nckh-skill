"""Validate matched-condition integrity without awarding behavioral quality."""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core.build import load_json
from core.paths import atomic_json, contained, digest_file, digest_record
from core.schema import ContractError


HASH_FIELDS = {"base_code", "instruction_policy", "subject", "resource_closure", "registry", "corpus", "split", "wrapper", "config", "output"}
SHARED_FIELDS = {"base_code", "instruction_policy", "subject", "registry", "corpus", "split", "wrapper"}
PAIRS = [("same-agent/resource-off", "same-agent/resource-on"),
         ("selective-delegation/resource-off", "selective-delegation/resource-on")]
CONDITIONS = {"no-skill", "selected-permitted-upstream", *(value for pair in PAIRS for value in pair)}
VARIANTS = {"no-skill": "no-skill", "selected-permitted-upstream": "relevant permitted upstream",
            **{identity: "nckh-same-agent" for identity in PAIRS[0]},
            **{identity: "nckh-selective-delegation" for identity in PAIRS[1]}}


def closed(record, fields, label):
    if not isinstance(record, dict) or set(record) != set(fields):
        raise ContractError(label + ": missing/unknown fields")


def reference_path(reference, work_context):
    closed(reference, {"path", "sha256"}, "evidence reference")
    if (not isinstance(reference["path"], str) or not reference["path"]
            or not isinstance(reference["sha256"], str)
            or not re.fullmatch(r"[a-f0-9]{64}", reference["sha256"])):
        raise ContractError("evidence reference requires a relative path and full hash")
    path = contained(work_context, reference["path"])
    if not path.is_file() or digest_file(path) != reference["sha256"]:
        raise ContractError("missing or stale evidence reference: " + reference["path"])
    return path


def compare(manifest, *, work_context=ROOT.parent):
    closed(manifest, {"schema_version", "status", "treatment", "conditions", "inputs", "migration", "round_lineage", "human_queue_reference", "holdout"}, "matched manifest")
    if manifest["schema_version"] != 1 or type(manifest["schema_version"]) is not int or manifest["treatment"] != "resource-access":
        raise ContractError("unsupported matched manifest version/treatment")
    if manifest["holdout"] != "pending/NOT_CALLABLE":
        raise ContractError("this comparison has no protected-holdout route")
    if manifest["status"] != "frozen-preparation":
        raise ContractError("this checker validates preparation, not a completed qualification")
    closed(manifest["inputs"], {"corpus_reference", "case_ids", "rights", "split"}, "frozen inputs")
    inputs = manifest["inputs"]
    if (not isinstance(inputs["case_ids"], list) or len(inputs["case_ids"]) != 148
            or not all(isinstance(value, str) for value in inputs["case_ids"])
            or len(set(inputs["case_ids"])) != 148 or inputs["split"] != "exposed-development"
            or inputs["rights"] != "historical-owned-synthetic-development-only"):
        raise ContractError("existing diagnostic inputs cannot become new gold or protected holdout")
    identities = {}
    for identity in inputs["case_ids"]:
        if not isinstance(identity, str) or not re.fullmatch(r"nckh-[a-z0-9]+(?:-[a-z0-9]+)*:(positive|negative|outcome|failure)", identity):
            raise ContractError("invalid frozen case identity")
        skill, kind = identity.split(":")
        identities.setdefault(skill, set()).add(kind)
    if len(identities) != 37 or any(kinds != {"positive", "negative", "outcome", "failure"} for kinds in identities.values()):
        raise ContractError("all 37 diagnostic identities and four case IDs must remain")
    corpus = load_json(reference_path(inputs["corpus_reference"], work_context))
    if (set(inputs["case_ids"]) != {row["id"] for row in corpus["cases"]}
            or len(corpus["cases"]) != 148
            or any(row["split"] != inputs["split"] or row["rights"] != "agent-authored-owned-synthetic"
                   for row in corpus["cases"])):
        raise ContractError("case scope/rights/split differ from the actual historical diagnostic corpus")
    reference_path(manifest["human_queue_reference"], work_context)
    if not isinstance(manifest["conditions"], list):
        raise ContractError("conditions must be an array")
    indexed = {}
    pending = []
    for row in manifest["conditions"]:
        closed(row, {"id", "variant", "resource_access", "status", "subject_revision", "hashes", "references", "model", "gates", "pending_reason"}, "condition")
        if (not isinstance(row["id"], str) or row["id"] in indexed or row["id"] not in CONDITIONS
                or row["status"] not in {"pending", "not-run", "completed-unreviewed"}):
            raise ContractError("duplicate/unsupported condition or evidence status")
        access = row["id"].split("/")[-1].removeprefix("resource-") if "/" in row["id"] else {"no-skill": "none", "selected-permitted-upstream": "upstream"}[row["id"]]
        if row["variant"] != VARIANTS[row["id"]] or row["resource_access"] != access:
            raise ContractError("existing variant/condition/treatment mapping changed")
        if row["subject_revision"] is not None and (not isinstance(row["subject_revision"], str) or not row["subject_revision"]):
            raise ContractError("subject revision must be a real revision or pending null")
        if not isinstance(row["pending_reason"], str) or not row["pending_reason"].strip():
            raise ContractError("condition requires an explicit evidence limitation")
        closed(row["hashes"], HASH_FIELDS, "condition hashes")
        closed(row["references"], HASH_FIELDS, "condition references")
        for key, value in row["hashes"].items():
            if value is not None and (not isinstance(value, str) or not re.fullmatch(r"[a-f0-9]{64}", value)):
                raise ContractError("invalid full condition hash: " + key)
            reference = row["references"][key]
            if value is None:
                if reference is not None:
                    raise ContractError("reference has no matching condition hash: " + key)
            else:
                if reference is None:
                    raise ContractError("condition hash has no matching evidence reference: " + key)
                reference_path(reference, work_context)
                if reference["sha256"] != value:
                    raise ContractError("condition hash differs from evidence reference: " + key)
        if row["hashes"]["corpus"] != inputs["corpus_reference"]["sha256"]:
            raise ContractError("condition changed the frozen corpus")
        closed(row["model"], {"requested", "resolved", "effective"}, "model observations")
        if any(value is not None and (not isinstance(value, str) or not value.strip()) for value in row["model"].values()):
            raise ContractError("model declarations/observations must be strings or pending null")
        closed(row["gates"], {"rights", "reviewers", "thresholds", "host_route", "provider_budget", "process_budget"}, "condition gates")
        for key, reference in row["gates"].items():
            if reference is not None:
                reference_path(reference, work_context)
        if row["status"] == "completed-unreviewed" and (row["subject_revision"] is None or any(value is None for value in row["hashes"].values())):
            raise ContractError("completed observation is missing subject/input/config/output hashes")
        gaps = [key for key, value in row["hashes"].items() if value is None]
        gaps += [key for key, value in row["gates"].items() if value is None]
        if not row["model"]["effective"]:
            gaps.append("effective-model-unobserved")
        if row["subject_revision"] is None:
            gaps.append("subject-revision-unselected")
        pending.append({"condition": row["id"], "missing": gaps, "status": row["status"], "reason": row["pending_reason"]})
        indexed[row["id"]] = row
    if set(indexed) != CONDITIONS:
        raise ContractError("all existing variants and both same-base pairs must remain")
    for off_id, on_id in PAIRS:
        off, on = indexed[off_id], indexed[on_id]
        if off["variant"] != on["variant"] or off["subject_revision"] != on["subject_revision"] or off["resource_access"] != "off" or on["resource_access"] != "on":
            raise ContractError("same-base pair subject/variant/treatment mismatch")
        for key in SHARED_FIELDS:
            if off["hashes"][key] != on["hashes"][key]:
                raise ContractError("same-base resource ablation confounded by " + key)
        if off["model"] != on["model"] or off["gates"] != on["gates"]:
            raise ContractError("same-base pair model/reviewer/rights/budget mismatch")
        if (off["hashes"]["resource_closure"] is not None and
                off["hashes"]["resource_closure"] == on["hashes"]["resource_closure"]):
            raise ContractError("resource-on/off closures must have their own different hashes")
        if off["hashes"]["config"] is not None and on["hashes"]["config"] is not None:
            configs = [load_json(reference_path(row["references"]["config"], work_context)) for row in (off, on)]
            for row, config in zip((off, on), configs):
                if (config.get("condition") != row["id"] or config.get("resource_access") != row["resource_access"]
                        or config.get("model") != row["model"]):
                    raise ContractError("condition config does not match declared treatment/model")
            if {k: v for k, v in configs[0].items() if k not in {"condition", "resource_access"}} != {k: v for k, v in configs[1].items() if k not in {"condition", "resource_access"}}:
                raise ContractError("same-base config differs beyond resource treatment")
    closed(manifest["migration"], {"comparison", "installed_revision", "candidate_revision", "initial_freeze_reference", "direct_linkage_reference", "causal_resource_claim"}, "migration")
    if manifest["migration"]["comparison"] != "migration-history-only" or manifest["migration"]["causal_resource_claim"] is not False:
        raise ContractError("historical migration is not a resource ablation")
    migration = manifest["migration"]
    initial = load_json(reference_path(migration["initial_freeze_reference"], work_context))
    reference_path(migration["direct_linkage_reference"], work_context)
    if (migration["installed_revision"] != initial["direct_lane"]["subject_revision"]
            or not isinstance(migration["candidate_revision"], str) or not migration["candidate_revision"].isdigit()
            or any(indexed[identity]["subject_revision"] != migration["candidate_revision"] for pair in PAIRS for identity in pair)):
        raise ContractError("migration subjects differ from frozen historical/candidate revisions")
    closed(manifest["round_lineage"], {"direct_reviews_sha256", "direct_reviews_reference", "rounds_observed", "new_round_allocated", "development_max_rounds", "holdout_runs"}, "round lineage")
    rounds = manifest["round_lineage"]
    if (type(rounds["development_max_rounds"]) is not int or rounds["development_max_rounds"] != 3
            or type(rounds["holdout_runs"]) is not int or rounds["holdout_runs"] != 1
            or rounds["new_round_allocated"] is not None):
        raise ContractError("round limits/lineage changed without operator review")
    if not re.fullmatch(r"[a-f0-9]{64}", str(rounds["direct_reviews_sha256"])) or not isinstance(rounds["rounds_observed"], dict):
        raise ContractError("round lineage requires hash-bound historical reviews")
    if set(rounds["rounds_observed"]) != set(identities) or any(type(value) is not int or not 1 <= value <= 3 for value in rounds["rounds_observed"].values()):
        raise ContractError("historical development round counts missing or reset")
    reviews = load_json(reference_path(rounds["direct_reviews_reference"], work_context))
    if rounds["direct_reviews_sha256"] != rounds["direct_reviews_reference"]["sha256"] or reviews["corpus_sha256"] != inputs["corpus_reference"]["sha256"]:
        raise ContractError("round lineage differs from actual corpus/review hashes")
    observed = {}
    for row in reviews["reviews"]:
        if type(row["round"]) is not int or not 1 <= row["round"] <= 3:
            raise ContractError("historical review has an unsupported development round")
        observed[row["skill_id"]] = max(observed.get(row["skill_id"], 0), row["round"])
    if rounds["rounds_observed"] != observed:
        raise ContractError("historical development rounds were reset or altered")
    return {"schema_version": 1, "integrity": "pass", "manifest_hash": digest_record(manifest),
            "comparison_status": "pending", "conditions": pending, "resource_benefit": "unknown",
            "evidence_class": "matched-manifest-integrity", "human_acceptance": "not-evaluated",
            "accepted_task_count": 0, "cost": "unknown", "qualification": "pending"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--work-context", type=Path, default=ROOT.parent, help="Root for hash-bound relative evidence references.")
    args = parser.parse_args()
    try:
        result = compare(load_json(args.manifest), work_context=args.work_context)
    except (ContractError, ValueError, OSError, KeyError, TypeError) as error:
        result = {"status": "fail", "error": str(error), "qualification": "pending"}
    if args.output:
        atomic_json(args.output, result)
    print(json.dumps(result, indent=2))
    return 3 if result.get("status") == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
