# Áp dụng và kiểm tra chín amendment đã duyệt

Ngày 04/10/2026, Asia/Saigon. Phạm vi: hoàn thiện review và implementation plan; không triển khai bộ skill. Đây là record hiện hành, supersede approval blocker trong [validation trước đó](./validation-261004-0047-research-data-hooks-writing.md), không sửa lại bằng chứng lịch sử.

## Approval và phạm vi

User xác nhận “duyệt 9 điều chỉnh”, sau đó “duyệt tất cả điều chỉnh”. Cả A1–A9 của [adjudication](./red-team-261004-0047-adjudication.md) đã được đưa vào index, bốn phase và source-adoption map của [cùng kế hoạch](../261004-0047-nckh-research-data-hooks-writing/plan.md). Ba nhóm Reject giữ nguyên vì review không bổ sung bằng chứng để đảo quyết định.

Giữ hai identity `nckh-humanwrite`, `nckh-paperwrite` với `--en`/`--vi`, compatibility router `nckh-write` và critic `nckh-taste`. Target 39 không phải số skill hiện đã cài. Approval này không cấp quyền cook, source edit/freeze, build/install, hook apply/trust, native/model/provider evaluation hoặc publish.

## Amendment coverage

| ID | Đã áp dụng vào contract của plan | Bằng chứng đối chiếu |
|---|---|---|
| A1 | Baseline full-check trước edit; focused suites không phụ thuộc global lock ở P1–P3; full evaluation/build sau single-owner freeze P4 | `core/build.py::verify_source_lock`, `core/evaluation.py::validate_cases`, acceptance/resource/evidence/runtime test call paths |
| A2 | Exact baseline 37 ∪ hai IDs; đúng 156 base cases, 19 families; schema/acceptance/build/eval/tests cùng chuyển, history 37/148/224 giữ nguyên | `core/acceptance.py`, `core/contracts/catalog.schema.json`, `tests/release/test_qualification.py`, `scripts/compare-matched.py` |
| A3 | Bounded hook source inventory, manifest v2, per-host closure và inactive plugin projection; extracted checker/runner tests | `core/build.py::SOURCE_AREAS`, `_materialize_host`, `verify_bundle`, `installer/schemas/bundle-v2.schema.json` |
| A4 | Dedicated config module/CLI; exact project targets, owned definitions/hash/lock/compare, no-write conflict, preserve edits và partial rollback | Existing installer chỉ quản lý skill/agent paths; target paths từ official capability report và Claude/Cursor docs |
| A5 | Persistent on/off/plugin builds; explicit archive/extract/outside-CWD/receipt paths; installer nhận đúng `--package` | `scripts/build-artifacts.py`, `scripts/resource-smoke.py`, `installer/nckh-installer.py` parser/data flow |
| A6 | Additive mapping Nature/Wikisource/PMC→humanwrite, PMC/Nature/scoped reporting→paperwrite; publisher visuals-owned | `core/registry/catalog/resources.json` current consumers/locale/domain/genre; `scripts/search-resource.py` |
| A7 | Direct linked Markdown Humanizer, context/counterexample/protected fields + edit diff/factual delta; mandatory matrix/schema/validator/tests | Existing evaluator nhận base manifests theo catalog; new matrix được nối vào `validate_cases`, không orphan flags |
| A8 | Measured và actual computed/derived/simulation outputs đều hợp lệ khi đúng scientific purpose/provenance/uncertainty/label | Current visual policy cấm giả measured results, không cấm toàn bộ computational research; không thêm simulation pipeline |
| A9 | Inventory actual instruction/binding routes; controlled synchronous preflight và per-event/version native failure tests; uncovered manual/not-callable | `nckh-visuals` + native-documents contract; checker chỉ đọc receipts; indirect skill/provider contracts và official hook coverage limits |

Writer supplemental matrix có 256 native planned cells và 20 scenario IDs riêng; không cộng vào 156 base IDs hoặc 224 historical cells và không tự cấp quyền chạy các cell. Các file/module/test mới đều được ghi là tương lai, không có assertion chúng đã tồn tại.

## Kiểm tra thực hiện trong lượt sửa plan

