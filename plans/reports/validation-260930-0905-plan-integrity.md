# Kiểm tra tính toàn vẹn bộ kế hoạch

Ngày 30/09/2026, Asia/Saigon; cập nhật sau khi người dùng duyệt 11 chỉnh sửa và bổ sung routing/hooks/subagents/standards/context budget. Phạm vi: tài liệu trong [kế hoạch năm phase](../260930-0905-vietnamese-research-skill-kit/plan.md), không kiểm thử một bộ skill đã triển khai.

## Kết quả kiểm tra trực tiếp

| Kiểm tra | Kết quả quan sát |
|---|---|
| `ak plan validate` với đường dẫn tuyệt đối, JSON/non-interactive | Exit 0, `valid: true`, không lỗi cấu trúc |
| `ak plan parse` | 5 phase, 57 task, 0 task/phase hoàn tất; plan `pending`, phase parser hiển thị `todo`; theo phase: 14/11/10/10/12 |
| Index sau biên tập | 90 dòng; chi tiết nằm trong phase files và hai design details được liên kết |
| Placeholder scaffold | Không còn `_TBD_`, Requirement A/B, Task A/B, Step 1/2 mẫu hoặc `_Define done_` trong tám file plan/detail |
| Liên kết cục bộ | Quét 76 inline local links trong 22 tài liệu dưới `plans/`, 0 hỏng; đây không phải kiểm uptime các URL web |
| Bảng Markdown | 0 hàng có số cột lệch trong 22 tài liệu |
| Quyền sở hữu đường dẫn CREATE | 61 file tương lai, 0 đường dẫn trùng quyền sở hữu, 0 file đã tồn tại, 0 path ra ngoài package root dự kiến |
| Module | 12 tên duy nhất: 2 entrypoint và 10 module chuyên môn, mỗi tên được phân một phase |
| Phạm vi ghi | Các thay đổi của task chỉ ở hồ sơ `plans/`; root hiện có `plans/` và blueprint gốc; `research-skill-kit/` chưa tồn tại |
| Blueprint gốc | SHA256 không đổi: `0E54218DBBB56B0C06A34B17854573C7DE8CBD7371321219945847F2A3811F8F` |
| ZIP gốc | SHA256 không đổi: `2AF342582DCC2F9053A94B63FE3EA854B6E367F9492D19C4BC21727F609EB441` |
| Nhật ký cục bộ | `ak journal validate`: exit 0, `ok: true`; không publish |

Các kiểm tra path ở đây xác nhận kế hoạch có ownership riêng, không xác nhận số lượng file đó là tối ưu hoặc mọi hợp đồng đã triển khai. Cross-phase references và các ranh giới lifecycle cần được phản biện riêng.

## Coverage theo yêu cầu

| Yêu cầu của người dùng | Owner trong plan |
|---|---|
| Văn phong/gu Việt | P3: `vi-writing`, `vi-taste`, corpus có quyền dùng, human review |
| Kiểm nguồn, giảm hallucination, Q1/Q2 | P1 contracts + P2 audit/policy + P5 fault suite |
| Nghiên cứu khoa học | P2 discovery, reader, reasoning; methodology/literature/gap modes |
| English scientific writing | P3 direct-EN/VI-to-EN, terminology và fidelity |
| Slide, ảnh và sơ đồ | P4 tách deck/chart/mechanism/artwork, native/source/render QA |
| Không lẫn venue | P1 profile + P2 policy + P5 isolation cases; lựa chọn theo task |
| Gọi AgentKit để giữ cập nhật | P1 resolution/adapter/receipt + P5 compatibility qualification |
| Chỉ dẫn skill bằng tiếng Anh | P1/P3 và index; ngôn ngữ output độc lập |
| Plan/cook như AgentKit | P1 có hai entrypoint và authorization/resume contract |
| Không cần tag/gọi từng skill | P1 live-catalog route, no-tag automatic selection; tag sai/không khả dụng là conflict riêng |
| Hooks và subagents | P1 actual host bindings, permission intersection, timeout reconciliation; P5 failure tests |
| Context 20k–40k / 10%–20% | P1 soft/hard formulas, per-context + shared pool, inherited/cached/idle context accounting; P5 cap/unknown cases |
| Tối ưu chi phí | Cost per accepted task với cùng scope/quality floor, all-attempt cost, coverage/unknown và verification reserve |
| Cô đọng official rules và lỗi AI | P2 rule cards theo scope/revision/exception; standards detail có 20 failure classes và negative controls |
| Chỉ lập kế hoạch lúc này | Tất cả phase pending; không package/provider/extension/install |

Các chức năng blueprint như polishing, fact-check/citation/claim audit, comparison/methodology/argument, terminology, literary studies và final review được map thành module/chế độ/đầu ra/test trong [standards và coverage](../260930-0905-vietnamese-research-skill-kit/standards-and-failure-catalog.md), không mất đi vì giảm số entrypoint. [Routing/context/cost detail](../260930-0905-vietnamese-research-skill-kit/design-routing-hooks-cost.md) là hợp đồng thiết kế, chưa phải runtime đo được.

