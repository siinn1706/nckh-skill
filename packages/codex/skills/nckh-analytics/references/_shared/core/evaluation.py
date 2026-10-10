"""Case validation and honest evidence aggregation; no autonomous paid runs."""

import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path
from urllib.parse import unquote

from core.build import load_json, validate_catalog, verify_source_lock
from core.ledger import EOL_PROFILES, inventory
from core.paths import contained, digest_file
from core.plan_check import FENCE, INLINE_CODE, LINK, SCHEME, check_plan
from core.route_hint import explicit_invocation, validate_routing_prompts
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


VI_LETTERS = frozenset(unicodedata.normalize("NFC", base + mark)
                       for base in "aăâeêioôơuưyAĂÂEÊIOÔƠUƯY"
                       for mark in ("", "̀", "́", "̃", "̉", "̣")) - set("aeiouyAEIOUY") | set("đĐ")


def has_vietnamese_diacritics(text):
    return any(char in VI_LETTERS for char in unicodedata.normalize("NFC", text))


def _check_language(case):
    if has_vietnamese_diacritics(case["prompt"]) and case["input_language"] not in {"vi", "bilingual"}:
        raise ContractError(f"{case['id']}: Vietnamese prompt requires input_language vi or bilingual")


def validate_case_manifest(record, identities):
    validate_record("skill-cases", record)
    if record["skill_id"] not in identities or len(record["cases"]) != 4:
        raise ContractError("case manifest requires one approved identity and four cases")
    cases = {}
    for case in record["cases"]:
        if (case["skill_id"] != record["skill_id"] or case["id"] != case["skill_id"] + ":" + case["type"]
                or case["id"] in cases):
            raise ContractError("duplicate or mismatched case identity/type")
        _check_language(case)
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
    if cases[record["skill_id"] + ":outcome"]["prompt"] == cases[record["skill_id"] + ":positive"]["prompt"]:
        raise ContractError(f"{record['skill_id']}: outcome prompt duplicates the positive prompt")
    return cases


# Regression suite: many scenario cases per type, each with mechanical oracle checks.
# A fixture path is "<fixture-set>/<workspace-relative path>" below the fixtures root;
# the operator copies it to the workspace path (the part after the set name).
CHECK_KINDS = ("file-exists", "file-absent", "sha256-unchanged", "sha256-equals", "eol-unchanged",
               "glob-count-min", "exit-status", "text-present", "text-absent", "links-resolve", "plan-check")
RESPONSE = "@response"
SHA256 = re.compile(r"[0-9a-f]{64}")
EXIT_TIMEOUT = 120
GIT_NAMES = frozenset({"git", "git.exe"})
# Only these variables pass from the operator's environment into an exit-status check.
INHERITED_ENV = ("PATH", "SYSTEMROOT", "TEMP", "TMP")
LAB02_FAMILIES = ("plan-deliverable-mix", "exit-masking", "input-preservation",
                  "claim-attempt-binding", "windows-unicode-shell")
# How a runner sends a case prompt: as written, or prefixed with the skill invocation.
DISPATCH_MODES = ("natural", "invoke-skill")
DEFAULT_INVOCATION = "/{skill}"
_HOOK_HOST = r"[a-z][a-z0-9-]{0,31}"
_HOOK_EVENTS = r"\.nckh-state/hooks/events/" + _HOOK_HOST
_HOOK_SNAPSHOTS = r"\.nckh-state/hooks/snapshots/" + _HOOK_HOST + r"/[a-f0-9]{16}"
HOOK_RUNTIME_STATE = (
    _HOOK_EVENTS + r"/(?:no-context-)?[a-f0-9]{64}\.(?:json|lock)",
    _HOOK_EVENTS + r"/cap-reached-no-context\.json",
    _HOOK_SNAPSHOTS + r"/[a-f0-9]{32}\.json",
    r"(?:" + _HOOK_EVENTS + "|" + _HOOK_SNAPSHOTS + r")/\.nckh-[a-z0-9_]{8}",
)
"""Full-path regexes for the files the kit's own advisory hooks write, not the agent under test.

A project install with hooks records event receipts (and their locks and cap marker),
pre-edit snapshots and the atomic-write temporaries of both while an attempt runs. Only
`file-absent` ignores new files of exactly these shapes; any other file in the hook
namespaces, every other check and every other `.nckh-state` path is scored as usual.
"""


