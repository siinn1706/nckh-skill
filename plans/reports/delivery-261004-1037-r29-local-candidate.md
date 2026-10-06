# NCKH r29 — bàn giao candidate cục bộ

Status: **local technical checkpoint PASS; native/owner/scientific gates pending**.

Thực thi theo `/goal ak-cook --auto` cho [kế hoạch](../261004-0047-nckh-research-data-hooks-writing/plan.md).
Source r29 có **281 pins**, canonical source-lock hash `6fbdf13a4ba296b3e492b89beaf7fc8299c926d73a02a0ffcd9ea16a88d16248`.
[Structured receipt](delivery-261004-1037-r29-local-candidate.json) bind các receipt thực và 16 archive hashes.

## Kết quả triển khai

- `nckh-humanwrite` và `nckh-paperwrite` dùng `--en`/`--vi`, chung preservation/language contract; `nckh-write` giữ route tương thích theo action. Humanizer là policy Markdown re-authored/attributed; LanguageTool còn deferred, optional English diagnostic.
- Scientific visuals có research-purpose, origin labels và source/code/transform/output/run bindings. Diagnostic phép tính thực đọc transform JSON. Purpose/hash không xác thực scientific truth hoặc một receipt bịa nhưng tự nhất quán; native engine/render/editability vẫn có gate riêng.
- Neutral hook policy, bốn codecs, runner/manual checker và config preview/apply/remove/recover đã có bounded tests và portable closure. Apply là transaction riêng, cần preview hash, grant và native evidence đúng host/version/surface. Templates và plugin reference projection giữ inactive.
- Catalog/profile/build/evaluation đúng **39 identities = 37 cũ + 2 writers**, **156 base cases**, **19 families**, **9 resources**. Giữ 148 old case IDs, historical 224 matrix và comparator/receipts. Bốn visual prompt bytes đã đổi; không regrade bằng receipt cũ.

## Evidence thực đã hoàn tất

| Checkpoint | Kết quả | Receipt |
|---|---|---|
| Full deterministic | 181 tests, `OK (skipped=1)`, 806.511 giây; một real-symlink fixture bị giới hạn quyền Windows | [result](../runs/nckh-writing-hooks-261004-1037-attempt-03/deterministic.json), [owned process cleanup](../runs/nckh-writing-hooks-261004-1037-attempt-03/deterministic-frozen.process.json) |
| Reproducibility/build | 4 variants × 4 hosts; đủ 16 persistent bundles | [build context](../runs/nckh-writing-hooks-261004-1037-attempt-03/delivery-context.json) |
| Actual archive/extract | 16 ZIP được Compress-Archive/Expand-Archive ra ngoài repository; extraction manifest/closure và archive chain khớp build | [archive receipt](../runs/nckh-writing-hooks-261004-1037-attempt-03/archive-summary.json) |
| Extracted resource reads | 216 actual observations: 27 consumer/resource pairs × 8 resource-on bundles; source/license/lineage hashes được đọc | [smoke receipt](../runs/nckh-writing-hooks-261004-1037-attempt-03/smoke-summary.json) |
| Disabled writers | 48 direct packaged-reader observations trên resource-off trả disabled, no-read, empty records | [per-bundle receipts](../runs/nckh-writing-hooks-261004-1037-attempt-03/receipts/) |
| Hook relocation | 24 primary/reference projections gọi runner, manual block và config preview từ outside CWD; disposable projects giữ nguyên bytes | [smoke receipt](../runs/nckh-writing-hooks-261004-1037-attempt-03/smoke-summary.json) |
| Installer preview | 8 surfaces, mỗi preview 39 skills + 6 native-agent proposals, không conflict và không viết project | [preview receipt](../runs/nckh-writing-hooks-261004-1037-attempt-03/installer-previews.json) |
| Preservation/legacy | 509 protected hashes không đổi; installed r25 chưa cập nhật; 4 existing schema-v1 bundles đọc được bằng verifier mới | [final preservation](../runs/nckh-writing-hooks-261004-1037-attempt-03/final-preservation.json) |

