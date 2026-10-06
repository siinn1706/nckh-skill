"""Add an explicit owned reference provenance variant without relabeling copies."""

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "nckh-kit"
def text(): return {"type": "string", "minLength": 1}
def arr(item): return {"type": "array", "items": item}
def obj(**fields): return {"type": "object", "additionalProperties": False, "properties": fields, "required": list(fields)}
def enum(*items): return {"enum": list(items)}
def sha(): return {"type": "string", "pattern": "^[a-f0-9]{64}$"}
def binding(): return obj(path=text(), sha256=sha())
def read(path): return json.loads((ROOT / path).read_text(encoding="utf-8"))
def save(path, value): (ROOT / path).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

owned = obj(schema_version={"const": 1}, source_kind={"const": "owned-reference"},
    copied_vs_reauthored={"const": "reauthored-with-sources"}, artifact_sha256=sha(), authoring_version=text(), as_of=text(),
    authoring_disposition={"const": "original-summary-no-upstream-bytes"}, release_rights={"const": "local-package-only"},
    record_ids=arr(text()), rights_record=binding(), attribution_record=binding(),
    contributions=arr(obj(source_id=text(), locator=text(), version_kind=enum("git-commit", "archive-snapshot", "web-snapshot"),
        version_or_snapshot=text(), upstream_commit={"description": "Verified 40 hex commit or null with unknown_reason."},
        unknown_reason={"type": "string"}, observed_hash=sha(), as_of=text(), license=text(),
        rights_scope={"const": "metadata-reference"}, attribution=text(), transformation={"const": "concept-only-own-text"},
        applicability=text(), record_ids=arr(text()))))
save("core/contracts/owned-resource-provenance.schema.json", owned)
registry = read("core/contracts/resource-registry.schema.json")
props = registry["properties"]["resources"]["items"]["properties"]
props["source_kind"]["enum"].append("owned-reference")
props["copied_vs_reauthored"]["enum"].append("reauthored-with-sources")
props["owned_provenance"] = copy.deepcopy(owned)
source = props["source"]
for key in ("upstream_path", "upstream_license_path"):
    source["required"].remove(key)
for key, value in (("license", "owned-local-package"), ("rights_scope", "local-package-only"),
                   ("redistribution", "local-package-only"), ("version_kind", "owned-authored")):
    source["properties"][key]["enum"].append(value)
save("core/contracts/resource-registry.schema.json", registry)
bundle = read("installer/schemas/bundle-v2.schema.json")
file_schema = bundle["properties"]["files"]["items"]["properties"]
file_schema["rights"]["enum"].append("owned-reference")
provenance = file_schema["provenance"]
provenance["required"] = []
for key, value in owned["properties"].items():
    if key not in provenance["properties"]:
        provenance["properties"][key] = value
provenance["properties"]["source_kind"]["enum"].append("owned-reference")
provenance["properties"]["copied_vs_reauthored"]["enum"].append("reauthored-with-sources")
save("installer/schemas/bundle-v2.schema.json", bundle)
print("owned provenance and explicit registry/manifest variants authored; typed owner validation remains mandatory")
