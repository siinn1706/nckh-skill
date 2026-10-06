"""Reindex canonical plan files while preserving lifecycle and maintainer bookkeeping."""

import hashlib
import json
import os
import re
import sqlite3
import subprocess
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / 'plans/261004-0047-nckh-research-data-hooks-writing'
RUNTIME = WORK / 'plans/.agentkit-runtime'
DATABASE = RUNTIME / 'plans/plans.db'
AK = Path(r'C:/Users/USER\bin\ak.exe')
ENV = {**os.environ, 'AGENTKIT_HOME': str(RUNTIME)}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {'path': p.relative_to(WORK).as_posix(), 'sha256': sha(p)}
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))


def write_new(path, value):
    path.parent.mkdir(exist_ok=True)
    with path.open('x', encoding='utf8') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def snapshot():
    with sqlite3.connect(DATABASE.as_uri() + '?mode=ro', uri=True) as database:
        database.row_factory = sqlite3.Row
        return {'plans': [dict(row) for row in database.execute('SELECT id,plan_dir,state,issue_number,root_comment_id,linked_pr,current_phase FROM plans')],
            'phase_bookkeeping': [dict(row) for row in database.execute('SELECT plan_id,n,comment_id,rev,notes,evidence,acceptance FROM phases ORDER BY plan_id,n')]}


def invoke(name, args):
    result = subprocess.run([str(AK), *args], cwd=WORK, env=ENV, capture_output=True, text=True, encoding='utf8', timeout=60)
    write_new(RUN / 'commands' / ('reconcile-' + name + '.json'), {'command': [str(AK), *args],
        'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
    assert result.returncode == 0, (name, result.stderr)
    return json.loads(result.stdout) if '--json' in args else result.stdout


assert not (RUN / 'plan-reconciliation.json').exists()
assert read(RUN / 'verified-cli-delivery.json')['status'] == 'verified-five-direct-agy-controls-with-previous-byte-failure-retained'
assert read(RUN / 'doc-update.json')['status'] == 'appended-native26-29-evidence'
backup = RUN / 'plan-store-before-reindex.sqlite'
assert not backup.exists()
with sqlite3.connect(DATABASE.as_uri() + '?mode=ro', uri=True) as source, sqlite3.connect(backup) as target:
    source.backup(target)
    assert target.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
before = snapshot()
write_new(RUN / 'index-bookkeeping-before-reindex.json', before)
write_new(RUN / 'plan-store-preimage.json', {'database': str(DATABASE), 'backup': bind(backup), 'integrity_check': 'ok'})
documents = [PLAN / 'plan.md', PLAN / 'phase-03-portable-hooks.md', PLAN / 'phase-04-integration-and-personal-acceptance.md',
    WORK / 'plans/journals/2026-10-05-cursor-native-timeout-controls-and-r37-repair.md',
    WORK / 'plans/reports/delivery-261005-2120-r37-agy-window-inventory.md',
    WORK / 'plans/reports/delivery-261005-2125-r37-cursor-write-faults.md',
    WORK / 'plans/reports/delivery-261005-2155-r37-agy-cli-byte-failure.md',
    WORK / 'plans/reports/delivery-261005-2210-r37-agy-cli-controls.md']
links = []
for document in documents:
    for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', document.read_text(encoding='utf8')):
        if target.startswith(('https://', 'http://', 'mailto:', '#')):
            continue
        assert (document.parent / target.strip('<>').split('#', 1)[0]).resolve().exists(), (document, target)
        links.append({'document': document.relative_to(WORK).as_posix(), 'target': target})
write_new(RUN / 'local-link-checks.json', {'status': 'pass', 'links_checked': len(links), 'links': links})
invoke('help', ['plan', '--help'])
for verb in ('validate', 'parse', 'reindex'):
    invoke(verb + '-help', ['plan', verb, '--help'])
invoke('validate', ['plan', 'validate', str(PLAN), '--json'])
parsed = invoke('parse', ['plan', 'parse', str(PLAN), '--json'])['data']
assert parsed['status'] == 'in-progress' and parsed['done_tasks'] == 44 and parsed['total_tasks'] == 45
assert [(p['number'], p['done_tasks'], p['total_tasks']) for p in parsed['phases']] == [(1,13,13),(2,9,9),(3,10,11),(4,12,12)]
invoke('reindex-preview', ['plan', 'reindex', '--path', str(WORK), '--json'])
invoke('reindex-apply', ['plan', 'reindex', '--path', str(WORK), '--apply', '--json'])
after = snapshot()
assert before == after
selected = [p for p in after['plans'] if Path(p['plan_dir']).resolve() == PLAN.resolve()]
assert len(selected) == 1 and selected[0]['state'] == 'active' and selected[0]['current_phase'] == 3
write_new(RUN / 'index-bookkeeping-after-reindex.json', after)
write_new(RUN / 'plan-reconciliation.json', {'status': 'verified-r37-native26-29-reconciled-gate-open',
    'plan': str(PLAN), 'done_tasks': 44, 'total_tasks': 45, 'current_phase': 3, 'state': 'active',
    'full_native_gate': 'unchecked', 'SQLite_backup': bind(backup), 'index_bookkeeping_preserved': True,
    'links_checked': len(links), 'documents': [bind(p) for p in documents],
    'current_cli_evidence': bind(RUN / 'verified-cli-delivery.json'), 'current_process_audit': bind(RUN / 'process-final-audit.json'),
    'previous_reconciliation': bind(WORK / 'plans/runs/nckh-native-261005-2055-r37-cursor-selected-write-attempt-25/plan-reconciliation.json'),
    'previous_hash_scope': 'historical documents; receipts preserved', 'verification_scope': 'structure-state-integrity only',
    'AgentWiki_publish': 'skipped', 'verifier': bind(Path(__file__))})
print(json.dumps({'status': 'reconciled-native-gate-open', 'done_tasks': 44, 'total_tasks': 45, 'links_checked': len(links)}))
