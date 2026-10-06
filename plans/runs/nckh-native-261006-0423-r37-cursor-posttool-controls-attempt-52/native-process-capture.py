"""Controller capture for future native tests: validate process generations and bound atomic-write retries."""
import importlib.util
import json
import time
import uuid
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2].resolve()
spec = importlib.util.spec_from_file_location("retained_owned_primitives", RUN / "owned-cli-command.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
creation_ticks = base.creation_ticks


def select_temporal_descendants(rows, root_pid, expected_creation_ticks):
    by_pid = {}
    for row in rows:
        if row["pid"] in by_pid:
            raise ValueError("Ambiguous process generations in one live snapshot")
        by_pid[row["pid"]] = row
    root = by_pid.get(root_pid)
    if root is None or root["creation_filetime_ticks"] != expected_creation_ticks:
        raise ValueError("Owned root identity changed or is not observable")
    selected = {root_pid: root}
    while True:
        added = {}
        for pid, row in by_pid.items():
            parent = selected.get(row["parent_pid"])
            if pid not in selected and parent is not None and row["creation_filetime_ticks"] >= parent["creation_filetime_ticks"]:
                added[pid] = row
        if not added:
            return list(selected.values())
        selected.update(added)


def tree(root_pid, expected_creation_ticks):
    if creation_ticks(root_pid) != expected_creation_ticks:
        raise ValueError("Owned root identity changed before snapshot")
    rows = base.tree(root_pid)
    selected = select_temporal_descendants(rows, root_pid, expected_creation_ticks)
    if creation_ticks(root_pid) != expected_creation_ticks:
        raise ValueError("Owned root identity changed during snapshot")
    return selected


def save(path, data):
    path = Path(path).resolve()
    if not path.is_relative_to(WORK):
        raise ValueError("Controller evidence target is outside the owned workspace")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".writing-" + uuid.uuid4().hex)
    with temporary.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    delays = (0, 0.025, 0.05, 0.1, 0.2, 0.4)
    for index, delay in enumerate(delays):
        if delay:
            time.sleep(delay)
        try:
            temporary.replace(path)
            return
        except PermissionError as error:
            if getattr(error, "winerror", None) not in {5, 32, 33} or index == len(delays) - 1:
                raise
    raise AssertionError("Atomic write did not reach a terminal outcome")
