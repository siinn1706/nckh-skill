# Checklist hoàn thành các plan

Cập nhật 03/10/2026. Project: `test-skill`. Bản hiện cài: **r25**. Plan personal-use **completed, 26/26 đầu việc** theo checkbox các phase. Cả ba đầu ra mới đã nhận lúc 21:13–21:29, repairs/source/render/native QA đạt trong phạm vi artifacts và receipts đã kiểm. r25 tests/build/extracted checks, installation/hash/binding integrity đạt; doctor 43 current, post-preview 43 unchanged. Owner scoring sau dùng vẫn `pending-personal-review`; portable/resource-quality qualification còn mở. Checkpoint trước khi nhận ba đầu ra ghi 25/26 và goal blocked được giữ làm lịch sử; `get_goal` trả active tại checkpoint closeout trước khi controller chốt docs/validation. Số checkbox không phải điểm chất lượng skill.

[Native goal đã chuyển `complete`](../evaluation/personal-use/personal-use-goal-completion-01.json) sau khi chốt docs và validation. Các ghi nhận goal blocked/active bên dưới là checkpoint lịch sử.

## 1. Việc kỹ thuật đã xong

- [x] Giữ đúng 37 skill và sáu agent hiện có.
- [x] Lấy mẫu thật từ Wikisource, PMC, World Bank, UCI và Django.
- [x] Nối năm nhóm mẫu vào reader và hướng dẫn của 12 skill sử dụng chúng; giữ nguồn, phiên bản, hash và giới hạn quyền.
- [x] Đặt tiêu chí chung/riêng có nguồn chính thức cho đủ 37 skill; áp dụng theo domain, venue, platform và phạm vi của từng nguồn.
- [x] Cho phép bàn giao personal-use để người dùng tự chấm sau; reviewer bên ngoài và protected holdout không chặn tuyến này.
- [x] Kiểm tra r24: 120/120 tests, build bật/tắt tài nguyên trên bốn môi trường và đọc sau giải nén đều đạt.
- [x] Candidate r25 đạt 10 technical checks: 136 tests gồm 135 pass/một symlink fixture skip, zero errors/failures; bốn host build on/off và extracted reads pass.
- [x] Cài r24 vào project: 37 skill cập nhật, sáu agent giữ nguyên; kiểm tra sau cài có 43 mục đúng và không xung đột.
- [x] Giữ first r25 timeout/TEMP failure và update failure; mọi candidate attempt đã cleanup. Update rolled-back không conflicts, r24 bytes/ownership nguyên và doctor 43 current.
- [x] Cài r25 thành công sau khi người dùng đóng Cursor: update exit 0/installed, transaction committed, install identity và physical after/backup hashes khớp; doctor 43 current, post-preview 43 unchanged/zero conflicts, ba binding integrity checks đạt. Review độc lập có 14 checks PASS, không có finding chặn cài đặt.
- [x] World Bank GPT-6.1 Sol r25: source/memo review và controller source-to-mark/render/native edit-save-reopen-restore/layout/contrast/accessibility cấu trúc checks đạt, gắn đúng artifact hashes. Owner vẫn pending-personal-review.

## 2. Bàn giao personal-use đã xong

