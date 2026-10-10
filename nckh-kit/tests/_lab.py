"""Select an isolated test parent without changing the user's TEMP or skills."""
import getpass
import os
import re
import tempfile
import uuid
from pathlib import Path

from core.build import load_json
from core.paths import no_links
from core.schema import ContractError

ROOT = Path(__file__).resolve().parents[1]
_selected = None


def assert_clean_ancestors(root):
    root = no_links(root)
    relative_roots = set()
    for host in ("agy", "claude", "codex", "cursor"):
        adapter = load_json(ROOT / "adapters" / host / "adapter.json")
        relative_roots.update(adapter["compatibility_project"])
        relative_roots.update(surface["global"] for surface in adapter["surfaces"].values())
    conflicts = []
    for ancestor in (root, *root.parents):
        for relative in sorted(relative_roots):
            skills = ancestor / relative
            if skills.is_dir():
                conflicts.extend(str(path) for path in skills.glob("nckh-*")
                                 if path.exists() or path.is_symlink())
    if conflicts:
        raise ContractError("test root has visible ancestor skills: " + ", ".join(conflicts)
                            + "; set NCKH_TEST_ROOT to a writable directory outside these ancestors")
    return root


def assert_writable(root):
    """Create and remove a unique probe so an unwritable root fails before any test runs."""
    probe = root / (".nckh-write-probe-" + uuid.uuid4().hex)
    probe.touch(exist_ok=False)
    probe.unlink()
    return root


def _candidates():
    user = re.sub(r"[^a-zA-Z0-9_-]", "-", getpass.getuser())
    candidates = ([Path(os.environ.get("SystemDrive", "C:") + "\\") / ("nckh-test-" + user)]
                  if os.name == "nt" else [Path("/tmp") / ("nckh-test-" + str(os.getuid()))])
    candidates.append(Path(tempfile.gettempdir()))
    return candidates


def lab_root():
    global _selected
    override = os.environ.get("NCKH_TEST_ROOT")
    if override:
        root = assert_clean_ancestors(Path(override).absolute())
        try:
            root.mkdir(parents=True, exist_ok=True)
            return assert_writable(root)
        except OSError as error:
            raise ContractError(f"NCKH_TEST_ROOT is not writable: {root}: {error}; "
                                "set NCKH_TEST_ROOT to a writable directory you own") from error
    if _selected is not None:
        return assert_clean_ancestors(_selected)
    failures = []
    for candidate in _candidates():
        try:
            root = assert_clean_ancestors(candidate)
            root.mkdir(parents=True, exist_ok=True)
            if os.name != "nt" and root.stat().st_uid != os.getuid():
                raise ContractError("test root belongs to another user")
            assert_writable(root)
            _selected = root
            return root
        except (OSError, ContractError) as error:
            failures.append(f"{candidate}: {error}")
    raise ContractError("no isolated writable test root; set NCKH_TEST_ROOT: " + "; ".join(failures))
