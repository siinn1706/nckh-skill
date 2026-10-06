import ast
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
PROJECT = RUN.parents[2]
ROOT = PROJECT / "nckh-kit"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from core.build import (APPROVED_IDENTITIES, BASE_IDENTITIES, LINK, load_json,
                        reference_path, source_members, validate_catalog)
from core.evaluation import validate_case_manifest, validate_writer_matrix
from core.paths import atomic_json, digest_file, digest_record
from core.schema import _check_schema


baseline = load_json(PROJECT / "plans/reports/checks-261004-1037-starting-baseline.json")
assert set(baseline["baseline_ids"]) == BASE_IDENTITIES
catalog = validate_catalog(load_json(ROOT / "core/registry/catalog/skills.json"))
assert set(catalog) == APPROVED_IDENTITIES
cases = {}
for path in (ROOT / "evals/cases").glob("*/*.json"):
    record = load_json(path)
    if "skill_id" in record:
        rows = validate_case_manifest(record, catalog)
        assert not set(rows) & set(cases)
        cases.update(rows)
assert set(cases) == set(baseline["baseline_case_ids"]) | {
    writer + ":" + kind for writer in ("nckh-humanwrite", "nckh-paperwrite")
    for kind in ("positive", "negative", "outcome", "failure")}
protected = {relative: digest_file(PROJECT / relative) for relative in baseline["protected_hashes"]}
assert protected == baseline["protected_hashes"], "protected baseline bytes changed"
members = source_members(ROOT)
archive = Path(baseline["baseline_archive"])
if not archive.is_absolute():
    archive = PROJECT / archive
assert digest_file(archive) == baseline["baseline_archive_sha256"]
with zipfile.ZipFile(archive) as saved:
    old = set(saved.namelist())
    changes = [{"path": member, "state": "added" if member not in old else "changed",
                "sha256": digest_file(ROOT / member)} for member in members
               if member not in old or saved.read(member) != (ROOT / member).read_bytes()]
    removed = sorted(old - set(members) - {"core/registry/source-lock/source-lock.json"})
assert not removed, removed
links = parsed = schemas = 0
for member in members:
    path = ROOT / member
    if path.suffix == ".py":
        ast.parse(path.read_text(encoding="utf8"), filename=member)
        parsed += 1
    elif path.suffix == ".md":
        for href in LINK.findall(path.read_text(encoding="utf8")):
            reference_path(ROOT, path, href)
            links += 1
    elif path.name.endswith(".schema.json"):
        _check_schema(load_json(path))
        schemas += 1
writer = validate_writer_matrix(load_json(ROOT / "evals/cases/runtime/writer-invocation-matrix.json"))
result = {"schema_version": 1, "recorded_at": datetime.now(timezone.utc).isoformat(),
    "status": "pre-freeze-integrity-pass", "evidence_class": "static",
    "project": str(PROJECT), "source": str(ROOT), "run": str(RUN),
    "source_lock_revision": load_json(ROOT / "core/registry/source-lock/source-lock.json")["revision"],
    "source_lock_matches_edited_source": False, "freeze_owner": "/root",
    "identities": sorted(catalog), "base_case_ids": sorted(cases), "writer_matrix": writer,
    "protected_hashes_checked": len(protected), "protected_hashes": protected,
    "changed_source_files": changes, "removed_source_files": removed, "source_inventory_count": len(members),
    "python_files_parsed": parsed, "schema_files_checked": schemas, "markdown_links_checked": links,
    "historical_matrix_hash": digest_file(ROOT / "evals/cases/runtime/invocation-matrix.json"),
    "native": "unverified", "owner_review": "pending-personal-review", "scientific": "pending"}
atomic_json(RUN / "pre-freeze-state.json", result)
print(json.dumps({key: result[key] for key in ("status", "source_inventory_count", "protected_hashes_checked",
                                             "python_files_parsed", "schema_files_checked", "markdown_links_checked")}))
