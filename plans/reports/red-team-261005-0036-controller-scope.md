# Controller review: scope, contracts và executable paths

Ngày 05/10/2026, Asia/Saigon. Review tài liệu; không chạy build/tests/source/provider. Đọc index và bảy phase đã có body; adoption/matrix chờ final handoff. Root áp Scope & Complexity Critic và Contract Verifier; requested scientific scope là constraint, không có `--yagni`.

## R1 — Medium: smoke CWD trong RUN không nằm ngoài repository

- Evidence: `phase-07-integration-and-qualification.md:74` dùng `<RUN/outside-cwd>`, trong khi `RUN` được P1 định nghĩa ở `WORK/plans/runs/`. `nckh-kit/scripts/resource-smoke.py:27-29` resolve repository root là `WORK` khi root có `plans/`, và refuse CWD là descendant của root/bundle.
- Failure: mọi bundle hợp lệ vẫn bị fail trước consumer invocation vì CWD thuộc repository; chạy lại không chữa được path policy mismatch.
- Correction: define `OUTSIDE` là owned permitted temporary root có absolute resolved path thực nằm ngoài `WORK` và bundle; record ownership/path mapping trong RUN. CWD dùng `OUTSIDE/cwd`, receipts lưu RUN; extraction/cleanup chỉ matching owned paths, không delete temp root rộng.
- Disposition: Accept làm drafting correction; đã gửi planner. Đây là executable validation route được xác minh từ source, không thay scope/user decision.

## C1 — factual correction, không severity finding: schema engine không có registration table

`phase-07-integration-and-qualification.md:23` gọi `core/schema.py` là “registration only”. `core/schema.py:87-88` chọn file contracts trực tiếp theo `kind`; engine hiện không có schema registration table. Đã gửi planner để giữ engine/subset unchanged và integrate named schemas/owning validators/closure ở owner thực. Không tạo abstraction hoặc edit engine không cần thiết.

## Scope review

Bốn owner phục vụ artifacts khoa học khác nhau; marketing và generic engineering semantics được giữ; writer/visual/hooks thuộc dependency đã được user xác định. Four packs có reader/consumer/output riêng; experiment checker không phải runner/orchestrator. Không phát hiện scope addition cần user cắt. Source rights/native/human/scientific qualifiers không được đóng bằng parser/count/build.

Full sweep và exact final line references sẽ được reconcile sau planner handoff; báo cáo này không kết luận implementation/runtime đã pass.

## Full-plan reconciliation sau planner handoff

Controller đã đọc đủ index, P1–P7, adoption map và acceptance matrix; đối chiếu các chỉnh sửa cuối sau khi planner dừng sửa directory. Các locators ban đầu ở trên là lịch sử của draft.

| Item | Disposition hiện tại | Resolution trong final plan |
|---|---|---|
| R1 Medium — smoke CWD | **RESOLVED IN PLAN** | P7:16/47/64/74 định nghĩa permitted attempt-owned `OUTSIDE` ngoài `WORK`, archive/extract và CWD ngoài mọi bundle, actual ownership/path/hash mapping trong `RUN`, exact owned cleanup. |
| C1 — schema registration | **CORRECTED FACTUAL CLAIM** | P1:34, P7:23/38 giữ dynamic `validate_record(kind)` lookup và supported subset; không thêm registration table hoặc sửa engine vô cớ. |
| Identity/resource prerequisites | **COHERENT AFTER CORRECTION** | P2:20/48, P5:27/55/59/72, P7:25/32/43 cùng đặt exact catalog/profile/base-case/source-kind integration trước actual local pack reads và P6; P7 reconcile final bytes. |
| Candidate lock/check order | **COHERENT AFTER CORRECTION** | P2/P3/P4 chỉ kiểm pre-freeze khi không phụ thuộc lock; P5 tách local typed/read gates khỏi frozen closure; P7:45–46/66–68 đặt independent checks → freeze khi owners quiescent → pinned regressions. |
| Required preview model choice | **COHERENT AFTER CORRECTION** | P7:75/78 có explicit `--models balanced` hoặc actual verified frozen profile; no-write preview không thành install/native/provider grant. |

Whole-plan scope/ownership/dependency/rollback sweep không có consequential finding mới. Bốn scientific owners và bốn bounded packs có source → producer → reader → artifact → verification riêng. Exact identities/cases là conditional P1 baseline; source rights/ref, actual pilot/runtime và scientific/native/owner verdict vẫn pending execution gates. Lượt planning không chạy các implementation verification commands.

Không khởi tạo long-lived server/watcher/process ở lượt này; các utility calls hoàn tất qua harness. Không có process do controller sở hữu cần giữ hoặc dừng sau handoff.

Status: DONE
Summary: Whole-plan scope/contract sweep hoàn tất; R1/C1 và các integration corrections đã đối chiếu coherent, không có finding mới cần đổi scope.
