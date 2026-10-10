"""Mechanical evidence-ledger checks for claims, task state and command receipts.

The JSON Schema subset in core.schema has no conditional keywords, so every rule
that depends on another field's value lives here. Validators never execute
recorded commands; they only compare records with each other and with the disk.
"""

import os
from pathlib import Path

from core.paths import _is_link_like, contained, digest_bytes, no_links
from core.schema import ContractError, validate_record


PASSING_EXIT = frozenset({"0", "pass", "passed", "ok", "success", "succeeded"})
EVIDENCE_GATE_STATUSES = frozenset({"pass", "fail"})
POWERSHELL = frozenset({"powershell", "pwsh", "powershell.exe", "pwsh.exe"})
CMD = frozenset({"cmd", "cmd.exe"})
EOL_PROFILES = frozenset({"none", "lf", "crlf", "cr", "mixed"})
BOMS = ((b"\xef\xbb\xbf", "utf-8"), (b"\xff\xfe", "utf-16-le"), (b"\xfe\xff", "utf-16-be"))


def eol_profile(data):
    """Return the line-ending style of raw bytes: none, lf, crlf, cr or mixed."""
    crlf = data.count(b"\r\n")
    lf = data.count(b"\n") - crlf
    cr = data.count(b"\r") - crlf
    styles = [name for name, count in (("crlf", crlf), ("lf", lf), ("cr", cr)) if count]
    if not styles:
        return "none"
    return styles[0] if len(styles) == 1 else "mixed"


def bom_profile(data):
    for marker, name in BOMS:
        if data.startswith(marker):
            return name
    return "none"


def _file_record(data):
    return {"sha256": digest_bytes(data), "eol": eol_profile(data), "bom": bom_profile(data),
            "size": len(data)}


def _link_like(path):
    # Junctions carry the name-surrogate reparse bit, so this needs no Path.is_junction (3.12+).
    return _is_link_like(os.lstat(path))


def inventory(root):
    """Hash every regular file below root with its EOL and BOM, skipping __pycache__.

    Link-like entries are listed but never followed, so the inventory cannot leave root.
    """
    root = no_links(root)
    if not root.is_dir():
        raise ContractError(f"inventory root is not a directory: {root}")
    files, links = {}, []
    for directory, children, names in os.walk(root, followlinks=False):
        base = Path(directory)
        kept = []
        for child in sorted(children):
            if child == "__pycache__":
                continue
            if _link_like(base / child):
                links.append((base / child).relative_to(root).as_posix())
            else:
                kept.append(child)
        children[:] = kept
        for name in sorted(names):
            path = base / name
            relative = path.relative_to(root).as_posix()
            if _link_like(path):
                links.append(relative)
            elif path.is_file():
                files[relative] = _file_record(path.read_bytes())
    return {"schema_version": 1, "files": dict(sorted(files.items())), "links": sorted(links)}


def _dialect(shell):
    name = os.path.basename(str(shell)).casefold()
    return "powershell" if name in POWERSHELL else "cmd" if name in CMD else "posix"


def _separator_width(command, index, current, dialect):
    """Width of the top-level separator starting at index, or 0 when there is none."""
    char = command[index]
    following = command[index + 1] if index + 1 < len(command) else ""
    previous = current[-1] if current and len(current[-1]) == 1 else ""
    if char in {"&", "|"} and following == char:
        return 2
    if char == "|":
        return 2 if following == "&" else 0 if previous == ">" else 1
    if char == "&":
        redirect = previous in {"<", ">"} or dialect == "posix" and following == ">"
        return 0 if dialect == "powershell" or redirect else 1
    return 1 if char == "\n" or char == ";" and dialect != "cmd" else 0


HEREDOC_WORD_END = frozenset(" \t\n;&|<>()")


def _heredoc_operator(command, index):
    """Parse a heredoc operator at index into (end, (word, strip_tabs, text)), or None."""
    if not command.startswith("<<", index) or command.startswith("<<<", index):
        return None
    position = index + 2
    strip_tabs = command.startswith("-", position)
    position += strip_tabs
    while position < len(command) and command[position] in " \t":
        position += 1
    if position < len(command) and command[position] in {"'", '"'}:
        close = command.find(command[position], position + 1)
        if close < 0:
            return None
        word, end = command[position + 1:close], close + 1
    else:
        end = position
        while end < len(command) and command[end] not in HEREDOC_WORD_END:
            end += 1
        word = "".join(char for char in command[position:end] if char not in "\\'\"")
    if not word:
        return None
    return end, (word, strip_tabs, command[index:end])


def _heredoc_bodies(command, position, delimiters):
    """(start, end) span of each consecutive heredoc body, through its terminator line.

    An unterminated body runs to the end of the command and later spans are empty.
    """
    spans = []
    for word, strip_tabs in delimiters:
        start = position
        while position <= len(command):
            newline = command.find("\n", position)
            end = len(command) if newline < 0 else newline
            line = command[position:end]
            position = end + 1
            if (line.lstrip("\t") if strip_tabs else line) == word:
                break
        spans.append((start, min(position - 1, len(command))))
    return spans


