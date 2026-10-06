"""Record real current-source CLI bindings and absent-root OFF behavior."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
KIT = RUN.parents[2] / "nckh-kit"
catalog = json.loads((KIT / "core/registry/catalog/resources.json").read_text())
results = []
for row in catalog["resources"]:
    if row["source_kind"] != "owned-reference":
        continue
    for consumer in row["consumers"]:
        argv = [sys.executable, "-I", str(KIT / row["reader"]), "--resource-id", row["resource_id"],
                "--consumer", consumer, "--domain", row["domain"], "--locale", row["locale"], "--genre", row["genre"], "--json"]
        completed = subprocess.run(argv, cwd=RUN, capture_output=True)
        name = row["resource_id"] + "-" + consumer
        (RUN / (name + ".stdout.json")).write_bytes(completed.stdout)
        (RUN / (name + ".stderr.txt")).write_bytes(completed.stderr)
        actual = json.loads(completed.stdout)
        assert completed.returncode == 0 and actual["resource_read"] and actual["records"]
        results.append({"argv": argv, "cwd": str(RUN), "exit_code": completed.returncode, "resource_id": row["resource_id"],
            "consumer": consumer, "records": len(actual["records"]), "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
            "resource_sha256": row["source"]["sha256"], "reader_sha256": actual["reader_sha256"], "observed": True})
spec = importlib.util.spec_from_file_location("actual_reader", KIT / "scripts/search-resource.py")
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)
absent = RUN / "absent-off-resource-root"
assert not absent.exists()
off = reader.lookup("R-telemetry-dictionary", "nckh-telemetry", domain="observability-research", genre="telemetry-field-reference", resource_access="off", root=absent)
assert off["resource_read"] is False and off["status"] == "resource-disabled"
receipt = {"schema_version": 1, "bindings": results, "binding_count": len(results), "off": {"root": str(absent), "exists": False, "result": off},
    "scope": "Current-source local CLI reads and OFF absent-root behavior; relocated bundle checks deferred until candidate freeze"}
(RUN / "p5-local-reader-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"bindings": len(results), "off": off["status"]}))