def fixture_destination(path):
    """Workspace-relative destination of a fixture path (drop the fixture-set segment)."""
    return path.split("/", 1)[1]


def _relative_glob(value, label):
    if (not isinstance(value, str) or not value or value.startswith("/") or "\\" in value or ":" in value
            or any(part in {"..", "."} for part in value.split("/"))):
        raise ContractError(f"{label}: target must be a workspace-relative POSIX glob without traversal")


def _regex(value, label):
    if not isinstance(value, str) or not value:
        raise ContractError(f"{label}: expected must be a nonempty regular expression")
    try:
        re.compile(value)
    except re.error as error:
        raise ContractError(f"{label}: invalid regular expression: {error}") from error


def validate_check(check, label):
    """Per-kind target/expected rules that the JSON Schema subset cannot express."""
    kind, target, expected = check["kind"], check["target"], check["expected"]
    if kind not in CHECK_KINDS:
        raise ContractError(f"{label}: unknown check kind {kind!r}")
    if kind == "exit-status":
        if (not isinstance(target, list) or not target or not all(isinstance(arg, str) and arg for arg in target)
                or type(expected) is not int):
            raise ContractError(f"{label}: exit-status needs an argv list and an integer exit")
        return
    if kind in {"text-present", "text-absent"}:
        if target != RESPONSE:
            _relative_glob(target, label)
        _regex(expected, label)
        return
    _relative_glob(target, label)
    if kind == "sha256-equals":
        if not isinstance(expected, str) or not SHA256.fullmatch(expected):
            raise ContractError(f"{label}: sha256-equals needs a lowercase hex digest")
    elif kind == "glob-count-min":
        if type(expected) is not int or expected < 1:
            raise ContractError(f"{label}: glob-count-min needs a positive integer")
    elif kind == "plan-check":
        if expected not in {"VERIFIED", "FAILED"}:
            raise ContractError(f"{label}: plan-check expects VERIFIED or FAILED")
    elif kind == "file-absent":
        if not isinstance(expected, list):
            raise ContractError(f"{label}: file-absent expected is the list of allowed new-file globs")
        for allowed in expected:
            _relative_glob(allowed, label)
    elif expected is not None:
        raise ContractError(f"{label}: {kind} takes no expected value")


def _verify_fixtures(case, fixtures_root):
    destinations = set()
    for fixture in case["fixtures"]:
        path = fixture["path"]
        if "/" not in path:
            raise ContractError(f"{case['id']}: fixture path needs a fixture-set prefix: {path}")
        source = contained(fixtures_root, path)
        if not source.is_file() or digest_file(source) != fixture["sha256"]:
            raise ContractError(f"{case['id']}: fixture missing or hash mismatch: {path}")
        destination = fixture_destination(path)
        if destination in destinations:
            raise ContractError(f"{case['id']}: two fixtures share workspace path {destination}")
        destinations.add(destination)
    return destinations


def dispatch_prompt(case, invocation=DEFAULT_INVOCATION):
    """The exact prompt a runner sends for a regression case; the single source for runners.

    `invoke-skill` prefixes the host invocation of the case's skill (for example `/nckh-x`
    or `$nckh-x`), because the oracle assumes that skill was called. `natural` sends the
    prompt unchanged so the host's own routing is part of the attempt.
    """
    if not isinstance(invocation, str) or "{skill}" not in invocation:
        raise ContractError("invocation template must contain {skill}")
    mode = case.get("dispatch", "natural")
    if mode not in DISPATCH_MODES:
        raise ContractError(f"{case['id']}: unknown dispatch mode {mode!r}")
    if mode == "natural":
        return case["prompt"]
    return invocation.replace("{skill}", case["skill_id"]) + " " + case["prompt"]


def _check_dispatch(case):
    mode = case.get("dispatch", "natural")
    if case["type"] == "negative" and mode != "invoke-skill":
        raise ContractError(f"{case['id']}: negative near-miss case requires dispatch invoke-skill, "
                            "because its oracle assumes the tested skill was invoked")
    if mode == "invoke-skill" and explicit_invocation(case["prompt"]):
        raise ContractError(f"{case['id']}: dispatch invoke-skill prompt already names a skill invocation")


