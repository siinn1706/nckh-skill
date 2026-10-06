import argparse
import json
import os
import shutil
import sys
import tempfile
import uuid
from pathlib import Path

WORK = Path(__file__).resolve().parents[1]
PUBLIC = WORK
OUT = WORK / '.nckh-state' / 'global-deployment-runs'
sys.path.insert(0, str(PUBLIC / 'nckh-kit'))
from core.build import verify_bundle
from core.install import tree_hash
from core.native import agent_filename, configured_agent
from core.paths import atomic_json, digest_bytes, no_links


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--restage-owned', action='store_true')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    home = Path.home()
    state_path = WORK / '.nckh-state/global-kit-deployment.json'
    previous = json.loads(state_path.read_text()) if state_path.exists() else {'items': {}}
    entries = {}
    hosts = {}
    # Global directories are separate from project discovery and precedence checks.
    # Every destination is checked directly; no runtime dedup qualification is asserted.
    for host in ('codex', 'claude', 'cursor', 'agy'):
        bundle = PUBLIC / 'packages' / host
        manifest = verify_bundle(bundle)
        adapter = json.loads((bundle / 'adapter.json').read_text())
        roots = sorted({spec['global'] for spec in adapter['surfaces'].values()})
        for root in roots:
            for skill in manifest['skills']:
                source = bundle / 'skills' / skill['id']
                target = no_links(home / root / skill['id'])
                expected = tree_hash(source)
                if expected != skill['tree_hash']:
                    raise RuntimeError('Source drift: ' + str(source))
                entries[str(target)] = dict(source=str(source), expected=expected, kind='skill', host=host)
        agent_root = adapter.get('agent_global_root', adapter['agent_root'])
        for agent in manifest['agents']:
            instructions = (bundle / agent['instructions_path']).read_text(encoding='utf-8')
            content, _ = configured_agent(host, agent['role'], agent['description'], instructions,
                                          profile='balanced', capabilities={})
            target = no_links(home / agent_root / agent_filename(host, agent['id']))
            entries[str(target)] = dict(content=content, expected='file:' + digest_bytes(content.encode()),
                                       kind='native-agent', host=host)
        hosts[host] = dict(skills=len(manifest['skills']), agents=len(manifest['agents']), roots=roots,
                           source_revision=json.loads((bundle / 'source-lock.json').read_text())['revision'],
                           closure_hash=manifest['closure_hash'])
    conflicts = []
    for path, entry in entries.items():
        entry['before'] = tree_hash(path)
        if entry['before'] is not None and entry['before'] != entry['expected']:
            baseline = previous['items'].get(path, {}).get('expected')
            if baseline != entry['before']:
                conflicts.append(path)
    preview = dict(hosts=hosts, paths=len(entries), conflicts=conflicts,
                   native_discovery='not-tested', hooks='project-only',
                   duplicate_precedence='not-qualified; host controls visible project and global definitions')
    atomic_json(OUT / 'global-preview.json', preview)
    print(json.dumps(preview), flush=True)
    if conflicts:
        raise SystemExit('Existing edited or unowned NCKH files need review.')
    if not args.apply:
        return
    transaction = Path(tempfile.mkdtemp(prefix='global-backups-', dir=OUT))
    applied = []
    try:
        for number, (path, entry) in enumerate(entries.items()):
            target = Path(path)
            if tree_hash(target) != entry['before']:
                raise RuntimeError('Destination changed after preview: ' + path)
            if entry['before'] == entry['expected'] and not args.restage_owned:
                continue
            if args.restage_owned and previous['items'].get(path, {}).get('expected') != entry['before']:
                raise RuntimeError('Restaging requires unchanged owned content: ' + path)
            target.parent.mkdir(parents=True, exist_ok=True)
            # Normal Windows inheritance keeps host and sandbox readers available.
            stage = target.parent / ('.nckh-stage-' + uuid.uuid4().hex)
            stage.mkdir(mode=0o777)
            payload = stage / 'payload'
            try:
                if entry['kind'] == 'skill':
                    shutil.copytree(entry['source'], payload)
                else:
                    payload.write_bytes(entry['content'].encode('utf-8'))
                if tree_hash(payload) != entry['expected']:
                    raise RuntimeError('Staged content mismatch: ' + path)
                backup = transaction / str(number)
                if target.exists():
                    os.replace(target, backup)
                applied.append((target, backup, entry['expected']))
                os.replace(payload, target)
            finally:
                shutil.rmtree(stage)
        for path, entry in entries.items():
            if tree_hash(path) != entry['expected']:
                raise RuntimeError('Installed hash mismatch: ' + path)
        state = dict(schema_version=1, source=str(PUBLIC), hosts=hosts,
                     items={path: {key: value for key, value in entry.items() if key != 'content'}
                            for path, entry in entries.items()}, status='installed-and-hash-verified')
        atomic_json(state_path, state)
        atomic_json(OUT / 'global-install-receipt.json', state)
        print(json.dumps(dict(status=state['status'], paths=len(entries), hosts=hosts)), flush=True)
    except BaseException:
        for target, backup, expected in reversed(applied):
            if target.exists() and tree_hash(target) != expected:
                continue
            if target.is_dir():
                shutil.rmtree(target)
            elif target.exists():
                target.unlink()
            if backup.exists():
                os.replace(backup, target)
        raise


if __name__ == '__main__':
    main()
