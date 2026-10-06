import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
PROJECT = RUN.parents[2]
ROOT = PROJECT / "nckh-kit"
REPORTS = PROJECT / "plans/reports"
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
from core.build import load_json, verify_source_lock
from core.paths import atomic_json, digest_file, digest_record

records = {name: load_json(RUN / filename) for name, filename in {
    "static": "validate.json", "deterministic": "deterministic.json",
    "build": "delivery-context.json", "archives": "archive-summary.json",
    "smoke": "smoke-summary.json", "preview": "installer-previews.json",
    "preservation": "final-preservation.json"}.items()}
lock = verify_source_lock(ROOT)
assert lock["revision"] == "29"
source_hash = digest_record(lock)
assert all(record["source_lock_hash"] == source_hash for record in records.values())
assert all(record["status"] == ("built" if name == "build" else "pass") for name, record in records.items())
assert records["deterministic"]["deterministic"]["status"] == "pass"
assert records["static"]["identities"] == 39 and records["static"]["skill_cases"] == 156
artifacts = {(row["variant"], row["host"]): row for row in records["build"]["artifacts"]}
assert len(artifacts) == len(records["archives"]["artifacts"]) == len(records["smoke"]["bundles"]) == 16
for row in records["archives"]["artifacts"]:
    key = row["variant"], row["host"]
    chain = load_json(RUN / "receipts" / ("-".join(key)) / "archive-chain.json")
    assert chain["archive_sha256"] == row["archive_sha256"] == digest_file(Path(row["archive"]))
    assert chain["source_lock_hash"] == source_hash
    assert chain["closure_hash"] == artifacts[key]["closure_hash"]
    assert chain["bundle"] == row["extracted"]
smokes = records["smoke"]["bundles"]
assert all(row["status"] == "pass" and row["project_unchanged"] for row in smokes)
assert len(records["preview"]["surfaces"]) == 8
assert all(row["project_unchanged"] and row["entries"] == 45 for row in records["preview"]["surfaces"])
reads = sum(row["resource_reads"] for row in smokes)
disabled = sum(row["writer_disabled_observations"] for row in smokes)
projections = sum(row["hook_projections_exercised"] for row in smokes)
assert (reads, disabled, projections) == (216, 48, 24)
test_output = records["deterministic"]["deterministic"]["output"]
skips = re.search(r"skipped=(\d+)", test_output)
summary = {"schema_version": 1, "recorded_at": datetime.now(timezone.utc).isoformat(),
    "status": "local-technical-checkpoint-pass-pending-user-gates", "source_revision": "29",
    "source_lock_hash": source_hash, "source_files_pinned": len(lock["files"]),
    "identities": 39, "base_cases": 156, "required_families": 19, "historical_matrix_cells": 224,
    "writer_native_cells": 256, "writer_scenarios": 20, "writer_matrix_observation": "unverified",
    "deterministic_tests": records["deterministic"]["deterministic"]["tests"],
    "deterministic_skips": int(skips.group(1)) if skips else 0,
    "reproducibility_variants": 4, "bundles_built_extracted_verified": 16,
    "actual_resource_reads": reads, "writer_disabled_no_read_observations": disabled,
    "hook_projections_exercised": projections, "installer_preview_surfaces": 8,
    "protected_hashes_unchanged": records["preservation"]["protected_hashes_checked"],
    "legacy_bundles": records["preservation"]["legacy_bundles"],
    "installed_revision": "25", "installed_update": "not-performed",
    "hooks_registered_enabled_trusted": False, "native": "unverified",
    "owner_review": "pending-personal-review", "scientific": "pending", "public_release": "not-performed",
    "archives": records["archives"]["artifacts"],
    "evidence_receipts": {name: {"path": str(RUN / filename), "sha256": digest_file(RUN / filename)}
        for name, filename in {"static": "validate.json", "deterministic": "deterministic.json",
        "build": "delivery-context.json", "archives": "archive-summary.json", "smoke": "smoke-summary.json",
        "preview": "installer-previews.json", "preservation": "final-preservation.json"}.items()}}
