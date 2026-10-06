import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

RUN = Path(__file__).resolve().parent
PROJECT = RUN.parents[2]
ROOT = PROJECT / "nckh-kit"
PLAN = PROJECT / "plans/261004-0047-nckh-research-data-hooks-writing"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
from core.build import LINK, load_json, verify_source_lock
from core.paths import atomic_json, digest_file, digest_record, no_links

lock = verify_source_lock(ROOT)
delivery = load_json(PROJECT / "plans/reports/delivery-261004-1037-r29-local-candidate.json")
assert lock["revision"] == "29" and digest_record(lock) == delivery["source_lock_hash"]
baseline = load_json(PROJECT / "plans/reports/checks-261004-1037-starting-baseline.json")
assert all(digest_file(PROJECT / name) == expected for name, expected in baseline["protected_hashes"].items())
checks = list(PLAN.glob("*.md")) + [PROJECT / "plans/reports/delivery-261004-1037-r29-local-candidate.md",
    PROJECT / "plans/reports/review-261004-1037-r29-source.md",
    PROJECT / "plans/journals/2026-10-04-nckh-r29-writers-visuals-hooks-local-checkpoint.md"]
def anchors(path):
    result, counts = set(), {}
    for line in path.read_text(encoding="utf8").splitlines():
        if not re.match(r"^#{1,6} ", line):
            continue
        heading = re.sub(r"^#{1,6}\s+", "", line).strip().lower().replace("`", "")
        slug = re.sub(r"[^\w\s-]", "", heading).replace(" ", "-")
        number = counts.get(slug, 0)
        counts[slug] = number + 1
        result.add(slug + ("-" + str(number) if number else ""))
    return result
links = anchor_count = 0
for path in checks:
    body = path.read_text(encoding="utf8")
    for href in LINK.findall(body):
        href = href.strip("<>")
        if re.match(r"^[a-z]+://", href):
            continue
        target, _, anchor = unquote(href).partition("#")
        resolved = no_links(path.parent / target).resolve() if target else path
        assert resolved.is_relative_to(PROJECT) and resolved.exists(), (path, href)
        links += 1
        if anchor:
            assert resolved.suffix == ".md" and anchor in anchors(resolved), (path, href, anchors(resolved))
            anchor_count += 1
journal = checks[-1].read_text(encoding="utf8")
assert re.search(r"^title:\s*.+", journal, re.M) and re.search(r"^date:\s*2026-10-04\s*$", journal, re.M)
phases = []
for path in sorted(PLAN.glob("phase-*.md")):
    items = re.findall(r"^- \[([ x])\] (.+)$", path.read_text(encoding="utf8"), re.M)
    phases.append({"file": str(path), "total": len(items), "done": sum(flag == "x" for flag, _ in items),
                   "pending": [item for flag, item in items if flag == " "]})
assert [(row["total"], row["done"]) for row in phases] == [(13,13),(9,9),(11,10),(12,10)]
parsed = load_json(RUN / "plan-parse.json")["data"]
assert parsed["total_tasks"] == 45 and parsed["done_tasks"] == 42 and parsed["status"] == "in-progress"
assert load_json(RUN / "plan-validate.json")["data"]["valid"] is True
receipt_files = list((RUN / "commands").glob("*.json")) + list(RUN.glob("*-frozen.process.json"))
receipts = []
for path in receipt_files:
    record = load_json(path)
    assert record["status"] != "running", path
    assert record["exit_status"] == record.get("expected_exit_status", 0), path
    assert record["process_cleanup"] == "owned-process-group-closed", path
    receipts.append({"receipt": str(path), "pid": record["pid"], "exit_status": record["exit_status"],
                     "process_cleanup": record["process_cleanup"]})
outcome = {"schema_version": 1, "status": "finalization-integrity-pass", "recorded_at": datetime.now(timezone.utc).isoformat(),
    "source_revision": "29", "source_lock_hash": digest_record(lock), "protected_hashes_checked": len(baseline["protected_hashes"]),
    "markdown_files_checked": len(checks), "local_links_checked": links, "anchors_checked": anchor_count,
    "journal_frontmatter": "valid", "phases": phases, "total_tasks": 45, "done_tasks": 42,
    "completed_owned_commands": len(receipts), "process_receipts": receipts,
    "goal_completion": "not-proven-native-owner-gates-pending", "native": "unverified", "owner_feedback": "pending"}
destination = RUN / "finalization-verification.json"
if destination.exists():
    raise RuntimeError("Preserve existing finalization verification")
atomic_json(destination, outcome)
print(json.dumps({key: outcome[key] for key in ("status", "markdown_files_checked", "local_links_checked",
    "anchors_checked", "protected_hashes_checked", "total_tasks", "done_tasks", "completed_owned_commands")}))
