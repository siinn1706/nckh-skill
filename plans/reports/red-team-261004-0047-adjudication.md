# Phân xử review plan NCKH — 04/10/2026

## Kết luận và trạng thái phê duyệt

Đã đọc cả sáu file plan và ba báo cáo độc lập. Có 15 finding gốc; sau gộp ba cặp trùng còn 12 nhóm: **9 Accept (5 High, 4 Medium) đã được người dùng duyệt và áp dụng vào plan; 3 Reject giữ nguyên**. Không có Critical đã được chứng minh. Trạng thái execution của plan vẫn pending; không suy approval triển khai hay chất lượng từ việc sửa plan.

Approval ngày 04/10/2026: user trả lời “duyệt 9 điều chỉnh”, sau đó “duyệt tất cả điều chỉnh”. Phạm vi là A1–A9 để hoàn thiện plan; không cấp quyền implement, build/install, trust, native/provider run hay publish. [Quyết định language](./decision-261004-0047-writer-language-options.md) giữ hai writer với `--en`/`--vi`, target 39. Gate xin duyệt amendment đã đóng; không hỏi lại.

Nguồn: [Security](./red-team-261004-0047-security.md), [Contracts](./red-team-261004-0047-contracts.md), [Failures](./red-team-261004-0047-failures.md). Các ký hiệu S/C/F bên dưới chỉ dùng trong hồ sơ review, không đưa vào tên code/test/commit.

## Chín điều chỉnh — finding và đề xuất ở snapshot review gốc

Các đoạn dưới giữ lý do/locator của bản draft trước sửa để truy vết. Từ “đề xuất/chưa duyệt” bên trong phần lịch sử không phải trạng thái hiện tại; bản áp dụng và kiểm chứng nằm ở [hồ sơ sau approval](./validation-261004-1002-approved-plan-amendments.md).

### A1 — HIGH — Sửa thứ tự freeze và kiểm tra toàn source (F1 + C3)

P1:10 giữ lock r26 bất biến đến P4 nhưng P1:47 và P2:45 gọi `--validate-only`. `nckh-kit/core/build.py:90-98` từ chối inventory/hash lệch; `core/evaluation.py:115` kiểm lock. Đây là lỗi chuỗi thực thi, không phải lý do bỏ guard.

**Đề xuất:** P1–P3 dùng phép kiểm tập trung không phụ thuộc lock; câu lệnh kiểm source toàn bộ chỉ là baseline trước sửa hoặc checkpoint sau freeze P4. Rà từng test xem có gọi `load_profile`/`verify_source_lock` trước khi xếp vào checkpoint. P4 vẫn là một owner freeze; đây là lựa chọn trong draft, chưa phải quyết định đã được user chấp thuận. Không bypass lock, không sửa lịch sử để làm test xanh.

### A2 — HIGH — Hoàn chỉnh contract 37→39 và giữ nguyên tập identity cũ (F2 + C2)

Draft đã nêu catalog/build/evaluation/profile/tests, nhưng bỏ owner `nckh-kit/core/acceptance.py:75-82`, nơi vẫn yêu cầu đúng 37. Schema `core/contracts/catalog.schema.json:12-15` chỉ đặt lower bound; `tests/release/test_qualification.py:12-19,34-49` có literal candidate counts. `scripts/compare-matched.py:51-65` lại cố ý giữ 37/148 cho historical diagnostic.

**Đề xuất:** thêm inventory các consumer/count theo hai loại candidate và immutable history. Expected identity set phải bằng đúng tập 37 của baseline hợp với hai ID mới; test thiếu/đổi/trùng ID. Candidate có đúng 39 identity và 156 base cases (4/identity); ca phụ cho routing/visual/hook là supplemental, không tùy tiện làm manifest bốn case thành 156+. Giữ 148 case IDs và các receipt lịch sử, phân biệt đổi nội dung case hiện tại với sửa lại bằng chứng đã đóng băng; giữ historical 224 matrix cùng nội dung cũ.

### A3 — HIGH — Đưa hook vào đường đóng gói thực (F3)

P3:32-33 tạo `hooks/runner.py`, config và codecs nhưng `nckh-kit/core/build.py:18-21` không quét `hooks`; closure tại `:218-231` bắt đầu từ skill/resources, manifest tại `:305-340` chưa có hook payload. Ghi file mới không tự khiến nó có trong bundle.

**Đề xuất:** chọn bounded hook closure trong package, không cắt bỏ portability đã yêu cầu. Nêu chính xác owner source inventory, artifact schema/manifest, closure, relocation, verification và tests. Pin các script/codecs/config template cùng dependencies; thử đọc/chạy checker từ package đã tách khỏi repo. Packaged không đồng nghĩa registered/enabled/trusted. Không thêm template mang schema chung giả cho cả bốn host.

