"""Advisory skill hints from Vietnamese routing cues.

The matcher reads `vi_cues` from route-boundaries.json and suggests at most a few
skills whose cues occur in a user prompt. It never invokes a skill and never
blocks; callers decide how to surface the hint. Standard library only so the
module can run inside the hook closure.
"""

import json
import re
import unicodedata
from pathlib import Path

from core.schema import ContractError, validate_record

PROMPT_LIMIT = 4000
RULE_LIMIT = 200
DEFAULT_LIMIT = 2
NONE = "none"
SPLITS = ("tune", "heldout")

# An explicit `/nckh-x` or `$nckh-x` token anywhere in the prompt means the user
# already chose a skill; the token must not continue a word or path segment.
_EXPLICIT = re.compile(r"(?:^|[^\w/$-])[/$]nckh-[a-z0-9]", re.IGNORECASE)
# Extra content tokens a multi-word cue may skip in total, e.g. "tìm (nốt) nguyên nhân".
MAX_GAP = 2
# Politeness and determiner words ("giúp mình", "các", "này") are skipped for free,
# up to MAX_SPAN skipped tokens overall, so "tìm giúp mình các bài báo" still
# matches "tìm bài báo" without widening the gap for content words.
MAX_SPAN = 6
FILLER = frozenset({"giúp", "giùm", "dùm", "hộ", "mình", "tôi", "em", "bạn", "cho", "các", "những", "mọi",
                    "một", "mấy", "này", "đó", "kia", "lại", "hãy", "cứ", "nhé", "với"})
_WORD = r"[\ẁ-ͯ]+"
_TOKEN = re.compile(rf"(?P<word>{_WORD}(?:[/.'+-]{_WORD})*)|[,.;:!?()\[\]{{}}\"\n]")


def _canonical_spelling():
    """Map spelling variants Vietnamese users type interchangeably onto one form.

    Tone placement in open `oa`/`oe`/`uy` syllables (`hoá`/`hóa`, `khoẻ`/`khỏe`)
    and syllable-final `y`/`i` after a consonant (`tỷ`/`tỉ`, `kỹ`/`kĩ`). Both the
    prompt and the cues pass through the same mapping, so only consistency matters.
    """
    tones = "̣̀́̉̃"
    placement = {}
    for first, second in (("o", "a"), ("o", "e"), ("u", "y")):
        for tone in tones:
            placement[first + unicodedata.normalize("NFC", second + tone)] = (
                unicodedata.normalize("NFC", first + tone) + second)
    final_y = {unicodedata.normalize("NFC", "y" + tone): unicodedata.normalize("NFC", "i" + tone)
               for tone in ("", *tones)}
    return placement, final_y


_PLACEMENT, _FINAL_Y = _canonical_spelling()
_PLACEMENT_RE = re.compile("(" + "|".join(map(re.escape, _PLACEMENT)) + r")(?!\w)")
_FINAL_Y_RE = re.compile(r"(?<!\w)([bcdđghklmnpqrstvx]+)(" + "|".join(map(re.escape, _FINAL_Y)) + r")(?!\w)")


def _normalize(text):
    text = unicodedata.normalize("NFC", text).casefold()
    text = _PLACEMENT_RE.sub(lambda m: _PLACEMENT[m.group(1)], text)
    return _FINAL_Y_RE.sub(lambda m: m.group(1) + _FINAL_Y[m.group(2)], text)


def _fold(text):
    """Drop combining marks and map đ to d on already-normalized text."""
    decomposed = unicodedata.normalize("NFD", text.replace("đ", "d").replace("Đ", "D"))
    return unicodedata.normalize("NFC", "".join(c for c in decomposed if not unicodedata.combining(c)))


def has_diacritics(text):
    """True when the text carries any Vietnamese diacritic (combining mark or đ)."""
    normalized = _normalize(text)
    return _fold(normalized) != normalized


def _tokens(text):
    """Split normalized text into word tokens, each tagged with its clause number.

    A token is a run of letters, digits, marks and underscores, optionally joined by
    `/ . ' + -` (so `train/test`, `ci/cd`, `test_app.py` stay whole). Clause
    punctuation starts a new clause; other characters only separate tokens.
    """
    result = []
    clause = 0
    for found in _TOKEN.finditer(text):
        if found.group("word"):
            result.append((found.group("word"), clause))
        else:
            clause += 1
    return result


