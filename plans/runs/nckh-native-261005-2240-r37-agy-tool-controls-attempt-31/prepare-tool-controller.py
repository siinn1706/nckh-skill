"""Reuse the verified direct AGY controller for the remaining mapped file tools."""

import ast
import hashlib
import json
import shutil
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / 'plans/runs/nckh-native-261005-2210-r37-agy-cli-controls-attempt-29'
LAST = WORK / 'plans/runs/nckh-native-261005-2230-r37-agy-preflight-faults-attempt-30'
read = lambda p: json.loads(p.read_text(encoding='utf8'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert read(LAST / 'verified-preflight-delivery.json')['status'] == 'verified-five-native-agy-Write-fault-denials'
assert read(LAST / 'process-final-audit.json')['tracked_live_count'] == 0
changes = []
for name in ('agy-cli-runtime.py', 'owned-cli-command.py', 'audit-owned-processes.ps1'):
    source = BASE / name
    text = source.read_text(encoding='utf8')
    if name == 'agy-cli-runtime.py':
        text = text.replace('.nckh-native-r37-agy-cli-controls-29', '.nckh-native-r37-agy-tool-controls-31')
        text = text.replace('native-agy-cli-controls-r37-29', 'native-agy-tool-controls-r37-31')
    if name == 'audit-owned-processes.ps1':
        text = text.replace('nckh-native-261005-2155-r37-agy-cli-controls-attempt-28',
            'nckh-native-261005-2230-r37-agy-preflight-faults-attempt-30')
        text = text.replace('prior native28 union audit', 'prior native30 union audit')
    if name.endswith('.py'):
        ast.parse(text)
    assert not (RUN/name).exists()
    (RUN/name).write_text(text, encoding='utf8')
    changes.append({'source': str(source), 'source_sha256': sha(source), 'after_sha256': sha(RUN/name)})
for name in ('agy-tool-observer.py', 'cursor-agy-model-dangerous-grant.json', 'cli-route-user-decision.json'):
    shutil.copyfile(BASE/name, RUN/name)
(RUN/'controller-adaptation.json').write_text(json.dumps({'changes': changes, 'source_modified':False,
    'direct_packaged_handlers':True,'all_hook_timeouts_seconds':5,'prior_process_audit_sha256':sha(LAST/'process-final-audit.json')},indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':'prepared-direct-tool-controller','source_modified':False}))
