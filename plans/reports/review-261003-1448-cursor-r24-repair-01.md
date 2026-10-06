# Review delta Cursor r24 repair round 1: Django và UCI

Ngày: 2026-10-03, Asia/Saigon. Mode: review-only. Phạm vi: hai memo và hai receipt trong `native/cursor-grok-r24-repair-01`; chủ dự án đã tự gửi prompt sửa trong Cursor. Báo cáo này kiểm tra snapshot lưu trên đĩa.

## Kết quả

| Case | Sửa đổi được yêu cầu | Facts/nguồn | Output contract trong snapshot |
|---|---|---|---|
| Django | Bỏ nhánh sửa message như một repair đầy đủ; chỉ rõ assertion đúng | pass | pass |
| UCI | Có bảng target hai dòng `no=10`, `yes=0`, mẫu số 10 | pass | pass |

Hai finding về memo trong review trước (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/reports/review-261003-1423-cursor-r24-outputs.md`; unavailable in the cleaned checkout) đã được khắc phục tại hash mới bên dưới. Không phát hiện factual regression trong delta. Kết luận này không sửa fixture Django, không xác nhận một lần chạy test hay reader mới, không chấm thay chủ dự án và không đóng gate World Bank.

## Phạm vi kiểm tra

- Đọc toàn bộ hai memo sửa và diff với hai bản gốc được giữ trong `native/cursor-grok-r24/`.
- Đối chiếu case manifest (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/cases/real-source-cases.json`; unavailable in the cleaned checkout), hai receipt mới và record đúng `source_id` trong hai pack đang cài.
- Tính SHA-256 của file đầu vào và canonical record hash bằng `json.dumps(content, sort_keys=True, ensure_ascii=False, separators=(',', ':'))`; so record content với installed pack. Đọc lại comparator Django trong receipt và đếm lại bảng UCI cục bộ.
- Dùng lại kết quả xác minh raw fixture/archive, license và phạm vi nguồn từ review trước: source record, pack/reader và artifact gốc có hash trùng. Không giải nén lại archive, không làm lại source/package/install qualification.
- Không chạy Django/test suite, reader, model/provider, UI hoặc external write. Chỉ tạo báo cáo này; giữ nguyên memo, receipt, raw source và báo cáo cũ.

## Django: finding sửa theo comparator đúng

Artifact: memo Django sửa (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/cursor-grok-r24-repair-01/real-source-django-code-review-01.md`; unavailable in the cleaned checkout).

| Observable | Kết quả | Vị trí/evidence |
|---|---|---|
| Corrective assertion chỉ rõ `index_drop_table` | pass | Dòng 58 và 64: `self.assertGreater(index_tx_end, index_drop_table)`. |
| Không còn coi message-only change là repair đầy đủ | pass | Dòng 58 và 64 nói rõ thay message không thêm comparator và giữ failure path. |
| Finding giữ location, impact và why/repro có căn cứ | pass | Dòng 43–58; source comparator trong fixture dòng 501–503. |
| Không nâng static reasoning thành runtime result | pass trong nội dung memo | Dòng 3, 34 và 56 giữ trạng thái chưa chạy; đây không phải audit side effects của phiên Cursor. |
| Commit, fixture hashes, BSD scope và giới hạn review giữ nguyên | pass | Dòng 18–30, 60 và 68; receipt/record khớp bản trước. |

Fixture test nguồn (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/source-acquisition/raw/swe-django-02cd16-test_commands.py:502`; unavailable in the cleaned checkout) so `index_tx_end` với `index_op_desc_unique_together`; `index_drop_table` được lấy ở dòng 480 và chỉ buộc đứng sau author ở dòng 497–500. Các dòng tương ứng đọc lại trong receipt có cùng bytes/hash với nguồn đã được review trước.

Chuỗi thứ tự ở memo dòng 56, `tx_start < unique_together < tx_end < tribble < author < drop_table`, thỏa các comparator hiện có nhưng không thỏa `tx_end > drop_table`. Memo đã nêu đúng đây là suy luận từ thứ tự/comparator. Đề nghị đổi đối số thứ hai thành `index_drop_table` khắc phục đúng lỗ hổng assertion đã nêu. Finding gốc vẫn có căn cứ; phần hướng sửa đã được sửa.

Delta còn lại chỉ thêm nhãn repair round, chuyển receipt path sang thư mục mới và làm rõ không có chứng nhận model. Ghi chú instance reuse tiếp tục `unverified`, không bị biến thành defect đã xác nhận. Nội dung private issue/task/patch không xuất hiện trong hai artifact/receipt được kiểm tra.

