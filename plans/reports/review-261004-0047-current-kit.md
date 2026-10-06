# Review read-only current NCKH kit — 2026-10-04

## Scope và kết quả

- Đã đọc `nckh-kit/docs/index.md`, `research-and-writing.md`, `personal-use.md`, source lock, catalog 37 identity/9 resource, sáu source skill (`nckh-write`, `nckh-taste`, `nckh-visuals`, `nckh-brand`, `nckh-content`, `nckh-analytics`), core `resources.py`/`guards.py`/`build.py`, resource/evidence tests, installed skills và `.nckh-state/ownership.json`.
- Chỉ review; không sửa product files, không rebuild/install/provider/native run. File này là output duy nhất được phép ghi.
- Source hiện: lock revision `26`, 243 pins (identity tại `nckh-kit/core/registry/source-lock/source-lock.json:1377-1380`), 37 IDs (`nckh-kit/core/build.py:166-190`; `nckh-kit/core/evaluation.py:72-77`), 9 registry entries (phase evidence tại `plans/261003-0101-nckh-personal-use-sources-and-standards/phase-02-sources.md:31`).
- Installed hiện: 37 thư mục `.agents/skills` + 6 `.codex/agents/*.toml` = 43 items; ownership ghi project/codex và bundle candidate-r25 tại `.nckh-state/ownership.json:53-104`, source-lock hash r25 tại `:67-68`. Không dùng dữ liệu memory r22.

## Findings ưu tiên

### F1 — INTEGRATION DELTA (chưa đủ căn cứ xếp HIGH): source r26 chưa được áp dụng vào installed r25

**Evidence.** Source lock hiện `revision: 26`, `previous_lock_hash: adc642...` tại `nckh-kit/core/registry/source-lock/source-lock.json:1377-1380`; candidate installed vẫn `revision: 25`, digest `adc642...` tại `plans/evaluation/personal-use/candidate-r25-attempt-02/bundles/on/codex/source-lock.json:1377-1380`. Ownership vẫn trỏ candidate r25 (`.nckh-state/ownership.json:53-68,96-104`). So sánh exact keyed `sha256` của `sourceLock.files` với `candidate-r25 bundleLock.files` chỉ cho thấy **bốn** pin thay đổi: `core/profiles/resources/pmc-rights.md`, `core/profiles/resources/wikisource-rights.md`, `core/profiles/resources/worldbank-rights.md` và `core/registry/catalog/resources.json`; các JSONL payload/data bytes được đối chiếu vẫn không đổi. Read-only doctor mới nhất (`plans/reports/checks-261004-0047-installed-doctor.json`) hoàn tất `exit_status: 0`, ghi nhận 43 item `current` (các skill closure `self-contained`, agent TOML `valid-toml`), `candidate_integrity: current` và `visibility_conflicts: []`.

**Impact/owner.** Installed lookup vẫn mang metadata/rights note và registry của r25, nên chưa đại diện cho source r26 nếu yêu cầu “current source + current install” được đưa vào acceptance. Đây là source delta chưa áp dụng, không phải bằng chứng baseline r25 bị hỏng và không tự tạo thành finding HIGH chỉ vì khác revision. Owner: source-lock/build/install handoff và plan closeout. Có thể lập plan từ trạng thái này; việc cập nhật/cài r26 và tạo receipt vẫn chờ implementation authority. Không tự install.

### F2 — HIGH, requested delta: chưa có route tách `humanwrite` và `scientific paperwrite`

**Evidence.** Catalog chỉ có một identity `nckh-write` (`nckh-kit/core/registry/catalog/skills.json:104-115`). Source/installed SKILL vẫn gộp VI/EN, literary translation và English scientific prose trong cùng route (`nckh-kit/skills/core/nckh-write/SKILL.md:24-34`; installed binding đã relocate ở `.agents/skills/nckh-write/SKILL.md:24-34`). Cùng consumer `nckh-write` đang nhận reporting clinical-health (`resources.json:4-25`), language-literary Wikisource (`:166-190`) và scientific PMC (`:270-328`).

**Impact/owner.** Old 37-ID contract chưa biểu diễn mode/route boundary mà user vừa yêu cầu; không được âm thầm xoá `nckh-write` hoặc bất kỳ 37 domain nào. Owner: catalog + source/installed SKILL binding, acceptance profile, eval manifests/runtime matrix; đề xuất additive IDs/modes mới giữ compatibility route cũ và cần approval trước khi đổi catalog.

### F3 — HIGH, requested delta: `nckh-visuals` vẫn cho phép ngoài research-only

**Evidence.** Description và workflow hiện cho phép “slides or illustrative artwork” (`nckh-kit/skills/core/nckh-visuals/SKILL.md:2-3,24-36`; installed tương ứng `.agents/skills/nckh-visuals/SKILL.md:2-3,24-36`). Docs còn tách artwork illustrative khỏi scientific evidence (`nckh-kit/docs/research-and-writing.md:32,46-47`). Reader chỉ khóa resource theo consumer/locale/genre/domain (`nckh-kit/scripts/search-resource.py:206-229`), không phải task-level gate cấm visual ngoài research; build chỉ chọn theo kit (`nckh-kit/core/build.py:166-190`).