[Independent writer forward test](reviewer-261004-1037-writer-forward-test.md) có bốn actual local agent trials: VI minimal polish, EN Methods outline, conflicting flags và ambiguous locale. Đây không phải native invocation, human taste hoặc scientific acceptance. Supplemental writer matrix **256 planned native cells / 20 scenarios** đã validate; observed behavior vẫn unverified, tách khỏi historical 224 cells.

## Gói để xem và dùng sau grant phù hợp

Resource-access ON giữ contract sử dụng/phân phối công khai; OFF chỉ là đối chứng nội bộ. Các archive dưới đây chưa được publish hoặc cài vào installation hiện có.

- [Claude standalone resource-on](../runs/nckh-writing-hooks-261004-1037-attempt-03/archives/on-standalone-claude.zip)
- [Codex standalone resource-on](../runs/nckh-writing-hooks-261004-1037-attempt-03/archives/on-standalone-codex.zip)
- [Cursor standalone resource-on](../runs/nckh-writing-hooks-261004-1037-attempt-03/archives/on-standalone-cursor.zip)
- [Antigravity standalone resource-on](../runs/nckh-writing-hooks-261004-1037-attempt-03/archives/on-standalone-agy.zip)
- [Đủ 16 archives, gồm inactive plugin projection](../runs/nckh-writing-hooks-261004-1037-attempt-03/archives/)

Manifest file counts, không tính `manifest.json`:

| Host | ON standalone | OFF standalone | ON plugin | OFF plugin |
|---|---:|---:|---:|---:|
| claude | 588 | 522 | 1169 | 1037 |
| codex | 588 | 522 | 1163 | 1031 |
| cursor | 587 | 521 | 1167 | 1035 |
| agy | 587 | 521 | 1167 | 1035 |

Hook closure có 26 members cho Claude/Codex, 25 cho Cursor/AGY. Packaging không đăng ký, enable hoặc trust hook. Setup/lifecycle commands do [installation docs](../../nckh-kit/docs/installation.md) sở hữu.

## Failures, review và cổng còn mở

[Review trước freeze](review-261004-1037-pre-freeze.md), [review r29 delta](review-261004-1037-r29-source.md) và [Xia source/schema comparison](researcher-261004-1037-hook-schemas-visual-source.md) giữ scope và giới hạn riêng. r26 → r27 → r28 → r29 có source-lock history; `/root` là freeze owner.

- r27 full-suite lỗi discovery shadowing và installer assumptions; promotion Windows sharing/access failure giữ tại [attempt 01](../runs/nckh-writing-hooks-261004-1037-attempt-01/). Holder của transient lock chưa xác định.
- r28 regression chọn sai `agent` thay vì `native-agent`; failed log (historical evidence path: `../runs/nckh-writing-hooks-261004-1037-attempt-02/installer-repair-tests.log`; unavailable in the cleaned checkout) còn nguyên. Lượt build r28 được dừng có chủ đích trước sửa/freeze; không gọi interruption là defect builder.
- Lần test trước freeze r29 bị source drift verifier từ chối; receipt riêng (historical evidence path: `../runs/nckh-writing-hooks-261004-1037-attempt-03/installer-repair-tests.log`; unavailable in the cleaned checkout) giữ nguyên. Frozen regression retry (historical evidence path: `../runs/nckh-writing-hooks-261004-1037-attempt-03/installer-frozen.stderr`; unavailable in the cleaned checkout) và full suite sau đó đạt; không bypass verifier hoặc weaken tests.

Cổng còn mở: cập nhật installation r25; native registration/trust/activation và event deny/malformed/timeout/crash/coverage theo đúng host/version/surface; owner feedback gắn revision/artifact/input hashes; stable/scientific/rights/reviewer/holdout/economics acceptance. Không có grant hoặc evidence cho những bước đó trong delivery này. Ba checkbox native/owner còn unchecked trong plan; technical checkpoint không tự đóng chúng. Không có Git live diff nên conditional simplifier không chạy. Không commit/publish release; AgentWiki publish skipped.
