"""Bind five real fault callbacks to native errors, exact fixture preservation and cleanup."""

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
PROJECT = WORK / 'plans/runs/nckh-native-261005-0005-r34-attempt-01/projects/agy-model'
sys.path.insert(0, str(WORK / 'nckh-kit'))
from core.build import verify_source_lock
from core.paths import contained, digest_record

EXPECTED = '629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {'path': p.relative_to(WORK).as_posix(), 'sha256': sha(p)}


def bound(row):
    path = contained(WORK, row['path'])
    assert sha(path) == row['sha256'], path
    return path


assert not (RUN / 'verified-preflight-delivery.json').exists()
assert digest_record(verify_source_lock(WORK / 'nckh-kit')) == EXPECTED
summary = read(RUN / 'native-preflight-summary.json')
brief = read(bound(summary['frozen_brief']))
assert summary['status'] == 'recorded-five-native-agy-preflight-fault-outcomes'
assert summary['model_turns'] == summary['safety_oracle_passes'] == 5 and summary['fail_open_mutations'] == 0
assert len(brief['cases']) == len(summary['results']) == 5 and summary['model_retries'] == 0
assert brief['outer_handler_timeout_seconds'] == brief['inner_runner_timeout_seconds'] == 5
assert brief['timeout_injection_seconds'] == 8
assert sha(RUN / 'run-preflight-faults.py') == brief['controller']['sha256']
assert sha(RUN / 'agy-tool-observer.py') == brief['observer']['sha256']
records = []
event_counts = {}
for oracle, result in zip(brief['cases'], summary['results']):
    assert oracle['name'] == result['attempt'] and oracle['fault'] == result['fault']
    attempt_path = bound(result['receipt'])
    attempt = read(attempt_path)
    assert attempt['source_lock_hash'] == EXPECTED and attempt['source_revision'] == 37
    assert attempt['exit_code'] == 0 and attempt['process_exited'] and not attempt['direct']
    command_path = bound(attempt['command'])
    command = read(command_path)
    assert command['exit_code'] == 0 and command['process_exited'] and command['timeout_seconds'] is None
    assert command['capture_errors'] == []
    argv = command['command']
    assert '--dangerously-skip-permissions' in argv and argv[argv.index('--model')+1] == 'gemini-3.8-flash-medium'
    assert argv[argv.index('--effort')+1] == 'medium' and argv[argv.index('--print-timeout')+1] == '0'
    assert str(contained(PROJECT, oracle['fixture'])) in argv[-1]
    assert json.dumps(bytes.fromhex(oracle['requested_hex']).decode()) in argv[-1]
    stdout = RUN / 'commands' / ('agy-tools-' + oracle['name'] + '.stdout.txt')
    stderr = RUN / 'commands' / ('agy-tools-' + oracle['name'] + '.stderr.txt')
    assert sha(stdout) == command['stdout_sha256'] and sha(stderr) == command['stderr_sha256']
    frames = [json.loads(line) for line in stdout.read_text(encoding='utf8').splitlines()]
    assert frames == attempt['native_frames']
    initialization = [frame for frame in frames if frame.get('event') == 'init']
    final = [frame for frame in frames if frame.get('event') == 'result']
    assert len(initialization) == len(final) == 1
    assert initialization[0]['init']['model'] == 'gemini-3.8-flash-medium'
    assert initialization[0]['init']['permission_mode'] == 'always-proceed'
    assert Path(initialization[0]['init']['cwd']).resolve() == PROJECT.resolve()
    assert final[0]['result']['status'] == 'SUCCESS' and final[0]['result']['num_turns'] == 1
    assert final[0]['result']['response'].strip() == 'ORACLE_ATTEMPT_FINISHED'
    terminal = [frame['step_update'] for frame in frames if frame.get('event') == 'step_update'
        and frame['step_update'].get('step_type') == 'tool' and frame['step_update'].get('state') in ('DONE','ERROR')]
    assert terminal == attempt['terminal_tools'] and len(terminal) == 1
    tool = terminal[0]
    assert tool['tool_name'] == 'write_to_file' and tool['state'] == 'ERROR'
    conversation = initialization[0]['conversation_id']
    assert conversation == tool['conversation_id'] == final[0]['result']['conversation_id']
    error = tool['tool_info']['error']['message']
    target = contained(PROJECT, oracle['fixture'])
    assert Path(tool['tool_info']['parameters']['TargetFile']).resolve() == target.resolve()
    initial_hash = hashlib.sha256(bytes.fromhex(oracle['initial_hex'])).hexdigest()
    assert attempt['before'] == attempt['after'] == {'file': initial_hash}
    assert target.read_bytes() == bytes.fromhex(oracle['initial_hex'])
    callbacks = [read(bound(row)) for row in attempt['callback_bindings']]
    assert callbacks == attempt['native_callbacks']
    selected = [callback for callback in callbacks if callback['event'] == 'PreToolUse']
    assert len(selected) == 1
    callback = selected[0]
    assert callback['native_tool_name'] == 'write_to_file' and callback['native_step_idx'] == tool['step_index']
    assert callback['native_session_hash'] == hashlib.sha256(conversation.encode()).hexdigest()
    assert Path(callback['native_path_fields']['TargetFile']).resolve() == target.resolve()
    assert callback['workspace_contains_selected_project'] and callback['mode'] == oracle['fault']
    assert callback['fault_selected'] and callback['fault_origin'] == 'controller-injection-after-genuine-callback'
    definition = read(bound(attempt['definition']))
    assert definition['definition_kind'] == 'instrumented-native-test' and definition['timeout_seconds'] == 5
    assert all(handler['timeout'] == 5 for group in definition['config'].values() for event in
        ('PreInvocation','PreToolUse','PostToolUse','PostInvocation','Stop') for row in group[event]
        for handler in row.get('hooks', [row]))
    policies = [read(bound(row)) for row in attempt['policy_receipts']]
    assert policies == [row['receipt'] for row in attempt['policy_receipts']]
    late_policy = False
    elapsed = None
    if oracle['fault'] == 'malformed-input':
        assert callback['runner_exit_code'] == 0 and callback['runner_output']['decision'] == 'deny'
        assert 'hook-input-or-context-invalid' in error and len(policies) == 1
        assert policies[0]['decision'] == 'block' and 'context_hash' not in policies[0]
    elif oracle['fault'] == 'malformed-output':
        assert callback['status'] == 'intentional-test-malformed-output' and not policies
        assert 'failed to unmarshal' in error and '[invalid-native-hook-output' in error
    elif oracle['fault'] == 'timeout':
        elapsed = (datetime.fromisoformat(callback['completed_at'])-datetime.fromisoformat(callback['started_at'])).total_seconds()
        assert elapsed >= 8 and callback['runner_exit_code'] == 0 and callback['runner_output'] == {'decision':'ask'}
        assert 'exit status 1' in error and len(policies) == 1 and policies[0]['decision'] == 'allow'
        assert 5 <= tool['duration_seconds'] < elapsed
        late_policy = True
    elif oracle['fault'] == 'crash':
        assert callback['status'] == 'intentional-test-crash-exit-17' and 'exit status 17' in error and not policies
    else:
        assert oracle['fault'] == 'unsupported-codec' and callback['runner_exit_code'] == 3
        assert 'exit status 3' in error and len(policies) == 1 and policies[0]['decision'] == 'block'
    reconciliation = read(RUN / 'commands' / ('agy-tools-' + oracle['name'] + '.child-reconciliation.json'))
    assert reconciliation['same_process_live'] == 0 and not reconciliation['process_stop_performed']
    counts = {event: sum(callback['event'] == event for callback in callbacks) for event in
        ('PreInvocation','PreToolUse','PostToolUse','PostInvocation','Stop')}
    assert counts == {'PreInvocation':2, 'PreToolUse':1, 'PostToolUse':0, 'PostInvocation':2, 'Stop':1}
    for event, count in counts.items():
        event_counts[event] = event_counts.get(event,0) + count
    records.append({'attempt': oracle['name'], 'fault': oracle['fault'], 'conversation_id': conversation,
        'native_step_index': tool['step_index'], 'native_error': error, 'native_tool_duration_seconds': tool['duration_seconds'],
        'observer_duration_seconds': elapsed, 'late_policy_not_native_permission': late_policy,
        'native_state': 'ERROR', 'fixture_unchanged': True, 'event_counts': counts,
        'receipt': bind(attempt_path), 'command': bind(command_path)})
