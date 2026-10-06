"""Read the current native application's model catalogue through its owned proxy."""

import json
import queue
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT / "nckh-kit"))
from core.processes import owned_process


def main():
    executable = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    if not output.is_relative_to(PROJECT):
        raise ValueError("receipt must remain in this project")
    output.parent.mkdir(parents=True, exist_ok=True)
    record = {"observed_at": datetime.now(timezone.utc).isoformat(),
              "route": "current-native-app-server-proxy", "status": "not-run",
              "executable": str(executable), "models": []}
    stderr = output.with_suffix(".stderr.txt")
    messages = queue.Queue()
    with stderr.open("xb") as errors:
        with owned_process([str(executable), "app-server", "proxy"], PROJECT,
                           subprocess.PIPE, errors) as (process, _):
            record["pid"] = process.pid

            def read_stdout():
                for line in iter(process.stdout.readline, b""):
                    messages.put(line)
                messages.put(None)

            reader = threading.Thread(target=read_stdout, daemon=True)
            reader.start()

            def send(message):
                process.stdin.write((json.dumps(message) + "\n").encode())
                process.stdin.flush()

            def response(identity):
                deadline = time.monotonic() + 30
                while time.monotonic() < deadline:
                    raw = messages.get(timeout=max(0.1, deadline - time.monotonic()))
                    if raw is None:
                        raise RuntimeError("proxy exited before response")
                    item = json.loads(raw)
                    if item.get("id") == identity:
                        if "error" in item:
                            raise RuntimeError(str(item["error"]))
                        return item["result"]
                raise TimeoutError("native catalogue response timeout")

            try:
                send({"id": 1, "method": "initialize", "params": {
                    "clientInfo": {"name": "nckh-project-model-probe", "version": "1"}}})
                record["initialize"] = response(1)
                send({"method": "initialized", "params": {}})
                cursor = None
                for index in range(10):
                    send({"id": index + 2, "method": "model/list", "params": {
                        "limit": 100, "includeHidden": False, "cursor": cursor}})
                    page = response(index + 2)
                    record["models"].extend(page["data"])
                    cursor = page.get("nextCursor")
                    if cursor is None:
                        break
                if cursor is not None:
                    raise RuntimeError("catalogue pagination incomplete")
                record["status"] = "catalogue-observed"
            except (OSError, ValueError, RuntimeError, TimeoutError, queue.Empty) as error:
                record["status"] = "unavailable"
                record["error"] = str(error)
    record["process_cleanup"] = "owned-proxy-closed; existing-daemon-preserved"
    with output.open("x", encoding="utf-8") as receipt:
        json.dump(record, receipt, ensure_ascii=False, indent=2)
        receipt.write("\n")
    print(json.dumps({"status": record["status"], "count": len(record["models"]),
                      "receipt": str(output), "error": record.get("error")}, ensure_ascii=False))
    return 0 if record["status"] == "catalogue-observed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
