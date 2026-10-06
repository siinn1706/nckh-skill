---
title: "Phase 6: Installer and recovery"
status: in-progress
---

# Phase 6: Installer, update và recovery

<!-- Updated 2026-10-01: shared engine approved; separate Codex project-copy installation grant received and executed. -->

## Overview

Priority P1. Shared engine và hai entry scripts đã triển khai theo [cook --auto được duyệt](plan.md), depends on P5 manifests. Effort ban đầu 4–6 ngày. Windows fixtures và PowerShell forwarding đã kiểm tra. Codex project-copy installation đã được duyệt riêng và thực hiện; actual native consumption, POSIX/macOS/Linux và symlink vẫn unverified. Python 3.11+ không được tự download/install.

## Context Links

- [Installer wizard/transactions](installer-evaluation-migration.md), [runtime paths](runtime-compatibility.md).
- [Architecture](architecture.md), [model profile policy](workflow-and-model-routing.md).

## Key Insights / Architecture

Install is an owned transaction, not recursive copy. Config merge sở hữu từng key/path; backup trước write, journal trước từng stage, compare commit hash trước rollback. Multiple runtimes có thể discover một shared skill root; ownership references ngăn uninstall phá consumer khác.

## Requirements

- Detect and ask runtime/surface, Core/Engineer/Marketing, project/global, copy/symlink, five model profiles and final transaction review.
- Dry-run deterministic diff, non-interactive explicit choices, no silent overwrite, no automatic privilege elevation or hook trust bypass.
- Install/update/doctor/config-models/list-skills/uninstall available through entry scripts/engine; `nckh` CLI shim optional, no service/updater daemon.
- Idempotent no-op; user-edited files/conflicting keys require keep/merge/explicit replace. Preserve unrelated runtime config and original permissions.
- Crash/concurrency/partial commit recoverable; uninstall only owned+unchanged paths and shared references. No broad delete.
- Read-only doctor no paid prompt/no autorepair; native smoke separate opt-in with cost/permission gate.

## File ownership — Create after P5

| Absolute path / bounded subtree | Files/content owned |
|---|---|
| `C:/Users/USER/Downloads/test-skill/nckh-kit/installer/install.ps1` | Windows entry, detect prerequisites, gather/forward choices. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/installer/install.sh` | POSIX entry with same operation contract. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/installer/nckh-installer.py` | Shared deterministic operations, paths/locks/backup/journal/recovery. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/installer/schemas/` | Transaction/install ownership/model config/diagnostic output schemas. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/installer/manifests/` | Versioned package manifests; no user's actual install secrets/state. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/tests/installer/` | Isolated temporary-home/filesystem transaction and OS tests. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/evals/cases/installer/` | Wizard/host visibility/recovery acceptance protocols. |
| `C:/Users/USER/Downloads/test-skill/nckh-kit/docs/installation.md` | Actual setup/help/prerequisites, update/rollback/uninstall and conflict UX. |

Actual global runtime destinations remain out of repo; modify only under separately authorized install with preview. Builder/dist owned by P5. No baseline deletion.

## Implementation Steps

1. Lock public operation/help/exit/error contracts and six-choice UX; freeze OS/host/surface support cells with actual lab owners. Print Python prerequisite before write; instruction-only use does not gain that dependency.
2. Write negative tests for unresolved root, traversal/junction/symlink escape, case-fold/namespace collision, denied permissions, Unicode/spaces and same target via two aliases.
3. Implement engine dry-run/discovery first, then stage/backup/commit/verify/rollback with local install journal and owned manifest.
4. Implement idempotency, shared visibility/owners/neutral-vs-host-specific projections, plugin lifecycle fields, stale lock recovery without killing others, concurrency serialization, update conflict and user-edit preservation. Enumerate Cursor compatibility/nested roots as well as direct targets.
5. Implement entry scripts and model setup. Unsupported per-agent controls show limitation; never claim saving a config string applied it to runtime.
6. Validate on Windows/macOS/Linux authorized isolated fixtures for copy and supported symlink cells, project/global target maps. Unit fake-home paths are installer inputs, not proof actual runtime reads files.
7. Authorized user-scope smoke only after preview; test complete uninstall/rollback against pre-install hash snapshots. Update local docs to match real help; không xuất bản ra ngoài.

## Todo

- [x] Lock wizard, operation and prerequisite contracts.
- [x] Write failure/recovery tests before mutating implementation.
- [x] Implement shared engine and two thin entrypoints.
- [x] Test idempotency/conflict/crash/concurrency/rollback/uninstall.
- [ ] Run OS/native acceptance when permitted and preserve all open gates.

[Project installation record](../reports/installation-261001-1813-codex-project-candidate.md) có actual installed/doctor receipts và post-install preview: 43 current/unchanged, zero conflict. Chưa chạy giao dịch update/rollback/uninstall trên project thật hoặc xác nhận native consumption; task nghiệm thu đầy đủ vẫn unchecked.

## Success Criteria

- Two shells produce same operation plan/manifest results; no duplicated catalog/business logic.
- Same install rerun causes no content/config drift; edited file preserved and reported, not overwritten.
- Interrupted transaction resumes or restores only owned unchanged changes; hash mismatch after commit becomes conflict.
- Shared target survives uninstall while another runtime/kit owns it; no deleting host roots, credentials or user plans.
- Python absence/unsupported symlink/unverified model config fail clearly. All advertised OS/runtime cells have actual evidence, not inferred from one Windows run.

## Validation commands và evidence scope

Working directory: `C:/Users/USER/Downloads/test-skill/nckh-kit/`.

`python -m unittest discover -s tests/installer -p "test_*.py"`

Narrow first: dry-run/path safety, then recovery/update/uninstall. Local receipt (historical evidence path: `../../nckh-kit/evals/results/local-checks.json`; unavailable in the cleaned checkout) có Windows fixture/PowerShell checks. [Installer/OS protocol](../../nckh-kit/evals/cases/installer/acceptance.json) giữ native/OS cells chưa chạy. Crash recovery hỗ trợ rollback rồi fresh preview; không replay staged writes. POSIX shell chưa có acceptance receipt.

## Risk / Security / Rollback

Installer có data-loss risk cao: read-only preflight resolve final absolute destinations and user-owned paths. No `curl | sh`, no automatic elevation, no credential inspection to guess subscription. Preserve private backup permissions and keep backups out of dist/reports. Rollback same transaction only; user changes after commit require confirmation. Stop and report recovery path if exact ownership cannot be established.

## Next Steps

P7 consumes transaction receipts and exact supported cells. Automatic global deployment/publishing không nằm trong acceptance; user gọi install là authorization riêng với setup proposal.