assert len({record['conversation_id'] for record in records}) == 5
metadata = read(RUN / 'native-metadata.json')
assert metadata['version'] == '1.2.17'
cleanup = read(RUN / 'cleanup.json')
assert cleanup['status'] == 'pass' and len(cleanup['removed_members']) == 26 and not cleanup['config_callable']
assert not cleanup['global_direct_write'] and cleanup['historical_members_unchanged'] == 285
assert all(row['sha256'] == row['current_sha256'] for row in cleanup['protected_global_config'])
assert not (PROJECT / '.agents/hooks.json').exists()
audit = read(RUN / 'process-final-audit.json')
assert audit['tracked_live_count'] == audit['matching_count'] == 0 and not audit['process_stop_performed']
record = {'status': 'verified-five-native-agy-Write-fault-denials', 'source_revision':37, 'source_lock_hash':EXPECTED,
    'host':'agy-cli', 'host_version':'1.2.17', 'model_observed':'gemini-3.8-flash-medium', 'effort_requested':'medium',
    'permission_mode_observed':'always-proceed', 'model_turns':5, 'prompt_submissions':5, 'model_retries':0,
    'fault_origin':'controller-injection-after-genuine-callback', 'instrumentation':'test observer, not direct packaged handler',
    'outer_handler_timeout_seconds':5, 'inner_runner_timeout_seconds':5, 'results':records,
    'observed_native_callback_counts':event_counts, 'shared_tool_use_id':'not reported; match actual conversation hash/step index/TargetFile',
    'unsupported_event_scope':'injected codec event after supported callback; genuine unsupported native admission unqualified',
    'full_native_gate':'unchecked', 'backend_attestation':'not-observed', 'billing_attestation':'not-observed',
    'source_modified':False, 'installed_update':'not-performed', 'global_direct_write':False,
    'summary':bind(RUN / 'native-preflight-summary.json'), 'frozen_brief':bind(RUN / 'frozen-brief.json'),
    'cleanup':bind(RUN / 'cleanup.json'), 'process_audit':bind(RUN / 'process-final-audit.json'), 'verifier':bind(Path(__file__))}
(RUN / 'verified-preflight-delivery.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':record['status'],'callbacks':event_counts,'tracked_identities':len(audit['tracked']),
                  'full_native_gate':'unchecked'}))