def _check_negative(case, destinations):
    oracle = case["oracle"]
    if case["expected_route"] != "reject-this-skill" or "route" not in oracle:
        raise ContractError(f"{case['id']}: negative oracle must require rejection, ownership handoff and no task execution")
    acceptance = " ".join(oracle["acceptance"]).casefold()
    if not all(text in acceptance for text in ("reject", "owner", "handoff", "do not execute")):
        raise ContractError(f"{case['id']}: negative acceptance does not cover the declared rejection route")
    unchanged = [glob_regex(c["target"]) for c in oracle["checks"] if c["kind"] == "sha256-unchanged"]
    if (not destinations or not any(c["kind"] == "file-absent" for c in oracle["checks"])
            or not all(any(regex.fullmatch(_nfc(path)) for regex in unchanged) for path in destinations)):
        raise ContractError(f"{case['id']}: negative case needs fixtures, sha256-unchanged for each fixture and file-absent")


def validate_regression_manifest(record, identities, fixtures_root):
    """Validate one regression manifest; every case is planned (not-run) and mechanically checkable."""
    validate_record("regression-cases", record)
    skill = record["skill"]
    if skill not in identities:
        raise ContractError(f"regression manifest names an unknown skill: {skill}")
    cases = {}
    for case in record["cases"]:
        identity = case["id"]
        parts = identity.split(":")
        if case["skill_id"] != skill or parts[0] != skill or parts[1] != case["type"] or identity in cases:
            raise ContractError(f"duplicate or mismatched regression case identity/type: {identity}")
        if case["status"] != "not-run" or case["receipt_reference"] is not None:
            raise ContractError(f"{identity}: unobserved regression case cannot carry a result or receipt")
        _check_language(case)
        _check_dispatch(case)
        for index, check in enumerate(case["oracle"]["checks"]):
            validate_check(check, f"{identity} check {index}")
        destinations = _verify_fixtures(case, fixtures_root)
        if case["type"] == "negative":
            _check_negative(case, destinations)
        elif case["expected_route"] != skill or "route" in case["oracle"]:
            raise ContractError(f"{identity}: non-negative case requires its skill route")
        cases[identity] = case
    return cases


def load_regression_cases(root, identities):
    """Load every evals/cases/regression/<skill>.json manifest without a source-lock check."""
    directory = Path(root) / "evals/cases/regression"
    cases = {}
    for path in sorted(directory.glob("*.json")):
        record = load_json(path)
        if record.get("kind") != "regression-cases" or record.get("skill") != path.stem:
            raise ContractError(f"regression directory holds a non-regression or misnamed manifest: {path.name}")
        validated = validate_regression_manifest(record, identities, directory / "fixtures")
        if cases.keys() & validated.keys():
            raise ContractError("duplicate regression case identity across manifests")
        cases.update(validated)
    for identity in identities:
        if not any(case["skill_id"] == identity and case["type"] == "negative" for case in cases.values()):
            raise ContractError(f"{identity}: regression suite requires a near-miss negative case")
    return cases


def _nfc(text):
    return unicodedata.normalize("NFC", text)


def glob_regex(pattern):
    """Compile a POSIX glob where * and ? stay inside one segment and ** spans segments."""
    pattern = _nfc(pattern)
    parts, index = [], 0
    while index < len(pattern):
        char = pattern[index]
        if pattern.startswith("**/", index):
            parts.append("(?:.*/)?")
            index += 3
        elif pattern.startswith("**", index):
            parts.append(".*")
            index += 2
        elif char == "*":
            parts.append("[^/]*")
            index += 1
        elif char == "?":
            parts.append("[^/]")
            index += 1
        elif char == "[" and "]" in pattern[index + 2:]:
            end = pattern.index("]", index + 2)
            body = pattern[index + 1:end].replace("\\", "\\\\")
            parts.append("[" + ("^" + body[1:] if body.startswith("!") else body) + "]")
            index = end + 1
        else:
            parts.append(re.escape(char))
            index += 1
    return re.compile("".join(parts), re.DOTALL)


_HOOK_STATE = tuple(re.compile(pattern) for pattern in HOOK_RUNTIME_STATE)


def _matching(paths, pattern):
    regex = glob_regex(pattern)
    return sorted(path for path in paths if regex.fullmatch(path))


def _read_text(workspace, relative):
    return contained(workspace, relative).read_bytes().decode("utf-8")


