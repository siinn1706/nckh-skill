# Cursor r41 — preflight thiết kế

Status: INCOMPLETE cho native testing. Package static verification PASS; 43 skill và 35 resource bindings khớp r41. Chưa mở/chạy Cursor CLI hoặc IDE trong delivery này; native observed cases: 0. Planned: 247 behavioral scenarios/surface, 56 invocation cells/host, 64 writer native cells/host, resource/integration tracks riêng.

Xem [report findings dùng chung](test-261006-2210-r41-test-design.md), [suite receipt](../261006-2210-r41-shared-testcases/suite-validation.json) và [plan Cursor](../261006-2210-r41-cursor-full-skill-test/plan.md). Source local mismatch và duplicated base prompts được giữ trong report dùng chung, chưa phải Cursor behavior failure.

Native host version/model/discovery/precedence/hook reaction/cleanup chưa quan sát. Khi execution, tạo report mới `test-261006-2210-r41-cursor-<attempt>.md`, lưu raw trace trước chấm và giữ record này là preflight.
