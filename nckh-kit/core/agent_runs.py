"""Opt-in command adapters for frozen development cases; no automatic quality verdict."""

import os
import re
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

from core.build import load_json, verify_source_lock
from core.install import SURFACE_HOST
from core.paths import atomic_json, digest_bytes, digest_file, digest_record, no_links
from core.processes import run_owned_command
from core.schema import ContractError


FREEZE_FIELDS = ("metrics", "sample_rights", "reviewers", "quality_thresholds", "provider_budget", "acceptable_economics")
BUDGET_FIELDS = {"schema_version", "kind", "scope", "mode", "unknown_cost_accepted", "max_cases",
                 "max_seconds_per_case", "funding_scope_reference"}
FIELDS = {"schema_version", "surface", "host_version", "argv", "executable_sha256", "driver_references", "transport",
          "interface_reference", "workspace", "private_store", "case_ids", "round", "timeout_seconds",
          "freeze_references", "requested_model", "requested_effort"}
FORBIDDEN_FLAGS = {"--dangerously-bypass-approvals-and-sandbox", "--dangerously-bypass-hook-trust",
                   "--dangerously-skip-permissions", "--skip-permissions", "--yolo", "--force", "--ignore-rules"}


def absolute_path(value):
    if not isinstance(value, str) or not Path(value).is_absolute():
        raise ContractError("runner paths must be explicit absolute paths")
    return no_links(value)


def reference_hash(record):
    if not isinstance(record, dict) or set(record) != {"path", "sha256"}:
        raise ContractError("freeze/interface references require an exact path and sha256")
    path = absolute_path(record["path"])
    if not path.is_file() or digest_file(path) != record["sha256"]:
        raise ContractError("freeze/interface reference is missing or changed")
    return record["sha256"]


def load_cases(root):
    cases = {}
    for path in (root / "evals/cases").glob("*/*.json"):
        record = load_json(path)
        if "skill_id" in record:
            for case in record["cases"]:
                if case["id"] in cases:
                    raise ContractError("duplicate case identity")
                cases[case["id"]] = case
    return cases