def _broken_links(workspace, relative, files):
    directories = {""}
    for path in files:
        parent = posixpath.dirname(path)
        while parent and parent not in directories:
            directories.add(parent)
            parent = posixpath.dirname(parent)
    broken, fenced = [], False
    for line in _read_text(workspace, relative).splitlines():
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        for href in LINK.findall(INLINE_CODE.sub("", line)):
            target = unquote(href.split("#", 1)[0])
            if not target or SCHEME.match(target) or target.startswith("/"):
                continue
            joined = _nfc(posixpath.normpath(posixpath.join(posixpath.dirname(relative), target)))
            if joined.startswith("..") or (joined not in files and joined not in directories):
                broken.append(target)
    return broken


def _file_check(kind, target, expected, before, after, workspace):
    matched = _matching(after, target)
    if kind == "file-exists":
        return bool(matched), f"{len(matched)} matching file(s)"
    if kind == "file-absent":
        allowed = [glob_regex(pattern) for pattern in expected] + list(_HOOK_STATE)
        created = [path for path in matched
                   if path not in before and not any(regex.fullmatch(path) for regex in allowed)]
        return not created, "new matching files: " + ", ".join(created) if created else "no new matching file"
    if kind == "glob-count-min":
        return len(matched) >= expected, f"{len(matched)} matching file(s), need {expected}"
    if kind in {"sha256-unchanged", "eol-unchanged"}:
        field = "sha256" if kind == "sha256-unchanged" else "eol"
        originals = _matching(before, target)
        if not originals:
            return False, "no file in the before inventory matches the target"
        changed = [path for path in originals if path not in after or after[path][field] != before[path][field]]
        return not changed, "changed or missing: " + ", ".join(changed) if changed else f"{len(originals)} file(s) unchanged"
    if kind == "sha256-equals":
        wrong = [path for path in matched if after[path]["sha256"] != expected]
        return bool(matched) and not wrong, f"{len(matched)} matching file(s); mismatched: {wrong}"
    if kind == "links-resolve":
        broken = {path: links for path in matched if (links := _broken_links(workspace, path, after))}
        if not matched:
            return False, "no matching document"
        return not broken, f"broken links: {broken}" if broken else "all relative links resolve"
    plans = [path for path in matched if posixpath.basename(path) == "plan.md"]
    if not plans:
        return False, "no plan.md matches the target"
    verdicts = {}
    for path in plans:
        parent = posixpath.dirname(path)
        verdicts[path] = check_plan(contained(workspace, parent) if parent else workspace)["verdict"]
    return all(verdict == expected for verdict in verdicts.values()), f"plan verdicts: {verdicts}"


def _text_check(kind, target, expected, after, workspace, response):
    pattern = re.compile(expected)
    if target == RESPONSE:
        if response is None:
            return False, "check needs the final response (--response) and none was supplied"
        sources = {RESPONSE: response}
    else:
        sources = {}
        for path in _matching(after, target):
            try:
                sources[path] = _read_text(workspace, path)
            except UnicodeDecodeError:
                return False, f"{path} is not strict UTF-8"
    hits = [name for name, text in sources.items() if pattern.search(text)]
    if kind == "text-present":
        return bool(hits), f"matched in: {hits}" if hits else f"no match in {len(sources)} source(s)"
    return not hits, f"forbidden match in: {hits}" if hits else f"absent from {len(sources)} source(s)"


def _is_git(argv):
    return os.path.basename(str(argv[0])).casefold() in GIT_NAMES


def _sandbox_env(sandbox, home):
    """Minimal environment: no inherited secrets, a scratch HOME and git kept off parent repos.

    GIT_CONFIG_COUNT applies the hardening as command-line config, so it also reaches git
    started by a Python check and outranks the copied repository's own config.
    """
    env = {name: os.environ[name] for name in INHERITED_ENV if name in os.environ}
    env.update({"HOME": str(home), "USERPROFILE": str(home), "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1",
                "PYTHONDONTWRITEBYTECODE": "1", "GIT_CEILING_DIRECTORIES": str(sandbox),
                "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_COUNT": "2",
                "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
                "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": str(home)})
    return env


