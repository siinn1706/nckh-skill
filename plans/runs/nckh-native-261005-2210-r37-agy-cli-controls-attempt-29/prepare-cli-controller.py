"""Freeze a separate line-terminated control batch, retaining the previous byte oracle failure."""

import ast
import hashlib
import json
import shutil
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / 'plans/runs/nckh-native-261005-2155-r37-agy-cli-controls-attempt-28'
read = lambda p: json.loads(p.read_text(encoding='utf8'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
previous = read(BASE / 'native-cli-summary.json')
assert len(previous['results']) == 1 and previous['results'][0]['status'] == 'failed-frozen-oracle-retained'
assert read(BASE / 'cleanup.json')['status'] == 'pass'
assert read(BASE / 'process-final-audit.json')['tracked_live_count'] == 0
changes = {}
for name in ('agy-cli-runtime.py', 'run-cli-controls.py', 'owned-cli-command.py', 'audit-owned-processes.ps1'):
    old = BASE / name
    text = old.read_text(encoding='utf8')
    if name == 'agy-cli-runtime.py':
        text = text.replace('.nckh-native-r37-agy-cli-controls-28', '.nckh-native-r37-agy-cli-controls-29')
        text = text.replace('native-agy-cli-controls-r37"', 'native-agy-cli-controls-r37-29"')
    if name == 'run-cli-controls.py':
        text = text.replace('r37-agy-cli28-', 'r37-agy-cli29-')
        text = text.replace("('NCKH_AGY_R37_' + case['name'].upper().replace('-', '_')).encode().hex()",
            "('NCKH_AGY_R37_' + case['name'].upper().replace('-', '_') + '\\n').encode().hex()")
        original = "instructions = ('TargetFile: ' + str(path) + '. Overwrite: true. CodeContent is exactly '\n                    + bytes.fromhex(case['requested_hex']).decode() + ' with no trailing newline. ')"
        revised = "instructions = ('TargetFile: ' + str(path) + '. Overwrite: true. CodeContent must be the decoded JSON string '\n                    + json.dumps(bytes.fromhex(case['requested_hex']).decode())\n                    + '. It ends with exactly one LF byte. Preserve these exact content bytes. ')"
        assert original in text
        text = text.replace(original, revised)
    if name == 'audit-owned-processes.ps1':
        text = text.replace('plans\\runs\\nckh-native-261005-2125-r37-cursor-Write-faults-attempt-27\\final-process-audit-attempt-02.json',
            'plans\\runs\\nckh-native-261005-2155-r37-agy-cli-controls-attempt-28\\process-final-audit.json')
        text = text.replace('$taskTicks = ([DateTimeOffset]::Parse($taskRow.expected)).UtcDateTime.ToFileTimeUtc()',
            '$taskTicks = $taskRow.creation_filetime_ticks')
        text = text.replace('prior native27 audit', 'prior native28 union audit')
    if name.endswith('.py'):
        ast.parse(text)
    assert not (RUN / name).exists()
    (RUN / name).write_text(text, encoding='utf8')
    changes[name] = {'source': str(old), 'source_sha256': sha(old), 'after_sha256': sha(RUN / name)}
for name in ('agy-tool-observer.py', 'cursor-agy-model-dangerous-grant.json', 'cli-route-user-decision.json'):
    shutil.copyfile(BASE / name, RUN / name)
(RUN / 'controller-adaptation.json').write_text(json.dumps({'stage': 'before admission and new brief',
    'previous_failed_batch': str(BASE), 'previous_summary_sha256': sha(BASE / 'native-cli-summary.json'),
    'previous_failed_bytes': {'requested': 'NCKH_AGY_R37_PUBLIC_WRITE', 'actual': 'NCKH_AGY_R37_PUBLIC_WRITE\\n'},
    'previous_raw_and_oracle_preserved': True, 'previous_grade_changed': False,
    'new_content_contract': 'explicit JSON decoded string, exactly one final LF byte',
    'cause_of_previous_added_newline': 'not proven; native tool frames omit CodeContent',
    'changes': changes, 'candidate_modified': False, 'independent_frozen_batch': True,
    'version_drift': {'observed_before': '1.2.16', 'observed_at_previous_prepare': '1.2.17',
        'controller_update_command': 'not-invoked', 'cause': 'unverified'}}, indent=2) + '\n', encoding='utf8')
print(json.dumps({'status': 'prepared-separate-line-terminated-controller', 'candidate_modified': False}))