def _index(tokens):
    positions = {}
    for position, (token, _) in enumerate(tokens):
        positions.setdefault(token, []).append(position)
    return positions


def _occurs(cue_tokens, tokens, positions, filler):
    """True when cue tokens appear in order inside one clause, skipping at most MAX_GAP
    non-filler tokens and MAX_SPAN tokens overall.

    Whole-token comparison gives the word boundary; for a fixed start the earliest
    next occurrence skips the fewest tokens, so a greedy scan is exact.
    """
    if not cue_tokens:
        return False
    for start in positions.get(cue_tokens[0], ()):
        clause = tokens[start][1]
        current = start
        gap = span = 0
        for token in cue_tokens[1:]:
            following = next((p for p in positions.get(token, ()) if p > current), None)
            if following is None or tokens[following][1] != clause:
                break
            skipped = [word for word, _ in tokens[current + 1:following]]
            span += len(skipped)
            gap += sum(word not in filler for word in skipped)
            if gap > MAX_GAP or span > MAX_SPAN:
                break
            current = following
        else:
            return True
    return False


_FOLDED_FILLER = frozenset(_fold(word) for word in FILLER)


def explicit_invocation(prompt):
    return _EXPLICIT.search(prompt[:PROMPT_LIMIT]) is not None


def load_boundaries(path):
    """Read route-boundaries.json, validate it and return the boundary list."""
    try:
        record = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"route boundaries unreadable: {path}: {exc}") from exc
    validate_record("route-boundaries", record)
    for index, boundary in enumerate(record["boundaries"]):
        cues = boundary["vi_cues"]
        if not isinstance(cues, dict) or set(cues) != set(boundary["skills"]):
            raise ContractError(f"$.boundaries[{index}].vi_cues: keys must equal skills")
        for skill, values in cues.items():
            if (not isinstance(values, list) or not values
                    or not all(isinstance(cue, str) and cue.strip() for cue in values)):
                raise ContractError(f"$.boundaries[{index}].vi_cues.{skill}: non-empty cue strings required")
    return record["boundaries"]


def match(prompt, boundaries, *, installed=None, limit=DEFAULT_LIMIT):
    """Return up to `limit` hints `[{skill, cues, score, owner_rule}]`, best first.

    Prompt and cues share one spelling canonicalization. A cue matches when its
    tokens occur in order within one clause, skipping at most MAX_GAP non-filler
    tokens (MAX_SPAN overall). Score is the number of distinct cues found; ties
    go to the longer matched cue, then to the skill ID. `installed=None` disables the
    installed-skill filter.
    """
    if not isinstance(prompt, str) or not prompt.strip() or limit < 1:
        return []
    text = prompt[:PROMPT_LIMIT]
    if explicit_invocation(text):
        return []
    haystack = _normalize(text)
    unaccented = not has_diacritics(haystack)
    if unaccented:
        haystack = _fold(haystack)
    tokens = _tokens(haystack)
    positions = _index(tokens)
    filler = _FOLDED_FILLER if unaccented else FILLER
    found = {}  # skill -> {"cues": [original cue, ...], "boundaries": {index: count}}
    for index, boundary in enumerate(boundaries):
        for skill, cues in boundary["vi_cues"].items():
            if installed is not None and skill not in installed:
                continue
            for cue in cues:
                needle = _normalize(cue)
                if unaccented:
                    needle = _fold(needle)
                if not _occurs([token for token, _ in _tokens(needle)], tokens, positions, filler):
                    continue
                entry = found.setdefault(skill, {"cues": [], "boundaries": {}})
                if cue not in entry["cues"]:
                    entry["cues"].append(cue)
                entry["boundaries"][index] = entry["boundaries"].get(index, 0) + 1
    ranked = sorted(found, key=lambda skill: (-len(found[skill]["cues"]),
                                              -max(len(cue) for cue in found[skill]["cues"]),
                                              skill))[:limit]
    chosen = set(ranked)
    hints = []
    for skill in ranked:
        counts = found[skill]["boundaries"]
        # Prefer the boundary that also names another suggested skill, since its
        # owner rule is the one that separates the suggestions.
        best = min(counts, key=lambda index: (
            not (chosen - {skill}) & set(boundaries[index]["skills"]), -counts[index], index))
        hints.append({"skill": skill, "cues": list(found[skill]["cues"]),
                      "score": len(found[skill]["cues"]),
                      "owner_rule": boundaries[best]["owner_rule"]})
    return hints


