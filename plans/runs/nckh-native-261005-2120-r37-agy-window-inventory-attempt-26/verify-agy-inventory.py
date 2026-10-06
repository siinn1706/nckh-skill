"""Keep native IDE evidence pending when the helper returns no owned window."""

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
read = lambda p: json.loads(p.read_text(encoding='utf8'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind = lambda p: {'path': p.relative_to(WORK).as_posix(), 'sha256': sha(p)}
raw = read(RUN / 'agy-inventory.json')
assert not raw.get('isError')
blocks = [p['text'] for p in raw['content'] if p['type'] == 'text' and p.get('text')]
assert len(blocks) == 1
inventory = json.loads(blocks[0])
apps = [a for a in inventory['apps'] if a['id'] in {'Google.Antigravity', 'electron.app.Antigravity'}]
assert len(apps) == 2 and all(a['isRunning'] and a['windows'] == [] for a in apps)
assert inventory['target_owned_windows'] == []
windows = inventory['windows']
assert len(windows) == 1 and windows[0]['title'] == 'Antigravity'
assert windows[0]['app'] == 'OpenAI.Codex_2p2nqsd0c76g0!App'
assert not inventory['app_input_sent'] and not inventory['app_capture_performed']
assert inventory['launch_attempts'] == 0
summary = {'status': 'verified-fresh-inventory-AGY-owned-window-still-unidentified',
    'timestamp_utc': inventory['timestamp_utc'], 'agy_owned_window_count': 0,
    'agy_apps_reported_running': len(apps), 'antigravity_title_owner_returned': windows[0]['app'],
    'app_input_sent': False, 'app_capture_performed': False, 'launch_attempts': 0,
    'model_turns': 0, 'prompt_submissions': 0, 'process_stop_performed': False,
    'access_and_unlock_grants': 'retained-no-new-approval-required',
    'scope': 'read-only sky.list_apps plus sky.list_windows; no selection/capture/input on a Codex-attributed window',
    'boundaries': 'computer-use skill requires a returned unique target window and prohibits Codex UI automation',
    'inventory': bind(RUN / 'agy-inventory.json'),
    'previous_supported_launch_observation': bind(WORK / 'plans/runs/nckh-native-261005-1956-r37-host-route-recovery-attempt-22/host-recovery-summary.json'),
    'retained_process_identity': bind(WORK / 'plans/runs/nckh-native-261005-2055-r37-cursor-selected-write-attempt-25/final-process-audit-attempt-02.json'),
    'verifier': bind(Path(__file__)), 'agy_ide_native_gate': 'pending-unverified', 'full_native_gate': 'unchecked',
    'plan_tasks': '44/45', 'source_changed': False, 'requested_user_action': 'Bring the separate AGY IDE window forward for fresh supported selection'}
assert not (RUN / 'host-window-summary.json').exists()
with (RUN / 'host-window-summary.json').open('x', encoding='utf8') as stream:
    stream.write(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
target = WORK / 'plans/reports/delivery-261005-2120-r37-agy-window-inventory.json'
with target.open('x', encoding='utf8') as stream:
    stream.write(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': summary['status'], 'owned_windows': 0, 'input_sent': False, 'agy_ide_gate': 'pending-unverified'}))
