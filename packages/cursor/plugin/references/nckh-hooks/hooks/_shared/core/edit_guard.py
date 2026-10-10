"""Bounded before/after snapshots that report line-ending or BOM drift caused by an edit.

A pre-edit event records the EOL/BOM profile of each target file under a
kit-owned runtime namespace; the matching post-edit event compares the file
with that record, consumes the snapshot and returns advisory findings. Nothing
here blocks, rewrites a target file or writes outside the snapshot namespace.
Callers own error handling: OSError and ContractError propagate.
"""

import json
import os
import re
import stat
import time

from core.ledger import _file_record, bom_profile, eol_profile
from core.paths import _is_link_like, atomic_json, contained, digest_record, no_links
from core.schema import ContractError


SNAPSHOT_ROOT = ".nckh-state/hooks/snapshots"
MAX_SNAPSHOT_BYTES = 16 * 1024 * 1024
MAX_PER_SESSION = 128
# Mirrors core.hook_policy.MAX_PATHS; kept local so the hook closure does not pull in
# the policy module. A test pins the two values together.
MAX_PATHS = 16
STALE_SECONDS = 24 * 60 * 60
MAX_PRUNE_SESSIONS = 64
MAX_ADVICE_FILES = 3
SESSION_PREFIX = 16
_HOST = re.compile(r"[a-z][a-z0-9-]{0,31}")
_SESSION = re.compile(r"[a-f0-9]{64}")
_SNAPSHOT_NAME = re.compile(r"[a-f0-9]{32}\.json")
# core.paths.atomic_bytes writes through mkstemp(prefix=".nckh-"): eight [a-z0-9_] characters.
_TEMPORARY_NAME = re.compile(r"\.nckh-[a-z0-9_]{8}")


def _session_dir(project, host, session_key):
    if not isinstance(host, str) or not _HOST.fullmatch(host):
        raise ContractError(f"invalid snapshot host: {host!r}")
    if not isinstance(session_key, str) or not _SESSION.fullmatch(session_key):
        raise ContractError("invalid snapshot session key")
    return contained(project, f"{SNAPSHOT_ROOT}/{host}/{session_key[:SESSION_PREFIX]}")


def _paths(relative_paths):
    paths = list(relative_paths)
    if len(paths) > MAX_PATHS:
        raise ContractError(f"edit guard path limit exceeded: {len(paths)} > {MAX_PATHS}")
    if not all(isinstance(path, str) for path in paths):
        raise ContractError("edit guard paths must be strings")
    return list(dict.fromkeys(paths))


def _has_link(project, relative):
    parts = relative.split("/")
    if "\\" in relative or ":" in relative or any(part in {"", ".", ".."} for part in parts):
        return False
    current = no_links(project)
    for part in parts:
        current = current / part
        try:
            if _is_link_like(os.lstat(current)):
                return True
        except (FileNotFoundError, NotADirectoryError):
            return False
    return False


def _target(project, relative):
    """Return the contained target, or None when a link-like component would be followed.

    Traversal, absolute and escaping paths still raise ContractError.
    """
    try:
        return contained(project, relative)
    except ContractError:
        if _has_link(project, relative):
            return None
        raise


def _regular(target):
    """Return (metadata, None) for a plain file, (None, reason) otherwise."""
    try:
        metadata = os.lstat(target)
    except (FileNotFoundError, NotADirectoryError):
        return None, "missing"
    if _is_link_like(metadata) or not stat.S_ISREG(metadata.st_mode):
        return None, "special"
    return metadata, None


def _read_bounded(target):
    with open(target, "rb") as stream:
        data = stream.read(MAX_SNAPSHOT_BYTES + 1)
    return None if len(data) > MAX_SNAPSHOT_BYTES else data


def _snapshot_file(directory, relative):
    return directory / (digest_record(relative)[:32] + ".json")


def _taken_at(path):
    try:
        value = json.loads(path.read_text(encoding="utf8")).get("taken_at")
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value)
    except (OSError, ValueError, AttributeError):
        pass
    try:
        return os.stat(path).st_mtime
    except FileNotFoundError:
        return 0.0


def _snapshot_entries(directory):
    entries = []
    try:
        with os.scandir(directory) as iterator:
            for entry in iterator:
                if (_SNAPSHOT_NAME.fullmatch(entry.name)
                        and entry.is_file(follow_symlinks=False)
                        and not _is_link_like(entry.stat(follow_symlinks=False))):
                    entries.append(directory / entry.name)
    except FileNotFoundError:
        return []
    return entries


def _stale_temporaries(directory, cutoff):
    """Atomic-write temporaries a killed writer left behind, older than the cutoff."""
    entries = []
    try:
        with os.scandir(directory) as iterator:
            for entry in iterator:
                if not _TEMPORARY_NAME.fullmatch(entry.name):
                    continue
                metadata = entry.stat(follow_symlinks=False)
                if (stat.S_ISREG(metadata.st_mode) and not _is_link_like(metadata)
                        and metadata.st_mtime < cutoff):
                    entries.append(directory / entry.name)
    except FileNotFoundError:
        return []
    return entries


def _unlink(path):
    try:
        os.unlink(path)
    except FileNotFoundError:
        pass


def _evict(directory):
    entries = _snapshot_entries(directory)
    excess = len(entries) - MAX_PER_SESSION
    if excess > 0:
        ordered = sorted(entries, key=lambda path: (_taken_at(path), path.name))
        for path in ordered[:excess]:
            _unlink(path)


