"""Read actual Windows process exit state without treating cached creation times as liveness."""
import ctypes
from ctypes import wintypes

kernel = ctypes.WinDLL("kernel32", use_last_error=True)
kernel.OpenProcess.argtypes = [wintypes.DWORD,wintypes.BOOL,wintypes.DWORD]
kernel.OpenProcess.restype = wintypes.HANDLE
kernel.CloseHandle.argtypes = [wintypes.HANDLE]
kernel.GetExitCodeProcess.argtypes = [wintypes.HANDLE,ctypes.POINTER(wintypes.DWORD)]
kernel.GetExitCodeProcess.restype = wintypes.BOOL
kernel.GetProcessTimes.argtypes = [wintypes.HANDLE,*([ctypes.POINTER(wintypes.FILETIME)]*4)]
kernel.GetProcessTimes.restype = wintypes.BOOL

def state(pid):
    handle = kernel.OpenProcess(0x1000,False,pid)
    if not handle:
        error = ctypes.get_last_error()
        return {"pid":pid,"status":"absent" if error in {87,1168} else "unobservable","winerror":error,
                "creation_filetime_ticks":None,"exit_code":None}
    try:
        fields = [wintypes.FILETIME() for _ in range(4)]
        if not kernel.GetProcessTimes(handle,*[ctypes.byref(field) for field in fields]):
            raise ctypes.WinError(ctypes.get_last_error())
        exit_code = wintypes.DWORD()
        if not kernel.GetExitCodeProcess(handle,ctypes.byref(exit_code)):
            raise ctypes.WinError(ctypes.get_last_error())
        ticks = (fields[0].dwHighDateTime << 32) | fields[0].dwLowDateTime
        return {"pid":pid,"status":"active" if exit_code.value == 259 else "terminated",
                "creation_filetime_ticks":ticks,"exit_code":exit_code.value,"winerror":None}
    finally:
        kernel.CloseHandle(handle)

def active_generation(pid,ticks):
    observed = state(pid)
    if observed["status"] == "unobservable":
        raise RuntimeError("Owned process state is unobservable; retain failure and audit")
    return observed["status"] == "active" and observed["creation_filetime_ticks"] == ticks
