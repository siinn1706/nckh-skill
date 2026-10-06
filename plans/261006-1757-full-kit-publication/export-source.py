import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parents[2]
source = root / 'nckh-kit'
target = root / 'github-publication' / 'nckh-kit'
lock = json.loads((source / 'core/registry/source-lock/source-lock.json').read_text())
paths = set(lock['files']) | {'core/registry/source-lock/source-lock.json'}
for relative in sorted(paths):
    origin = source / relative
    output = target / relative
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(origin, output)
print(f"Exported {len(paths)} pinned source members, revision {lock['revision']}.")
