"""Bounded Windows access/share diagnostic; never renames or deletes resources."""
import argparse
import ctypes as c
from ctypes import wintypes as w
from datetime import datetime, timezone, timedelta
import json
import os
from pathlib import Path
import uuid

PROJECT = Path(r"C:/Users/USER\Downloads\test-skill")
TARGET = PROJECT / ".agents/skills/nckh-visuals"


class UniqueProcess(c.Structure):
    _fields_ = [("pid", w.DWORD), ("started", w.FILETIME)]


class ProcessInfo(c.Structure):
    _fields_ = [("process", UniqueProcess), ("app", w.WCHAR * 256),
                ("service", w.WCHAR * 64), ("kind", c.c_int),
                ("status", w.ULONG), ("session", w.DWORD), ("restartable", w.BOOL)]


def error(code):
    return {"code": code, "message": c.FormatError(code).strip()}


def probe(kernel, path, name, access):
    handle = kernel.CreateFileW(str(path), access, 7, None, 3, 0x02000000, None)
    if handle == c.c_void_p(-1).value:
        return {"path": str(path), "access": name, "opened": False,
                "error": error(c.get_last_error())}
    try:
        return {"path": str(path), "access": name, "opened": True}
    finally:
        if not kernel.CloseHandle(handle):
            raise c.WinError(c.get_last_error())


def resources():
    files, skipped = [], []
    pending = [TARGET]
    visited = 0
    while pending:
        folder = pending.pop()
        with os.scandir(folder) as entries:
            for entry in entries:
                visited += 1
                if visited > 256:
                    raise RuntimeError("Target exceeds bounded 256 entry enumeration")
                if entry.stat(follow_symlinks=False).st_file_attributes & 0x400:
                    skipped.append({"path": entry.path, "reason": "reparse point"})
                elif entry.is_dir(follow_symlinks=False):
                    pending.append(Path(entry.path))
                elif entry.is_file(follow_symlinks=False):
                    files.append(entry.path)
    return files, skipped


def restart_manager(files):
    rm = c.WinDLL("Rstrtmgr", use_last_error=True)
    rm.RmStartSession.argtypes = [c.POINTER(w.DWORD), w.DWORD, w.LPWSTR]
    rm.RmRegisterResources.argtypes = [w.DWORD, w.UINT, c.POINTER(w.LPCWSTR),
                                     w.UINT, c.POINTER(UniqueProcess), w.UINT, c.POINTER(w.LPCWSTR)]
    rm.RmGetList.argtypes = [w.DWORD, c.POINTER(w.UINT), c.POINTER(w.UINT),
                            c.POINTER(ProcessInfo), c.POINTER(w.DWORD)]
    rm.RmEndSession.argtypes = [w.DWORD]
    for name in ("RmStartSession", "RmRegisterResources", "RmGetList", "RmEndSession"):
        getattr(rm, name).restype = w.DWORD
    session, key = w.DWORD(), c.create_unicode_buffer(33)
    result = {"file_resources": len(files), "processes": [], "enumeration_available": False}
    rc = rm.RmStartSession(c.byref(session), 0, key)
    result["start"] = error(rc)
    if rc:
        return result
    try:
        if not files:
            result["enumeration_available"] = True
            return result
        names = (w.LPCWSTR * len(files))(*files)
        rc = rm.RmRegisterResources(session, len(files), names, 0, None, 0, None)
        result["register"] = error(rc)
        if rc:
            return result
        needed, count, reasons = w.UINT(), w.UINT(), w.DWORD()
        rc = rm.RmGetList(session, c.byref(needed), c.byref(count), None, c.byref(reasons))
        for _ in range(3):
            if rc != 234:
                break
            if needed.value > 4096:
                raise RuntimeError("Restart Manager process list exceeds bound")
            count.value = needed.value
            buffer = (ProcessInfo * count.value)()
            rc = rm.RmGetList(session, c.byref(needed), c.byref(count), buffer, c.byref(reasons))
            if not rc:
                for item in buffer[:count.value]:
                    ticks = (item.process.started.dwHighDateTime << 32) | item.process.started.dwLowDateTime
                    started = datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=ticks // 10)
                    result["processes"].append({"pid": item.process.pid,
                        "start_time_utc": started.isoformat(), "start_time_filetime": ticks,
                        "app_name": item.app, "service_name": item.service, "app_type": item.kind})
        result["get_list"] = error(rc)
        result["enumeration_available"] = rc == 0
        return result
    finally:
        result["end"] = error(rm.RmEndSession(session))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true", help="Save a fresh JSON receipt beside this script")
    parser.add_argument("--context", choices=("codex-sandbox", "controller-escalated", "user-foreground"), required=True)
    args = parser.parse_args()
    if os.name != "nt" or Path(__file__).resolve().parent != PROJECT / "plans/evaluation/personal-use":
        raise SystemExit("Restricted to the exact approved Windows project")
    result = {"observed_at": datetime.now(timezone.utc).isoformat(), "pid": os.getpid(),
              "context_declared_by_caller": args.context, "target": str(TARGET),
              "limits": ["Context is caller-declared; effective token is not dumped or equated across runs.",
                         "DELETE access opens and closes a handle only; no delete, rename or delete-on-close.",
                         "Access denied (5) does not uniquely identify ACL versus filesystem filter denial.",
                         "Sharing violation (32) indicates incompatible sharing at observation time.",
                         "Successful DELETE open does not prove the full rename or destination permissions.",
                         "Restart Manager lists users of enumerated regular files, not every directory handle or filter.",
                         "An empty process list does not exclude locks; snapshots can race.",
                         "Restart Manager creates transient OS session/registry metadata; EndSession cleans the session.",
                         "No privileges enabled, ACL changes, process stops, installation or resource writes."]}
    try:
        for path in (PROJECT / ".agents", TARGET.parent, TARGET):
            if path.lstat().st_file_attributes & 0x400:
                raise RuntimeError("Refusing reparse point in restricted target path")
        kernel = c.WinDLL("kernel32", use_last_error=True)
        kernel.CreateFileW.argtypes = [w.LPCWSTR, w.DWORD, w.DWORD, c.c_void_p,
                                      w.DWORD, w.DWORD, w.HANDLE]
        kernel.CreateFileW.restype = w.HANDLE
        kernel.CloseHandle.argtypes = [w.HANDLE]
        kernel.CloseHandle.restype = w.BOOL
        result["access_probes"] = [probe(kernel, TARGET, "FILE_READ_ATTRIBUTES", 0x80),
                                   probe(kernel, TARGET, "DELETE", 0x10000)]
        files, skipped = resources()
        result["skipped_resources"] = skipped
        result["restart_manager"] = restart_manager(files)
        result["status"] = ("diagnostic-completed" if result["restart_manager"]["enumeration_available"]
                            else "diagnostic-incomplete")
    except Exception as exc:
        result["status"] = "diagnostic-incomplete"
        result["exception"] = {"type": type(exc).__name__, "message": str(exc)}
    if args.save:
        output = Path(__file__).parent / ("diagnose-r25-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:8] + ".json")
        result["receipt"] = str(output)
        with output.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "diagnostic-completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