def _exit_check(argv, expected, workspace):
    """Run a kit-manifest argv against a disposable copy of the workspace.

    The copy lives in a fresh temporary directory outside the workspace and is deleted
    afterwards, so the scored workspace stays byte-identical. This is filesystem isolation
    only: the command still runs as the operator's user with network and process access,
    and the copied repository's own config (for example a diff driver) still applies to git.
    """
    workspace = Path(os.path.realpath(workspace))
    with tempfile.TemporaryDirectory(prefix="nckh-oracle-", ignore_cleanup_errors=True) as scratch:
        sandbox = Path(os.path.realpath(scratch))
        if sandbox.is_relative_to(workspace):
            raise ContractError("exit-status sandbox would sit inside the workspace; point TEMP elsewhere")
        home, copy = sandbox / "home", sandbox / "workspace"
        home.mkdir()
        try:
            shutil.copytree(workspace, copy, symlinks=True)
        except (OSError, shutil.Error) as error:
            return False, f"workspace copy failed: {type(error).__name__}"
        command = [sys.executable if argv[0] == "python" else argv[0], *argv[1:]]
        if _is_git(command):
            command[1:1] = ["-c", "core.fsmonitor=false", "-c", f"core.hooksPath={home}"]
        try:
            result = subprocess.run(command, cwd=copy, env=_sandbox_env(sandbox, home), stdin=subprocess.DEVNULL,
                                    capture_output=True, timeout=EXIT_TIMEOUT)
        except (OSError, subprocess.TimeoutExpired) as error:
            return False, f"command did not complete: {type(error).__name__}"
    return result.returncode == expected, f"exit {result.returncode}, expected {expected}"


def _inventory_files(record, label):
    if (not isinstance(record, dict) or record.get("schema_version") != 1 or not isinstance(record.get("files"), dict)
            or not all(isinstance(row, dict) and SHA256.fullmatch(str(row.get("sha256", "")))
                       and row.get("eol") in EOL_PROFILES for row in record["files"].values())):
        raise ContractError(f"{label} is not a check-receipt.py inventory record")
    return {_nfc(path): row for path, row in record["files"].items()}


def _inventory_links(record, label):
    """Link-like entries of an inventory; an older record without `links` counts as none."""
    links = record.get("links", [])
    if not isinstance(links, list) or not all(isinstance(path, str) and path for path in links):
        raise ContractError(f"{label} has a malformed links list")
    return {_nfc(path) for path in links}


def evaluate_case(case, workspace, before, response=None):
    """Score the mechanical checks of one regression case without any model call.

    Response text is matched, never executed. Only exit-status checks run a command: the argv
    recorded in the kit manifest, against a disposable copy of the workspace, after the file
    inventory is taken. A fixture missing or altered in the before inventory, or a git check
    on a workspace without its own .git, blocks scoring (setup error). A link-like entry that
    is absent from the before inventory adds a failing `links-created` row.
    """
    workspace = Path(workspace)
    before_files = _inventory_files(before, "before inventory")
    before_links = _inventory_links(before, "before inventory")
    setup = [fixture_destination(f["path"]) for f in case["fixtures"]
             if before_files.get(_nfc(fixture_destination(f["path"])), {}).get("sha256") != f["sha256"]]
    result = {"case_id": case["id"], "evidence_class": "mechanical-only", "checks": [],
              "setup_findings": [f"fixture absent or altered before the attempt: {path}" for path in setup],
              "reviewer_acceptance": case["oracle"]["acceptance"]}
    if any(c["kind"] == "exit-status" and _is_git(c["target"]) for c in case["oracle"]["checks"]) \
            and not (workspace / ".git").exists():
        result["setup_findings"].append("git exit-status check needs the workspace's own .git; "
                                        "refusing to let git use a parent repository")
    if result["setup_findings"]:
        return {**result, "verdict": "BLOCKED"}
    current = inventory(workspace)
    after = _inventory_files(current, "workspace inventory")
    created_links = sorted(_inventory_links(current, "workspace inventory") - before_links)
    checks = case["oracle"]["checks"]
    for check in [c for c in checks if c["kind"] != "exit-status"] + [c for c in checks if c["kind"] == "exit-status"]:
        kind, target, expected = check["kind"], check["target"], check["expected"]
        if kind == "exit-status":
            passed, detail = _exit_check(target, expected, workspace)
        elif kind in {"text-present", "text-absent"}:
            passed, detail = _text_check(kind, target, expected, after, workspace, response)
        else:
            passed, detail = _file_check(kind, target, expected, before_files, after, workspace)
        result["checks"].append({**check, "result": "pass" if passed else "fail", "detail": detail})
    if created_links:
        # The inventory never follows links, so a link the agent created could hide a write
        # outside the workspace; no manifest check can score it, so it always fails.
        result["checks"].append({"kind": "links-created", "target": "**", "expected": None, "result": "fail",
                                 "detail": "link-like entries created during the attempt: " + ", ".join(created_links)})
    return {**result, "verdict": "PASS" if all(row["result"] == "pass" for row in result["checks"]) else "FAIL"}