### A4 — HIGH — Owner thực thi cho preview/apply/remove cấu hình hook (F4 + S4)

P3:41 và P4:42 hứa merge owned blocks nhưng chưa có mutator owner. `nckh-kit/installer/nckh-installer.py:39-56` chưa có hook operation; `core/install.py:49-58,149-229,499-515,570-594` quản lý skill/agent paths. `core/paths.py:97-108` là atomic replacement cả file, không tự giải quyết sửa đồng thời.

**Đề xuất:** plan một module/entrypoint transaction hook có preview/apply/remove rõ ràng; không ngầm coi installer skill hiện có đã hỗ trợ. Trước triển khai chốt exact target từng host, owned definition IDs/JSON members, parent/preimage/definition hashes, khóa và compare-before-write; config đổi sau preview hoặc JSON không hợp lệ phải no-write/conflict. Preserve mọi mục không sở hữu; rollback chỉ gỡ phần còn khớp receipt, không overwrite sửa mới. Ưu tiên dừng khi xung đột, không bắt xây dịch vụ merge phức tạp. Chỉ apply cấu hình khi có grant; trust do user/host quyết định riêng.

### A5 — MEDIUM — Nối đúng build, extract, smoke và installer (F5)

P4:47 chỉ ghi build `--check`, nhưng `nckh-kit/scripts/build-artifacts.py:31-38` xóa staging check và chỉ ghi output bền ở nhánh non-check. Smoke cần bundle thật; installer mặc định `dist` nếu thiếu `--package` (`installer/nckh-installer.py:40`).

**Đề xuất:** giữ reproducibility check, bổ sung lệnh tạo output vào thư mục owned rỗng cho on/off/plugin, đường extract/outside-repo/receipt cụ thể và `--package` trỏ đúng output. CLI placeholder phải được giải quyết thành path của run trước thực thi. Không ghi đè `evals/results/local-checks.json` lịch sử; dùng attempt mới.

### A6 — HIGH — Resource→consumer của hai writer phải được khai báo cụ thể (C1, chấp nhận hẹp)

P1:28 **đã liệt kê** `resources.json`; khẳng định reviewer rằng file owner hoàn toàn vắng là sai. Góp ý đúng là chưa có matrix binding cụ thể. `nckh-kit/scripts/search-resource.py:220-223` từ chối consumer không đăng ký; `core/build.py:224-229` không cho identity mới thừa hưởng resource của `nckh-write`.

**Đề xuất:** giữ mọi consumer cũ; humanwrite được đọc Nature English, Wikisource VI và PMC khi cần fidelity khoa học; paperwrite được đọc PMC, Nature English và reporting lookup đúng clinical/health applicability. Không cấp Wikisource cho paperwrite như scientific-style gold. Cập nhật resource registry, reference/reader invocation và test on/off/extracted closure cho từng consumer; không đổi locale/domain/rights filters. Publisher vẫn do visuals sở hữu. Chín packs hiện có được tái dùng, không thu gom thêm corpus vì số lượng.

### A7 — MEDIUM — Chốt reader/test cho candidate mới và validator writer matrix (C4, chấp nhận hẹp)

Base cases mới sẽ được evaluator đọc theo catalog (`nckh-kit/core/evaluation.py:79-95`); không chấp nhận kết luận chúng không có validator. Khoảng trống thật: runtime reader hiện chỉ đọc matrix cũ (`:104-115`), còn file mới/flag `--writer-matrix` trong P1/P4 chưa có owner/schema/oracles chốt. Humanizer ở source map:16 còn để Markdown/JSONL/generic reader tùy chọn.

**Đề xuất:** Humanizer thành owned local policy `nckh-humanwrite/references/humanizer-adaptation.md`, reader trực tiếp từ entrypoint skill, linked/pinned trong closure; mỗi rule có context/counterexample/protected fields, output là edit diff và factual-delta record. Test link/closure, positive/counterexample và không đổi số/citation; không gọi ví dụ soạn mới là corpus/human gold. Matrix writer có schema/validator bắt buộc, exact ID set, route/surface/receipt oracles; nối nó vào evaluator hay command riêng có owner rõ ràng, không chỉ để file tồn tại. Tên module test tùy tái dùng suite, coverage không được optional.

### A8 — MEDIUM — Không đồng nhất nghiên cứu định lượng với chỉ số đo quan sát (C5)

P2:14 và source map:27 hạn chế chart vào measurement và cấm dữ liệu tổng hợp. User yêu cầu scientific purpose, không yêu cầu loại toàn bộ simulation/theory. `nckh-kit/skills/core/nckh-visuals/SKILL.md:26` chỉ cấm synthetic measurement giả làm observed result.

