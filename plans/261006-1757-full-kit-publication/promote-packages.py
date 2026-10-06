import json
import shutil
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / 'github-publication/nckh-kit'))
from core.build import verify_bundle

for host in ('claude', 'codex', 'cursor', 'agy'):
    source = root / 'publication-r41' / host
    manifest = verify_bundle(source)
    assert manifest['resource_access'] == 'on' and manifest['plugin']['projected']
    target = root / 'github-publication/packages' / host
    assert target.resolve().is_relative_to((root / 'github-publication/packages').resolve())
    expected = {row['path'] for row in manifest['files']} | {'manifest.json', 'source-lock.json'}
    for path in target.rglob('*'):
        if path.is_file() and path.relative_to(target).as_posix() not in expected:
            path.unlink()
    for relative in sorted(expected):
        output = target / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / relative, output)
    verify_bundle(target)
    print(json.dumps({'host': host, 'files': len(expected), 'resources': len(manifest['resources'])}))