def validate_required_families(record, identities, cases, regression_cases=None):
    """Check family membership; regression case IDs are resolved when the caller supplies them."""
    validate_record("required-families", record)
    families = record["families"]
    if len(families) != 24 or len({f["id"] for f in families}) != 24:
        raise ContractError("all 24 unique required case families must remain")
    for family in families:
        if len(set(family["skills"])) != len(family["skills"]):
            raise ContractError("duplicate family skill mapping")
        for identity in family["skills"]:
            if identity not in identities or not set(identities[identity]["eval_ids"]) <= cases.keys():
                raise ContractError("required family maps to unknown skill/cases")
        if len(set(family["family_cases"])) != len(family["family_cases"]):
            raise ContractError("duplicate family regression case")
        if family["id"] in LAB02_FAMILIES and not family["family_cases"]:
            raise ContractError(f"family {family['id']} requires regression cases")
        for identity in family["family_cases"]:
            if identity.split(":")[0] not in family["skills"]:
                raise ContractError(f"family {family['id']} case {identity} belongs to a skill outside the family")
            if regression_cases is not None and identity not in regression_cases:
                raise ContractError(f"family {family['id']} names a missing regression case: {identity}")
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
    regression = load_regression_cases(root, identities)
    routing_ids = set()
    for path in (root / "evals/cases").glob("*/*.json"):
        record = load_json(path)
        if path == research_path:
            continue
        if record.get("kind") == "research-domain-scenarios":
            raise ContractError("research supplemental matrix has a duplicate or misplaced loader route")
        # Routing prompts carry no skill_id, so they must be routed before the base-case branch
        # or they would be skipped silently. They never count toward the 172 base cases.
        if record.get("kind") == "routing-prompts" or path.parent.name == "routing":
            if path.parent != root / "evals/cases/routing" or record.get("kind") != "routing-prompts":
                raise ContractError(f"routing prompts belong only in evals/cases/routing: {path.name}")
            ids = {row["id"] for row in validate_routing_prompts(record, identities)}
            if routing_ids & ids:
                raise ContractError("duplicate routing prompt identity across files")
            routing_ids |= ids
            continue
        if record.get("kind") == "regression-cases" or path.parent.name == "regression":
            if path.parent != root / "evals/cases/regression":
                raise ContractError("regression manifest outside evals/cases/regression")
            continue
        if "skill_id" not in record:
            continue
        validated = validate_case_manifest(record, identities)
        if cases.keys() & validated.keys():
            raise ContractError("duplicate case identity across manifests")
        cases.update(validated)
    if not routing_ids:
        raise ContractError("routing prompt suite missing from evals/cases/routing")
    if set(cases) != {identity + ":" + kind for identity in identities for kind in ("positive", "negative", "outcome", "failure")}:
        raise ContractError("exactly 172 approved base case IDs required")
    for skill in identities.values():
        if set(skill["eval_ids"]) != {skill["id"] + ":" + t for t in ["positive", "negative", "outcome", "failure"]}:
            raise ContractError("skill requires positive/negative/outcome/failure IDs")
        if not set(skill["eval_ids"]) <= cases.keys():
            raise ContractError("missing required skill case")
        if skill["status"] == "stable":
            raise ContractError("this candidate has no complete scoped stable qualification")
    if cases.keys() & regression.keys():
        raise ContractError("regression case identity collides with a base case")
    families = validate_required_families(load_json(root / "evals/cases/required-families.json"), identities, cases,
                                          regression)
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
            "regression_cases": len(regression), "routing_prompts": len(routing_ids),
            "regression_not_run": sum(c["status"] == "not-run" for c in regression.values()),
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
