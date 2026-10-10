"""Routing contract between easily confused sibling skills.

`core/registry/catalog/route-boundaries.json` is the single source for sibling
pairs, the rule that decides the owner and the Vietnamese activation cues. Each
per-kit test checks only the SKILL.md files of that kit, so a kit can be brought
into compliance without touching the others.
"""

import importlib
import json
import re
import unicodedata
import unittest
from pathlib import Path

from core.build import LINK, SCRIPT_REQUIREMENTS, closure, load_json, validate_catalog
from core.schema import validate


ROOT = Path(__file__).resolve().parents[2]
BOUNDARIES = "core/registry/catalog/route-boundaries.json"
SCHEMA = "core/contracts/route-boundaries.schema.json"
MAX_DESCRIPTION = 400
EXECUTION = "core/workflows/execution.md"
HANDOFF = "core/workflows/review-and-handoff.md"
PRESERVATION = "core/policies/preservation-policy.md"
EVIDENCE = "core/policies/evidence-policy.md"
VISUAL_ASSETS = "core/policies/visual-asset-policy.md"
ATTEMPT_STATUSES = "<attempt-statuses>"

# Shared sections, the validators named on their closing "Validator:" line and the
# terms each section must keep. A ".py" name is a script under scripts/; a dotted
# name is a module attribute. ATTEMPT_STATUSES expands to the claim schema enum.
SHARED_SECTIONS = {
    (EXECUTION, "Plan artifact"): (("check-plan.py",), ("plan.md", "phase-NN-slug.md", "receipt")),
    (EXECUTION, "Command discipline"): (("check-receipt.py",),
                                        ("$LASTEXITCODE", "$?", "command_results", "segment_exit_statuses")),
    (EXECUTION, "Attempt ledger"): (("check-receipt.py",), (ATTEMPT_STATUSES, "plan directory", "ask once")),
    (EXECUTION, "Host shell robustness"): (("check-receipt.py",),
                                           ("python -X utf8", "PYTHONIOENCODING=utf-8", "python -c", "Set-Content")),
    (HANDOFF, "Handoff packet"): (("check-receipt.py",), ("authority reference", "next action and owner", "not-durable")),
    (PRESERVATION, "Input preservation"): (("check-receipt.py",), ("read-only", "new path", "preimage", "BOM", "/tmp")),
    (EVIDENCE, "Attempt status"): (("core.ledger.validate_claim",), ("attempt_status", "unverified")),
    (VISUAL_ASSETS, "Purpose preflight"): (("core.guards.check_visual_purpose", "check-visual-engine.py"),
                                           ("visual_purpose",)),
    (VISUAL_ASSETS, "Marketing and brand assets"): (("check-visual-engine.py",), ("unavailable", "pending", "brief")),
}

# Core-loop skills: the shared sections each SKILL.md links by anchor and the
# validator scripts it links so the build packages them into the skill closure.
CORE_LOOP_LINKS = {
    "nckh-plan": ({(EXECUTION, "Plan artifact")}, ("check-plan.py",)),
    "nckh-cook": ({(EXECUTION, "Command discipline"), (EXECUTION, "Attempt ledger"),
                   (EXECUTION, "Host shell robustness"), (PRESERVATION, "Input preservation")}, ("check-receipt.py",)),
    "nckh-handoff": ({(EXECUTION, "Attempt ledger"), (HANDOFF, "Handoff packet")}, ("check-receipt.py",)),
    "nckh-review": ({(EXECUTION, "Attempt ledger")}, ("check-receipt.py", "check-plan.py")),
}

# Boundaries that must stay encoded; adding more is allowed, removing these is not.
REQUIRED_GROUPS = (
    ("nckh-plan", "nckh-research", "nckh-method"), ("nckh-debug", "nckh-fix"),
    ("nckh-test", "nckh-debug"), ("nckh-data", "nckh-dataset", "nckh-statistics"),
    ("nckh-review", "nckh-code-review"), ("nckh-git", "nckh-code-review"),
    ("nckh-security", "nckh-code-review"), ("nckh-devops", "nckh-aiops"),
    ("nckh-debug", "nckh-aiops"), ("nckh-context", "nckh-handoff"),
    ("nckh-write", "nckh-humanwrite", "nckh-paperwrite"), ("nckh-docs", "nckh-write"),
    ("nckh-copy", "nckh-humanwrite"), ("nckh-copy", "nckh-content"), ("nckh-cro", "nckh-seo"),
    ("nckh-content", "nckh-social", "nckh-campaign"), ("nckh-email", "nckh-campaign"),
    ("nckh-launch", "nckh-campaign"), ("nckh-brand", "nckh-social"),
    ("nckh-analytics", "nckh-experiment"), ("nckh-experiment", "nckh-statistics"),
    ("nckh-market-research", "nckh-research"), ("nckh-marketing-plan", "nckh-plan"),
    ("nckh-scout", "nckh-plan"), ("nckh-frontend", "nckh-visuals", "nckh-brand"),
    ("nckh-xia", "nckh-plan"),
)

