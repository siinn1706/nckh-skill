"""Containment, hashes and atomic records used by build and installation."""

import hashlib
import json
import os
import re
import tempfile
import shutil
import uuid
from contextlib import contextmanager
from pathlib import Path, PurePosixPath

from core.schema import ContractError


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()


def digest_file(path):
    return digest_bytes(Path(path).read_bytes())


def digest_record(record):
    return digest_bytes(json.dumps(record, sort_keys=True, ensure_ascii=False,
                                  separators=(",", ":"), allow_nan=False).encode("utf-8"))


def no_links(path):
    path = Path(os.path.abspath(path))
    for current in (path, *path.parents):
        if current.is_symlink() or getattr(current, "is_junction", lambda: False)():
            raise ContractError(f"linked path is not allowed: {current}")
    return path


def contained(root, relative):
    relative = str(relative)
    part = PurePosixPath(relative)
    if not relative or "\\" in relative or part.is_absolute() or ":" in relative:
        raise ContractError(f"invalid relative path: {relative}")
    if any(p in {"..", ".", ""} for p in relative.split("/")):
        raise ContractError(f"path traversal: {relative}")
    root = no_links(root)
    target = no_links(root.joinpath(*part.parts))
    if not target.resolve().is_relative_to(root.resolve()):
        raise ContractError(f"path escapes root: {relative}")
    return target


def skill_id(value):
    if not isinstance(value, str) or not re.fullmatch(r"nckh-[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise ContractError(f"invalid skill identity: {value!r}")
    return value


def owned_target(root, identity):
    root = no_links(root)
    target = root / skill_id(identity)
    if getattr(target, "is_junction", lambda: False)():
        raise ContractError(f"junction destination is not allowed: {target}")
    return target


def device_identity(path):
    current = no_links(path)
    while not current.exists():
        current = current.parent
    return current.stat().st_dev


def unique_paths(paths):
    seen = set()
    for path in paths:
        folded = str(path).casefold()
        if folded in seen:
            raise ContractError(f"case-fold collision: {path}")
        seen.add(folded)


@contextmanager
def temporary_tree(parent=None):
    """Inherit Windows ACLs; Python's private-directory mode rejects sandbox access."""
    parent = no_links(parent or tempfile.gettempdir())
    path = parent / ("nckh-" + uuid.uuid4().hex)
    path.mkdir(mode=0o777 if os.name == "nt" else 0o700)
    try:
        yield path
    finally:
        no_links(path)
        if not path.resolve().is_relative_to(parent.resolve()):
            raise ContractError("temporary directory escaped its owning root")
        if path.exists():
            shutil.rmtree(path)


def atomic_json(path, value):
    path = no_links(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2,
                      allow_nan=False) + "\n"
    fd, temporary = tempfile.mkstemp(prefix=".nckh-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
