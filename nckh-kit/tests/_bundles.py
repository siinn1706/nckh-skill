"""Build each distinct test bundle once per process and hand every caller a private copy.

``build_host`` is the slowest step in the suite and many tests only need an ordinary bundle as
input. The first request for a ``(root, host, kits, include_plugin, include_resources)`` key runs
the real ``build_host`` into a cache directory under the isolated test root; every request copies
that tree to the caller's destination. The cached tree is never handed out, so tests may tamper
with their copy freely. Each copy is compared with the tree hash recorded right after the build,
which fails the caller if the cache or the copy ever differs from the original build output.
"""
import atexit
import shutil
from copy import deepcopy
from pathlib import Path

from core.build import build_host
from core.install import tree_hash
from core.paths import no_links, temporary_tree
from tests._lab import lab_root

ROOT = Path(__file__).resolve().parents[1]
_cache = {}
_context = None
_parent = None


def _cache_parent():
    global _context, _parent
    if _parent is None:
        _context = temporary_tree(lab_root())
        _parent = _context.__enter__()
        atexit.register(_release)
    return _parent


def _release():
    global _context, _parent
    if _context is not None:
        context, _context, _parent = _context, None, None
        context.__exit__(None, None, None)
        _cache.clear()


def copy_bundle(destination, host, kits, *, include_plugin=False, include_resources=True, root=ROOT):
    """Copy a real bundle for ``host``/``kits`` to ``destination`` and return its build manifest.

    ``destination`` must not exist yet or must be an empty directory, matching ``build_host``.
    """
    root = Path(root).resolve()
    key = (str(root), host, tuple(kits), bool(include_plugin), bool(include_resources))
    if key not in _cache:
        output = _cache_parent() / f"bundle-{len(_cache)}" / host
        manifest = build_host(root, host, list(kits), output,
                              include_plugin=include_plugin, include_resources=include_resources)
        _cache[key] = (output, manifest, tree_hash(output))
    source, manifest, expected = _cache[key]
    destination = no_links(destination)
    if destination.exists():
        if any(destination.iterdir()):
            raise AssertionError(f"bundle copy destination is not empty: {destination}")
        destination.rmdir()
    shutil.copytree(source, destination)
    if tree_hash(destination) != expected:
        raise AssertionError(f"cached {host} bundle differs from its original build output")
    return deepcopy(manifest)