**Đề xuất cần duyệt:** cho phép biểu đồ derived/computational/simulation từ phép tính hoặc run thực có code/model/version/parameters/source/transform hashes và nhãn rõ không phải số đo quan sát. Không xây thêm simulation pipeline; chỉ sửa hợp đồng/ca kiểm tra. Tiếp tục cấm invented observations, fabricated runtime và generic decorative art. Explanatory illustration vẫn có nhãn không phải evidence.

### A9 — MEDIUM — Phân biệt instruction gate với host enforcement (S3, chấp nhận hẹp)

P2:53 hứa mọi route fail-closed; P3:18 thừa nhận degraded/manual. Official capability report:13-16 ghi Codex tool-coverage ngoại lệ và Cursor có thể fail-open; chưa có native evidence. Điều này không chứng minh bug của kit hiện hành, nhưng cần giới hạn lời hứa trong exit criteria.

**Đề xuất:** liệt kê actual generating entrypoints/bindings và negative tests direct/indirect; đường controlled script gọi synchronous preflight trước side effect. Instruction-only/uncovered host routes không được báo là enforced. Test deny/malformed/timeout/crash/unsupported riêng cho từng event/version được bật; thiếu capability giữ manual/not-callable và dừng generation tại workflow. Hook không bảo vệ mọi đường thoát shell/host, không dùng post-check làm proof ngăn side effect. Không tạo service/capability mới chỉ để giả lập sandbox.

## Ba nhóm Reject

| Finding | Phân xử dựa trên source/plan |
|---|---|
| S1: bắt non-forgeable capability/private controller cho visual purpose | Reject phần kiến trúc bắt buộc. Threat model là kit instruction + checker cục bộ trong quyền host, không phải malicious-client authorization service. `authorization-policy.md:3-6`, P2:16/P3:38 đã loại JSON/model thành grant. Purpose declaration không chứng nhận khoa học; không thể biến kiểm field thành proof mục đích. Kiểm route/negative nằm trong A9. |
| S2: bắt private sidecar/monotonic capability để tin hook event | Reject phần bắt buộc cùng lý do. Caller truyền trusted task context từ host/controller và payload là untrusted data; contract đã đòi không suy grant từ payload. Không có bằng chứng cần hệ thống cấp quyền mới. Test thiếu/sai context thuộc policy/codec tests của A9, không service mới. |
| S5: current visual guard làm rò private path, bắt sidecar mới | Reject kết luận từ source. `core/guards.py:61-69` đọc/hashes paths nhưng chỉ trả status, không ghi path vào receipt. P3:16 cấm log path/command/raw draft; `authorization-policy.md:17-20` đã yêu cầu private store/opaque public refs. Giữ negative privacy tests khi thiết kế schema, không khẳng định leak đã tồn tại hay nhân đôi storage architecture. |

Report security đã sửa lỗi attribution: fail-open của ClaudeKit script không phải default của Claude host. Chỉ dùng official Cursor evidence và các host coverage chưa xác minh.

## Áp dụng sau approval

| Amendment | Owning plan surface | Điều đã đưa vào kế hoạch |
|---|---|---|
| A1 | P1/P2/P3/P4 | Trace focused tests, full validator/build sau single-owner freeze; correction tạo revision mới, giữ failure receipts |
| A2 | P1/P4 | acceptance/schema/count consumers; exact 39/156 và missing/replaced/duplicate tests, history 37/148/224 không sửa |
| A3 | P3/P4/source map | hooks source inventory, v2 typed manifest, bounded deps, inactive plugin payload, extracted verification |
| A4 | P3/P4 | dedicated config module/CLI, exact project targets, preview hashes/lock/compare, owned remove/rollback |
| A5 | P4 | persistent on/off/plugin builds, per-host archive/extraction/CWD/receipt contract, explicit installer package |
| A6 | P1/source map/P4 | exact additive writer/resource matrix; locale/domain/genre/rights và extracted on/off tests |
| A7 | P1/P4/source map | direct linked Markdown Humanizer, diff/factual delta, mandatory writer matrix/schema/validator; không orphan flag |
| A8 | P2/source map/index | calculated/simulated plots có actual output/provenance/uncertainty/label; không thêm simulation pipeline |
| A9 | P2/P3/P4/index | actual entrypoint/binding inventory, instruction vs host coverage, per-event native failure tests trước activation |

Các phase vẫn unchecked/pending vì đây là kế hoạch triển khai. Whole-plan sweep, CLI/path checks và integrity reconciliation được ghi trong hồ sơ sau approval; các finding gốc và ba lý do Reject không bị sửa để giả rằng draft ban đầu đã đầy đủ. Không còn câu hỏi duyệt A1–A9; cook/install/trust cần lệnh riêng.