json_path = REPORTS / "delivery-261004-1037-r29-local-candidate.json"
md_path = json_path.with_suffix(".md")
if json_path.exists() or md_path.exists():
    raise RuntimeError("Preserve existing delivery report")
atomic_json(json_path, summary)
variants = ("on-standalone", "off-standalone", "on-plugin", "off-plugin")
table = "\n".join("| " + host + " | " + " | ".join(str(artifacts[variant, host]["files"]) for variant in variants) + " |"
    for host in ("claude", "codex", "cursor", "agy"))
md = f"""# NCKH r29 — bàn giao candidate cục bộ

Status: **local technical checkpoint PASS; native/owner/scientific gates pending**.

Thực thi theo `/goal ak-cook --auto` cho [kế hoạch](../261004-0047-nckh-research-data-hooks-writing/plan.md).
Source r29 có **281 pins**, canonical source-lock hash `{source_hash}`.
[Structured receipt](delivery-261004-1037-r29-local-candidate.json) bind các receipt thực và 16 archive hashes.

## Kết quả triển khai

- `nckh-humanwrite` và `nckh-paperwrite` dùng `--en`/`--vi`, chung preservation/language contract; `nckh-write` giữ route tương thích theo action. Humanizer là policy Markdown re-authored/attributed; LanguageTool còn deferred, optional English diagnostic.
- Scientific visuals có research-purpose, origin labels và source/code/transform/output/run bindings. Diagnostic phép tính thực đọc transform JSON. Purpose/hash không xác thực scientific truth hoặc một receipt bịa nhưng tự nhất quán; native engine/render/editability vẫn có gate riêng.
- Neutral hook policy, bốn codecs, runner/manual checker và config preview/apply/remove/recover đã có bounded tests và portable closure. Apply là transaction riêng, cần preview hash, grant và native evidence đúng host/version/surface. Templates và plugin reference projection giữ inactive.
- Catalog/profile/build/evaluation đúng **39 identities = 37 cũ + 2 writers**, **156 base cases**, **19 families**, **9 resources**. Giữ 148 old case IDs, historical 224 matrix và comparator/receipts. Bốn visual prompt bytes đã đổi; không regrade bằng receipt cũ.

## Evidence thực đã hoàn tất

| Checkpoint | Kết quả | Receipt |
|---|---|---|
| Full deterministic | 181 tests, `OK (skipped=1)`, 806.511 giây; một real-symlink fixture bị giới hạn quyền Windows | [result](../runs/{RUN.name}/deterministic.json), [owned process cleanup](../runs/{RUN.name}/deterministic-frozen.process.json) |
| Reproducibility/build | 4 variants × 4 hosts; đủ 16 persistent bundles | [build context](../runs/{RUN.name}/delivery-context.json) |
| Actual archive/extract | 16 ZIP được Compress-Archive/Expand-Archive ra ngoài repository; extraction manifest/closure và archive chain khớp build | [archive receipt](../runs/{RUN.name}/archive-summary.json) |
| Extracted resource reads | 216 actual observations: 27 consumer/resource pairs × 8 resource-on bundles; source/license/lineage hashes được đọc | [smoke receipt](../runs/{RUN.name}/smoke-summary.json) |
| Disabled writers | 48 direct packaged-reader observations trên resource-off trả disabled, no-read, empty records | [per-bundle receipts](../runs/{RUN.name}/receipts/) |
| Hook relocation | 24 primary/reference projections gọi runner, manual block và config preview từ outside CWD; disposable projects giữ nguyên bytes | [smoke receipt](../runs/{RUN.name}/smoke-summary.json) |
| Installer preview | 8 surfaces, mỗi preview 39 skills + 6 native-agent proposals, không conflict và không viết project | [preview receipt](../runs/{RUN.name}/installer-previews.json) |
| Preservation/legacy | 509 protected hashes không đổi; installed r25 chưa cập nhật; 4 existing schema-v1 bundles đọc được bằng verifier mới | [final preservation](../runs/{RUN.name}/final-preservation.json) |

[Independent writer forward test](reviewer-261004-1037-writer-forward-test.md) có bốn actual local agent trials: VI minimal polish, EN Methods outline, conflicting flags và ambiguous locale. Đây không phải native invocation, human taste hoặc scientific acceptance. Supplemental writer matrix **256 planned native cells / 20 scenarios** đã validate; observed behavior vẫn unverified, tách khỏi historical 224 cells.

## Gói để xem và dùng sau grant phù hợp

Resource-access ON giữ contract sử dụng/phân phối công khai; OFF chỉ là đối chứng nội bộ. Các archive dưới đây chưa được publish hoặc cài vào installation hiện có.

- [Claude standalone resource-on](../runs/{RUN.name}/archives/on-standalone-claude.zip)
- [Codex standalone resource-on](../runs/{RUN.name}/archives/on-standalone-codex.zip)
- [Cursor standalone resource-on](../runs/{RUN.name}/archives/on-standalone-cursor.zip)
- [Antigravity standalone resource-on](../runs/{RUN.name}/archives/on-standalone-agy.zip)
- [Đủ 16 archives, gồm inactive plugin projection](../runs/{RUN.name}/archives/)

Manifest file counts, không tính `manifest.json`:

| Host | ON standalone | OFF standalone | ON plugin | OFF plugin |
|---|---:|---:|---:|---:|
{table}

Hook closure có 26 members cho Claude/Codex, 25 cho Cursor/AGY. Packaging không đăng ký, enable hoặc trust hook. Setup/lifecycle commands do [installation docs](../../nckh-kit/docs/installation.md) sở hữu.

## Failures, review và cổng còn mở

[Review trước freeze](review-261004-1037-pre-freeze.md), [review r29 delta](review-261004-1037-r29-source.md) và [Xia source/schema comparison](researcher-261004-1037-hook-schemas-visual-source.md) giữ scope và giới hạn riêng. r26 → r27 → r28 → r29 có source-lock history; `/root` là freeze owner.

- r27 full-suite lỗi discovery shadowing và installer assumptions; promotion Windows sharing/access failure giữ tại [attempt 01](../runs/nckh-writing-hooks-261004-1037-attempt-01/). Holder của transient lock chưa xác định.
- r28 regression chọn sai `agent` thay vì `native-agent`; [failed log](../runs/nckh-writing-hooks-261004-1037-attempt-02/installer-repair-tests.log) còn nguyên. Lượt build r28 được dừng có chủ đích trước sửa/freeze; không gọi interruption là defect builder.
- Lần test trước freeze r29 bị source drift verifier từ chối; [receipt riêng](../runs/{RUN.name}/installer-repair-tests.log) giữ nguyên. [Frozen regression retry](../runs/{RUN.name}/installer-frozen.stderr) và full suite sau đó đạt; không bypass verifier hoặc weaken tests.

Cổng còn mở: cập nhật installation r25; native registration/trust/activation và event deny/malformed/timeout/crash/coverage theo đúng host/version/surface; owner feedback gắn revision/artifact/input hashes; stable/scientific/rights/reviewer/holdout/economics acceptance. Không có grant hoặc evidence cho những bước đó trong delivery này. Ba checkbox native/owner còn unchecked trong plan; technical checkpoint không tự đóng chúng. Không có Git live diff nên conditional simplifier không chạy. Không commit/publish release; AgentWiki publish skipped.
"""
md_path.write_text(md, encoding="utf8")
print(json.dumps({key: summary[key] for key in ("status", "deterministic_tests", "bundles_built_extracted_verified",
    "actual_resource_reads", "writer_disabled_no_read_observations", "hook_projections_exercised", "protected_hashes_unchanged")}))
