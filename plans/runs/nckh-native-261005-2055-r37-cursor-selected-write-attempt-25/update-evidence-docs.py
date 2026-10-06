"""Append revision-bound native evidence while preserving historical plan records."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PLAN = WORK / 'plans/261004-0047-nckh-research-data-hooks-writing'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text(encoding='utf8'))
summary = read(RUN / 'native-selected-write-summary.json')
assert summary['status'] == 'verified-scoped-public-Write-and-private-Write-prevention'
assert not (RUN / 'doc-update.json').exists()
index = ('\n[Selected Write25](../reports/delivery-261005-2055-r37-cursor-selected-write.md) verifies exact public Write and native private Write denial/unchanged bytes with test-only `^Write$` matcher. Read prerequisites are outside that selected scope; earlier private Read failures retain their original status. One turn/final marker/native exit0, cleanup26/preserved786/zero owned processes; source r37 unchanged. Full native matrix remains unchecked/44 of45.\n')
phase = ('\n## Scoped native Write control\n\n'
    '[Selected Write25](../reports/delivery-261005-2055-r37-cursor-selected-write.md) / [bindings](../reports/delivery-261005-2055-r37-cursor-selected-write.json) adds one actual public Write/allow/exact bytes and one actual private Write/permission_denied/private-holdout-credential-path with nonempty native ID/version/path. Private bytes remain unchanged and no successful private post receipt exists. Direct packaged r37 handlers use preToolUse20s/failClosed=true; tool hooks select `^Write$`, leaving authorized synthetic Read prerequisites outside selected coverage. This is scoped Write evidence, not default-all-tools or confidential-Read enforcement.\n\n'
    'One model turn/submission, no retry/fault injection, final marker/native exit0. Five total policy receipts/four after control selection and one native failure receipt; public post artifact QA remains pending. Cleanup26/preserved786/protected global configs unchanged; union start/before-stop audit40 identities leaves zero matching/tracked-live and retains exact AGY identity. Initial preparation encoding error occurred before staging/submission; initial verifier failed because the AGY audit compared UTC ticks with parsed local ticks. Both failures/preimages/raw records remain; corrected UTC audit and verifier exit0 without resubmission. Source r37/281 pins/hash unchanged; previous native16/18 private Read outcomes stay historical. Full native task remains unchecked/44 of45.\n')
integration = ('\n## Additional evidence — scoped r37 private Write\n\n'
    '[Selected Write25](../reports/delivery-261005-2055-r37-cursor-selected-write.md) verifies public exact Write and private native Write prevention on CLI2026.09.15/Grok4.7/context500k/xhigh/fastfalse. `^Write$` matcher narrows this test to Write; synthetic Read prerequisites are outside selected hooks. One turn, five total policy receipts/one native failure, private unchanged/final marker/native exit0. Cleanup26/preserved786/final zero owned processes; controller encoding/UTC comparison failures and corrections retained. Source/local checkpoint/owner exact r29 acceptance remain unchanged; P4 retains12/12, plan44/45 and P3 native task stays unchecked.\n')
journal = ('\n## Scoped native Write control\n\n'
    '[Write25](../reports/delivery-261005-2055-r37-cursor-selected-write.md) adds the previously missing actual private Write observation: exact public mutation succeeds; selected private Write is natively denied/private-holdout-credential-path and leaves bytes unchanged. Test-only `^Write$` matcher allows bounded synthetic Read prerequisites outside this coverage. One granted Grok4.7/500k/xhigh/fastfalse turn; no model retry/source change/regrading of private Read failures. Native exit0, cleanup26/preserved786 and union audit40 identities with zero matching/tracked-live. Preparation codec-spelling error and UTC/local timestamp comparison error are retained with preimages, then repaired before dependent work; final verifier exit0. Full native task stays open/44 of45/P3 active.\n')
documents = [(PLAN / 'plan.md', 'plan.md', index),
    (PLAN / 'phase-03-portable-hooks.md', 'phase-03-portable-hooks.md', phase),
    (PLAN / 'phase-04-integration-and-personal-acceptance.md', 'phase-04-integration-and-personal-acceptance.md', integration),
    (WORK / 'plans/journals/2026-10-05-cursor-native-timeout-controls-and-r37-repair.md', 'journal.md', journal)]
records = []
for document, name, text in documents:
    preimage = RUN / 'doc-preimages' / name
    assert document.read_bytes() == preimage.read_bytes()
    before = sha(document)
    with document.open('ab') as stream:
        stream.write(text.encode())
    assert document.read_bytes().startswith(preimage.read_bytes())
    records.append({'path': document.relative_to(WORK).as_posix(), 'before_sha256': before, 'after_sha256': sha(document),
                    'preimage': preimage.relative_to(WORK).as_posix(), 'preimage_sha256': sha(preimage)})
with (RUN / 'doc-update.json').open('x', encoding='utf8') as stream:
    stream.write(json.dumps({'status': 'appended-scoped-native-evidence', 'documents': records,
        'source_changed': False, 'task_status_changed': False, 'full_native_gate': 'unchecked'}, indent=2) + '\n')
print(json.dumps({'status': 'appended-scoped-native-evidence', 'documents': len(records), 'full_native_gate': 'unchecked'}))
