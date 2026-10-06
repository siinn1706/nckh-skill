"""Run only an owned process group; retain output without claiming task acceptance."""

import os
import signal
import subprocess
import time
from contextlib import contextmanager


class WindowsJob:
    """Assign a suspended child before it can create untracked descendants."""

    def __init__(self):
        import ctypes
        from ctypes import wintypes as w
        self.c = ctypes
        self.assigned = False
        self.k = ctypes.WinDLL("kernel32", use_last_error=True)
        signatures = {
            "CreateJobObjectW": ([w.LPVOID, w.LPCWSTR], w.HANDLE),
            "SetInformationJobObject": ([w.HANDLE, ctypes.c_int, w.LPVOID, w.DWORD], w.BOOL),
            "AssignProcessToJobObject": ([w.HANDLE, w.HANDLE], w.BOOL),
            "TerminateJobObject": ([w.HANDLE, w.UINT], w.BOOL),
            "OpenProcess": ([w.DWORD, w.BOOL, w.DWORD], w.HANDLE),
            "CreateToolhelp32Snapshot": ([w.DWORD, w.DWORD], w.HANDLE),
            "Thread32First": ([w.HANDLE, w.LPVOID], w.BOOL),
            "Thread32Next": ([w.HANDLE, w.LPVOID], w.BOOL),
            "OpenThread": ([w.DWORD, w.BOOL, w.DWORD], w.HANDLE),
            "ResumeThread": ([w.HANDLE], w.DWORD),
            "CloseHandle": ([w.HANDLE], w.BOOL),
        }
        for name, (args, result) in signatures.items():
            fn = getattr(self.k, name)
            fn.argtypes, fn.restype = args, result

        class Basic(ctypes.Structure):
            _fields_ = [("process_time", ctypes.c_longlong), ("job_time", ctypes.c_longlong),
                        ("flags", w.DWORD), ("min_working", ctypes.c_size_t),
                        ("max_working", ctypes.c_size_t), ("process_limit", w.DWORD),
                        ("affinity", ctypes.c_size_t), ("priority", w.DWORD), ("scheduling", w.DWORD)]

        class Extended(ctypes.Structure):
            _fields_ = [("basic", Basic), ("io", ctypes.c_ulonglong * 6),
                        ("process_memory", ctypes.c_size_t), ("job_memory", ctypes.c_size_t),
                        ("peak_process", ctypes.c_size_t), ("peak_job", ctypes.c_size_t)]

        self.handle = self.k.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        limits = Extended()
        limits.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.k.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            self.close()
            raise ctypes.WinError(ctypes.get_last_error())

    def assign_and_resume(self, pid):
        c = self.c
        from ctypes import wintypes as w
        process = self.k.OpenProcess(0x0101, False, pid)
        if not process:
            raise c.WinError(c.get_last_error())
        try:
            if not self.k.AssignProcessToJobObject(self.handle, process):
                raise c.WinError(c.get_last_error())
            self.assigned = True
        finally:
            self.k.CloseHandle(process)

        class Thread(c.Structure):
            _fields_ = [("size", w.DWORD), ("usage", w.DWORD), ("id", w.DWORD),
                        ("owner", w.DWORD), ("priority", w.LONG), ("delta", w.LONG), ("flags", w.DWORD)]

        snapshot = self.k.CreateToolhelp32Snapshot(4, 0)
        if snapshot == w.HANDLE(-1).value:
            raise c.WinError(c.get_last_error())
        resumed = False
        try:
            entry = Thread()
            entry.size = c.sizeof(entry)
            more = self.k.Thread32First(snapshot, c.byref(entry))
            while more:
                if entry.owner == pid:
                    thread = self.k.OpenThread(2, False, entry.id)
                    if not thread:
                        raise c.WinError(c.get_last_error())
                    try:
                        if self.k.ResumeThread(thread) != 1:
                            raise OSError("owned child thread did not resume from its initial suspension")
                        resumed = True
                    finally:
                        self.k.CloseHandle(thread)
                    break
                entry.size = c.sizeof(entry)
                more = self.k.Thread32Next(snapshot, c.byref(entry))
            if not resumed:
                raise OSError("owned suspended child thread was not found")
        finally:
            self.k.CloseHandle(snapshot)

    def kill(self):
        if self.handle and not self.k.TerminateJobObject(self.handle, 1):
            raise self.c.WinError(self.c.get_last_error())

    def close(self):
        if self.handle:
            self.k.CloseHandle(self.handle)
            self.handle = None


@contextmanager
def owned_process(argv, cwd, stdout, stderr):
    job = WindowsJob() if os.name == "nt" else None
    process = None
    try:
        process = subprocess.Popen(argv, cwd=cwd, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr,
                                   shell=False, start_new_session=os.name != "nt",
                                   creationflags=0x00000004 | subprocess.CREATE_NEW_PROCESS_GROUP if job else 0)
        if job:
            job.assign_and_resume(process.pid)
        yield process, job
    finally:
        try:
            if process is not None:
                stop_process(process, job)
                if process.stdin:
                    process.stdin.close()
        finally:
            if job:
                job.close()


def stop_process(process, job):
    if job and not job.assigned:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        return
    if process.poll() is None:
        try:
            if job:
                process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=2)
        except (OSError, subprocess.TimeoutExpired):
            if job:
                job.kill()
            else:
                os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)
    if not job:
        try:
            os.killpg(process.pid, signal.SIGTERM)
            deadline = time.monotonic() + 2
            while time.monotonic() < deadline:
                os.killpg(process.pid, 0)
                time.sleep(0.05)
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def run_owned_command(argv, cwd, input_bytes, stdout_path, stderr_path, *, timeout, on_started=None):
    started = time.monotonic()
    with open(stdout_path, "xb") as stdout, open(stderr_path, "xb") as stderr:
        with owned_process(argv, cwd, stdout, stderr) as (process, job):
            pid = process.pid
            if on_started:
                on_started(pid)
            try:
                process.communicate(input=input_bytes, timeout=timeout)
                status = "completed-unreviewed" if process.returncode == 0 else "fail"
                exit_status = process.returncode
            except subprocess.TimeoutExpired:
                stop_process(process, job)
                status, exit_status = "timeout-unknown", None
    return {"status": status, "exit_status": exit_status, "pid": pid,
            "seconds": time.monotonic() - started, "process_cleanup": "owned-process-group-closed"}