def prepare_agent_run(root, recipe):
    root = no_links(root)
    if not isinstance(recipe, dict) or set(recipe) != FIELDS or type(recipe["schema_version"]) is not int or recipe["schema_version"] != 1:
        raise ContractError("unknown or incomplete agent runner recipe")
    surface = recipe["surface"]
    if not isinstance(surface, str) or surface not in SURFACE_HOST:
        raise ContractError("unsupported runner surface; no invented native binding")
    for key in ("host_version", "requested_model", "requested_effort"):
        if not isinstance(recipe[key], str) or not recipe[key].strip():
            raise ContractError("runner needs explicit version/model/effort declarations, including unknown/inherit")
    argv = recipe["argv"]
    if not isinstance(argv, list) or not argv or any(not isinstance(v, str) or not v or "\0" in v for v in argv):
        raise ContractError("runner argv must be a nonempty literal argument array")
    if any(v.split("=", 1)[0] in FORBIDDEN_FLAGS or v == "danger-full-access" or
           re.search(r"(?:approval_policy|sandbox_mode)\s*=\s*[\"']?(?:never|danger-full-access)", v) for v in argv):
        raise ContractError("runner cannot bypass native sandbox/approval/hook rules")
    executable = absolute_path(argv[0])
    if executable.suffix.casefold() in {".cmd", ".bat"} or not executable.is_file():
        raise ContractError("NOT_CALLABLE: use a real executable; batch/shell interpolation is unsupported")
    if digest_file(executable) != recipe["executable_sha256"]:
        raise ContractError("runner executable changed after selection")
    if Path(executable).stem.casefold() in {"cmd", "powershell", "pwsh", "bash", "sh", "zsh"}:
        raise ContractError("shell command drivers are unsupported; select an explicit native executable or reviewed bridge")
    if not isinstance(recipe["transport"], str) or recipe["transport"] not in {"prompt-stdin", "json-stdin"}:
        raise ContractError("unsupported driver transport; input is never interpolated into shell text")
    interface_hash = reference_hash(recipe["interface_reference"])
    workspace, store = absolute_path(recipe["workspace"]), absolute_path(recipe["private_store"])
    if not workspace.is_dir() or not store.is_dir():
        raise ContractError("workspace and owner-approved private store must already exist")
    driver_refs = recipe["driver_references"]
    if not isinstance(driver_refs, list):
        raise ContractError("driver references must list hash-bound bridge scripts and dependencies")
    driver_hashes = {}
    for ref in driver_refs:
        value = reference_hash(ref)
        driver_hashes[str(absolute_path(ref["path"]))] = value
    for value in argv[1:]:
        path = Path(value)
        if path.suffix.casefold() in {".py", ".js", ".mjs", ".cjs", ".sh"}:
            path = no_links(path if path.is_absolute() else workspace / path)
            if str(path) not in driver_hashes:
                raise ContractError("bridge script arguments need a driver reference before preview")
    for public in (root, root.parent, workspace):
        if store.is_relative_to(public) or public.is_relative_to(store):
            raise ContractError("raw traces must be outside source, distribution and the agent workspace")
    ids = recipe["case_ids"]
    if not isinstance(ids, list) or not ids or any(not isinstance(v, str) for v in ids) or len(set(ids)) != len(ids):
        raise ContractError("select explicit unique case IDs; no implicit whole-catalog run")
    maximum = load_json(root / "evals/protocols/qualification.json")["development_max_rounds"]
    if type(recipe["round"]) is not int or not 1 <= recipe["round"] <= maximum:
        raise ContractError("new human authority required outside the development-round bound")
    if type(recipe["timeout_seconds"]) is not int or not 1 <= recipe["timeout_seconds"] <= 900:
        raise ContractError("choose an explicit per-case timeout from 1 to 900 seconds")
    cases = load_cases(root)
    selected = []
    for case_id in ids:
        case = cases.get(case_id)
        if not case or case.get("input_rights") not in {"owned", "cleared"} or not isinstance(case.get("prompt"), str):
            raise ContractError("unknown case or uncleared execution rights")
        selected.append({"case_id": case_id, "definition_hash": digest_record(case),
                         "input_hash": digest_bytes(case_input(case, recipe["transport"]))})
    freeze = recipe["freeze_references"]
    if not isinstance(freeze, dict) or set(freeze) != set(FREEZE_FIELDS):
        raise ContractError("all metrics/rights/review/threshold/budget/economics freeze references are required")
    blockers, hashes = [], {}
    for name in FREEZE_FIELDS:
        if freeze[name] is None:
            blockers.append("missing freeze reference: " + name)
        else:
            hashes[name] = reference_hash(freeze[name])
    if recipe["host_version"] == "unknown":
        blockers.append("native host version is unverified")
    lock = verify_source_lock(root)
    if freeze["provider_budget"] is not None:
        budget = load_json(absolute_path(freeze["provider_budget"]["path"]))
        if not isinstance(budget, dict) or set(budget) != BUDGET_FIELDS:
            raise ContractError("unknown provider budget fields; unsupported billing limits cannot be enforced")
        scope = budget["scope"]
        if (not isinstance(scope, dict) or set(scope) != {"source_lock_hash", "case_ids"}
                or not isinstance(scope["case_ids"], list)
                or any(not isinstance(case_id, str) for case_id in scope["case_ids"])):
            raise ContractError("provider budget needs an exact source/case scope")
        if (type(budget["schema_version"]) is not int or budget["schema_version"] != 1 or budget["kind"] != "provider-run-budget"
                or scope.get("source_lock_hash") != digest_record(lock)
                or not set(ids) <= set(scope.get("case_ids", []))):
            raise ContractError("provider budget must cover the selected source and every case")
        if budget.get("mode") != "time-and-case-bound-unknown-cost" or budget.get("unknown_cost_accepted") is not True:
            blockers.append("NOT_CALLABLE: this command adapter cannot enforce a monetary billing cap")
        if (type(budget.get("max_cases")) is not int or budget["max_cases"] < len(ids)
                or type(budget.get("max_seconds_per_case")) is not int
                or budget["max_seconds_per_case"] < recipe["timeout_seconds"]
                or not isinstance(budget.get("funding_scope_reference"), str) or not budget["funding_scope_reference"].strip()):
            raise ContractError("provider budget lacks sufficient case/time bounds or an explicit funding scope")
    return {"schema_version": 1, "status": "preview", "evidence_class": "static",
            "source_lock_hash": digest_record(lock), "recipe_hash": digest_record(recipe),
            "host": SURFACE_HOST[surface], "surface": surface, "declared_version": recipe["host_version"],
            "command": {"executable": str(executable), "argv_hash": digest_record(argv), "argument_count": len(argv) - 1},
            "executable_hash": recipe["executable_sha256"], "interface_hash": interface_hash,
            "driver_reference_hashes": driver_hashes,
            "workspace": str(workspace), "private_store": str(store), "transport": recipe["transport"],
            "cases": selected, "split": "development", "round": recipe["round"],
            "timeout_seconds": recipe["timeout_seconds"], "maximum_attempts": len(selected),
            "freeze_reference_hashes": hashes, "blockers": blockers,
            "model": {"requested": recipe["requested_model"], "resolved": "unverified", "effective": "unknown"},
            "effort": {"requested": recipe["requested_effort"], "resolved": "unverified", "effective": "unknown"},
            "cost": "unknown", "accepted_task_count": 0, "qualification": "pending",
            "native_binding": "operator-selected; encoding/discovery/effectiveness remain unverified"}


