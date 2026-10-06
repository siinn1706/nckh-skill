"""Bind genuine selected Write failures to native IDs, absent effects and cleanup."""

import importlib.util
import json
from datetime import datetime
from pathlib import Path

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('write_fault_delivery', RUN / 'cursor-write-fault-runtime.py')
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.check_source()
prep = probe.read(RUN / 'preparation.json')
definition = probe.read(RUN / 'definitions/session.json')
hooks = definition['config']['hooks']
assert hooks['preToolUse'][0]['timeout'] == 20 and hooks['preToolUse'][0]['failClosed']
assert all(hooks[event][0]['matcher'] == '^Write$' for event in ('preToolUse', 'postToolUse', 'postToolUseFailure'))
assert all(hooks[event][0]['timeout'] == 5 for event in ('sessionStart', 'beforeSubmitPrompt', 'postToolUse', 'stop'))
assert hooks['postToolUseFailure'][0]['timeout'] == 10
metadata = probe.read(RUN / 'native-metadata.json')
model = probe.read(RUN / 'model-selection-before-prompt.json')['selected_model']
assert model['modelId'] == 'grok-4.7'
assert {p['id']: p['value'] for p in model['parameters']} == {'context': '500k', 'reasoning_effort': 'xhigh', 'fast': 'false'}
assert prep == probe.read(RUN / 'frozen-brief.json')
rows, tool_ids = [], []
expected_modes = ('malformed-input', 'malformed-output', 'timeout', 'crash', 'unsupported-codec')
for number, mode in enumerate(expected_modes, 1):
    case_path = RUN / ('case-' + str(number) + '.json')
    case = probe.read(case_path)
    assert case['case'] == prep['cases'][number - 1] and case['case']['mode'] == mode
    assert case['selected_observers_terminal'] and case['model_reply_marker_observed']
    assert case['selected_native_write_failures'] == 1 and case['actual_selected_write_post_receipts'] == 0
    assert case['fixture_unchanged'] and case['fixture_after_sha256'] == prep['before_sha256']
    assert case['prompt_retries'] == 0 and case['fault_origin'] == 'controller-injection-after-genuine-callback'
    assert len(case['observations']) == 1 and len(case['native_failures']) == 1
    callback = case['observations'][0]['record']
    assert callback['native_tool_name'] == 'Write' and callback['native_version'] == metadata['version']
    actual_path = Path(callback['native_path_fields']['file_path']).resolve()
    assert actual_path == probe.contained(probe.PROJECT, prep['relative']).resolve()
    assert callback['native_tool_use_id'] and callback['reported_event'] == 'preToolUse'
    assert callback['fault_selected'] and callback['fault_origin'] == 'controller-injection-after-genuine-callback'
    assert callback['workspace_contains_selected_project']
    failure = case['native_failures'][0]['record']
    assert failure['native_tool_use_id'] == callback['native_tool_use_id']
    assert failure['native_session_hash'] == callback['native_session_hash']
    assert failure['native_tool_name'] == 'Write' and failure['native_version'] == metadata['version']
    assert failure['failure_type'] == 'permission_denied' and failure['selected_path_matches']
    assert failure['workspace_contains_selected_project'] and not failure['policy_invoked']
    error = failure['scrubbed_selected_error']
    elapsed = None
    if callback.get('completed_at'):
        elapsed = (datetime.fromisoformat(callback['completed_at']) - datetime.fromisoformat(callback['started_at'])).total_seconds()
    if mode == 'malformed-input':
        assert error == 'hook-input-or-context-invalid'
        assert callback['runner_exit_code'] == 0 and callback['runner_output']['permission'] == 'deny'
        assert len(case['degraded_without_context_hash']) == 1
    elif mode == 'malformed-output':
        assert callback['status'] == 'intentional-test-malformed-output' and 'invalid JSON' in error
    elif mode == 'timeout':
        assert elapsed is not None and elapsed >= 24
        assert '20000ms' in error and callback['runner_exit_code'] == 0
    elif mode == 'crash':
        assert callback['status'] == 'intentional-test-crash-exit-17' and '17' in error
    elif mode == 'unsupported-codec':
        assert callback['runner_exit_code'] == 3 and '3' in error
    for collection in ('observations', 'policy_receipts', 'direct_receipts', 'native_failures', 'terminal'):
        for item in case[collection]:
            assert probe.digest_file(probe.WORK / item['path']) == item['sha256']
    tool_ids.append(callback['native_tool_use_id'])
    rows.append({'index': number, 'mode': mode, 'case': probe.bind(case_path),
        'native_tool': 'Write', 'native_tool_use_id': callback['native_tool_use_id'],
        'native_version': metadata['version'], 'native_error': error, 'native_permission_denied_count': 1,
        'observer_status': callback['status'], 'observer_elapsed_seconds': elapsed,
        'runner_output': callback.get('runner_output', 'not-invoked'),
        'degraded_receipts_without_context_hash': len(case['degraded_without_context_hash']),
        'successful_selected_Write_post_receipts': 0, 'fixture_unchanged': True,
        'final_marker_observed': True, 'terminal_truncated': case['terminal_truncated']})