| Check | Quan sát | Giới hạn |
|---|---|---|
| `ak plan validate` | `valid: true`, exit 0 | Chỉ cấu trúc Markdown/frontmatter |
| `ak plan parse` | 4 phases, 45 tasks, 0 done; pending/todo | Không coi task triển khai đã xong |
| Existing file-owner scan | 80 absolute mentions, 57 distinct existing paths, 0 missing | Chỉ phần Existing/reuse; new paths là planned artifacts |
| Count-consumer search | Candidate consumers ở build/evaluation/acceptance/catalog schema/profile/release tests; historical comparator giữ riêng | Không search-replace 37/148 trong lịch sử |
| Source pin reconciliation sau sửa | 243/243 khớp baseline, 0 mismatch | Không phải scientific/behavioral acceptance |
| Raw source-lock hash | `11ac90b7e9ec865bda3a346c7ceea1c4ca762a354518a297eb4d88ea5ce1806f`, không đổi | Source vẫn r26, không freeze |
| Installed ownership hash | `4751266952d2c7fd6bd406900f51437a5c3cfc9895038933ff7b66f672f8b3c8`, không đổi | Không rerun hoặc suy thêm từ historical doctor |
| Process reconciliation | CIM ban đầu bị sandbox từ chối; approved read-only retry không thấy Python/Node/Java/.NET process khớp workspace | Không dừng process của người dùng; không mở tiến trình nền mới |

Index 58 dòng; phase lengths 70/67/90/71, source map 52. Rà sau sửa phát hiện local schema engine không hỗ trợ `maxItems`: contract dùng `minItems`/enum được hỗ trợ và exact length/set/duplicate checks trong owning validators, không thêm keyword lỗi. Rollback owner được tách skill installer và hook-config transaction; public event log không lẫn private config-path journal.

## Whole-Plan Consistency Sweep

Đã đọc lại index, cả bốn phase và source map. Chín decision deltas đồng bộ owners/tasks/validation/exit/rollback; không còn current gate xin duyệt A1–A9, measurement-only prohibition, 156+ target hoặc CLI matrix flag được đề xuất nhưng thiếu owner. Các câu pending trong review/audit cũ giữ lại dưới nhãn snapshot lịch sử; pending implementation/native/rights/human là intentional, không phải unresolved planning decision.

Relative-link/anchor pass, CLI checks, local-index backup/reindex và journal validation được ghi tại checkpoint cuối bên dưới. Không dùng parser/hash pass làm proof language quality, hook enforcement hay scientific validity.

## Checkpoint cuối

- 10 Markdown files được kiểm, 33 local links và 1 heading anchor hợp lệ, 0 broken links. Bao gồm sáu file plan, adjudication, hai validation records và journal.
- Final `ak plan validate` hợp lệ; `ak plan parse` ghi 4 phase với 13/9/11/12 tasks = 45, tất cả 0 done. `ak journal validate` bằng filename stem trả `ok: true`, exit 0.
- Đã preview reindex rồi sao lưu DB vào `plans/.agentkit-state/plans/plans.db.before-261004-1002-approved-plan-amendments.bak`; hash backup khớp DB trước sửa: `aca4600f591a7f3cf9cdc58aa0663dfc9dca55b040fee3011ec7c3e9e6458e4d`. Không có WAL tại lúc copy. Reindex `--apply` exit 0, nhận đúng plan `test-skill/261004-0047` với 4 phase; không xóa các plan/historical rows khác.
- Chỉ dùng process-local `AGENTKIT_HOME` dưới `plans/.agentkit-state`. Source 243 pins/raw lock và installed ownership giữ nguyên; không source/install/global-config mutation. Đây là phạm vi integrity có bằng chứng, không khẳng định toàn workspace sạch khi root không có Git.
- Whole-plan sweep không còn unresolved contradiction của A1–A9. Các file tương lai và native/human/rights gates được ghi là pending, không giả kết quả runtime.

Plan files vẫn là authority; local index chỉ là projection có thể dựng lại. Yêu cầu mở plan trong pane trả `queued`, không báo đã hiển thị nếu app chưa xác nhận.

## Completion boundary

Review hiện trạng và bounded upstream comparison đã có report; chín amendment được duyệt đã có đủ execution contract trong plan và checkpoint cuối đã qua. **Outcome review+plan hoàn tất.** Các việc triển khai/native/human/scientific là công việc tương lai theo plan pending, không phải lý do để tự triển khai hoặc giữ goal review+plan mở vô hạn.

AgentWiki publish skipped; journal chỉ là work history.