def _prune(host_dir, current, now):
    """Remove other sessions whose snapshots are all older than the stale age.

    Oldest sessions go first and at most MAX_PRUNE_SESSIONS are removed per call; a
    session kept by a foreign file does not count, so it cannot starve the rest.
    """
    candidates = []
    try:
        with os.scandir(host_dir) as iterator:
            for entry in iterator:
                metadata = entry.stat(follow_symlinks=False)
                if (entry.name != current and stat.S_ISDIR(metadata.st_mode)
                        and not _is_link_like(metadata)):
                    candidates.append((metadata.st_mtime, entry.name))
    except FileNotFoundError:
        return
    cutoff = now - STALE_SECONDS
    removed = 0
    for modified, name in sorted(candidates):
        # A recent directory mtime means another session is still writing or consuming;
        # candidates are sorted, so every later one is at least as recent.
        if modified >= cutoff or removed >= MAX_PRUNE_SESSIONS:
            break
        directory = host_dir / name
        entries = _snapshot_entries(directory)
        if any(_taken_at(path) >= cutoff for path in entries):
            continue
        for path in entries + _stale_temporaries(directory, cutoff):
            _unlink(path)
        try:
            os.rmdir(directory)
        except FileNotFoundError:
            pass
        except OSError:
            # Foreign files keep the directory; only kit snapshots and temporaries are removed.
            continue
        removed += 1


def snapshot(project, host, session_key, relative_paths, *, now=None):
    """Record the pre-edit EOL/BOM profile of each path; return the written records."""
    now = time.time() if now is None else float(now)
    project = no_links(project)
    paths = _paths(relative_paths)
    directory = _session_dir(project, host, session_key)
    records = []
    for relative in paths:
        target = _target(project, relative)
        if target is None:
            continue
        metadata, reason = _regular(target)
        if reason == "special":
            continue
        if reason == "missing":
            record = {"path": relative, "exists": False, "taken_at": now}
        elif metadata.st_size > MAX_SNAPSHOT_BYTES:
            record = {"path": relative, "skipped": "too-large", "size": metadata.st_size, "taken_at": now}
        else:
            data = _read_bounded(target)
            if data is None:
                record = {"path": relative, "skipped": "too-large", "taken_at": now}
            else:
                record = {"path": relative, "exists": True, **_file_record(data), "taken_at": now}
        atomic_json(_snapshot_file(directory, relative), record)
        records.append(record)
    if records:
        _evict(directory)
    _prune(directory.parent, directory.name, now)
    return records


def discard(project, host, session_key, relative_paths):
    """Drop any snapshot left for paths without writing state.

    A pre-edit event whose post-edit event never fired (a denied or rejected write)
    leaves its snapshot behind; a later edit that recreates the file must not be
    compared against it.
    """
    project = no_links(project)
    paths = _paths(relative_paths)
    directory = _session_dir(project, host, session_key)
    for relative in paths:
        _target(project, relative)  # traversal and escaping paths still raise
        _unlink(_snapshot_file(directory, relative))


def _load_snapshot(path):
    try:
        record = json.loads(path.read_text(encoding="utf8"))
    except FileNotFoundError:
        return None
    except (OSError, ValueError):
        record = None
    _unlink(path)
    return record if isinstance(record, dict) else None


def compare(project, host, session_key, relative_paths):
    """Consume the snapshots for paths and return findings for changed EOL or BOM."""
    project = no_links(project)
    paths = _paths(relative_paths)
    directory = _session_dir(project, host, session_key)
    findings = []
    for relative in paths:
        target = _target(project, relative)
        record = _load_snapshot(_snapshot_file(directory, relative))
        if (target is None or record is None or record.get("exists") is not True
                or record.get("path") != relative or "skipped" in record):
            continue
        metadata, reason = _regular(target)
        if reason is not None or metadata.st_size > MAX_SNAPSHOT_BYTES:
            continue
        data = _read_bounded(target)
        if data is None:
            continue
        eol_after, bom_after = eol_profile(data), bom_profile(data)
        if eol_after != record.get("eol") or bom_after != record.get("bom"):
            findings.append({"path": relative, "eol_before": record.get("eol"), "eol_after": eol_after,
                             "bom_before": record.get("bom"), "bom_after": bom_after})
    return findings


def _bom_text(bom):
    return "no BOM" if bom == "none" else f"{bom} BOM"


def advice_text(findings):
    """Return an English advisory for at most three findings, or an empty string."""
    if not findings:
        return ""
    parts = []
    for finding in findings[:MAX_ADVICE_FILES]:
        after = []
        if finding["eol_after"] != finding["eol_before"]:
            after.append(finding["eol_after"])
        if finding["bom_after"] != finding["bom_before"]:
            after.append(_bom_text(finding["bom_after"]))
        parts.append(f"{finding['path']} was {finding['eol_before']}/{_bom_text(finding['bom_before'])} "
                     f"before this edit and is now {'/'.join(after)}")
    remaining = len(findings) - MAX_ADVICE_FILES
    if remaining > 0:
        parts.append(f"{remaining} more file(s) changed the same way")
    return ("nckh EOL/BOM guard (advisory): " + "; ".join(parts)
            + ". Restore the original line endings and BOM unless the user asked for this change; "
            "re-check with check-receipt.py inventory.")
