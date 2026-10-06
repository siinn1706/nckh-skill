# Validation và completion audit — NCKH review/plan

Ngày: 04/10/2026, Asia/Saigon. **Snapshot lịch sử trước approval A1–A9**; các con số và blocker bên dưới giữ theo thời điểm kiểm. User đã duyệt “duyệt 9 điều chỉnh” và “duyệt tất cả điều chỉnh”; trạng thái hiện tại được supersede bởi [hồ sơ sau approval](./validation-261004-1002-approved-plan-amendments.md), không dùng gate cũ để hỏi duyệt lại. Phạm vi vẫn review/plan, không implementation.

## Những gì đã kiểm

| Kiểm tra | Kết quả quan sát | Giới hạn |
|---|---|---|
| Source baseline và đối soát cuối | r26; 243/243 pinned paths khớp, không mismatch | Integrity, không scientific validity |
| Catalog/resources | 37 identities, 9 packs; hash payload của cả 9 khớp baseline | Không phải 37 skill đã behavioral-qualified |
| Source lock raw file | SHA-256 `11ac90b7e9ec865bda3a346c7ceea1c4ca762a354518a297eb4d88ea5ce1806f`, không đổi | Không lẫn raw file hash với canonical digest của validator |
| Ownership file | SHA-256 `4751266952d2c7fd6bd406900f51437a5c3cfc9895038933ff7b66f672f8b3c8`, không đổi | Không cài/sửa bundle |
| Installed doctor cuối | Exit 0, read-only; 43/43 items current, candidate integrity current, visibility conflicts rỗng | Hook enforcement/native freshness vẫn unverified |
| Existing source structural eval | `python -B evals/run-evals.py --validate-only` exit 0: 37 identities, 148 cases, 19 families, 224 native cells, 243 pins | Không chạy 148 model cases hoặc 224 native cells; qualification pending |
| Plan validate/parse ban đầu | Exit 0; 4 phase; 41 tasks, 0 done, 0%; pending/todo | Snapshot trước user bổ sung language options; chỉ cấu trúc |
| Existing owner path scan | 63 absolute path mentions trong phần Existing, 0 missing | Kiểm tồn tại, không proof toàn bộ caller closure |
| Journal | Validate bằng filename stem exit 0, ngày 2026-10-04 | Local historical record; AgentWiki publish skipped |
| Independent review | 3 reports; 15 raw findings, 12 nhóm sau gộp; 9 proposed Accept, 3 Reject | Không user approval, chưa áp dụng amendment |

Receipts: [source baseline](./checks-261004-0047-source-baseline.json), [source structure](./checks-261004-0047-source-structure.json), final doctor (historical evidence path: `./checks-261004-0047-installed-doctor-final.json`; unavailable in the cleaned checkout), [plan structure](./checks-261004-0047-plan-structure.json), [adjudication](./red-team-261004-0047-adjudication.md).

## Phân lớp evidence

Source r26 so với installed r25 là delta chưa cài: chỉ ba rights note và registry resource đổi pin, không JSONL payload. Doctor pass không tự cấp quyền update. Số native 224 thuộc plan/cook/xia, không phủ mọi identity. Hash/lookup/parse/packaging không chứng minh prose hay hơn, hook chặn side effect, nội dung khoa học đúng hay tác giả đã chấp nhận.

Tài liệu official host đã được đối chiếu trong [native capability report](./researcher-261004-0047-native-hook-capabilities.md); đó là documentation evidence, chưa phải native enforcement. Hai nguồn ClaudeKit bị loại khỏi copy vì LICENSE hạn chế/xung đột package metadata; kế hoạch dùng public host schemas để tự triển khai. Không chạy upstream scripts.

## Completion audit theo yêu cầu gốc

