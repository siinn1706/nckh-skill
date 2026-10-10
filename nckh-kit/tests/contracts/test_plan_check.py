from tests._lab import lab_root
import shutil
import unittest
from pathlib import Path

from core.paths import temporary_tree
from core.plan_check import SECTION_ALIASES, check_plan


FIXTURES = Path(__file__).resolve().parent / "fixtures" / "plans"

VI_PLAN = """---
title: "Sửa hàm chuyển đổi"
status: pending
---

# Sửa hàm chuyển đổi

## Các giai đoạn

| Giai đoạn | Nội dung | Trạng thái |
|---|---|---|
| 1 | [Tái hiện lỗi](./phase-01-tai-hien-loi.md) | hoàn thành |
| 2 | [Sửa và kiểm chứng](./phase-02-sua-va-kiem-chung.md) | đang chờ |
"""

VI_PHASE = """---
phase: {number}
status: {status}
{receipt}---

# Giai đoạn {number}

## Yêu cầu

- Ba test trong `test_app.py` đều pass.

## Tệp liên quan

- `app.py`

## Các bước thực hiện

1. Chạy test một lần, ghi exit riêng.

## Kiểm chứng

- Lệnh test exit 0.

## Rủi ro và hoàn tác

Khôi phục `app.py` từ preimage.
"""


class PlanCheckTests(unittest.TestCase):
    def setUp(self):
        self.tree = temporary_tree(lab_root())
        self.root = self.tree.__enter__()
        self.addCleanup(self.tree.__exit__, None, None, None)

    def rules(self, result):
        return {finding["rule"] for finding in result["findings"]}

    def copy_fixture(self, name):
        target = self.root / name
        shutil.copytree(FIXTURES / name, target)
        return target

    def test_lab02_single_file_plan_fails(self):
        result = check_plan(FIXTURES / "lab02-single-file")
        self.assertEqual(result["verdict"], "FAILED")
        self.assertTrue({"single-file-plan", "phase-link", "status-without-receipt"} <= self.rules(result),
                        result["findings"])
        markers = [f["line"] for f in result["findings"] if f["rule"] == "status-without-receipt"]
        self.assertEqual(len(markers), 5, "four completed stages plus the VERIFIED line")

    def test_two_phase_plan_with_sections_verifies(self):
        result = check_plan(FIXTURES / "valid-two-phase")
        self.assertEqual(result, {"verdict": "VERIFIED", "findings": []})
        plan = self.copy_fixture("valid-two-phase")
        phase = plan / "phase-02-repair-and-verify.md"
        phase.write_text(phase.read_text(encoding="utf-8").replace("## Risk & rollback", "## Notes"),
                         encoding="utf-8")
        result = check_plan(plan)
        self.assertEqual(self.rules(result), {"phase-sections"})
        self.assertIn("risk-rollback", result["findings"][0]["message"])

    def test_completed_status_without_receipt_fails(self):
        result = check_plan(FIXTURES / "status-without-receipt")
        self.assertEqual(result["verdict"], "FAILED")
        self.assertEqual(self.rules(result), {"status-without-receipt"})
        self.assertEqual({f["path"] for f in result["findings"]},
                         {"plan.md", "phase-01-reproduce-failure.md"})
        plan = self.copy_fixture("status-without-receipt")
        (plan / "reports").mkdir()
        (plan / "reports/phase-01-report.md").write_text("Receipt for phase 1\n", encoding="utf-8")
        phase = plan / "phase-01-reproduce-failure.md"
        phase.write_text(phase.read_text(encoding="utf-8").replace(
            "status: done\n", "status: done\nreceipt: reports/phase-01-report.md\n"), encoding="utf-8")
        self.assertEqual(check_plan(plan), {"verdict": "VERIFIED", "findings": []})
        plan = self.copy_fixture("valid-two-phase")
        (plan / "reports/phase-01-receipt.json").unlink()
        result = check_plan(plan)
        self.assertIn("status-without-receipt", self.rules(result))
        self.assertIn("broken-link", self.rules(result))

    def test_broken_relative_link_fails(self):
        plan = self.copy_fixture("valid-two-phase")
        with (plan / "plan.md").open("a", encoding="utf-8") as stream:
            stream.write("\nSee [notes](./reports/missing-notes.md) and `[code](./not-a-link.md)`.\n"
                         "```\n[fenced](./also-not-a-link.md)\n```\n")
        result = check_plan(plan)
        self.assertEqual(self.rules(result), {"broken-link"})
        self.assertEqual(len(result["findings"]), 1)
        self.assertIn("missing-notes.md", result["findings"][0]["message"])

    def test_vietnamese_section_aliases_accepted(self):
        plan = self.root / "kế-hoạch"
        (plan / "reports").mkdir(parents=True)
        (plan / "plan.md").write_text(VI_PLAN, encoding="utf-8")
        (plan / "reports/bien-nhan-01.json").write_text("{}", encoding="utf-8")
        (plan / "phase-01-tai-hien-loi.md").write_text(VI_PHASE.format(
            number=1, status="hoàn thành", receipt="receipt: reports/bien-nhan-01.json\n"), encoding="utf-8")
        (plan / "phase-02-sua-va-kiem-chung.md").write_text(VI_PHASE.format(
            number=2, status="đang chờ", receipt=""), encoding="utf-8")
        self.assertEqual(check_plan(plan), {"verdict": "VERIFIED", "findings": []})
        for group, aliases in SECTION_ALIASES.items():
            self.assertTrue(any(not alias.isascii() for alias in aliases), group)
        (plan / "phase-01-tai-hien-loi.md").write_text(VI_PHASE.format(
            number=1, status="hoàn thành", receipt=""), encoding="utf-8")
        self.assertEqual(self.rules(check_plan(plan)), {"status-without-receipt"})

    def test_receipts_must_stay_under_the_plans_root(self):
        plans = self.root / "kế-hoạch"
        plan = plans / "sửa-lỗi"
        shutil.copytree(FIXTURES / "status-without-receipt", plan)
        outside = self.root / "ngoài.txt"
        outside.write_text("not a receipt\n", encoding="utf-8")
        (plans / "chung").mkdir()
        (plans / "chung/biên-nhận.json").write_text("{}", encoding="utf-8")
        phase = plan / "phase-01-reproduce-failure.md"
        original = phase.read_text(encoding="utf-8")
        rooted = outside.as_posix()[len(outside.drive):]
        for receipt, verdict in ((rooted, "FAILED"), ("../../ngoài.txt", "FAILED"),
                                 ("..\\..\\ngoài.txt", "FAILED"), ("../chung/biên-nhận.json", "VERIFIED")):
            with self.subTest(receipt=receipt):
                phase.write_text(original.replace("status: done\n", f"status: done\nreceipt: {receipt}\n"),
                                 encoding="utf-8")
                result = check_plan(plan)
                self.assertEqual(result["verdict"], verdict, result["findings"])
                if verdict == "FAILED":
                    self.assertEqual(self.rules(result), {"status-without-receipt"})
        phase.write_text(original.replace("status: done\n", "status: done\nreceipt: ../chung/biên-nhận.json\n")
                         + f"\nStatus: done `{rooted}`\n", encoding="utf-8")
        result = check_plan(plan)
        self.assertEqual(self.rules(result), {"status-without-receipt"})
        self.assertEqual({f["path"] for f in result["findings"]}, {"phase-01-reproduce-failure.md"})


if __name__ == "__main__":
    unittest.main()