- [x] Xác nhận bằng run thật rằng neutral shared root/installed source readers được đọc đúng trên các route đã quan sát. Coverage chỉ năm consumer identities, không phải native behavior của cả 37 skills.
- [x] Cursor — **chỉ Grok 4.7 Extra High** — đã hoàn tất năm memo và sáu reader receipts r24.
- [x] Antigravity — **Gemini 3.8 Flash High** — đã hoàn tất năm memo và sáu reader receipts r24.
- [x] Ứng dụng hiện tại — **chỉ GPT-6.1 Sol** — attempt 03 có artifact VI thật, exit 0, cleanup và artifact review pass; task này chỉ bao phủ ca VI. Tám model khác excluded theo người dùng.
- [x] Cursor đã sửa Django repair-direction và thêm UCI target count table; delta artifact review pass, giữ dữ liệu/giới hạn và outputs gốc.
- [x] Antigravity đã sửa EN early-career claim, UCI overdraft interpretation, Django missed finding, VI moral voice/chẩn đoán/metadata; repair 02 đã đóng chú giải VI và self-count EN.
- [x] GPT-6.1 Sol đã reconcile instruction-authority/brief mismatch và sửa quote capitalization/path label. Mandatory global development-rule read được ghi riêng theo host hierarchy; trace gốc giữ nguyên.
- [x] Task-local visual binding source đã review và freeze r25 với 243 files; integrity/extracted checker evidence chỉ áp dụng route và source đã kiểm.
- [x] Đã nhận Antigravity repair 02 và review delta đạt: contextual-gloss labels đúng, giữ quotes/ba anchors; EN conclusion không đổi, đúng 161 whitespace-separated tokens và bỏ nhãn 178 không có phương pháp.
- [x] Đọc actual r25 update/doctor/post-preview/installed binding receipts sau khi người dùng đóng Cursor; installation và binding integrity đạt. Các failed updates/rollback trước được giữ làm lịch sử.
- [x] Đã nhận hai World Bank SVG/output IDE; source-to-mark, actual render/open/edit/save/close/reopen/restore, layout và accessibility cấu trúc/contrast QA đạt theo từng artifact hash.
- [x] Giữ raw outputs/failures, source audit và final native review đạt scope đã giao; đóng task IDE repairs/SVG/QA và hoàn tất plan personal-use 26/26.

[Cursor repair review](review-261003-1448-cursor-r24-repair-01.md) · [Antigravity repair review](review-261003-1448-agy-r24-repair-01.md) · [GPT-6.1 Sol attempt 03 review](review-261003-1448-gpt-6-1-sol-r24-repair-01.md). Completed run chưa có nghĩa là toàn bộ output contracts đã pass. Effective model/effort và fresh UI observation vẫn unknown/unverified; owner scoring chưa có.

Người dùng báo cả ba prompts đã hoàn tất; artifacts đã nhận và [repair 02 review](review-261003-2137-agy-repair-02.md) đạt. User-reported Antigravity PowerShell/`dangerous` route và selected models giữ riêng với effective provider telemetry. Ba repair reader receipts khớp installed inputs nhưng có JSON bằng repair 01/bytes bằng originals, không chứng minh fresh reader execution.

Năm ca đã chuẩn bị:

| Ca thử | Đầu ra cần có | Điều cần kiểm |
|---|---|---|
| Văn phong tiếng Việt — Wikisource | Nhận xét văn phong có neo vào đoạn gốc | Đọc trang con thật; giữ chính tả lịch sử; tách lỗi khỏi khẩu vị |
| Viết khoa học tiếng Anh — PMC | Bản chỉnh và ghi nhận thay đổi | Giữ ý, mức độ chắc chắn, số liệu, nguồn và giới hạn của bài |
| Biểu đồ — World Bank | SVG chỉnh sửa được và ghi nhận kiểm tra | Dùng 26 quan sát thật; tính đúng; giữ metadata nguồn |
| Rà mã — Django | Nhận xét gắn vị trí mã và bằng chứng | Dùng đúng hai fixture BSD; chỉ kết luận trong phạm vi đã đọc |
| Phân tích — UCI | Bảng thống kê và diễn giải | Đúng mẫu 10 dòng/17 cột; không suy ra hiệu quả toàn bộ chiến dịch; nêu rủi ro của biến duration |

[Định nghĩa ca thử](../evaluation/personal-use/native/cases/real-source-cases.json) · Prompt Cursor (historical evidence path: `../evaluation/personal-use/native/cursor-grok-r24-prompt.txt`; unavailable in the cleaned checkout) · Prompt Antigravity (historical evidence path: `../evaluation/personal-use/native/agy-gemini-r24-prompt.txt`; unavailable in the cleaned checkout).

