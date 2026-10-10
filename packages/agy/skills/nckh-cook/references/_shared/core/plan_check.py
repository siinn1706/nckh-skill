"""Mechanical checks for a plan directory written in English or Vietnamese.

A plan is VERIFIED only when its structure can be checked from the files alone:
an index with frontmatter, one phase file per declared phase, the required
section groups in every phase, resolvable relative links, and a resolvable
receipt beside every completion status. Nothing here judges plan quality.
"""

import re
import unicodedata
from pathlib import Path
from urllib.parse import unquote


# The single bilingual alias table for required phase sections. A heading
# satisfies a group when its normalized text equals an alias or starts with
# the alias followed by a non-word character.
SECTION_ALIASES = {
    "requirements": ("requirements", "requirement", "acceptance criteria",
                     "yêu cầu", "tiêu chí chấp nhận"),
    "files": ("files", "file", "related code files", "tệp", "tập tin"),
    "steps": ("implementation steps", "steps", "todo", "todo list",
              "các bước", "bước thực hiện", "bước", "kế hoạch thực hiện"),
    "checks": ("checks", "verification", "validation", "tests", "test", "success criteria",
               "kiểm tra", "kiểm chứng", "xác minh", "tiêu chí thành công"),
    "risk-rollback": ("risk", "risks", "rollback", "rủi ro", "hoàn tác", "khôi phục"),
}
PHASE_COLUMN = ("phase", "phases", "giai đoạn")
PHASE_LIST = ("phases", "phase", "các giai đoạn", "giai đoạn", "các phase")
STATUS_COLUMN = ("status", "trạng thái", "tình trạng")
RECEIPT_LABELS = ("receipt", "receipts", "evidence", "biên nhận", "bằng chứng")

COMPLETION = re.compile(r"(?<!\w)(done|completed|hoàn thành|verified)(?!\w)", re.IGNORECASE)
LIST_PREFIX = r"^\s*(?:(?:[-*+>]|\d+[.)])\s*)*(?:\*\*|__)?"
MARKER_LINE = re.compile(LIST_PREFIX + r"(done|completed|hoàn thành|verified)(?:\*\*|__)?\s*[:：]",
                         re.IGNORECASE)
STATUS_LINE = re.compile(LIST_PREFIX + r"(?:status|trạng thái|tình trạng)(?:\*\*|__)?\s*[:：](.*)$",
                         re.IGNORECASE)
RECEIPT_LINE = re.compile(LIST_PREFIX + r"(?:" + "|".join(RECEIPT_LABELS) + r")(?:\*\*|__)?\s*[:：]",
                          re.IGNORECASE)
LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
INLINE_CODE = re.compile(r"`([^`\n]+)`")
FENCE = re.compile(r"^\s*(```|~~~)")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
PHASE_FILE = re.compile(r"^phase-\d+[^/\\]*\.md$", re.IGNORECASE)
HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
PHASE_HEADING = re.compile(r"^(?:phase|giai đoạn)\s+\d+", re.IGNORECASE)


