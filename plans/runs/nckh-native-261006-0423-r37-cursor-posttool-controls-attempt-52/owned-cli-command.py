"""Monitor each exact child and its process tree while keeping native command output."""

import ctypes
import hashlib
import json
import subprocess
import threading
import time
import uuid
from ctypes import wintypes
from datetime import datetime, timedelta, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2].resolve()
ROOT_GENERATIONS = {}
kernel = ctypes.WinDLL('kernel32', use_last_error=True)


class Entry(ctypes.Structure):
    _fields_ = [('dwSize', wintypes.DWORD), ('cntUsage', wintypes.DWORD), ('pid', wintypes.DWORD),
                ('heap', ctypes.c_size_t), ('module', wintypes.DWORD), ('threads', wintypes.DWORD),
                ('ppid', wintypes.DWORD), ('priority', wintypes.LONG), ('flags', wintypes.DWORD),
                ('name', wintypes.WCHAR * 260)]


kernel.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
kernel.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
kernel.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(Entry)]
kernel.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(Entry)]
kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
kernel.OpenProcess.restype = wintypes.HANDLE
kernel.CloseHandle.argtypes = [wintypes.HANDLE]
kernel.GetProcessTimes.argtypes = [wintypes.HANDLE, *([ctypes.POINTER(wintypes.FILETIME)] * 4)]


def creation_ticks(pid):
    handle = kernel.OpenProcess(0x1000, False, pid)
    if not handle:
        return None
    try:
        fields = [wintypes.FILETIME() for _ in range(4)]
        if not kernel.GetProcessTimes(handle, *[ctypes.byref(f) for f in fields]):
            return None
        return (fields[0].dwHighDateTime << 32) | fields[0].dwLowDateTime
    finally:
        kernel.CloseHandle(handle)


def tree(root):
    handle = kernel.CreateToolhelp32Snapshot(2, 0)
    if handle == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    rows = []
    try:
        entry = Entry()
        entry.dwSize = ctypes.sizeof(entry)
        available = kernel.Process32FirstW(handle, ctypes.byref(entry))
        while available:
            rows.append((entry.pid, entry.ppid, entry.name))
            available = kernel.Process32NextW(handle, ctypes.byref(entry))
    finally:
        kernel.CloseHandle(handle)
    selected = {root}
    while True:
        expanded = selected | {pid for pid, parent, _ in rows if parent in selected}
        if expanded == selected:
            break
        selected = expanded
    output = []
    for pid, parent, name in rows:
        if pid not in selected:
            continue
        ticks = creation_ticks(pid)
        if ticks is not None:
            created = datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=ticks // 10)
            output.append({'pid': pid, 'parent_pid': parent, 'name': name,
                           'creation_filetime_ticks': ticks, 'creation_utc': created.isoformat()})
    root_row = next((row for row in output if row["pid"] == root), None)
    expected = ROOT_GENERATIONS.get(root)
    if root_row is None or (expected is not None and root_row["creation_filetime_ticks"] != expected):
        return []
    selected = {root: root_row}
    while True:
        added = {row["pid"]: row for row in output if row["pid"] not in selected and
                 row["parent_pid"] in selected and
                 row["creation_filetime_ticks"] >= selected[row["parent_pid"]]["creation_filetime_ticks"]}
        if not added:
            return list(selected.values())
        selected.update(added)


def save(path, data):
    path = Path(path).resolve()
    if not path.is_relative_to(WORK):
        raise ValueError("Controller evidence target is outside the owned workspace")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".writing-" + uuid.uuid4().hex)
    with temporary.open("x", encoding="utf8") as stream:
        stream.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    delays = (0, 0.025, 0.05, 0.1, 0.2, 0.4)
    for index, delay in enumerate(delays):
        if delay:
            time.sleep(delay)
        try:
            temporary.replace(path)
            return
        except PermissionError as error:
            if getattr(error, "winerror", None) not in {5, 32, 33} or index == len(delays) - 1:
                raise
    raise AssertionError("Atomic write did not reach a terminal outcome")


def run_command(name, argv, *, cwd=RUN, timeout=45, env=None, stdin=None):
    directory = RUN / 'commands'
    receipt = directory / (name + '.json')
    assert not receipt.exists(), 'Preserve command receipt'
    directory.mkdir(exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    begin = time.monotonic()
    process = subprocess.Popen([str(item) for item in argv], cwd=cwd, env=env,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NO_WINDOW)
    record = {'command': [str(item) for item in argv], 'pid': process.pid, 'cwd': str(cwd),
              'started_at': started, 'creation_filetime_ticks': creation_ticks(process.pid),
              'owned_by': str(RUN), 'port': None, 'port_authority': 'native CLI manages listener ports',
              'status': 'running', 'timeout_seconds': timeout}
    ROOT_GENERATIONS[process.pid] = record["creation_filetime_ticks"]
    save(receipt, record)
    stop = threading.Event()
    identities = {}
    errors = []

    def capture():
        try:
            for row in tree(process.pid):
                identities[str(row['pid']) + ':' + str(row['creation_filetime_ticks'])] = row
            save(directory / (name + '.process-tree.json'), {'root_pid': process.pid,
                'processes': list(identities.values()), 'capture_errors': list(errors),
                'captured_at': datetime.now(timezone.utc).isoformat()})
        except Exception as error:
            errors.append(type(error).__name__ + ': ' + str(error))

    def monitor():
        while not stop.is_set():
            capture()
            stop.wait(0.25)

    watcher = threading.Thread(target=monitor, daemon=True)
    watcher.start()
    timed_out = False
    try:
        stdout, stderr = process.communicate(stdin, timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate(timeout=10)
    finally:
        stop.set()
        watcher.join(timeout=5)
        capture()
    (directory / (name + '.stdout.txt')).write_bytes(stdout)
    (directory / (name + '.stderr.txt')).write_bytes(stderr)
    sha = lambda value: hashlib.sha256(value).hexdigest()
    record.update(status='timeout' if timed_out else 'completed', exit_code=process.returncode,
        ended_at=datetime.now(timezone.utc).isoformat(), elapsed_seconds=round(time.monotonic() - begin, 3),
        process_exited=process.poll() is not None, stdout_sha256=sha(stdout), stderr_sha256=sha(stderr),
        observed_process_identities=len(identities), capture_errors=errors,
        owned_handle_stop_performed=timed_out)
    save(receipt, record)
    print(json.dumps({'command': name, 'exit_code': process.returncode,
        'elapsed_seconds': record['elapsed_seconds'], 'process_identities': len(identities)}), flush=True)
    assert not errors, 'Process monitor failed; retain command and stop dependent work'
    return record, stdout, stderr