## UCI: bảng target đầy đủ, dữ liệu và giới hạn giữ nguyên

Artifact: memo UCI sửa (historical evidence path: `C:/Users/USER/Downloads/test-skill/plans/evaluation/personal-use/native/cursor-grok-r24-repair-01/real-source-uci-analytics-01.md`; unavailable in the cleaned checkout).

| Observable | Kết quả | Vị trí/evidence |
|---|---|---|
| Bảng target có cả `no` và `yes` | pass | Dòng 47–50: `no | 10 | 10`, `yes | 0 | 10`. |
| Mẫu số là mười dòng đầu, không population response rate | pass | Dòng 31–34, 45 và 83. Zero của `yes` là đếm nhãn vắng mặt, không phải null bị thay thế. |
| 10 rows, 17 columns, delimiter `;`, DOI và locator giữ đúng | pass | Dòng 7–9, 20–21 và 43. |
| Month counts, balance âm và các ô dữ liệu giữ đúng | pass | Dòng 52–67; từng dòng của bảng mười quan sát khớp giá trị string trong receipt/pack. |
| Descriptive/causal, bounded sample và duration leakage giữ đúng | pass | Dòng 73–85; không thêm inference/forecast/causal lift. |
| Raw archive/derived hashes và attribution giữ nguyên | pass | Dòng 15–26; không có thay đổi trong diff. |

Đếm lại trên record đã cài: `no=10`, `yes=0`; `may=5`, `apr=2`, `feb=1`, `jun=1`, `oct=1`. Balance theo thứ tự dòng là `1787, 4789, 1350, 1476, 0, 747, 307, 147, 221, -88`. Bảng mười quan sát không đổi so với artifact gốc; cả mười dòng và các cột case yêu cầu đều khớp receipt. Sentinel `pdays=-1`, `poutcome=unknown`, zero và balance âm được giữ.

Hợp đồng marketing provider đang cài (historical evidence path: `C:/Users/USER/Downloads/test-skill/.agents/skills/nckh-analytics/references/_shared/extensions/providers/marketing/contract.json`; unavailable in the cleaned checkout) vẫn có `status=unavailable`, `engine_binding=null`, đúng nội dung memo dòng 39. Nhận xét này chỉ xác nhận file contract hiện tại, không xác nhận hành vi provider của phiên Cursor.

## Receipt và nguồn

Hai receipt đều có schema 2, `status=matched`, `resource_read=true`, đúng consumer/query/domain/locale/genre và một record. Canonical record hash tính lại khớp field `record_sha256`; content khớp record chọn đúng `source_id` trong installed resource. Hai reader đang cài có cùng SHA-256 `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb`.

| Case | Resource SHA-256 | Canonical record SHA-256 |
|---|---|---|
| Django | `e81048922d196fd302555f192d289d51d82449b0ae724fc05cb2e2b4bfeb90cf` | `3600a5e446a811f585fe3bc7c044cf7305db5815e2a9ff04ec1168ee52b318a8` |
| UCI | `647a774b9fb4545d6bc652114910df53677fbe993a00c268c16d4f50b03fe123` | `d85b74d70eacd63a194a0188527a233d5dd65b77a6a12b4a9c3defba04d6eaf6` |

Receipt Django mới có hash `705d2b978dd7e58539e6dec380dca9d73e534ca4d390d6b4c5dfc2ba419e548a`; receipt UCI mới có hash `b0100b18d4d3ffd96e4458bbea9a5b3a7daaabec88824ac518146f86116ef1e6`. Cả hai **trùng bytes/hash với receipt gốc**. Reader tạo receipt nội dung xác định nên hash trùng không mâu thuẫn với việc chạy lại, nhưng file này không có timestamp/process trace để tự chứng minh chữ “Fresh receipt” trong memo. Không có trace thực thi mới được giao cho review này; chỉ ghi content/lineage pass. `human_acceptance=not-evaluated` vẫn được giữ.

## Snapshot hash trước/sau review

Các hash trong bảng được ghi lúc nhận snapshot và kiểm tra lại sau khi lưu báo cáo. Không có thay đổi ở bất kỳ đầu vào nào trong bảng. Đường dẫn rút gọn trong bảng tương đối với project root `C:/Users/USER/Downloads/test-skill`; đây là binding snapshot, không phải script/package qualification.