| Yêu cầu | Bằng chứng | Trạng thái |
|---|---|---|
| Review bộ skill hiện tại/data/hook | Current-kit report, source/doctor receipts, 9-pack source map, adapter states | Hoàn tất review |
| Tham khảo resources chọn lọc | 7 archive, writing/hook reports, selected hashes/license/consumer mapping | Hoàn tất nghiên cứu có giới hạn; archive commit unknown được giữ rõ |
| Brainstorm hướng humanwrite/paperwrite | Brainstorm contract, compatibility option, writer phase và language decision mới | User giao quyền lựa chọn; đã chọn 2 writer + --en/--vi, target 39; chưa implementation |
| Giữ hình/biểu đồ cho NCKH | P2 và negative direct/indirect scenarios | Draft có scope; cần A8/A9 để không cắt computational research hay hứa quá coverage |
| Tạo plan bằng ak-plan | 4 phase + source-adoption map, scaffold/parse/validate, 41 tasks pending | Draft đã có; chưa hoàn tất refinement gate |
| Review độc lập, resolve trước handoff implementation | 3 reviewer và adjudication A1–A9 | Cần user duyệt áp dụng amendment; không ready-to-cook |
| Giữ phạm vi plan-only | 243 hashes + ownership unchanged, final doctor; edits chỉ plan/reports/journal và rebuildable local index | Đạt; không build/install/trust/provider/native/model/publish |

Không đánh dấu native goal complete: chín amendment còn phải được duyệt và áp dụng rồi rà lại toàn plan. Đây là lần đầu giao gate này cho user; không đặt blocked/paused tùy ý và không coi automated goal continuation là approval.

## Recovery, process và index

- Doctor lần đầu trong phần trước của lượt bị parse khi tiến trình chưa terminal; đã đối soát/rerun thành công. Doctor cuối session 48860 hoàn tất exit 0; không còn process do task cần giữ lại. Reconcile CIM chỉ thấy tiến trình đọc hiện hành.
- Journal validate bằng relative path trả exit 1 không output; đổi sang filename stem đúng CLI, exit 0. Không giấu lần lỗi.
- Root không phải Git repository nên không có diff Git để khẳng định toàn workspace unchanged. Bằng chứng giới hạn ở 243 pinned source files và installed/ownership, cùng ownership scope của các delegate.
- Plan files là authority. Local AgentKit state ở `plans/.agentkit-state`, đã có backup DB trước tạo plan. Reindex chỉ cập nhật projection, không sửa/xóa plan lịch sử hoặc cấu hình toàn cục; UTC scaffolding row cũ có thể còn trong lịch sử, không xóa ngầm.

## Bước tiếp ở snapshot trước approval (đã được thay thế)

Xin duyệt A1–A9 **chỉ để chỉnh hoàn thiện plan**. Quyết định hai writer có --en/--vi đã được chọn theo quyền user giao và cập nhật trong P1/P4/source map, không cần hỏi lại. Sau duyệt amendment: áp dụng đồng bộ, whole-plan sweep, validate/parse/reindex và completion audit lại. Implementation, hook apply/trust, native/model runs và release là quyền riêng, chưa được cấp.

## Kiểm lại sau language decision

Plan validate/parse đều exit 0: 4 phase, **43 tasks, 0 done**, pending/todo. Index 57 dòng; phase lengths 57/53/56/59. Kiểm 21 relative links trong plan và các report/journal liên quan không thấy link hỏng (trước thêm link receipt bên dưới). Đối soát lại 243 source pins: 0 mismatch; raw lock và ownership hash không đổi. P2/P3 hashes giữ nguyên bản reviewer đọc; P1/P4/source map/index chỉ đổi theo language decision được user giao quyền chọn, không áp dụng A1–A9.

Local `ak plan reindex --apply` exit 0, nhận diện đúng plan mới với 4 phase; chỉ thay rebuildable index. Journal validation exit 0. [Final structural/integrity receipt](./checks-261004-0047-plan-final.json) lưu hash plan cùng output parse/validate. Những kết quả này không đóng amendment approval, implementation hoặc quality gates.
