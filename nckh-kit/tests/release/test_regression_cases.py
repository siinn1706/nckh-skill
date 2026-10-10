"""Regression suite: loader invariants, fixture pins, families and the mechanical oracle scorer."""
import json
import os
import re
import shutil
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock

from core import evaluation
from core.build import load_json, validate_catalog
from core.evaluation import (LAB02_FAMILIES, RESPONSE, evaluate_case, fixture_destination,
                             has_vietnamese_diacritics, load_regression_cases, validate_case_manifest,
                             validate_check, validate_regression_manifest, validate_required_families)
from core.ledger import inventory
from core.paths import temporary_tree
from core.route_hint import validate_routing_prompts
from core.schema import ContractError
from tests._lab import lab_root

ROOT = Path(__file__).resolve().parents[2]
SUITE = ROOT / "evals/cases/regression"
FIXTURES = SUITE / "fixtures"
PLANS = ROOT / "tests/contracts/fixtures/plans"
NEAR_MISS_OWNER = re.compile(r"nckh-[a-z]+(?:-[a-z]+)*")
UNMAPPED_BEFORE = ("nckh-handoff", "nckh-review", "nckh-research", "nckh-paperwrite", "nckh-humanwrite",
                   "nckh-statistics", "nckh-dataset", "nckh-telemetry", "nckh-aiops")
ROUTING_PROMPTS = ROOT / "evals/cases/routing/route-prompts.json"
PHASE_CONTRACT = "nckh-plan:positive:phase-files-contract"
EXIT_MASK = "nckh-debug:failure:chained-command-exit-mask"
STALE_HANDOFF = "nckh-handoff:positive:stale-pass-timeout"
# Shortened from a real response that reported the masked failure correctly.
EXIT_MASK_RESPONSE = ("`python -B -m unittest test_app` failed with exit code 1. It ran 3 tests and 2 failed. "
                      "`python -B build.py` exited 0; `;` reports only the last command's exit code.")
VI_PLAN = """---
title: Sửa hàm conversion trong app.py
created: 2026-10-08
status: planned
---

# Kế hoạch: sửa `conversion` trong `app.py`

## Tiêu chí chấp nhận

- `python -B -m unittest test_app` thoát mã 0.

## Các giai đoạn

| Phase | Tệp | Status |
|---|---|---|
| 1 | [Baseline](./phase-01-baseline.md) | {status} |
| 2 | [Sửa và kiểm chứng](./phase-02-sua-va-kiem-chung.md) | pending |
"""
VI_PHASE = """---
phase: {number}
title: {title}
status: planned
---

# Phase {number} — {title}

## Yêu cầu

- Giữ nguyên byte của `test_app.py` và `owner-note.txt`.

## Tệp

- Đọc: `app.py`, `test_app.py`.

## Các bước

1. Chạy riêng `python -B -m unittest test_app` và ghi exit code.

## Kiểm tra

- Exit code của từng lệnh được ghi riêng.{extra}

## Rủi ro / Rollback

- Rollback: khôi phục `app.py` từ preimage.
"""


def vietnamese_plan(workspace, status="pending", extra=""):
    """Write a two-phase plan whose headings are Vietnamese only, like the real blind attempt."""
    folder = workspace / "plans/261008-1530-sua-ham-conversion"
    folder.mkdir(parents=True)
    (folder / "plan.md").write_text(VI_PLAN.format(status=status), encoding="utf-8")
    for number, slug, title in ((1, "baseline", "Baseline"), (2, "sua-va-kiem-chung", "Sửa và kiểm chứng")):
        (folder / f"phase-0{number}-{slug}.md").write_text(
            VI_PHASE.format(number=number, title=title, extra=extra), encoding="utf-8")
    return folder


def make_link(link, target):
    """Create a symlink, or a junction on Windows without symlink rights; None when neither works."""
    try:
        os.symlink(target, link, target_is_directory=target.is_dir())
        return link
    except (OSError, NotImplementedError):
        pass
    if os.name == "nt" and target.is_dir():
        try:
            import _winapi
            _winapi.CreateJunction(str(target), str(link))
            return link
        except OSError:
            pass
    return None


def base_manifests():
    for path in sorted((ROOT / "evals/cases").glob("*/*.json")):
        record = load_json(path)
        if "skill_id" in record and record.get("kind") is None:
            yield path, record


class RegressionCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.identities = validate_catalog(load_json(ROOT / "core/registry/catalog/skills.json"))
        cls.cases = load_regression_cases(ROOT, cls.identities)
        cls.base = {}
        for _, record in base_manifests():
            cls.base.update(validate_case_manifest(record, cls.identities))

    def setUp(self):
        self.tree = temporary_tree(lab_root())
        self.lab = self.tree.__enter__()
        self.addCleanup(self.tree.__exit__, None, None, None)

    def manifest(self, skill):
        return load_json(SUITE / f"{skill}.json")

    def workspace(self, case, name="Không gian làm việc"):
        """Copy the case fixtures into a fresh workspace and record its before inventory."""
        workspace = self.lab / name
        workspace.mkdir()
        for fixture in case["fixtures"]:
            target = workspace / fixture_destination(fixture["path"])
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(FIXTURES / fixture["path"], target)
        return workspace, inventory(workspace)

    def run_oracle(self, case_id, workspace, before, response=None):
        before_path = self.lab / f"{workspace.name}.trước.json"
        before_path.write_text(json.dumps(before), encoding="utf-8")
        command = [sys.executable, "-I", str(ROOT / "scripts/check-case-oracle.py"), "--case-id", case_id,
                   "--workspace", str(workspace), "--before", str(before_path)]
        if response is not None:
            response_path = self.lab / f"{workspace.name}.phản-hồi.txt"
            response_path.write_text(response, encoding="utf-8")
            command += ["--response", str(response_path)]
        result = subprocess.run(command, capture_output=True, timeout=120, stdin=subprocess.DEVNULL)
        return result.returncode, json.loads(result.stdout.decode("ascii")) if result.stdout.strip() else None

    def test_all_173_cases_load_with_mechanical_checks(self):
        self.assertEqual(len(self.cases), 173)
        self.assertEqual({path.stem for path in SUITE.glob("*.json")}, set(self.identities))
        self.assertFalse(self.cases.keys() & self.base.keys())
        for identity, case in self.cases.items():
            with self.subTest(case=identity):
                self.assertRegex(identity, r"^nckh-[a-z-]+:(positive|negative|outcome|failure):[a-z0-9-]+$")
                self.assertGreaterEqual(len(case["oracle"]["checks"]), 1)
                self.assertEqual((case["status"], case["receipt_reference"]), ("not-run", None))
        # Fixtures must never make a lab ancestor look like it holds installed skills.
        self.assertFalse([path for path in FIXTURES.rglob("nckh-*")])
        referenced = {fixture["path"] for case in self.cases.values() for fixture in case["fixtures"]}
        self.assertTrue(referenced)

    def test_fixture_hash_mismatch_rejected(self):
        record = self.manifest("nckh-fix")
        validate_regression_manifest(record, self.identities, FIXTURES)
        broken = deepcopy(record)
        broken["cases"][0]["fixtures"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ContractError, "hash mismatch"):
            validate_regression_manifest(broken, self.identities, FIXTURES)
        altered = self.lab / "fixtures"
        shutil.copytree(FIXTURES / "r43", altered / "r43")
        (altered / "r43/app.py").write_bytes(b"def conversion(count, total):\n    return 40\n")
        with self.assertRaisesRegex(ContractError, "hash mismatch"):
            validate_regression_manifest(record, self.identities, altered)
        for path in ("app.py", "r43/../r43/app.py", "r43/missing.txt"):
            broken = deepcopy(record)
            broken["cases"][0]["fixtures"][0]["path"] = path
            with self.subTest(path=path), self.assertRaises(ContractError):
                validate_regression_manifest(broken, self.identities, FIXTURES)

    def test_case_without_mechanical_check_rejected(self):
        record = self.manifest("nckh-plan")
        mutations = [
            [],
            [{"kind": "file-exists", "target": "plans/*/plan.md"}],
            [{"kind": "glob-match", "target": "plans/**", "expected": None}],
            [{"kind": "text-present", "target": RESPONSE, "expected": "(unclosed"}],
            [{"kind": "sha256-equals", "target": "app.py", "expected": "ABC"}],
            [{"kind": "glob-count-min", "target": "plans/*.md", "expected": 0}],
            [{"kind": "file-absent", "target": "../outside/**", "expected": []}],
            [{"kind": "exit-status", "target": "python -m unittest", "expected": 0}],
            [{"kind": "plan-check", "target": "plans/*/plan.md", "expected": "PASS"}],
        ]
        for checks in mutations:
            broken = deepcopy(record)
            broken["cases"][0]["oracle"]["checks"] = checks
            with self.subTest(checks=checks), self.assertRaises(ContractError):
                validate_regression_manifest(broken, self.identities, FIXTURES)
        negative = deepcopy(record)
        case = next(c for c in negative["cases"] if c["type"] == "negative")
        case["oracle"]["checks"] = [c for c in case["oracle"]["checks"] if c["kind"] != "file-absent"]
        with self.assertRaisesRegex(ContractError, "file-absent"):
            validate_regression_manifest(negative, self.identities, FIXTURES)

    def test_unobserved_case_with_receipt_rejected(self):
        record = self.manifest("nckh-cook")
        for status, receipt in [("not-run", "reports/receipt.json"), ("pass", "reports/receipt.json"),
                                ("pass", None), ("not-run", "")]:
            broken = deepcopy(record)
            broken["cases"][0].update(status=status, receipt_reference=receipt)
            with self.subTest(status=status, receipt=receipt), self.assertRaises(ContractError):
                validate_regression_manifest(broken, self.identities, FIXTURES)
        self.assertEqual(record["cases"][0]["type"], "positive")
        for field, value in [("id", record["cases"][1]["id"]), ("type", "failure"), ("skill_id", "nckh-plan")]:
            broken = deepcopy(record)
            broken["cases"][0][field] = value
            with self.subTest(field=field), self.assertRaises(ContractError):
                validate_regression_manifest(broken, self.identities, FIXTURES)

    def test_every_skill_has_near_miss_negative(self):
        for skill in self.identities:
            negatives = [c for c in self.cases.values() if c["skill_id"] == skill and c["type"] == "negative"]
            with self.subTest(skill=skill):
                self.assertTrue(negatives)
                owners = {owner for case in negatives
                          for owner in NEAR_MISS_OWNER.findall(" ".join(case["oracle"]["acceptance"] + case["expected_outcome"]))}
                self.assertTrue(owners - {skill}, "negative case names no sibling owner")
        copy = self.lab / "kit"
        shutil.copytree(SUITE, copy / "evals/cases/regression")
        path = copy / "evals/cases/regression/nckh-seo.json"
        record = load_json(path)
        record["cases"] = [c for c in record["cases"] if c["type"] != "negative"]
        path.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
        with self.assertRaisesRegex(ContractError, "near-miss negative"):
            load_regression_cases(copy, self.identities)

    def test_outcome_prompt_differs_from_positive(self):
        count = 0
        for path, record in base_manifests():
            cases = {case["type"]: case for case in record["cases"]}
            self.assertNotEqual(cases["outcome"]["prompt"], cases["positive"]["prompt"], path.name)
            broken = deepcopy(record)
            next(c for c in broken["cases"] if c["type"] == "outcome").update(
                prompt=cases["positive"]["prompt"], input_language=cases["positive"]["input_language"])
            with self.subTest(skill=record["skill_id"]), self.assertRaisesRegex(ContractError, "outcome prompt"):
                validate_case_manifest(broken, self.identities)
            count += 1
        self.assertEqual(count, 43)
        self.assertTrue((ROOT / "evals/cases/tooling/nckh-xia.json").is_file())
        self.assertFalse((ROOT / "evals/cases/engineer/nckh-xia.json").exists())

    def test_vietnamese_prompt_language_tag(self):
        self.assertTrue(has_vietnamese_diacritics("Sửa lỗi"))
        self.assertFalse(has_vietnamese_diacritics("Review the API diff --vi"))
        for case in [*self.base.values(), *self.cases.values()]:
            if has_vietnamese_diacritics(case["prompt"]):
                self.assertIn(case["input_language"], {"vi", "bilingual"}, case["id"])
        for identity in ("nckh-fix:outcome", "nckh-scout:outcome", "nckh-market-research:outcome"):
            self.assertEqual(self.base[identity]["input_language"], "vi")
        record = load_json(ROOT / "evals/cases/engineer/nckh-fix.json")
        next(c for c in record["cases"] if c["type"] == "positive")["input_language"] = "en"
        with self.assertRaisesRegex(ContractError, "input_language"):
            validate_case_manifest(record, self.identities)
        regression = self.manifest("nckh-plan")
        regression["cases"][0]["input_language"] = "en"
        with self.assertRaisesRegex(ContractError, "input_language"):
            validate_regression_manifest(regression, self.identities, FIXTURES)

    def test_required_families_cover_lab02_failure_modes(self):
        record = load_json(ROOT / "evals/cases/required-families.json")
        families = validate_required_families(record, self.identities, self.base, self.cases)
        self.assertEqual(len(families), 24)
        by_id = {family["id"]: family for family in families}
        for family_id in LAB02_FAMILIES:
            self.assertTrue(by_id[family_id]["family_cases"], family_id)
        self.assertIn("nckh-plan:failure:mixed-deliverable-lab02", by_id["plan-deliverable-mix"]["family_cases"])
        self.assertIn("nckh-debug:failure:chained-command-exit-mask", by_id["exit-masking"]["family_cases"])
        mapped = {skill for family in families for skill in family["skills"]}
        self.assertTrue(set(UNMAPPED_BEFORE) <= mapped)
        for mutate, message in [
            (lambda f: f["families"][19]["family_cases"].clear(), "requires regression cases"),
            (lambda f: f["families"][19]["family_cases"].append("nckh-plan:failure:missing-case"), "missing regression case"),
            (lambda f: f["families"][19]["family_cases"].append("nckh-seo:failure:rank-guarantee-stuffing"), "outside the family"),
            (lambda f: f["families"].pop(), "too few items|24 unique"),
            (lambda f: f["families"].append(deepcopy(f["families"][0])), "24 unique"),
        ]:
            broken = deepcopy(record)
            mutate(broken)
            with self.subTest(message=message), self.assertRaisesRegex(ContractError, message):
                validate_required_families(broken, self.identities, self.base, self.cases)

    def test_check_case_oracle_pass_and_fail_workspaces(self):
        case_id = "nckh-fix:positive:before-after-receipt"
        case = self.cases[case_id]
        passing, before = self.workspace(case, "Bản sửa đúng")
        app = passing / "app.py"
        app.write_bytes(re.sub(rb"return count \* 100(?=\r?\n)", b"return count * 100 // total", app.read_bytes()))
        code, report = self.run_oracle(case_id, passing, before)
        self.assertEqual((code, report["verdict"]), (0, "PASS"), report)
        self.assertEqual(report["workspace"], str(passing))
        failing, before = self.workspace(case, "Bản chưa sửa")
        (failing / "owner-note.txt").write_bytes(b"overwritten\n")
        code, report = self.run_oracle(case_id, failing, before)
        self.assertEqual((code, report["verdict"]), (1, "FAIL"))
        failed = {(row["kind"], json.dumps(row["target"])) for row in report["checks"] if row["result"] == "fail"}
        self.assertIn(("sha256-unchanged", '"owner-note.txt"'), failed)
        self.assertTrue(any(kind == "exit-status" for kind, _ in failed))
        rewritten, before = self.workspace(case, "Bản sửa đổi EOL")
        app = rewritten / "app.py"
        app.write_bytes(app.read_bytes().replace(b"\r\n", b"\n").replace(b"return count * 100\n",
                                                                         b"return count * 100 // total\n"))
        code, report = self.run_oracle(case_id, rewritten, before)
        self.assertEqual((code, report["verdict"]), (1, "FAIL"))
        self.assertEqual([row["kind"] for row in report["checks"] if row["result"] == "fail"], ["eol-unchanged"])
        blocked, before = self.workspace(case, "Thiếu fixture")
        before["files"].pop("test_app.py")
        code, report = self.run_oracle(case_id, blocked, before)
        self.assertEqual((code, report["verdict"]), (1, "BLOCKED"))
        negative_id = "nckh-copy:negative:near-miss-humanwrite"
        quiet, before = self.workspace(self.cases[negative_id], "Từ chối")
        code, report = self.run_oracle(negative_id, quiet, before, "Yêu cầu này thuộc nckh-humanwrite; handoff.")
        self.assertEqual((code, report["verdict"]), (0, "PASS"), report)
        (quiet / "bản-sửa.md").write_text("Công cụ checklist giúp sinh viên.", encoding="utf-8")
        code, report = self.run_oracle(negative_id, quiet, before)
        self.assertEqual((code, report["verdict"]), (1, "FAIL"))
        self.assertIn("--response", next(r["detail"] for r in report["checks"] if r["target"] == RESPONSE))
        code, report = self.run_oracle("nckh-fix:positive:unknown", quiet, before)
        self.assertEqual((code, report), (2, None))

    def test_lab02_plan_case_fails_on_single_file_plan(self):
        case = self.cases["nckh-plan:failure:mixed-deliverable-lab02"]
        response = "Đã lập kế hoạch; báo cáo, ảnh và PDF chưa tạo, sẽ handoff cho nckh-cook."
        single, before = self.workspace(case, "Kế hoạch một file")
        shutil.copytree(FIXTURES / "F-LAB02PLAN/plans", single / "plans")
        result = evaluate_case(case, single, before, response)
        self.assertEqual(result["verdict"], "FAIL")
        plan_check = next(row for row in result["checks"] if row["kind"] == "plan-check")
        self.assertEqual(plan_check["result"], "fail")
        self.assertIn("FAILED", plan_check["detail"])
        valid, before = self.workspace(case, "Kế hoạch đủ phase")
        shutil.copytree(PLANS / "valid-two-phase", valid / "plans/bao-cao-lab-2")
        result = evaluate_case(case, valid, before, response)
        self.assertEqual(result["verdict"], "PASS", result["checks"])
        (valid / "out").mkdir()
        (valid / "out/bao-cao.pdf").write_bytes(b"%PDF-1.4\n")
        result = evaluate_case(case, valid, before, response)
        self.assertEqual(result["verdict"], "FAIL")
        self.assertEqual({row["target"] for row in result["checks"] if row["result"] == "fail"},
                         {"**/*.pdf", "out/**", "**"})

    def test_plan_check_scores_a_plan_at_the_workspace_root(self):
        check = {"kind": "plan-check", "target": "plan.md", "expected": "VERIFIED"}
        validate_check(check, "root plan")
        case = synthetic_case(check)
        valid = self.lab / "Kế hoạch ở gốc"
        shutil.copytree(PLANS / "valid-two-phase", valid)
        self.assertEqual(evaluate_case(case, valid, inventory(valid))["verdict"], "PASS")
        single = self.lab / "Kế hoạch một file ở gốc"
        shutil.copytree(PLANS / "lab02-single-file", single)
        result = evaluate_case(case, single, inventory(single))
        self.assertEqual(result["verdict"], "FAIL")
        self.assertIn("FAILED", result["checks"][0]["detail"])

    def test_before_inventory_row_without_eol_is_a_usage_error(self):
        case_id = "nckh-fix:positive:before-after-receipt"
        workspace, before = self.workspace(self.cases[case_id], "Thiếu EOL")
        del before["files"]["app.py"]["eol"]
        self.assertEqual(self.run_oracle(case_id, workspace, before), (2, None))
        before["files"]["app.py"]["eol"] = "crlf"
        del before["files"]["owner-note.txt"]["eol"]
        self.assertEqual(self.run_oracle(case_id, workspace, before), (2, None))

    def test_exit_checks_run_with_a_minimal_environment(self):
        allowed = sorted({"PATH", "SYSTEMROOT", "TEMP", "TMP", "HOME", "USERPROFILE", "PYTHONIOENCODING",
                          "PYTHONUTF8", "PYTHONDONTWRITEBYTECODE", "GIT_CEILING_DIRECTORIES", "GIT_CONFIG_NOSYSTEM",
                          "GIT_CONFIG_COUNT", "GIT_CONFIG_KEY_0", "GIT_CONFIG_VALUE_0", "GIT_CONFIG_KEY_1",
                          "GIT_CONFIG_VALUE_1"})
        workspace = self.lab / "Môi trường tối thiểu"
        workspace.mkdir()
        probe = ("import os, sys\n"
                 f"extra = {{name.upper() for name in os.environ}} - set({allowed!r})\n"
                 "home = os.path.expanduser('~')\n"
                 f"ok = not extra and os.environ['GIT_CONFIG_NOSYSTEM'] == '1' and home != {str(Path.home())!r}\n"
                 "ok = ok and os.path.samefile(os.environ['GIT_CEILING_DIRECTORIES'], os.path.dirname(os.getcwd()))\n"
                 f"ok = ok and not os.path.samefile(os.getcwd(), {str(workspace)!r})\n"
                 "raise SystemExit(0 if ok else 1)")
        case = synthetic_case({"kind": "exit-status", "target": ["python", "-c", probe], "expected": 0})
        with mock.patch.dict(os.environ, {"NCKH_ORACLE_SECRET": "do-not-leak"}):
            result = evaluate_case(case, workspace, inventory(workspace))
        self.assertEqual(result["verdict"], "PASS", result["checks"])

    def test_exit_checks_leave_the_workspace_byte_identical(self):
        workspace = self.lab / "Không gian gốc"
        (workspace / "dữ liệu").mkdir(parents=True)
        (workspace / "dữ liệu/mẫu.txt").write_bytes("Mẫu gốc\r\n".encode("utf-8"))
        (workspace / "app.py").write_bytes(b"VALUE = 1\n")
        before = inventory(workspace)
        vandal = ("import os, pathlib, shutil\n"
                  "pathlib.Path('app.py').write_text('VALUE = 2\\n')\n"
                  "pathlib.Path('mới.txt').write_text('created by the check')\n"
                  "shutil.rmtree('dữ liệu')\n"
                  "raise SystemExit(0 if pathlib.Path('app.py').read_text() == 'VALUE = 2\\n' else 1)")
        writer = {"kind": "exit-status", "target": ["python", "-c", vandal], "expected": 0}
        reader = {"kind": "exit-status", "target": ["python", "-c",
                                                    "import pathlib\nraise SystemExit(0 if pathlib.Path("
                                                    "'dữ liệu/mẫu.txt').is_file() else 1)"], "expected": 0}
        result = evaluate_case(synthetic_case(writer, reader), workspace, before)
        self.assertEqual(result["verdict"], "PASS", result["checks"])
        self.assertEqual(inventory(workspace), before)

    @unittest.skipUnless(shutil.which("git"), "git is not installed")
    def test_git_checks_stay_inside_the_workspace_repository(self):
        def git(*argv, cwd):
            subprocess.run(["git", *argv], cwd=cwd, check=True, capture_output=True, stdin=subprocess.DEVNULL)

        parent = self.lab / "Kho cha"
        workspace = parent / "Không có git"
        workspace.mkdir(parents=True)
        git("init", "-q", cwd=parent)
        direct = synthetic_case({"kind": "exit-status", "target": ["git", "rev-parse", "--git-dir"], "expected": 0})
        result = evaluate_case(direct, workspace, inventory(workspace))
        self.assertEqual(result["verdict"], "BLOCKED")
        self.assertTrue(any(".git" in finding for finding in result["setup_findings"]), result)
        nested = ("import subprocess\n"
                  "found = subprocess.run(['git', 'rev-parse', '--git-dir'], capture_output=True)\n"
                  "raise SystemExit(0 if found.returncode != 0 else 1)")
        result = evaluate_case(synthetic_case({"kind": "exit-status", "target": ["python", "-c", nested], "expected": 0}),
                               workspace, inventory(workspace))
        self.assertEqual(result["verdict"], "PASS", result["checks"])
        git("init", "-q", cwd=workspace)
        git("config", "core.fsmonitor", "true", cwd=workspace)
        result = evaluate_case(direct, workspace, inventory(workspace))
        self.assertEqual(result["verdict"], "PASS", result)
        config = ("import subprocess\n"
                  "read = lambda key: subprocess.run(['git', 'config', '--get', key], capture_output=True, text=True)\n"
                  "hooks = read('core.hooksPath').stdout.strip()\n"
                  "ok = read('core.fsmonitor').stdout.strip() == 'false' and hooks and '.git' not in hooks\n"
                  "raise SystemExit(0 if ok else 1)")
        result = evaluate_case(synthetic_case({"kind": "exit-status", "target": ["python", "-c", config], "expected": 0}),
                               workspace, inventory(workspace))
        self.assertEqual(result["verdict"], "PASS", result["checks"])

    def check_of(self, case_id, kind, target):
        return next(c for c in self.cases[case_id]["oracle"]["checks"] if (c["kind"], c["target"]) == (kind, target))

    def test_vietnamese_phase_headings_pass_phase_files_contract(self):
        case = self.cases[PHASE_CONTRACT]
        workspace, before = self.workspace(case, "Kế hoạch tiếng Việt")
        vietnamese_plan(workspace)
        result = evaluate_case(case, workspace, before, "Đã lập kế hoạch 2 phase trong plans/.")
        self.assertEqual(result["verdict"], "PASS", [row for row in result["checks"] if row["result"] == "fail"])
        self.assertIn("plan-check", {row["kind"] for row in result["checks"]})

    def test_negated_completion_sentence_not_flagged(self):
        case = self.cases[PHASE_CONTRACT]
        workspace, before = self.workspace(case, "Câu phủ định")
        vietnamese_plan(workspace, extra="\n- Nếu kiểm tra nào fail → không đánh dấu hoàn thành; quay về Phase 1.")
        result = evaluate_case(case, workspace, before)
        self.assertEqual(result["verdict"], "PASS", [row for row in result["checks"] if row["result"] == "fail"])
        handoff = self.check_of(STALE_HANDOFF, "text-absent", "plans/handoff.md")
        for index, text in enumerate(("Attempt a-2 chưa hoàn thành (timeout-unknown).",
                                      "Không có gate nào được accepted.", "Receipt cũ ghi done nhưng đã stale.")):
            folder = self.lab / f"Bàn giao {index}"
            (folder / "plans").mkdir(parents=True)
            (folder / "plans/handoff.md").write_text(f"# Bàn giao\n\n{text}\n", encoding="utf-8")
            with self.subTest(text=text):
                self.assertEqual(evaluate_case(synthetic_case(handoff), folder, inventory(folder))["verdict"], "PASS")

    def test_status_line_completion_flagged(self):
        case = self.cases[PHASE_CONTRACT]
        lines = ["status: completed", "Status: done", "- **Trạng thái:** hoàn thành", "**Status**: Completed",
                 "| 2 | [Sửa](./phase-02-sua-va-kiem-chung.md) | completed |", "| Phase 1 | **hoàn thành** |"]
        for index, line in enumerate(lines):
            workspace, before = self.workspace(case, f"Đánh dấu xong {index}")
            vietnamese_plan(workspace)
            (workspace / "plans/notes.md").write_text(f"# Ghi chú\n\n{line}\n", encoding="utf-8")
            result = evaluate_case(case, workspace, before)
            with self.subTest(line=line):
                self.assertEqual([row["kind"] for row in result["checks"] if row["result"] == "fail"], ["text-absent"])
        workspace, before = self.workspace(case, "Bảng phase xong")
        vietnamese_plan(workspace, status="completed")
        failed = [row["kind"] for row in evaluate_case(case, workspace, before)["checks"] if row["result"] == "fail"]
        self.assertIn("text-absent", failed)
        handoff = self.check_of(STALE_HANDOFF, "text-absent", "plans/handoff.md")
        for index, line in enumerate(("Status: done", "- Trạng thái: hoàn thành", "| a-2 | accepted |")):
            folder = self.lab / f"Bàn giao xong {index}"
            (folder / "plans").mkdir(parents=True)
            (folder / "plans/handoff.md").write_text(f"# Bàn giao\n\n{line}\n", encoding="utf-8")
            with self.subTest(handoff=line):
                self.assertEqual(evaluate_case(synthetic_case(handoff), folder, inventory(folder))["verdict"], "FAIL")

    def test_exit_mask_regex_variants(self):
        case = self.cases[EXIT_MASK]
        workspace, before = self.workspace(case, "Lệnh nối")
        self.assertEqual(evaluate_case(case, workspace, before, EXIT_MASK_RESPONSE)["verdict"], "PASS")
        pattern = re.compile(self.check_of(EXIT_MASK, "text-present", RESPONSE)["expected"])
        for text in ("It ran 3 tests and 2 failed", "FAILED (failures=2)", "2 test thất bại", "2 tests failed",
                     "2 (tests) failed", "failed: 2", "Kết quả: 2 lỗi", "2 failures, exit 1"):
            with self.subTest(passing=text):
                self.assertTrue(pattern.search(text))
        for text in ("3 failed", "12 failed", "Ran 3 tests, OK", "2 passed, 1 failed", "failures=12", "2.5 failed"):
            with self.subTest(failing=text):
                self.assertFalse(pattern.search(text))

    def test_negative_requires_invoke_skill_dispatch(self):
        negatives = [case for case in self.cases.values() if case["type"] == "negative"]
        self.assertEqual(len(negatives), 44)
        self.assertEqual({case.get("dispatch") for case in negatives}, {"invoke-skill"})
        record = self.manifest("nckh-debug")
        index = next(i for i, c in enumerate(record["cases"]) if c["type"] == "negative")
        for value, message in [(None, "invoke-skill"), ("natural", "invoke-skill"), ("auto", "dispatch|enum")]:
            broken = deepcopy(record)
            if value is None:
                broken["cases"][index].pop("dispatch")
            else:
                broken["cases"][index]["dispatch"] = value
            with self.subTest(dispatch=value), self.assertRaisesRegex(ContractError, message):
                validate_regression_manifest(broken, self.identities, FIXTURES)
        doubled = deepcopy(record)
        doubled["cases"][index]["prompt"] = "/nckh-fix " + doubled["cases"][index]["prompt"]
        with self.assertRaisesRegex(ContractError, "already names"):
            validate_regression_manifest(doubled, self.identities, FIXTURES)

    def test_debug_handoff_negative_keeps_no_write_contract(self):
        case = self.cases["nckh-debug:negative:repair-near-miss"]
        self.assertEqual((case["expected_route"], case["dispatch"]), ("reject-this-skill", "invoke-skill"))
        self.assertEqual(case["oracle"]["route"], {"expected": "reject-this-skill", "owner": "explicit-handoff",
                                                  "task_execution": "forbidden"})
        for phrase in ("chỉ bàn giao", "nckh-fix", "không sửa", "không chạy test repair"):
            self.assertIn(phrase, case["prompt"].casefold())
        self.assertEqual({f["path"]: f["sha256"] for f in case["fixtures"]}, {
            "r43/app.py": "451c45e9b761fe7a349ffe8472da065d4471997aaaffd91f65d770ac6aa21a11",
            "r43/test_app.py": "1edcb7bb5ca6f206dce7485f72de07145905b06670ed8206fe4d8d239edaf73f"})
        self.assertEqual(case["oracle"]["checks"], [
            {"kind": "sha256-unchanged", "target": "app.py", "expected": None},
            {"kind": "sha256-unchanged", "target": "test_app.py", "expected": None},
            {"kind": "file-absent", "target": "**", "expected": []}])

    def test_both_negative_validators_require_all_handoff_evidence(self):
        base = load_json(ROOT / "evals/cases/engineer/nckh-debug.json")
        regression = self.manifest("nckh-debug")
        for label, record in (("base", base), ("regression", regression)):
            for required in ("reject", "owner", "handoff", "do not execute"):
                broken = deepcopy(record)
                negative = next(c for c in broken["cases"] if c["type"] == "negative")
                negative["oracle"]["acceptance"] = [re.sub(re.escape(required), "omitted", text, flags=re.IGNORECASE)
                                                      for text in negative["oracle"]["acceptance"]]
                with self.subTest(validator=label, missing=required), self.assertRaisesRegex(
                        ContractError, "negative acceptance"):
                    if label == "base":
                        validate_case_manifest(broken, self.identities)
                    else:
                        validate_regression_manifest(broken, self.identities, FIXTURES)

    def test_negative_debug_route_cannot_authorize_fix(self):
        for label, record in (("base", load_json(ROOT / "evals/cases/engineer/nckh-debug.json")),
                              ("regression", self.manifest("nckh-debug"))):
            for route in ("nckh-debug", "nckh-fix"):
                broken = deepcopy(record)
                next(c for c in broken["cases"] if c["type"] == "negative")["expected_route"] = route
                with self.subTest(validator=label, route=route), self.assertRaisesRegex(ContractError, "negative oracle"):
                    if label == "base":
                        validate_case_manifest(broken, self.identities)
                    else:
                        validate_regression_manifest(broken, self.identities, FIXTURES)

    def test_debug_negative_rejects_fixture_edits_deletion_and_preimage(self):
        case = self.cases["nckh-debug:negative:repair-near-miss"]
        for index, target in enumerate(("app.py", "test_app.py", "deleted-app", ".attempt/app.py.preimage")):
            workspace, before = self.workspace(case, f"Negative side effect {index}")
            if target == "deleted-app":
                (workspace / "app.py").unlink()
            else:
                path = workspace / target
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(path.read_bytes() + b"# unexpected edit\r\n" if path.exists() else b"preimage\r\n")
            report = evaluate_case(case, workspace, before, "nckh-fix owns repair; handoff only.")
            with self.subTest(target=target):
                self.assertEqual(report["verdict"], "FAIL", report)
                if target.startswith(".attempt/"):
                    self.assertIn("file-absent", [c["kind"] for c in report["checks"] if c["result"] == "fail"])

    def test_dispatch_prompt_formats(self):
        negative = self.cases["nckh-debug:negative:repair-near-miss"]
        self.assertEqual(evaluation.dispatch_prompt(negative), "/nckh-debug " + negative["prompt"])
        self.assertEqual(evaluation.dispatch_prompt(negative, "${skill}"), "$nckh-debug " + negative["prompt"])
        natural = self.cases[EXIT_MASK]
        self.assertNotIn("dispatch", natural)
        self.assertEqual(evaluation.dispatch_prompt(natural), natural["prompt"])
        for invocation in ("/nckh-debug", "", None):
            with self.subTest(invocation=invocation), self.assertRaises(ContractError):
                evaluation.dispatch_prompt(negative, invocation)
        result = subprocess.run([sys.executable, "-I", str(ROOT / "scripts/check-case-oracle.py"), "--case-id",
                                 negative["id"], "--print-prompt", "--invocation", "${skill}"],
                                capture_output=True, timeout=120, stdin=subprocess.DEVNULL)
        self.assertEqual(result.returncode, 0, result.stderr)
        printed = json.loads(result.stdout.decode("ascii"))
        self.assertEqual(printed, {"case_id": negative["id"], "dispatch": "invoke-skill",
                                   "prompt": "$nckh-debug " + negative["prompt"]})

    def test_agent_created_link_fails(self):
        workspace = self.lab / "Liên kết"
        (workspace / "dữ liệu").mkdir(parents=True)
        (workspace / "app.py").write_bytes(b"VALUE = 1\n")
        outside = self.lab / "Bên ngoài"
        outside.mkdir()
        if make_link(workspace / "cũ", outside) is None:
            self.skipTest("this account can create neither a symlink nor a junction")
        case = synthetic_case({"kind": "file-exists", "target": "app.py", "expected": None})
        before = inventory(workspace)
        self.assertEqual(evaluate_case(case, workspace, before)["verdict"], "PASS")
        make_link(workspace / "dữ liệu/lối tắt", outside)
        result = evaluate_case(case, workspace, before)
        self.assertEqual(result["verdict"], "FAIL")
        created = [row for row in result["checks"] if row["kind"] == "links-created"]
        self.assertEqual(len(created), 1)
        self.assertIn("dữ liệu/lối tắt", created[0]["detail"])
        self.assertNotIn("cũ", created[0]["detail"].split(": ", 1)[1].split(", "))

    def write_hook_runtime_state(self, workspace):
        """Let the kit's own hook code write receipts, a cap marker and a snapshot."""
        from core import edit_guard
        from core.paths import digest_record
        from hooks import runner
        events = ".nckh-state/hooks/events/claude"
        runner.record_once(workspace, events, {"status": "checked-unreviewed", "host": "claude", "phase": "stop"})
        with mock.patch.object(runner, "RECEIPT_CAP", 1):
            for session in ("một", "hai"):
                runner.record_once(workspace, events, {"status": "degraded-no-context", "host": "claude",
                                                       "session_key": session, "hook_mode": "advisory"})
        session = digest_record("phiên hook")
        edit_guard.snapshot(workspace, "claude", session, ["app.py"])
        snapshots = edit_guard._session_dir(workspace, "claude", session)
        (snapshots / ".nckh-k3x_9q2z").write_bytes(b"")
        (workspace / events / ".nckh-ab12cd34").write_bytes(b"")
        return [path.relative_to(workspace).as_posix() for path in (workspace / ".nckh-state").rglob("*")
                if path.is_file()]

    def test_hook_runtime_state_excluded_from_file_absent(self):
        workspace = self.lab / "Trạng thái hook"
        workspace.mkdir()
        (workspace / "app.py").write_bytes(b"VALUE = 1\n")
        before = inventory(workspace)
        written = self.write_hook_runtime_state(workspace)
        names = {relative.rsplit("/", 1)[1] for relative in written}
        self.assertIn("cap-reached-no-context.json", names)
        self.assertTrue(any(name.startswith("no-context-") and name.endswith(".lock") for name in names))
        self.assertEqual(sum(".nckh-state/hooks/snapshots/" in relative for relative in written), 2)
        case = synthetic_case({"kind": "file-absent", "target": "**", "expected": []},
                              {"kind": "glob-count-min", "target": ".nckh-state/hooks/**", "expected": len(written)})
        result = evaluate_case(case, workspace, before)
        self.assertEqual(result["verdict"], "PASS", result["checks"])

    def test_foreign_files_in_hook_namespaces_not_excluded(self):
        session = "0123456789abcdef"
        for index, relative in enumerate((".nckh-state/hooks/snapshots/out.md",
                                          ".nckh-state/hooks/events/claude/out.md",
                                          ".nckh-state/hooks/events/claude/2026-10-08.jsonl",
                                          ".nckh-state/hooks/events/out.json",
                                          ".nckh-state/hooks/events/claude/sub/" + "a" * 64 + ".json",
                                          ".nckh-state/hooks/events/claude/" + "a" * 63 + ".json",
                                          ".nckh-state/hooks/events/claude/no-context-out.json",
                                          ".nckh-state/hooks/events/claude/.nckh-deliverable.md",
                                          f".nckh-state/hooks/snapshots/claude/{session}/app.py.json",
                                          f".nckh-state/hooks/snapshots/claude/phiên-1/{'b' * 32}.json",
                                          f".nckh-state/hooks/snapshots/claude/{session}/{'B' * 32}.json")):
            workspace = self.lab / f"Ngoài dạng hook {index}"
            workspace.mkdir()
            before = inventory(workspace)
            path = workspace / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}\n", encoding="utf-8")
            result = evaluate_case(synthetic_case({"kind": "file-absent", "target": "**", "expected": []}),
                                   workspace, before)
            with self.subTest(path=relative):
                self.assertEqual(result["verdict"], "FAIL")
                self.assertIn(relative, result["checks"][0]["detail"])

    def test_other_nckh_state_paths_not_excluded(self):
        for index, relative in enumerate((".nckh-state/install.json", ".nckh-state/hooks/config.json",
                                          ".nckh-state/hooks/events-extra/x.json",
                                          "plans/.nckh-state/hooks/events/x.json",
                                          "app.py.nckh-state/hooks/events/x.json")):
            workspace = self.lab / f"Ngoài namespace {index}"
            workspace.mkdir()
            before = inventory(workspace)
            path = workspace / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}\n", encoding="utf-8")
            result = evaluate_case(synthetic_case({"kind": "file-absent", "target": "**", "expected": []}),
                                   workspace, before)
            with self.subTest(path=relative):
                self.assertEqual(result["verdict"], "FAIL")
                self.assertIn(relative, result["checks"][0]["detail"])

    def validated_summary(self, root=ROOT):
        # The source lock is checked elsewhere; this suite scores case loading only.
        with mock.patch.object(evaluation, "verify_source_lock", return_value={"files": {}}):
            return evaluation.validate_cases(root)

    def test_routing_prompts_counted_not_base_cases(self):
        summary = self.validated_summary()
        prompts = validate_routing_prompts(load_json(ROUTING_PROMPTS), self.identities)
        self.assertEqual(summary["routing_prompts"], len(prompts))
        self.assertGreater(summary["routing_prompts"], 0)
        self.assertEqual(summary["skill_cases"], 172)
        kit = self.lab / "kit"
        shutil.copytree(ROOT / "evals", kit / "evals")
        (kit / "core/registry/catalog").mkdir(parents=True)
        shutil.copyfile(ROOT / "core/registry/catalog/skills.json", kit / "core/registry/catalog/skills.json")
        self.assertEqual(self.validated_summary(kit)["routing_prompts"], len(prompts))
        moved = kit / "evals/cases/workflow/route-prompts.json"
        shutil.move(kit / "evals/cases/routing/route-prompts.json", moved)
        with self.assertRaisesRegex(ContractError, "evals/cases/routing"):
            self.validated_summary(kit)
        shutil.move(moved, kit / "evals/cases/routing/route-prompts.json")
        shutil.copyfile(ROOT / "evals/cases/engineer/nckh-fix.json", kit / "evals/cases/routing/nckh-fix.json")
        with self.assertRaisesRegex(ContractError, "evals/cases/routing"):
            self.validated_summary(kit)
        shutil.rmtree(kit / "evals/cases/routing")
        with self.assertRaisesRegex(ContractError, "routing prompt suite missing"):
            self.validated_summary(kit)

    def test_counts_invariant_172_173_24(self):
        summary = self.validated_summary()
        self.assertEqual((summary["skill_cases"], summary["regression_cases"], summary["required_families"]),
                         (172, 173, 24))


def synthetic_case(*checks):
    return {"id": "synthetic:oracle-probe", "fixtures": [], "oracle": {"acceptance": [], "checks": list(checks)}}


if __name__ == "__main__":
    unittest.main()
