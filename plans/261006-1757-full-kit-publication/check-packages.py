import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
outside = Path('C:/Users/USER/.codex/visualizations/2026/10/06/01a110db-4f44-7f91-98be-6d0c9e5e7f18')
sys.path.insert(0, str(root / 'github-publication/nckh-kit'))
from scripts import __name__ as unused

def check(host):
    bundle = root / 'publication-r41' / host
    receipt = Path(__file__).parent / (host + '-resource-read.json')
    if host != 'codex':
        process = subprocess.run([sys.executable, str(root / 'github-publication/nckh-kit/scripts/resource-smoke.py'),
            '--bundle', str(bundle), '--cwd', str(outside), '--unset-pythonpath', '--output', str(receipt)],
            capture_output=True, text=True, timeout=240)
        if process.returncode:
            raise RuntimeError(process.stderr)
    record = json.loads(receipt.read_text())
    assert record['status'] == 'pass' and len(record['observations']) == 35
    event = 'preToolUse' if host == 'cursor' else 'PreToolUse'
    process = subprocess.run([sys.executable, '-I', str(bundle / 'hooks/runner.py'), '--host', host,
        '--event', event, '--mode', 'advisory', '--project', str(outside), '--context', 'missing-context.json'],
        input=b'invalid', capture_output=True, cwd=outside, timeout=30)
    assert process.returncode == 0, process.stderr
    wire = json.loads(process.stdout)
    assert 'deny' not in json.dumps(wire) and wire.get('continue') is not False
    return {'host': host, 'resource_reads': len(record['observations']), 'advisory_malformed_input': 'pass'}

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for result in pool.map(check, ('claude', 'codex', 'cursor', 'agy')):
        print(json.dumps(result), flush=True)
