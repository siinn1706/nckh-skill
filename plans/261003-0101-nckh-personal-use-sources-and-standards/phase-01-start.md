---
title: "Phase 1: Nguồn và phạm vi"
status: completed
---

# 1. Nguồn và phạm vi

## Requirements

Đọc [hợp đồng](../reports/brainstorm-261003-personal-use-contract.md), [nguồn](../reports/researcher-261003-real-sources.md), [tiêu chí](../reports/researcher-261003-official-acceptance.md) và [scout](../reports/scout-261003-project-runtime.md). Giữ 37 identity, project boundary và nguồn có consumer.

## Todo

- [x] Xác minh r22, installation r14, catalog và owner code/schema/installer.
- [x] Ghi quyết định owner tự chấm và @ChatGPT là ứng dụng local hiện tại.
- [x] Nghiên cứu nguồn primary/official; giữ giới hạn domain/venue/jurisdiction/vendor.
- [x] Kiểm JSON source map đúng 37 identity, references resolve, không universal percentage.
- [x] Kiểm toàn plan: links, ownership, dependencies, checks, rollback; cập nhật project index.

Bằng chứng: [validation](../reports/validation-261003-personal-use-plan.md). Source definitions được đưa vào package ở phase 3; native evidence vẫn mở ở phase 4.

## Implementation Steps

Controller sở hữu plan/integration/runtime. Sources researcher chỉ sở hữu staging acquisition/report. Acceptance worker sở hữu policy/profile/checks riêng. Resource worker sở hữu resource schema/registry/reader/tests riêng. Không ghi global config, publish hoặc commit.

## Validation, risk and rollback

Kiểm source IDs/catalog bằng dữ liệu thực và đọc mọi phase. ak plan validate chỉ kiểm cấu trúc. Tool model metadata là discovery input; phải giữ actual run evidence. Không thêm routine approval gate cho cook đã được giao. Giữ historical receipts, sửa plan theo evidence; task thiếu bằng chứng vẫn mở.