def _shorten(rule):
    rule = " ".join(rule.split())
    return rule if len(rule) <= RULE_LIMIT else rule[:RULE_LIMIT - 3].rstrip() + "..."


def hint_text(matches, invocation):
    """Short English advisory naming each full skill ID and its invocation."""
    if not matches:
        return ""
    if not isinstance(invocation, str) or "{skill}" not in invocation:
        raise ContractError("invocation template must contain {skill}")
    named = [hint["skill"] + " (" + ", ".join(f'"{cue}"' for cue in hint["cues"]) + ")"
             for hint in matches]
    calls = [invocation.replace("{skill}", hint["skill"]) for hint in matches]
    rules = []
    for hint in matches:
        rule = _shorten(hint["owner_rule"])
        if rule not in rules:
            rules.append(rule)
    if len(matches) == 1:
        lead = f"this request matches {named[0]}. If it fits, load {calls[0]} before acting; ignore otherwise."
    else:
        lead = (f"this request matches {', '.join(named[:-1])} and {named[-1]}. "
                f"If one fits, load {' or '.join(calls)} before acting; ignore otherwise.")
    return f"nckh routing hint (advisory): {lead} Boundary: {' | '.join(rules)}"


def evaluate_prompts(prompts, boundaries, *, limit=DEFAULT_LIMIT):
    """Score prompts per split: hit rate for skill prompts, false-positive rate for `none`.

    A skill prompt hits when its expected skill is among the suggestions; a `none`
    prompt is a false positive when anything is suggested.
    """
    rows = []
    summary = {}
    for row in prompts:
        suggested = [hint["skill"] for hint in match(row["prompt"], boundaries, limit=limit)]
        positive = row["expected"] != NONE
        ok = row["expected"] in suggested if positive else not suggested
        rows.append({"id": row["id"], "split": row["split"], "expected": row["expected"],
                     "suggested": suggested, "ok": ok})
        bucket = summary.setdefault(row["split"], {"skill_total": 0, "skill_hits": 0,
                                                   "none_total": 0, "none_false_positives": 0})
        if positive:
            bucket["skill_total"] += 1
            bucket["skill_hits"] += ok
        else:
            bucket["none_total"] += 1
            bucket["none_false_positives"] += not ok
    for bucket in summary.values():
        bucket["accuracy"] = bucket["skill_hits"] / bucket["skill_total"] if bucket["skill_total"] else None
        bucket["false_positive_rate"] = (bucket["none_false_positives"] / bucket["none_total"]
                                         if bucket["none_total"] else None)
    return rows, summary


def validate_routing_prompts(record, identities):
    """Validate a routing-prompts record against the skill catalog; return its prompts."""
    validate_record("routing-prompts", record)
    known = set(identities)
    seen = set()
    coverage = {skill: set() for skill in known}
    for index, row in enumerate(record["prompts"]):
        where = f"$.prompts[{index}]"
        if row["id"] in seen:
            raise ContractError(f"{where}: duplicate prompt id {row['id']}")
        seen.add(row["id"])
        expected = row["expected"]
        if expected != NONE and expected not in known:
            raise ContractError(f"{where}: unknown expected skill {expected}")
        if expected != NONE:
            coverage[expected].add(row["split"])
        if "origin" in row and row["split"] != "tune":
            raise ContractError(f"{where}: exposed held-out prompts must stay in the tune split")
        accented = has_diacritics(row["prompt"])
        if row.get("unaccented", False):
            if accented:
                raise ContractError(f"{where}: unaccented prompt carries diacritics")
        elif not accented:
            raise ContractError(f"{where}: prompt lacks Vietnamese diacritics")
    # Every skill needs tune prompts; once any held-out prompt exists, every skill
    # needs one there too (the held-out set is added separately and may be absent).
    required = SPLITS if any(row["split"] == "heldout" for row in record["prompts"]) else ("tune",)
    missing = sorted(f"{skill}:{split}" for skill, splits in coverage.items()
                     for split in required if split not in splits)
    if missing:
        raise ContractError(f"routing prompts missing split coverage: {missing}")
    return record["prompts"]
