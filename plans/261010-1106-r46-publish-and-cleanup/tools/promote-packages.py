"""Promote the verified reproducible packages without discarding the old tree."""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "nckh-kit"))
from core.build import load_json, verify_bundle, verify_source_lock
from core.paths import no_links


def main():
    state = ROOT / ".nckh-state/release-r46-261010"
    stage = no_links(state / "staged-packages")
    target = no_links(ROOT / "packages")
    backup = no_links(state / "previous-packages")
    lock = verify_source_lock(ROOT / "nckh-kit")
    observed = load_json(state / "commands/reproducible-build/stdout.txt")
    expected = {row["host"]: row["closure_hash"] for row in observed["artifacts"]}
    if lock["revision"] != "46" or backup.exists() or set(expected) != {"claude", "codex", "cursor", "agy"}:
        raise RuntimeError("unexpected revision, host inventory or existing backup")
    for host, closure in expected.items():
        manifest = verify_bundle(stage / host)
        if (manifest["closure_hash"] != closure or manifest["resource_access"] != "on"
                or load_json(stage / host / "source-lock.json") != lock):
            raise RuntimeError("staged package differs from the reproducibility check")
    os.replace(target, backup)
    try:
        os.replace(stage, target)
    except BaseException:
        os.replace(backup, target)
        raise
    print(json.dumps({"status": "promoted", "revision": "46", "hosts": sorted(expected),
                      "previous_packages_preserved": True}))


if __name__ == "__main__":
    main()