| File | SHA-256 trước = sau |
|---|---|
| `plans/reports/review-261003-1423-cursor-r24-outputs.md` | `f8778b6b57ae228662f37d039bde7578626728f242861b0c3430829d7a358bdd` |
| `plans/evaluation/personal-use/native/cases/real-source-cases.json` | `d4b926e855cbf8203d8f434db3fa6a427eb71fbd02a07d274fe5ef485cfeb875` |
| `plans/evaluation/personal-use/native/cursor-grok-r24/real-source-django-code-review-01.md` | `f11d5980067173426c88e1d2f15efc8f5fae91e59ec8b7071a475ddd567cda5a` |
| `plans/evaluation/personal-use/native/cursor-grok-r24/real-source-uci-analytics-01.md` | `e80e562268652416ab00571643672c68c53b8416f069b680f7e58acdfd00925b` |
| `plans/evaluation/personal-use/native/cursor-grok-r24-repair-01/real-source-django-code-review-01.md` | `1f0d84edbac230f90324ada124e94db7771219e0d4eb1c17405b5e471e74f850` |
| `plans/evaluation/personal-use/native/cursor-grok-r24-repair-01/real-source-uci-analytics-01.md` | `0348de5270369480371b5d4a5cd5a8b315e525b2c3d657685bb8b922414288d8` |
| Hai Django receipt, trong `cursor-grok-r24/reader-receipts/` và `cursor-grok-r24-repair-01/reader-receipts/`, tên `nckh-code-review__R-django-sqlmigrate-fixtures__django__django-10087.json` | `705d2b978dd7e58539e6dec380dca9d73e534ca4d390d6b4c5dfc2ba419e548a` |
| Hai UCI receipt, trong hai thư mục receipt trên, tên `nckh-analytics__R-uci-bank-marketing__uci-bank-marketing-bank-csv-first-10.json` | `b0100b18d4d3ffd96e4458bbea9a5b3a7daaabec88824ac518146f86116ef1e6` |
| `.agents/skills/nckh-code-review/references/_shared/core/profiles/resources/swe-bench-reference.jsonl` | `e81048922d196fd302555f192d289d51d82449b0ae724fc05cb2e2b4bfeb90cf` |
| `.agents/skills/nckh-analytics/references/_shared/core/profiles/resources/uci-bank-marketing.jsonl` | `647a774b9fb4545d6bc652114910df53677fbe993a00c268c16d4f50b03fe123` |
| `.agents/skills/nckh-code-review/references/_shared/scripts/search-resource.py` | `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb` |
| `.agents/skills/nckh-analytics/references/_shared/scripts/search-resource.py` | `e8eb4cb75cc3220f41f85502cd40fa93fd7e258f6629b0e2588367c1165fdffb` |
| `.agents/skills/nckh-analytics/references/_shared/extensions/providers/marketing/contract.json` | `929d27548f56ccab238087e14de4e9fbae8c54befadc087af031985e3165854f` |

## Gate matrix và bàn giao

| Gate | Trạng thái | Evidence/giới hạn |
|---|---|---|
| Hai repair-direction/output defects trong memo | pass | Assertion Django và bảng target UCI tại hash mới. |
| Factual preservation/source identity/content integrity | pass | Diff, canonical hashes, installed pack/reader hashes và values khớp. |
| Review-only nội dung artifact | pass | Không patch/code-change/merge/publish/runtime guarantee trong memo. |
| Reader execution mới trong phiên sửa | unverified | Receipt contents pass; không có trace/process receipt mới trong input review. |
| Native UI, effective model/effort, cost, session side effects | unverified | Không được kiểm tra trong nhiệm vụ này; label yêu cầu là Cursor Grok 4.7 Extra High, không fallback. |
| Owner acceptance | pending-personal-review | Chủ dự án tự chấm artifact theo hash sau khi dùng. |
| World Bank visual delivery | ngoài phạm vi review này | Báo cáo này không tạo SVG hay đóng gate visual còn thiếu ở review gốc. |

Controller có thể bàn giao hai memo sửa dưới kết quả kiểm tra artifact pass, cùng hash mới và giới hạn trên. Giữ bản gốc/báo cáo cũ như lịch sử lỗi; không sửa nguồn để xóa finding. Không thêm external reviewer/holdout prerequisite cho personal-use lane.

Status: DONE

Summary: Hai sửa đổi Cursor đều đạt scoped artifact acceptance: Django nêu comparator sửa đúng và loại message-only repair; UCI có bảng target đủ hai nhãn, giữ dữ liệu, lineage và giới hạn mẫu.

Concerns/Blockers: Không còn blocker cho hai artifact delta. Fresh reader execution, native UI/effective model và owner acceptance không được xác nhận từ snapshot này.
