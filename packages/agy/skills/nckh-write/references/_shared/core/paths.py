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
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2,
                      allow_nan=False) + "\n"
    atomic_bytes(path, data.encode("utf8"))


def atomic_bytes(path, data):
    path = no_links(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".nckh-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def exclusive_file_lock(path):
    """Kernel-backed, nonblocking lock for an owned hook transaction/receipt."""
    path = no_links(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
    acquired = False
    try:
        if os.name == "nt":
            import msvcrt
            if os.fstat(descriptor).st_size == 0:
                os.write(descriptor, b"0")
            os.lseek(descriptor, 0, os.SEEK_SET)
            msvcrt.locking(descriptor, msvcrt.LK_NBLCK, 1)
        elif os.name == "posix":
            import fcntl
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        else:
            raise ContractError("hook locking unsupported; no config write")
        acquired = True
        yield
    except OSError as error:
        raise ContractError("hook lock unavailable/conflict; no uncoordinated write") from error
    finally:
        if acquired:
            if os.name == "nt":
                os.lseek(descriptor, 0, os.SEEK_SET)
                msvcrt.locking(descriptor, msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)
