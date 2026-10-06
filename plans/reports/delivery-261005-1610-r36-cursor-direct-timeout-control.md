# R36 Cursor direct preToolUse20s Read control, attempt13

[Verified bindings](./delivery-261005-1610-r36-cursor-direct-timeout-control.json) ghi một prompt/một model turn, cùng CLI `2026.09.15-d2fe57e`, exact Grok4.7/500k/xhigh/fast=false, synthetic Read path và packaged runner của [failure12](./delivery-261005-1550-r36-cursor-direct-failure-observer.md). Chỉ `preToolUse` timing bound đổi5s→20s; bốn packaged events khác5s và failure logger10s. Controller task identity/receipt namespace đổi cho isolation, source default r36 không đổi trong control.

Four case policy receipts gồm advisory/preflight/pre-delivery/stop, thêm một startup advisory. Neutral-event hashes khớp Read ở preflight/allow và postToolUse/pre-delivery/pending; zero native failure receipts và final marker được quan sát. Fixture byte-identical trước/sau. Đây là direct20s Read pre/post observation; raw tool-return content và native tool-use ID không được giữ, artifact QA vẫn pending.

Control không qualify mutation, private-path prevention, every-event timing, scheduling/process overhead hoặc full matrix. Failure12 vẫn actual5s timeout; các ca cũ thiếu native failure response vẫn giữ limitation. Terminal chunk13 không truncated.

Cleanup gỡ26 matching members, giữ582 historical members, zero final matching/zero tracked-live processes; graceful128/identity-verified force0 và harness1 được giữ. Protected global config hashes không đổi; CLI-owned hashes được ghi riêng, controller direct-write=false. Source r36/281 pins giữ nguyên. Full native task unchecked, plan44/45, owner samples/installed/release gates riêng.
