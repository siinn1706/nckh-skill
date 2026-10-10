"""Record observed command/process evidence in ignored local state."""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    root = Path(__file__).resolve().parents[3]
    record = root / ".nckh-state/release-r46-261010/commands" / args.label
    record.mkdir(parents=True, exist_ok=False)
    receipt_path = record / "receipt.json"
    receipt = {
        "argv": command, "cwd": str(args.cwd.resolve()),
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "starting", "wrapper_pid": os.getpid(),
    }

    def write():
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    write()
    started = time.monotonic()
    with (record / "stdout.txt").open("wb") as stdout, (record / "stderr.txt").open("wb") as stderr:
        try:
            process = subprocess.Popen(command, cwd=args.cwd, stdout=stdout, stderr=stderr)
            receipt.update(pid=process.pid, status="running")
            write()
            print(json.dumps({"command": args.label, "pid": process.pid}), flush=True)
            exit_code = process.wait()
        except BaseException as error:
            receipt.update(status="error", error=str(error))
            write()
            raise
    receipt.update(
        status="completed", exit_code=exit_code, process_reaped=True,
        finished_at_utc=datetime.now(timezone.utc).isoformat(),
        elapsed_seconds=round(time.monotonic() - started, 3),
        stdout_sha256=hashlib.sha256((record / "stdout.txt").read_bytes()).hexdigest(),
        stderr_sha256=hashlib.sha256((record / "stderr.txt").read_bytes()).hexdigest(),
    )
    write()
    print(json.dumps({"command": args.label, "exit_code": exit_code,
                      "elapsed_seconds": receipt["elapsed_seconds"], "process_reaped": True}), flush=True)
    if exit_code:
        print((record / "stderr.txt").read_text(encoding="utf-8", errors="replace")[-4000:], file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
