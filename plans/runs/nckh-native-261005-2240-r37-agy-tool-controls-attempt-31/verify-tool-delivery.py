"""Verify the two replace controls and retain actual unsupported-tool counterevidence."""

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


assert not (RUN/'verified-tool-delivery.json').exists()
assert digest_record(verify_source_lock(WORK/'nckh-kit'))==EXPECTED
summary=read(RUN/'native-tool-summary.json')
brief=read(bound(summary['frozen_brief']))
assert len(brief['cases'])==10 and len(summary['results'])==3 and summary['status']=='running'
assert read(RUN/'native-tool-failure.json')['completed_cases']==3
assert sha(RUN/'run-tool-controls.py')==brief['controller']['sha256']
cases=[]
for index,observation in enumerate(summary['results']):
    oracle=brief['cases'][index]
    attempt=read(bound(observation['receipt']))
    assert oracle['name']==observation['attempt'] and attempt['direct']
    assert attempt['source_lock_hash']==EXPECTED and attempt['source_revision']==37
    assert attempt['exit_code']==0 and attempt['process_exited']
    command=read(bound(attempt['command']))
    assert command['exit_code']==0 and command['process_exited'] and command['timeout_seconds'] is None
    argv=command['command']
    assert '--dangerously-skip-permissions' in argv and argv[argv.index('--model')+1]=='gemini-3.8-flash-medium'
    assert argv[argv.index('--effort')+1]=='medium'
    stdout=RUN/'commands'/('agy-tools-'+oracle['name']+'.stdout.txt')
    assert sha(stdout)==command['stdout_sha256']
    frames=[json.loads(line) for line in stdout.read_text(encoding='utf8').splitlines()]
    assert frames==attempt['native_frames']
    init=[f for f in frames if f.get('event')=='init']
    final=[f for f in frames if f.get('event')=='result']
    assert len(init)==len(final)==1
    assert init[0]['init']['model']=='gemini-3.8-flash-medium' and init[0]['init']['permission_mode']=='always-proceed'
    assert Path(init[0]['init']['cwd']).resolve()==PROJECT.resolve()
    assert final[0]['result']['status']=='SUCCESS' and final[0]['result']['num_turns']==1
    assert final[0]['result']['response'].strip()=='ORACLE_ATTEMPT_FINISHED'
    terminal=[f['step_update'] for f in frames if f.get('event')=='step_update'
        and f['step_update'].get('step_type')=='tool' and f['step_update'].get('state') in ('DONE','ERROR')]
    assert terminal==attempt['terminal_tools'] and len(terminal)==1
    tool=terminal[0]
    assert tool['tool_name']==oracle['tool'] and tool['conversation_id']==init[0]['conversation_id']==final[0]['result']['conversation_id']
    assert Path(tool['tool_info']['parameters']['TargetFile']).resolve()==contained(PROJECT,oracle['fixture']).resolve()
    policies=[read(bound(p)) for p in attempt['policy_receipts']]
    assert policies==[p['receipt'] for p in attempt['policy_receipts']]
    assert all(p['session_key']==digest_record(tool['conversation_id']) for p in policies)
    preflight=[p for p in policies if p['phase']=='preflight']
    initial=hashlib.sha256(bytes.fromhex(oracle['initial_hex'])).hexdigest()
    assert attempt['before']=={'file':initial}
    data=contained(PROJECT,oracle['fixture']).read_bytes()
    expected=bytes.fromhex(oracle['expected_hex'])
    definition=read(bound(attempt['definition']))
    assert definition['definition_kind']=='direct-packaged-runner' and definition['timeout_seconds']==5
    error=tool['tool_info'].get('error',{}).get('message')
    if index<2:
        assert observation['status']=='verified-direct-tool-control' and data==expected
        assert tool['state']==oracle['expected_state'] and len(preflight)==1
        assert preflight[0]['decision']==('block' if oracle['private'] else 'allow')
        if oracle['private']:
            assert 'private-holdout-credential-path' in preflight[0]['reason_codes'] and 'private-holdout-credential-path' in error
        outcome='verified-public-replace-exact-bytes' if index==0 else 'verified-private-replace-prevention'
    else:
        assert oracle['tool']=='multi_replace_file_content' and oracle['tool'] in init[0]['init']['tools']
        assert tool['state']=='ERROR' and 'unknown tool: "multi_replace_file_content"' in error
        assert preflight==[] and not any(p['phase']=='pre-delivery' for p in policies)
        assert data==bytes.fromhex(oracle['initial_hex']) and data!=expected
        assert observation['status']=='failed-frozen-tool-oracle-retained'
        assert not observation['native_expected'] and not observation['policy_expected'] and not observation['fixture_expected']
        outcome='genuine-native-unknown-tool-observation; original public allow oracle failed'
    assert attempt['after']=={'file':hashlib.sha256(data).hexdigest()}
    cases.append({'attempt':oracle['name'],'native_tool':tool['tool_name'],'native_state':tool['state'],
        'conversation_id':tool['conversation_id'],'step_index':tool['step_index'],'native_error':error,
        'preflight_receipts':len(preflight),'outcome':outcome,'receipt':observation['receipt']})
assert len({case['conversation_id'] for case in cases})==3
cleanup=read(RUN/'cleanup.json')
audit=read(RUN/'process-final-audit.json')
assert cleanup['status']=='pass' and len(cleanup['removed_members'])==26 and not cleanup['config_callable']
assert cleanup['historical_members_unchanged']==359 and not cleanup['global_direct_write']
assert all(row['sha256']==row['current_sha256'] for row in cleanup['protected_global_config'])
assert not (PROJECT/'.agents/hooks.json').exists()
assert audit['matching_count']==audit['tracked_live_count']==0 and not audit['process_stop_performed']
assert read(RUN/'native-metadata.json')['version']=='1.2.17'
record={'status':'verified-two-replace-controls-and-native-unknown-multi-replace-counterevidence',
    'source_revision':37,'source_lock_hash':EXPECTED,'host':'agy-cli','host_version':'1.2.17',
    'model_observed':'gemini-3.8-flash-medium','effort_requested':'medium','permission_mode_observed':'always-proceed',
    'maximum_frozen_turns':10,'actual_user_turns':3,'remaining_frozen_cases_not_run':7,'model_retries':0,
    'cases':cases,'native_unsupported_tool_observation':'multi_replace_file_content advertised in init, actual unknown tool ERROR, no preflight receipts',
    'original_failed_oracle_regraded':False,'full_native_gate':'unchecked','source_modified':False,
    'installed_update':'not-performed','global_direct_write':False,'backend_attestation':'not-observed',
    'summary':bind(RUN/'native-tool-summary.json'),'frozen_brief':bind(RUN/'frozen-brief.json'),
    'failure':bind(RUN/'native-tool-failure.json'),'cleanup':bind(RUN/'cleanup.json'),
    'process_audit':bind(RUN/'process-final-audit.json'),'verifier':bind(Path(__file__))}
(RUN/'verified-tool-delivery.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':record['status'],'actual_turns':3,'original_failed_oracle_regraded':False,'full_native_gate':'unchecked'}))
