# Cursor r37 — uncovered search admission failure

CLI `2026.09.15-d2fe57e` từ chối explicit `--model grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]`, in available-model aliases và thoát1 trước khi prompt được chọn/gửi. **Zero model turns, zero prompt submissions, zero native callbacks/policy receipts**. Tool-search oracle chưa chạy; original collected status `native-uncovered-search-unqualified` được giữ. Không đổi kết quả của các lượt Grok được granted trước đó.

Root capture thất bại vì CLI đã thoát, không có PID được bịa. Controller vẫn thử prompt selection rồi nhận missing ownership record; không tạo prompt-intent và không gửi prompt. Một audit call khác từ chối ghi đè preflight đã tồn tại. Các lỗi này được giữ trong [controller failure record](../runs/nckh-native-261005-2004-r37-cursor-uncovered-search-attempt-23/admission-controller-failure.json); dependent actions của lượt sau phải dừng ngay khi bước prerequisite lỗi.

Cleanup gỡ27 matching owned members gồm fixture, giữ763 historical members/protected global configs; final audit có zero selected-project/process matches. Native root không kịp captured nên tracked count không được trình bày như một captured-tree proof.36 Illustrator startup candidates trong audit đều có creation trước lượt này, không khớp root-owned retained identities; không dừng process chưa xác định owner.

Installed CLI help có bracket-override example dùng key `effort`; successful runtime observations trước đó có native model `grok-4.7-xhigh`. Current selectedModel vẫn là Grok4.7/context500k/reasoning_effortxhigh/fastfalse. Những dữ kiện này hướng tới kiểm tra selection route trước lượt tiếp theo; không tự đổi model/effort/context hoặc claim một syntax đã chạy được. Source kit r37/plan44/45/full gate unchecked giữ nguyên.

## Evidence

- [Verified admission summary](../runs/nckh-native-261005-2004-r37-cursor-uncovered-search-attempt-23/native-admission-summary.json)
- Native rejection/exit1 (historical evidence path: `../runs/nckh-native-261005-2004-r37-cursor-uncovered-search-attempt-23/terminal-ready-01.json`; unavailable in the cleaned checkout)
- [Original unqualified case](../runs/nckh-native-261005-2004-r37-cursor-uncovered-search-attempt-23/case-uncovered-search.json)
- [Cleanup](../runs/nckh-native-261005-2004-r37-cursor-uncovered-search-attempt-23/cleanup.json) và [process audit](../runs/nckh-native-261005-2004-r37-cursor-uncovered-search-attempt-23/final-process-audit.json)
- [Startup identity correlation](../runs/nckh-native-261005-2004-r37-cursor-uncovered-search-attempt-23/startup-process-ownership-correlation.json)
