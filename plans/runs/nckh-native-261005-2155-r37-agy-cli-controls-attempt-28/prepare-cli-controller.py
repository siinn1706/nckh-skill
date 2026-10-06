"""Adapt the retained AGY controller without modifying the candidate or old evidence."""

import ast
import hashlib
import json
import shutil
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / 'plans/runs/nckh-native-261005-1134-r36-agy-shell-attempt-01'
source = BASE / 'agy-shell-runtime.py'
original = source.read_bytes()
text = original.decode('utf8').split('\nif __name__ == "__main__":', 1)[0]
changes = {
    '.nckh-native-r36-agy-shell-01': '.nckh-native-r37-agy-cli-controls-28',
    'plans/runs/nckh-native-261005-1050-r36-shell-guard-attempt-02': 'plans/runs/nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-02',
    '1a471686c5b1e89e6838957161a8ae4c6787d46d227420d8644636062da90d30': '629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb',
    'native-agy-shell-r36': 'native-agy-cli-controls-r37',
    'nckh-native-r36-shell': 'nckh-native-r37-cli-controls',
    '"source_revision": 36': '"source_revision": 37',
    '"--print-timeout", "4m"': '"--print-timeout", "0"',
    'cwd=PROJECT, timeout=270': 'cwd=PROJECT, timeout=None',
}
for old, new in changes.items():
    assert old in text, old
    text = text.replace(old, new)
ast.parse(text)
target = RUN / 'agy-cli-runtime.py'
assert not target.exists()
(RUN / 'controller-preimage.py').write_bytes(original)
target.write_text(text, encoding='utf8')
for name, location in (
    ('agy-tool-observer.py', BASE / 'agy-tool-observer.py'),
    ('cursor-agy-model-dangerous-grant.json', BASE / 'cursor-agy-model-dangerous-grant.json'),
    ('cli-route-user-decision.json', WORK / 'plans/runs/nckh-native-261005-2125-r37-cursor-Write-faults-attempt-27/cli-route-user-decision.json'),
):
    assert not (RUN / name).exists()
    shutil.copyfile(location, RUN / name)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
(RUN / 'controller-adaptation.json').write_text(json.dumps({
    'source': str(source), 'source_sha256': sha(source), 'preserved_preimage_sha256': sha(RUN / 'controller-preimage.py'),
    'adapted_controller_sha256': sha(target), 'replacements': changes, 'candidate_modified': False,
    'direct_packaged_handlers': True, 'hook_timeout_seconds': 5,
    'model_turn_timeout': 'none; monitor exact owned process',
    'sandbox_models_failure': {'chunk_id': 'c2ccde', 'exit_code': 1, 'model_prompts': 0,
        'observed': ['global log access denied', 'sandbox proxy 127.0.0.1:9 refused'],
        'raw_tool_output': 'bounded and truncated; not a model authentication conclusion'},
}, indent=2) + '\n', encoding='utf8')
print(json.dumps({'status': 'controller-adapted', 'source_modified': False}))