Batch chín model lỗi startup, automatic approval review rejection và lỗi UI ở checkpoint trước được giữ làm lịch sử. Quyết định current-app/chỉ GPT-6.1 Sol đã thay phạm vi all-model; không còn yêu cầu chạy lại cả batch. Failures cũ không chứng minh tám model bị loại là unavailable. Các run r14 cũng chỉ là lịch sử, không thay thế r24.

Installed r24 visual contract unavailable/null là checkpoint lịch sử. [Checkpoint kỹ thuật r25](runtime-261003-1623-r25-verification-and-install-handoff.md) ghi source-lock `adc6422394da5a833e1059d922b27c5658eb6699b2ab950568a557d48d71968c`, technical pass và failed update/rollback thực tế. Lệnh update trước được approved và chạy, nhưng WinError 5 chặn rename vào backup; không phải automatic approval review rejection. Parent `.agents/skills` có explicit Deny sandbox SIDs theo read-only inspection; không thay ACL. Rollback giữ r24 nguyên và doctor 43 current tại lần kiểm đó.

[Script cài thủ công](../evaluation/personal-use/complete-r25-install.ps1) đã qua parser và independent source review không có finding trong scope; người dùng đã chạy nhưng update thất bại và rollback. [Checkpoint manual failure](runtime-261003-1720-r25-manual-failure-and-lock-diagnosis.md) giữ nguyên lịch sử Cursor đang dùng file target, wrapper error parser đã sửa và SVG checker có 12 focused tests đạt. Sau khi người dùng đóng Cursor, [receipt cài r25 thành công](../evaluation/personal-use/install-r25-after-cursor-close-01/receipt.json) và [review cài đặt độc lập](review-261003-1757-r25-project-install.md) xác nhận project hiện cài r25, transaction committed, identity/hash/doctor/post-preview/binding integrity đạt. Lần thành công không chứng minh Cursor là nguyên nhân khóa duy nhất; binding integrity không xác nhận native execution hoặc final SVG QA.

Checkpoint current-app ngày 03/10/2026, trước khi nhận ba đầu ra IDE mới: [controller probe](../evaluation/personal-use/visual-engine-probe-01/native-observation.json) giữ capability observation riêng. [Run receipt World Bank current-app/chỉ GPT-6.1 Sol](../evaluation/personal-use/native/app-gpt-6-1-sol-r25-visual-attempt-01/gpt-6.1-sol/real-source-worldbank-visual-01/receipt.json) giữ generation-time `completed-unreviewed`, exit 0, 286.531 giây và `owned-process-group-closed`; [source review](review-261003-gpt-sol-r25-worldbank-source-and-memo.md) và [controller QA sau đó](../evaluation/personal-use/native/app-gpt-6-1-sol-r25-visual-attempt-01/gpt-6.1-sol/real-source-worldbank-visual-01/controller-qa.json) đạt source-to-mark/render/native/layout/contrast/accessibility cấu trúc trong scope artifact đã gắn hash.

Current-app QA dùng Illustrator 28.0.0: 29 text frames/26 data paths/zero raster; edit/save/close/reopen/restore đạt, tọa độ trong 0.000023 SVG units. Controller đã xem hai ảnh; không thấy clipping/text overlap ngoài ý định, contrast tối thiểu 6.0989 cho bốn màu đã kiểm. Raw pending captions giữ trạng thái lúc generation; receipt QA riêng gắn SVG/PNG/AI derivative hashes. Kết quả này giữ scope current-app riêng với các IDE QAs nhận sau.

[Review current-app QA](review-261003-gpt-sol-r25-worldbank-controller-qa.md) và [nhật ký r25 trước](../journals/2026-10-03-nckh-r25-installed-and-gpt-sol-world-bank-controller-qa.md) giữ checkpoint lúc IDE còn pending. Closeout mới: [runtime](runtime-261003-2137-three-prompts-and-personal-use-closeout.md), [source audit hai IDE](review-261003-2137-ide-worldbank-source-and-receipts.md) và [final native review](review-261003-2137-ide-worldbank-controller-qa.md) xác nhận source/render/native QA đạt scope hiện tại, không có blocker.

