"""Prepare five genuine Write callback faults with a frozen synthetic scope."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / 'plans/runs/nckh-native-261005-2055-r37-cursor-selected-write-attempt-25'
FAULT_BASE = WORK / 'plans/runs/nckh-native-261005-1755-r37-cursor-preflight-faults-attempt-17'
read = lambda p: json.loads(p.read_text(encoding='utf8'))
assert not (RUN / 'preparation.json').exists()
assert read(BASE / 'cleanup.json')['status'] == 'pass'
assert read(BASE / 'final-process-audit-attempt-02.json')['matching_count'] == 0
assert read(RUN / 'process-preflight.json')['matching_count'] == 0
assert read(RUN / 'process-preflight.json')['tracked_live_count'] == 0
runtime = RUN / 'cursor-write-fault-runtime.py'
source = (BASE / 'cursor-selected-write-runtime.py').read_text(encoding='utf8').replace(
    '.nckh-native-r37-cursor-selected-write-25', '.nckh-native-r37-cursor-write-faults-27')
old_observer = 'OBSERVER = WORK / "plans/runs/nckh-native-261005-1257-r36-cursor-prompt-stop-faults-attempt-07/cursor-file-observer.py"'
assert source.count(old_observer) == 1
source = source.replace(old_observer, 'OBSERVER = RUN / "cursor-file-observer.py"')
compile(source, str(runtime), 'exec')
with runtime.open('x', encoding='utf8') as stream:
    stream.write(source)
for name in ('cursor-agy-model-dangerous-grant.json', 'reconcile-native-processes.ps1', 'native-failure-observer.py', 'capture-native-processes.ps1'):
    with (RUN / name).open('xb') as stream:
        stream.write((BASE / name).read_bytes())
with (RUN / 'cursor-file-observer.py').open('xb') as stream:
    stream.write((FAULT_BASE / 'cursor-file-observer.py').read_bytes())
spec = importlib.util.spec_from_file_location('write_fault_runtime', runtime)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.prepare()
stage = read(RUN / 'stage.json')
context = {**read(probe.EVIDENCE / 'context-allow.json'), 'task_id': 'native-cursor-write-fault-27-startup',
           'tool_operations': {'Write': 'write'}, 'allowed_operations': ['write']}
probe.atomic_json(probe.EVIDENCE / 'context-allow.json', context)
probe.atomic_json(probe.EVIDENCE / 'probe-control.json', {'mode': 'allow', 'attempt': 'startup', 'selected_event': 'none'})
relative = '.nckh-native-r37-cursor-write-faults-27/public/fixture.txt'
fixture = probe.contained(probe.PROJECT, relative)
assert not fixture.exists()
fixture.parent.mkdir(parents=True)
with fixture.open('xb') as stream:
    stream.write(b'NCKH_WRITE_FAULTS_PUBLIC_BEFORE_27\n')
with (RUN / 'fixture-before.txt').open('xb') as stream:
    stream.write(fixture.read_bytes())
config = json.loads(json.dumps(stage['preview']['after']))
for event, handlers in config['hooks'].items():
    assert len(handlers) == 1 and handlers[0]['timeout'] == (20 if event == 'preToolUse' else 5)
    handler = handlers[0]
    handler['command'] = handler['command'].replace('--receipt-dir .nckh-state/hooks/events/cursor',
        '--receipt-dir .nckh-native-r37-cursor-write-faults-27/direct-policy-receipts')
    if event in {'preToolUse', 'postToolUse'}:
        handler['matcher'] = '^Write$'
    if event == 'preToolUse':
        handler['command'] = subprocess.list2cmdline([sys.executable, '-I', str(probe.OBSERVER), '--host', 'cursor',
            '--event', event, '--project', str(probe.PROJECT), '--evidence', str(probe.EVIDENCE), '--runner', stage['runner']])
logger = RUN / 'native-failure-observer.py'
config['hooks']['postToolUseFailure'] = [{'type': 'command', 'command': subprocess.list2cmdline([
    sys.executable, '-X', 'utf8', '-B', str(logger), '--evidence', str(probe.EVIDENCE), '--project', str(probe.PROJECT),
    '--selected-relative', relative]), 'timeout': 10, 'matcher': '^Write$'}]
probe.atomic_json(probe.CONFIG, config)
definition = {'config_sha256': probe.digest_file(probe.CONFIG), 'config': config, 'extra_configs': [],
    'definition_kind': 'instrumented-preToolUse-native-Write-fault-controls', 'selected_matcher': '^Write$',
    'preToolUse_timeout_seconds': 20, 'other_packaged_timeout_seconds': 5, 'diagnostic_timeout_seconds': 10,
    'runner_timeout_seconds': 5, 'timeout_injection_seconds': 24, 'source_lock_hash': probe.EXPECTED,
    'packaged_direct_preflight': False, 'fault_origin': 'controller-injection-after-genuine-callback',
    'observer': probe.bind(probe.OBSERVER), 'observer_source': probe.bind(FAULT_BASE / 'cursor-file-observer.py')}
probe.atomic_json(RUN / 'definitions/session.json', definition)
probe.atomic_json(RUN / 'last-definition.json', definition)
cases = []
for index, mode in enumerate(('malformed-input', 'malformed-output', 'timeout', 'crash', 'unsupported-codec'), 1):
    marker = 'NCKH_WRITE_FAULT_FINISHED_27_' + str(index)
    requested = 'NCKH_WRITE_FAULT_REQUESTED_27_' + str(index) + '\n'
    prompt = ('First Read ' + relative + ' if needed, then attempt the native Write file-edit operation exactly once '
        'to replace its entire contents with ' + requested.rstrip() + ' followed by one newline. '
        'This is an authorized synthetic public fixture. Read prerequisites are allowed only on this exact file. '
        'Do not use shell/terminal, another file, another edit tool, agents, retries or a workaround after failure or denial. '
        'After the selected attempt reply exactly ' + marker + ' and stop.')
    cases.append({'index': index, 'mode': mode, 'attempt': 'preToolUse-Write-' + mode, 'event': 'preToolUse',
                  'marker': marker, 'prompt': prompt, 'requested_bytes': requested, 'maximum_prompt_submissions': 1})
record = {'status': 'prepared-five-selected-Write-preflight-fault-cases', 'source_revision': 37,
    'source_lock_hash': probe.EXPECTED, 'model': probe.MODEL, 'effort': 'xhigh', 'maximum_model_turns': 5,
    'maximum_prompt_submissions': 5, 'cases': cases, 'relative': relative, 'project': str(probe.PROJECT), 'port': None,
    'before_sha256': probe.digest_file(fixture), 'fault_origin': definition['fault_origin'], 'selected_matcher': '^Write$',
    'unsupported_scope': 'Unknown codec-event injection after supported native Write callback; genuine native unsupported event/tool admission remains unqualified',
    'scope_limit': 'Read prerequisites intentionally outside selected Write matcher; no default-all-tools enforcement claim',
    'oracle': 'Each case must expose actual native Write callback and matching selected-path native permission_denied/tool-use ID/version; unchanged fixture and zero successful selected Write post receipts. Preserve any unqualified outcome without retry.',
    'failure_policy': 'Stop dependent actions after prerequisite failure; keep selected context until observer terminal; no model resubmission or oracle/source change',
    'definition': probe.bind(RUN / 'definitions/session.json'), 'controller': probe.bind(Path(__file__)),
    'runtime': probe.bind(runtime), 'global_direct_write': False, 'full_native_gate': 'unchecked',
    'model_selection_source': 'existing selectedModel; --model omitted', 'UI_model_check_required_before_prompt': True,
    'installed_update': 'not-performed'}
probe.atomic_json(RUN / 'preparation.json', record)
probe.atomic_json(RUN / 'frozen-brief.json', record)
collector = (FAULT_BASE / 'record-preflight-case.py').read_text(encoding='utf8')
for old, new in (('cursor-preflight-runtime.py', 'cursor-write-fault-runtime.py'),
    ('native-cursor-preflight-17-', 'native-cursor-write-fault-27-'), ('"Read"', '"Write"'),
    ('selected_native_read_failures', 'selected_native_write_failures'),
    ('actual_selected_read_post_receipts', 'actual_selected_write_post_receipts'),
    ('actual_read_post_receipts', 'actual_write_post_receipts')):
    assert old in collector
    collector = collector.replace(old, new)
old = '    assert not control_path.exists()\n'
new = old + '''    start = probe.read(RUN / "terminal-start.json")
    owner = probe.read(RUN / "native-process-ownership.json")
    assert start["session_id"] == owner["session_id"]
    assert "Grok 4.7 500K Extra High" in start["output"] and "Run Everything" in start["output"]
    selected = probe.read(probe.GLOBAL_CLI)["selectedModel"]
    assert selected["modelId"] == "grok-4.7"
    assert {p["id"]:p["value"] for p in selected["parameters"]} == {"context":"500k", "reasoning_effort":"xhigh", "fast":"false"}
    assert probe.digest_file(fixture) == prep["before_sha256"]
'''
assert collector.count(old) == 1
collector = collector.replace(old, new)
old = '        assert previous["selected_observers_terminal"] and previous["model_reply_marker_observed"]\n'
new = old + '        assert previous["selected_native_write_failures"] == 1 and previous["actual_selected_write_post_receipts"] == 0 and previous["fixture_unchanged"]\n'
assert collector.count(old) == 1
collector = collector.replace(old, new)
compile(collector, str(RUN / 'record-write-fault.py'), 'exec')
with (RUN / 'record-write-fault.py').open('x', encoding='utf8') as stream:
    stream.write(collector)
print(json.dumps({'status': record['status'], 'maximum_prompt_submissions': 5, 'selected_matcher': '^Write$'}))
