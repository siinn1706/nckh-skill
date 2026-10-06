# Review plan completion and strongest kit state

Ngày kiểm tra: 06/10/2026, Asia/Saigon.

## Kết luận

Chưa hoàn thành tất cả plan. Ba plan hiện hành còn tổng cộng chín Todo trong các phase. Điều kiện của người dùng “nếu ổn hết rồi” chưa đạt, nên review này không đổi source, cấu hình hook thật, package hoặc GitHub sang một trạng thái mạnh nhất. Việc cho phép dùng thêm skill không tự đóng các acceptance gate.

## Trạng thái từng plan

Số task dưới đây được đếm trực tiếp từ checkbox trong các file `phase-*.md`, không tính lặp lại acceptance checkbox ở index.

| Plan | Task hoàn tất | Kết luận |
|---|---:|---|
| [Vietnamese research skill kit](../260930-0905-vietnamese-research-skill-kit/plan.md) | 0/57 checkbox phase | SUPERSEDED; hồ sơ lịch sử, không đưa vào backlog hiện hành. |
| [Portable skill kit](../260930-1910-nckh-portable-skill-kit/plan.md) | 30/36 | In-progress; sáu Todo behavioral/native/human/OS/protocol acceptance còn mở. |
| [Resource quality](../261002-0832-nckh-skill-resource-quality/plan.md) | 27/29 | In-progress; matched behavioral/human qualification và các đầu vào tương ứng chưa hoàn tất. |
| [Personal use](../261003-0101-nckh-personal-use-sources-and-standards/plan.md) | 26/26 | Completed trong phạm vi bàn giao personal-use; không thay scientific/stable qualification. Owner scoring sau dùng giữ pending. |
| [Research data, hooks, writing](../261004-0047-nckh-research-data-hooks-writing/plan.md) | 44/45 | In-progress; full native hooks gate chưa hoàn tất. |
| [DevOps/AIOps research upgrade](../261005-0036-nckh-devops-aiops-research-upgrade/plan.md) | 39/39 | Completed trong phạm vi implementation/local experimental delivery r41; semantic/native/scientific/owner/public/real-install gates giữ riêng. |
| [Default advisory hooks](../261006-0758-default-advisory-hooks/plan.md) | Không có phase checkbox | Complete trong phạm vi default advisory installation và publication r38. |

## Findings và vướng mắc

### P1 — Chưa đủ bằng chứng để mặc định enforcement cho tất cả hooks

Native hooks plan còn một task chưa được đóng. Các quan sát thực giữ những giới hạn cụ thể:

- [Cursor duplicate attempt](delivery-261006-0240-r37-cursor-workspace-duplicates.md): frozen oracle failed; thiếu callback plugin `beforeSubmitPrompt`/`stop`, extra Read tạo số receipt khác oracle. Không regrade sau chạy.
- [Cursor PostToolUse](delivery-261006-0453-r37-cursor-posttool-lf-controls.md): timeout khai báo 5 giây nhưng callback hoàn tất sau 8.263741 giây; chưa chứng minh effective native deadline.
- [Codex Stop](delivery-261006-0320-r37-codex-stop-controls.md): codec trả `{}` cho advisory và block; quan sát chưa chứng minh native enforcement tại Stop.
- Claude model/effort/native turns, các host/tool/surface còn thiếu và quyền cache/metadata Codex ngoài workspace giữ pending theo plan hiện hành.

Các finding này không phủ định những allow/block observations đã đạt trên route cụ thể. Chúng ngăn kết luận mọi hook trên bốn host đã có enforcement đầy đủ. `configure-hooks.py` tiếp tục yêu cầu native evidence khi dùng enforce; không xóa gate để đạt cấu hình mong muốn.

### P2 — Public deterministic entrypoint còn timeout cố định 900 giây

[run-evals.py](../../nckh-kit/evals/run-evals.py) dòng 55 dùng `subprocess.run(..., timeout=900)` cho toàn bộ discovery suite. [Delivery r41](delivery-261006-research-upgrade-r41.md) ghi một lần public runner timeout trên r40; suite đầy đủ r41 hoàn tất trong 914.791 giây qua task-local observable wrapper. Vì vậy public command có thể timeout trước khi suite hiện tại hoàn tất trên máy này. Đây là lỗi/giới hạn operational còn thật; không được suy rằng local suite pass đã sửa public entrypoint. Review này không sửa runner do quyền thay đổi được người dùng đặt sau điều kiện toàn bộ review đạt.

