# Phân xử review kế hoạch — 11 điều chỉnh đã được duyệt và áp dụng

Ngày 30/09/2026, Asia/Saigon. Đối tượng là [bản kế hoạch](../260930-0905-vietnamese-research-skill-kit/plan.md), không phải một sản phẩm đã triển khai.

## Trạng thái

Ba reviewer đã nộp tổng cộng 27 đề xuất thô. Controller đọc cả ba, đối chiếu với sáu file plan và hợp đồng thiết kế; gộp thành **14 mục**: **11 đề xuất nhận có thu hẹp phạm vi**, **3 loại**. Phân mức sau phân xử: 9 High và 5 Medium; không xác định Critical có căn cứ cho một lượt plan-only. **Người dùng đã xác nhận áp dụng cả 11 chỉnh sửa ngày 30/09/2026; controller đã sửa các phase, chỉ tài liệu.** Không coi thống kê reviewer là 225 test hay 225 claim độc lập đã xác minh; các tập mẫu chồng nhau, cách gán VERIFIED/FAILED khác nhau và phần lớn là thiết kế tương lai.

Threat model: kit cá nhân project-local trên máy người dùng; nguồn web/PDF, upstream skills và worker artifacts có thể chứa dữ liệu/chỉ dẫn không đáng tin. Chưa có yêu cầu multi-tenant server, tài khoản người dùng, backend tải URL hay publication service. Không dựng thêm hệ auth token, proxy, ký số hoặc encryption infrastructure chỉ để giải quyết một quan ngại trừu tượng.

Tất cả đề xuất được xét đều có `file:line` trong báo cáo gốc; line refs áp dụng cho snapshot review trước khi sửa nội dung phase. Ba báo cáo:

- [Assumptions/scope](review-260930-0905-assumptions.md).
- [Security](review-260930-0905-security.md).
- [Failure modes](review-260930-0905-failure-modes.md).

## 11 đề xuất nhận — đã áp dụng theo phê duyệt

