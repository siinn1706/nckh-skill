"""Record one genuine native callback and forward unchanged advisory runner bytes."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--project', type=Path, required=True)
p.add_argument('--runner', type=Path, required=True)
a = p.parse_args()
data = sys.stdin.buffer.read(65537)
sha = lambda value: hashlib.sha256(value).hexdigest()
native = json.loads(data)
record = {'status': 'entered-from-native-host', 'started_at': datetime.now(timezone.utc).isoformat(),
          'pid': os.getpid(), 'parent_pid': os.getppid(), 'input_sha256': sha(data),
          'input_size': len(data), 'native_event': native.get('hook_event_name'),
          'native_tool': native.get('tool_name'), 'native_model': native.get('model'),
          'native_tool_id': native.get('tool_use_id'), 'native_turn_id': native.get('turn_id'),
          'native_session_sha256': sha(str(native.get('session_id')).encode()),
          'native_cwd': native.get('cwd'), 'runner_sha256': sha(a.runner.read_bytes())}
command = native.get('tool_input', {}).get('command')
record['native_command_sha256'] = sha(command.encode()) if isinstance(command, str) else None
target = a.project / 'evidence/native-callback.json'
target.write_text(json.dumps(record, indent=2) + '\n', encoding='utf8')
argv = [sys.executable, '-I', str(a.runner), '--host', 'codex', '--event', 'PreToolUse',
        '--project', str(a.project), '--context', 'evidence/context.json', '--mode', 'advisory',
        '--receipt-dir', 'evidence/policy-receipts']
result = subprocess.run(argv, input=data, capture_output=True, timeout=5, creationflags=subprocess.CREATE_NO_WINDOW)
record.update(status='completed', ended_at=datetime.now(timezone.utc).isoformat(),
              runner_exit_code=result.returncode, runner_output=json.loads(result.stdout),
              runner_stdout_sha256=sha(result.stdout), runner_stderr_sha256=sha(result.stderr))
target.write_text(json.dumps(record, indent=2) + '\n', encoding='utf8')
sys.stdout.buffer.write(result.stdout)
sys.stderr.buffer.write(result.stderr)
sys.exit(result.returncode)