# Handoff phrasing. "<X> owns ..." must name X by full ID. "<X/Y> own ..." is the
# plural form of the same sentence; a bare "own" after a pronoun ("their own") is
# not a handoff. "... remain(s) <owner>" names the owner after the verb, so the
# complement is checked when it is a possessive, a slash list or a bare skill name
# that ends the clause.
OWNS = re.compile(r"(\S+)\s+owns\b")
PLURAL_OWN = re.compile(r"(\S+/\S+)\s+own\b")
REMAINS = re.compile(r"\bremains?\s+(\S+)")
EDGE = "`*\"'()[],.;:"


def _fold(text):
    return unicodedata.normalize("NFC", text).casefold()


def _mentions(text, skill_id):
    return re.search(rf"(?<![\w-]){re.escape(skill_id)}(?![\w-])", text) is not None


def _description(text, rel):
    match = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not match:
        raise AssertionError(f"{rel}: missing front matter")
    for line in match.group(1).splitlines():
        if line.startswith("description:"):
            value = line[len("description:"):].strip()
            return json.loads(value) if value.startswith('"') else value.strip("'")
    raise AssertionError(f"{rel}: front matter has no description")


def _sections(text):
    """Map each level-2 heading to the stripped, non-empty lines under it."""
    sections, current = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            current = sections.setdefault(line[3:].strip(), [])
        elif current is not None and line.strip():
            current.append(line.strip())
    return sections


def _anchor(heading):
    return re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")


def _short_owner(token, short_names):
    """Return the bare skill name a token refers to without its nckh- ID, if any."""
    for part in token.strip(EDGE).split("/"):
        bare = re.sub(r"['’]s$", "", part.strip(EDGE)).lower()
        if bare in short_names and not part.strip(EDGE).startswith("nckh-"):
            return part.strip(EDGE)
    return None


class SkillRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = validate_catalog(load_json(ROOT / "core/registry/catalog/skills.json"))
        cls.data = load_json(ROOT / BOUNDARIES)
        cls.skill_text = {skill_id: (ROOT / entry["path"] / "SKILL.md").read_text(encoding="utf-8")
                          for skill_id, entry in cls.catalog.items()}
        cls.short_names = {skill_id[len("nckh-"):] for skill_id in cls.catalog}

    def _cues(self):
        cues = {}
        for boundary in self.data["boundaries"]:
            for skill_id, values in boundary["vi_cues"].items():
                cues.setdefault(skill_id, []).extend(values)
        return cues

    def _violations(self, kits):
        owned = {skill_id for skill_id, entry in self.catalog.items() if entry["kit"] in kits}
        cues = self._cues()
        found = []
        for boundary in self.data["boundaries"]:
            for skill_id in boundary["skills"]:
                if skill_id not in owned:
                    continue
                for other in boundary["skills"]:
                    if other != skill_id and not _mentions(self.skill_text[skill_id], other):
                        found.append(f"{skill_id}: SKILL.md does not name sibling {other} "
                                     f"(rule: {boundary['owner_rule']})")
        for skill_id in sorted(owned):
            text = self.skill_text[skill_id]
            rel = self.catalog[skill_id]["path"] + "/SKILL.md"
            description = _description(text, rel)
            if len(description) > MAX_DESCRIPTION:
                found.append(f"{skill_id}: description has {len(description)} characters (limit {MAX_DESCRIPTION})")
            folded = _fold(description)
            if not any(_fold(cue) in folded for cue in cues.get(skill_id, [])):
                found.append(f"{skill_id}: description has no Vietnamese cue from {BOUNDARIES}")
            for number, line in enumerate(text.splitlines(), 1):
                for pattern in (OWNS, PLURAL_OWN):
                    for match in pattern.finditer(line):
                        subject = match.group(1).strip(EDGE)
                        if any(not part.strip(EDGE).startswith("nckh-") for part in subject.split("/")):
                            found.append(f"{rel}:{number}: handoff '{match.group(0)}' must name the owner by nckh- ID")
                for match in REMAINS.finditer(line):
                    token = match.group(1)
                    bare = token.strip(EDGE)
                    possessive_or_list = "/" in bare or re.search(r"['’]s$", bare)
                    ends_clause = token != bare and token[-1] in ",.;:"
                    if (possessive_or_list or ends_clause) and _short_owner(token, self.short_names):
                        found.append(f"{rel}:{number}: handoff '{match.group(0)}' must name the owner by nckh- ID")
        return found

    def _assert_clean(self, kits):
        found = self._violations(kits)
        if found:
            self.fail(f"{len(found)} routing violation(s) for kits {sorted(kits)}:\n" + "\n".join(found))

    def test_route_boundaries_schema_and_ids(self):
        schema = load_json(ROOT / SCHEMA)
        validate(self.data, schema)
        groups = []
        for index, boundary in enumerate(self.data["boundaries"]):
            where = f"boundaries[{index}]"
            skills = boundary["skills"]
            self.assertLessEqual(len(skills), 3, where)
            self.assertEqual(len(skills), len(set(skills)), f"{where}: duplicate skill")
            unknown = set(skills) - self.catalog.keys()
            self.assertFalse(unknown, f"{where}: unknown skill IDs {sorted(unknown)}")
            self.assertNotIn(frozenset(skills), groups, f"{where}: duplicate boundary")
            groups.append(frozenset(skills))
            for skill_id in skills:
                self.assertTrue(_mentions(boundary["owner_rule"], skill_id),
                                f"{where}: owner_rule must name {skill_id}")
            cues = boundary["vi_cues"]
            self.assertEqual(set(cues), set(skills), f"{where}: vi_cues keys must equal skills")
            seen = {}
            for skill_id, values in cues.items():
                self.assertIsInstance(values, list, f"{where}.{skill_id}")
                self.assertTrue(values, f"{where}.{skill_id}: no cues")
                for cue in values:
                    self.assertIsInstance(cue, str, f"{where}.{skill_id}")
                    self.assertEqual(cue, cue.strip(), f"{where}.{skill_id}: untrimmed cue")
                    self.assertTrue(any(ord(char) > 127 and char.isalpha() for char in cue),
                                    f"{where}.{skill_id}: cue {cue!r} lacks Vietnamese diacritics")
                    self.assertNotIn(_fold(cue), seen, f"{where}: cue {cue!r} is shared by two siblings")
                    seen[_fold(cue)] = skill_id
        for required in REQUIRED_GROUPS:
            self.assertIn(frozenset(required), groups, f"required boundary missing: {required}")
        uncued = self.catalog.keys() - self._cues().keys()
        self.assertFalse(uncued, f"skills without any Vietnamese cue: {sorted(uncued)}")

    def test_shared_contracts_name_their_validators(self):
        claim = load_json(ROOT / "core/contracts/claim.schema.json")
        statuses = claim["properties"]["attempt_status"]["enum"]
        texts = {}
        for (rel, heading), (validators, terms) in SHARED_SECTIONS.items():
            where = f"{rel} ## {heading}"
            if rel not in texts:
                texts[rel] = _sections((ROOT / rel).read_text(encoding="utf-8"))
            lines = texts[rel].get(heading)
            self.assertTrue(lines, f"{where}: section missing or empty")
            closing = lines[-1]
            self.assertTrue(closing.startswith("Validator:"), f"{where}: must end with a Validator: line")
            for name in validators:
                self.assertIn(f"`{name}", closing, f"{where}: validator {name} not named")
                if name.endswith(".py"):
                    self.assertTrue((ROOT / "scripts" / name).is_file(), f"{where}: scripts/{name} missing")
                else:
                    module, attribute = name.rsplit(".", 1)
                    self.assertTrue(callable(getattr(importlib.import_module(module), attribute, None)),
                                    f"{where}: {name} is not callable")
            body = " ".join(lines)
            for term in terms:
                for expected in (statuses if term == ATTEMPT_STATUSES else [term]):
                    self.assertIn(expected, body, f"{where}: missing {expected!r}")

    def test_core_loop_skills_link_execution_sections(self):
        for skill_id, (sections, scripts) in CORE_LOOP_LINKS.items():
            skill_dir = ROOT / self.catalog[skill_id]["path"]
            targets = set()
            for href in LINK.findall(self.skill_text[skill_id]):
                path, _, fragment = href.partition("#")
                targets.add(((skill_dir / path).resolve().relative_to(ROOT).as_posix(), fragment))
            for rel, heading in sections:
                self.assertIn(heading, _sections((ROOT / rel).read_text(encoding="utf-8")), f"{rel}: no ## {heading}")
                self.assertIn((rel, _anchor(heading)), targets, f"{skill_id}: no link to {rel}#{_anchor(heading)}")
            members = {path.relative_to(ROOT).as_posix()
                       for path in closure(ROOT, [p for p in skill_dir.rglob("*") if p.is_file()])}
            for name in scripts:
                script = f"scripts/{name}"
                self.assertIn((script, ""), targets, f"{skill_id}: SKILL.md does not link {script}")
                missing = {script, *SCRIPT_REQUIREMENTS[script]} - members
                self.assertFalse(missing, f"{skill_id}: closure lacks {sorted(missing)}")

    def test_core_routing_contract(self):
        self._assert_clean({"core", "tooling"})

    def test_engineer_routing_contract(self):
        self._assert_clean({"engineer"})

    def test_marketing_routing_contract(self):
        self._assert_clean({"marketing"})


if __name__ == "__main__":
    unittest.main()
