"""Freeze preparation from actual source/artifact/history files; never run agents."""

import argparse
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[3]
ROOT = PROJECT / "nckh-kit"
EVIDENCE = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from core.build import load_json, verify_bundle, verify_source_lock
from core.paths import atomic_json, digest_file, digest_record


def reference(path):
    return {"path": path.relative_to(PROJECT).as_posix(), "sha256": digest_file(path)}


def record(relative, value):
    path = EVIDENCE / relative
    atomic_json(path, value)
    return reference(path)


def prepare(artifacts):
    lock = verify_source_lock(ROOT)
    source_hash = digest_record(lock)
    subject = record("matched/subject.json", {"revision": lock["revision"], "source_lock_hash": source_hash,
                                               "source_lock_reference": reference(ROOT / "core/registry/source-lock/source-lock.json"),
                                               "kits": ["core", "engineer", "marketing"], "native_route": None})
    base = record("matched/base-code.json", {"source_lock_hash": source_hash,
                                             "files": {path: pin for path, pin in lock["files"].items()
                                                       if path.endswith(".py") and not path.startswith("tests/")}})
    instructions = record("matched/instruction-policy.json", {"source_lock_hash": source_hash,
                                                               "files": {path: pin for path, pin in lock["files"].items()
                                                                         if path.endswith(".md") and pin["rights"] == "owned-local-package"}})
    corpus_path = PROJECT / "plans/evaluation/direct-skill-tests/development-corpus.json"
    corpus = reference(corpus_path)
    cases = [row["id"] for row in load_json(corpus_path)["cases"]]
    split = record("matched/split.json", {"split": "exposed-development", "corpus_reference": corpus,
                                          "case_ids": cases, "protected_holdout": "pending/NOT_CALLABLE"})
    registry = reference(ROOT / "core/registry/catalog/resources.json")
    closures = {}
    for access in ["off", "on"]:
        bundles = {}
        for host in ["claude", "codex", "cursor", "agy"]:
            bundle = artifacts / access / host
            manifest = verify_bundle(bundle)
            if manifest["source_lock_hash"] != source_hash or manifest["resource_access"] != access:
                raise ValueError("artifact does not match candidate pin/resource treatment")
            bundles[host] = {"manifest_reference": reference(bundle / "manifest.json"),
                             "manifest_hash": digest_record(manifest), "closure_hash": manifest["closure_hash"]}
        closures[access] = record("matched/closure-" + access + ".json", {"source_lock_hash": source_hash,
                                                                          "resource_access": access, "artifacts": bundles})
    rubric_catalog = load_json(ROOT / "evals/rubrics/catalog.json")
    queue = record("human-review-queue.json", {"schema_version": 1, "status": "pending", "accepted_task_count": 0,
                                               "corpus_reference": None, "sample_rights_reference": None,
                                               "host_os_model_reference": None, "provider_process_budget_reference": None,
                                               "acceptable_economics_reference": None, "holdout": "pending/NOT_CALLABLE",
                                               "rubric_catalog_reference": reference(ROOT / "evals/rubrics/catalog.json"),
                                               "reviews": [{"rubric_id": row["id"],
                                                            "rubric_reference": reference(ROOT / "evals/rubrics" / row["path"]),
                                                            "required_role": row["reviewer"], "reviewer_reference": None,
                                                            "threshold_reference": None, "artifact_reference": None,
                                                            "receipt_reference": None, "status": "pending"}
                                                           for row in rubric_catalog["rubrics"]]})
    conditions = []
    variants = {"no-skill": ("no-skill", "none"), "selected-permitted-upstream": ("relevant permitted upstream", "upstream"),
                "same-agent": ("nckh-same-agent", None), "selective-delegation": ("nckh-selective-delegation", None)}
    fields = ["base_code", "instruction_policy", "subject", "resource_closure", "registry", "corpus", "split", "wrapper", "config", "output"]
    for mode, (variant, treatment) in variants.items():
        wrapper = record("matched/wrapper-" + mode + ".json", {"schema_version": 1, "variant": variant,
                                                              "status": "specification-only", "driver_binding": None,
                                                              "input_policy": "original frozen task and permitted materials; no oracle labels",
                                                              "resource_policy": "use declared access only; no retrieval through an undeclared route",
                                                              "delegation_policy": "selective owned delegation with frozen scope and budget" if mode == "selective-delegation" else "no child delegation",
                                                              "model": {"requested": None, "resolved": None, "effective": None},
                                                              "budget_policy": None, "effective_model_evidence": None})
        for access in ([treatment] if treatment else ["off", "on"]):
            identity = mode if treatment else mode + "/resource-" + access
            references = dict.fromkeys(fields)
            references.update(corpus=corpus, split=split, wrapper=wrapper)
            if not treatment:
                references.update(base_code=base, instruction_policy=instructions, subject=subject,
                                  resource_closure=closures[access], registry=registry)
            config = {"schema_version": 1, "condition": identity, "variant": variant, "resource_access": access,
                      "source_lock_hash": source_hash if not treatment else None,
                      "corpus_sha256": corpus["sha256"], "split_sha256": split["sha256"], "wrapper_sha256": wrapper["sha256"],
                      "model": {"requested": None, "resolved": None, "effective": None},
                      "seed": None, "host_route": None, "provider_budget": None, "process_budget": None}
            references["config"] = record("matched/config-" + identity.replace("/", "-") + ".json", config)
            conditions.append({"id": identity, "variant": variant, "resource_access": access, "status": "pending",
                               "subject_revision": lock["revision"] if not treatment else None,
                               "references": references, "hashes": {key: value["sha256"] if value else None for key, value in references.items()},
                               "model": config["model"], "gates": dict.fromkeys(["rights", "reviewers", "thresholds", "host_route", "provider_budget", "process_budget"]),
                               "pending_reason": "Actual corpus/reviewers/thresholds/host/model/budget are unselected; no run or observed model/output."
                                                 + (" Actual baseline subject and permitted native route are also pending." if treatment else "")})
    reviews_path = PROJECT / "plans/evaluation/direct-skill-tests/controller-reviews.json"
    reviews_reference = reference(reviews_path)
    rounds = {}
    for row in load_json(reviews_path)["reviews"]:
        rounds[row["skill_id"]] = max(rounds.get(row["skill_id"], 0), row["round"])
    manifest = {"schema_version": 1, "status": "frozen-preparation", "treatment": "resource-access", "conditions": conditions,
                "inputs": {"corpus_reference": corpus, "case_ids": cases,
                           "rights": "historical-owned-synthetic-development-only", "split": "exposed-development"},
                "migration": {"comparison": "migration-history-only", "installed_revision": "14", "candidate_revision": lock["revision"],
                              "initial_freeze_reference": reference(EVIDENCE / "initial-freeze.json"),
                              "direct_linkage_reference": reference(EVIDENCE / "direct-linkage.json"), "causal_resource_claim": False},
                "round_lineage": {"direct_reviews_sha256": reviews_reference["sha256"], "direct_reviews_reference": reviews_reference,
                                  "rounds_observed": rounds, "new_round_allocated": None, "development_max_rounds": 3, "holdout_runs": 1},
                "human_queue_reference": queue, "holdout": "pending/NOT_CALLABLE"}
    record("matched-manifest.json", manifest)
    return {"status": "frozen-preparation", "candidate_revision": lock["revision"], "conditions": len(conditions),
            "artifacts": artifacts.relative_to(PROJECT).as_posix(), "new_round_allocated": None, "qualification": "pending"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, required=True, help="Existing candidate containing on/off and four verified hosts.")
    args = parser.parse_args()
    import json
    print(json.dumps(prepare(args.artifacts.resolve()), indent=2))
