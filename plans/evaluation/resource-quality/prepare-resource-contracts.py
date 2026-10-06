"""Create the closed resource schemas before any content promotion."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "nckh-kit"
sys.path.insert(0, str(ROOT))
from core.paths import atomic_json


def obj(properties, required=None):
    return {"type": "object", "additionalProperties": False, "properties": properties,
            "required": list(properties) if required is None else required}


string = {"type": "string", "minLength": 1}
hash_value = {"type": "string", "pattern": "^[a-f0-9]{64}$"}
notice_hash = {"type": "string", "pattern": "^([a-f0-9]{64})?$"}
source_fields = {"repository": string, "version": {"type": "string", "pattern": "^[a-f0-9]{40}$"},
                 "as_of": {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"},
                 "license": {"enum": ["MIT", "Apache-2.0"]}, "license_path": string,
                 "license_sha256": hash_value, "notice_path": {"type": "string"},
                 "notice_sha256": notice_hash, "redistribution": {"const": "permitted-with-notices"},
                 "review_reference": string}
source = obj({**source_fields, "upstream_path": string, "sha256": hash_value,
              "upstream_license_path": string})
provenance = obj({**source_fields, "source_kind": {"const": "copied-upstream"},
                  "upstream_path": string, "upstream_sha256": hash_value})
atomic_json(ROOT / "core/contracts/resource-provenance.schema.json", provenance)
resource = obj({"resource_id": string, "consumers": {"type": "array", "minItems": 1, "items": string},
                "path": string, "format": {"enum": ["json", "csv", "jsonl", "svg", "markdown"]},
                "reader": string, "producer": string,
                "requires": {"type": "array", "minItems": 1, "items": string},
                "dependency": {"enum": ["required", "optional"]}, "source": source,
                "source_kind": {"const": "copied-upstream"}, "copied_vs_reauthored": {"const": "verbatim-upstream"},
                "release_state": {"const": "experimental-local"},
                "domain": string, "locale": {"const": "en"}, "genre": string,
                "expected_artifact": string, "acceptance": string, "rollback": string})
atomic_json(ROOT / "core/contracts/resource-registry.schema.json", obj({"schema_version": {"const": 1},
            "resources": {"type": "array", "items": resource}}))
atomic_json(ROOT / "core/registry/catalog/resources.json", {"schema_version": 1, "resources": []})
print("Closed resource registry/provenance contracts created; no upstream bytes promoted.")