### P2 — Chưa có contract chỉ một trạng thái

Source hiện cho phép `--resource-access on|off`, installer `--hooks advisory|off`, configurator `--mode advisory|enforce`; agents vẫn là lựa chọn `--with-agents`. Public verifier r38 bắt buộc resources ON và install default advisory nhưng yêu cầu payload ở trạng thái packaged-inactive, không được tự khai enabled/registered/trusted. OFF comparison là quyền lịch sử cho internal evaluation; yêu cầu mới của người dùng về một trạng thái là thay đổi contract cần áp dụng đồng bộ sau khi điều kiện review đạt.

Không dùng model/effort cao hơn, host trust hoặc quyền tool làm cách mặc định để giải quyết thiếu native evidence. Các quyền đó thuộc host và từng công việc, không phải một cờ kit.

### P2 — Current source, publication và live installation chưa đồng bộ

Current source r41 có 43 skills, 13 resource groups và 35 consumer bindings. GitHub hiện là r38 với 39 skills, 9 groups và 27 bindings. Đây là hai revision khác nhau; public verifier r38 không chứng nhận r41.

Kiểm tra hiện tại không thấy `.claude/settings.local.json`, `.codex/hooks.json`, `.cursor/hooks.json`, `.agents/hooks.json` hoặc `.nckh-state/hooks/ownership.json` trong project. Default advisory của installer không chứng minh hooks đang được đăng ký/chạy trong project. Không có live activation hoặc installation mới trong review này.

### Acceptance còn mở

Portable/resource-quality giữ matched agent behavior, actual host/surface/model/OS, quyền sample, reviewer/threshold, protected holdout và cost/provider scopes chưa đủ bằng chứng. Personal-use lane không đòi external reviewer/protected holdout; việc bàn giao lane này hoàn tất không thay qualification rộng hơn. Không gọi synthetic development hoặc hashing là human/scientific acceptance.

## Kiểm chứng trong lần review này

- `--validate-only` pass trên source hiện tại: r41, 337 pins, 43 identities, 172 base cases, 19 families. Canonical lock hash `114e57918889a52474b514c09443a2afd1999e2dd11990a099d5b8069a9267d5`. [Receipt mới](review-261006-1554-current-structure.json) giữ đầy đủ pending states.
- 38 focused tests của runner/config/policy/adapter/installer pass trong 84.585 giây, exit 0.
- Public verifier chạy lại pass cho bốn package r38, resources ON và hook install default advisory; payload packaged-inactive.
- GitHub remote `main` kiểm tra chỉ đọc khớp local HEAD `d449288970ada6c9749579ede4878f66485aeae4`. Publication checkout sạch ở thời điểm kiểm tra. Lần truy cập đầu bị proxy sandbox chặn; lần đọc được phép sau đó thành công.
- Full 311-case suite không chạy lại: receipt r41 ghi 310 pass, một Windows symlink skip và zero failure/error. Kiểm tra binding và persistent bundles được lưu trong [evidence reconciliation](review-261006-1554-evidence-reconciliation.json); đây là kiểm tra bằng chứng hiện có, không phải một native/human run mới.

## Điều kiện còn thiếu để thực hiện nhánh cấu hình mạnh nhất

1. Đóng các native findings/cells còn mở theo đúng host/version/surface/event, giữ failure history và quyền hiện có.
2. Hoàn tất hoặc nhận quyết định scope rõ ràng cho các acceptance task còn mở của portable/resource-quality; không tự đổi chúng thành pass.
3. Giải quyết public deterministic runner timeout trước khi gọi đường kiểm tra tiêu chuẩn là đạt đầy đủ.
4. Khi đủ điều kiện, cập nhật một owner cấu hình, installer/build/verifier/tests/docs và public export cùng revision; kiểm tra real installation riêng với package state và host trust.

Không có câu hỏi xin xác nhận mới trong review này. Các đầu vào/quyền pending đã có trong plan và được giữ đúng trạng thái.
