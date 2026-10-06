"""Bounded read-only primary reference acquisition; never execute source content."""

import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
TARGET = RUN / "reference-snapshots"
TARGET.mkdir(exist_ok=True)
sources = {"rcaeval-readme": "https://raw.githubusercontent.com/phamquiluan/RCAEval/main/README.md",
    "aiopslab-readme": "https://raw.githubusercontent.com/microsoft/AIOpsLab/main/README.md",
    "aiopslab-license": "https://raw.githubusercontent.com/microsoft/AIOpsLab/main/LICENSE",
    "otel-conventions": "https://opentelemetry.io/docs/specs/semconv/index.md",
    "otel-metrics": "https://opentelemetry.io/docs/specs/otel/metrics/data-model/index.md"}
results = []
total = 0
for source_id, locator in sources.items():
    destination = TARGET / (source_id + ".txt")
    if destination.exists():
        raise RuntimeError("preserve prior acquisition; choose a new attempt")
    observed = datetime.now(timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(urllib.request.Request(locator, headers={"User-Agent": "NCKH-reference-review/1"}), timeout=30) as response:
            data = response.read(1024 * 1024 + 1)
            if len(data) > 1024 * 1024 or total + len(data) > 4 * 1024 * 1024:
                raise RuntimeError("trusted reference acquisition byte cap exceeded")
            total += len(data)
            destination.write_bytes(data)
            results.append({"source_id": source_id, "locator": locator, "final_url": response.url, "observed_at": observed,
                "status": "acquired", "path": destination.relative_to(RUN).as_posix(), "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(), "upstream_commit": None,
                "unknown_reason": "web snapshot only; no commit resolved; raw bytes retained privately in run", "executed": False})
    except Exception as error:
        results.append({"source_id": source_id, "locator": locator, "observed_at": observed, "status": "failed", "reason": str(error), "executed": False})
    (RUN / "primary-snapshot-receipt.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
print(json.dumps(results, indent=2))
if any(row["status"] != "acquired" for row in results):
    raise SystemExit(1)
