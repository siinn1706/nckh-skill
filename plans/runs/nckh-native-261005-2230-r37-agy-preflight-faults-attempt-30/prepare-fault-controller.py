"""Adapt test instrumentation at the packaged five-second native handler bound."""

import ast
import hashlib
import json
import shutil
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / 'plans/runs/nckh-native-261005-2210-r37-agy-cli-controls-attempt-29'
read = lambda p: json.loads(p.read_text(encoding='utf8'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert read(BASE / 'verified-cli-delivery.json')['status'] == 'verified-five-direct-agy-controls-with-previous-byte-failure-retained'
assert read(BASE / 'process-final-audit.json')['tracked_live_count'] == 0
records = []
for name in ('agy-cli-runtime.py', 'owned-cli-command.py', 'audit-owned-processes.ps1'):
    source = BASE / name
    text = source.read_text(encoding='utf8')
    if name == 'agy-cli-runtime.py':
        text = text.replace('.nckh-native-r37-agy-cli-controls-29', '.nckh-native-r37-agy-preflight-faults-30')
        text = text.replace('native-agy-cli-controls-r37-29', 'native-agy-preflight-faults-r37-30')
        text = text.replace('nckh-native-r37-cli-controls', 'nckh-native-r37-preflight-faults')
        text = text.replace('"timeout": 20', '"timeout": 5')
        text = text.replace('"timeout_seconds": 5 if direct else 20', '"timeout_seconds": 5')
    if name == 'audit-owned-processes.ps1':
        text = text.replace('nckh-native-261005-2155-r37-agy-cli-controls-attempt-28',
            'nckh-native-261005-2210-r37-agy-cli-controls-attempt-29')
        text = text.replace('prior native28 union audit', 'prior native29 union audit')
    if name.endswith('.py'):
        ast.parse(text)
    assert not (RUN / name).exists()
    (RUN / name).write_text(text, encoding='utf8')
    records.append({'source': str(source), 'source_sha256': sha(source), 'after_sha256': sha(RUN / name)})
for name in ('agy-tool-observer.py', 'cursor-agy-model-dangerous-grant.json', 'cli-route-user-decision.json'):
    shutil.copyfile(BASE / name, RUN / name)
(RUN / 'controller-adaptation.json').write_text(json.dumps({'source_revision': 37,
    'source_modified': False, 'instrumentation': 'test-only callback fault observer',
    'outer_handler_timeout_seconds': 5, 'inner_runner_timeout_seconds': 5,
    'fault_origin': 'controller-injection-after-genuine-native-callback',
    'changes': records, 'previous_checkpoint_sha256': sha(BASE / 'verified-cli-delivery.json')}, indent=2) + '\n', encoding='utf8')
print(json.dumps({'status': 'prepared-five-second-fault-controller', 'source_modified': False}))
