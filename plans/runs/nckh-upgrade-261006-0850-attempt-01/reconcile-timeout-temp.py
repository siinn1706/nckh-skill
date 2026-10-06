"""Record and remove two exact interrupted-suite staging roots."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
from datetime import datetime, timezone

RUN = Path(__file__).resolve().parent
KIT = RUN.parents[2] / "nckh-kit"
sys.path.insert(0, str(KIT))
from core.paths import digest_file, no_links

parent = no_links(Path(tempfile.gettempdir())).resolve()
roots = [parent / "nckh-0d27267dd5f74a1f8529ca8158ac4026", parent / "nckh-89b7bf7947d34d75b2f87b7f871079e2"]
attempt = json.loads((RUN / "p7-command-deterministic.json").read_text(encoding="utf-8"))
start = datetime.fromisoformat(attempt["started_at"]).timestamp()
end = datetime.fromisoformat(attempt["ended_at"]).timestamp()
rows = []
for root in roots:
    assert no_links(root).resolve().parent == parent and root.is_dir()
    created = root.stat().st_birthtime if hasattr(root.stat(), "st_birthtime") else root.stat().st_ctime
    assert start <= created <= end
    files, directories = {}, []
    for path in sorted(root.rglob("*")):
        assert no_links(path).resolve().is_relative_to(root.resolve())
        if path.is_file():
            files[path.relative_to(root).as_posix()] = digest_file(path)
        else:
            assert path.is_dir()
            directories.append(path.relative_to(root).as_posix())
    expected_child = "nckh-806e34310ab94d6ea47461057596fce3"
    if root == roots[0]:
        assert {path.name for path in root.iterdir()} == {expected_child}
        assert all(name.startswith(expected_child + "/") for name in files)
    else:
        assert not files and not directories
    rows.append({"root": str(root), "created_at": datetime.fromtimestamp(created, timezone.utc).isoformat(),
                 "owner": str(RUN), "context": "owned full-suite timeout; resource closure pair and interrupted nested build staging",
                 "files": files, "directories": directories, "no_reparse": True, "within_exact_temp_parent": True})

with (RUN / "p7-timeout-temp-before-cleanup.json").open("x", encoding="utf-8") as stream:
    stream.write(json.dumps({"attempt": attempt, "roots": rows, "process_observation": "Get-Process python,pythonw found no live process before this cleanup"}, indent=2) + "\n")

for row in rows:
    root = Path(row["root"])
    assert no_links(root).resolve().parent == parent
    observed = {path.relative_to(root).as_posix(): digest_file(no_links(path)) for path in root.rglob("*") if path.is_file()}
    assert observed == row["files"]
    for path in root.rglob("*"):
        no_links(path)
    shutil.rmtree(root)
    assert not root.exists()
with (RUN / "p7-timeout-temp-cleanup.json").open("x", encoding="utf-8") as stream:
    stream.write(json.dumps({"roots": [row["root"] for row in rows], "removed": True,
                             "retained_precleanup_snapshot": "p7-timeout-temp-before-cleanup.json", "owned_live": 0}, indent=2) + "\n")
print(json.dumps({"removed_exact_owned_roots": len(rows), "recorded_files": sum(len(row["files"]) for row in rows)}))