| Artifact bàn giao | Native structure | QA và bản chỉnh sửa được |
|---|---|---|
| Antigravity World Bank | 29 text frames, 26 data paths, zero raster | [QA](../evaluation/personal-use/native/agy-gemini-r25-visual-01/controller-qa-01/controller-qa.json) · [SVG](../evaluation/personal-use/native/agy-gemini-r25-visual-01/real-source-worldbank-visual-01.svg) · [AI đã restore](../evaluation/personal-use/native/agy-gemini-r25-visual-01/controller-qa-01/native-qa-copy.ai) |
| Cursor World Bank | 166 text frames, 26 data paths, zero raster | [QA](../evaluation/personal-use/native/cursor-grok-r25-visual-01/controller-qa-01/controller-qa.json) · [SVG](../evaluation/personal-use/native/cursor-grok-r25-visual-01/real-source-worldbank-visual-01.svg) · [AI đã restore](../evaluation/personal-use/native/cursor-grok-r25-visual-01/controller-qa-01/native-qa-copy.ai) |

Hai IDE SVG có 26 source values/marks/polyline/table/ticks/formulas khớp nguồn. Actual rsvg 2.40.20 render tái tạo submitted PNG bytes; Illustrator 28.0.0 edit text/point, save/close/reopen giữ sửa, restore/save/close/reopen giữ nguyên text và 26 points với sai lệch dưới 0.0001 SVG units. Controller và reviewer đã xem các ảnh cuối; không thấy clipping/text overlap ngoài ý định hoặc mất điểm. AGY SVG/PNG byte-identical với bản GPT-6.1 Sol trước đó, không chứng minh independent Gemini generation.

AGY raw Source truth pass sớm được giữ; [reviewed memo](../evaluation/personal-use/native/agy-gemini-r25-visual-01/controller-qa-01/reviewed-memo.md) và [revision receipt](../evaluation/personal-use/native/agy-gemini-r25-visual-01/controller-qa-01/memo-revision.json) sửa nhãn generation/controller/model provenance, không đổi SVG. Accessibility chỉ gồm cấu trúc SVG/contrast; AGY có role/ARIA, Cursor có title/desc/lang theo thiết kế đã ghi. Chưa AT testing, không claim SVG accessibility metadata persistence trong AI hoặc exact rsvg font resolution. Effective model/effort vẫn unverified; owner acceptance thuộc người dùng sau sử dụng. [Nhật ký closeout](../journals/2026-10-03-nckh-three-prompts-reviewed-and-personal-use-handoff.md) ghi bàn giao 26/26.

## 3. Phần owner tự đánh giá sau khi dùng

1. Dùng thử skills và các artifacts đã bàn giao trong project `test-skill`; bản r25 đã cài, hai World Bank SVG/AI có QA receipts.
2. Đánh giá đúng/sai, hữu ích, văn phong và khả năng chỉnh sửa theo nhu cầu cá nhân. Owner score vẫn `pending-personal-review` cho tới khi có feedback thật.
3. Nếu cần sửa, gửi tên skill, file/đoạn sai, kết quả mong muốn và phần cần giữ nguyên; feedback gắn artifact/revision. Không cần hội đồng review hoặc bộ holdout để bắt đầu dùng cá nhân.

## 4. Hiểu trạng thái các plan cũ

| Plan | Cách xử lý hiện tại |
|---|---|
| [Việt–Anh ban đầu](../260930-0905-vietnamese-research-skill-kit/plan.md) | Đã được thay thế; giữ làm hồ sơ, không triển khai lại. |
| [NCKH portable](../260930-1910-nckh-portable-skill-kit/plan.md) | Vẫn active. Phần source/package/install có bằng chứng; các yêu cầu stable, khoa học, runtime/OS đầy đủ và phát hành vẫn có phạm vi riêng. |
| [Resource quality](../261002-0832-nckh-skill-resource-quality/plan.md) | Vẫn active. Giữ kết quả kỹ thuật và các yêu cầu so sánh có kiểm soát/human qualification; không dùng nguồn mẫu hoặc tests để tự đóng chúng. |
| [Personal-use hiện tại](../261003-0101-nckh-personal-use-sources-and-standards/plan.md) | completed, 26/26 đầu việc theo phase checkboxes. Cả ba đầu ra mới/repairs và source/render/native QA đạt scope đã kiểm; owner scoring sau dùng còn pending. |

