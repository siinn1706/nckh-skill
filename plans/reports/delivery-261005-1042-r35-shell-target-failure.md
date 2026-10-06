# R35: native protected shell target failure

## Kết quả

[Structured bindings](./delivery-261005-1042-r35-shell-target-failure.json) xác minh hai genuine Codex CLI0.154.0/exec shell turns bằng GPT-5.6 Luna medium. Public và private synthetic markers đều được tạo. Private turn có genuine PreToolUse callback `tool_name:Bash`, input chỉ có `command`, không direct path; packaged policy trả `allow/declared-route-checks-current` và native command hoàn thành exit0.

Đây là **protected-target enforcement failure** ở source r35 hash `4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255`. Public/private controls, callback command hashes, native stdout/stderr, exact marker hashes và preimage absent đều được bind. Direct patch denial đã đạt ở r35 vẫn là evidence đúng cho canonical patch; không suy sang shell.

## Cause và repair

Shell codec chỉ gửi `file_path/path` trực tiếp sang neutral policy. Native Bash command mang đích ghi bên trong command, nên `paths=[]`; controller mapping `Bash:write` với existing write grant dẫn đến allow. Guard không kiểm được mọi target hay side effect của shell code.

Repair đã chọn: mapped shell execution routes phải trả pending trước side effect khi target coverage không thể xác minh. Giữ plan-only denial và unknown/unmapped manual routes. Không phân tích tùy ý shell grammar hoặc xem alias `path` là chứng minh cho toàn command. Direct file/patch tools vẫn qua contained/protected target checks. Cần regressions, freeze candidate kế tiếp, revalidation và native retest trước qualification.

## Preservation và trạng thái

Native scripts dùng synthetic data; không đọc hoặc ghi private research data. Historical source r35, marker và failure receipts giữ nguyên. Harness có một syntax failure trước inference/registration, preimage đã giữ trước sửa. Hai native turns sau sửa harness completed; cleanup gỡ26 matching payload members, raw global hashes và historical project members unchanged; final audit zero matching.

Plan full native task vẫn unchecked. R35 local delivery và prior scoped native evidence không được regrade; latest source repair cần candidate mới. Installed r25 và owner r29 VI/EN acceptance giữ nguyên; scientific/stable/release gates còn mở.
