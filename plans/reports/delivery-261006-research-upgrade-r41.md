# Bàn giao research upgrade r41

Status: experimental-delivered; phạm vi cook hoàn tất, các gate scientific/native/owner/provider/stable/public giữ riêng.

## Candidate và kiểm tra thực

| Hạng mục | Kết quả |
|---|---|
| Source | r41, 337 pins; canonical SHA-256 `114e57918889a52474b514c09443a2afd1999e2dd11990a099d5b8069a9267d5` |
| Identity/cases | 43 identities, 172 base IDs; 19 required families; historical 148/224 và writer 256+20 được giữ |
| Resources | 13 groups, 35 consumer bindings; bốn authored packs chứa 14 records; public contract ON |
| Deterministic | 311 tests hoàn tất trong 914.791 giây: 310 pass, 1 skip với lý do ghi trong receipt; exit 0 trên hash hiện tại |
| Fresh packages | 16 bundles: bốn host × standalone/plugin × ON/internal OFF; tám bundle ON để bàn giao |
| Relocation | 420 actual isolated resource reads; 8 isolated research checker runs; OFF no-read |
| Installer | Eight explicit-package read-only previews; source/target user bytes preserved |
| Preservation | 590 protected hashes, zero mismatch; original format1/2 bundles verify unchanged; owned external temp removed |

Chi tiết và exact artifact hashes ở [candidate](../runs/nckh-upgrade-261006-0850-attempt-01/experimental-candidate.json), [local gates](../runs/nckh-upgrade-261006-0850-attempt-01/p7-local-gates.json), [deterministic](../runs/nckh-upgrade-261006-0850-attempt-01/p7-deterministic-attempt-02.json), [extracted qualification](../runs/nckh-upgrade-261006-0850-attempt-01/p7-extracted-qualification.json), [preservation](../runs/nckh-upgrade-261006-0850-attempt-01/p7-final-preservation.json) và [migration inventory](../runs/nckh-upgrade-261006-0850-attempt-01/migration-inventory-v2.json).

## Research chain và pilot

Bốn owner mới: dataset, statistics, telemetry, AIOps; method/cook/devops giữ design/lifecycle/environment. Read-only checker bind actual data/split/rights/code/config/environment/attempt outputs; không thực thi manifest argv. Review sửa exact run-output binding, denominator/no-gold/corpus policies, simulation freeze và distinct retry routes.

Pilot dùng snapshot dân số Việt Nam từ World Bank: 26 observations trong giai đoạn 2000–2025; train 20 / validation 3 / test 3. Tiến trình gốc PID 31900 exit 0, tạo sáu predictions từ hai baseline naive/drift đã cố định; các giá trị được đối chiếu độc lập bằng Fraction. Mean drift-minus-naive absolute-error contrast mô tả là `-270039.7598265261`. Tiến trình bổ sung PID 23416 exit 0, báo cáo mọi partition với 52 outcomes: 49 completed và 3 explicit unknown; sáu giá trị test gốc giữ nguyên. Independent_n = 1; chuỗi phụ thuộc được phân tích hồi cứu, source units để trống, prior access và giới hạn vintage/availability được giữ. Không có claim CI/p-value, causal/generalization/blind efficacy hoặc incident RCA. [Pilot readout](../runs/nckh-upgrade-261006-0850-attempt-01/pilot-readout.md), [partition supplement](../runs/nckh-upgrade-261006-0850-attempt-01/partition-supplement-output.json) và [paperwrite handoff](../runs/nckh-upgrade-261006-0850-attempt-01/paperwrite-evidence-handoff-v2.json).

## Native và pending gates

[Quick genuine Codex hooks check](verification-261006-0850-quick-native-hooks.md) theo chỉ đạo user quan sát advisory callback `{}` / exit 0 và sandbox chặn benign mutation. Đây là bounded check trước upgrade; full qualification của plan cũ 44/45 vẫn riêng. Mười hai supplemental domain routes là static expected declarations, chưa có observed semantic routing. Human/owner/scientific/full-native/provider/stable/public và real install/migration chưa được cấp verdict từ delivery này. CPU/peak memory/provider cost unknown, provider unused.

## Failures, repair và cleanup

Original failed attempts/counsel được giữ. First r39 pinned78 run có2fails2errors: stale36/13 counts, missing fixture catalog và bytecode writes. [Counsel](counsel-261006-pinned-regression-failure.md), eight focused tests và114domain tests đóng sửa trước corrective r40 freeze. Public deterministic runner trên r40 bị ngắt ở900giây, verdict timeout-unknown; focused diagnostic xác nhận exact Core count16≠12. [Timeout counsel](counsel-261006-deterministic-timeout.md) và independent source review cho phép chỉ sửa expected count16, giữ qualification/preservation/empty-index assertions. Full/package descendants hiện tại dùng r41 hashes. Full discovery suite chạy qua task-local observable Popen command với verbose output, không exclusions hoặc deadline900giây; public runner được giữ nguyên, timeout cũ không bị ghi đè. Validator/rights/post-smoke checks không bị nới. [Integration review](review-261006-research-integration-p7.md) và [experiment re-review](review-261006-experiment-graph-and-pilot.md) giữ lịch sử findings và source fingerprints.

Actual owned child handles đều reaped; không background server/port/provider/cluster. Archive/extract tại owned host temp ngoài workspace, separate CWD, Python isolated và PYTHONPATH unset; receipt/hashes được giữ trước exact unchanged-owned cleanup. Installed source/ownership và archived publication verifier không đổi. Local-package-only experimental candidate; không publish hoặc upgrade global install.
