"""Capture an actual local SVG render probe and project-scoped engine bindings."""

import argparse
import hashlib
import json
import sys
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', type=Path, required=True)
    parser.add_argument('--probe', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[3]
    engine, probe, output = args.engine.resolve(), args.probe.resolve(), args.output.resolve()
    if not probe.is_relative_to(project) or not output.is_relative_to(project) or output.exists():
        parser.error('probe and fresh output must be inside this project')
    output.mkdir(parents=True)
    sys.path.insert(0, str(project / 'nckh-kit'))
    from core.processes import run_owned_command

    def ref(path):
        return {'path': path.relative_to(project).as_posix(), 'sha256': digest(path)}

    def write(path, value):
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    version_command = [str(engine), '--version']
    render = output / 'probe.png'
    render_command = [str(engine), '-o', str(render), str(probe)]
    details = []
    version = None
    for name, command in [('version', version_command), ('render', render_command)]:
        stdout, stderr = output / (name + '.stdout.txt'), output / (name + '.stderr.txt')
        result = run_owned_command(command, project, b'', stdout, stderr, timeout=30)
        details.append({'operation': name, 'command': command, **result})
        write(output / 'process-details.json', details)
        if result['exit_status'] != 0:
            raise RuntimeError(name + ' failed; preserved output and process receipt')
        if name == 'version':
            version = stdout.read_text(encoding='utf-8').strip()
        receipt = {'command': command, 'exit_status': result['exit_status'],
                   'executable_sha256': digest(engine), 'version': version,
                   'stdout': ref(stdout), 'stderr': ref(stderr), 'status': result['status'],
                   'cleanup': result['process_cleanup']}
        if name == 'render':
            receipt.update(input_sha256=digest(probe), render_sha256=digest(render))
        write(output / (name + '.json'), receipt)
    observations = {'version_receipt': ref(output / 'version.json'),
                    'render_receipt': ref(output / 'render.json'),
                    'input_svg': ref(probe), 'render_png': ref(render)}
    for host in ('cursor', 'agy', 'codex'):
        binding = {'schema_version': 1, 'scope': {'project_root': str(project),
                   'task_id': 'real-source-worldbank-visual-01', 'host': host}, 'format': 'svg',
                   'engine': {'executable': str(engine), 'sha256': digest(engine), 'version': version},
                   'capabilities': ['svg-render'], 'observations': observations}
        write(output / (host + '-binding.json'), binding)
    print(json.dumps({'status': 'actual-render-captured', 'version': version,
                      'output': str(output), 'input_sha256': digest(probe),
                      'render_sha256': digest(render), 'processes': details}, ensure_ascii=False))


if __name__ == '__main__':
    main()