def case_input(case, transport):
    if transport == "prompt-stdin":
        return case["prompt"].encode("utf-8")
    payload = {"case_id": case["id"], "skill_id": case["skill_id"], "prompt": case["prompt"],
               "forbidden_actions": case["forbidden_actions"], "input_provenance": case["input_provenance"],
               "input_rights": case["input_rights"], "split": "development"}
    import json
    return json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")


def run_agent_cases(root, recipe, *, approved_plan_hash=None, allow_provider=False):
    plan = prepare_agent_run(root, recipe)
    if not allow_provider or approved_plan_hash != digest_record(plan):
        raise ContractError("provider execution requires live operator opt-in and the exact reviewed plan hash; recipe fields do not grant authority")
    if plan["blockers"]:
        raise ContractError("agent run blocked: " + "; ".join(plan["blockers"]))
    store = absolute_path(recipe["private_store"])
    area = store / ("nckh-agent-run-" + uuid.uuid4().hex)
    area.mkdir(mode=0o777 if os.name == "nt" else 0o700)
    receipt = {"schema_version": 1, "kind": "agent-command-observation", "evidence_class": "unclassified-command-observation",
               "declared_purpose": "agent-behavior; independent native/agent verification is still required",
               "status": "running", "plan_hash": digest_record(plan), "source_lock_hash": plan["source_lock_hash"],
               "host": plan["host"], "surface": plan["surface"], "version": plan["declared_version"],
               "split": "development", "round": plan["round"], "attempts": [],
               "model": plan["model"], "effort": plan["effort"], "cost": "unknown",
               "accepted_task_count": 0, "cost_per_accepted_task": "undefined", "qualification": "pending",
               "native_identity": "declared; not independently verified", "private_record": str(area / "run.json"),
               "command": plan["command"], "private_command_record": str(area / "command.json"),
               "recorded_at": datetime.now(timezone.utc).isoformat()}
    atomic_json(area / "command.json", {"argv": recipe["argv"], "workspace": plan["workspace"]})
    atomic_json(area / "plan.json", plan)
    atomic_json(area / "run.json", receipt)
    try:
        cases = load_cases(root)
        for number, selected in enumerate(plan["cases"]):
            if prepare_agent_run(root, recipe) != plan:
                raise ContractError("source/driver/freeze/input changed; review a fresh preview before dispatch")
            case = cases[selected["case_id"]]
            input_bytes = case_input(case, recipe["transport"])
            if digest_record(case) != selected["definition_hash"] or digest_bytes(input_bytes) != selected["input_hash"]:
                raise ContractError("cached case input differs from the reviewed preview; no dispatch")
            output, errors = area / f"{number}-stdout.bin", area / f"{number}-stderr.bin"
            attempt = {"case_id": selected["case_id"], "input_hash": selected["input_hash"],
                       "status": "starting", "pid": None, "command_hash": plan["command"]["argv_hash"], "workspace": plan["workspace"],
                       "stdout_reference": str(output), "stderr_reference": str(errors),
                       "outcome_acceptance": "pending-independent-review"}
            receipt["attempts"].append(attempt)
            atomic_json(area / "run.json", receipt)

            def started(pid):
                attempt.update(status="running", pid=pid)
                atomic_json(area / "run.json", receipt)

            result = run_owned_command(recipe["argv"], plan["workspace"], input_bytes,
                                       output, errors, timeout=plan["timeout_seconds"], on_started=started)
            attempt.update(**result, stdout_hash=digest_file(output), stderr_hash=digest_file(errors))
            atomic_json(area / "run.json", receipt)
            if result["status"] != "completed-unreviewed":
                receipt["status"] = result["status"]
                break
        else:
            receipt["status"] = "completed-unreviewed"
        if prepare_agent_run(root, recipe) != plan:
            raise ContractError("source/driver/freeze/input changed during execution; observation is stale")
    except subprocess.TimeoutExpired:
        receipt.update(status="timeout-unknown", error="owned-process lifecycle wait timed out; cleanup and exit status remain unverified")
    except subprocess.SubprocessError as error:
        receipt.update(status="fail", error="owned-process lifecycle failed; inspect the private command and process journal",
                       error_kind=type(error).__name__)
    except (ContractError, OSError, ValueError, KeyError, TypeError) as error:
        receipt.update(status="fail", error=str(error))
    except (KeyboardInterrupt, SystemExit):
        receipt.update(status="interrupted-unknown", error="controller interrupted; reconcile the retained private run record before another attempt")
    for attempt in receipt["attempts"]:
        if attempt["status"] in {"starting", "running"}:
            attempt.update(status=receipt["status"], exit_status=None,
                           process_cleanup="unverified; inspect the private process journal")
    atomic_json(area / "run.json", receipt)
    return receipt