def command_segments(command, shell="bash"):
    """Split a command line into the steps whose exit statuses a receipt must record.

    Top-level separators are &&, ||, | (not the >| redirection), newline and ; (not
    in cmd, where ; is an argument delimiter). A lone & also separates in bash and
    cmd unless it belongs to a redirection (2>&1, >&2, <&3, bash &>); in PowerShell
    & is the call operator. Quoting follows the shell: cmd quotes only with " and its
    caret escape is literal inside quotes; PowerShell escapes with a backtick and
    other shells with a backslash, both outside single quotes. In bash, $( ), <( ),
    >( ) and backtick substitutions never split, and a # that starts a word begins
    a comment that is dropped. A top-level bash heredoc (<<WORD, <<-WORD, <<'WORD'
    or <<"WORD") keeps its body, from the next line through the line holding only
    WORD (leading tabs ignored for <<-), inside the segment of its command; an
    unterminated body runs to the end. The <<< here-string and a << shift inside
    (( )) or $(( )) arithmetic are not heredocs, and
    cmd and PowerShell have no heredocs. Empty segments (a trailing newline or a
    background &) are dropped.
    """
    dialect = _dialect(shell)
    posix = dialect == "posix"
    escape = {"powershell": "`", "cmd": "^", "posix": "\\"}[dialect]
    quotes = {'"'} if dialect == "cmd" else {"'", '"'}
    segments, current, stack, index, heredocs, arithmetic = [], [], [], 0, [], 0
    while index < len(command):
        char = command[index]
        following = command[index + 1] if index + 1 < len(command) else ""
        top = stack[-1] if stack else None
        width = 1
        if top == "'":
            if char == "'":
                stack.pop()
        elif char == escape and following and not (dialect == "cmd" and top == '"'):
            width = 2
        elif posix and top is None and char in "()" and (arithmetic or command.startswith("((", index)):
            # A top-level (( ... )) is arithmetic: its << is a shift, never a heredoc.
            arithmetic = max(arithmetic + (1 if char == "(" else -1), 0)
        elif posix and top is None and command.startswith("<<<", index):
            width = 3
        elif posix and top is None and not arithmetic and (heredoc := _heredoc_operator(command, index)):
            index, (word, strip_tabs, text) = heredoc
            current.append(text)
            heredocs.append((word, strip_tabs, len(segments)))
            continue
        elif posix and top is None and char == "\n" and heredocs:
            # Each body joins the segment holding its operator; the newline that ends
            # the last terminator line still separates the following command.
            spans = _heredoc_bodies(command, index + 1, [entry[:2] for entry in heredocs])
            for (_, _, owner), (start, end) in zip(heredocs, spans):
                body = "\n" + command[start:end]
                if owner == len(segments):
                    current.append(body)
                else:
                    segments[owner] = segments[owner].rstrip(" \t") + body
            heredocs = []
            index = spans[-1][1]
            continue
        elif posix and following == "(" and (char == "$" or char in {"<", ">"} and top in {None, "("}):
            stack.append("(")
            width = 2
        elif top in {'"', "`"}:
            if char == top:
                stack.pop()
        elif char in quotes or posix and char == "`":
            stack.append(char)
        elif posix and char == "#" and (index == 0 or command[index - 1] in " \t\n;&|()"):
            end = command.find("\n", index)
            index = len(command) if end < 0 else end
            continue
        elif top == "(":
            if char == "(":
                stack.append("(")
            elif char == ")":
                stack.pop()
        elif separator := _separator_width(command, index, current, dialect):
            segments.append("".join(current))
            current = []
            index += separator
            continue
        current.append(command[index:index + width])
        index += width
    segments.append("".join(current))
    return [segment.strip() for segment in segments if segment.strip()]


def _result(findings):
    return {"verdict": "FAILED" if findings else "VERIFIED", "findings": findings}


VERSIONED_KINDS = frozenset({"claim", "receipt", "task-state"})


def _schema(kind, record, findings):
    version = record.get("schema_version") if isinstance(record, dict) else None
    if kind in VERSIONED_KINDS and type(version) is int and version == 1:
        findings.append(f"{kind} schema: schema_version 1 is unsupported for {kind}; "
                        "regenerate the record as schema_version 2")
        return False
    try:
        validate_record(kind, record)
        return True
    except ContractError as error:
        findings.append(f"{kind} schema: {error}")
        return False


def validate_claim(record):
    findings = []
    if not _schema("claim", record, findings):
        return _result(findings)
    if record["verdict"] == "supported" and not record["evidence_ids"]:
        findings.append(f"claim {record['id']}: supported verdict has no evidence_ids")
    if record["attempt_status"] == "verified-this-attempt" and not record["evidence_ids"]:
        findings.append(f"claim {record['id']}: verified-this-attempt has no evidence_ids")
    return _result(findings)