**Impact/owner.** Resource lookup không tự leak sai domain, nhưng skill contract vẫn mở cho generic slide/artwork. Owner: `nckh-visuals` scope/routing/evals. Giữ nguyên các domain `brand/content/analytics` và các identity còn lại; chỉ thêm research-only visual gate/negative cases, không cắt domain silently.

### F4 — MEDIUM, actual hook absence/wiring gap

**Evidence.** Adapter Codex ghi `hooks.state=not-installed`, `enforcement=host permissions; no hook guarantee`, `coverage=unverified` (`nckh-kit/adapters/codex/adapter.json:54-57`); các adapter khác cùng contract. Test chỉ xác nhận trạng thái chưa kiểm (`nckh-kit/tests/runtime/test_adapters.py:31-40`), docs cũng nói live discovery và hook enforcement còn unverified (`nckh-kit/docs/installation.md:110-115`). Không tìm thấy hook implementation/registration trong current source closure.

**Impact/owner.** Research-first, rights, human-gate và visual boundary hiện là instruction/reader checks, không phải host-enforced interception. Owner: adapter/installer/host integration evidence; không claim “hook đã chặn” từ static pass. Đây là known unverified gate theo old spec, không phải lý do tự sửa adapter trong review này.

### F5 — MEDIUM, static/resource tests chưa đủ evidence cho route mới hoặc behavior

**Evidence.** `validate_case_manifest` chỉ yêu cầu mỗi identity bốn case và receipt nếu đã chạy (`nckh-kit/core/evaluation.py:14-37`); `validate_cases` vẫn khóa đúng 37 IDs, 224 runtime cells và trả `qualification: pending`, đồng thời đếm `not-run` (`:72-124`). Các case hiện tại chỉ kiểm route cũ: `nckh-write` một route (`evals/cases/research-writing-visuals/nckh-write.json:20-172`), visuals positive là scientific diagram và failure là invented measurements/no native engine (`nckh-visuals.json:20-172`), không có generic-illustration rejection hoặc humanwrite/paperwrite split. Resource tests kiểm provenance/domain/locale/no-match (`tests/resource/test_consumers.py:17-59`, `tests/resource/test_real_sources.py:98-139`); visual guard test chỉ chứng minh hash stale/current (`tests/evidence/test_guards.py:57-66`).

**Impact/owner.** Pass structural/resource không chứng minh model routing, language-vs-paper behavior, hook enforcement, scientific meaning, native editability hay human acceptance. Owner: eval case owners + runtime/native evidence + human/domain reviewers; bổ sung cases/receipts sau khi route delta được duyệt, không regrade old 37 from counts alone.

## Điểm đang được bảo vệ tốt

- `resources.py` khóa consumer/path/format/rights/lineage và explicit dependencies (`nckh-kit/core/resources.py:45-98`); `build.py` chặn unpinned/private/secret closure (`:218-244`).
- Reader fail-closed consumer/locale/genre/domain và trả `no-applicable-record` khi domain lệch (`nckh-kit/scripts/search-resource.py:206-229`); không thấy bằng chứng resource tự động trộn sang marketing/brand/content/analytics.
- Guards và docs phân biệt structural/hash, semantic support, human taste, native visual và scientific gates (`nckh-kit/core/guards.py:1-20,61-69`; `nckh-kit/docs/research-and-writing.md:43-64`).

## Integration owners và next-plan gates

1. Giữ source r26 và installed r25 như hai revisions riêng; lập plan additive scope 37→39 và source/install reconciliation từ baseline này. Chỉ tạo install receipt/cập nhật bản cài sau khi có implementation authority, kèm registry/rights/source-lock hash reconciliation.
2. Duy trì `nckh-write` compatibility; mô hình hóa `humanwrite`/`paperwrite` additive và cập nhật catalog, profile, consumer refs, eval/runtime matrix cùng transaction.
3. Đặt research-only gate cho image/diagram/visual artifact; giữ brand design brief và 37 domain khác ngoài phạm vi visual production thay vì xoá route.
4. Ghi hook status là `unverified` cho tới khi có host observation; không suy diễn từ adapter JSON, static test hoặc install receipt.
5. Không gọi 37/148/19/224 là behavioral/native/scientific acceptance; các số đó chỉ là catalog/case/family/runtime structural coverage khi receipts còn `not-run` và qualification `pending`.

## Unresolved questions

- Revision r26 sẽ trở thành installed baseline qua plan mới hay tiếp tục là source amendment; đây là quyết định trước implementation/install, không phải blocker của việc lập plan.
- User muốn `humanwrite`/`paperwrite` là hai identity mới hay hai mode trong một identity; compatibility kỳ vọng của `nckh-write` cần ghi rõ trước khi cập nhật catalog.
- “Research-only visuals” bao gồm chart/diagram/scientific slides nào, và có loại trừ illustrative artwork hoàn toàn hay chỉ cấm khi không có research objective/evidence?

Status: DONE_WITH_CONCERNS
Summary: Đã hoàn tất review read-only, xác nhận source r26/installed r25 là một source delta chưa áp dụng, thiếu hook enforcement, và các route visuals/write chưa đáp ứng delta mới. Không sửa code, không rebuild/install/provider run.
Concerns/Blockers: Plan được phép lập từ trạng thái hiện tại; route shape và source-r26 installation vẫn là các gate trước implementation/install, không phải blocker của việc lập plan.