| # | Mức / nhóm | Phân xử và thay đổi tối thiểu đề xuất | Bằng chứng chính |
|---|---|---|---|
| 1 | High — quyền cook/resume | **Accept narrowed.** Lưu dấu vết sự cho phép thật của người dùng, task/workspace/plan/input/profile/worker/egress scope và revision. Trước resume kiểm quyền còn hiệu lực; file tự ghi `approved` không cấp quyền. Không bắt nonce, expiry hay principal server cho kit cá nhân; chỉ thêm khi host thật yêu cầu. | A-F2, SEC-01, F-02; `phase-01-start.md:28`, `phase-01-start.md:57`, `phase-01-start.md:133` |
| 2 | High — timeout và rollback | **Accept narrowed.** Bổ sung attempt ID, staging/committed/timeout-unknown và reconcile-before-retry; không chạy lại side effect chưa biết kết quả. Disable/rollback phải gắn candidate outputs là chưa được nhận và làm mất hiệu lực receipts phụ thuộc; không tự revoke credential của người dùng. | F-01, SEC-08; `phase-01-start.md:111`, `phase-01-start.md:155`, `phase-05-evaluation-and-packaging.md:156` |
| 3 | High — upstream và contract drift | **Accept narrowed.** Receipt chứa contract revision và dependency-closure manifest; có mapping dependency→capability và invalidation xuống artifact. Bản đang chạy phải phát hiện thay đổi trong lúc chạy, không gắn nhãn accepted cho nội dung mới. Hash không chứng minh tác giả: giữ trusted origin/review/promotion record; không bắt mọi repo phải có signed commit hay tự freeze global AgentKit. | A-F7, SEC-05, F-03; `phase-01-start.md:35`, `phase-01-start.md:85`, `phase-01-start.md:92`, `phase-05-evaluation-and-packaging.md:109` |
| 4 | High — claim, profile và trạng thái bàn giao | **Accept narrowed.** Viết ma trận verdict→cách diễn đạt và gate tổng hợp. Claim chưa đủ chứng cứ không được nhận như fact; xung đột phải được thể hiện như xung đột, không cấm thảo luận nguồn trái chiều. Profile/reporting/mentor conflict chặn tuyên bố compliant; output còn gate bắt buộc không được accepted qua tên trạng thái khác. Không tự bỏ phần được người dùng yêu cầu. | A-F5, F-04, F-05; `phase-02-evidence-and-research.md:52`, `phase-03-vietnamese-and-english-writing.md:54`, `phase-05-evaluation-and-packaging.md:52` |
| 5 | High — factual delta sau polishing | **Accept.** Luồng pure-prose vẫn ngắn; sau sửa phải so dữ kiện cũ/mới. Nếu thêm hoặc đổi factual claim, chuyển riêng phần đó sang evidence audit hoặc để evidence-pending. Nhãn “chỉ sửa văn” trong brief không thay cho kiểm đầu ra; fiction không bị ép tìm citation. | A-F4; `phase-03-vietnamese-and-english-writing.md:38`, `phase-03-vietnamese-and-english-writing.md:50`, `phase-03-vietnamese-and-english-writing.md:131` |
| 6 | High — nguồn/policy trở nên cũ | **Accept narrowed.** Định nghĩa thời điểm cần kiểm lại corrections/retractions, ranking và guideline, nhất là trước handoff mang tính nộp bài. Lưu as-of/status-source; thay đổi làm stale dependent claims. Không mặc định poll liên tục hay mở lại mọi URL sau mỗi sửa dấu câu. Snapshot toàn văn không làm trạng thái rút bài vĩnh viễn hợp lệ. | F-09, A-F5; `phase-02-evidence-and-research.md:56`, `phase-02-evidence-and-research.md:106`, `phase-05-evaluation-and-packaging.md:127` |
| 7 | High — dữ liệu riêng và package boundary | **Accept narrowed.** Tách private task artifacts khỏi distributable skills; storage/retention/egress matrix và explicit package allowlist. Kiểm resolved path containment, junction/symlink và không overwrite originals. Redact URL token/private paths; hash giữ cục bộ không tự là lỗ hổng, không thêm HMAC/encryption mặc định khi chưa cần. | A-F9, SEC-06, SEC-07; `phase-01-start.md:35`, `phase-05-evaluation-and-packaging.md:60`, `phase-05-evaluation-and-packaging.md:112` |
| 8 | High — tool boundary khi đọc nguồn | **Accept narrowed.** Nêu khả năng host thực sự enforce, tách source text khỏi instruction authority và chỉ cấp tool cần thiết. URL/parsing do tool có sandbox của host xử lý; nếu sau này tự viết downloader/parser thì phải kiểm redirects, resource limits và local/private network theo quyền. Không yêu cầu xây capability-token proxy hoặc tự nhận delimiter ngăn được mọi injection. | SEC-03, SEC-04; `phase-02-evidence-and-research.md:43`, `phase-02-evidence-and-research.md:88`, `phase-01-start.md:61` |
| 9 | High — QA visual gắn đúng file | **Accept.** Gắn source/data/render/manifest hash, viewer/font version và QA run ID; sửa source hay render làm stale kết quả liên quan. Kiểm lại phần ảnh hưởng trước handoff, không dùng báo cáo pass của file cũ cho file mới. | F-06; `phase-04-slides-and-scientific-visuals.md:48`, `phase-04-slides-and-scientific-visuals.md:68`, `phase-04-slides-and-scientific-visuals.md:103` |
| 10 | Medium — eval có điểm dừng và holdout đúng nghĩa | **Accept narrowed.** Đưa giới hạn ba vòng development từ design proposal vào P5, khóa reviewer/coverage/threshold/budget trước quality run; thiếu thì pending. Tách label khỏi context/đường đọc của writer khi host cho phép; ghi exposure và invalidation/lineage của replacement. Không coi tự chấm hoặc fixtures kỹ thuật là human gold; không ép dựng nền tảng nhiều reviewer. | A-F6, F-07, F-08; `phase-05-evaluation-and-packaging.md:32`, `phase-05-evaluation-and-packaging.md:96`, `phase-05-evaluation-and-packaging.md:141`; design proposal mục nghiệm thu |
| 11 | Medium — coverage và plan-only outputs | **Accept narrowed.** Thêm bảng blueprint capability→module/mode→đầu ra/test, cùng allowed outputs của research-plan. Cho phép plan/research/validation/journal cục bộ đúng brief; không vô cớ cấm mọi journal/task metadata. Chặn implementation/publish ngoài quyền, và không nhận worker có chỉ dẫn bắt buộc xung đột. | A-F3, SEC-02; `phase-02-evidence-and-research.md:62`, `phase-01-start.md:28`, `plan.md:49`; design proposal mục phân rã |

Những mục này chủ yếu làm cụ thể các contract đã có; không đổi năm mục tiêu, lựa chọn English instructions, plan/cook, Q1/Q2 policy hay hướng gọi AgentKit để nhận cập nhật. Chúng đã được user duyệt cho tài liệu; không có approval triển khai đi kèm.

