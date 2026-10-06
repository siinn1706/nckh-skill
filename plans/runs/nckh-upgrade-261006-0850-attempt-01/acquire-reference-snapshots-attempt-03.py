"""Acquire bounded selected public references, retaining earlier failures."""
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

run = Path(__file__).resolve().parent
target = run / "reference-snapshots-attempt-03"
target.mkdir(exist_ok=True)
sources = {
    "aiopslab-license": "https://raw.githubusercontent.com/microsoft/AIOpsLab/main/LICENSE.txt",
    "aiopslab-notice": "https://raw.githubusercontent.com/microsoft/AIOpsLab/main/NOTICE.txt",
    "rcaeval-license": "https://raw.githubusercontent.com/phamquiluan/RCAEval/main/LICENSE",
    "otel-license": "https://raw.githubusercontent.com/open-telemetry/opentelemetry.io/main/LICENSE",
    "otel-logs": "https://opentelemetry.io/docs/specs/otel/logs/data-model/index.md",
    "otel-traces": "https://opentelemetry.io/docs/specs/otel/trace/api/index.md",
}
receipt = []
total = 0
for source_id, locator in sources.items():
    path = target / (source_id + ".txt")
    if path.exists():
        raise RuntimeError("preserve existing snapshots")
    row = {"source_id": source_id, "locator": locator, "observed_at": datetime.now(timezone.utc).isoformat(), "executed": False}
    try:
        with urllib.request.urlopen(locator, timeout=30) as response:
            data = response.read(1024 * 1024 + 1)
        total += len(data)
        if len(data) > 1024 * 1024 or total > 4 * 1024 * 1024:
            raise RuntimeError("reference byte budget exceeded")
        path.write_bytes(data)
        row.update(status="acquired", path=path.relative_to(run).as_posix(), bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), upstream_commit=None, unknown_reason="web snapshot; commit not resolved")
    except Exception as error:
        row.update(status="failed", reason=str(error))
    receipt.append(row)
    (run / "primary-snapshot-receipt-attempt-03.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
if any(row["status"] != "acquired" for row in receipt):
    raise SystemExit(1)
