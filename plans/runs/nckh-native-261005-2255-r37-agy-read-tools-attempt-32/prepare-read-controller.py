"""Freeze independent read-tool controls after retaining unsupported multi-replace evidence."""

import ast
import hashlib
import json
import shutil
from pathlib import Path

RUN=Path(__file__).resolve().parent
WORK=RUN.parents[2]
BASE=WORK/'plans/runs/nckh-native-261005-2240-r37-agy-tool-controls-attempt-31'
read=lambda p:json.loads(p.read_text(encoding='utf8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert read(BASE/'verified-tool-delivery.json')['status']=='verified-two-replace-controls-and-native-unknown-multi-replace-counterevidence'
assert read(BASE/'process-final-audit.json')['tracked_live_count']==0
rows=[]
for name in ('agy-cli-runtime.py','owned-cli-command.py','audit-owned-processes.ps1','run-tool-controls.py'):
    source=BASE/name
    text=source.read_text(encoding='utf8')
    if name=='agy-cli-runtime.py':
        text=text.replace('.nckh-native-r37-agy-tool-controls-31','.nckh-native-r37-agy-read-tools-32')
        text=text.replace('native-agy-tool-controls-r37-31','native-agy-read-tools-r37-32')
    if name=='audit-owned-processes.ps1':
        text=text.replace('nckh-native-261005-2230-r37-agy-preflight-faults-attempt-30',
            'nckh-native-261005-2240-r37-agy-tool-controls-attempt-31')
        text=text.replace('prior native30 union audit','prior native31 union audit')
    if name=='run-tool-controls.py':
        text=text.replace('r37-agy-tool31-','r37-agy-read32-')
        original="PATH_FIELDS = {'replace_file_content':'TargetFile','multi_replace_file_content':'TargetFile',\n    'list_dir':'DirectoryPath','find_by_name':'SearchDirectory','grep_search':'SearchPath'}"
        assert original in text
        text=text.replace(original,"PATH_FIELDS = {'list_dir':'DirectoryPath','find_by_name':'SearchDirectory','grep_search':'SearchPath'}")
        text=text.replace("'maximum_model_turns':10","'maximum_model_turns':6")
        text=text.replace("'source_modified':False,\n        'safety_oracle'","'source_modified':False,\n        'collection_policy':'six independent cases; retain failed or unknown native controls without regrading, stop only on unexpected tool/process',\n        'safety_oracle'")
        original="assert result['status']=='verified-direct-tool-control','Frozen tool oracle failed; preserve evidence and stop dependent turns'"
        assert original in text
        text=text.replace(original,"assert len(terminal)==1 and terminal[0]['tool_name']==case['tool'] and row['exit_code']==0 and row['process_exited'],'Unexpected native route/process; preserve evidence and stop dependent turns'")
        text=text.replace("summary.update(status='recorded-ten-direct-agy-tool-controls',model_turns=10,model_retries=0)",
            "summary.update(status='recorded-six-native-agy-read-tool-outcomes',model_turns=6,model_retries=0,\n            verified_controls=sum(r['status']=='verified-direct-tool-control' for r in summary['results']),\n            failed_frozen_oracles=sum(r['status']=='failed-frozen-tool-oracle-retained' for r in summary['results']))")
    if name.endswith('.py'):
        ast.parse(text)
    assert not (RUN/name).exists()
    (RUN/name).write_text(text,encoding='utf8')
    rows.append({'source':str(source),'source_sha256':sha(source),'after_sha256':sha(RUN/name)})
for name in ('agy-tool-observer.py','cursor-agy-model-dangerous-grant.json','cli-route-user-decision.json'):
    shutil.copyfile(BASE/name,RUN/name)
(RUN/'controller-adaptation.json').write_text(json.dumps({'stage':'before admission/new independent frozen brief',
    'source_modified':False,'changes':rows,'previous_evidence_sha256':sha(BASE/'verified-tool-delivery.json'),
    'previous_failed_oracle_regraded':False,'scope':'six remaining read-tool public/private controls; unsupported multi-replace remains not-callable/unqualified',
    'collection_policy':'each new case retains its original allow/deny oracle; independent cases continue even when one records native unknown or failed oracle'},indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':'prepared-independent-read-tool-controller','previous_oracle_regraded':False}))
