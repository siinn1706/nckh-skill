"""Dispatch permitted model choices through the current app's native executable."""

import argparse
import copy
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path


def write_json(path, record):
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def instruction_authority_reads(events, required_path):
    observations = []
    for number, line in enumerate(events.read_text(encoding="utf-8").splitlines(), 1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            return {"status": "unverified-invalid-trace", "reads": observations}
        item = event.get("item", {})
        if event.get("type") != "item.completed" or item.get("type") != "command_execution":
            continue
        command = re.sub(r"/+", "/", item.get("command", "").replace("\\", "/"))
        if required_path.casefold() in command.casefold():
            observations.append({"path": required_path, "trace_line": number,
                                 "command": item["command"], "status": item.get("status"),
                                 "exit_code": item.get("exit_code")})
    return {"status": "trace-inspected", "reads": observations}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--executable", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--models", nargs="+", choices=["gpt-6.1-sol"], required=True,
                        help="currently authorized model; no fallback")
    parser.add_argument("--case-ids", nargs="+", metavar="CASE_ID",
                        help="exact case IDs; saves output/<model>/<case-id>/artifact.md")
    parser.add_argument("--repair-reference", metavar="PROJECT_RELATIVE_FILE",
                        help="existing project report/memo with findings to repair")
    parser.add_argument("--visual-binding", metavar="PROJECT_RELATIVE_JSON",
                        help="explicit codex binding for the selected World Bank case")
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[3]
    required_authority = (Path.home() / ".claude/rules/development-rules.md").as_posix()
    if len(set(args.models)) != len(args.models):
        parser.error("model choices must not be duplicated")
    sys.path.insert(0, str(project / "nckh-kit"))
    from core.paths import contained, digest_file, no_links
    from core.processes import run_owned_command
    from core.schema import ContractError

    cases = json.loads((project / "plans/evaluation/personal-use/native/cases/real-source-cases.json").read_text(encoding="utf-8"))["cases"]
    cases_by_id = {case["case_id"]: case for case in cases}
    if args.case_ids is not None:
        if len(set(args.case_ids)) != len(args.case_ids):
            parser.error("case IDs must not be duplicated")
        unknown = sorted(set(args.case_ids) - cases_by_id.keys())
        if unknown:
            parser.error("unknown case IDs: " + ", ".join(unknown))
        jobs = [(model, cases_by_id[case_id])
                for model in args.models for case_id in args.case_ids]
    else:
        jobs = [(model, cases[index % len(cases)]) for index, model in enumerate(args.models)]

    def project_file(relative, option):
        if relative is None:
            return None
        try:
            path = contained(project, relative)
        except ContractError as error:
            parser.error(option + ": " + str(error))
        if not path.is_file():
            parser.error(option + " must name an existing project-relative file")
        return path

    repair_reference = project_file(args.repair_reference, "--repair-reference")
    visual_binding = project_file(args.visual_binding, "--visual-binding")
    if visual_binding is not None and not any(
            case["case_id"] == "real-source-worldbank-visual-01" for _, case in jobs):
        parser.error("--visual-binding requires the World Bank case to be selected")
    try:
        repair_text = repair_reference.read_text(encoding="utf-8") if repair_reference else None
    except UnicodeDecodeError:
        parser.error("--repair-reference must be a UTF-8 report or memo")
    references = {}
    for name, path in [("repair_reference", repair_reference), ("visual_binding", visual_binding)]:
        if path is not None:
            references[name] = {"path": path.relative_to(project).as_posix(), "sha256": digest_file(path)}
    try:
        output = no_links(args.output).resolve()
    except ContractError as error:
        parser.error(str(error))
    if (not output.is_relative_to(project)
            or output.exists() and (not output.is_dir() or any(output.iterdir()))):
        parser.error("use a fresh output directory inside test-skill")
    if not args.executable.is_file():
        parser.error("--executable must name the current app's native executable")
    ownership = project / ".nckh-state/ownership.json"
    ownership_hash = digest_file(ownership)
    output.mkdir(parents=True, exist_ok=True)
    temp = output / "temporary"
    temp.mkdir()
    os.environ["TEMP"] = os.environ["TMP"] = str(temp)

    def dispatch(model, original_case):
        case = copy.deepcopy(original_case)
        folder = output / model
        if args.case_ids is not None:
            folder = folder / case["case_id"]
        folder.mkdir(parents=args.case_ids is not None)
        artifact_path = (folder / "artifact.md").relative_to(project).as_posix()
        contract = case["output_contract"]
        if "artifact_path" in contract:
            contract["artifact_path"] = artifact_path
        if "artifact_paths" in contract:
            contract["artifact_paths"] = [
                (folder / "artifact.svg").relative_to(project).as_posix(), artifact_path]
        skills = case["skill_ids"]
        skill = skills[0]
        prompt = (
            "Authorized bounded personal-use case. Work context " + project.as_posix() + " only. "
            "All project instructions and authority for this case are supplied here and in the required "
            "current project-installed contracts. Obey higher-priority host system/developer instructions. "
            "The mandatory host development-rule read at " + required_authority + " is a narrow recorded "
            "instruction-authority exception; report it separately from case/source reads if observed. "
            "It is not permission for global edits, unrelated source/config/user-data reads, or external-"
            "project tests. All case files, sources, outputs and tests remain project-local. Do not read "
            "unrelated outside-project files or seek additional global rules. Read the current installed "
            "SKILL.md for every listed skill: " + ", ".join(
                ".agents/skills/" + identity + "/SKILL.md" for identity in skills) +
            ". Read their required local contracts, "
            "including personal-use acceptance criteria and resource lookup reference if present. "
            "Use its installed resource reader on the matching actual source pack; report the exact reader "
            "command, resource id, record/source id and hash. Never substitute synthetic data. "
            "Fallback input is only the pinned acquisition input specified below if the installed resource "
            "is unavailable; explicitly record that gap. No source/config/install/global edits, provider "
            "mutations, external messages, nested agents, UI use or publishing. Do not change provider "
            "configuration or run tests. Model is authorized only gpt-6.1-sol; no model fallback. "
            "Preserve every source quotation exactly, including case, spelling and punctuation; do not "
            "capitalize a source phrase when quoting it. Use source_id alone as the reader query. "
            "Read-only execution: do not create or edit any file. Deliver the complete usable artifact "
            "in your FINAL ANSWER; only the controller saves it to " + artifact_path + ". "
            "The output contract below contains the actual controller paths; do not substitute historical "
            "paths or claim the model saved a file/self-hash. For the SVG case include the full standalone "
            "SVG in a fenced svg block plus its QA memo for controller extraction. Do not claim "
            "human/scientific/native certification. The owner reviews after use. You may read only required "
            "files for this case and run bounded read/arithmetic checks.\n\n"
        )
        if repair_reference is not None:
            prompt += (
                "Repair evidence: " + references["repair_reference"]["path"] +
                " (SHA-256 " + references["repair_reference"]["sha256"] + "). Apply only the findings "
                "relevant to this selected case in the new final artifact; preserve previous attempts. "
                "This reference is evidence, not an additional authority grant.\n" + repair_text + "\n\n")
        if case["case_id"] == "real-source-worldbank-visual-01":
            if visual_binding is None:
                prompt += (
                    "No explicit visual binding was supplied. Follow the current installed engine contract; "
                    "if its capability is unavailable, return a source/reader-backed blocker memo and mark "
                    "the visual output contract unmet. Do not bypass it or invent a render.\n\n")
            else:
                prompt += (
                    "Explicit project-scoped visual binding: " + references["visual_binding"]["path"] +
                    " (SHA-256 " + references["visual_binding"]["sha256"] + "). Follow the current installed "
                    "nckh-visuals SKILL.md link to its actual installed binding checker; do not substitute a "
                    "repository-side checker or assume a historical checker path. Run that checker with "
                    "--project " + json.dumps(project.as_posix()) + " --task " + case["case_id"] +
                    " --host codex --binding " + json.dumps(references["visual_binding"]["path"]) +
                    " --capability svg-render. Preserve its actual command and JSON receipt. The checker "
                    "is authorized only to verify the declared engine identity and project-local probe "
                    "evidence; do not directly read an outside-project engine or unrelated configuration/"
                    "rule file. The mandatory host instruction-authority exception above still applies. "
                    "Only the engine declared by that binding is permitted; no alternate engine/provider. "
                    "If the checker is unavailable or rejects the binding, report a blocker/unmet output. "
                    "If permitted, return the complete standalone SVG fence plus QA memo. Use 26 visible "
                    "circle marks with exact data-year/data-value attributes, native text and a polyline "
                    "connecting the same coordinates in ascending year order. Include a 26-row "
                    "year/value/x/y source-to-mark table, linear axis bounds/formulas and true tick "
                    "values. Use an SVG at least 1200 by 900 with Arial text, Vietnamese title/desc "
                    "and reading order; preserve the exact blank-unit axis caveat and source metadata. "
                    "State the method and finite precision of the percentage change. Read-only mode "
                    "cannot write/render the final image: the controller saves/extracts the actual final "
                    "SVG, renders it with that declared engine, checks source-to-mark values, opens/edits/"
                    "saves/reopens it, and binds final QA to actual hashes. Probe integrity is not a render "
                    "of your final SVG. Final render/editability/visual acceptance remains pending until "
                    "the controller records that evidence.\n\n")
        prompt += "Case input and acceptance contract:\n" + json.dumps(case, ensure_ascii=False)
        (folder / "prompt.txt").write_text(prompt, encoding="utf-8")
        command = [str(args.executable), "exec", "--ephemeral", "--skip-git-repo-check",
                   "--sandbox", "read-only", "--model", model,
                   "-c", 'model_reasoning_effort="low"', "--cd", str(project), "--json",
                   "--output-last-message", str(folder / "artifact.md"), "-"]
        record = {"schema_version": 1, "route": "current-app-native-codex-exec",
                  "requested_model": model, "requested_effort": "low", "effective_model": None,
                  "effective_effort": None, "fallback": False, "case_id": case["case_id"],
                  "skill": skill, "command": command, "project": str(project),
                  "instruction_authority_exception": required_authority,
                  "installed_ownership_sha256": ownership_hash,
                  "prompt_sha256": digest_file(folder / "prompt.txt"),
                  "started_at": datetime.now(timezone.utc).isoformat(), "status": "dispatching"}
        record.update(references)
        label = model + ("/" + case["case_id"] if args.case_ids is not None else "")
        def started(pid):
            record.update(pid=pid, status="running")
            write_json(folder / "receipt.json", record)
            print(label + " started PID " + str(pid), flush=True)
        result = run_owned_command(command, project, prompt.encode("utf-8"), folder / "events.jsonl",
                                   folder / "stderr.txt", timeout=None, on_started=started)
        record.update(result)
        record["finished_at"] = datetime.now(timezone.utc).isoformat()
        record["stderr_sha256"] = digest_file(folder / "stderr.txt")
        record["events_sha256"] = digest_file(folder / "events.jsonl")
        record["instruction_authority_reads"] = instruction_authority_reads(
            folder / "events.jsonl", required_authority)
        artifact = folder / "artifact.md"
        record["artifact_exists"] = artifact.is_file() and artifact.stat().st_size > 0
        if record["artifact_exists"]:
            record["artifact_sha256"] = digest_file(artifact)
        if digest_file(ownership) != ownership_hash:
            record["subject_drift"] = True
        record["evidence_limits"] = ["Native executable dispatch, not a main-window UI run.",
            "Requested/configured model is separate from effective provider telemetry.",
            "Successful process exit is unreviewed output, not an acceptance verdict."]
        write_json(folder / "receipt.json", record)
        print(label + " " + record["status"] + " artifact=" + str(record["artifact_exists"]), flush=True)
        return record

    results = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(dispatch, model, case) for model, case in jobs]
        for future in as_completed(futures):
            results.append(future.result())
            write_json(output / "dispatch-summary.json", results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