## 5. Nếu muốn đóng đầy đủ các plan portable và resource-quality

Những yêu cầu dưới đây thuộc phạm vi kiểm định rộng hơn. Chúng không chặn bàn giao và bắt đầu dùng cá nhân theo quyết định hiện tại.

- [ ] Kiểm tra thực tế các chế độ tự động, tương tác, nhận feedback và tiếp tục phiên; ghi được model/effort thực sự áp dụng — [Portable phase 1](../260930-1910-nckh-portable-skill-kit/phase-01-start.md).
- [ ] Có đánh giá phù hợp cho văn phong Việt, độ trung thành bản viết Anh, chất lượng khoa học/chuyên môn và khả năng chỉnh sửa hình trong ứng dụng gốc — [Portable phase 2](../260930-1910-nckh-portable-skill-kit/phase-02-core-research-writing-visuals.md).
- [ ] Kiểm tra skill được ứng dụng tìm thấy và gọi đúng; kiểm tra model, hooks và quyền trên từng ứng dụng được công bố hỗ trợ — [Portable phase 5](../260930-1910-nckh-portable-skill-kit/phase-05-runtime-adapters-and-build.md).
- [ ] Kiểm tra cài đặt/gỡ/khôi phục trên các hệ điều hành và cách cài được công bố hỗ trợ — [Portable phase 6](../260930-1910-nckh-portable-skill-kit/phase-06-installer-and-recovery.md).
- [ ] Chốt protocol, quyền nguồn, ngân sách và phần đánh giá độc lập của tuyến stable; chạy đủ bộ kiểm tra hành vi/runtime/installer và so sánh với baseline — [Portable phase 7](../260930-1910-nckh-portable-skill-kit/phase-07-qualification-and-migration.md).
- [ ] So sánh skill có/không tài nguyên với cùng đầu vào và chính sách; giữ đủ sáu điều kiện, tách migration; có tiêu chí, ngưỡng chấm và kết quả human/native theo protocol — [Resource-quality phase 4](../261002-0832-nckh-skill-resource-quality/phase-04-behavioral-qualification.md).

Các lượt r14/r18 và manifest so sánh đã chuẩn bị là hồ sơ lịch sử hoặc bằng chứng chuẩn bị; phải đối chiếu đúng revision/artifact hiện đánh giá khi chốt. Quyền cook trong project hiện tại không tự cấp quyền cài global, chạy ngoài project hoặc phát hành.

[Plan hiện tại](../261003-0101-nckh-personal-use-sources-and-standards/plan.md) · [Bằng chứng r24 và blockers](runtime-261003-candidate-r24-checkpoint.md) · [Hướng dẫn dùng cá nhân](../../nckh-kit/docs/personal-use.md) · [Nhật ký](../journals/2026-10-03-nckh-r24-personal-use-resources-and-runtime-checkpoint.md).

Trạng thái mới nhất: **personal-use completed, 26/26**. Antigravity repair 02, hai World Bank IDE artifacts và current-app artifacts đã có scoped reviews/QA; original outputs/failures giữ nguyên. [Audit blocked](blocked-audit-261003-native-r24.md) và checkpoint 25/26 trước ngày 03/10/2026 lúc 21:13 là lịch sử; `get_goal` trả active tại checkpoint closeout, controller chốt goal sau docs/validation. Scope model giữ Cursor chỉ Grok 4.7 Extra High, Antigravity Gemini 3.8 Flash High và current app chỉ GPT-6.1 Sol; selected/user-reported model riêng với effective telemetry chưa xác minh.

Completion personal-use không tạo điểm chấm của owner, human gold, scientific/stable certification, effective-provider-model certification hoặc publishing clearance. Owner scoring sau dùng và các qualification gates rộng hơn của portable/resource-quality tiếp tục giữ trạng thái thực.