def validate_task_state(record):
    findings = []
    if not _schema("task-state", record, findings):
        return _result(findings)
    for gate in record["gates"]:
        if gate["status"] in EVIDENCE_GATE_STATUSES and not gate.get("evidence_reference"):
            findings.append(f"gate {gate['id']}: status {gate['status']} has no evidence_reference")
    for attempt in record["attempts"]:
        produced = {item["path"] for item in attempt.get("output_hashes", [])}
        for path in attempt.get("created_this_attempt", []):
            if path not in produced:
                findings.append(f"attempt {attempt['handle']}: created file {path} has no output hash")
    return _result(findings)


def _check_commands(record, findings):
    failing = []
    for index, result in enumerate(record["command_results"]):
        label = f"command_results[{index}]"
        segments = command_segments(result["command"], result["shell"])
        statuses = result.get("segment_exit_statuses")
        if len(segments) > 1 and statuses is None:
            findings.append(f"{label}: compound command with {len(segments)} segments "
                            "has no segment_exit_statuses")
        if statuses is not None and len(statuses) != len(segments):
            findings.append(f"{label}: {len(statuses)} segment exit statuses for "
                            f"{len(segments)} segments")
        nonzero = result["exit_status"] != 0 or any(code != 0 for code in statuses or [])
        if nonzero and not result["expected_nonzero"]:
            failing.append(label)
    if failing and record["exit_status"].strip().casefold() in PASSING_EXIT:
        findings.append(f"exit_status {record['exit_status']!r} hides unexpected nonzero exits in "
                        + ", ".join(failing))


def _check_files(record, findings):
    inputs = {}
    for item in record["input_files"]:
        inputs[item["path"]] = item
        if item["mutation"] == "none":
            if item["sha256_before"] != item["sha256_after"]:
                findings.append(f"input {item['path']}: unauthorized content change")
            if item["eol_before"] != item["eol_after"]:
                findings.append(f"input {item['path']}: unauthorized EOL change "
                                f"{item['eol_before']} -> {item['eol_after']}")
        elif not item.get("preimage_path"):
            findings.append(f"input {item['path']}: authorized mutation has no preimage_path")
    for item in record["output_files"]:
        source = inputs.get(item["path"])
        if source and source["mutation"] != "authorized-with-preimage":
            findings.append(f"output {item['path']}: overwrites an input without an authorized preimage")
    return inputs


def _disk(workspace, relative, findings, label):
    try:
        path = contained(workspace, relative)
    except ContractError as error:
        findings.append(f"{label}: {error}")
        return None
    if not path.is_file():
        findings.append(f"{label}: file is missing on disk: {relative}")
        return None
    return _file_record(path.read_bytes())


def _check_workspace(record, inputs, workspace, findings):
    for path, item in inputs.items():
        actual = _disk(workspace, path, findings, f"input {path}")
        if actual and (actual["sha256"], actual["eol"]) != (item["sha256_after"], item["eol_after"]):
            findings.append(f"input {path}: recorded after-state does not match disk")
        if item["mutation"] == "authorized-with-preimage" and item.get("preimage_path"):
            preimage = _disk(workspace, item["preimage_path"], findings, f"input {path} preimage")
            if preimage and preimage["sha256"] != item["sha256_before"]:
                findings.append(f"input {path}: preimage hash differs from sha256_before")
    for item in record["output_files"]:
        actual = _disk(workspace, item["path"], findings, f"output {item['path']}")
        if actual and actual["sha256"] != item["sha256"]:
            findings.append(f"output {item['path']}: recorded sha256 does not match disk")


def _check_before(record, inputs, before, findings):
    files = before.get("files") if isinstance(before, dict) else None
    if not isinstance(files, dict):
        findings.append("before inventory has no files mapping")
        return
    for path, item in inputs.items():
        prior = files.get(path)
        if prior is None:
            findings.append(f"input {path}: absent from the before inventory")
        elif (prior.get("sha256"), prior.get("eol")) != (item["sha256_before"], item["eol_before"]):
            findings.append(f"input {path}: recorded before-state does not match the before inventory")
    for item in record["output_files"]:
        existed = item["path"] in files
        if item["created_this_attempt"] == existed:
            findings.append(f"output {item['path']}: created_this_attempt={item['created_this_attempt']} "
                            f"but the file {'existed' if existed else 'was absent'} before the attempt")


def validate_receipt(record, *, before=None, workspace=None):
    """Check a v2 receipt; with workspace/before, recompute real hashes and creation."""
    findings = []
    if not _schema("receipt", record, findings):
        return _result(findings)
    _check_commands(record, findings)
    inputs = _check_files(record, findings)
    if workspace is not None:
        _check_workspace(record, inputs, workspace, findings)
    elif any(item["mutation"] == "authorized-with-preimage" for item in inputs.values()):
        findings.append("authorized mutation preimage cannot be verified without a workspace")
    if before is not None:
        _check_before(record, inputs, before, findings)
    return _result(findings)