## Kiểm tra nguồn và giới hạn

Controller đã đọc các báo cáo nguồn và đối chiếu lại trực tiếp những điểm chịu lực: K-Dense scientific-writing/citation-management, nhánh default image/PDF và PowerPoint của scientific-slides, Orchestra presenting-conference-talks, Apache-2.0 của nature ở revision ghim, điều khoản PPTX của Anthropic, quy tắc license theo skill của OpenAI, cùng help thực tế của `ak skills`/`ak orchestrate`. Hai researcher kiểm phần nguồn được giao; không dùng tên repo hay số stars làm bằng chứng chất lượng.

Nguồn remote branch `main` chưa có commit/hash đầy đủ vẫn là snapshot theo ngày, không đủ để copy/install. Những official policy không truy cập được vẫn pending. Không gọi provider thử nghiệm, không chạy build script trong ZIP, không tạo ảnh/slide, không benchmark văn phong hay khoa học.

Lượt bổ sung đã kiểm các phần chịu lực của nguồn vendor về hooks/subagents/usage và các nguồn official/university về evidence, reporting, writing. Xem [runtime research](researcher-260930-1706-hooks-agents-cost.md) và [official writing research](researcher-260930-1706-official-standards-writing.md). Local flags không chứng minh hook coverage hay runtime adapter đã chạy. `multi_agent_v2` là stable nhưng disabled; `token_budget`/`runtime_metrics` under development và disabled. Nature exact AI policy chưa resolve; không áp blanket ban/exception từ snippets hay editorial khác. Các writing heuristics không biến thành quy chuẩn tiếng Việt phổ quát.

## Tình trạng workflow

- File plan là authority cục bộ. CLI tạo file thành công nhưng global plan index báo access denied; không sửa hay reset cấu hình toàn cục. Validate/parse ở đường dẫn thật vẫn đọc được.
- Không tìm thấy tool task-management riêng trong catalog hiện tại; dùng checklist trong phase files. Agent-dispatch tools không phải task store và không phải arbitrary skill API.
- Không khởi chạy dev server/watcher/daemon cho task này; các researcher/reviewer được giao đã hoàn tất. Kiểm kê tiến trình bằng CIM ở lượt trước bị access denied; yêu cầu tăng quyền bị từ chối và không thử đường vòng. Không tuyên bố đã kiểm kê toàn máy.
- [Nhật ký cục bộ](../journals/2026-09-30-personal-research-skill-kit-plan.md) đã tạo; không publish AgentWiki.
- Red-team gồm ba góc nhìn đã hoàn tất. [Phân xử review](red-team-260930-0905-adjudication.md) giữ 11 đề xuất đã thu hẹp, loại 3 nhóm; người dùng đã duyệt và cả 11 đã áp dụng vào phase. Không hỏi lại approval này, cũng không suy nó thành quyền triển khai.

## Whole-Plan Consistency Sweep sau phê duyệt

- Đã đọc lại index, năm phase, hai design details, synthesis và adjudication; đối chiếu 11 finding cùng toàn bộ yêu cầu bổ sung. Không còn xung đột thiết kế chưa xử lý trong phạm vi đã rà soát.
- [Lượt reviewer riêng](review-260930-1713-plan-update-consistency.md) xác nhận coverage và nêu hai clarification, không đổi kiến trúc; đây vẫn là model review, không phải human acceptance hay bảo đảm độc lập nhận thức. Controller đã làm rõ trong design §1 rằng bỏ tag tự route, còn tag sai/không khả dụng mới báo conflict; P1 và P4 làm rõ lifecycle, local artifact status và aggregate `accepted-for-scope` là các trục khác nhau. Local `accepted`/`human-reviewed`/`handoff` không ghi đè mandatory fail/pending. Line citations trong report là snapshot trước hai chỉnh lý này.
- Kiểm lại công thức budget ở index/P1/design/P5: soft `min(20k, 10% W)`, hard `min(40k, 20% W)`; pool neo theo controller và mọi worker còn giữ context vẫn tính; từng context còn phải thỏa cap riêng. Không báo compliance/savings khi window hoặc telemetry unknown.
- Kiểm hook semantics theo đúng host: advisory hook không thành enforcement; hosted tools/continuation không được coi đã nằm trong matcher chỉ từ tên event. Không thêm API gọi skill, automatic installation hay provider authority.
- Năm phase và 57 checklist items tiếp tục pending. Đây là bàn giao hoàn tất **tài liệu lập kế hoạch**; nghiệm thu runtime, quyền sample, reviewer, ngân sách tiền/provider và venue theo task chưa được thực hiện.

## Phân biệt mức bằng chứng

`valid: true` chỉ là cấu trúc plan hợp lệ. Kiểm tra liên kết, số task và hash không chứng minh wrapper hoạt động, không chứng minh giảm ảo giác, English instructions tốt hơn, gu Việt đúng ý người dùng hay slide thực sự editable. Các kết quả đó đều chờ thực thi có quyền và nghiệm thu sau này.