## Mapping sau áp dụng

| Finding | Nơi áp dụng | Nội dung kiểm khi sweep |
|---|---|---|
| 1 | P1 Authorization | Quyền thật gắn scope, không lấy file approval làm authority |
| 2 | P1 attempts; P5 rollback | Timeout-unknown, reconcile, quarantine và invalidation |
| 3 | P1 dependency lifetime; P5 qualification | Contract/closure/origin, mid-run drift, descendants |
| 4 | P2 verdict matrix; P3 fidelity; P5 aggregate | Wording, profile conflict và mọi mandatory gate |
| 5 | P3 factual delta | Polish không được thêm fact rồi bỏ audit |
| 6 | P2 freshness; P5 stale tests | Notice/ranking/venue recheck theo trigger |
| 7 | P1 private storage; P5 package allowlist | Private data tách package, containment và retention |
| 8 | P1 host enforcement; P2 source tools | Prompt/hook reminder không là sandbox; actual host checks |
| 9 | P4 QA binding; P5 stale tests | Exact source/data/render/manifest/viewer/font |
| 10 | P5 isolation and budget | Threshold/reviewer freeze, exposure lineage, tối đa ba vòng |
| 11 | P1 plan outputs; standards detail coverage | Hồ sơ planning được phép và mọi chức năng blueprint |

Tên P1–P5 trỏ tới phase links trong [plan index](../260930-0905-vietnamese-research-skill-kit/plan.md).
Các dẫn `file:line` ở bảng review gốc là snapshot **trước chỉnh sửa**, không phải
line numbers của phiên bản đã cập nhật.

## 3 đề xuất loại

| # | Mức sau phân xử | Disposition và lý do |
|---|---|---|
| 12 | Medium — chưa có invocation runtime | **Reject as blocker riêng (A-F1).** P1 đã giao khám phá interface thật, có adapter/capability registry, same-agent/native/subagent route và `NOT_CALLABLE` khi không có đường chạy; P2–P4 phụ thuộc P1. Không thể yêu cầu runtime đã chạy trong lượt plan-only. Chi tiết enforcement hợp lý được giữ ở mục 8; việc hiện chưa có consumer run vẫn công khai là chưa kiểm. Nguồn: `phase-01-start.md:85`, `phase-01-start.md:104`, `phase-01-start.md:131`. |
| 13 | Medium — bắt A/B instruction English–Vietnamese | **Reject (A-F8).** Người dùng đã chọn viết skill bằng English. Kế hoạch không tuyên bố English tự nó tốt hơn. Giữ English instruction cố định khi so baseline/upstream/wrapper đủ cho mục tiêu; thí nghiệm ngôn ngữ là một yêu cầu mới, không tự thêm factorial design/sample-power gate. Nguồn: `phase-03-vietnamese-and-english-writing.md:42`, `plan.md:17`. |
| 14 | Medium — Unpaywall được hiểu là quyền phân phối | **Reject as separate finding (SEC-09).** P2 yêu cầu license/access tách biệt, hạn chế lưu trữ và package license gate; báo cáo nguồn đã nói rõ OA/free access không tự cho redistribution. Không có câu nào trong plan cấp quyền phân phối từ Unpaywall. Mục 7 vẫn cụ thể hóa storage/package policy chung. Nguồn: `phase-02-evidence-and-research.md:29`, `phase-02-evidence-and-research.md:151`, `research-260930-0905-local-sources-and-evidence.md:92`. |

## Whole-Plan Consistency Sweep

- Controller đã đọc lại `plan.md` và cả năm phase sau khi planner bàn giao; kiểm các bổ sung về English instructions, upstream wrapper, plan/cook, pure-prose route, glossary theo task và nhánh PowerPoint của K-Dense.
- Sửa lỗi soạn thảo trước review đã hoàn tất ở snapshot đầu. Lượt này áp dụng đủ 11 findings và thêm scope user về hooks/subagents/cost, catalog-first plan/cook và context cap. Ước tính mới 12–20 ngày chỉ là effort dự kiến, không cam kết.
- Whole-plan sweep và kiểm cấu trúc/link/ownership được ghi ở [validation](validation-260930-0905-plan-integrity.md); không gọi cook, không coi static checks là behavioral evidence.
- Cổng duyệt 11 findings đã đóng. Runtime, corpus có quyền dùng, money budget, reviewer và venue cụ thể vẫn là gates trước triển khai hoặc trước mỗi task, không buộc chốt một venue cho toàn kit hay hỏi lại approval đã có.
