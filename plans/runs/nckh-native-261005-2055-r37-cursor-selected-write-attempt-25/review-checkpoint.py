"""Review actual evidence, scope, preservation and final plan state inline."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
read = lambda p: json.loads(p.read_text(encoding='utf8'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert not (RUN / 'inline-review.json').exists()
summary = read(RUN / 'native-selected-write-summary.json')
reconciliation = read(RUN / 'plan-reconciliation.json')
updates = read(RUN / 'doc-update.json')
verified = []
def walk(value):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and isinstance(value.get('sha256'), str):
            path = (WORK / value['path']).resolve()
            assert path.is_relative_to(WORK) and sha(path) == value['sha256'], value
            verified.append(value)
        for child in value.values():
            walk(child)
    elif isinstance(value, list):
        for child in value:
            walk(child)
walk(summary)
walk(read(RUN / 'case-selected-write.json'))
walk(reconciliation)
for row in updates['documents']:
    document = WORK / row['path']
    preimage = WORK / row['preimage']
    assert sha(document) == row['after_sha256'] and sha(preimage) == row['preimage_sha256'] == row['before_sha256']
    assert document.read_bytes().startswith(preimage.read_bytes())
assert summary['full_native_gate'] == 'unchecked' and not summary['default_all_tools_scope_qualified']
assert not summary['earlier_private_Read_failures_regraded']
assert summary['native_denied_tool'] == 'Write' and summary['private_successful_post_receipts'] == 0
assert reconciliation['done_tasks'] == 44 and reconciliation['total_tasks'] == 45
assert reconciliation['current_phase'] == 3 and reconciliation['state'] == 'active'
assert reconciliation['index_bookkeeping_preserved'] and reconciliation['verification_scope'] == 'structure-state-integrity only'
report = WORK / 'plans/reports/delivery-261005-2055-r37-cursor-selected-write.md'
text = report.read_text(encoding='utf8')
assert 'Read prerequisites' in text and 'không chứng minh confidential Read' in text
assert 'First verifier failure' in text and 'Preparation failure' in text
result = {'status': 'pass-with-native-matrix-limitations', 'review_type': 'controller-inline; no independent reviewer',
    'verified_binding_count': len(verified), 'unique_binding_count': len({p['path'] for p in verified}),
    'findings': [], 'checks': ['frozen oracle and prompt unchanged', 'actual native selected Write/denial and byte snapshots',
        'test-only matcher scope explicit', 'historical source/failures/reports preserved', 'matching cleanup and union process audit',
        'protected globals preserved', 'documents append-only with preimages', '44/45 P3 active and index bookkeeping preserved'],
    'limitations': ['Read outside selected matcher', 'remaining host/event/tool/fault matrix unqualified',
        'backend model attestation absent', 'terminal truncated; raw tool-return content not retained',
        'scientific/stable/release gates separate'],
    'source_changed': False, 'full_native_gate': 'unchecked', 'report_sha256': sha(report)}
with (RUN / 'inline-review.json').open('x', encoding='utf8') as stream:
    stream.write(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'verified_bindings': len(verified), 'unique_bindings': result['unique_binding_count']}))