assert len(set(tool_ids)) == 5
assert probe.contained(probe.PROJECT, prep['relative']).read_bytes() == (RUN / 'fixture-before.txt').read_bytes()
cleanup = probe.read(RUN / 'cleanup.json')
assert cleanup['status'] == 'pass' and len(cleanup['removed_members']) == 26 and not cleanup['config_callable']
assert all(p['current_sha256'] == p['sha256'] for p in cleanup['protected_global_config'])
audit = probe.read(RUN / 'final-process-audit-attempt-02.json')
assert audit['matching_count'] == audit['tracked_live_count'] == 0
assert audit['identity_source'] == 'union of start and before-stop captures'
assert all(p['expected_identity'] for p in audit['retained_agy_for_continuation'])
assert probe.read(RUN / 'terminal-native-exit-poll.json')['exit_code'] == 0
summary = {'status': 'verified-five-native-selected-Write-preflight-fault-observations',
    'source_revision': 37, 'source_lock_hash': probe.EXPECTED, 'native_version': metadata['version'],
    'surface': 'cursor-cli', 'model': prep['model'], 'model_selection': probe.bind(RUN / 'model-selection-before-prompt.json'),
    'model_turns': 5, 'prompt_submissions': 5, 'model_prompt_retries': 0,
    'distinct_native_Write_tool_ids': 5, 'native_permission_denied_count': 5, 'rows': rows,
    'selected_matcher': '^Write$', 'scope_limit': prep['scope_limit'], 'unsupported_scope': prep['unsupported_scope'],
    'fault_origin': 'controller-injection-after-genuine-callback', 'preflight_timeout_seconds': 20,
    'inner_runner_timeout_seconds': 5, 'timeout_injection_seconds': 24, 'other_handler_timeout_seconds': 5,
    'diagnostic_timeout_seconds': 10, 'handler_kind': 'explicit fault observer after genuine native Write callback',
    'fixture_unchanged_in_every_case': True, 'successful_selected_Write_post_receipts': 0,
    'native_ID_binding': 'Actual callback and failure observer share the same selected Write ID/session/path/version',
    'degraded_receipt_limit': 'Parse failures omit context_hash; bind to genuine callback/control/runner and native failure ID',
    'raw_terminal_truncated': any(r['terminal_truncated'] for r in rows), 'raw_native_tool_return_content': 'not-retained',
    'backend_attestation': 'not-observed', 'global_direct_write': False, 'protected_global_configs_unchanged': True,
    'cli_owned_state_hash_changed': cleanup['global_cli_hash_before'] != cleanup['global_cli_hash_after'],
    'CLI_owned_state_fields': 'not-inferred-from-hashes', 'native_terminal_exit_code': 0,
    'cleanup_removed_members': 26, 'historical_members_preserved': cleanup['historical_members_unchanged'],
    'cleanup': probe.bind(RUN / 'cleanup.json'), 'process_audit': probe.bind(RUN / 'final-process-audit-attempt-02.json'),
    'process_identity_count': len(audit['tracked']), 'matching_process_count': 0,
    'terminal_exit': probe.bind(RUN / 'terminal-native-exit-poll.json'), 'definition': prep['definition'],
    'frozen_brief': probe.bind(RUN / 'frozen-brief.json'), 'collector': probe.bind(RUN / 'record-write-fault.py'),
    'startup_display_binding_adaptation': probe.bind(RUN / 'startup-display-binding-adaptation.json'),
    'verifier': probe.bind(Path(__file__)), 'plan_tasks': '44/45', 'full_native_gate': 'unchecked',
    'owner_acceptance': 'exact-r29-VI-EN-only', 'installed_update': 'not-performed',
    'publication': 'not-performed', 'scientific_stable_release': 'pending'}
target = probe.WORK / 'plans/reports/delivery-261005-2125-r37-cursor-write-faults.json'
assert not target.exists() and not (RUN / 'native-write-fault-summary.json').exists()
probe.atomic_json(RUN / 'native-write-fault-summary.json', summary)
probe.atomic_json(target, summary)
print(json.dumps({'status': summary['status'], 'denials': 5, 'fixture_unchanged': True,
                  'historical_preserved': summary['historical_members_preserved'], 'full_native_gate': 'unchecked'}))
