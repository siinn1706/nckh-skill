"""Verify the model-only refusal while preserving the missing native tool evidence."""

import hashlib
import json
import sys
from pathlib import Path

RUN=Path(__file__).resolve().parent
WORK=RUN.parents[2]
PROJECT=WORK/'plans/runs/nckh-native-261005-0005-r34-attempt-01/projects/agy-model'
sys.path.insert(0,str(WORK/'nckh-kit'))
from core.build import verify_source_lock
from core.paths import contained,digest_record
EXPECTED='629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bind=lambda p:{'path':p.relative_to(WORK).as_posix(),'sha256':sha(p)}


def bound(row):
    path=contained(WORK,row['path'])
    assert sha(path)==row['sha256']
    return path


assert not (RUN/'verified-read-attempt.json').exists()
assert digest_record(verify_source_lock(WORK/'nckh-kit'))==EXPECTED
summary=read(RUN/'native-tool-summary.json')
brief=read(bound(summary['frozen_brief']))
assert len(brief['cases'])==6 and len(summary['results'])==1 and summary['status']=='running'
assert read(RUN/'native-tool-failure.json')['completed_cases']==1
oracle=brief['cases'][0]
observation=summary['results'][0]
assert oracle['name']==observation['attempt']=='list-dir-public'
assert observation['status']=='failed-frozen-tool-oracle-retained'
attempt=read(bound(observation['receipt']))
assert attempt['source_revision']==37 and attempt['source_lock_hash']==EXPECTED and attempt['direct']
command=read(bound(attempt['command']))
assert command['exit_code']==attempt['exit_code']==0 and command['process_exited'] and attempt['process_exited']
assert command['timeout_seconds'] is None and command['capture_errors']==[]
stdout=RUN/'commands/agy-tools-list-dir-public.stdout.txt'
assert sha(stdout)==command['stdout_sha256']
frames=[json.loads(line) for line in stdout.read_text(encoding='utf8').splitlines()]
assert frames==attempt['native_frames']
init=[f for f in frames if f.get('event')=='init']
final=[f for f in frames if f.get('event')=='result']
assert len(init)==len(final)==1
assert init[0]['init']['model']=='gemini-3.8-flash-medium' and init[0]['init']['permission_mode']=='always-proceed'
assert Path(init[0]['init']['cwd']).resolve()==PROJECT.resolve()
assert 'list_dir' in init[0]['init']['tools']
assert final[0]['result']['status']=='SUCCESS' and final[0]['result']['num_turns']==1
response=final[0]['result']['response']
assert 'list_dir' in response and 'not available' in response and 'ORACLE_ATTEMPT_FINISHED' in response
all_tools=[f['step_update'] for f in frames if f.get('event')=='step_update'
    and (f['step_update'].get('step_type')=='tool' or 'tool_name' in f['step_update'] or 'tool_info' in f['step_update'])]
assert all_tools==attempt['terminal_tools']==[]
policies=[read(bound(row)) for row in attempt['policy_receipts']]
assert policies==[row['receipt'] for row in attempt['policy_receipts']]
assert {p['phase'] for p in policies}=={'advisory','stop'}
assert all(p['session_key']==digest_record(init[0]['conversation_id']) for p in policies)
initial=hashlib.sha256(bytes.fromhex(oracle['initial_hex'])).hexdigest()
assert attempt['before']==attempt['after']=={'marker.txt':initial}
assert sha(contained(PROJECT,oracle['fixture']))==initial
cleanup=read(RUN/'cleanup.json')
audit=read(RUN/'process-final-audit.json')
assert cleanup['status']=='pass' and len(cleanup['removed_members'])==26 and not cleanup['config_callable']
assert cleanup['historical_members_unchanged']==383 and not cleanup['global_direct_write']
assert all(row['sha256']==row['current_sha256'] for row in cleanup['protected_global_config'])
assert not (PROJECT/'.agents/hooks.json').exists()
assert audit['matching_count']==audit['tracked_live_count']==0 and not audit['process_stop_performed']
record={'status':'verified-recorded-model-only-list-dir-refusal-native-control-unqualified',
    'source_revision':37,'source_lock_hash':EXPECTED,'host_version':read(RUN/'native-metadata.json')['version'],
    'model_observed':'gemini-3.8-flash-medium','effort_requested':'medium','permission_mode_observed':'always-proceed',
    'actual_user_turns':1,'actual_native_tool_requests':0,'maximum_frozen_turns':6,'remaining_cases_not_run':5,
    'model_retries':0,'availability_class':'unqualified; init advertises list_dir, model says unavailable, no actual admission',
    'native_unsupported_tool_claim':False,'native_enforcement_claim':False,'original_failed_oracle_regraded':False,
    'source_modified':False,'installed_update':'not-performed','full_native_gate':'unchecked',
    'summary':bind(RUN/'native-tool-summary.json'),'frozen_brief':bind(RUN/'frozen-brief.json'),
    'attempt':observation['receipt'],'failure':bind(RUN/'native-tool-failure.json'),
    'cleanup':bind(RUN/'cleanup.json'),'process_audit':bind(RUN/'process-final-audit.json'),'verifier':bind(Path(__file__))}
(RUN/'verified-read-attempt.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':record['status'],'native_tool_requests':0,'unsupported_tool_claim':False}))
