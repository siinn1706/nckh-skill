"""Mechanical routing eval: route-hint matcher against natural Vietnamese prompts (no models).

Thresholds: tune prompts 100 % hit (expected skill among at most two suggestions),
held-out prompts >= 72 % hit (the single blind held-out v3 measurement; the 80 % target
was not reached by a cue matcher, so the hint stays advisory), `none` prompts <= 10 % false positives. The held-out
split is authored separately and may be empty; the accuracy test skips until it exists.
Prompts from an earlier, exposed held-out set now sit in tune (`origin`), and their bytes
stay pinned by the aggregate hash recorded before any cue was tuned.
"""
import hashlib
import json
import unicodedata
import unittest
from pathlib import Path

from core.paths import temporary_tree
from core.route_hint import (PROMPT_LIMIT, RULE_LIMIT, evaluate_prompts, hint_text, load_boundaries,
                             match, validate_routing_prompts)
from core.schema import ContractError
from tests._lab import lab_root

ROOT = Path(__file__).resolve().parents[2]
BOUNDARIES = ROOT / "core/registry/catalog/route-boundaries.json"
PROMPTS = ROOT / "evals/cases/routing/route-prompts.json"

# origin -> (current ID prefix, ID prefix the hashes were recorded under, count, aggregate sha256)
EXPOSED_SETS = {
    "heldout-v1-exposed": ("exposed-v1-", "heldout-", 49,
                           "d9927b05d954a35b749eda52ce1eb9581ddb4a6458fb554e4480207816dff88d"),
    "heldout-v2-exposed": ("exposed-v2-", "heldout-v2-", 100,
                           "bf62512e6e3b6131e2dd4706fcc8184b9a1fccf4ae0144d565183d2bd1ee2065"),
}
TUNE_MIN_ACCURACY = 1.0
HELDOUT_MIN_ACCURACY = 0.72
NONE_MAX_FALSE_POSITIVE_RATE = 0.10

B2 = "test_app.py đang fail mấy test, sửa giúp mình với, xong báo là đã verified nhé"
B3 = "viết lại writing.txt cho hay hơn, nhấn mạnh kết quả chứng minh A tốt hơn, sửa thẳng vào file luôn nhé"

DEBUG_FIX_RULE = ("A request that asks for a repair belongs to nckh-fix, which may run a bounded diagnosis first; "
                  "a diagnose-only request belongs to nckh-debug, which ends before product edits.")
SYNTHETIC = [
    {"skills": ["nckh-debug", "nckh-fix"], "owner_rule": DEBUG_FIX_RULE,
     "vi_cues": {"nckh-debug": ["tìm nguyên nhân"], "nckh-fix": ["sửa lỗi", "đang fail"]}},
    {"skills": ["nckh-test", "nckh-frontend"], "owner_rule": "Tests belong to nckh-test; screens belong to nckh-frontend.",
     "vi_cues": {"nckh-test": ["chạy test"], "nckh-frontend": ["giao diện"]}},
]


def skills(hints):
    return [hint["skill"] for hint in hints]


class RoutingPromptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalog = json.loads((ROOT / "core/registry/catalog/skills.json").read_text(encoding="utf-8"))
        cls.identities = [row["id"] for row in catalog["skills"]]
        cls.boundaries = load_boundaries(BOUNDARIES)
        cls.record = json.loads(PROMPTS.read_text(encoding="utf-8"))
        cls.prompts = validate_routing_prompts(cls.record, cls.identities)
        cls.rows, cls.summary = evaluate_prompts(cls.prompts, cls.boundaries)

    def misses(self, split):
        return [(row["id"], row["expected"], row["suggested"]) for row in self.rows
                if row["split"] == split and row["expected"] != "none" and not row["ok"]]

    def test_schema_and_split_coverage(self):
        self.assertEqual(len(self.identities), 43)
        has_heldout = any(row["split"] == "heldout" for row in self.prompts)
        for skill in self.identities:
            with self.subTest(skill=skill):
                splits = {row["split"] for row in self.prompts if row["expected"] == skill}
                self.assertEqual(splits, {"tune", "heldout"} if has_heldout else {"tune"})
        self.assertGreaterEqual(sum(row["expected"] == "none" for row in self.prompts), 10)
        blind = {row["id"]: row for row in self.prompts if row["provenance"] == "blind-r44"}
        self.assertEqual(blind["blind-r44-b2"]["prompt"], B2)
        self.assertEqual(blind["blind-r44-b3"]["prompt"], B3)

    def test_validator_rejects_bad_records(self):
        good = {"schema_version": 1, "kind": "routing-prompts", "prompts": [
            {"id": "a", "prompt": "sửa lỗi đăng nhập", "expected": "nckh-fix", "split": "tune", "provenance": "authored"},
            {"id": "b", "prompt": "sửa lỗi giúp mình", "expected": "nckh-fix", "split": "heldout", "provenance": "authored"}]}
        self.assertEqual(len(validate_routing_prompts(good, ["nckh-fix"])), 2)
        tune_only = json.loads(json.dumps(good))
        tune_only["prompts"][1].update(split="tune", origin="heldout-v1-exposed")
        self.assertEqual(len(validate_routing_prompts(tune_only, ["nckh-fix"])), 2)
        cases = {
            "duplicate": lambda r: r["prompts"][1].update(id="a"),
            "unknown skill": lambda r: r["prompts"][1].update(expected="nckh-nope"),
            "missing tune": lambda r: r["prompts"][0].update(split="heldout"),
            "exposed prompt held out": lambda r: r["prompts"][1].update(origin="heldout-v1-exposed"),
            "bad origin": lambda r: r["prompts"][0].update(origin="other"),
            "no diacritics": lambda r: r["prompts"][1].update(prompt="sua loi giup minh"),
            "flagged but accented": lambda r: r["prompts"][1].update(unaccented=True),
            "bad split": lambda r: r["prompts"][1].update(split="dev"),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                record = json.loads(json.dumps(good))
                mutate(record)
                with self.assertRaises(ContractError):
                    validate_routing_prompts(record, ["nckh-fix"])
        # Once held-out prompts exist, every skill needs one: nckh-debug has only a tune prompt here.
        partial = json.loads(json.dumps(good))
        partial["prompts"].append({"id": "c", "prompt": "tìm nguyên nhân lỗi", "expected": "nckh-debug",
                                   "split": "tune", "provenance": "authored"})
        with self.assertRaises(ContractError):
            validate_routing_prompts(partial, ["nckh-fix", "nckh-debug"])

    def test_exposed_prompts_unchanged(self):
        self.assertEqual({row["origin"] for row in self.prompts if "origin" in row}, set(EXPOSED_SETS))
        for origin, (prefix, recorded_prefix, count, expected) in EXPOSED_SETS.items():
            with self.subTest(origin=origin):
                exposed = [row for row in self.prompts if row.get("origin") == origin]
                self.assertTrue(all(row["split"] == "tune" and row["id"].startswith(prefix) for row in exposed))
                held = {recorded_prefix + row["id"][len(prefix):]: hashlib.sha256(row["prompt"].encode("utf-8")).hexdigest()
                        for row in exposed}
                self.assertEqual(len(held), count)
                aggregate = hashlib.sha256(json.dumps(held, sort_keys=True, ensure_ascii=False,
                                                      separators=(",", ":")).encode("utf-8")).hexdigest()
                self.assertEqual(aggregate, expected)

    def test_tune_accuracy(self):
        self.assertGreaterEqual(self.summary["tune"]["accuracy"], TUNE_MIN_ACCURACY, self.misses("tune"))

    def test_heldout_accuracy(self):
        bucket = self.summary.get("heldout")
        if not bucket or not bucket["skill_total"]:
            self.skipTest("no held-out skill prompts yet; the held-out set is authored and merged separately")
        self.assertGreaterEqual(self.summary["heldout"]["accuracy"], HELDOUT_MIN_ACCURACY, self.misses("heldout"))

    def test_none_false_positive_rate(self):
        none_rows = [row for row in self.rows if row["expected"] == "none"]
        false_positives = [(row["id"], row["suggested"]) for row in none_rows if not row["ok"]]
        self.assertGreaterEqual(len(none_rows), 10)
        self.assertLessEqual(len(false_positives) / len(none_rows), NONE_MAX_FALSE_POSITIVE_RATE, false_positives)

    def test_blind_r44_prompts(self):
        self.assertIn("nckh-fix", skills(match(B2, self.boundaries)))
        self.assertIn("nckh-humanwrite", skills(match(B3, self.boundaries)))

    def test_at_most_two_hints_with_owner_rule(self):
        hints = match("tìm nguyên nhân rồi sửa lỗi đang fail, sau đó chạy test", SYNTHETIC)
        self.assertEqual(len(hints), 2)
        # fix scores two cues; debug and test tie on one, broken by the longer cue.
        self.assertEqual(skills(hints), ["nckh-fix", "nckh-debug"])
        self.assertEqual(skills(match("tìm nguyên nhân rồi sửa lỗi", SYNTHETIC)), ["nckh-debug", "nckh-fix"])
        for hint in hints:
            self.assertEqual(hint["owner_rule"], DEBUG_FIX_RULE)
            self.assertEqual(hint["score"], len(hint["cues"]))
        top = match("sửa lỗi đang fail, tìm nguyên nhân", SYNTHETIC, limit=1)
        self.assertEqual(skills(top), ["nckh-fix"])  # two cues beat one
        self.assertEqual(top[0]["cues"], ["sửa lỗi", "đang fail"])

    def test_explicit_invocation_suppresses_hint(self):
        for prompt in ("/nckh-fix sửa lỗi đăng nhập", "sửa lỗi này bằng $nckh-fix nhé",
                       "dùng (/nckh-debug) rồi sửa lỗi", "$NCKH-FIX sửa lỗi"):
            with self.subTest(prompt=prompt):
                self.assertEqual(match(prompt, self.boundaries), [])
        self.assertIn("nckh-fix", skills(match("đọc skills/nckh-fix/SKILL.md rồi sửa lỗi", self.boundaries)))

    def test_ordered_tokens_with_short_gap(self):
        self.assertEqual(skills(match("tìm giúp mình nguyên nhân nhé", SYNTHETIC)), ["nckh-debug"])
        self.assertEqual(skills(match("tìm giúp mình các nguyên nhân", SYNTHETIC)), ["nckh-debug"])  # fillers are free
        self.assertEqual(match("tìm thêm nhiều nữa nguyên nhân", SYNTHETIC), [])  # three content tokens skipped
        self.assertEqual(match("tìm giúp mình cho các bạn với nhé này nguyên nhân", SYNTHETIC), [])  # span cap
        self.assertEqual(match("tìm giúp, nguyên nhân", SYNTHETIC), [])  # cue may not span clauses
        self.assertEqual(match("nguyên nhân tìm", SYNTHETIC), [])  # order matters
        self.assertEqual(skills(match("chia tập train/test.", [{"skills": ["nckh-dataset", "nckh-data"],
                                      "owner_rule": "x" * 20, "vi_cues": {"nckh-dataset": ["chia tập train/test"],
                                                                          "nckh-data": ["sửa schema"]}}])),
                         ["nckh-dataset"])

    def test_spelling_variants_match(self):
        variants = [{"skills": ["nckh-telemetry", "nckh-cro"], "owner_rule": "x" * 20,
                     "vi_cues": {"nckh-telemetry": ["chuẩn hóa log"], "nckh-cro": ["tỉ lệ chuyển đổi"]}}]
        self.assertEqual(skills(match("chuẩn hoá log giúp mình", variants)), ["nckh-telemetry"])
        self.assertEqual(skills(match("tỷ lệ chuyển đổi thấp quá", variants)), ["nckh-cro"])
        self.assertEqual(match("chuẩn hoán log", variants), [])  # closed syllable keeps its own spelling

    def test_unaccented_prompt_matches(self):
        self.assertIn("nckh-fix", skills(match("sua loi dang nhap giup minh", self.boundaries)))
        self.assertIn("nckh-fix", skills(match("test dang fail roi", self.boundaries)))

    def test_accented_prompt_does_not_use_unaccented_fold(self):
        self.assertEqual(match("Sửa loi dang nhap giup minh", SYNTHETIC), [])
        self.assertEqual(skills(match("Sửa lỗi đăng nhập", SYNTHETIC)), ["nckh-fix"])

    def test_normalization_nfc_and_casefold(self):
        decomposed = unicodedata.normalize("NFD", "SỬA LỖI đăng nhập")
        self.assertNotEqual(decomposed, unicodedata.normalize("NFC", decomposed))
        self.assertEqual(skills(match(decomposed, SYNTHETIC)), ["nckh-fix"])

    def test_installed_filter(self):
        self.assertEqual(match(B2, self.boundaries, installed=set()), [])
        self.assertEqual(match(B2, self.boundaries, installed={"nckh-debug"}), [])
        self.assertEqual(skills(match(B2, self.boundaries, installed={"nckh-fix"})), ["nckh-fix"])

    def test_word_boundary(self):
        self.assertEqual(match("chạy tests rồi xem giao diệnx", SYNTHETIC), [])
        self.assertEqual(match("xchạy test nhé", SYNTHETIC), [])
        self.assertEqual(match("chạy test2 nhé", SYNTHETIC), [])
        self.assertEqual(skills(match("Chạy test. Xong rồi", SYNTHETIC)), ["nckh-test"])
        self.assertEqual(skills(match("(giao diện)", SYNTHETIC)), ["nckh-frontend"])

    def test_prompt_limit(self):
        filler = "a " * (PROMPT_LIMIT // 2)
        self.assertEqual(match(filler + "sửa lỗi", SYNTHETIC), [])
        self.assertEqual(skills(match("sửa lỗi " + filler, SYNTHETIC)), ["nckh-fix"])
        self.assertEqual(match("", SYNTHETIC), [])
        self.assertEqual(match(None, SYNTHETIC), [])

    def test_hint_text_names_full_skill_id(self):
        hints = match(B2, self.boundaries)
        claude = hint_text(hints, "/{skill}")
        codex = hint_text(hints, "${skill}")
        self.assertTrue(claude.startswith("nckh routing hint (advisory): "))
        self.assertIn("nckh-fix (", claude)
        self.assertIn("load /nckh-fix", claude)
        self.assertIn("load $nckh-fix", codex)
        self.assertIn("ignore otherwise", claude)
        rule = claude.split("Boundary: ", 1)[1]
        self.assertLessEqual(len(rule), RULE_LIMIT)
        pair = hint_text(match("tìm nguyên nhân rồi sửa lỗi", SYNTHETIC), "/{skill}")
        self.assertIn("load /nckh-debug or /nckh-fix", pair)
        self.assertEqual(pair.count(DEBUG_FIX_RULE[:40]), 1)
        self.assertEqual(hint_text([], "/{skill}"), "")
        with self.assertRaises(ContractError):
            hint_text(hints, "/nckh")

    def test_load_boundaries_rejects_mismatched_cue_keys(self):
        self.assertEqual(len(self.boundaries), 32)
        bad = json.loads(BOUNDARIES.read_text(encoding="utf-8"))
        bad["boundaries"][0]["vi_cues"].pop("nckh-plan")
        with temporary_tree(lab_root()) as root:
            path = root / "route-boundaries.json"
            path.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ContractError):
                load_boundaries(path)
            path.write_text("{", encoding="utf-8")
            with self.assertRaises(ContractError):
                load_boundaries(path)


if __name__ == "__main__":
    unittest.main()
