# Đọc skill trong project: hai probe thực trên r14

Ngày 03/10/2026, Asia/Saigon. Project duy nhất: `C:/Users/USER/Downloads/test-skill`.

## Kết quả quan sát

| Ứng dụng | Model được yêu cầu và label UI quan sát | Subject | Đầu ra thực |
|---|---|---|---|
| Cursor Agents, This PC | Grok 4.7 Extra High | Installed revision 14 | [Báo cáo](../evaluation/personal-use/native/cursor-grok-neutral-r14.md) |
| Antigravity, Local | Gemini 3.8 Flash High | Installed revision 14 | [Báo cáo](../evaluation/personal-use/native/agy-neutral-r14.md) |

Cả hai được yêu cầu tự tìm `nckh-analytics` trong project, đọc required contracts
và dùng snapshot World Bank thực. Input không cung cấp đường dẫn tới `SKILL.md`.
UI hiển thị việc đọc skill/contracts/source; artifact thực ghi đường dẫn
`.agents/skills/nckh-analytics/SKILL.md`. Đây là bằng chứng đọc trực tiếp neutral
root cho một skill ở subject r14, không chứng minh toàn bộ discovery/mode/agent
cells hoặc candidate mới.

Controller tính lại từ snapshot: 26 quan sát, 26 non-null, 2000=`77154011`,
2025=`101598527`, delta=`24444516`, tăng khoảng `31.68275464%`. Cả hai artifact
giữ unit trống và giới hạn suy luận nhân quả. [Content review](../evaluation/personal-use/native/neutral-r14-content-review.json)
ghim input/output hashes và giới hạn của kiểm tra.

Prompt và observations được giữ:

- Cursor prompt (historical evidence path: `../evaluation/personal-use/native/cursor-grok-neutral-r14-prompt.txt`; unavailable in the cleaned checkout),
  [final transcript](../evaluation/personal-use/native/cursor-grok-neutral-r14-observed-final.json).
- Antigravity prompt (historical evidence path: `../evaluation/personal-use/native/agy-neutral-r14-prompt.txt`; unavailable in the cleaned checkout),
  [final transcript](../evaluation/personal-use/native/agy-neutral-r14-observed-final.json).

Không test model Cursor nào khác và không fallback. UI label được lưu riêng với
effective model/effort; chưa có provider telemetry để xác nhận effective fields.
Model tự nhận trong artifact không được dùng làm telemetry. Owner chưa chấm.

## Route cài đặt

[Installer scout](review-261003-install-route.md) xác nhận thêm bản riêng vào
`.cursor/skills` bị guard chặn vì trùng `.agents/skills`. Không tạo bản trùng.
Hai observations trên xác minh một route dùng trực tiếp root hiện có. Candidate
mới vẫn phải build, update Codex với ownership/candidate guards và được đọc lại
trong các môi trường đã chọn.

## Sự cố công cụ và cleanup

Automatic approval review từ chối inventory toàn bộ cửa sổ vì có thể lộ metadata
ứng dụng ngoài phạm vi. Controller dùng lại đúng hai window đã được xác định;
không còn blocker inventory và không yêu cầu user mở rộng phạm vi.

Click khi không có screenshot geometry fail trước dispatch; đã reobserve target,
activate đúng cửa sổ và kiểm focus trước typing. Lúc Cursor bị minimize/user focus
đổi, controller reobserve trước tiếp tục. Không điều khiển ChatGPT desktop UI,
authentication/security dialog hoặc terminal UI.

Hai owned proxy PID lịch sử đã absent trong [process reconciliation](../evaluation/personal-use/process-reconciliation-03.json).
Foreground apps của user được giữ nguyên. Các probe là tác vụ trong app, không
tạo daemon/watchers hay sửa model/global settings.