def _normalize(text):
    text = unicodedata.normalize("NFC", text).casefold()
    text = re.sub(r"[*_`]", "", text)
    text = re.sub(r"^[\s\d.):#-]+", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _matches(text, aliases):
    return any(text == alias or (text.startswith(alias) and not text[len(alias)].isalnum())
               for alias in aliases)


class _Document:
    def __init__(self, path, plan_dir, findings):
        self.path = path
        self.name = path.relative_to(plan_dir).as_posix()
        self.receipt_root = plan_dir.resolve().parent
        self.frontmatter, self.lines = {}, []
        self.has_frontmatter = False
        try:
            text = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            findings.append(_finding("encoding", self.name, 0, "file is not valid UTF-8"))
            return
        lines = text.lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n").split("\n")
        start = 0
        if lines and lines[0].strip() == "---":
            for index in range(1, len(lines)):
                if lines[index].strip() == "---":
                    self.has_frontmatter = True
                    for raw in lines[1:index]:
                        match = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", raw)
                        if match:
                            self.frontmatter[match.group(1).casefold()] = match.group(2).strip().strip("\"'")
                    start = index + 1
                    break
        fenced = False
        for number, raw in enumerate(lines[start:], start + 1):
            if FENCE.match(raw):
                fenced = not fenced
                continue
            if not fenced:
                self.lines.append((number, raw))

    def headings(self):
        for number, raw in self.lines:
            match = HEADING.match(raw)
            if match:
                yield number, _normalize(match.group(2))

    def tables(self):
        """Yield (nearest heading, normalized header cells, data rows) per Markdown table."""
        block, heading = [], ""
        for number, raw in [*self.lines, (None, "")]:
            if raw.lstrip().startswith("|"):
                block.append((number, raw))
                continue
            if len(block) >= 2 and re.fullmatch(r"\s*\|?[\s:|-]+\|?\s*", block[1][1]):
                header = [_normalize(cell) for cell in _cells(block[0][1])]
                yield heading, header, [(n, row, _cells(row)) for n, row in block[2:]]
            block = []
            match = HEADING.match(raw)
            if match:
                heading = _normalize(match.group(2))


def _cells(row):
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|") and not row.endswith("\\|"):
        row = row[:-1]
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", row)]


def _finding(rule, path, line, message):
    return {"rule": rule, "path": path, "line": line, "message": message}


def _relative_targets(text):
    """Yield local link targets of a line, ignoring links inside inline code."""
    for href in LINK.findall(INLINE_CODE.sub("", text)):
        target = unquote(href.split("#", 1)[0])
        if target and not SCHEME.match(target) and not target.startswith("/"):
            yield target


def _resolves(document, target):
    try:
        return (document.path.parent / target).exists()
    except (OSError, ValueError):
        return False


def _plan_file(document, target):
    """True when target names plan.md or a phase file inside the plan directory itself."""
    name = Path(target).name
    try:
        same_dir = (document.path.parent / target).resolve().parent == document.path.parent.resolve()
    except (OSError, ValueError):
        return False
    return same_dir and (bool(PHASE_FILE.match(name)) or name.casefold() == "plan.md")


def _receipt_paths(document, text):
    """Resolvable receipt candidates in text: links and inline-code paths, excluding plan files.

    A receipt is a relative path that resolves under the plans root (the plan directory's
    parent), so a sibling plan's receipt counts but a rooted path or any system or
    repository file outside that root does not.
    """
    candidates = list(_relative_targets(text))
    candidates += [code.strip() for code in INLINE_CODE.findall(text)
                   if re.fullmatch(r"[^\s<>|*?\"]+", code.strip()) and not SCHEME.match(code.strip())]
    found = []
    for target in candidates:
        if target.startswith(("/", "\\")) or _plan_file(document, target):
            continue
        try:
            candidate = (document.path.parent / target).resolve()
            if candidate.is_relative_to(document.receipt_root) and candidate.is_file():
                found.append(target)
        except (OSError, ValueError):
            continue
    return found


def _document_receipts(document):
    receipts = []
    for key in RECEIPT_LABELS:
        value = document.frontmatter.get(key.replace(" ", "_"))
        if value and _receipt_paths(document, f"`{value}`"):
            receipts.append(value)
    for _, raw in document.lines:
        if RECEIPT_LINE.match(raw):
            receipts += _receipt_paths(document, raw)
    return receipts


def _check_links(document, findings):
    for number, raw in document.lines:
        for target in _relative_targets(raw):
            if not _resolves(document, target):
                findings.append(_finding("broken-link", document.name, number,
                                         f"relative link does not resolve: {target}"))


def _check_sections(document, findings):
    headings = [text for _, text in document.headings()]
    missing = [group for group, aliases in SECTION_ALIASES.items()
               if not any(_matches(text, aliases) for text in headings)]
    if missing:
        findings.append(_finding("phase-sections", document.name, 0,
                                 "missing section groups: " + ", ".join(missing)))


def _check_statuses(document, findings, phase_receipts):
    status = document.frontmatter.get("status", "")
    if COMPLETION.search(status) and not _document_receipts(document):
        findings.append(_finding("status-without-receipt", document.name, 1,
                                 f"frontmatter status {status!r} has no resolvable receipt"))
    table_rows = set()
    for _, header, rows in document.tables():
        columns = [index for index, cell in enumerate(header) if _matches(cell, STATUS_COLUMN)]
        for number, raw, cells in rows:
            table_rows.add(number)
            values = [cells[index] for index in columns if index < len(cells)]
            if not any(COMPLETION.search(INLINE_CODE.sub("", value)) for value in values):
                continue
            linked = [phase_receipts.get(Path(t).name) for t in _relative_targets(raw)
                      if _plan_file(document, t)]
            if not _receipt_paths(document, raw) and not any(linked):
                findings.append(_finding("status-without-receipt", document.name, number,
                                         "completion status in table row has no resolvable receipt"))
    for number, raw in document.lines:
        if number in table_rows:
            continue
        prose = INLINE_CODE.sub("", raw)
        status_line = STATUS_LINE.match(prose)
        marked = MARKER_LINE.match(prose) or (status_line and COMPLETION.search(status_line.group(1)))
        if marked and not _receipt_paths(document, raw):
            findings.append(_finding("status-without-receipt", document.name, number,
                                     "completion marker has no resolvable receipt on the same line"))


def _declared_phases(plan):
    """A phase table has a phase column plus a status column or a phase-list heading."""
    rows = []
    for heading, header, table_rows in plan.tables():
        if any(cell in PHASE_COLUMN for cell in header) and (
                any(_matches(cell, STATUS_COLUMN) for cell in header) or _matches(heading, PHASE_LIST)):
            rows.extend(table_rows)
    headings = [text for _, text in plan.headings() if PHASE_HEADING.match(text)]
    return rows, max(len(rows), len(headings))


def check_plan(plan_dir):
    """Return {"verdict": "VERIFIED" | "FAILED", "findings": [...]} for a plan directory."""
    plan_dir = Path(plan_dir)
    if not plan_dir.is_dir():
        raise NotADirectoryError(f"plan directory does not exist: {plan_dir}")
    findings = []
    index = plan_dir / "plan.md"
    if not index.is_file():
        findings.append(_finding("plan-index", "plan.md", 0, "plan.md is missing"))
        return {"verdict": "FAILED", "findings": findings}
    plan = _Document(index, plan_dir, findings)
    if not plan.has_frontmatter:
        findings.append(_finding("frontmatter", plan.name, 1, "plan.md has no YAML frontmatter"))
    phases = [_Document(path, plan_dir, findings) for path in sorted(plan_dir.glob("phase-*.md"))
              if PHASE_FILE.match(path.name)]
    rows, declared = _declared_phases(plan)
    if not phases and declared > 1:
        findings.append(_finding("single-file-plan", plan.name, 0,
                                 f"single-file plan declares {declared} phases; "
                                 "a plan file alone is valid only for one phase"))
    if len(rows) >= 2:
        for number, raw, _ in rows:
            targets = [t for t in _relative_targets(raw)
                       if _plan_file(plan, t) and PHASE_FILE.match(Path(t).name)]
            if not any(_resolves(plan, target) for target in targets):
                findings.append(_finding("phase-link", plan.name, number,
                                         "phase row does not link to an existing phase-NN-*.md file"))
    phase_receipts = {}
    for document in [plan, *phases]:
        _check_links(document, findings)
    for document in phases:
        _check_sections(document, findings)
        phase_receipts[document.path.name] = _document_receipts(document)
    for document in [*phases, plan]:
        _check_statuses(document, findings, phase_receipts)
    return {"verdict": "FAILED" if findings else "VERIFIED", "findings": findings}
